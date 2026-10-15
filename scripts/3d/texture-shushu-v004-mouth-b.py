"""Final local texture stage after geometry-clay review. UV/topology never edited.

Rasterize current closed geometry through ORIGINAL triangle UVs. Remove only
the obsolete local mouth ink with nearby original cream texels, then place a
thin seam on the actual physical lip. No pink open-mouth painting is retained.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,binary_dilation
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'
d=np.load(OUT/'mouth-source.npz');e=np.load(OUT/'head-edit-mask.npz');p=d['Head__base'];closed=e['closed'];tri=d['Head__tri'];uv=d['Head__uv']
srcpath=OUT.parent/'production-rig-v004-skin-compat/ShushuStatic_Head-original-basecolor.png'
src=np.array(Image.open(srcpath).convert('RGBA'));h,w=src.shape[:2]
pos=np.full((h,w,3),np.nan,dtype=np.float32);original=np.full_like(pos,np.nan)
cent=p[tri].mean(1);ids=np.where((abs(cent[:,0])<.073)&(cent[:,2]>.548)&(cent[:,2]<.634)&(cent[:,1]<-.218))[0]
for i in ids:
    t=tri[i];a=uv[i]*[w,-h]+[0,h];lo=np.maximum(0,np.floor(a.min(0)-1).astype(int));hi=np.minimum([w-1,h-1],np.ceil(a.max(0)+1).astype(int))
    if np.any(hi<lo):continue
    xs,ys=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5);q=np.stack([xs,ys],-1)
    v0=a[1]-a[0];v1=a[2]-a[0];det=v0[0]*v1[1]-v1[0]*v0[1]
    if abs(det)<1e-12:continue
    v=q-a[0];b1=(v[...,0]*v1[1]-v[...,1]*v1[0])/det;b2=(v0[0]*v[...,1]-v0[1]*v[...,0])/det;b0=1-b1-b2;inside=(b0>=-1e-5)&(b1>=-1e-5)&(b2>=-1e-5)
    sl=np.s_[lo[1]:hi[1]+1,lo[0]:hi[0]+1];bary=np.stack([b0,b1,b2],-1)
    pos[sl][inside]=(bary@closed[t])[inside];original[sl][inside]=(bary@p[t])[inside]
x,y,z=np.moveaxis(original,-1,0)
local=(((abs(x)<.061)&(z>.556)&(z<.624))|((abs(x)<.009)&(z>=.624)&(z<.632)))&(y<-.22)
rgb=src[...,:3].astype(float)
# Remove the pale antialiased fringe too. Four-texel UV padding prevents old
# mouth ink outside island samples from returning through runtime mipmaps.
allowed=binary_dilation(local,iterations=4)
ink=allowed&((rgb[...,0]-rgb[...,1])>5)&(rgb[...,1]<249)
# A white surrounding surface supplies actual original cream/noise, never generated skin.
safe=np.isfinite(x)&~ink&(rgb[...,0]-rgb[...,1]<5)&(rgb[...,1]>205)
assert safe.sum()>100
_,nearest=distance_transform_edt(~safe,return_indices=True)
out=src.copy();out[ink,:3]=src[nearest[0][ink],nearest[1][ink],:3]
cx,cy,cz=np.moveaxis(pos,-1,0);u=np.clip(cx/.043,-1,1);seam=.616-.010*np.maximum(0,np.sin(np.pi*np.abs(u)))**.9
dist=np.sqrt((cz-seam)**2+np.maximum(0,abs(cx)-.043)**2)
lip=np.clip((.0022-dist)/.0007,0,1)*local
phil=np.clip((.0013-abs(cx))/.0005,0,1)*((cz>=seam)&(cz<.632))*local
coverage=np.maximum(lip,phil);coverage=np.nan_to_num(coverage)
color=np.array([123,39,47]);out[...,:3]=np.round(out[...,:3]*(1-coverage[...,None])+color*coverage[...,None]).astype(np.uint8)
changed=np.any(src!=out,axis=-1)
assert not (changed&~allowed).any()
target=OUT/'Head-mouth-b-local.png';Image.fromarray(out).save(target)
Image.fromarray((changed*255).astype('uint8')).save(OUT/'head-texture-changed-mask.png')
# Original bytes and final pixel view remain explicit; texture overview is a diagnostic.
ys,xs=np.where(changed);box=(max(0,xs.min()-30),max(0,ys.min()-30),min(w,xs.max()+31),min(h,ys.max()+31))
tiles=[]
for arr in [src,out]:
    im=Image.fromarray(arr).crop(box).convert('RGB');im.thumbnail((900,900));tiles.append(im)
board=Image.new('RGB',(sum(v.width for v in tiles),max(v.height for v in tiles)+25),'white');draw=ImageDraw.Draw(board);off=0
for label,im in zip(['original texture','local geometry-aligned seam'],tiles):board.paste(im,(off,25));draw.text((off+4,5),label,fill='black');off+=im.width
board.save(OUT/'texture-before-after.png')
(OUT/'texture-authoring.json').write_text(json.dumps({'source':str(srcpath.relative_to(ROOT)),'source_sha256':hashlib.sha256(srcpath.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'changed_texels':int(changed.sum()),'head_texels':w*h,'outside_local_changes':int((changed&~allowed).sum()),'old_ink_removed':int(ink.sum()),'uv_changes':0,'geometry_unchanged_by_this_stage':True,'method':'Original UV triangle barycentric raster of geometry-closed position; local cream from nearest original cream texels; thin seam on actual physical lip. No painted open mouth or tongue.'},indent=2)+'\n')
print('TEXTURE_LOCAL',changed.sum(),'/',w*h)
