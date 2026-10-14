"""Focused v002 evidence. Reuse read-only v001 sampling and glTF correspondence."""
import bpy, sys, json, importlib.util, math
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
v=module('build_v002','scripts/blender/build-shushu-production-rig-v002.py')
p=module('proof_v001','scripts/blender/prove-shushu-production-rig-v001.py')
b=v.b;b.ASSET=v.ASSET;b.PROOF=v.PROOF;b.GLB=v.GLB
p.b=b;p.OUT=v.OUT;p.RENDERS=v.OUT/'renders'
p.VIEWS=[('front',(0,-1,0)),('3q-L',(-.65,-.76,0)),('3q-R',(.65,-.76,0)),('left',(-1,0,0)),('right',(1,0,0))]
EXTRA=[('seat-quarter',{'Seat':.25}),('seat-three-quarter',{'Seat':.75}),('seat-lowhead',{'Seat':1,'HeadPitch':1,'Rest':.4,'Blink.L':.5,'Blink.R':.5}),('seat-shift-L',{'Seat':1,'WeightShift':1,'HeadRoll':-.5,'Joy':.6}),('seat-shift-R',{'Seat':1,'WeightShift':-1,'HeadRoll':.5,'Blink.L':1,'Blink.R':.5}),('hold-conflict-L',{'Seat':1,'Hold.L':1,'Offer.L':1,'SelfContact.L':1,'SelfContact.R':1}),('hold-conflict-R',{'Seat':1,'Hold.R':1,'Offer.R':1,'SelfContact.R':1,'Offer.L':1}),('extreme-face',{'Seat':1,'WeightShift':1,'HeadYaw':1,'HeadPitch':1,'HeadRoll':1,'Rest':1,'Joy':1,'Blink.L':1,'Blink.R':1,'MouthClose':1,'MouthOpen':1,'Tongue':1,'CheekPressure.L':1,'Hold.L':1,'SelfContact.R':1}),('stroke-belly-start',{'Seat':1,'Hold.L':1,'StrokeZone':3,'StrokeU':-1,'StrokeV':-.5,'StrokePressure':1}),('stroke-belly-end',{'Seat':1,'Hold.L':1,'StrokeZone':3,'StrokeU':1,'StrokeV':.5,'StrokePressure':1}),('stroke-reverse',{'Seat':1,'Hold.L':1,'StrokeZone':3,'StrokeU':-1,'StrokeV':-.5,'StrokePressure':1}),('stroke-cheek-L',{'HeadYaw':-.6,'StrokeZone':1,'StrokeU':1,'StrokeV':.5,'StrokePressure':1,'Hold.R':1}),('stroke-cheek-R',{'HeadYaw':.6,'StrokeZone':2,'StrokeU':-1,'StrokeV':-.5,'StrokePressure':1,'Hold.L':1}),('stroke-forehead',{'HeadPitch':.7,'StrokeZone':0,'StrokeU':0,'StrokeV':0,'StrokePressure':1}),('interrupt-return',{'Seat':.5,'Hold.L':1,'Offer.L':1,'Blink.R':.4}),('capability-neutral-return',{})]
PROXY_EVENTS=[('proxy-both-acquire',{'Hold.L':1,'Hold.R':1}),('proxy-both-seat',{'Seat':1,'Hold.L':1,'Hold.R':1}),('proxy-both-interrupt',{'Seat':1,'WeightShift':.7,'Hold.L':1,'Hold.R':1,'Offer.L':1,'HeadPitch':.6,'Blink.R':1,'StrokeZone':3,'StrokeU':.5,'StrokePressure':1}),('proxy-both-resume',{'Seat':.5,'Hold.L':1,'Hold.R':1}),('proxy-both-release',{'Seat':.5}),('food-small',{'Seat':1,'MouthOpen':1}),('food-multi-a',{'Seat':1,'MouthOpen':1,'Hold.L':1}),('food-multi-close',{'Seat':1,'MouthClose':1,'Hold.L':1,'Blink.R':.5}),('food-multi-b',{'Seat':1,'MouthOpen':1,'Hold.L':1,'CheekPressure.R':.3}),('food-lick',{'Seat':1,'MouthOpen':.7,'Tongue':1,'Hold.R':1}),('food-drink',{'Seat':1,'MouthOpen':.45,'HeadPitch':.35,'HeadRoll':.25}),('food-large',{'Seat':1,'MouthOpen':1,'Hold.L':1,'Hold.R':1}),('food-cancel',{'Seat':1,'Hold.L':1,'MouthClose':1}),('food-resume',{'Seat':1,'Hold.L':1,'MouthOpen':1}),('food-return',{'Seat':1,'Joy':.6})]
p.EVENTS=p.EVENTS[:-1]+EXTRA+PROXY_EVENTS+[('neutral-return',{})]

