"""Offline capability proof, baked glTF round trip, and repeatable image evidence."""
import bpy, sys, json, hashlib, importlib.util, math
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('rigbuild',ROOT/'scripts/blender/build-shushu-production-rig-v001.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
OUT=b.OUT; RENDERS=OUT/'renders'
def load():
    bpy.ops.wm.open_mainfile(filepath=str(b.ASSET))
    rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
    meshes=sorted([o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')],key=lambda o:o.name)
    return rig,meshes
def import_saved(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path));j,_=b.read_glb(path)
    semantic={j['meshes'][n['mesh']]['name']:n['name'] for n in j['nodes'] if 'mesh' in n}
    for o in bpy.data.objects:
        if o.type=='MESH' and o.data.name in semantic:
            name=semantic[o.data.name];container=bpy.data.objects.get(name)
            if container is not None and container!=o:container.name='GLTF_NODE_'+name
            o.name=name
    assert any(o.name=='ShushuStatic_Torso' for o in bpy.data.objects),'Imported torso missing'
def positions(meshes):return {o.name:b.evaluated(o)[0] for o in meshes}
def stat(a):return {'max':float(np.max(a)),'mean':float(np.mean(a)),'p95':float(np.percentile(a,95))}
def texture_bytes(o):
    result=[]
    for m in o.data.materials:
        for n in m.node_tree.nodes:
            if n.type=='TEX_IMAGE' and n.image:
                im=n.image;raw=bytes(im.packed_file.data) if im.packed_file else Path(bpy.path.abspath(im.filepath)).read_bytes()
                result.append({'size':list(im.size),'sha256':hashlib.sha256(raw).hexdigest()})
    return result
def audit():
    sr,source=b.fresh();original={o.name:{'p':np.array([v.co for v in o.data.vertices]),'uv':np.array([v.uv for v in o.data.uv_layers.active.data]),'tri':np.array([list(p.vertices) for p in o.data.polygons]),'texture':texture_bytes(o)} for o in source}
    rig,meshes=load();b.reset(rig);neutral=positions(meshes);preservation=[];weights=[]
    for o in meshes:
        if o.name in original:
            a=original[o.name];p=np.array([v.co for v in o.data.vertices]);uv=np.array([v.uv for v in o.data.uv_layers.active.data]);tri=np.array([list(p.vertices) for p in o.data.polygons])
            preservation.append({'mesh':o.name,'vertex_count':len(p),'topology_equal':bool(np.array_equal(a['tri'],tri)),'uv_equal':bool(np.array_equal(a['uv'],uv)),'texture_bytes_equal':a['texture']==texture_bytes(o),'neutral_position_delta':stat(np.linalg.norm(p-a['p'],axis=1))})
        sums=np.array([sum(g.weight for g in v.groups) for v in o.data.vertices]);weights.append({'mesh':o.name,'sum_error':float(np.max(np.abs(sums-1))),'max_influences':max(len(v.groups) for v in o.data.vertices),'negative':sum(g.weight<0 for v in o.data.vertices for g in v.groups)})
    isolation=[]
    tests=[('head-yaw',{'HeadYaw':1},['Paw_L','Paw_R','Torso']),('head-pitch',{'HeadPitch':1},['Paw_L','Paw_R','Torso']),('neck',{'NeckPitch':1},['Paw_L','Paw_R','Torso']),('ear-L',{'Ear.L':1},['Paw_L','Paw_R','Torso','Head','Ear_R']),('ear-R',{'Ear.R':1},['Paw_L','Paw_R','Torso','Head','Ear_L']),('hand-L',{'Wrist.L':1},['Paw_R','Torso','Head']),('hand-R',{'Wrist.R':1},['Paw_L','Torso','Head']),('blink-L',{'Blink.L':1},['Paw_L','Paw_R','Torso','Eye_R']),('blink-R',{'Blink.R':1},['Paw_L','Paw_R','Torso','Eye_L']),('cheek-L',{'CheekPressure.L':1},['Paw_L','Paw_R','Torso','Eye_R']),('belly',{'BellyPressure':1},['Paw_L','Paw_R','Head'])]
    for name,values,quiet in tests:
        b.state(rig,values);p=positions(meshes);isolation.append({'test':name,'protected_displacement':{k:stat(np.linalg.norm(p['ShushuStatic_'+k]-neutral['ShushuStatic_'+k],axis=1)) for k in quiet},'active_displacement_max':max(float(np.linalg.norm(p[k]-neutral[k],axis=1).max()) for k in p)})
    for side in ['Left','Right']:
        for bone in ['Arm','ForeArm','Hand']:
            b.reset(rig);pb=rig.pose.bones[b.PREFIX+side+bone];pb.rotation_euler[0]=math.radians(15);rig.update_tag();bpy.context.view_layer.update();p=positions(meshes)
            isolation.append({'test':side+bone+'-FK15','protected_displacement':{k:stat(np.linalg.norm(p['ShushuStatic_'+k]-neutral['ShushuStatic_'+k],axis=1)) for k in ['Torso','Head','Paw_'+('R' if side=='Left' else 'L')]},'active_displacement_max':float(np.linalg.norm(p['ShushuStatic_Paw_'+('L' if side=='Left' else 'R')]-neutral['ShushuStatic_Paw_'+('L' if side=='Left' else 'R')],axis=1).max())})
    body_fk=[];torso=next(o for o in meshes if o.name.endswith('Torso'));rest=np.array([v.co for v in torso.data.vertices])
    for name in ['Spine','Spine1','Spine2','Hips','LeftUpLeg','RightUpLeg','LeftLeg','RightLeg','LeftFoot','RightFoot']:
        b.reset(rig);rig.pose.bones[b.PREFIX+name].rotation_euler[0]=math.radians(5);rig.update_tag();bpy.context.view_layer.update();p=positions(meshes);movement=np.linalg.norm(p['ShushuStatic_Torso']-neutral['ShushuStatic_Torso'],axis=1)
        body_fk.append({'bone':name,'FK_degrees':5,'torso_max_displacement':float(movement.max()),'torso_upper_z_over_037_displacement_max':float(movement[rest[:,2]>.37].max()),'head_displacement_max':float(np.linalg.norm(p['ShushuStatic_Head']-neutral['ShushuStatic_Head'],axis=1).max()),'interpretation':'Attached descendants follow parent transforms. Limb tests protect upper torso and head. Arbitrary unsupported FK is not a floor-contact PASS.'})
    foot_control=[]
    for side in ['L','R']:
        mask=(rest[:,0]>0 if side=='L' else rest[:,0]<0)&(rest[:,2]<.015);opposite=(rest[:,0]<0 if side=='L' else rest[:,0]>0)&(rest[:,2]<.015)
        for control in ['FootLift','FootSide','FootForward']:
            b.state(rig,{control+'.'+side:1});p=positions(meshes);movement=np.linalg.norm(p['ShushuStatic_Torso']-neutral['ShushuStatic_Torso'],axis=1)
            foot_control.append({'control':control+'.'+side,'active_sole_movement':float(movement[mask].max()),'opposite_sole_movement':float(movement[opposite].max()),'upper_torso_movement':float(movement[rest[:,2]>.37].max()),'head_movement':float(np.linalg.norm(p['ShushuStatic_Head']-neutral['ShushuStatic_Head'],axis=1).max())})
    torso=next(o for o in meshes if o.name.endswith('Torso'));rest=np.array([v.co for v in torso.data.vertices]);support=[]
    for shift in [-1,0,1]:
        for seat in np.linspace(0,1,201):
            b.state(rig,{'Seat':float(seat),'WeightShift':float(shift)});p,_=b.evaluated(torso)
            feet={}
            for side,s in [('L',1),('R',-1)]:
                mask=(rest[:,0]*s>0)&(rest[:,2]<.082);sole=(rest[:,0]*s>0)&(rest[:,2]<.015);feet[side]={'min_z':float(p[mask,2].min()),'near_floor_vertices':int((p[mask,2]<.001).sum()),'sole_xy_drift_max':float(np.linalg.norm(p[sole,:2]-rest[sole,:2],axis=1).max())}
            rump=(rest[:,1]>.08)&(rest[:,2]>.11)&(rest[:,2]<.24)&(np.abs(rest[:,0])<.15)
            support.append({'seat':float(seat),'shift':shift,'min_z':float(p[:,2].min()),'below_minus_001':int((p[:,2]<-.001).sum()),'feet':feet,'rump_min_z':float(p[rump,2].min()),'rump_near_floor_vertices':int((p[rump,2]<.004).sum()),'finite':bool(np.isfinite(p).all())})
    contacts=[]
    for side in ['L','R']:
        for mode in ['Offer','SelfContact','Hold']:
            for seat in [0,1]:
                b.state(rig,{mode+'.'+side:1,'Seat':seat});p,t=b.evaluated(torso);tree=BVHTree.FromPolygons(p.tolist(),t.tolist(),all_triangles=True)
                paw=next(o for o in meshes if o.name.endswith('Paw_'+side));pp,_=b.evaluated(paw);nearest=[tree.find_nearest(Vector(v)) for v in pp];ds=np.array([v[3] for v in nearest]);signed=np.array([(Vector(pp[i])-v[0]).dot(v[1]) for i,v in enumerate(nearest)])
                longname='Left' if side=='L' else 'Right';root=rig.data.bones[b.PREFIX+longname+'Shoulder'].head_local;hand=rig.data.bones[b.PREFIX+longname+'Hand'].head_local;axis=(hand-root).normalized();tip=((np.array([v.co for v in paw.data.vertices])-np.array(root))@np.array(axis))/(hand-root).length>.85
                contacts.append({'side':side,'mode':mode,'seat':seat,'surface_gap_min':float(ds.min()),'tip_gap_min':float(ds[tip].min()),'tip_signed_min':float(signed[tip].min()),'tip_penetration_vertices_over_002':int((signed[tip]<-.002).sum()),'root_inclusive_penetration_vertices_over_002':int((signed<-.002).sum()),'paw_min_z':float(pp[:,2].min()),'effector_target_gap':float((rig.pose.bones[b.PREFIX+longname+'Hand'].head-bpy.data.objects['CTRL_Paw.'+side].location).length)})
    eyes=[]
    for name,values in [('neutral',{}),('half',{'Blink.L':.5,'Blink.R':.5}),('closed',{'Blink.L':1,'Blink.R':1}),('wink-L',{'Blink.L':1}),('closed-tilt-gaze',{'HeadYaw':.83,'HeadRoll':.83,'Blink.L':1,'Blink.R':1,'GazeX.L':1,'GazeY.R':-1})]:
        b.state(rig,values);occluders=[]
        for obj in meshes:
            if obj.name.endswith(('Head','LidWall_L','LidWall_R','Nose','Ear_L','Ear_R')):
                p,t=b.evaluated(obj);occluders.append(BVHTree.FromPolygons(p.tolist(),t.tolist(),all_triangles=True))
        for side in ['L','R']:
            pp,_=b.evaluated(bpy.data.objects['ShushuStatic_Eye_'+side])
            for view,dir in VIEWS:
                d=Vector(dir).normalized();visible=0
                for q in pp:
                    origin=Vector(q)+d*3
                    blocked=any((hit:=tree.ray_cast(origin,-d,3.00001))[0] is not None and hit[3]<2.99998 for tree in occluders)
                    visible+=not blocked
                eyes.append({'state':name,'side':side,'view':view,'eye_surface_vertices_potentially_visible':visible,'test':'Head/lid/nose/ear occlusion rays, conservatively includes back eye surface; not iris pixel segmentation'})
    oral=[]
    for name,values in [('mouth-closed',{'MouthClose':1}),('closed-override',{'MouthClose':1,'MouthOpen':1,'Tongue':1,'Joy':.5})]:
        b.state(rig,values);p,t=b.evaluated(bpy.data.objects['ShushuStatic_Head']);tree=BVHTree.FromPolygons(p.tolist(),t.tolist(),all_triangles=True)
        for part in ['Tongue','OralBowl']:
            pp,_=b.evaluated(bpy.data.objects['ShushuStatic_'+part])
            for view,direction in VIEWS:
                d=Vector(direction).normalized();visible=0
                for q in pp:
                    hit=tree.ray_cast(Vector(q)+d*3,-d,3.00001);visible+=hit[0] is None or hit[3]>=2.99998
                oral.append({'state':name,'part':part,'view':view,'surface_vertices_potentially_visible':visible})
    b.reset(rig);returns={k:float(np.linalg.norm(v-neutral[k],axis=1).max()) for k,v in positions(meshes).items()}
    b.write('capability-numeric.json',{'units':'normalized character height ~1.0, Blender Z up; thresholds are explicitly local proof checks, not Human approval','preservation':preservation,'weights':weights,'isolation':isolation,'body_fk':body_fk,'foot_control':foot_control,'support':support,'contacts':contacts,'eye_occlusion':eyes,'closed_oral_occlusion':oral,'neutral_return':returns})
    assert all(x['uv_equal'] and x['topology_equal'] and x['texture_bytes_equal'] for x in preservation),'Identity attributes changed'
    assert all(x['below_minus_001']==0 for x in support),'Support floor penetration'
    assert max(y['sole_xy_drift_max'] for x in support for y in x['feet'].values())<.001,'Planted soles slipped'
    assert all(x['tip_penetration_vertices_over_002']==0 for x in contacts),'Distal paw penetrates body'
    assert all(x['eye_surface_vertices_potentially_visible']==0 for x in eyes if 'closed' in x['state']),'Closed eye exposed'
    assert all(x['surface_vertices_potentially_visible']==0 for x in oral),'Closed mouth exposes oral controls'
    assert all(x['upper_torso_movement']<1e-6 and x['head_movement']==0 and x['opposite_sole_movement']<1e-6 for x in foot_control),'Foot control pulls upper body or opposite sole'
    assert max(returns.values())==0,'Neutral restoration failed'
    print('AUDIT',{'support_min':min(x['min_z'] for x in support),'return_max':max(returns.values())},flush=True)

# Each entry is a capability witness, not a authored product performance.
EVENTS=[
 ('neutral',{}),('head-left',{'HeadYaw':.83}),('head-right',{'HeadYaw':-.83}),
 ('head-tilt-blink',{'HeadRoll':.83,'Blink.L':1,'Blink.R':.5}),('neck',{'NeckPitch':.7}),
 ('ear-L',{'Ear.L':1}),('ear-R',{'Ear.R':-1}),('half',{'Blink.L':.5,'Blink.R':.5}),
 ('closed',{'Blink.L':1,'Blink.R':1}),('wink-L',{'Blink.L':1}),('wink-R',{'Blink.R':1}),
 ('gaze-L',{'GazeX.L':-1,'GazeX.R':-1}),('gaze-up',{'GazeY.L':1,'GazeY.R':1}),('gaze-down',{'GazeY.L':-1,'GazeY.R':-1}),
 ('smile',{'Smile':1}),('joy',{'Joy':1,'Blink.L':.25,'Blink.R':.25}),('surprise',{'Surprise':1}),
 ('hesitate',{'Hesitate':1,'Blink.L':.15,'GazeX.L':-.4,'GazeX.R':-.4}),('discomfort',{'Discomfort':1,'Blink.L':.2,'Blink.R':.2}),
 ('mouth-close',{'MouthClose':1}),('mouth-close-override',{'MouthClose':1,'MouthOpen':1,'Tongue':1,'Joy':.5}),('mouth-open',{'MouthOpen':.6}),('mouth-open-max',{'MouthOpen':1}),('tongue',{'MouthOpen':.6,'Tongue':1}),
 ('pressure-L',{'CheekPressure.L':1,'BellyPressure':1}),('pressure-R',{'CheekPressure.R':1}),
 ('shift-L',{'WeightShift':1}),('shift-R',{'WeightShift':-1}),('foot-lift-L',{'FootLift.L':1,'WeightShift':-.7}),('foot-lift-R',{'FootLift.R':1,'WeightShift':.7}),('seat-entry',{'Seat':.25}),('seat-mid',{'Seat':.5}),
 ('seat',{'Seat':1}),('seat-rest',{'Seat':1,'Rest':1}),('seat-joy',{'Seat':1,'Joy':1,'Blink.L':.3,'Blink.R':.3}),
 ('recovery-mid',{'Seat':.5}),('standing-return',{}),
 ('offer-L',{'Offer.L':1}),('offer-R',{'Offer.R':1}),('wrist-L',{'Offer.L':1,'Wrist.L':.8}),('wrist-R',{'Offer.R':1,'Wrist.R':.8}),('self-L',{'SelfContact.L':1}),('self-R',{'SelfContact.R':1}),
 ('hold-L',{'Hold.L':1}),('hold-both',{'Hold.L':1,'Hold.R':1}),('hold-L-touch-R',{'Hold.L':1,'SelfContact.R':1,'CheekPressure.R':.6}),
 ('seat-hold-interrupt',{'Seat':1,'Hold.L':1,'SelfContact.R':1,'Blink.R':.7,'CheekPressure.R':.6}),
 ('hold-resume',{'Hold.L':1}),('release',{}),('neutral-return',{})]
FRAME_STEP=12
def markers():return [{'frame':1+i*FRAME_STEP,'name':name,'controls':v} for i,(name,v) in enumerate(EVENTS)]
def fixture(rig):
    b.state(rig,{'Hold.L':1});paw=bpy.data.objects['ShushuStatic_Paw_L'];p,_=b.evaluated(paw)
    # Tangent fixture at the frontmost distal paw surface, rather than at a guessed arm joint.
    anchor=bpy.data.objects['ANCHOR_Hold.L'];i=int(anchor['surface_vertex']);center=anchor.matrix_world.translation.copy()
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=.030,location=center);o=bpy.context.object;o.name='PROOF_HeldFixture';m=bpy.data.materials.new('ProofFixture');m.diffuse_color=(.18,.6,.7,1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.18,.6,.7,1);o.data.materials.append(m)
    o['role']='Diagnostic tangent fixture only, not an approved accessory';o['attachment_surface_vertex']=int(i)
    # Object action is baked from the paw-owned attachment until release; editable attachment remains on the rig.
    b.reset(rig);return o,i,center
def proof():
    rig,meshes=load();scene=bpy.context.scene;scene.name='Shushu_RigCapability_Proof';scene.render.fps=24;scene.frame_start=1;scene.frame_end=markers()[-1]['frame']
    channels=[k for k in rig.keys() if isinstance(rig[k],float)]
    for row in markers():
        b.state(rig,row['controls']);scene.timeline_markers.new(row['name'],frame=row['frame'])
        for k in channels:rig.keyframe_insert(data_path='["'+k+'"]',frame=row['frame'],group='Production capabilities')
    # Linear bounded values prevent overshoot. This sequence verifies composition and restoration.
    for slot in rig.animation_data.action.slots:
        for layer in rig.animation_data.action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='LINEAR'
    scene.frame_set(1);o,vertex,_=fixture(rig);scene.frame_set(1)
    first_hold=next(x['frame'] for x in markers() if x['name']=='hold-L');release=next(x['frame'] for x in markers() if x['name']=='release');held_end=release-FRAME_STEP
    held_world=None;attachment=[];fixture_track=[]
    for f in range(1,scene.frame_end+1):
        scene.frame_set(f);anchor=bpy.data.objects['ANCHOR_Hold.L']
        if f<=held_end:held_world=anchor.matrix_world.copy()
        o.matrix_world=held_world;o.keyframe_insert(data_path='location',frame=f);o.keyframe_insert(data_path='rotation_euler',frame=f);o.keyframe_insert(data_path='scale',frame=f)
        fixture_track.append({'frame':f,'world_matrix':list(map(list,o.matrix_world))})
        # Fixture is visible during acquisition, hold, interrupt, resume, release; hide it earlier in Blender proof.
        visible=f>=first_hold-FRAME_STEP
        o.hide_render=not visible;o.keyframe_insert(data_path='hide_render',frame=f)
        if first_hold<=f<=held_end:
            pp,_=b.evaluated(bpy.data.objects['ShushuStatic_Paw_L']);gap=float((o.matrix_world.translation-Vector(pp[vertex])).length-.030)
            attachment.append({'frame':f,'surface_gap':gap,'anchor_to_fixture':float((o.matrix_world.translation-anchor.matrix_world.translation).length)})
    scene.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(b.PROOF))
    b.write('proof-timeline.json',{'fps':24,'frames':scene.frame_end,'purpose':'Minimal capability sequence; DRAFT motion timings are not adopted','markers':markers(),'attachment':attachment,'fixture_track':fixture_track,'release_frame':release,'release_policy':'World matrix frozen at hold-resume before hand returns; no physics simulation','fixture_visibility':'Editable Blender hides diagnostic before acquisition; glTF has no visibility track here, so fixture proof GLB shows it throughout'})
    # Bake evaluated constraints and drivers to ordinary transform/morph channels, retaining the editable proof on disk.
    anchors=[o for o in bpy.data.objects if o.name.startswith('ANCHOR_')];anchor_basis={};anchor_world={o.name:[] for o in anchors}
    pose={};morph={};reference={};floor=[];names=[o.name for o in meshes]
    sampleframes=set(x['frame'] for x in markers())
    for f in range(1,scene.frame_end+1):
        scene.frame_set(f);bpy.context.view_layer.update()
        if f%120==0:print('SAMPLING',f,flush=True)
        pose[f]={pb.name:pb.matrix.copy() for pb in rig.pose.bones}
        anchor_basis[f]={a.name:a.matrix_basis.copy() for a in anchors}
        for a in anchors:anchor_world[a.name].append(np.array(a.matrix_world))
        morph[f]={o.name:{k.name:float(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.shape_keys.key_blocks[k.name].value) for k in o.data.shape_keys.key_blocks[1:]} for o in meshes if o.data.shape_keys}
        tp,_=b.evaluated(bpy.data.objects['ShushuStatic_Torso']);floor.append({'frame':f,'min_z':float(tp[:,2].min()),'below_minus_001':int((tp[:,2]<-.001).sum())})
        if f in sampleframes:
            for n,p in positions(meshes).items():reference[n+'__'+str(f)]=p.astype(np.float32)
    np.savez_compressed(OUT/'roundtrip-reference.npz',**reference)
    np.savez_compressed(OUT/'anchor-reference.npz',**{n:np.array(v) for n,v in anchor_world.items()})
    b.write('proof-floor.json',floor)
    if rig.animation_data:
        rig.animation_data.action=None
        for d in list(rig.animation_data.drivers):rig.driver_remove(d.data_path,d.array_index)
    for pb in rig.pose.bones:
        for c in list(pb.constraints):pb.constraints.remove(c)
        pb.rotation_mode='QUATERNION'
    for obj in meshes:
        if obj.data.shape_keys and obj.data.shape_keys.animation_data:
            obj.data.shape_keys.animation_data.action=None
            for d in list(obj.data.shape_keys.animation_data.drivers):obj.data.shape_keys.driver_remove(d.data_path,d.array_index)
    for a in anchors:
        a.rotation_mode='QUATERNION'
        if a.animation_data:
            a.animation_data.action=None
            for d in list(a.animation_data.drivers):a.driver_remove(d.data_path,d.array_index)
    baking=[]
    for f in range(1,scene.frame_end+1):
        scene.frame_set(f)
        if f%120==0:print('BAKING',f,flush=True)
        for pb in rig.pose.bones:
            parent_pose=pose[f].get(pb.parent.name) if pb.parent else None
            local=pb.bone.convert_local_to_pose(pose[f][pb.name],pb.bone.matrix_local,parent_matrix=parent_pose if pb.parent else Matrix.Identity(4),parent_matrix_local=pb.parent.bone.matrix_local if pb.parent else Matrix.Identity(4),invert=True)
            pb.matrix_basis=local;pb.keyframe_insert(data_path='location',frame=f);pb.keyframe_insert(data_path='rotation_quaternion',frame=f);pb.keyframe_insert(data_path='scale',frame=f)
        for n,keys in morph[f].items():
            for name,value in keys.items():
                k=bpy.data.objects[n].data.shape_keys.key_blocks[name];k.value=value;k.keyframe_insert(data_path='value',frame=f)
        for a in anchors:
            a.matrix_basis=anchor_basis[f][a.name]
            for channel in ['location','rotation_quaternion','scale']:a.keyframe_insert(data_path=channel,frame=f)
        bpy.context.view_layer.update()
        if f in sampleframes:
            for n,p in positions(meshes).items():baking.append({'frame':f,'mesh':n,'max_error':float(np.linalg.norm(p-reference[n+'__'+str(f)],axis=1).max())})
    b.write('bake-verification.json',baking)
    assert max(x['max_error'] for x in baking)<2e-6,'Bake lost evaluated deformation'
    scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
    for obj in meshes:obj.select_set(True)
    for a in anchors:a.select_set(True)
    bpy.context.view_layer.objects.active=rig
    settings=dict(export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_frame_step=1,export_force_sampling=True,export_bake_animation=True,export_anim_scene_split_object=False,export_nla_strips_merged_animation_name='Shushu_RigCapability_Proof',export_optimize_animation_size=False,export_skins=True,export_all_influences=True,export_morph=True,export_morph_animation=True,export_apply=False,export_keep_originals=False,export_extras=True)
    bpy.ops.export_scene.gltf(filepath=str(b.GLB),**settings)
    # A separate fixture proof GLB includes the ordinary baked object transform action.
    o.select_set(True);bpy.ops.export_scene.gltf(filepath=str(b.GLB.with_name(b.GLB.stem+'-proof.glb')),**settings)
    print('PROOF_SAVED',{'frames':scene.frame_end,'bake_max':max(x['max_error'] for x in baking),'floor_min':min(x['min_z'] for x in floor)},flush=True)
