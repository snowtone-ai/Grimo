"""UV0 orientation/owner fixture and polygon masks; never production artwork."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from scipy.ndimage import distance_transform_edt
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/rig-pretexture-technical-v003'
d=np.load(E/'after.npz');q=d['uv'][d['loops']];owners=json.loads((E/'material-ownership.json').read_text())['polygon_owners'];names=sorted(set(owners));ids={n:i+1 for i,n in enumerate(names)};size=4096
mask=Image.new('I',(size,size));draw=ImageDraw.Draw(mask)
for uv,pi in zip(q,d['polygons']):draw.polygon([(float(u*(size-1)),float((1-v)*(size-1))) for u,v in uv],fill=ids[owners[pi]])
a=np.asarray(mask);Image.fromarray(a.astype('uint16')).save(E/'paint-owner-mask.png')
pixels={n:int(np.count_nonzero(a==i)) for n,i in ids.items()}
yy,xx=np.mgrid[:size,:size];checker=((xx//32+yy//32)%2)*.25+.7
rgb=np.zeros((size,size,3),dtype=np.uint8)
for name,i in ids.items():
    color=np.array([65+(i*53)%170,65+(i*97)%170,65+(i*31)%170]);sel=a==i;rgb[sel]=np.clip(color[None,:]*checker[sel,None],0,255).astype('uint8')
# Add a 4px nearest-colour dilation as a bounded mip/filter diagnostic.
dist,index=distance_transform_edt(a==0,return_indices=True);fill=(a==0)&(dist<=4);rgb[fill]=rgb[index[0][fill],index[1][fill]]
im=Image.fromarray(rgb);dr=ImageDraw.Draw(im)
for y in range(0,size,256):
    for x in range(0,size,256):dr.text((x+4,y+4),f'U{x//256} V{15-y//256}',fill='white')
im.save(E/'diagnostic-uv0.png')
im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(E/'diagnostic-uv-changed.png')
(E/'paint-owner-mask.json').write_text(json.dumps({'resolution':size,'ids':ids,'pixels':pixels,'zero_pixel_owners':[n for n,p in pixels.items() if not p],'dilation_px':4,'purpose':'Synthetic checker, owner colours and UV0 labels only. Not formal Texture or Tripo input. Mask is uint16 IDs; no colour-space conversion.'},indent=2)+'\n')
print('OWNERS',len(names),'ZERO_PIXEL',[n for n,p in pixels.items() if not p])
