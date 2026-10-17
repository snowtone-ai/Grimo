"""Remove only dark eye-art residuals on the surrounding host skin."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/eye-boundary-v008';A=ROOT/'assets/grimo/production/jill/tripo/eye-boundary-v008'
SOURCE=ROOT/'assets/grimo/production/jill/tripo/clover-v007/jill-basecolor-v007.png'
im=np.array(Image.open(SOURCE).convert('RGB'));out=im.copy();N=len(im);mask=np.zeros((N,N),bool);field=np.zeros_like(im);eligible=np.zeros_like(mask)
d=np.load(E/'host-surface.npz');owner=np.array(Image.open(ROOT/'docs/production/jill/rig-pretexture-technical-v003/paint-owner-mask.png'));body=json.loads((ROOT/'docs/production/jill/rig-pretexture-technical-v003/paint-owner-mask.json').read_text())['ids']['body_skin']
for xyz,uv in zip(d['xyz'],d['uv']):
    p=uv*[N,-N]+[-.5,N-.5];lo=np.maximum(np.floor(p.min(0)).astype(int)-2,0);hi=np.minimum(np.ceil(p.max(0)).astype(int)+2,N-1);B=np.stack((p[1]-p[0],p[2]-p[0]),1)
    if abs(np.linalg.det(B))<1e-12:continue
    yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];q=np.c_[xx.ravel(),yy.ravel()];ab=(q-p[0])@np.linalg.inv(B).T;w=np.c_[1-ab.sum(1),ab];alt=abs(np.linalg.det(B))/np.linalg.norm(np.roll(p,-1,axis=0)-np.roll(p,-2,axis=0),axis=1)
    ok=(w*alt>=-2).all(1)&np.isin(owner[q[:,1],q[:,0]],[0,body]);q=q[ok];v=w[ok]@xyz;x,h,f=v[:,0],v[:,2],-v[:,1]
    ok=(f>.18)&(abs(x)>.055)&(abs(x)<.205)&(h>.595)&(h<.755)&((((abs(x)-.114)/.082)**2+((h-.674)/.087)**2)<1)
    q=q[ok];h=h[ok];xx,yy=q.T;a=np.clip((h-.635)/.055,0,1)[:,None];field[yy,xx]=np.rint([244,236,151]*(1-a)+np.array([176,230,93])*a).astype('uint8');eligible[yy,xx]=True
mask=eligible&(im.max(2)<170)
# Two texels around the dark footprint remove filtering fringes; actual eye,
# eyelid and all other owners are excluded. No whole-face recoloring.
core=mask.copy()
for dy,dx in [(0,1),(0,-1),(1,0),(-1,0),(0,2),(0,-2),(2,0),(-2,0)]:mask|=np.roll(core,(dy,dx),(0,1))&eligible
out[mask]=field[mask];changed=np.any(out!=im,2);assert changed.sum()>100 and np.array_equal(out[~mask],im[~mask])
Image.fromarray(out).save(A/'jill-basecolor-v008.png');Image.fromarray(mask.astype('uint8')*255).save(E/'host-eye-uv-mask.png')
(E/'texture-diff.json').write_text(json.dumps({'pass':True,'changed_pixels':int(changed.sum()),'mask_pixels':int(mask.sum()),'outside_local_mask_exact':True,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((A/'jill-basecolor-v008.png').read_bytes()).hexdigest(),'owner':'body_skin plus <=2 texel owner-free gutter; eye and lid artwork preserved','root_cause':'Old host-eye cleanup used front > .278 m and missed lateral dark eye art. It was visible beyond the real eye/lid edge.','method':'Existing local body triangles, bounded dark residual footprint, same green/cream skin field used by v005; no geometry or UV edits.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Local changed pixels',int(changed.sum()),flush=True)
