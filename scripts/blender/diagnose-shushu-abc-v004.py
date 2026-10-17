"""Read-only source diagnosis for Human arm/mouth/belly FAIL, 2026-10-17."""
import bpy,sys,json,importlib.util,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2]
D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004'
D.mkdir(parents=True,exist_ok=True)
B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
bpy.ops.wm.open_mainfile(filepath=str(B/'shushu-v004-motion-gate-v003-proof.blend'))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');rows=[];payload={}
for o in bpy.data.objects:
 if o.type!='MESH' or not o.name.startswith('ShushuStatic_'):continue
 o.data.calc_loop_triangles();payload[o.name+'__tri']=np.array([t.vertices[:] for t in o.data.loop_triangles]);payload[o.name+'__base']=np.array([v.co[:] for v in o.data.vertices])
 if o.name in ['ShushuStatic_Torso','ShushuStatic_Head','ShushuStatic_MouthInterior','ShushuStatic_OralBowl','ShushuStatic_Tongue']:
  for k in o.data.shape_keys.key_blocks:payload[o.name+'__key__'+k.name]=np.array([v.co[:] for v in k.data])
for f in [1,103,1041,1085,1089,1095,1101,1107,1110,1113,1117,1119,1125,1149]:
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update()
 row={'frame':f,'controls':{k:float(rig[k]) for k in ['Seat','WeightShift','Hold.L','Hold.R','SelfContact.R','Offer.L','MouthOpen','MouthClose','Tongue','Blink.R','CheekPressure.R']},'active':{}}
 for o in bpy.data.objects:
  if o.type!='MESH' or not o.name.startswith('ShushuStatic_'):continue
  if o.data.shape_keys:row['active'][o.name]={k.name:float(k.value) for k in o.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.shape_keys.key_blocks[1:] if abs(k.value)>1e-6}
  if o.name in ['ShushuStatic_Torso','ShushuStatic_Head','ShushuStatic_MouthInterior','ShushuStatic_OralBowl','ShushuStatic_Tongue','ShushuStatic_Paw_L','ShushuStatic_Paw_R']:payload[o.name+'__f'+str(f)]=g.evaluate(o)
 rows.append(row)
inventory={o.name:{'vertices':len(o.data.vertices),'groups':[v.name for v in o.vertex_groups],'modifiers':[(m.name,m.type) for m in o.modifiers],'drivers':[(d.data_path,d.driver.expression) for d in o.data.shape_keys.animation_data.drivers] if o.data.shape_keys and o.data.shape_keys.animation_data else []} for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')}
np.savez_compressed(D/'source-diagnosis.npz',**payload)
(D/'source-diagnosis.json').write_text(json.dumps({'source_sha256':hashlib.sha256((B/'shushu-v004-motion-gate-v003-proof.blend').read_bytes()).hexdigest(),'inventory':inventory,'frames':rows},indent=2),encoding='utf-8')
scene,cam=g.r.b.setup_review(640,8);scene.render.engine='BLENDER_EEVEE';cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location=(-2,-2.5,.65);cam.rotation_euler=(Vector((0,0,.5))-cam.location).to_track_quat('-Z','Y').to_euler()
for f in [1089,1095,1101,1107,1113,1119]:
 scene.frame_set(f);scene.render.filepath=str(D/f'source-f{f}.png');bpy.ops.render.render(write_still=True)
print('SOURCE_DIAGNOSIS_COMPLETE',flush=True)
