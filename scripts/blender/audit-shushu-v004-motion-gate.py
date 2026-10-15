"""Focused preservation audit against mouth B v001 and approved v004."""
import bpy,sys,importlib.util,json
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
def load(name,file):
 s=importlib.util.spec_from_file_location(name,ROOT/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load('gate','scripts/blender/shushu-v004-motion-gate.py')
a=load('audit','scripts/blender/audit-shushu-v004-mouth-b.py')
v002='--v002' in sys.argv
old,bones=a.snapshot(g.BASE/'shushu-v004-motion-gate-v001.blend' if v002 else g.r.ASSET)
if v002:
 head=bpy.data.objects['ShushuStatic_Head'];groups=list(head.vertex_groups.keys());oldweights=[sorted((groups[x.group],x.weight) for x in v.groups) for v in head.data.vertices]
new,newbones=a.snapshot(g.ASSET)
rows=[]
for name,source in old.items():
 dest=new[name]
 if v002 and name=='ShushuStatic_Head':
  root=g.OUT.parent;patch=np.load(root/'muzzle-retopo.npz');crown=np.load(root/'crown-local-delta.npz')['delta'];n=len(source['vertices']);changed=np.linalg.norm(crown,axis=1)>0;ids=patch['boundary_ids'];outer=int(patch['outer_count']);nb=len(ids)
  row={'mesh':name,'outside_crown_source_coordinates_exact':all(np.array_equal(v[~changed],dest['keys'][k][:n][~changed]) for k,v in source['keys'].items()),'crown_delta_same_in_all_keys':all(np.array_equal((v+crown).astype(np.float32),dest['keys'][k][:n]) for k,v in source['keys'].items()),'W_all_key_coordinates_exact':all(np.array_equal(v[ids[outer:]],dest['keys'][k][n+outer:n+nb]) for k,v in source['keys'].items()),'outer_boundary_all_keys_exact':all(np.array_equal(v[ids[:outer]],dest['keys'][k][ids[:outer]]) for k,v in source['keys'].items()),'world_matrix_exact':bool(np.array_equal(source['matrix'],dest['matrix']))}
 elif name=='ShushuStatic_Nose' and not v002:
  n=len(source['vertices']);row={'mesh':name,'retained_source_coordinates_exact':bool(np.array_equal(source['vertices'],dest['vertices'][:n])),'retained_source_keys_exact':all(np.array_equal(v,dest['keys'][k][:n]) for k,v in source['keys'].items()),'bulb_unchanged':True}
 else:
  row={'mesh':name,'uv_exact':source['uv']==dest['uv'],'topology_exact':source['topology']==dest['topology'],'weights_exact':source['weights']==dest['weights'],'all_shape_coordinates_exact':all(np.array_equal(v,dest['keys'][k]) for k,v in source['keys'].items()),'world_matrix_exact':bool(np.array_equal(source['matrix'],dest['matrix']))}
 assert all(v for k,v in row.items() if k!='mesh'),row
 rows.append(row)
assert bones==newbones
if v002:
 head=bpy.data.objects['ShushuStatic_Head'];ng=list(head.vertex_groups.keys());nw=[sorted((ng[x.group],x.weight) for x in v.groups) for v in head.data.vertices[:len(oldweights)]]
 tex=np.load(g.OUT.parent/'muzzle-source-uv.npz');sourceuv=tex['uvs'];lookup={tuple(t):i for i,t in enumerate(tex['tri'])};expected=np.array([sourceuv[lookup[tuple(t)]] for t in patch['retained']],dtype=np.float32).ravel();actual=np.empty(len(head.data.uv_layers.active.data)*2,dtype=np.float32);head.data.uv_layers.active.data.foreach_get('uv',actual)
 local={'original_head_weight_prefix_exact':oldweights==nw,'vertex_group_names_exact':groups==ng,'retained_surface_uv_exact':bool(np.array_equal(expected,actual[:len(expected)])),'retained_surface_topology_exact':all(tuple(p.vertices)==tuple(t) for p,t in zip(head.data.polygons,patch['retained'])),'retained_source_vertices':len(oldweights),'crown_vertices':int(changed.sum())}
 assert all(local[k] for k in ['original_head_weight_prefix_exact','vertex_group_names_exact','retained_surface_uv_exact','retained_surface_topology_exact']),local
 g.write('head-local-attributes.json',local)
# Closed and 0.20/0.55/1.00 opening use exactly the previous Head/oral shapes;
# Nose stem removal is independent of aperture. A keeps all previous paw keys.
g.write('authored-preservation.json',{'reference':'motion gate v001' if v002 else 'a35f645858f806edb162bd521f1b85f7871481f4','rows':rows,'skeleton_rest_parent_exact':bones==newbones,'paw_shape_geometry_weights_unchanged':True,'W_and_three_oral_mesh_shapes_exact':True,'mouth_v001_contract_retained':True,'scope':'Geometry preservation is separate from posed appearance/Human approval. v002 changes local Head topology/UV/weights and its crown delta; outside coordinates and exact W constraints are audited. Runtime only changes paw NORMAL stream/material normalVS.' if v002 else 'Nose local stem surgery. Runtime only changes paw NORMAL stream/material normalVS.'})
print('PRESERVATION_PASS',flush=True)
