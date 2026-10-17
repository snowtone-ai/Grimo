"""Project the extracted Canonical decal into existing owner-bound thigh UVs only."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/clover-v007';A=ROOT/'assets/grimo/production/jill/tripo/clover-v007'
source=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005/jill-basecolor-v005.png'
image=np.array(Image.open(source).convert('RGB'));out=image.copy();N=len(image)
decal=Image.open(A/'canonical-clover-decal.png').convert('RGBA');decal=decal.crop(decal.getbbox());stamp=np.array(decal).astype(float)/255
surface=np.load(E/'thigh-surface.npz');config=json.loads((E/'projection.json').read_text());center=np.array(config['center']);tangent=np.array(config['tangent']);changed=np.zeros((N,N),bool);used=[]
owner_mask=np.array(Image.open(ROOT/'docs/production/jill/rig-pretexture-technical-v003/paint-owner-mask.png'))
body_id=json.loads((ROOT/'docs/production/jill/rig-pretexture-technical-v003/paint-owner-mask.json').read_text())['ids']['body_skin']
for ti,(pos,uv) in enumerate(zip(surface['xyz'],surface['uv'])):
    p=uv*np.array([N,-N])+[-.5,N-.5];lo=np.maximum(np.floor(p.min(0)).astype(int)-2,0);hi=np.minimum(np.ceil(p.max(0)).astype(int)+2,N-1)
    B=np.stack((p[1]-p[0],p[2]-p[0]),1)
    if abs(np.linalg.det(B))<1e-10:continue
    yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];q=np.c_[xx.ravel(),yy.ravel()];ab=(q-p[0])@np.linalg.inv(B).T;w=np.c_[1-ab.sum(1),ab]
    # Extrapolate the same 3D projection into two UV texels of gutter. Merely
    # painting triangle interiors leaves the old green under linear filtering.
    altitude=abs(np.linalg.det(B))/np.linalg.norm(np.roll(p,-1,axis=0)-np.roll(p,-2,axis=0),axis=1)
    ok=(w*altitude>=-2).all(1)&np.isin(owner_mask[q[:,1],q[:,0]],[0,body_id]);q=q[ok];w=w[ok];xyz=w@pos
    u=(xyz-center)@tangent/config['width_m']+.5;v=.5-(xyz[:,2]-center[2])/config['height_m'];ok=(u>=0)&(u<=1)&(v>=0)&(v<=1)
    q=q[ok];xyz=xyz[ok];sx=u[ok]*(stamp.shape[1]-1);sy=v[ok]*(stamp.shape[0]-1);x0=sx.astype(int);y0=sy.astype(int);x1=np.minimum(x0+1,stamp.shape[1]-1);y1=np.minimum(y0+1,stamp.shape[0]-1);fx=(sx-x0)[:,None];fy=(sy-y0)[:,None]
    samples=(stamp[y0,x0]*(1-fx)+stamp[y0,x1]*fx)*(1-fy)+(stamp[y1,x0]*(1-fx)+stamp[y1,x1]*fx)*fy
    alpha=samples[:,3:];ok=alpha[:,0]>0;q=q[ok];xyz=xyz[ok];samples=samples[ok];alpha=alpha[ok];xx,yy=q.T
    out[yy,xx]=np.rint(image[yy,xx]*(1-alpha)+samples[:,:3]*255*alpha).astype(np.uint8);changed[yy,xx]=True
    if len(q):used.extend(xyz.tolist())
assert used and changed.sum()>100
assert np.array_equal(out[~changed],image[~changed]);used=np.array(used);assert used[:,0].max()<-.12 and used[:,2].min()>.12 and used[:,2].max()<.28
Image.fromarray(out).save(A/'jill-basecolor-v007.png');Image.fromarray(changed.astype(np.uint8)*255).save(E/'clover-uv-mask.png')
(E/'texture-diff.json').write_text(json.dumps({'pass':True,'changed_pixels':int(np.any(out!=image,axis=2).sum()),'mask_pixels':int(changed.sum()),'pixels_outside_local_mask_exact':True,'xyz_min':used.min(0).tolist(),'xyz_max':used.max(0).tolist(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'decal_sha256':hashlib.sha256((A/'canonical-clover-decal.png').read_bytes()).hexdigest(),'method':'Existing thigh owner triangles only; barycentric UV0 projection, four-leaf extracted decal alpha composite; no geometry/UV change or opposite-side copy'},indent=2)+'\n')
print('Changed local pixels',changed.sum())
