"""Localized eyelid / gaze / minimal mouth proof and actual glTF roundtrip."""
import bpy, numpy as np, math, sys, json
from pathlib import Path
from mathutils import Vector, Matrix, Euler
from mathutils.kdtree import KDTree
sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import importlib
audit=importlib.import_module('shushu-candidate-b-audit')
deform=importlib.import_module('shushu-candidate-b-deform')
ROOT,OUT,BLEND,RENDERS=audit.ROOT,audit.OUT,audit.BLEND,audit.RENDERS
GLB=ROOT/'assets/grimo/production/shushu/runtime-probes/shushu-candidate-b-diagnostic.glb'

def mesh_obj(name,verts,faces,color=(.65,.68,.73,1)):
    m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update()
    o=bpy.data.objects.new(name,m);bpy.context.scene.collection.objects.link(o);o.color=color
    for p in m.polygons:p.use_smooth=True
    return o

def attach(o,rig):
    world=o.matrix_world.copy();o.parent=rig;o.matrix_world=world
    group=o.vertex_groups.new(name='Head');group.add(list(range(len(o.data.vertices))),1,'REPLACE')
    mod=o.modifiers.new('Head ownership','ARMATURE');mod.object=rig
    o['role']='Disposable localized reconstruction feasibility proof; not final visual design'

def add_lid(side,sign,upper,rig):
    cx=sign*.139;cy=-.214;cz=.667;rx=.050;ry=.031;rz=.059
    verts=[];closed=[];faces=[];nu=25;nv=9
    # Ellipsoidal covering skin, not a scaled eyeball. Shared end poles avoid duplicate degenerate faces.
    for i in range(nu):
        angle=-math.pi/2+i/(nu-1)*math.pi;u=math.sin(angle);height=math.cos(angle)
        for j in range(nv):
            ratio=j/(nv-1);z=height*(.87+.13*ratio)*(1 if upper else -1)
            zc=height*ratio*(1 if upper else -1)
            verts.append((cx+rx*u,cy-ry*math.sqrt(max(0,1-u*u-z*z))-.001,cz+rz*z))
            closed.append((cx+rx*u,cy-ry*math.sqrt(max(0,1-u*u-zc*zc))-.001,cz+rz*zc))
    for i in range(nu-1):
        for j in range(nv-1):
            a=i*nv+j;b=(i+1)*nv+j
            if i==0:faces.append((a,b,b+1))
            elif i==nu-2:faces.append((a,b,a+1))
            else:faces.append((a,b,b+1,a+1))
    # Merge duplicated zero-width side poles with consistent index remapping.
    unique=[];mapids={};mapping=[]
    for i,v in enumerate(verts):
        key=tuple(round(c,8) for c in v)
        if key not in mapids:mapids[key]=len(unique);unique.append(i)
        mapping.append(mapids[key])
    compact=[]
    for f in faces:
        f=list(dict.fromkeys(mapping[i] for i in f))
        if len(f)>=3:compact.append(f)
    name='FacialRepair_Lid'+('Upper' if upper else 'Lower')+'.'+side
    if not upper:compact=[list(reversed(f)) for f in compact]
    o=mesh_obj(name,[verts[i] for i in unique],compact);o.shape_key_add(name='Basis',from_mix=False)
    key=o.shape_key_add(name='Close.'+side,from_mix=False)
    for p,i in zip(key.data,unique):p.co=closed[i]
    attach(o,rig);return o

def make_eyes(rig):
    result=[];lids={};irises={}
    for side,sign in [('L',1),('R',-1)]:
        center=Vector((sign*.139,-.214,.667))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,radius=1,location=center)
        eye=bpy.context.object;eye.name='FacialRepair_Eyeball.'+side;eye.scale=(.050,.029,.059)
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        # Convert mesh coordinates to world so skinning uses one common space.
        for v in eye.data.vertices:v.co=eye.matrix_world@v.co
        for p in eye.data.polygons:p.use_smooth=True
        eye.matrix_world=Matrix.Identity(4);eye.color=(.24,.27,.32,1);attach(eye,rig);result.append(eye)
        lids[side]=[add_lid(side,sign,u,rig) for u in [True,False]];result+=lids[side]
        verts=[center+Vector((0,-.030,0))];faces=[]
        for i in range(32):
            a=i/32*2*math.pi;x=.027*math.cos(a);z=.033*math.sin(a)
            y=-.031*math.sqrt(max(0,1-(x/.050)**2-(z/.059)**2))-.0005
            verts.append(center+Vector((x,y,z)));faces.append((0,i+1,(i+1)%32+1))
        iris=mesh_obj('FacialRepair_Iris.'+side,verts,faces,(.055,.07,.09,1));attach(iris,rig);irises[side]=iris;result.append(iris)
        iris.shape_key_add(name='Basis',from_mix=False)
        for label,angles in [('GazeLeft',(0,0,-8)),('GazeRight',(0,0,8)),('GazeDown',(6,0,0))]:
            k=iris.shape_key_add(name=label,from_mix=False);rot=Euler([math.radians(a) for a in angles],'XYZ').to_matrix()
            for p in k.data:p.co=center+rot@(p.co-center)
    return result,lids,irises

