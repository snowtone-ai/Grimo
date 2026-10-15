"""One-way Neutral exports and focused roundtrip evidence. Never saves a blend.
Run with fresh background Blender 5.2.1 from repository root. Not an autorig.
"""
import bpy, json, hashlib, sys, struct
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree

ROOT = Path(__file__).resolve().parents[2]
ASSET = ROOT / 'assets/grimo/production/jill/tripo/smartmesh25k-v002'
OUT = ASSET / 'tripo-input'
E = ROOT / 'docs/production/jill/evidence/tripo-input-v002'
OUT.mkdir(exist_ok=True); E.mkdir(parents=True, exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
master = ASSET / 'jill-geometry-master-v002.blend'
protected = json.loads((E.parent/'smartmesh25k-v002/protected-inputs.json').read_text())
protected[str(master.relative_to(ROOT))] = sha(master)
assert protected[str(master.relative_to(ROOT))] == '8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97'
assert all(sha(ROOT/p) == h for p,h in protected.items())
bpy.ops.wm.open_mainfile(filepath=str(master))
s = bpy.context.scene; s.frame_set(1)
o = bpy.data.objects['JILL_GEOMETRY_MASTER']
assert len(o.data.vertices)==28050 and len(o.data.polygons)==28809 and not o.modifiers
assert all(k.value == 0 for k in o.data.shape_keys.key_blocks[1:])
assert all(tuple(v.co)==tuple(k.co) for v,k in zip(o.data.vertices,o.data.shape_keys.key_blocks['Basis'].data))
def points(obj):
    bpy.context.view_layer.update()
    return [obj.matrix_world@v.co for v in obj.data.vertices]
def stats(obj):
    p=points(obj); obj.data.calc_loop_triangles()
    return dict(vertices=len(p), polygons=len(obj.data.polygons), triangles=len(obj.data.loop_triangles),
        bounds=[[min(v[i] for v in p) for i in range(3)],[max(v[i] for v in p) for i in range(3)]],
        uv_layers=len(obj.data.uv_layers), materials=len(obj.data.materials),
        shape_keys=bool(obj.data.shape_keys), vertex_groups=len(obj.vertex_groups),
        modifiers=[m.type for m in obj.modifiers])
baseline=points(o); source_stats=stats(o)
surface_ids=sorted({i for f in o.data.polygons for i in f.vertices})
surface_baseline=[baseline[i] for i in surface_ids]
source_stats['surface_used_vertices']=len(surface_ids)
source_stats['unreferenced_vertices']=len(baseline)-len(surface_ids)
# Work only on a detached in-memory copy of the approved lineage.
copy=o.copy(); copy.data=o.data.copy(); s.collection.objects.link(copy)
copy.animation_data_clear(); copy.shape_key_clear(); copy.vertex_groups.clear(); copy.name='Jill_v002_Neutral'
assert max((a-b).length for a,b in zip(baseline,points(copy)))==0
for ob in list(bpy.data.objects):
    if ob != copy: bpy.data.objects.remove(ob,do_unlink=True)
# No hidden archive, source, diagnostics or action datablocks in export scene.
for action in list(bpy.data.actions): bpy.data.actions.remove(action)
copy.hide_set(False); copy.hide_render=False
bpy.ops.object.select_all(action='DESELECT'); copy.select_set(True); bpy.context.view_layer.objects.active=copy
fbx=OUT/'jill-v002-neutral-tripo.fbx'; glb=OUT/'jill-v002-neutral-tripo.glb'
bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'MESH'},
    use_mesh_modifiers=False,bake_anim=False,add_leaf_bones=False,axis_forward='-Z',axis_up='Y',
    apply_unit_scale=True,global_scale=1.0,use_custom_props=False,path_mode='AUTO')
bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,
    export_animations=False,export_skins=False,export_morph=False,export_cameras=False,
    export_lights=False,export_extras=False,export_apply=False,export_yup=True)
def distance(a,b):
    tree=KDTree(len(b))
    for i,p in enumerate(b): tree.insert(p,i)
    tree.balance()
    return max(tree.find(p)[2] for p in a)