def roundtrip():
    ref=np.load(OUT/'roundtrip-reference.npz');_,original=load();source_attributes={}
    def attrs(o):
        uv=[set() for _ in o.data.vertices]
        if o.data.uv_layers.active:
            for loop,data in zip(o.data.loops,o.data.uv_layers.active.data):uv[loop.vertex_index].add(tuple(data.uv))
        weights=[{o.vertex_groups[g.group].name:float(g.weight) for g in v.groups} for v in o.data.vertices]
        return uv,weights
    for obj in original:source_attributes[obj.name]=attrs(obj)
    import_saved(b.GLB);scene=bpy.context.scene;scene.frame_set(1);meshes=sorted([o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')],key=lambda o:o.name)
    assert len(meshes)==len([n for n in ref.files if n.endswith('__1')]),'Mesh count mismatch'
    lookup={};mapping=[];import_weights={}
    for o in meshes:
        base=ref[o.name+'__1'];tree=KDTree(len(base))
        for i,p in enumerate(base):tree.insert(Vector(p),i)
        tree.balance();p,_=b.evaluated(o);found=[tree.find(Vector(q)) for q in p];source_uv,source_w=source_attributes[o.name];uv,ww=attrs(o);ids=[];ambiguous=0
        for i,q in enumerate(p):
            candidates=tree.find_range(Vector(q),1e-6)
            if len(candidates)>1:
                ambiguous+=1
                def score(v):
                    index=v[1];a=source_w[index];w=ww[i];weight_error=sum(abs(a.get(k,0)-w.get(k,0)) for k in set(a)|set(w));uv_error=0 if source_uv[index]&uv[i] else 1
                    return (uv_error,round(weight_error,6),v[2])
                chosen=min(candidates,key=score)[1]
            else:chosen=found[i][1]
            ids.append(chosen)
        lookup[o.name]=np.array(ids);import_weights[o.name]=ww;mapping.append({'mesh':o.name,'vertices_after_import':len(p),'vertices_before_export':len(base),'rest_match_max':max(x[2] for x in found),'duplicate_position_candidates':ambiguous,'method':'Nearest rest position with UV seam and bone weight correspondence; avoids comparing coincident seam vertices with different deformation ownership.'})
    rows=[];floors=[];outliers=[]
    for mark in markers():
        scene.frame_set(mark['frame']);bpy.context.view_layer.update()
        for o in meshes:
            p,_=b.evaluated(o);expected=ref[o.name+'__'+str(mark['frame'])][lookup[o.name]];errors=np.linalg.norm(p-expected,axis=1);rows.append({'frame':mark['frame'],'state':mark['name'],'mesh':o.name,'world_error':stat(errors)})
            if errors.max()>1e-5:
                for i in np.argsort(errors)[-3:]:
                    src=int(lookup[o.name][i]);outliers.append({'state':mark['name'],'mesh':o.name,'import_vertex':int(i),'source_vertex':src,'error':float(errors[i]),'expected':expected[i].tolist(),'actual':p[i].tolist(),'weights_before':source_attributes[o.name][1][src],'weights_after':import_weights[o.name][i]})
    torso=next(o for o in meshes if o.name.endswith('Torso'))
    for f in range(1,markers()[-1]['frame']+1):
        scene.frame_set(f);p,_=b.evaluated(torso);floors.append({'frame':f,'min_z':float(p[:,2].min()),'below_minus_001':int((p[:,2]<-.001).sum())})
    j,bin=b.read_glb(b.GLB);animation=[]
    for a in j.get('animations',[]):
        paths={}
        for c in a['channels']:paths[c['target']['path']]=paths.get(c['target']['path'],0)+1
        animation.append({'name':a.get('name'),'channels':paths,'samplers':len(a['samplers'])})
    b.write('glb-roundtrip.json',{'sha256':b.sha(b.GLB),'mapping':mapping,'states':rows,'floor':floors,'skins':[len(s['joints']) for s in j.get('skins',[])],'morph_targets':{m['name']:len(m['primitives'][0].get('targets',[])) for m in j['meshes']},'animations':animation,'max_world_error':max(x['world_error']['max'] for x in rows),'max_rest_error':max(x['rest_match_max'] for x in mapping)})
    b.write('roundtrip-outliers.json',outliers)
    assert max(x['world_error']['max'] for x in rows)<1e-5,'GLB deformation mismatch'
    anchor_ref=np.load(OUT/'anchor-reference.npz');ar=[]
    for f in range(1,markers()[-1]['frame']+1):
        scene.frame_set(f)
        for name in anchor_ref.files:
            obj=bpy.data.objects.get(name);assert obj is not None,'Missing exported anchor '+name
            ar.append({'frame':f,'anchor':name,'max_matrix_error':float(np.max(np.abs(np.array(obj.matrix_world)-anchor_ref[name][f-1])))})
    b.write('anchor-roundtrip.json',ar);assert max(x['max_matrix_error'] for x in ar)<1e-5,'Anchor transform mismatch'
    timeline=json.loads((OUT/'proof-timeline.json').read_text(encoding='utf-8'));import_saved(b.GLB.with_name(b.GLB.stem+'-proof.glb'));fixture_obj=bpy.data.objects['PROOF_HeldFixture'];fixture_rows=[]
    for row in timeline['fixture_track']:
        bpy.context.scene.frame_set(row['frame']);fixture_rows.append({'frame':row['frame'],'max_matrix_error':float(np.max(np.abs(np.array(fixture_obj.matrix_world)-np.array(row['world_matrix']))))})
    b.write('fixture-roundtrip.json',fixture_rows);assert max(x['max_matrix_error'] for x in fixture_rows)<1e-5,'Fixture transform mismatch'
    print('ROUNDTRIP',max(x['world_error']['max'] for x in rows),flush=True)
VIEWS=[('front',(0,-1,0)),('3q',(-.65,-.76,0)),('left',(-1,0,0)),('right',(1,0,0))]
def fixture_check():
    bpy.ops.wm.open_mainfile(filepath=str(b.PROOF));scene=bpy.context.scene;o=bpy.data.objects['PROOF_HeldFixture'];rows=[]
    start=next(x['frame'] for x in markers() if x['name']=='hold-L')
    for frame in range(start,scene.frame_end+1):
        scene.frame_set(frame);center=o.matrix_world.translation
        for name in ['ShushuStatic_Paw_L','ShushuStatic_Paw_R','ShushuStatic_Torso']:
            p,t=b.evaluated(bpy.data.objects[name]);tree=BVHTree.FromPolygons(p.tolist(),t.tolist(),all_triangles=True);point,normal,_,distance=tree.find_nearest(center)
            outside_aabb=bool(((np.array(center)<p.min(0))|(np.array(center)>p.max(0))).any())
            rows.append({'frame':frame,'mesh':name,'sphere_surface_clearance':float(distance-.030),'center_outside_mesh_aabb':outside_aabb,'center_on_outside_of_nearest_face':bool((center-point).dot(normal)>=0),'method':'Nearest triangle distance to spherical fixture center minus radius. AABB excludes containment when available; nearest-face orientation is local evidence, not a watertight winding-number test or force/friction solver.'})
    b.write('fixture-clearance.json',rows)
    assert min(x['sphere_surface_clearance'] for x in rows)>-.0001,'Held/released fixture intersects character'
    assert all(x['center_outside_mesh_aabb'] or x['center_on_outside_of_nearest_face'] for x in rows),'Fixture containment not excluded'
    print('FIXTURE_CLEARANCE',min(x['sphere_surface_clearance'] for x in rows),flush=True)
def camera(cam,direction):
    d=Vector(direction).normalized();cam.location=Vector((0,0,.5))+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
def render():
    reimport='--reimport' in sys.argv;source='--source' in sys.argv;approved='--approved' in sys.argv;with_fixture='--fixture' in sys.argv
    if reimport:
        import_saved(b.GLB);rig=None
    elif source:
        b.fresh();rig=None
    elif approved:
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(b.BASE/'texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb'));rig=None
    elif with_fixture:
        bpy.ops.wm.open_mainfile(filepath=str(b.PROOF));rig=None
    else:rig,meshes=load()
    scene,cam=b.setup_review(640,24);folder=RENDERS/('reimport' if reimport else 'source' if source else 'approved-static' if approved else 'fixture' if with_fixture else 'editable');folder.mkdir(parents=True,exist_ok=True)
    chosen=sys.argv[sys.argv.index('--names')+1].split(',') if '--names' in sys.argv else [x['name'] for x in markers() if x['name'] not in ['head-left','head-right','recovery-mid','standing-return','hold-L','hold-resume','release']]
    if source or approved:chosen=['neutral']
    for row in markers():
        if row['name'] not in chosen:continue
        if reimport or with_fixture:scene.frame_set(row['frame'])
        elif rig:b.state(rig,row['controls'])
        for view,d in VIEWS:
            camera(cam,d);scene.render.filepath=str(folder/(row['name']+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
        print('RENDERED',folder.name,row['name'],flush=True)
    b.write('render-conditions.json',{'size':[640,640],'samples':24,'seed':0,'denoise':False,'display':'AgX, exposure -0.5','ortho_scale':1.14,'target':[0,0,.5],'distance':3,'floor_z':-.002,'views':VIEWS,'lighting':'Same setup as prior Auto Rig Gate; fixed world/key/fill/camera','source':'Autorig before repair, compared under identical conditions'})
if __name__=='__main__':
    audit() if '--audit' in sys.argv else proof() if '--proof' in sys.argv else roundtrip() if '--roundtrip' in sys.argv else fixture_check() if '--fixture-check' in sys.argv else render()
