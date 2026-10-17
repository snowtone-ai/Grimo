"""Explicitly document the retained legacy-FK limitation; never claim support."""
import bpy, importlib.util, json, hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2]
sp=importlib.util.spec_from_file_location('repair',R/'scripts/blender/repair-shushu-abc-v004.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
bpy.ops.wm.open_mainfile(filepath=str(m.ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');m.b.reset(rig)
paws=[bpy.data.objects['ShushuStatic_Paw_'+s] for s in ['L','R']]
before=[m.b.evaluated(o)[0] for o in paws]
names=[n for n in rig.pose.bones.keys() if any(k in n for k in ['Arm','ForeArm','Hand'])]
for name in names:
 bone=rig.pose.bones[name];bone.rotation_mode='XYZ';bone.rotation_euler[1]+=.35
bpy.context.view_layer.update()
after=[m.b.evaluated(o)[0] for o in paws]
errors=[float(np.linalg.norm(a-b,axis=1).max()) for a,b in zip(after,before)]
assert max(errors)<1e-6
(m.D/'legacy-fk-contract.json').write_text(json.dumps({'asset_sha256':hashlib.sha256(m.ASSET.read_bytes()).hexdigest(),'rotated_bones':names,'radians_added':.35,'paw_max_change':errors,'status':'UNSUPPORTED, retained source contract. Use Purpose/Wrist/Seat; no unchanged legacy arm-FK compatibility is claimed. Bones/rest/parents/weights separately preserved.'},indent=2))
print('LEGACY_FK_CONTRACT',errors,flush=True)
