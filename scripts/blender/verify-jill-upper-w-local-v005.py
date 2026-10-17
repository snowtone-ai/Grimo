"""Reuse the UV/owner-bound fresh-import proof for this isolated candidate."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'scripts/blender/verify-jill-texture-glb-v005.py').read_text(encoding='utf8')
source=source.replace("E=ROOT/'docs/production/jill/texture-return-v005'","E=ROOT/'docs/production/jill/texture-return-v005/upper-w-local'")
source=source.replace('jill-textured-rig-v005.blend','jill-upper-w-local-v005.blend').replace('jill-textured-rig-v005.glb','jill-upper-w-local-v005.glb')
source=source.replace("bpy.ops.wm.open_mainfile(filepath=str(A/", "ns['E']=E\nbpy.ops.wm.open_mainfile(filepath=str(A/")
exec(compile(source,'<upper W fresh import>','exec'),globals())
