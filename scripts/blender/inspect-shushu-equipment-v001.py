"""Read-only equipment planning from the approved candidate."""
import bpy,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v004-proof.blend'))
bpy.context.scene.frame_set(1)
rows=[]
for o in bpy.data.objects:
 if o.type=='ARMATURE':
  rows.append({'rig':o.name,'bones':[{'name':b.name,'head':list(b.head_local),'tail':list(b.tail_local)} for b in o.data.bones if any(s in b.name for s in ['Head','Foot','Toe','Ear'])]})
 if o.type!='MESH':continue
 p=np.array([o.matrix_world@v.co for v in o.data.vertices])
 mats=[]
 for m in o.data.materials:
  mats.append({'name':m.name,'images':[{'name':n.image.name,'size':list(n.image.size),'path':n.image.filepath} for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]})
 rows.append({'mesh':o.name,'min':p.min(0).tolist(),'max':p.max(0).tolist(),'materials':mats,'keys':[k.name for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else []})
 if o.name=='ShushuStatic_Torso':
  o.data.calc_loop_triangles()
  np.savez(R/'output/shushu-equipment-torso.npz',p=p,n=np.array([v.normal[:] for v in o.data.vertices]),tri=np.array([t.vertices[:] for t in o.data.loop_triangles]),uv=np.array([[o.data.uv_layers.active.data[i].uv[:] for i in t.loops] for t in o.data.loop_triangles]))
  bpy.context.scene.frame_set(103);ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();np.save(R/'output/shushu-equipment-seat.npy',np.array([ev.matrix_world@v.co for v in em.vertices]));ev.to_mesh_clear();bpy.context.scene.frame_set(1)
  for m in o.data.materials:
   for n in m.node_tree.nodes:
    if n.type=='TEX_IMAGE' and n.image:n.image.save_render(str(R/'output/shushu-equipment-torso-original.png'))
(R/'output/shushu-equipment-inventory.json').write_text(json.dumps(rows,indent=2))