def tangent_contact(rig,tree,seed):
    direction=(rig.matrix_world@rig.pose.bones[b.PREFIX+'Head'].matrix).to_3x3()@Vector((0,-1,0));direction.normalize()
    surface,_,_,_=tree.find_nearest(seed)
    # March from a known external point to the FIRST obstruction. Distance to
    # several oral surfaces is not monotonic, so one binary search across the
    # entire ray can skip a lip and return a sphere inside another surface.
    hi=.10
    assert tree.find_nearest(surface+direction*hi)[3]>.0061,'No external contact bracket'
    lo=None
    for step in range(1,201):
        candidate=.10-step*.0005
        if tree.find_nearest(surface+direction*candidate)[3]<=.0061:
            lo=candidate;break
        hi=candidate
    assert lo is not None,'No mouth contact along external ray'
    for _ in range(20):
        distance_along=(lo+hi)/2;candidate=surface+direction*distance_along;near,n,_,distance=tree.find_nearest(candidate)
        if distance>=.0061:hi=distance_along
        else:lo=distance_along
    return surface+direction*hi

def food_seed(rig,lick,tip):
    anchor=bpy.data.objects['ANCHOR_Mouth'].matrix_world.translation.copy()
    if not lick:return anchor
    tongue=Vector(b.evaluated(bpy.data.objects['ShushuStatic_Tongue'])[0][tip])
    t=float(rig['Tongue']);t=t*t*(3-2*t)
    return anchor.lerp(tongue,t)

def oral_tree():
    points=[];triangles=[];owners=[];count=0
    for name in ['Head','Tongue','OralBowl','Nose']:
        q,t=b.evaluated(bpy.data.objects['ShushuStatic_'+name]);points.extend(q.tolist());triangles.extend((t+count).tolist());owners.extend([name]*len(t));count+=len(q)
    return BVHTree.FromPolygons(points,triangles,all_triangles=True),owners

