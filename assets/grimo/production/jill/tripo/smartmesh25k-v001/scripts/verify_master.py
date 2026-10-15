import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
o=bpy.data.objects['JILL_GEOMETRY_MASTER'];m=o.data;scene=bpy.context.scene
scene.frame_set(1);bpy.context.view_layer.update()
orig=bpy.data.objects['REFERENCE_FBX_UNEDITED'];selection=json.loads((EVIDENCE/'editing-source-selection.json').read_text())
keep=[p.index for p in orig.data.polygons if p.index not in selection['fbx_remove_face_ids']]
assert all(tuple(a.co)==tuple(b.co) for a,b in zip(orig.data.vertices,m.vertices))
assert all(tuple(a.co)==tuple(b.co) for a,b in zip(m.vertices,m.shape_keys.key_blocks['Basis'].data))
assert all(tuple(p.vertices)==tuple(orig.data.polygons[i].vertices) for p,i in zip(m.polygons,keep))
assert all(k.value==0 for k in m.shape_keys.key_blocks if k.name!='Basis')
data=np.load(EVIDENCE/'diagnostic-positions.npz');xyz=data['neutral'];tris=data['triangles']

def intersections(positions,moving,stationary):
    if not len(moving) or not len(stationary):return set()
    a=BVHTree.FromPolygons(positions.tolist(),tris[moving].tolist(),all_triangles=True,epsilon=0.0)
    b=BVHTree.FromPolygons(positions.tolist(),tris[stationary].tolist(),all_triangles=True,epsilon=0.0)
    pairs=set()
    for i,j in a.overlap(b):
        ti,tj=int(moving[i]),int(stationary[j])
        if not set(tris[ti])&set(tris[tj]):pairs.add((ti,tj))
    return pairs

report={'method':'BVH triangle overlap at neutral, half amplitude and peak; only moving vs stationary triangles, shared-vertex pairs excluded. New pair counts are contact candidates, not certified penetration depth.',
        'limits':['Does not detect enclosed-volume penetration without surface crossings.','Does not prove absence of self-folding within the moving region.','Does not certify unsampled animation times or arbitrary angles.'], 'cases':[]}
proof=json.loads((EVIDENCE/'deformation-validation.json').read_text())
for ci,c in enumerate(proof['cases']):
    name=c['name'];peak=data[name];movev=np.linalg.norm(peak-xyz,axis=1)>1e-9
    movet=np.any(movev[tris],axis=1);moving=np.where(movet)[0];stationary=np.where(~movet)[0]
    baseline=intersections(xyz,moving,stationary)
    stages=[]
    for level in [.5,1.]:
        p=xyz+(peak-xyz)*level;now=intersections(p,moving,stationary);new=now-baseline
        stages.append({'amplitude':level,'baseline_pairs':len(baseline),'current_pairs':len(now),
                       'new_pair_count':len(new),'new_triangle_pairs':[list(q) for q in sorted(new)],
                       'new_pair_centroids':[(p[tris[a]].mean(0)).tolist() for a,b in sorted(new)[:20]]})
    report['cases'].append({'name':name,'samples':stages})
write_json('collision-screen.json',report)

# Export only the repaired master at the saved neutral; diagnostics intentionally excluded.
scene.frame_set(1);bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
path=ASSET/'jill-repaired-neutral.glb'
bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,
    export_animations=False,export_skins=False,export_morph=False,export_apply=False,export_extras=False,
    export_normals=True,export_materials='EXPORT')
before=set(scene.objects);bpy.ops.import_scene.gltf(filepath=str(path),merge_vertices=False)
imports=[ob for ob in scene.objects if ob not in before and ob.type=='MESH']
assert len(imports)==1
rt=imports[0];rt.data.calc_loop_triangles();m.calc_loop_triangles()
points=[rt.matrix_world@v.co for v in rt.data.vertices]
used=sorted({i for p in m.polygons for i in p.vertices})
kd=KDTree(len(points))
for i,p in enumerate(points):kd.insert(p,i)
kd.balance();errors=[kd.find(o.matrix_world@m.vertices[i].co)[2] for i in used]
kd2=KDTree(len(used))
for j,i in enumerate(used):kd2.insert(o.matrix_world@m.vertices[i].co,j)
kd2.balance();reverse=[kd2.find(p)[2] for p in points]
validation={'master_reopened_and_basis_matches_immutable_fbx_vertices':True,'retained_fbx_faces_match':True,
 'shape_keys_at_neutral':all(k.value==0 for k in m.shape_keys.key_blocks if k.name!='Basis'),'master_quads':sum(len(p.vertices)==4 for p in m.polygons),
 'master_triangles':len(m.loop_triangles),'export_triangles':len(rt.data.loop_triangles),
 'max_master_to_export_used_vertex_distance':max(errors),'max_export_to_master_vertex_distance':max(reverse),
 'export_vertex_count':len(points),'master_vertices_in_use':len(used),'export_has_shape_keys':bool(rt.data.shape_keys),
 'export_has_armature':any(ob.type=='ARMATURE' for ob in scene.objects if ob not in before),
 'export_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'original_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ASSET/'input').iterdir() if p.is_file()}}
assert max(errors)<1e-6 and max(reverse)<1e-6 and len(m.loop_triangles)==len(rt.data.loop_triangles)
write_json('saved-master-export-validation.json',validation)
print('VERIFIED',json.dumps(validation))
print('COLLISION_SCREEN',[(c['name'],[s['new_pair_count'] for s in c['samples']]) for c in report['cases']])
