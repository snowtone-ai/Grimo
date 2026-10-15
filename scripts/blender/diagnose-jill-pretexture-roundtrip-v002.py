"""Narrow diagnostic for asymmetric nearest-surface error on the GLB import."""
import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/rig-pretexture-v002';A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-v002'
refs=np.load(E/'proof-positions.npz')['mouth-12'];used=np.unique(np.load(E/'surface-contract.npz')['polygons']);refs=refs[used]
k=KDTree(len(refs))
for i,p in enumerate(refs):k.insert(Vector(p),i)
k.balance();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=24;bpy.ops.import_scene.gltf(filepath=str(A/'jill-rig-pretexture-v002.glb'));bpy.context.scene.frame_set(13);bpy.context.view_layer.update()
rows=[]
for o in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();ids={i for p in m.polygons for i in p.vertices};out=[]
 for i in ids:
  p=o.matrix_world@m.vertices[i].co;d=k.find(p)[2]
  if d>.001:out.append({'vertex':i,'co':list(p),'distance':d,'groups':[(o.vertex_groups[x.group].name,x.weight) for x in o.data.vertices[i].groups]})
 rows.append({'mesh':o.name,'vertices':len(m.vertices),'used':len(ids),'outliers':len(out),'largest':sorted(out,key=lambda x:-x['distance'])[:10]});ev.to_mesh_clear()
(E/'roundtrip-diagnostic.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
