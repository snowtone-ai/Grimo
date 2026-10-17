"""Reuse the owner/UV/position-bound proof against this candidate, not old geometry."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'scripts/blender/verify-jill-texture-glb-v005.py').read_text(encoding='utf8')
source=source.replace("E=ROOT/'docs/production/jill/texture-return-v005'","E=ROOT/'docs/production/jill/mouth-integration-v006'")
source=source.replace("A=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005'","A=ROOT/'assets/grimo/production/jill/tripo/mouth-integration-v006'")
source=source.replace('jill-textured-rig-v005.blend','jill-textured-rig-v006.blend').replace('jill-textured-rig-v005.glb','jill-textured-rig-v006.glb')
source=source.replace("bpy.ops.wm.open_mainfile(filepath=str(A/", "ns['E']=E\nbpy.ops.wm.open_mainfile(filepath=str(A/")
source=source.replace("states=['neutral','blink-half','blink-full','mouth-closed','mouth-small','mouth-large','recovery']", "ns['STATES'].update({'open-smile':{'mouth_open':1,'smile.L':1,'smile.R':1},'closed-open-smile':{'mouth_close':1,'mouth_open':1,'smile.L':1,'smile.R':1}})\nstates=['neutral','blink-half','blink-full','mouth-closed','mouth-small','mouth-large','combined','open-smile','closed-open-smile','recovery']")
source=source.replace("ns['E']=E", "ns['E']=E\nns['STATES']['combined']={'blink.L':.5,'blink.R':.5,'mouth_open':.5}")
exec(compile(source,'<integrated mouth fresh import>','exec'),globals())