def mouth_proof(rig):
    # A small fitted pocket over the raw cavity region. Interface stitching remains production work.
    center=(0,-.284,.578);rx=.030;rz=.020;verts=[(0,-.264,.578)];closed=[(0,-.280,.596)];faces=[]
    for ring in range(1,5):
        r=ring/4
        for i in range(32):
            a=i/32*2*math.pi;x=rx*r*math.cos(a);z=.578+rz*r*math.sin(a)
            verts.append((x,-.284+.020*(1-r*r),z));closed.append((x,-.284+.004*(1-r*r),.596+.002*r*math.sin(a)))
    for i in range(32):faces.append((0,i+1,(i+1)%32+1))
    for ring in range(1,4):
        for i in range(32):
            a=1+(ring-1)*32+i;b=1+(ring-1)*32+(i+1)%32;c=b+32;d=a+32;faces.append((a,b,c,d))
    o=mesh_obj('FacialRepair_MouthPocket',verts,faces,(.13,.15,.18,1));o.shape_key_add(name='Basis',from_mix=False)
    k=o.shape_key_add(name='CloseMouth',from_mix=False)
    for v,p in zip(k.data,closed):v.co=p
    attach(o,rig);return o

def close(lids,side,value):
    for o in lids[side]:o.data.shape_keys.key_blocks['Close.'+side].value=value

