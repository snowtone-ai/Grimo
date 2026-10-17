import bpy,json,numpy as np,sys,importlib.util
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
bpy.ops.wm.open_mainfile(filepath=str(B/'shushu-v004-motion-gate-v003.blend'));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');b=g.r.b
out={'bones':{x.name:{'head':list(x.head_local),'tail':list(x.tail_local)} for x in rig.data.bones if any(t in x.name for t in ['Shoulder','ForeArm','Hand','Spine2'])}}
o=bpy.data.objects['ShushuStatic_Torso'];p=np.array([v.co[:] for v in o.data.vertices]);mask=(p[:,1]<-.08)&(p[:,2]>.17)&(p[:,2]<.27)
out['belly_weights']=[{'i':int(i),'base':p[i].tolist(),'weights':{o.vertex_groups[a.group].name:a.weight for a in o.data.vertices[i].groups}} for i in np.where(mask)[0][::30]]
comparisons=[]
for seat in [.35,.5,1]:
 b.state(rig,{'Seat':seat});q,t=b.evaluated(o);keys=o.data.shape_keys
 values={k.name:k.value for k in keys.key_blocks if k.name.startswith('Corrective.TrueSeat.')}
 for fc in keys.animation_data.drivers:
  if 'Corrective.TrueSeat.' in fc.data_path:fc.mute=True
 for k in keys.key_blocks:
  if k.name.startswith('Corrective.TrueSeat.'):k.value=0
 o.update_tag();bpy.context.view_layer.update();raw,_=b.evaluated(o)
 comparisons.append({'seat':seat,'max_belly_correction':float(np.linalg.norm((q-raw)[mask],axis=1).max())})
 np.savez_compressed(D/f'belly-skin-isolation-{seat}.npz',base=p,corrected=q,skin_only=raw,tri=t)
 for fc in keys.animation_data.drivers:
  if 'Corrective.TrueSeat.' in fc.data_path:fc.mute=False
 b.state(rig,{'Seat':seat})
out['seat_corrective_comparison']=comparisons
(D/'structure-probe.json').write_text(json.dumps(out,indent=2))
# Fixed-camera rays identify actual source belly triangles, not screen colour guesses.
b.state(rig,{'Seat':.35});q,t=b.evaluated(o);tree=BVHTree.FromPolygons(q.tolist(),t.tolist(),all_triangles=True)
cam=bpy.data.objects.new('ABC_DIAGNOSTIC_CAMERA',bpy.data.cameras.new('ABC_DIAGNOSTIC_CAMERA'));bpy.context.scene.collection.objects.link(cam);cam.location=(-2,-2.5,.65);cam.rotation_euler=(Vector((0,0,.5))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();rot=cam.matrix_world.to_3x3();rays=[]
for y in range(440,525,3):
 for x in range(280,460,3):
  origin=cam.location+rot@Vector(((x/640-.5)*1.18,(.5-y/640)*1.18,0));hit,n,idx,dist=tree.ray_cast(origin,rot@Vector((0,0,-1)))
  if hit is not None:rays.append({'pixel':[x,y],'mesh':o.name,'triangle':idx,'vertices':t[idx].tolist(),'world':list(hit)})
(D/'belly-source-triangles.json').write_text(json.dumps(rays,indent=2));print('STRUCTURE_PROBE_COMPLETE',flush=True)
