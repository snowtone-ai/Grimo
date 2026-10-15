import sys, json, struct, hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *

g=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('OriginalGLB'))
f=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('OriginalFBX'))
gp=np.array([tuple(g.matrix_world@v.co) for v in g.data.vertices]); fp=np.array([tuple(f.matrix_world@v.co) for v in f.data.vertices])
from mathutils.kdtree import KDTree
kd=KDTree(len(fp))
for i,p in enumerate(fp): kd.insert(p,i)
kd.balance(); matches=[kd.find(p) for p in gp]
mapping=[r[1] for r in matches]
ft={tuple(sorted(p.vertices)) for p in f.data.polygons}
match_faces=sum(tuple(sorted(mapping[i] for i in p.vertices)) in ft for p in g.data.polygons)
write_json('fbx-glb-equivalence.json',{'max_world_vertex_distance':max(r[2] for r in matches),
    'unique_nearest_matches':len(set(mapping)), 'glb_vertices':len(gp),'fbx_vertices':len(fp),
    'matching_triangle_vertex_sets':match_faces,'triangle_count':len(g.data.polygons),
    'polygon_indices_identical': all(tuple(a.vertices)==tuple(b.vertices) for a,b in zip(g.data.polygons,f.data.polygons)),
    'same_index_max_vertex_distance':float(np.max(np.linalg.norm(gp-fp,axis=1)))})

# Face connectivity through shared edges, separate from vertex-only connectivity.
m=g.data; parents=list(range(len(m.polygons))); by_edge={}
def root(a):
    while parents[a]!=a: parents[a]=parents[parents[a]]; a=parents[a]
    return a
for p in m.polygons:
    for e in p.edge_keys:
        if e in by_edge: parents[root(p.index)]=root(by_edge[e])
        else: by_edge[e]=p.index
groups={}
for p in m.polygons: groups.setdefault(root(p.index),[]).append(p.index)
small=[]
for fs in groups.values():
    if len(fs)>12: continue
    vs=sorted(set(v for fi in fs for v in m.polygons[fi].vertices)); pos=gp[vs]
    small.append({'faces':fs,'vertex_ids':vs,'bounds':[pos.min(0).tolist(),pos.max(0).tolist()],
                  'area':sum(m.polygons[i].area for i in fs)})
large=[]
for p in m.polygons:
    if p.area>0.006:
        large.append({'id':p.index,'area':p.area,'vertices':list(p.vertices),'coords':[gp[v].tolist() for v in p.vertices]})
write_json('plate-investigation.json',{'edge_connected_components':len(groups),'small_components':small,'large_triangles':large})
print('ANALYSIS',json.dumps({'small_components':small,'large_triangles':large}))