def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND));obj=bpy.data.objects['CandidateB_ScratchCore'];rig=bpy.data.objects['CandidateB_ScratchCore_Rig'];cam=bpy.context.scene.camera
    # Save clips aside; manual probes run without action influence.
    rig.animation_data_clear();obj.data.shape_keys.animation_data_clear();deform.reset(rig,obj)
    for o in list(bpy.data.objects):
        if o.name.startswith('FacialRepair_'):bpy.data.objects.remove(o,do_unlink=True)
    eyes,lids,irises=make_eyes(rig);mouth=mouth_proof(rig);proofs=eyes+[mouth]
    bpy.context.scene.display.shading.color_type='OBJECT';obj.color=(.65,.68,.73,1)
    report={'purpose':'Local eye reconstruction and mouth-interior capacity proof; not canonical-final face. Eight-core scratch deliberately omits original eye-cap islands; raw mesh remains in scene.',
            'tests':{},'glb_path':GLB.relative_to(ROOT).as_posix()}
    tests=[('eyes-open',0,0,None,1),('left-half',.5,0,None,1),('left-closed',1,0,None,1),('right-closed',0,1,None,1),
           ('both-closed',1,1,None,1),('gaze-left',0,0,'GazeLeft',1),('gaze-right',0,0,'GazeRight',1),
           ('gaze-down',0,0,'GazeDown',1),('mouth-small-open',0,0,None,0),('mouth-small-chew',0,0,None,.4)]
    original_eyes={o.name:deform.evaluated(o)[0] for o in eyes if 'Eyeball' in o.name}
    for label,l,r,gaze,mouthclose in tests:
        close(lids,'L',l);close(lids,'R',r)
        for o in irises.values():
            for k in o.data.shape_keys.key_blocks:k.value=1 if k.name==gaze else 0
        mouth.data.shape_keys.key_blocks['CloseMouth'].value=mouthclose
        audit.render(cam,'repair-'+label+'-front',(0,-1,0),target=(0,-.16,.66),scale=.44)
        audit.render(cam,'repair-'+label+'-threequarter',(1,-1,0),target=(0,-.16,.66),scale=.44)
        unchanged={o.name:float(np.linalg.norm(deform.evaluated(o)[0]-original_eyes[o.name],axis=1).max()) for o in eyes if 'Eyeball' in o.name}
        seam={}
        for side in ['L','R']:
            a=deform.evaluated(lids[side][0])[0];b=deform.evaluated(lids[side][1])[0]
            # Aperture between central upper/lower lid vertices; side poles excluded.
            maska=np.abs(a[:,0]-(.139 if side=='L' else -.139))<.002
            maskb=np.abs(b[:,0]-(.139 if side=='L' else -.139))<.002
            seam[side]=float(a[maska,2].min()-b[maskb,2].max())
        report['tests'][label]={'eyeball_geometry_change':unchanged,'central_lid_aperture':seam,'mouth_close':mouthclose,'gaze':gaze,
                               'scope':'mechanical local proof; Human eye shape/identity acceptance pending'}
    # Vertex-sample mouth approach and chest/ear Wear attachment clearance.
    for label,loc,radius in [('food-contact',(0,-.310,.582),.018),('wear-chest',(.09,-.245,.405),.018),('bouquet-low',(0,-.28,.35),.065)]:
        v,t=deform.evaluated(obj);prop=deform.proxy('TEMP_'+label,loc,radius)
        if label=='bouquet-low':
            deform.paw_target(rig,'L',(.095,-.205,.365));deform.paw_target(rig,'R',(-.095,-.205,.365));v,t=deform.evaluated(obj)
        audit.render(cam,'repair-'+label,(1,-1,.12))
        head=v[v[:,2]>.53]
        report['tests'][label]={'center':loc,'radius':radius,'head_min_vertex_distance_minus_radius':float((np.linalg.norm(head-np.array(loc),axis=1)-radius).min()),
                               'limitation':'bounded proxy and vertex samples; triangle contact, final prop shape and semantics not approved'}
        bpy.data.objects.remove(prop,do_unlink=True);deform.reset(rig,obj)
    # A pose-space local smoothing trial demonstrates what a cheap corrective can and cannot repair.
    deform.support_pose(rig,.095);v,t=deform.evaluated(obj)
    repaired=v.copy();adj=defaultdict(set)
    for tri in t:
        for a,b in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])]:adj[a].add(b);adj[b].add(a)
    original=np.array([p.co[:] for p in obj.data.shape_keys.key_blocks['Basis'].data])
    region=(original[:,2]>.065)&(original[:,2]<.245)&(np.abs(original[:,0])>.06)
    for _ in range(10):
        nxt=repaired.copy()
        for i in np.flatnonzero(region):
            nxt[i]=.65*repaired[i]+.35*repaired[list(adj[i])].mean(0)
        repaired=nxt
    local=mesh_obj('FacialRepair_SupportSmoothingFailure',repaired,t.tolist());obj.hide_render=True
    for o in proofs:o.hide_render=True
    audit.render(cam,'repair-sitting-local-smoothing',(1,-1,.12))
    report['support_corrective_trial']={'method':'10 local Laplacian steps at 0.35 with original sole region fixed; baked disposable copy',
                                        'before_min_z':float(v[:,2].min()),'after_min_z':float(repaired[:,2].min()),
                                        'verdict':'FAIL if ground penetration persists; smoothing is not deformation-oriented retopology'}
    local.hide_render=True;local.hide_set(True);obj.hide_render=False
    for o in proofs:o.hide_render=False
    deform.reset(rig,obj)
    # Export linear skinning truth. Dual-quaternion preserve-volume is Blender-only.
    obj.modifiers['Temporary anatomical skinning'].use_deform_preserve_volume=False
    obj.parent=rig
    report['unsupported_functionality']=['Blender dual-quaternion preserve-volume skinning; temporary IK solved and baked as explicit joint transforms; Workbench diagnostic lighting']
    for frame in [1,12,24]:
        deform.reset(rig,obj);deform.support_pose(rig,.035 if frame==12 else 0)
        if frame==12:deform.paw_target(rig,'L',(.30,-.14,.41))
        for b in rig.pose.bones:
            b.keyframe_insert('location',frame=frame);b.keyframe_insert('rotation_quaternion' if b.rotation_mode=='QUATERNION' else 'rotation_euler',frame=frame);b.keyframe_insert('scale',frame=frame)
        for side in ['L','R']:
            close(lids,side,1 if frame==12 and side=='L' else 0)
            for o in lids[side]:o.data.shape_keys.key_blocks['Close.'+side].keyframe_insert('value',frame=frame)
        for iris in irises.values():
            for k in list(iris.data.shape_keys.key_blocks)[1:]:
                k.value=1 if frame==12 and k.name=='GazeRight' else 0;k.keyframe_insert('value',frame=frame)
        mouth.data.shape_keys.key_blocks['CloseMouth'].value=.25 if frame==12 else 1;mouth.data.shape_keys.key_blocks['CloseMouth'].keyframe_insert('value',frame=frame)
        obj.data.shape_keys.key_blocks['BellyPressure'].value=1 if frame==12 else 0;obj.data.shape_keys.key_blocks['BellyPressure'].keyframe_insert('value',frame=frame)
    scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=24;scene.frame_set(1)
    expected={}
    for o in [obj]+proofs:o['probe_id']=o.name
    for frame in [1,12,24]:
        scene.frame_set(frame);expected[frame]={o.name:deform.evaluated(o)[0].tolist() for o in [obj]+proofs}
    GLB.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in [obj,rig]+proofs:o.hide_set(False);o.select_set(True)
    bpy.context.view_layer.objects.active=obj
    bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',
                              export_frame_range=True,export_force_sampling=True,export_morph=True,export_skins=True,export_extras=True,export_anim_scene_split_object=False)
    scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    # Independent binary reader checks structure before Blender importer.
    doc,binary=audit.glb(GLB)
    report['export_structure']={'bytes':GLB.stat().st_size,'nodes':len(doc['nodes']),'meshes':len(doc['meshes']),'skins':len(doc.get('skins',[])),
                                'animations':[{ 'name':a.get('name'),'channels':len(a['channels']),'paths':sorted(set(c['target']['path'] for c in a['channels']))} for a in doc.get('animations',[])],
                                'morph_counts':{m['name']:len(m['primitives'][0].get('targets',[])) for m in doc['meshes']}}
    times=audit.accessor(doc,binary,doc['animations'][0]['samplers'][0]['input']).reshape(-1)
    report['export_time_range_seconds']=[float(times.min()),float(times.max())]
    report['export_fps']=scene.render.fps/scene.render.fps_base
    report['resolved_export_setup_issue']='Default scene export split rig and each morph owner into 9 glTF animations. Blender imported only the active clip; a stressed sample differed by up to 0.05 model units. export_anim_scene_split_object=False merges the shared timeline into one animation, then vertex agreement is retested.'
    for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
    bpy.ops.import_scene.gltf(filepath=str(GLB))
    actual={o.get('probe_id',o.name):o for o in scene.objects if o.type=='MESH'};errors={}
    for frame in [1,12,24]:
        # Blender preserves the initial frame-1 timestamp (1/24 second), rather than sliding to zero.
        scene.frame_set(frame);row={}
        for name,verts in expected[frame].items():
            imported=actual.get(name) or actual.get(name+'_Mesh')
            if imported is None:
                candidates=[o for key,o in actual.items() for base in [name,name+'_Mesh']
                            if key.startswith(base+'.') and key[len(base)+1:].isdigit()]
                assert len(candidates)==1,(name,[o.name for o in candidates])
                imported=candidates[0]
            assert imported is not None,(name,list(actual))
            v,t=deform.evaluated(imported);tree=KDTree(len(v))
            for i,p in enumerate(v):tree.insert(Vector(p),i)
            tree.balance();dist=np.array([tree.find(Vector(p))[2] for p in verts])
            row[name]={'original_vertices':len(verts),'reimport_vertices':len(v),'triangles':len(t),'max_nearest_vertex_error':float(dist.max()),'rms_nearest_vertex_error':float(np.sqrt((dist*dist).mean())),
                       'limitation':'nearest-vertex correspondence tolerates normal-split export duplication; not an animation-quality judgment'}
        errors[str(frame)]={'import_frame':frame,'meshes':row}
    report['roundtrip_samples']=errors
    # Source→import agreement plus a meaningful animated displacement guard.
    deltas={}
    for name in expected[1]:
        a=np.array(expected[1][name]);b=np.array(expected[12][name]);deltas[name]=float(np.linalg.norm(a-b,axis=1).max())
    report['source_sample_motion_amplitudes']=deltas
    scene.frame_set(12);cam=audit.setup_render();scene.display.shading.color_type='SINGLE'
    audit.render(cam,'roundtrip-frame12',(1,-1,.12))
    audit.write('facial-repair-and-roundtrip.json',report)
    print('FACIAL_ROUNDTRIP_COMPLETE',json.dumps(report['export_structure']))

from collections import defaultdict
if __name__=='__main__':main()
