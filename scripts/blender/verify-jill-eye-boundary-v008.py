"""Fresh v008 GLB import: actual eye/mouth states and texture routing."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
s=(ROOT/'scripts/blender/verify-jill-texture-glb-v005.py').read_text(encoding='utf8')
s=s.replace("E=ROOT/'docs/production/jill/texture-return-v005'","E=ROOT/'docs/production/jill/eye-boundary-v008'").replace("A=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005'","A=ROOT/'assets/grimo/production/jill/tripo/eye-boundary-v008'")
s=s.replace('jill-textured-rig-v005.blend','jill-textured-rig-v008.blend').replace('jill-textured-rig-v005.glb','jill-textured-rig-v008.glb')
s=s.replace("bpy.ops.wm.open_mainfile(filepath=str(A/", "ns['E']=E\nbpy.ops.wm.open_mainfile(filepath=str(A/")
exec(compile(s,'<v008 fresh import>','exec'),globals())
