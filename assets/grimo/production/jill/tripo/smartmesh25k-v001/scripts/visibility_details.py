"""Unoccluded wing undersides and right-side diagnostic views; read-only master."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *
scene=bpy.context.scene
master=bpy.data.objects['JILL_GEOMETRY_MASTER']
original=bpy.data.objects['REFERENCE_FBX_UNEDITED']
ref=bpy.data.collections['00_REFERENCE_FBX_LOCKED']
scene.frame_set(1)
for label,obj in [('before-fbx',original),('after-fbx',master)]:
    ref.hide_render=obj!=original;original.hide_render=obj!=original;master.hide_render=obj!=master
    for side,name in [(1,'left'),(-1,'right')]:
        render(scene,label+'-wing-underside-detail-'+name,(side,3,-.5),(.25*side,.04,.56),.55)
ref.hide_render=True;original.hide_render=True;master.hide_render=False
proof=json.loads((EVIDENCE/'deformation-validation.json').read_text())
for ci,c in enumerate(proof['cases']):
    if c['name'] in ['WingR_Open','WingR_Close','ArmR_Offer','Combined_Right']:
        scene.frame_set(1+24*ci+12)
        render(scene,'proof-'+c['name']+'-opposite-side',(-1,0,0),(0,0,.5),1.16)
print('VISIBILITY_DETAILS_COMPLETE; master not saved')
