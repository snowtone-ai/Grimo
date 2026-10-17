"""Mask only legacy internal body texels beneath the existing W contour."""
from pathlib import Path
import numpy as np,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/texture-return-v005/upper-w-local';A=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005'
cache=ROOT.parent/'jill-texture-v005-scratch';xyz=np.load(cache/'xyz.npy');owners=np.load(cache/'owners.npy')
ids=json.loads((ROOT/'docs/production/jill/rig-pretexture-technical-v003/paint-owner-mask.json').read_text())['ids']
rows=json.loads((E/'rim-targets.json').read_text());rows=sorted(rows,key=lambda r:r['before'][0]);xs=[r['before'][0] for r in rows];zs=[r['target'][2] for r in rows]
x=xyz[:,:,0];h=xyz[:,:,1];f=xyz[:,:,2]
mask=(owners==ids['body_skin'])&(abs(x)<.044)&(h>.618)&(h<np.interp(x,xs,zs)-.001)&(f>.36)
img=np.array(Image.open(A/'jill-basecolor-v005.png').convert('RGBA'));img[mask,3]=0
path=A/'jill-basecolor-upper-w-local-v005.png';Image.fromarray(img).save(path);Image.fromarray((mask*255).astype('uint8')).save(E/'legacy-internal-alpha-mask.png')
(E/'alpha-mask.json').write_text(json.dumps({'pixels':int(mask.sum()),'rgb_unchanged':True,'scope':'Only original body-owned old internal mouth/teeth below the preserved W contour; all other texels alpha 255.','output':path.name},indent=2)+'\n')
