"""Focused static GLB proof and actual whole-body texture reimport render."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'scripts/blender/verify-jill-texture-glb-v005.py').read_text(encoding='utf8')
source=source.replace("E=ROOT/'docs/production/jill/texture-return-v005'","E=ROOT/'docs/production/jill/clover-v007'").replace("A=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005'","A=ROOT/'assets/grimo/production/jill/tripo/clover-v007'")
source=source.replace('jill-textured-rig-v005.blend','jill-textured-rig-v007.blend').replace('jill-textured-rig-v005.glb','jill-textured-rig-v007.glb')
source=source.replace("bpy.ops.wm.open_mainfile(filepath=str(A/", "ns['E']=E\nbpy.ops.wm.open_mainfile(filepath=str(A/")
source=source.replace("['front','side','3q']:ns['render']('reimport-'+state,view)","['front','side','3q']:ns['render']('reimport-'+state,view,False)")
exec(compile(source,'<v007 fresh import>','exec'),globals())
