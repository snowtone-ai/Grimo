"""Bounded representative proof, local exports and actual rendered evidence."""
import bpy, json, math, sys, hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-v002'
E=ROOT/'docs/production/jill/rig-pretexture-v002'
bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-pretexture-v002.blend'))
s=bpy.context.scene;r=bpy.data.objects['JILL_RIG'];b=bpy.data.objects['Jill_Body'];cam=s.camera
channels=list(json.loads((E/'control-contract.json').read_text())['authoring_properties'])
def update():r.update_tag();bpy.context.view_layer.update()
def apply(values):
 for k in channels:r[k]=0.
 for k,v in values.items():r[k]=float(v)
 update()
def xyz():
 ev=b.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();q=np.array([tuple(b.matrix_world@v.co) for v in m.vertices]);ev.to_mesh_clear();return q
VIEWS={'front':(0,-1,0),'side':(1,0,0),'3q':(1,-2,.12),'back3q':(1,2,.1)}
def render(name,view='3q',face=False,res=640):
 target=Vector((0,-.24,.68) if face else (0,0,.50));d=Vector(VIEWS[view]);cam.location=target+d.normalized()*5
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.44 if face else 1.16
 s.render.resolution_x=res;s.render.resolution_y=res;s.render.image_settings.file_format='PNG';s.render.filepath=str(E/'renders'/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
if '--preview' in sys.argv:
 for name,val in [('smile',{}),('closed',{'mouth_close':1}),('big',{'mouth_open':1}),('half',{'blink.L':.5,'blink.R':.5}),('blink',{'blink.L':1,'blink.R':1})]:
  apply(val)
  for view in ['front','3q']:render('preview-'+name,view,True)
 print('PREVIEW_DONE');sys.exit(0)

CASES=[
 ('mouth',[(0,{'mouth_close':1}),(6,{'mouth_close':.65}),(12,{}),(18,{'mouth_open':1}),(24,{'mouth_close':1})]),
 ('blink',[(0,{}),(6,{'blink.L':.5,'blink.R':.5}),(12,{'blink.L':1,'blink.R':1}),(18,{'blink.L':.5,'blink.R':.5}),(24,{})]),
 ('head',[(0,{}),(6,{'head_yaw':.5,'head_nod':.2}),(12,{'head_yaw':1,'head_nod':.4,'head_tilt':.3}),(18,{'head_yaw':-.5}),(24,{})]),
 ('wing-L',[(0,{}),(6,{'wing_open.L':.5}),(12,{'wing_open.L':1,'wing_camber.L':.5}),(18,{'wing_open.L':-1}),(24,{})]),
 ('wing-R',[(0,{}),(6,{'wing_open.R':.5}),(12,{'wing_open.R':1,'wing_camber.R':.5}),(18,{'wing_open.R':-1}),(24,{})]),
 ('wings-fold',[(0,{}),(6,{'wing_open.L':-.5,'wing_open.R':-.5}),(12,{'wing_open.L':-1,'wing_open.R':-1}),(18,{'wing_open.L':-.5,'wing_open.R':-.5}),(24,{})]),
 ('paw-L',[(0,{}),(6,{'paw_offer.L':.5}),(12,{'paw_offer.L':1,'paw_turn.L':.3}),(18,{'paw_offer.L':.5}),(24,{})]),
 ('paw-R',[(0,{}),(6,{'paw_offer.R':.5}),(12,{'paw_offer.R':1,'paw_turn.R':-.3}),(18,{'paw_offer.R':.5}),(24,{})]),
 ('tail-leaves',[(0,{}),(6,{'tail_sway':.5,'leaves_tail':.3}),(12,{'tail_sway':1,'tail_curl':.3,'leaves_tail':.5,'leaves_neck.L':.5}),(18,{'tail_sway':-.5,'leaves_tail':-.3}),(24,{})]),
 ('combined-L',[(0,{}),(6,{'head_yaw':-.25,'wing_open.L':.4,'paw_offer.L':.35,'tail_sway':.3,'blink.R':.25}),
 (12,{'head_yaw':-.5,'head_tilt':.3,'wing_open.L':.8,'wing_open.R':-.65,'paw_offer.L':.7,'tail_sway':.65,'blink.R':.5,'mouth_close':.6,'leaves_neck.L':.5,'breath':.7}),
 (18,{'head_yaw':-.25,'wing_open.L':.4,'paw_offer.L':.35,'tail_sway':.3,'blink.R':.25}),(24,{})]),
 ('combined-R',[(0,{}),(6,{'head_yaw':.25,'wing_open.R':.4,'paw_offer.R':.35,'tail_sway':-.3,'blink.L':.25}),
 (12,{'head_yaw':.5,'head_tilt':-.3,'wing_open.R':.8,'wing_open.L':-.65,'paw_offer.R':.7,'tail_sway':-.65,'blink.L':.5,'mouth_open':.35,'leaves_neck.R':.5}),
 (18,{'head_yaw':.25,'wing_open.R':.4,'paw_offer.R':.35,'tail_sway':-.3,'blink.L':.25}),(24,{})])]
apply({});base=xyz();samples={'neutral':base};schedule=[];reports=[]
for ci,(name,points) in enumerate(CASES):
 start=1+ci*28
 for offset,values in points:
  # Frame boundary is shared, all cases except mouth return to neutral.
  frame=start+offset;s.frame_set(frame);apply(values)
  for k in channels:r.keyframe_insert(data_path='["'+k+'"]',frame=frame)
  p=xyz();samples[name+'-'+str(offset)]=p
  reports.append({'case':name,'frame':frame,'offset':offset,'finite':bool(np.isfinite(p).all()),'return_delta':float(np.linalg.norm(p-base,axis=1).max()) if offset==24 and name!='mouth' else None})
 schedule.append({'name':name,'start':start,'half':start+6,'peak':start+12,'end':start+18,'return':start+24,'values':points})
r.animation_data.action.name='Jill_Pretexture_Bounded_Proof'
for layer in r.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
s.frame_start=1;s.frame_end=1+(len(CASES)-1)*28+24;s.render.fps=24
# Save with the Canonical smile displayed at the mouth's middle opening.
s.frame_set(13);update();bpy.ops.wm.save_as_mainfile(filepath=str(A/'jill-rig-pretexture-v002.blend'))
for o in s.objects:o.select_set(o.type not in ['CAMERA','LIGHT'] and not o.name.startswith('CTRL_'))
bpy.context.view_layer.objects.active=r
bpy.ops.export_scene.gltf(filepath=str(A/'jill-rig-pretexture-v002.glb'),export_format='GLB',use_selection=True,
 export_animations=True,export_animation_mode='SCENE',export_force_sampling=True,export_frame_range=True,export_frame_step=1,
 export_bake_animation=True,export_skins=True,export_def_bones=False,export_morph=True,export_morph_animation=True,
 export_all_influences=False,export_influence_nb=4,export_extras=True,export_cameras=False,export_lights=False)
np.savez_compressed(E/'proof-positions.npz',**samples)
(E/'proof-schedule.json').write_text(json.dumps(schedule,indent=2),encoding='utf8')
(E/'pose-validation.json').write_text(json.dumps({'samples':reports,'scope':'Bounded proof, no full Motion library or continuous collision solver'},indent=2),encoding='utf8')
if '--no-render' in sys.argv:sys.exit(0)
for case in schedule:
 phases=['half','peak','end','return'] if case['name'] in ['mouth','blink','head','wings-fold','combined-L','combined-R'] else ['half','peak','return']
 for phase in phases:
  s.frame_set(case[phase]);update()
  for view in ['front','side','3q']:render(case['name']+'-'+phase,view,res=480)
  if case['name'] in ['mouth','blink']:
   for view in ['front','side','3q']:render('face-'+case['name']+'-'+phase,view,True,res=640)
 if case['name'] in ['wings-fold','combined-L','tail-leaves','paw-L','head']:
  s.frame_set(case['peak']);update();render(case['name']+'-root','back3q',res=640)
s.frame_set(13);update()
for view in ['front','side','3q','back3q']:render('smile',view,res=640)
print('PROOF_DONE',s.frame_end)