def proxy_fixture(rig):
    """One rigid object, calibrated paw handles, independently owned contact probe.

    These are bounded geometric fixtures. No stock, consumption or product events
    are inferred from them. Food probes follow an explicit contact trajectory.
    """
    original,vertex,center=original_fixture(rig)
    scene=bpy.context.scene
    b.state(rig,{'Hold.L':1,'Hold.R':1});L=bpy.data.objects['ANCHOR_Hold.L'].matrix_world.translation.copy();R=bpy.data.objects['ANCHOR_Hold.R'].matrix_world.translation.copy()
    length=(L-R).length;parts=[]
    mat=original.data.materials[0]
    for sign in [-1,1]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,radius=.030,location=(sign*length/2,0,0));ob=bpy.context.object;group=ob.vertex_groups.new(name='Handle.'+('L' if sign==1 else 'R'));group.add(list(range(len(ob.data.vertices))),1,'REPLACE');parts.append(ob)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=.009,depth=length,rotation=(0,math.pi/2,0));parts.append(bpy.context.object)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in parts:ob.select_set(True)
    bpy.context.view_layer.objects.active=parts[-1];bpy.ops.object.join();bar=bpy.context.object;bar.name='PROOF_RigidTwoHandItem'
    # Convert the joined cylinder's local transform to canonical world geometry.
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    centers={side:np.mean([q.co for q in bar.data.vertices if any(g.group==bar.vertex_groups['Handle.'+side].index for g in q.groups)],axis=0) for side in ['L','R']}
    assert max(np.linalg.norm(centers[side]-[sign*length/2,0,0]) for side,sign in [('L',1),('R',-1)])<1e-6,'Rendered proxy handles disagree with measured coordinates'
    bar.data.materials.clear();bar.data.materials.append(mat)
    bar['role']='One rigid diagnostic item with two fixed 0.030 tangent handles; no scale animation';bar['handle_separation']=length
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,radius=.006);food=bpy.context.object;food.name='PROOF_FoodContact';food.data.materials.append(mat)
    food['role']='External spherical contact tip, radius .006; five style surface-contact capacity only, not approved food'
    b.reset(rig);head=bpy.data.objects['ShushuStatic_Head'];hp=np.array([q.co for q in head.data.vertices]);mask=(hp[:,1]<-.15)&(abs(hp[:,0])<.025)&(hp[:,2]>.545)&(hp[:,2]<.60)
    candidates=np.where(mask)[0];lip=int(candidates[np.argmin(np.linalg.norm(hp[candidates]-[0,-.278,.572],axis=1))])
    tongue=bpy.data.objects['ShushuStatic_Tongue'];tp=np.array([q.co for q in tongue.data.vertices]);tip=int(np.argmin(tp[:,1]))
    marks=p.markers();acquire=next(q['frame'] for q in marks if q['name']=='proxy-both-acquire');release=next(q['frame'] for q in marks if q['name']=='proxy-both-release')
    food_start=next(q['frame'] for q in marks if q['name']=='food-small');food_end=next(q['frame'] for q in marks if q['name']=='food-return');lick=next(q['frame'] for q in marks if q['name']=='food-lick')
    both=[];contacts=[];tracks={bar.name:[],food.name:[]};frozen=None
    for frame in range(1,scene.frame_end+1):
        if frame%120==0:print('PROXY_TRACK',frame,flush=True)
        scene.frame_set(frame);bpy.context.view_layer.update();la=bpy.data.objects['ANCHOR_Hold.L'].matrix_world.translation.copy();ra=bpy.data.objects['ANCHOR_Hold.R'].matrix_world.translation.copy()
        if frame<release:
            axis=(la-ra).normalized();bar.location=(la+ra)/2;bar.rotation_mode='QUATERNION';bar.rotation_quaternion=axis.to_track_quat('X','Z');frozen=bar.matrix_world.copy()
        else:bar.matrix_world=frozen
        bpy.context.view_layer.update()
        bar.hide_render=not(acquire<=frame<release);bar.keyframe_insert(data_path='hide_render',frame=frame)
        if acquire<=frame<release-12:
            gap=[]
            for sign,pos in [(1,la),(-1,ra)]:gap.append((bar.matrix_world@Vector((sign*length/2,0,0))-pos).length)
            both.append({'frame':frame,'handle_to_anchor_max':max(gap),'anchor_separation':(la-ra).length,'scale':list(bar.scale)})
        active=food_start<=frame<food_end
        if active:
            ob=tongue if lick<=frame<lick+12 else head;index=tip if ob==tongue else lip;tree,owners=oral_tree()
            seed=food_seed(rig,ob==tongue,tip)
            food.location=tangent_contact(rig,tree,seed)
        else:food.location=(0,-.5,.2)
        food.hide_render=not active;food.keyframe_insert(data_path='hide_render',frame=frame);bpy.context.view_layer.update()
        if active:
            near,n,triangle,distance=tree.find_nearest(food.location)
            contacts.append({'frame':frame,'state':next(x['name'] for x in reversed(marks) if x['frame']<=frame),'surface_owner':owners[triangle],'intended_region':'Tongue' if ob==tongue else 'mouth aperture','mouth_anchor_distance':float((food.location-bpy.data.objects['ANCHOR_Mouth'].matrix_world.translation).length),'sphere_surface_gap':float(distance-.006),'outside_nearest_face':bool((food.location-near).dot(n)>=0),'interpretation':'Tangent to union of head/tongue/oral bowl/nose. No solid food body, residual geometry, liquid or consumption state proof.'})
        for ob in [bar,food]:
            for channel in ['location','rotation_quaternion','scale']:ob.keyframe_insert(data_path=channel,frame=frame)
            tracks[ob.name].append(np.array(ob.matrix_world).tolist())
    b.write('proxy-contact.json',{'rigid_item':{'handle_separation':length,'radius':.030,'mesh_handle_centers':{n:q.tolist() for n,q in centers.items()},'frames':both,'limits':'Only fixed-handle span and controlled Hold endpoints; wrists/one-sided arbitrary regrasp are outside this rigid-item proof'},'food':contacts,'tracks':tracks,'visibility':'Blender hides inactive proxies. glTF lacks visibility tracks: proxy GLB contains probes throughout.'})
    assert max(row['handle_to_anchor_max'] for row in both)<.001,'Rigid grip fit failed before bake'
    assert all(0<=row['sphere_surface_gap']<.0002 and row['outside_nearest_face'] for row in contacts),'Food tangent failed before bake'
    assert all(row['mouth_anchor_distance']<.045 for row in contacts),'Food probe misses mouth region'
    scene.frame_set(1);return original,vertex,center

