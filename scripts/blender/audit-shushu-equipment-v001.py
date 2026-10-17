"""Finite-pose visible flower/leaf clearance audit; hidden mount contact excluded."""
import bpy,json,sys
from pathlib import Path
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(R/'assets/grimo/production/shushu/equipment/standard-v001/shushu-standard-appearance-v001-proof.blend'))
rows=[]
for frame in [1,103,189,197,205,221,229,405,413,589,1089,1113,1149]:
 bpy.context.scene.frame_set(frame);dg=bpy.context.evaluated_depsgraph_get()
 trees={}
 for name in ['ShushuStatic_Head','ShushuStatic_Ear_L','ShushuStatic_Ear_R']:
  o=bpy.data.objects[name].evaluated_get(dg);me=o.to_mesh();trees[name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[tuple(p.vertices) for p in me.polygons]);o.to_mesh_clear()
 for source in bpy.data.objects['Shushu_HeadFlower_v001'].children:
  if not ('Petals' in source.name or source.name.startswith('Leaf_')):continue
  o=source.evaluated_get(dg);me=o.to_mesh();points=[o.matrix_world@v.co for v in me.vertices];o.to_mesh_clear()
  for name,tree in trees.items():
   samples=[tree.find_nearest(p) for p in points]
   signed=[(p-q[0]).dot(q[1]) for p,q in zip(points,samples)]
   rows.append({'frame':frame,'part':source.name,'body':name,'minNearestDistance':min(q[3] for q in samples),'minNearestNormalSigned':min(signed),'verticesBelowMinus1mm':sum(s<-.001 for s in signed)})
report={'scope':'13 selected actual poses; nearest-normal vertex test on visible petals and leaves versus evaluated Head/ears. Not exact triangle intersection or arbitrary-input proof. Hidden backing/stalk/calyx intentional contact excluded; eye visibility reviewed in renders.','rows':rows}
(R/'docs/production/shushu/evidence/standard-appearance-v001/visible-clearance.json').write_text(json.dumps(report,indent=2))
print('EQUIPMENT_CLEARANCE',min(r['minNearestNormalSigned'] for r in rows),sum(r['verticesBelowMinus1mm'] for r in rows),flush=True)
