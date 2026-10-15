"""v004 inheritance, support, editable/baked Skin/Morph/Anchor proof."""
import bpy,sys,json,importlib.util,math
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
def module(n,f):
    sp=importlib.util.spec_from_file_location(n,ROOT/f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
v=module('v004','scripts/blender/build-shushu-production-rig-v004.py')
q=module('proof003','scripts/blender/prove-shushu-production-rig-v003.py')
p=q.p;b=q.b
b.OUT=v.OUT;b.ASSET=v.ASSET;b.PROOF=v.PROOF;b.GLB=v.GLB
p.OUT=v.OUT;p.RENDERS=v.OUT/'renders';p.VIEWS=v.VIEWS
v.b.evaluated=q.evaluated;b.evaluated=q.evaluated
inherited=list(p.EVENTS)
frames=[1,13,31,49,67,79,103,121,145,169]
timeline=[{'frame':f,'name':n,'controls':c} for f,(n,c) in zip(frames,v.STATES)]
timeline += [{'frame':181+i*8,'name':'cap-'+n,'controls':c} for i,(n,c) in enumerate(inherited)]
# The reusable fixture proof identifies these events by exact name.
for row in timeline:
    if row['name'] in ['cap-hold-L','cap-hold-resume','cap-release']:row['name']=row['name'][4:]
p.markers=lambda:timeline
p.FRAME_STEP=8
def focused():
    rig,meshes=v.load(v.SOURCE);neutral=p.positions(meshes)
    identity={o.name:{'basis':np.array([x.co for x in o.data.vertices]),'uv':np.array([x.uv for x in o.data.uv_layers.active.data]),'faces':[tuple(x.vertices) for x in o.data.polygons],'keys':{k.name:np.array([x.co for x in k.data]) for k in o.data.shape_keys.key_blocks} if o.data.shape_keys else {},'tex':p.texture_bytes(o)} for o in meshes}
    bones={x.name:np.array(x.matrix_local) for x in rig.data.bones};props=set(rig.keys());old={};oldhead={}
    for name,values in inherited+v.COMPOSE:
        b.state(rig,values);old[name]=p.positions(meshes);oldhead[name]=np.array(rig.matrix_world@rig.pose.bones[b.PREFIX+'Head'].matrix)
    rig,meshes=v.load();now=p.positions(meshes);rows=[]
    for o in meshes:
        a=identity[o.name];keys=o.data.shape_keys.key_blocks if o.data.shape_keys else []
        rows.append({'mesh':o.name,'basis_delta':float(abs(np.array([x.co for x in o.data.vertices])-a['basis']).max()),'neutral_delta':float(np.linalg.norm(now[o.name]-neutral[o.name],axis=1).max()),'uv_exact':bool(np.array_equal(np.array([x.uv for x in o.data.uv_layers.active.data]),a['uv'])),'faces_exact':[tuple(x.vertices) for x in o.data.polygons]==a['faces'],'textures_exact':p.texture_bytes(o)==a['tex'],'retained_key_delta':max([float(abs(np.array([x.co for x in k.data])-a['keys'][k.name]).max()) for k in keys if k.name in a['keys']],default=0),'removed':[n for n in a['keys'] if n not in keys]})
    v.write('inheritance.json',{'rows':rows,'rest_bones_exact':all(np.array_equal(bones[x.name],np.array(x.matrix_local)) for x in rig.data.bones),'controls_retained':props<=set(rig.keys())})
    regression=[]
    for name,values in inherited+v.COMPOSE:
        b.state(rig,values);now=p.positions(meshes);newhead=np.array(rig.matrix_world@rig.pose.bones[b.PREFIX+'Head'].matrix);registration=oldhead[name]@np.linalg.inv(newhead)
        face={}
        for n,points in now.items():
            if any(s in n for s in ['Torso','Paw_','Ear_']):continue
            registered=points@registration[:3,:3].T+registration[:3,3];face[n]=float(np.linalg.norm(registered-old[name][n],axis=1).max())
        regression.append({'state':name,'head_registered_face':face,'non_torso_world_delta':{n:float(np.linalg.norm(now[n]-old[name][n],axis=1).max()) for n in now if not n.endswith('Torso')},'pose_changed':values.get('Seat',0)>0})
    v.write('v003-face-regression.json',regression)
    o=bpy.data.objects['ShushuStatic_Torso'];rest=np.array([x.co for x in o.data.vertices]);support=[]
    for shift in [-1,-.5,0,.5,1]:
        for seat in np.linspace(0,1,101):
            b.state(rig,{'Seat':float(seat),'WeightShift':float(shift)});points,_=b.evaluated(o);feet={}
            for side,s in [('L',1),('R',-1)]:
                mask=(rest[:,0]*s>0)&(rest[:,2]<.095);sole=(rest[:,0]*s>0)&(rest[:,2]<.015)
                # Distances within the approved whole foot prove no flattening/lengthening.
                a=rest[mask];aa=points[mask];ids=np.linspace(0,len(a)-1,32,dtype=int)
                footbone=rig.pose.bones[b.PREFIX+('Left' if s>0 else 'Right')+'Foot'];mat=np.array(footbone.matrix@footbone.bone.matrix_local.inverted());expected=a@mat[:3,:3].T+mat[:3,3]
                feet[side]={'min_z':float(aa[:,2].min()),'center':aa.mean(0).tolist(),'sole_center':points[sole].mean(0).tolist(),'rigid_error':float(np.linalg.norm(aa-expected,axis=1).max()),'pair_distance_error':float(abs(np.linalg.norm(aa[ids,None]-aa[None,ids],axis=2)-np.linalg.norm(a[ids,None]-a[None,ids],axis=2)).max())}
            rump=(rest[:,1]>.08)&(rest[:,2]>.12)&(rest[:,2]<.24)&(abs(rest[:,0])<.13)
            support.append({'seat':float(seat),'shift':shift,'floor':float(points[:,2].min()),'below_minus_001':int((points[:,2]<-.001).sum()),'rump_min':float(points[rump,2].min()),'rump_near_floor':int((points[rump,2]<.004).sum()),'feet':feet,'finite':bool(np.isfinite(points).all())})
    b.reset(rig);returns={n:float(np.linalg.norm(points-neutral[n],axis=1).max()) for n,points in p.positions(meshes).items()}
    invalid=[]
    for idblock in list(bpy.data.objects)+list(bpy.data.shape_keys):
        if idblock.animation_data:
            invalid += [{'id':idblock.name,'path':fc.data_path,'expression':fc.driver.expression} for fc in idblock.animation_data.drivers if not fc.is_valid]
    v.write('support-regression.json',{'samples':support,'neutral_return':returns,'invalid_drivers':invalid})
    assert all(r['basis_delta']==0 and r['neutral_delta']<1e-6 and r['uv_exact'] and r['faces_exact'] and r['textures_exact'] and r['retained_key_delta']==0 for r in rows),'Identity inheritance changed'
    assert max(max(r['head_registered_face'].values()) for r in regression)<2e-6,'Facial shape regression'
    assert not invalid,'Invalid driver'
    assert all(r['below_minus_001']==0 and r['finite'] for r in support),'Support floor failure'
    assert max(returns.values())<1e-6,'Neutral return failed'
    print('FOCUSED_PASS',flush=True)
def render():
    saved='--saved' in sys.argv
    if saved:p.import_saved(v.GLB);rig=None
    else:rig,meshes=v.load()
    scene,cam=b.setup_review(512,16);folder=v.OUT/('detail' if '--detail' in sys.argv else 'renders')/('reimport' if saved else 'candidate');folder.mkdir(parents=True,exist_ok=True)
    names=sys.argv[sys.argv.index('--names')+1].split(',') if '--names' in sys.argv else None
    for name,values in v.STATES+v.COMPOSE:
        if names and name not in names:continue
        if saved:
            mark=next((r for r in timeline if r['name']==name or r['name']=='cap-'+name),None)
            if not mark:continue
            scene.frame_set(mark['frame'])
        else:b.state(rig,values)
        views=[x for x in v.VIEWS if x[0] in ('front','3q-L','3q-R','left','right')] if '--detail' in sys.argv else v.VIEWS
        for view,d in views:
            if '--detail' in sys.argv:v.v.camera(cam,d,(0,.015*values.get('Seat',0),.715-.116*values.get('Seat',0)),.56)
            else:v.v.camera(cam,d)
            scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
        print('RENDERED',name,flush=True)
def video_frames():
    bpy.ops.wm.open_mainfile(filepath=str(v.PROOF));scene,cam=b.setup_review(448,12);folder=v.OUT/'sequence';folder.mkdir(exist_ok=True)
    v.v.camera(cam,(-.65,-.76,.03))
    for f in range(1,170,6):
        scene.frame_set(f);scene.render.filepath=str(folder/f'{f:04}.png');bpy.ops.render.render(write_still=True)
def composition_frames():
    bpy.ops.wm.open_mainfile(filepath=str(v.PROOF));scene,cam=b.setup_review(448,12);folder=v.OUT/'composition-sequence';folder.mkdir(exist_ok=True)
    v.v.camera(cam,(-.65,-.76,.03))
    # Consecutive saved-action samples: low head, both shifts and occupied-paw
    # arbitration. These are a separate continuous excerpt, not spliced motion.
    for f in range(589,622,4):
        scene.frame_set(f);scene.render.filepath=str(folder/f'{f:04}.png');bpy.ops.render.render(write_still=True)
def capabilities():
    q.q.v.ASSET=v.ASSET;q.q.v.OUT=v.OUT
    q.q.audit_grip();q.q.audit_face()
    rig,meshes=v.load();neutral=p.positions(meshes);rows=[];strokes=[]
    # Existing independent channels, including target orientation, remain usable.
    for side in ['L','R']:
        for seat in [0,.5,1]:
            for mode,req in [('Hold',{'Hold.'+side:1}),('SelfContact',{'SelfContact.'+side:1})]:
                b.state(rig,{'Seat':seat,**req});single=p.positions(meshes)
                b.state(rig,{'Seat':seat,**req,'Offer.'+side:1,**({'SelfContact.'+side:1} if mode=='Hold' else {})});now=p.positions(meshes)
                rows.append({'side':side,'seat':seat,'mode':mode,'arbitration_error':max(float(np.linalg.norm(now[n]-single[n],axis=1).max()) for n in now)})
    for zone in range(4):
        for u in [-1,0,1]:
            values={'Seat':1,'StrokeZone':zone,'StrokeU':u,'Hold.L':1}
            b.state(rig,values);base=p.positions(meshes);b.state(rig,{**values,'StrokePressure':1});now=p.positions(meshes);owner='ShushuStatic_'+q.q.v.ZONES[zone][1]
            strokes.append({'zone':zone,'u':u,'owner_movement':float(np.linalg.norm(now[owner]-base[owner],axis=1).max()),'other_movement':max(float(np.linalg.norm(now[n]-base[n],axis=1).max()) for n in now if n!=owner)})
    feet=[]
    for side,longname in [('L','Left'),('R','Right')]:
        for seat in [0,1]:
            for channel in ['FootLift','FootSide','FootForward']:
                b.state(rig,{'Seat':seat});base=p.positions(meshes);b.state(rig,{'Seat':seat,channel+'.'+side:1});now=p.positions(meshes)
                feet.append({'side':side,'seat':seat,'control':channel,'torso_movement':float(np.linalg.norm(now['ShushuStatic_Torso']-base['ShushuStatic_Torso'],axis=1).max()),'head_movement':float(np.linalg.norm(now['ShushuStatic_Head']-base['ShushuStatic_Head'],axis=1).max())})
            b.state(rig,{'Seat':seat});target=bpy.data.objects['CTRL_Foot.'+longname];restq=target.rotation_quaternion.copy();base=p.positions(meshes);target.rotation_quaternion=restq@Vector((1,0,0)).rotation_difference(Vector((1,.1,0)));target.update_tag();bpy.context.view_layer.update();now=p.positions(meshes)
            feet.append({'side':side,'seat':seat,'control':'free target rotation','torso_movement':float(np.linalg.norm(now['ShushuStatic_Torso']-base['ShushuStatic_Torso'],axis=1).max()),'head_movement':float(np.linalg.norm(now['ShushuStatic_Head']-base['ShushuStatic_Head'],axis=1).max())});target.rotation_quaternion=restq
    v.write('capability-regression.json',{'arbitration':rows,'stroke':strokes,'feet':feet,'limits':'Bounded witnesses. Arbitrary FK, real items and smartphone runtime remain unverified.'})
    assert max(r['arbitration_error'] for r in rows)<1e-6
    assert all(r['other_movement']<1e-6 and r['owner_movement']>1e-4 for r in strokes)
    assert all(r['head_movement']<1e-6 and r['torso_movement']>.001 for r in feet)
    print('CAPABILITY_PASS',flush=True)
if __name__=='__main__':
    if '--focused' in sys.argv:focused()
    elif '--proof' in sys.argv:p.proof()
    elif '--roundtrip' in sys.argv:p.roundtrip()
    elif '--render' in sys.argv:render()
    elif '--sequence' in sys.argv:video_frames()
    elif '--composition-sequence' in sys.argv:composition_frames()
    elif '--capabilities' in sys.argv:capabilities()
