import bpy, sys, json, importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(sys.argv[sys.argv.index('--')+1]); out=Path(sys.argv[sys.argv.index('--')+2]);out.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('gate',root/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
base=root/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
bpy.ops.wm.open_mainfile(filepath=str(base/'shushu-v004-motion-gate-v002.blend'))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');g.r.b.reset(rig)
records={};payload={}
for o in bpy.data.objects:
 if o.type!='MESH' or not o.name.startswith('ShushuStatic_'):continue
 o.data.calc_loop_triangles();prefix=o.name+'__';payload[prefix+'tri']=np.array([t.vertices[:] for t in o.data.loop_triangles])
 payload[prefix+'normal']=np.array([n.vector[:] for n in o.data.vertex_normals])
 for k in o.data.shape_keys.key_blocks if o.data.shape_keys else []:payload[prefix+k.name]=g.r.coords(k)
 records[o.name]={'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'modifiers':[(m.name,m.type) for m in o.modifiers],'keys':len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0,'custom_normals':o.data.has_custom_normals,'smooth_faces':sum(p.use_smooth for p in o.data.polygons),'groups':[(v.name) for v in o.vertex_groups]}
np.savez_compressed(out/'diagnostic-source.npz',**payload)
# Match the PlayCanvas mouth camera exactly: glTF (x,y,z) = Blender (x,z,-y).
cam=bpy.data.objects.new('DIAGNOSTIC_RAY_CAMERA',bpy.data.cameras.new('DIAGNOSTIC_RAY_CAMERA'));bpy.context.scene.collection.objects.link(cam);cam.location=(-2,-2.5,.65);cam.rotation_euler=(Vector((0,-.02,.69))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
trees={};coords={}
for o in bpy.data.objects:
 if o.type!='MESH' or not o.name.startswith('ShushuStatic_'):continue
 p,n,t=g.evaluate(o,True);trees[o.name]=BVHTree.FromPolygons(p.tolist(),t.tolist(),all_triangles=True);coords[o.name]=(p,t)
rot=cam.matrix_world.to_3x3();direction=rot@Vector((0,0,-1));hits=[]
for y in range(37,76):
 for x in range(177,227):
  origin=cam.location+rot@Vector(((x/640-.5)*.56,(.5-y/640)*.56,0));row=[]
  for name,tree in trees.items():
   pt,n,idx,dist=tree.ray_cast(origin,direction)
   if pt is not None:row.append((dist,name,idx,list(pt)))
  if row:
   dist,name,idx,point=min(row);p,t=coords[name];hits.append({'pixel':[x,y],'mesh':name,'triangle':idx,'indices':t[idx].tolist(),'point':point,'triangle_positions':p[t[idx]].tolist()})
(out/'crown-rays.json').write_text(json.dumps(hits,indent=2))
bpy.ops.wm.open_mainfile(filepath=str(base/'shushu-v004-motion-gate-v002-proof.blend'))
payload={}
for f in [1,103,477,485,493,501,509,517,525,533,541,549,557,825,837,849,861,993]:
 bpy.context.scene.frame_set(f)
 for name in ['ShushuStatic_Head','ShushuStatic_Paw_L','ShushuStatic_Paw_R']:
  o=bpy.data.objects[name];p,n,t=g.evaluate(o,True);payload[name+'__p'+str(f)]=p;payload[name+'__n'+str(f)]=n
np.savez_compressed(out/'diagnostic-evaluated.npz',**payload)
(out/'scene-inventory.json').write_text(json.dumps(records,indent=2));print('DIAG_COMPLETE',flush=True)
