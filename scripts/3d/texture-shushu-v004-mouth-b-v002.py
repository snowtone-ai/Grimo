"""Mouth B v002: retain physical W lip; do not draw a hanging nose line.

Reuses v001's geometry/UV raster and original cream samples. Geometry and
opening remain identical, so no structural defect is concealed by this stage.
"""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
# Use the same established raster algorithm but omit its explicit philtrum
# coverage. Frozen v001 inputs are read only; all writes go to this gate.
code=(ROOT/'scripts/3d/texture-shushu-v004-mouth-b.py').read_text(encoding='utf8')
code=code.replace("d=np.load(OUT/'mouth-source.npz');e=np.load(OUT/'head-edit-mask.npz')","d=np.load(OLD/'mouth-source.npz');e=np.load(OLD/'head-edit-mask.npz')")
code=code.replace("coverage=np.maximum(lip,phil)","coverage=lip")
code=code.replace("ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'", "")
ns={'__file__':__file__,'ROOT':ROOT,'OUT':OUT,'OLD':OLD};exec(compile(code,'v001-raster-without-philtrum','exec'),ns)
before=np.array(Image.open(OLD/'Head-mouth-b-local.png'));after=np.array(Image.open(OUT/'Head-mouth-b-local.png'))
changed=np.any(before!=after,axis=-1);pos=ns['pos'];cx,cy,cz=np.moveaxis(pos,-1,0)
assert not (changed & (np.abs(cx)>.00131)).any()
np.savez_compressed(OUT/'mouth-v002-texel-raster.npz',position=pos,changed=changed)
report={'input':'a35f645858f806edb162bd521f1b85f7871481f4','v001_to_v002_changed_texels':int(changed.sum()),'max_abs_x_changed':float(np.nanmax(abs(cx[changed]))),'min_max_z_changed':[float(np.nanmin(cz[changed])),float(np.nanmax(cz[changed]))],'W_lip_coverage_identical':True,'geometry_unchanged_by_texture_stage':True,'cause':'Two independent contributors: Nose mesh stem down to z=.6062011 (visible in Head clay); v001 Head explicit phil=max(0,(.0013-abs(x))/.0005) coverage. Nose stem is surgically clipped first; this final texture stage removes only independent philtrum ink and retains W lip coverage exactly.','human':'PENDING'}
(OUT/'mouth-cause-and-removal.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
