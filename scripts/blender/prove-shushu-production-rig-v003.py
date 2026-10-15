"""Focused support/face regression and saved glTF proof; immutable v002 input."""
import bpy,sys,json,importlib.util
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
def module(name,path):
    sp=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
v=module('v003','scripts/blender/build-shushu-production-rig-v003.py')
q=module('proof_v002','scripts/blender/prove-shushu-production-rig-v002.py')
p=q.p;b=q.b
q.v.OUT=v.OUT;q.v.ASSET=v.ASSET;q.v.PROOF=v.PROOF;q.v.GLB=v.GLB
b.OUT=v.OUT;b.ASSET=v.ASSET;b.PROOF=v.PROOF;b.GLB=v.GLB
p.OUT=v.OUT;p.RENDERS=v.OUT/'renders';p.VIEWS=v.VIEWS
def evaluated(o):
    bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles()
    points=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',points)
    matrix=np.array(ev.matrix_world);points=points.reshape(-1,3)@matrix[:3,:3].T+matrix[:3,3]
    triangles=np.empty(len(me.loop_triangles)*3,dtype=np.int32);me.loop_triangles.foreach_get('vertices',triangles)
    ev.to_mesh_clear();return points,triangles.reshape(-1,3)
b.evaluated=evaluated;v.b.evaluated=evaluated
def focused():
    rig,meshes=v.load(v.SOURCE);neutral=p.positions(meshes)
    baseline={name:p.positions(meshes) for name in []}
    controls=q.p.EVENTS
    for name,values in controls:
        b.state(rig,values);baseline[name]=p.positions(meshes)
    identity={o.name:{'basis':np.array([x.co for x in o.data.vertices]),'uv':np.array([x.uv for x in o.data.uv_layers.active.data]),'faces':[tuple(x.vertices) for x in o.data.polygons],'keys':{k.name:np.array([x.co for x in k.data]) for k in o.data.shape_keys.key_blocks} if o.data.shape_keys else {},'weights':[{o.vertex_groups[g.group].name:float(g.weight) for g in x.groups} for x in o.data.vertices]} for o in meshes}
    bones={x.name:np.array(x.matrix_local) for x in rig.data.bones};control_names=set(rig.keys())
    rig,meshes=v.load(v.ASSET);now=p.positions(meshes);rows=[]
    for o in meshes:
        old=identity[o.name];keys=o.data.shape_keys.key_blocks if o.data.shape_keys else []
        retained={k.name:float(abs(np.array([x.co for x in k.data])-old['keys'][k.name]).max()) for k in keys if k.name in old['keys']}
        missing=[name for name in old['keys'] if name not in keys]
        weights=[{o.vertex_groups[g.group].name:float(g.weight) for g in x.groups} for x in o.data.vertices]
        rows.append({'mesh':o.name,'basis_delta':float(abs(np.array([x.co for x in o.data.vertices])-old['basis']).max()),'neutral_world_delta':float(np.linalg.norm(now[o.name]-neutral[o.name],axis=1).max()),'uv_exact':bool(np.array_equal(old['uv'],np.array([x.uv for x in o.data.uv_layers.active.data]))),'faces_exact':old['faces']==[tuple(x.vertices) for x in o.data.polygons],'retained_key_max_delta':max(retained.values(),default=0),'removed_keys':missing,'added_keys':[k.name for k in keys if k.name not in old['keys']],'weight_changed_vertices':sum(a!=bb for a,bb in zip(old['weights'],weights))})
    b.write('inheritance.json',{'source_sha256':b.sha(v.SOURCE),'v003_sha256':b.sha(v.ASSET),'rows':rows,'bone_rest_exact':all(np.array_equal(bones[x.name],np.array(x.matrix_local)) for x in rig.data.bones),'rig_controls_retained':control_names<=set(rig.keys())})
    # Reload after the final source comparison above; no stale object references.
    rig,meshes=v.load(v.ASSET);regression=[]
    targets={'seat-lowhead','seat-shift-L'}
    for name,values in controls:
        b.state(rig,values);now=p.positions(meshes)
        regression.append({'state':name,'non_torso':{n:float(np.linalg.norm(now[n]-baseline[name][n],axis=1).max()) for n in now if not n.endswith('Torso')},'eye_correction_values':{o.name:{k.name:float(k.value) for k in o.data.shape_keys.key_blocks if k.name.startswith('Corrective.EyeIntegrity')} for o in meshes if o.data.shape_keys}})
    b.write('v002-regression.json',regression)
    # Do not infer pass from only a few seated endpoint samples.
    o=bpy.data.objects['ShushuStatic_Torso'];rest=np.array([x.co for x in o.data.vertices]);support=[]
    b.reset(rig);reference=b.evaluated(o)[0]
    for shift in [-1,-.5,0,.5,1]:
        for seat in np.linspace(0,1,81):
            b.state(rig,{'Seat':float(seat),'WeightShift':float(shift)});points,_=b.evaluated(o);foot={}
            for side,s in [('L',1),('R',-1)]:
                mask=(rest[:,0]*s>0)&(rest[:,2]<.095);sole=(rest[:,0]*s>0)&(rest[:,2]<.015)
                foot[side]={'entire_original_foot_max_displacement':float(np.linalg.norm(points[mask]-reference[mask],axis=1).max()),'sole_max_displacement':float(np.linalg.norm(points[sole]-reference[sole],axis=1).max()),'height':float(np.ptp(points[mask,2]))}
            rump=(rest[:,1]>.08)&(rest[:,2]>.11)&(rest[:,2]<.24)&(abs(rest[:,0])<.15)
            knee={side:list(rig.pose.bones[b.PREFIX+side+'Leg'].head) for side in ['Left','Right']}
            support.append({'seat':float(seat),'shift':shift,'floor':float(points[:,2].min()),'below_minus_001':int((points[:,2]<-.001).sum()),'rump_min':float(points[rump,2].min()),'feet':foot,'knees':knee,'finite':bool(np.isfinite(points).all())})
    b.reset(rig);returns=p.positions(meshes)
    b.write('support-regression.json',{'samples':support,'neutral_return':{n:float(np.linalg.norm(returns[n]-neutral[n],axis=1).max()) for n in returns}})
    assert all(row['basis_delta']==0 and row['neutral_world_delta']<1e-6 and row['uv_exact'] and row['faces_exact'] and row['retained_key_max_delta']==0 for row in rows),'Inherited identity or morph changed'
    assert all(row['below_minus_001']==0 and row['finite'] for row in support),'Support floor/finite failure'
    assert max(f['entire_original_foot_max_displacement'] for row in support for f in row['feet'].values())<1e-5,'Original foot lost rigid volume'
    protected=[row for row in regression if row['state'] not in targets]
    assert all(max(row['non_torso'].values())<1e-6 for row in protected),'Unrequested face/limb expression changed'
    print('FOCUSED_PASS',flush=True)
def render_saved():
    p.import_saved(v.GLB);scene,cam=b.setup_review(640,16);folder=v.OUT/'renders/reimport';folder.mkdir(parents=True,exist_ok=True)
    for mark in p.markers():
        if mark['name'] not in {'neutral','seat-mid','seat','seat-rest','seat-lowhead','seat-shift-L','standing-return'}:continue
        scene.frame_set(mark['frame'])
        for view,d in v.VIEWS:
            v.camera(cam,d);scene.render.filepath=str(folder/(mark['name']+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
        print('SAVED_RENDER',mark['name'],flush=True)
if __name__=='__main__':
    if '--focused' in sys.argv:focused()
    elif '--audit' in sys.argv:p.audit();q.audit_new();q.audit_grip();q.audit_face()
    elif '--proof' in sys.argv:p.proof()
    elif '--roundtrip' in sys.argv:p.roundtrip()
    elif '--render-saved' in sys.argv:render_saved()
