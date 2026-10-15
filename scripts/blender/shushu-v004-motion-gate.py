"""Separate A/B gate candidate. Preserve approved geometry; revise local mouth ink last.

Blender authoring and saved GLB keep the evaluated paw surface. The companion
runtime adapter repairs its non-linear normal evaluation, not its rig or shape.
"""
import bpy, sys, json, hashlib, importlib.util
from pathlib import Path
import numpy as np
from mathutils import Matrix, Vector
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
BASE = ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
ASSET = BASE/'shushu-v004-motion-gate-v001.blend'
PROOF = ASSET.with_name(ASSET.stem+'-proof.blend')
GLB = ASSET.with_suffix('.glb')
if '--v002' in sys.argv:
    OUT=OUT/'final-v002';ASSET=BASE/'shushu-v004-motion-gate-v002.blend';PROOF=ASSET.with_name(ASSET.stem+'-proof.blend');GLB=ASSET.with_suffix('.glb')
def module(name, path):
    s=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
r=module('mouth_b','scripts/blender/repair-shushu-v004-mouth-b.py')
def write(name, value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def evaluate(o, normals=False):
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get()); m=ev.to_mesh(); m.calc_loop_triangles()
    p=np.array([ev.matrix_world@v.co for v in m.vertices])
    if normals:
        nm=ev.matrix_world.to_3x3().inverted().transposed()
        n=np.array([(nm@v.vector).normalized() for v in m.vertex_normals]); t=np.array([list(v.vertices) for v in m.loop_triangles])
        ev.to_mesh_clear(); return p,n,t
    ev.to_mesh_clear(); return p
def trim_philtrum():
    """Clip only the thin Nose stem below z=.632; retain bulb and all its keys."""
    o=bpy.data.objects['ShushuStatic_Nose'];old=o.data
    points=np.array([v.co for v in old.vertices]);keys=old.shape_keys
    states={k.name:r.coords(k) for k in keys.key_blocks} if keys else {'Basis':points}
    drivers=[]
    if keys and keys.animation_data:
        for fc in keys.animation_data.drivers:
            drivers.append((fc.data_path,fc.driver.expression,[(v.name,v.type,[(t.id,t.data_path) for t in v.targets]) for v in fc.driver.variables]))
    weights=[[(g.group,g.weight) for g in v.groups] for v in old.vertices];groupnames=[g.name for g in o.vertex_groups]
    verts=list(points);edges={};faces=[];uvs=[];cut=[];threshold=.632
    old.calc_loop_triangles()
    def intersection(a,b):
        edge=tuple(sorted((a,b)))
        if edge not in edges:
            t=(threshold-points[a,2])/(points[b,2]-points[a,2]);idx=len(verts);verts.append(points[a]*(1-t)+points[b]*t);edges[edge]=(idx,a,b,t);cut.append(idx)
        return edges[edge]
    for tri in old.loop_triangles:
        ids=list(tri.vertices);uv=[np.array(old.uv_layers.active.data[i].uv) for i in tri.loops];poly=[];tex=[]
        for k,a in enumerate(ids):
            b=ids[(k+1)%3];inside=points[a,2]>=threshold;nextinside=points[b,2]>=threshold
            if inside:poly.append(a);tex.append(uv[k])
            if inside!=nextinside:
                idx,aa,bb,t=intersection(a,b);tt=t if aa==a else 1-t;poly.append(idx);tex.append(uv[k]*(1-tt)+uv[(k+1)%3]*tt)
        if len(poly)>=3:faces.append(poly);uvs.append(tex)
    # Stem is one connected, small section. The cap faces down into the muzzle.
    cp=np.array(verts)[cut];center=cp.mean(0);order=np.argsort(np.arctan2(cp[:,1]-center[1],cp[:,0]-center[0]))[::-1]
    cap=[cut[i] for i in order];faces.append(cap);uvs.append([np.array((.5,.5))]*len(cap))
    mesh=bpy.data.meshes.new(old.name+'_StemRemoved');mesh.from_pydata(verts,[],faces);mesh.update();o.data=mesh
    o.vertex_groups.clear()
    for name in groupnames:o.vertex_groups.new(name=name)
    for m in old.materials:mesh.materials.append(m)
    uv=mesh.uv_layers.new(name=old.uv_layers.active.name)
    for poly,values in zip(mesh.polygons,uvs):
        poly.use_smooth=True
        for loop,value in zip(poly.loop_indices,values):uv.data[loop].uv=value
    for i,ws in enumerate(weights):
        for group,w in ws:o.vertex_groups[group].add([i],w,'REPLACE')
    for idx,a,b,t in edges.values():
        ws={g:w*(1-t) for g,w in weights[a]}
        for g,w in weights[b]:ws[g]=ws.get(g,0)+w*t
        for g,w in ws.items():o.vertex_groups[g].add([idx],w,'REPLACE')
    for name,p in states.items():
        arr=np.zeros((len(verts),3));arr[:len(p)]=p
        for idx,a,b,t in edges.values():arr[idx]=p[a]*(1-t)+p[b]*t
        k=o.shape_key_add(name=name);k.data.foreach_set('co',arr.ravel())
    for path,expression,variables in drivers:
        fc=mesh.shape_keys.driver_add(path);fc.driver.expression=expression
        for name,typ,targets in variables:
            v=fc.driver.variables.new();v.name=name;v.type=typ
            for target,(ident,dp) in zip(v.targets,targets):target.id=ident;target.data_path=dp
    # Unreferenced stem coordinates are intentionally retained to preserve source
    # key coordinate; export only emits referenced vertices.
    assert all(np.array_equal(r.coords(mesh.shape_keys.key_blocks[n])[:len(p)],p) for n,p in states.items())
    write('nose-local-surgery.json',{'threshold_z':threshold,'source_vertices':len(points),'source_faces':len(old.polygons),'removed_stem_vertices_below_cut':int((points[:,2]<threshold).sum()),'cut_vertices':len(cut),'retained_source_shape_coordinates_exact':True,'source_geometry_bounds':[points.min(0).tolist(),points.max(0).tolist()],'stem_bounds':[points[points[:,2]<threshold].min(0).tolist(),points[points[:,2]<threshold].max(0).tolist()],'nose_bulb_z_ge_0632_unchanged':True,'cap':'local clipped section, closed by one downward polygon','W_Head_and_oral_geometry_unchanged':True})
