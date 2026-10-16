"""Reuse the verified FBX/GLB image-only protocol on the new mouth geometry.

Only output/source paths are rebound. Existing v003 evidence stays read-only.
The asymmetric synthetic test images and UV0 contract are unchanged.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD_E=ROOT/'docs/production/jill/rig-pretexture-technical-v003'
source=(ROOT/'scripts/blender/prove-jill-texture-transfer-v003.py').read_text(encoding='utf8')
for a,b in [
    ('rig-pretexture-technical-v003','mouth-profile-v004'),
    ('jill-rig-texture-uv-v003.blend','jill-rig-mouth-profile-v004.blend'),
    ('jill-texture-input-neutral-v003','jill-texture-input-neutral-v004'),
    ('Jill_Texture_Input_Neutral_v003','Jill_Texture_Input_Neutral_v004'),
    ("E/'diagnostic-uv0.png'","OLD_E/'diagnostic-uv0.png'"),
    ("E/'diagnostic-uv-changed.png'","OLD_E/'diagnostic-uv-changed.png'"),
]:source=source.replace(a,b)
exec(compile(source,str(ROOT/'scripts/blender/prove-jill-texture-transfer-v003.py'),'exec'),globals())
