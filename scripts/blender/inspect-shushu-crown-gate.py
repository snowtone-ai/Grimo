import bpy,sys,json,importlib.util
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2];sp=importlib.util.spec_from_file_location('g',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
bpy.ops.wm.open_mainfile(filepath=str(g.ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');g.r.b.reset(rig);scene,cam=g.r.b.setup_review(640,4);cam.data.type='ORTHO';cam.data.ortho_scale=.56;cam.location=g.r.VIEWS['front'];cam.rotation_euler=(Vector((0,-.02,.69))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
trees={};coords={}
for o in bpy.data.objects:
 if o.type!='MESH' or not o.name.startswith('ShushuStatic_'):continue
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles();p=[ev.matrix_world@v.co for v in m.vertices];t=[x.vertices[:] for x in m.loop_triangles];trees[o.name]=BVHTree.FromPolygons(p,t,all_triangles=True);coords[o.name]=(p,t);ev.to_mesh_clear()
rows=[];rot=cam.matrix_world.to_3x3();direction=rot@Vector((0,0,-1))
for y in range(36,48):
 for x in range(207,224):
  origin=cam.location+rot@Vector(((x/640-.5)*.56,(.5-y/640)*.56,0));hits=[]
  for name,tree in trees.items():
   pt,n,idx,dist=tree.ray_cast(origin,direction)
   if pt is not None:hits.append((dist,name,idx,list(pt)))
  if hits:
   hit=min(hits);rows.append({'pixel':[x,y],'object':hit[1],'triangle':hit[2],'point':hit[3],'vertices':[list(coords[hit[1]][0][i]) for i in coords[hit[1]][1][hit[2]]]})
g.write('crown-ray-inspection.json',rows)
print('CROWN',sorted(set((x['object'],x['triangle']) for x in rows)),flush=True)