def build():
    bpy.ops.wm.open_mainfile(filepath=str(r.ASSET))
    rig=next(o for o in bpy.data.objects if o.type=='ARMATURE'); r.b.reset(rig)
    trim_philtrum(); head=bpy.data.objects['ShushuStatic_Head']
    before=hashlib.sha256(b''.join(r.coords(k).tobytes() for k in head.data.shape_keys.key_blocks)).hexdigest()
    if '--geometry-review' in sys.argv:
        scene,cam=r.b.setup_review(640,12);cam.data.type='ORTHO';cam.data.ortho_scale=.56
        materials=list(head.data.materials);head.data.materials.clear();head.data.materials.append(r.material('Gate geometry cream',(.78,.75,.71)))
        folder=OUT/'geometry-clay';folder.mkdir(exist_ok=True)
        for state,controls in r.STATES.items():
            r.b.state(rig,controls)
            for view,loc in r.VIEWS.items():
                cam.location=loc;cam.rotation_euler=(Vector((0,-.02,.69))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/f'{state}-{view}.png');bpy.ops.render.render(write_still=True)
        head.data.materials.clear()
        for m in materials:head.data.materials.append(m)
        r.b.reset(rig)
    # Clip the actual Nose stem and inspect geometry/aperture before binding the
    # local texture, which also removes the old philtrum ink coverage.
    img=bpy.data.images.load(str(OUT/'Head-mouth-b-local.png'),check_existing=False); img.pack()
    next(n for m in head.data.materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE').image=img
    after=hashlib.sha256(b''.join(r.coords(k).tobytes() for k in head.data.shape_keys.key_blocks)).hexdigest()
    assert before==after
    rig['A/B gate']='Mouth B v002 no hanging philtrum ink; A surface normal companion required. Human PENDING.'
    bpy.context.preferences.filepaths.save_version=0; bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    write('texture-stage-geometry-invariance.json',{'before':before,'after':after,'equal':before==after})
def proof():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET)); rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
    with bpy.data.libraries.load(str(BASE/'shushu-v006-production-rig-v004-proof.blend'),link=False) as (src,dst):
        dst.actions=['Shushu_ProductionRig_v004Action']
    rig.animation_data_create(); rig.animation_data.action=dst.actions[0]
    if rig.animation_data.action_slot is None:rig.animation_data.action_slot=dst.actions[0].slots[0]
    controls=[k for k in rig.keys() if isinstance(rig[k],(int,float))]
    for f,op,seat in [(825,0,0),(837,.2,0),(849,.55,0),(861,1,0),(873,.55,0),(885,.2,0),(897,0,0),(909,0,1),(921,.2,1),(933,.55,1),(945,1,1),(957,0,1),(969,1,1),(981,0,1),(993,0,0)]:
        r.b.reset(rig)
        for k,v in {'MouthOpen':op,'Seat':seat,'MouthClose':1 if f==969 else 0,'Tongue':1 if f in [969,981] else 0}.items():rig[k]=float(v)
        for k in controls:rig.keyframe_insert(data_path='["'+k+'"]',frame=f)
    for layer in rig.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='LINEAR'
    scene=bpy.context.scene; scene.frame_start=1; scene.frame_end=993; scene.render.fps=24; scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(PROOF))
    meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')]
    anchors=[o for o in bpy.data.objects if o.name.startswith('ANCHOR_')]
    pose={}; morph={}; anchor={}; ref={}; ar={o.name:[] for o in anchors}
    samples=set([1,49,103,169,477,493,509,517,533,549,821,825,831,837,843,849,855,861,873,885,897,909,945,969,981,993]+list(range(505,542,3)))
    for f in range(1,994):
        scene.frame_set(f); bpy.context.view_layer.update()
        pose[f]={pb.name:pb.matrix.copy() for pb in rig.pose.bones}
        morph[f]={o.name:{k.name:float(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.shape_keys.key_blocks[k.name].value) for k in o.data.shape_keys.key_blocks[1:]} for o in meshes if o.data.shape_keys}
        anchor[f]={o.name:o.matrix_basis.copy() for o in anchors}
        for o in anchors:ar[o.name].append(np.array(o.matrix_world))
        if f in samples:
            for o in meshes:ref[o.name+'__'+str(f)]=evaluate(o).astype(np.float32)
        if f in samples and f<=821:
            data={}
            for o in meshes:
                if 'Paw_' in o.name:
                    p,n,t=evaluate(o,True);data[o.name+'-p']=p;data[o.name+'-n']=n;data[o.name+'-tri']=t
            folder=OUT/'author-normals';folder.mkdir(exist_ok=True);np.savez_compressed(folder/f'f{f}.npz',**data)
    np.savez_compressed(OUT/'saved-reference.npz',**ref);np.savez_compressed(OUT/'anchor-reference.npz',**ar)
    for o in [rig]+anchors:
        if o.animation_data:
            o.animation_data.action=None
            for fc in list(o.animation_data.drivers):o.driver_remove(fc.data_path,fc.array_index)
    for pb in rig.pose.bones:
        for c in list(pb.constraints):pb.constraints.remove(c)
        pb.rotation_mode='QUATERNION'
    for o in meshes:
        if o.data.shape_keys and o.data.shape_keys.animation_data:
            o.data.shape_keys.animation_data.action=None
            for fc in list(o.data.shape_keys.animation_data.drivers):o.data.shape_keys.driver_remove(fc.data_path,fc.array_index)
    for f in range(1,994):
        scene.frame_set(f)
        for pb in rig.pose.bones:
            pb.matrix_basis=pb.bone.convert_local_to_pose(pose[f][pb.name],pb.bone.matrix_local,parent_matrix=pose[f][pb.parent.name] if pb.parent else Matrix.Identity(4),parent_matrix_local=pb.parent.bone.matrix_local if pb.parent else Matrix.Identity(4),invert=True)
            for path in ['location','rotation_quaternion','scale']:pb.keyframe_insert(data_path=path,frame=f)
        for name,keys in morph[f].items():
            for key,value in keys.items():k=bpy.data.objects[name].data.shape_keys.key_blocks[key];k.value=value;k.keyframe_insert(data_path='value',frame=f)
        for o in anchors:
            o.matrix_basis=anchor[f][o.name]
            for path in ['location','rotation_euler','scale']:o.keyframe_insert(data_path=path,frame=f)
    scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT')
    for o in [rig]+meshes+anchors:o.select_set(True)
    bpy.context.view_layer.objects.active=rig
    bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_frame_step=1,export_force_sampling=True,export_bake_animation=True,export_anim_scene_split_object=False,export_nla_strips_merged_animation_name='AB_Gate_Diagnostic_NotProduction',export_optimize_animation_size=False,export_skins=True,export_all_influences=True,export_morph=True,export_morph_animation=True,export_apply=False,export_keep_originals=False,export_extras=True)
    write('diagnostic-timeline.json',{'fps':24,'frames':993,'original_v004_frames':[1,821],'mouth_frames':{'closed':825,'small':837,'medium':849,'large':861,'return':897,'seated':909,'close_priority':969,'tongue':981,'neutral_return':993},'production_motion':False})