original_fixture=p.fixture
def proof():
    p.fixture=proxy_fixture;p.proof()
    for name in ['PROOF_RigidTwoHandItem','PROOF_FoodContact']:bpy.data.objects[name].select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(v.GLB.with_name(v.GLB.stem+'-contacts.glb')),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_force_sampling=True,export_bake_animation=True,export_anim_scene_split_object=False,export_all_influences=True,export_morph=True,export_morph_animation=True,export_optimize_animation_size=False,export_extras=True)

def contact_roundtrip():
    data=json.loads((v.OUT/'proxy-contact.json').read_text());p.import_saved(v.GLB.with_name(v.GLB.stem+'-contacts.glb'));rows=[]
    for name,track in data['tracks'].items():
        ob=bpy.data.objects[name]
        for frame,expected in enumerate(track,1):
            bpy.context.scene.frame_set(frame);rows.append({'object':name,'frame':frame,'matrix_error':float(np.max(abs(np.array(ob.matrix_world)-np.array(expected))))})
    b.write('contact-roundtrip.json',rows);assert max(x['matrix_error'] for x in rows)<1e-5,'Contact proxy transform mismatch'
    assert max(x['handle_to_anchor_max'] for x in data['rigid_item']['frames'])<.001,'Rigid handle span exceeds proof tolerance'
    assert all(0<=x['sphere_surface_gap']<.0002 and x['outside_nearest_face'] for x in data['food']),'Food contact proxy invalid'
    print('CONTACT_ROUNDTRIP_PASS',flush=True)

