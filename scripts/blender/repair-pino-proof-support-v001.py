"""Repair only the saved foot-IK endpoint curves; do not rerender the four tests."""
import bpy,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'assets/grimo/production/pino/candidate-c/rig-v001';OUT=ROOT/'docs/production/pino/evidence/rig-v001'
bpy.ops.wm.open_mainfile(filepath=str(D/'pino-c-base-rig-v001-proof.blend'));scene=bpy.context.scene;o=bpy.data.objects['PINO_C_BASE_RIG_V001'];rig=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001']
def metric(frame):
 scene.frame_set(frame);bpy.context.view_layer.update();e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());v=np.array([tuple(e.matrix_world@p.co) for p in e.data.vertices]);return {'frame':frame,'min_z':float(v[:,2].min()),'below_floor_vertices':int(np.sum(v[:,2]<-.001))}
before=metric(232);action=rig.animation_data.action;slot=rig.animation_data.action_slot;changed=0
for layer in action.layers:
 for strip in layer.strips:
  bag=strip.channelbag(slot)
  if bag:
   for fc in bag.fcurves:
    if 'constraints' in fc.data_path and ('Pino_foot_no_stretch' in fc.data_path or 'Copy Rotation' in fc.data_path):
     for p in fc.keyframe_points:
      if p.co.x>=187 and p.co.y!=1:p.co.y=1;changed+=1
     fc.update()
after=metric(232);assert before['below_floor_vertices']>0 and after['below_floor_vertices']==0
scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(D/'pino-c-base-rig-v001-proof.blend'))
(OUT/'interpolation-repair.json').write_text(json.dumps({'cause':'Foot IK influence interpolated from 1 to 0 during recovery; keep support active at both zero-strength rest endpoints. Base neutral has IK off.','before':before,'after':after,'curve_points_changed':changed},indent=2)+'\n')
print('PINO_INTERPOLATION_REPAIR',before,after)