def imported():
    p=module('importer','scripts/blender/prove-shushu-production-rig-v001.py');p.import_saved(GLB)
def verify():
    imported();scene=bpy.context.scene;ref=np.load(OUT/'saved-reference.npz');meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')]
    from mathutils.kdtree import KDTree
    maps={};scene.frame_set(861)
    for o in meshes:
        pts=ref[o.name+'__861'];tree=KDTree(len(pts))
        for i,p in enumerate(pts):tree.insert(p,i)
        tree.balance();maps[o.name]=np.array([tree.find(p)[1] for p in evaluate(o)])
    rows=[]
    for f in sorted(set(int(k.rsplit('__',1)[1]) for k in ref.files)):
        scene.frame_set(f)
        for o in meshes:rows.append({'frame':f,'mesh':o.name,'max_position_error':float(np.linalg.norm(evaluate(o)-ref[o.name+'__'+str(f)][maps[o.name]],axis=1).max())})
    ar=np.load(OUT/'anchor-reference.npz');error=0
    for f in range(1,994):
        scene.frame_set(f)
        for name in ar.files:error=max(error,float(abs(np.array(bpy.data.objects[name].matrix_world)-ar[name][f-1]).max()))
    write('saved-roundtrip.json',{'rows':rows,'max_position_error':max(r['max_position_error'] for r in rows),'anchor_max_matrix_error':error,'mapping':'fixed fully-open frame861 nearest; UV-equivalent duplicates retained'})
    assert max(r['max_position_error'] for r in rows)<1e-5 and error<1e-5