def proxy_clearance():
    bpy.ops.wm.open_mainfile(filepath=str(v.PROOF));scene=bpy.context.scene;bar=bpy.data.objects['PROOF_RigidTwoHandItem'];food=bpy.data.objects['PROOF_FoodContact'];data=json.loads((v.OUT/'proxy-contact.json').read_text());rows=[]
    span=data['rigid_item']['handle_separation'];frames=[row['frame'] for row in data['rigid_item']['frames']]
    for frame in frames:
        scene.frame_set(frame)
        for side,sign in [('L',1),('R',-1)]:
            center=bar.matrix_world@Vector((sign*span/2,0,0));q,t=b.evaluated(bpy.data.objects['ShushuStatic_Paw_'+side]);tree=BVHTree.FromPolygons(q.tolist(),t.tolist(),all_triangles=True);point,normal,_,distance=tree.find_nearest(center)
            rows.append({'frame':frame,'part':'handle-'+side,'owner':'Paw_'+side,'clearance':float(distance-.030),'outside_nearest_face':bool((center-point).dot(normal)>=0)})
    for contact in data['food']:
        scene.frame_set(contact['frame']);center=food.matrix_world.translation
        for name in ['Head','Tongue','OralBowl','Nose']:
            q,t=b.evaluated(bpy.data.objects['ShushuStatic_'+name]);tree=BVHTree.FromPolygons(q.tolist(),t.tolist(),all_triangles=True);point,normal,_,distance=tree.find_nearest(center)
            rows.append({'frame':contact['frame'],'part':'food','owner':name,'clearance':float(distance-.006),'outside_nearest_face':bool((center-point).dot(normal)>=0),'state':contact['state']})
    b.write('proxy-clearance.json',rows);assert min(row['clearance'] for row in rows)>-.0002,'Proxy overlaps surface'
    print('PROXY_CLEARANCE_PASS',min(row['clearance'] for row in rows),flush=True)

