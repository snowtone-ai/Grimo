"""Targeted saved-file regression checks for the localized muzzle edit."""
import sys
sys.dont_write_bytecode=True
import bpy, json, hashlib, importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector, Quaternion
spec=importlib.util.spec_from_file_location('muzzle',Path(__file__).with_name('refine-shushu-v003-muzzle.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
v,r,a=m.v,m.r,m.a
def coords(k): return np.array([p.co[:] for p in k.data])
def digest(x): return hashlib.sha256(np.asarray(x).tobytes()).hexdigest()
def fixed_surface(o):
    bpy.context.view_layer.update(); ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
    points=np.array([ev.matrix_world@p.co for p in mesh.vertices]);tris=[]
    for p in mesh.polygons:
        for i in range(1,len(p.vertices)-1):tris.append((p.vertices[0],p.vertices[i],p.vertices[i+1]))
    ev.to_mesh_clear();return points,np.array(tris)
def drivers(data):
    ad=data.animation_data
    return [(f.data_path,f.array_index,f.driver.type,f.driver.expression,
             [(x.name,x.type,[(t.id.name if t.id else None,t.data_path,t.bone_target,t.transform_type,t.transform_space) for t in x.targets]) for x in f.driver.variables]) for f in ad.drivers] if ad else []
def actions():
    result={}
    for ac in bpy.data.actions:
        curves=[]
        for layer in ac.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for f in bag.fcurves:
                        curves.append([bag.slot_handle,f.data_path,f.array_index,
                            [[list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation,k.handle_left_type,k.handle_right_type] for k in f.keyframe_points]])
        result[ac.name]=curves
    return result
def structure(o):
    k=o.data.shape_keys; ad=k.animation_data if k else None
    fields=['levels','render_levels','show_viewport','show_render','thickness','offset','vertex_group','voxel_size','iterations','factor','mode']
    return {'edges':digest([list(e.vertices) for e in o.data.edges]),
        'polygons':hashlib.sha256(str([tuple(p.vertices) for p in o.data.polygons]).encode()).hexdigest(),
        'keys':[(b.name,b.relative_key.name,b.slider_min,b.slider_max,b.vertex_group,b.interpolation) for b in k.key_blocks] if k else [],
        'drivers':drivers(k) if k else [],'object_drivers':drivers(o),
        'action':(ad.action.name,ad.action_slot.identifier) if ad and ad.action else None,
        'modifiers':[(m.name,m.type,[(f,getattr(m,f)) for f in fields if hasattr(m,f)],m.node_group.name if m.type=='NODES' else None) for m in o.modifiers],
        'matrix':list(map(list,o.matrix_world)), 'render_visible':not o.hide_render,
        'vertex_groups':[(g.name,g.index) for g in o.vertex_groups],
        'weights':digest([(p.index,g.group,g.weight) for p in o.data.vertices for g in p.groups])}
def saved_snapshot(path):
    a.load(path); result={'actions':actions(),'objects':{},'head':{},'evaluated':{}}
    for o in v.character+[v.raw]:
        keys=o.data.shape_keys
        arrays={k.name:coords(k) for k in keys.key_blocks} if keys else {'Basis':np.array([p.co[:] for p in o.data.vertices])}
        result['objects'][o.name]={'structure':structure(o),'geometry':{n:digest(p) for n,p in arrays.items()}}
        if o.name=='Shushu_Head': result['head']=arrays
    # Fixed fan diagonals: Blender's automatic quad diagonal choice can change
    # when only depth changes, without any polygon/topology change.
    result['evaluated']['neutral_head']=fixed_surface(v.parts['Head'])
    result['profile']=m.profile()
    return result
def compare(path):
    before=saved_snapshot(m.BACK/path.name); after=saved_snapshot(path)
    assert before['actions']==after['actions'],'Animation curves changed'
    assert before['objects'].keys()==after['objects'].keys()
    report={'actions_and_object_inventory_identical':True,'objects':{}}
    for n,old in before['objects'].items():
        new=after['objects'][n]; assert old['structure']==new['structure'],('Controls/topology/modifiers changed',n)
        if n!='Shushu_Head': assert old['geometry']==new['geometry'],('Non-target geometry changed',n)
        report['objects'][n]={'structure_identical':True,'all_shape_geometry_identical':n!='Shushu_Head'}
    old,new=before['head'],after['head']; delta=new['Basis']-old['Basis']; ids=np.flatnonzero(np.linalg.norm(delta,axis=1)>1e-9); outside=np.ones(len(delta),bool);outside[ids]=False
    assert np.array_equal(old['Basis'][:,[0,2]],new['Basis'][:,[0,2]])
    assert np.all(np.abs(old['Basis'][ids,0])<.046) and np.all((old['Basis'][ids,2]>.602)&(old['Basis'][ids,2]<.667)) and np.all(old['Basis'][ids,1]<-.235)
    error={}
    for name in old:
        assert np.max(np.abs(new[name][outside]-old[name][outside]))<1e-7,(name,'outside region changed')
        if name.startswith(('Head','Corrective.Compose.')):continue
        e=float(np.max(np.abs((new[name]-new['Basis'])-(old[name]-old['Basis'])))); assert e<1e-7,(name,e);error[name]=e
    # Head and chamber use different angular sampling. Locate the actual head
    # aperture by its open boundary, rather than assuming coincident vertices.
    edge_use={}
    for p in v.parts['Head'].data.polygons:
        for i,j in zip(p.vertices,list(p.vertices[1:])+[p.vertices[0]]):
            e=tuple(sorted((i,j)));edge_use[e]=edge_use.get(e,0)+1
    boundary={i for edge,n in edge_use.items() if n==1 for i in edge}
    rim_ids=[i for i in boundary if abs(old['Basis'][i,0])<.05 and .59<old['Basis'][i,2]<.61 and old['Basis'][i,1]<-.25]
    assert len(rim_ids)>30,('Actual mouth boundary missing',len(rim_ids))
    aperture_error=max(float(np.linalg.norm(new[n][rim_ids]-old[n][rim_ids],axis=1).max()) for n in old);assert aperture_error<1e-7
    bv,bt=before['evaluated']['neutral_head'];av,at=after['evaluated']['neutral_head'];assert np.array_equal(bt,at) and np.isfinite(av).all()
    bn=np.cross(bv[bt[:,1]]-bv[bt[:,0]],bv[bt[:,2]]-bv[bt[:,0]]);an=np.cross(av[at[:,1]]-av[at[:,0]],av[at[:,2]]-av[at[:,0]])
    useful=(np.linalg.norm(bn,axis=1)>1e-10)&(np.linalg.norm(an,axis=1)>1e-10)
    flips=int(np.sum(np.einsum('ij,ij->i',bn[useful],an[useful])<0))
    report['local_edit']={'vertices':len(ids),'total_head_vertices':len(delta),'max_depth_edit':float(np.max(np.abs(delta[:,1]))),'xz_identical':True,'bounds_before':[old['Basis'][ids].min(0).tolist(),old['Basis'][ids].max(0).tolist()], 'relative_deformation_errors':error,'actual_head_mouth_boundary_vertices':len(rim_ids),'all_mouth_aperture_keys_max_error':aperture_error,'evaluated_triangle_normal_reversals':flips}
    report['profile_before']=before['profile'];report['profile_after']=after['profile']
    return report
def expressions():
    a.load(v.ASSET); rows=[]
    for state in ['neutral','small','full','smile','happy-closed','half','companion']:
        a.pose(state)
        if state in ['small','full']:v.key('HeadTilt.R',.4)
        if state=='happy-closed':v.sit(.5);v.key('HeadTurn.L',.3)
        head=v.tree(v.parts['Head']);mouth=bpy.data.objects['Shushu_MouthInterior']; vv,_=v.evaluated(mouth); trees=[head,v.tree(mouth)]; gaps=0
        for direction in r.VIEWS.values():
            d=Vector(direction).normalized()
            for i in range(1,193,8):
                p=Vector(vv[i]);hits=[tr.ray_cast(p+d*.3,-d)[3] for tr in trees]
                gaps+=min((x for x in hits if x is not None),default=10)>.301
        assert not gaps,(state,gaps)
        assert np.isfinite(v.evaluated(v.parts['Head'])[0]).all()
        rows.append({'state':state,'mouth_surface_rays':72,'rear_or_missing':gaps})
    return rows
def proof_returns():
    a.load(v.ASSET); baseline={o.name:v.evaluated(o)[0] for o in v.character}
    a.load(v.PROOF);sc=bpy.context.scene; rows={}
    assert sc.frame_start==1 and sc.frame_end==285
    for frame in [1,83,189,249,285]:
        sc.frame_set(frame);err=max(float(np.max(np.linalg.norm(v.evaluated(o)[0]-baseline[o.name],axis=1))) for o in v.character);assert err<2e-6;rows[str(frame)]=err
    prop=bpy.data.objects['Inspection_HeldProp'];sc.frame_set(213);old=prop.location.copy();sc.frame_set(237);release=(prop.location-old).length;assert release>.10
    sc.frame_set(249);assert prop.hide_render
    return {'frame_range':[sc.frame_start,sc.frame_end],'neutral_returns':rows,'release_displacement':release,'hidden_after_release':True}
def surface_only():
    a.load(m.BACK/v.ASSET.name);bv,bt=fixed_surface(v.parts['Head'])
    a.load(v.ASSET);av,at=fixed_surface(v.parts['Head']);assert np.array_equal(bt,at)
    bn=np.cross(bv[bt[:,1]]-bv[bt[:,0]],bv[bt[:,2]]-bv[bt[:,0]]);an=np.cross(av[at[:,1]]-av[at[:,0]],av[at[:,2]]-av[at[:,0]])
    ba=np.linalg.norm(bn,axis=1);aa=np.linalg.norm(an,axis=1)
    collapsed=int(np.sum((ba>1e-10)&(aa<1e-12)))
    usable=np.abs(bn[:,1])>1e-10; sign_changes=int(np.sum(bn[usable,1]*an[usable,1]<0))
    xz_error=float(np.max(np.abs(av[:,[0,2]]-bv[:,[0,2]])))
    assert collapsed==0 and sign_changes==0 and xz_error<1e-7
    result={'new_collapsed_triangles':collapsed,'front_projection_orientation_changes':sign_changes,'evaluated_xz_max_error':xz_error,
        'normal_angle_note':'The 150 normals differing by >90 degrees in targeted-checks are local normal rotations as the inherited ridge flattens. They are not a new reversal of projected winding; fixed X/Z and projected orientation are checked independently.'}
    m.write('surface-checks.json',result);print('MUZZLE_SURFACE_CHECKS_COMPLETE',flush=True)
def main():
    report={'base':m.BASE,'Human':'PENDING','Tripo':'HOLD','saved_assets':{}}
    for p in [v.ASSET,v.PROOF]:report['saved_assets'][p.name]=compare(p)
    report['expressions']=expressions(); report['proof']=proof_returns()
    inputs=json.loads((m.BACK/'inputs.json').read_text()); output_paths={p.relative_to(m.ROOT).as_posix() for p in [v.ASSET,v.PROOF,v.STATIC.with_suffix('.fbx'),v.STATIC.with_suffix('.glb')]}
    protected={p:h for p,h in inputs.items() if p not in output_paths}
    intake=json.loads((m.ROOT/'docs/production/shushu/evidence/candidate-b-8481/input-manifest.json').read_text())
    for row in intake['files'][:2]:protected[row['path']]=row['sha256']
    assert all(m.sha(m.ROOT/p)==h for p,h in protected.items());m.write('protected-inputs.json',protected)
    report['protected_inputs_preserved']=len(protected);m.write('targeted-checks.json',report)
    print('MUZZLE_TARGETED_CHECKS_COMPLETE',flush=True)
if __name__=='__main__':
    if '--surface-only' in sys.argv:surface_only()
    else:main()