def video():
    saved='--saved' in sys.argv
    if saved:imported()
    else:bpy.ops.wm.open_mainfile(filepath=str(PROOF))
    scene,cam=r.b.setup_review(384,8);scene.render.engine='BLENDER_EEVEE';cam.data.type='ORTHO'
    for name,start,end,view in [('arm',477,557,'3q'),('mouth',825,897,'front')]:
        mouth=name=='mouth';folder=OUT/('saved-video' if saved else 'author-video')/name;folder.mkdir(parents=True,exist_ok=True)
        cam.data.ortho_scale=.56 if mouth else 1.18;target=(0,-.02,.69) if mouth else (0,0,.5)
        cam.location=r.VIEWS[view] if mouth else (-2,-2.5,.65);cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
        for f in range(start,end+1):
            scene.frame_set(f);scene.render.filepath=str(folder/f'{f:04}.png');bpy.ops.render.render(write_still=True)
        print('VIDEO_FRAMES',saved,name,flush=True)
def render():
    saved='--saved' in sys.argv
    if saved:imported()
    else:bpy.ops.wm.open_mainfile(filepath=str(PROOF))
    scene,cam=r.b.setup_review(640,16);cam.data.type='ORTHO'
    folder=OUT/('saved' if saved else 'author');folder.mkdir(exist_ok=True)
    rows=[('closed',825),('small',837),('medium',849),('large',861),('neutral',1),('seat',103),('offer',477),('wrist',493),('self',509),('self-r',517),('hold',533),('seat-hold',549),('return',993)]
    if '--face-only' in sys.argv:rows=[(n,f) for n,f in rows if n in ['closed','small','medium','large','seat','hold','return']]
    if '--sequence' in sys.argv:rows=[(f'f{f}',f) for f in range(505,542,3)]
    for label,f in rows:
        scene.frame_set(f);mouth=label in ['closed','small','medium','large'];cam.data.ortho_scale=.56 if mouth else 1.18;target=(0,-.02,.69) if mouth else (0,0,.5)
        for view,loc in (r.VIEWS if mouth else {'front':(0,-3,.5),'side':(-3,0,.5),'3q':(-2,-2.5,.65)}).items():
            if '--sequence' in sys.argv and view=='front':continue
            cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/f'{label}-{view}.png');bpy.ops.render.render(write_still=True)
        print('GATE_RENDER',saved,label,flush=True)
if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    if '--build' in sys.argv:build()
    elif '--export' in sys.argv:proof()
    elif '--verify' in sys.argv:verify()
    elif '--render' in sys.argv:render()
    elif '--video' in sys.argv:video()