def preview():
    before='--before' in sys.argv
    rig,meshes=v.load(v.V001 if before else v.ASSET);scene,cam=b.setup_review(640,16)
    names=sys.argv[sys.argv.index('--names')+1].split(',') if '--names' in sys.argv else ['seat-entry','seat-mid','seat','seat-rest','seat-joy','seat-lowhead','seat-shift-L','seat-shift-R']
    folder=v.OUT/'renders'/('before' if before else 'candidate');folder.mkdir(parents=True,exist_ok=True)
    for row in p.markers():
        if row['name'] not in names:continue
        b.state(rig,row['controls'])
        for view,d in p.VIEWS:
            if '--quick' in sys.argv and view not in ['front','left']:continue
            p.camera(cam,d);scene.render.filepath=str(folder/(row['name']+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
        print('RENDERED',row['name'],flush=True)

def audit_new():
    rig,meshes=v.load(v.ASSET);b.reset(rig);neutral=p.positions(meshes)
    isolation=[];stroke=[]
    for zone in range(4):
        track=[]
        for u in np.linspace(-1,1,21):
            values={'StrokeZone':zone,'StrokeU':float(u),'StrokeV':float(u*.5),'StrokePressure':1,'Seat':1,'Hold.L':1,'HeadPitch':.8,'Blink.R':.5}
            b.state(rig,{k:val for k,val in values.items() if k!='StrokePressure'});base=p.positions(meshes)
            b.state(rig,values);now=p.positions(meshes)
            diffs={name:np.linalg.norm(now[name]-base[name],axis=1) for name in base}
            owner='ShushuStatic_'+v.ZONES[zone][1];d=diffs[owner];points=now[owner];active=d>1e-5
            centroid=(points*d[:,None]).sum(0)/max(d.sum(),1e-12)
            track.append({'u':float(u),'centroid_world':centroid.tolist(),'peak':float(d.max()),'active_vertices':int(active.sum()),'protected_max':max(float(q.max()) for n,q in diffs.items() if n!=owner)})
        stroke.append({'zone':zone,'path':track,'centroid_travel':float(np.linalg.norm(np.array(track[-1]['centroid_world'])-np.array(track[0]['centroid_world'])))})
    for side in ['L','R']:
        for seat in [0,.5,1]:
            for mode,requests in [('hold',{'Hold.'+side:1}),('self',{'SelfContact.'+side:1})]:
                b.state(rig,{'Seat':seat,**requests});single=p.positions(meshes);anchor=np.array(bpy.data.objects['ANCHOR_Hold.'+side].matrix_world)
                combined={**requests,'Offer.'+side:1}
                if mode=='hold':combined['SelfContact.'+side]=1
                b.state(rig,{'Seat':seat,**combined});now=p.positions(meshes)
                isolation.append({'side':side,'seat':seat,'owner':mode,'request':combined,'geometry_difference_max':max(float(np.linalg.norm(now[n]-single[n],axis=1).max()) for n in now),'anchor_difference_max':float(np.max(np.abs(np.array(bpy.data.objects['ANCHOR_Hold.'+side].matrix_world)-anchor)))})
    support=[];torso=bpy.data.objects['ShushuStatic_Torso'];rest=np.array([q.co for q in torso.data.vertices]);soles=rest[:,2]<.015
    for shift in [-1,0,1]:
        for t in np.linspace(0,1,81):
            b.state(rig,{'Seat':float(t),'WeightShift':shift});q,_=b.evaluated(torso)
            support.append({'seat':float(t),'shift':shift,'min_z':float(q[:,2].min()),'below_minus_001':int((q[:,2]<-.001).sum()),'sole_xy_drift':float(np.linalg.norm(q[soles,:2]-neutral[torso.name][soles,:2],axis=1).max())})
    b.reset(rig);ret=p.positions(meshes)
    returns={n:float(np.linalg.norm(ret[n]-neutral[n],axis=1).max()) for n in ret}
    b.write('v002-capability.json',{'stroke':stroke,'arbitration':isolation,'support':support,'neutral_return':returns})
    assert max(x['geometry_difference_max'] for x in isolation)<1e-6,'Reach arbitration mismatch'
    assert all(x['below_minus_001']==0 for x in support),'Floor penetration'
    assert max(x['sole_xy_drift'] for x in support)<1e-5,'Sole drift'
    assert all(row['protected_max']<1e-6 and row['peak']>1e-4 for z in stroke for row in z['path']),'Stroke missing or leaking'
    print('V002_AUDIT_PASS',flush=True)

def audit_face():
    rig,meshes=v.load(v.ASSET);rows=[]
    cases=[('seat-low-closed',{'Seat':1,'HeadPitch':1,'Blink.L':1,'Blink.R':1}),('seat-shift-L-joy',{'Seat':1,'WeightShift':1,'HeadRoll':-.5,'Joy':1}),('seat-shift-R-joy',{'Seat':1,'WeightShift':-1,'HeadRoll':.5,'Joy':1}),('extreme-closed',dict(EXTRA[7][1]))]
    for name,values in cases:
        b.state(rig,values);occluders=[]
        for obj in meshes:
            if obj.name.endswith(('Head','LidWall_L','LidWall_R','Nose','Ear_L','Ear_R')):
                q,t=b.evaluated(obj);occluders.append(BVHTree.FromPolygons(q.tolist(),t.tolist(),all_triangles=True))
        for side in ['L','R']:
            q,_=b.evaluated(bpy.data.objects['ShushuStatic_Eye_'+side])
            for view,direction in p.VIEWS:
                d=Vector(direction).normalized();visible=sum(not any((hit:=tree.ray_cast(Vector(point)+d*3,-d,3.00001))[0] is not None and hit[3]<2.99998 for tree in occluders) for point in q)
                rows.append({'state':name,'part':'Eye_'+side,'view':view,'potentially_visible':int(visible)})
        if values.get('MouthClose'):
            q,t=b.evaluated(bpy.data.objects['ShushuStatic_Head']);tree=BVHTree.FromPolygons(q.tolist(),t.tolist(),all_triangles=True)
            for part in ['Tongue','OralBowl']:
                q,_=b.evaluated(bpy.data.objects['ShushuStatic_'+part])
                for view,direction in p.VIEWS:
                    d=Vector(direction).normalized();visible=0
                    for point in q:
                        hit=tree.ray_cast(Vector(point)+d*3,-d,3.00001);visible+=hit[0] is None or hit[3]>=2.99998
                    rows.append({'state':name,'part':part,'view':view,'potentially_visible':int(visible)})
    b.write('composed-face-occlusion.json',{'method':'Conservative eye/oral surface vertex rays under composed low head, support shifts and extreme requests; inspect renders separately for appeal','rows':rows})
    assert all(row['potentially_visible']==0 for row in rows),'Composed closed surface leaked'
    print('COMPOSED_FACE_PASS',flush=True)

def audit_grip():
    rig,meshes=v.load(v.ASSET);rows=[]
    for seat in [0,.5,1]:
        for shift in [-1,-.7,0,.7,1]:
            b.state(rig,{'Seat':seat,'WeightShift':shift,'Hold.L':1,'Hold.R':1})
            L=bpy.data.objects['ANCHOR_Hold.L'];R=bpy.data.objects['ANCHOR_Hold.R'];rows.append({'seat':seat,'shift':shift,'span':(L.matrix_world.translation-R.matrix_world.translation).length,'fit_values':{key:float(rig[key]) for key in rig.keys() if key.startswith('GripFit')},'valid_drivers':all(fc.driver.is_valid for ob in [rig,L,R] for fc in ob.animation_data.drivers)})
    b.write('grip-audit.json',rows);print('GRIP_AUDIT',flush=True)
    assert max(abs(row['span']-rows[2]['span']) for row in rows)<.001,'Grip span outside tolerance'
    assert all(row['valid_drivers'] for row in rows),'Invalid grip driver'

def audit_food():
    rig,meshes=v.load(v.ASSET);rows=[];scene,cam=b.setup_review(640,12)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,radius=.006);probe=bpy.context.object;probe.name='CONTACT_Probe';mat=bpy.data.materials.new('Contact orange');mat.diffuse_color=(1,.25,.02,1);probe.data.materials.append(mat)
    for name,values in PROXY_EVENTS:
        if name not in ['food-small','food-lick','food-drink']:continue
        b.state(rig,values);ob=bpy.data.objects['ShushuStatic_Tongue' if name=='food-lick' else 'ShushuStatic_Head'];q,tris=b.evaluated(ob);tree,owners=oral_tree()
        seed=Vector(q[np.argmin(q[:,1])]) if name=='food-lick' else bpy.data.objects['ANCHOR_Mouth'].matrix_world.translation
        probe.location=tangent_contact(rig,tree,seed);bpy.context.view_layer.update();near,n,_,distance=tree.find_nearest(probe.location);anchor=bpy.data.objects['ANCHOR_Mouth'].matrix_world.translation
        rows.append({'state':name,'anchor':list(anchor),'probe':list(probe.location),'gap':distance-.006,'mouth_distance':(probe.location-anchor).length,'outside':(probe.location-near).dot(n)>=0})
        folder=v.OUT/'renders/contact-calibration';folder.mkdir(exist_ok=True)
        for view,d in [('front',(0,-1,0)),('left',(-1,0,0))]:p.camera(cam,d);scene.render.filepath=str(folder/(name+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
    b.write('food-calibration.json',rows);assert all(0<=row['gap']<.0002 and row['mouth_distance']<.045 and row['outside'] for row in rows),'Food calibration failed'
    print('FOOD_CALIBRATION_PASS',flush=True)

def audit_food_transitions():
    rig,meshes=v.load(v.ASSET);rows=[];tongue=bpy.data.objects['ShushuStatic_Tongue'];tip=int(np.argmin(np.array([q.co for q in tongue.data.vertices])[:,1]))
    events=[q for q in PROXY_EVENTS if q[0].startswith('food-')]
    for i,(name,values) in enumerate(events[:-1]):
        next_values=events[i+1][1]
        for step in range(12):
            t=step/12;controls={k:values.get(k,0)*(1-t)+next_values.get(k,0)*t for k in set(values)|set(next_values)}
            b.state(rig,controls);tree,owners=oral_tree();center=tangent_contact(rig,tree,food_seed(rig,name=='food-lick',tip));point,normal,triangle,distance=tree.find_nearest(center)
            rows.append({'state':name,'step':step,'gap':distance-.006,'outside':bool((center-point).dot(normal)>=0),'mouth_distance':(center-bpy.data.objects['ANCHOR_Mouth'].matrix_world.translation).length,'owner':owners[triangle]})
    b.write('food-transition-preflight.json',rows)
    assert all(0<=r['gap']<.0002 and r['outside'] and r['mouth_distance']<.045 for r in rows),'Food transitions fail'
    print('FOOD_TRANSITION_PASS',len(rows),min(r['gap'] for r in rows),max(r['mouth_distance'] for r in rows),flush=True)

def render():
    setup=b.setup_review
    b.setup_review=lambda size,samples:setup(size,16)
    p.render()
    conditions=json.loads((v.OUT/'render-conditions.json').read_text())
    conditions.update(samples=16,source='v001/v002/approved-static and GLB: fixed identical cameras, lights, samples; capability witnesses, Human PENDING')
    b.write('render-conditions.json',conditions)

def inheritance():
    source,meshes=v.load(v.V001);b.reset(source);neutral=p.positions(meshes)
    basis={o.name:np.array([q.co for q in o.data.vertices]) for o in meshes}
    uv={o.name:np.array([q.uv for q in o.data.uv_layers.active.data]) for o in meshes}
    triangles={o.name:[tuple(q.vertices) for q in o.data.polygons] for o in meshes}
    bones={q.name:np.array(q.matrix_local) for q in source.data.bones}
    b.state(source,{'Blink.L':1,'Blink.R':1});closed=p.positions(meshes)
    rig,meshes=v.load(v.ASSET);b.reset(rig);now=p.positions(meshes);rows=[]
    for o in meshes:
        rows.append({'mesh':o.name,'basis_max':float(np.abs(np.array([q.co for q in o.data.vertices])-basis[o.name]).max()),'neutral_world_max':float(np.linalg.norm(now[o.name]-neutral[o.name],axis=1).max()),'uv_exact':bool(np.array_equal(uv[o.name],np.array([q.uv for q in o.data.uv_layers.active.data]))),'topology_exact':triangles[o.name]==[tuple(q.vertices) for q in o.data.polygons]})
    b.state(rig,{'Blink.L':1,'Blink.R':1});now=p.positions(meshes)
    for row in rows:row['closed_world_max']=float(np.linalg.norm(now[row['mesh']]-closed[row['mesh']],axis=1).max())
    bone_match=set(bones)==set(q.name for q in rig.data.bones) and all(np.array_equal(bones[q.name],np.array(q.matrix_local)) for q in rig.data.bones)
    b.write('v001-inheritance.json',{'source_sha256':b.sha(v.V001),'v002_sha256':b.sha(v.ASSET),'bone_rest_exact':bool(bone_match),'rows':rows})
    assert bone_match and all(r['basis_max']==0 and r['neutral_world_max']<1e-6 and r['closed_world_max']<1e-6 and r['uv_exact'] and r['topology_exact'] for r in rows),'Inherited identity/endpoints changed'
    print('V001_INHERITANCE_PASS',flush=True)

if __name__=='__main__':
    if '--preview' in sys.argv:preview()
    elif '--new-audit' in sys.argv:audit_new()
    elif '--face-audit' in sys.argv:audit_face()
    elif '--grip-audit' in sys.argv:audit_grip()
    elif '--food-audit' in sys.argv:audit_food()
    elif '--food-transitions' in sys.argv:audit_food_transitions()
    elif '--inheritance' in sys.argv:inheritance()
    elif '--audit' in sys.argv:p.audit()
    elif '--proof' in sys.argv:proof()
    elif '--contact-roundtrip' in sys.argv:contact_roundtrip()
    elif '--proxy-clearance' in sys.argv:proxy_clearance()
    elif '--roundtrip' in sys.argv:p.roundtrip()
    elif '--fixture-check' in sys.argv:p.fixture_check()
    else:render()