def face_signature(obj):
    p=points(obj)
    return sorted(tuple(sorted(tuple(round(x,6) for x in p[v]) for v in f.vertices)) for f in obj.data.polygons)
source_faces=face_signature(copy)
sys.path.insert(0,str(ASSET.parent/'smartmesh25k-v001/scripts'))
sys.dont_write_bytecode=True
import audit_common as a
lo=Vector(source_stats['bounds'][0]); hi=Vector(source_stats['bounds'][1]); center=(lo+hi)/2; scale=max(hi-lo)*1.18
def capture(obj,label):
    scene=bpy.context.scene
    if not scene.world: scene.world=bpy.data.worlds.new('EvidenceWorld')
    a.setup_render(scene); scene.render.resolution_x=480; scene.render.resolution_y=480
    scene.render.image_settings.file_format='JPEG'; scene.render.image_settings.quality=96
    obj.color=(.58,.68,.55,1)
    for view,direction in [('front',(0,-1,0)),('side',(1,0,0)),('three-quarter',(1,-2,.6))]:
        a.setup_camera(scene,direction,center,scale)
        scene.render.filepath=str(E/f'{label}-{view}.jpg'); bpy.ops.render.render(write_still=True)
capture(copy,'source')
report=dict(blender=bpy.app.version_string,source_path=str(master.relative_to(ROOT)),source_sha256=sha(master),
    source=source_stats,source_units={'system':s.unit_settings.system,'scale_length':s.unit_settings.scale_length},
    start_head='709cddb570fa806112139161a6b3084c51665425',main_authority='8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b',
    exports={},geometry_gate='HOLD',human_visual='PENDING',tripo_operations=0)
for file in (fbx,glb):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if file.suffix=='.fbx': bpy.ops.import_scene.fbx(filepath=str(file))
    else: bpy.ops.import_scene.gltf(filepath=str(file),merge_vertices=False)
    objects=list(bpy.context.scene.objects)
    assert len(objects)==1 and objects[0].type=='MESH', [(x.name,x.type) for x in objects]
    obj=objects[0]; p=points(obj); st=stats(obj)
    st.update(bytes=file.stat().st_size,sha256=sha(file),objects=[(x.name,x.type) for x in objects],
        actions=len(bpy.data.actions),armatures=len(bpy.data.armatures),images=len(bpy.data.images),
        source_all_vertices_to_import_max=distance(baseline,p),
        source_surface_to_import_max=distance(surface_baseline,p),import_to_source_surface_max=distance(p,surface_baseline),
        imported_transform=[list(r) for r in obj.matrix_world])
    assert st['source_surface_to_import_max']<1e-6, st
    if file.suffix=='.glb': assert st['import_to_source_surface_max']<1e-6, st
    else: assert distance(p,baseline)<1e-6, st
    assert st['triangles']==source_stats['triangles'] and not st['shape_keys'] and not st['actions']
    assert not st['vertex_groups'] and not st['modifiers'] and not st['armatures'] and not st['images']
    if file.suffix=='.fbx':
        st['polygon_coordinate_signature_equal_1e6']=face_signature(obj)==source_faces
        assert st['polygon_coordinate_signature_equal_1e6']
    else:
        data=file.read_bytes(); n=struct.unpack_from('<I',data,12)[0]; doc=json.loads(data[20:20+n])
        st['glb_payload']={k:len(doc.get(k,[])) for k in ['nodes','meshes','skins','animations','cameras','images']}
        assert not doc.get('skins') and not doc.get('animations')
        assert not any(p.get('targets') for m in doc['meshes'] for p in m['primitives'])
    report['exports'][file.name]=st
    capture(obj,file.suffix[1:])
report['protected_files_checked']=len(protected)
report['protected_hashes_unchanged']=all(sha(ROOT/p)==h for p,h in protected.items())
assert report['protected_hashes_unchanged']
(E/'roundtrip.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('JILL_NEUTRAL_EXPORT_COMPLETE',json.dumps(report))
