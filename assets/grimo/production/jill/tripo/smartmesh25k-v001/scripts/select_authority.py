import sys,json,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *
g=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('OriginalGLB'))
f=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('OriginalFBX'))
gm=g.data; fm=f.data; gm.calc_loop_triangles();fm.calc_loop_triangles()
gpos=np.array([tuple(g.matrix_world@v.co) for v in gm.vertices]); fpos=np.array([tuple(f.matrix_world@v.co) for v in fm.vertices])
vertex_faces=collections.defaultdict(set)
for p in fm.polygons:
    for v in p.vertices:vertex_faces[v].add(p.index)
coverage=collections.Counter(); missed=[]
for p in gm.polygons:
    match=set.intersection(*(vertex_faces[v] for v in p.vertices))
    if len(match)==1:coverage[next(iter(match))]+=1
    else:missed.append(p.index)
gt={tuple(sorted(p.vertices)) for p in gm.polygons}
same_tris=sum(tuple(sorted(t.vertices)) in gt for t in fm.loop_triangles)
from mathutils.bvhtree import BVHTree
gbvh=BVHTree.FromPolygons(gpos.tolist(),[list(t.vertices) for t in gm.loop_triangles],all_triangles=True)
fbvh=BVHTree.FromPolygons(fpos.tolist(),[list(t.vertices) for t in fm.loop_triangles],all_triangles=True)
distances=[]
for ob,xyz,bvh in [(g,gpos,fbvh),(f,fpos,gbvh)]:
    ds=[bvh.find_nearest(Vector(xyz[list(t.vertices)].mean(0)))[3] for t in ob.data.loop_triangles]
    distances.append({'from':ob.name,'max_triangle_centroid_surface_distance':max(ds),'p99':float(np.quantile(ds,.99))})
suspect=json.loads((EVIDENCE/'plate-investigation.json').read_text())
glb_ids=[i for c in suspect['small_components'] for i in c['faces']]
f_lookup={tuple(sorted(p.vertices)):p.index for p in fm.polygons}
fbx_ids=sorted(set(next(iter(set.intersection(*(vertex_faces[v] for v in gm.polygons[i].vertices)))) for i in glb_ids))
selected=set(fbx_ids)
kept_edges=set(e for p in fm.polygons if p.index not in selected for e in p.edge_keys)
removed_edges=set(e for i in fbx_ids for e in fm.polygons[i].edge_keys)
kept_vertices=set(v for p in fm.polygons if p.index not in selected for v in p.vertices)
plate_vertices=set(v for i in fbx_ids for v in fm.polygons[i].vertices)
r={'selected_editing_source':'input/cute dragon 3d model (1).fbx','reason':'FBX retains source quad topology; GLB triangulates the same vertex positions and polygon domains. No material disadvantage found.',
   'glb_faces_by_size':dict(collections.Counter(len(p.vertices) for p in gm.polygons)),
   'fbx_faces_by_size':dict(collections.Counter(len(p.vertices) for p in fm.polygons)),
   'max_same_index_world_vertex_distance':float(np.max(np.linalg.norm(gpos-fpos,axis=1))),
   'glb_triangles_unmapped_to_fbx_polygon':missed,'fbx_polygon_coverage_mismatches':[p.index for p in fm.polygons if coverage[p.index]!=len(p.vertices)-2],
   'same_triangulation_triangles':same_tris,'sampled_surface_distances':distances,
   'materials':{'glb':len(gm.materials),'fbx':len(fm.materials)},'uv_layers':{'glb':len(gm.uv_layers),'fbx':len(fm.uv_layers)},
   'fbx_remove_face_ids':fbx_ids,'glb_comparison_face_ids':glb_ids,
   'plate_shared_edges_with_kept_faces':[list(e) for e in removed_edges&kept_edges],
   'plate_shared_vertices_with_kept_faces':sorted(plate_vertices&kept_vertices),
   'component_correction':'12 plate triangles form 3 edge-connected patches, not 5 vertex-disconnected components. Lower 8-face patch touches retained geometry only at vertices 3 and 4; preserve every vertex and every retained face.',
   'state':'SELECTED_FBX_BEFORE_REPAIR; HUMAN_GEOMETRY_GATE_PENDING'}
assert not missed and not r['fbx_polygon_coverage_mismatches']
assert not r['plate_shared_edges_with_kept_faces'] and sum(len(fm.polygons[i].vertices)-2 for i in fbx_ids)==12
write_json('editing-source-selection.json',r)
print(json.dumps(r))
