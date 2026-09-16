"""Extract the existing historical look screenshot, never geometry."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
src=root/'docs/production/carol/evidence/blockout-v004/historical-benchmark-front.png'
out=root/'docs/production/carol/evidence/reconstruction-v006'
image=Image.open(src).convert('RGBA').crop((0,70,1100,948))
a=np.array(image);background=np.max(np.abs(a[:,:,:3].astype(int)-a[0,0,:3]),axis=2)<4
barrier=Image.fromarray(np.where(background,0,255).astype('uint8')).copy()
ImageDraw.floodfill(barrier,(0,0),128);a[:,:,3]=np.where(np.asarray(barrier)==128,0,255)
image=Image.fromarray(a);image=image.crop(image.getbbox());image.save(out/'old-look-native.png')
(out/'old-look-provenance.json').write_text(json.dumps({'source':str(src.relative_to(root)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'processing':'Toolbar crop; border-connected flat background removed; original character pixels retained.','view':'historical front, fixed across all review tabs','authority':'LOOK ONLY; not used for new geometry or camera fitting'},indent=2))
