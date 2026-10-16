"""Deterministic face-correspondence resampling and bounded review-only fills.

No generated artwork or diagnostic palette. Source JPEG remains byte-exact.
Colour samples are provisional Tripo samples, NOT Human approved RGB swatches.
"""
import json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/texture-return-v005';A=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005';OLD=ROOT/'docs/production/jill/rig-pretexture-technical-v003'
assert json.loads((E/'correspondence.json').read_text())['pass']
with np.load(E/'face-owner-correspondence.npz') as packed:d={k:packed[k] for k in packed.files}
N=4096
source=np.array(Image.open(A/'source/original-basecolor-0.jpg').convert('RGB'));out=source.copy();xyz=np.zeros((N,N,3),np.float32);cover=np.zeros((N,N),bool)
ids=json.loads((OLD/'paint-owner-mask.json').read_text())['ids'];owners=np.zeros((N,N),np.uint8)
CACHE=ROOT.parent/'jill-texture-v005-scratch';CACHE.mkdir(exist_ok=True)
def sample(uv):
    # glTF exported TEXCOORD_0 is top-left image convention. Blender's original
    # loop UV is bottom-left; the exporter has already flipped V exactly once.
    x=np.clip(uv[:,0]*N-.5,0,N-1);y=np.clip(uv[:,1]*N-.5,0,N-1);x0=x.astype(int);y0=y.astype(int);x1=np.minimum(x0+1,N-1);y1=np.minimum(y0+1,N-1);fx=(x-x0)[:,None];fy=(y-y0)[:,None]
    return np.rint((source[y0,x0]*(1-fx)+source[y0,x1]*fx)*(1-fy)+(source[y1,x0]*(1-fx)+source[y1,x1]*fx)*fy).astype(np.uint8)
collapsed={}
triangles=[] if '--repair-only' in sys.argv else zip(d['source_uv'],d['returned_uv_in_source_order'],d['source_xyz'],d['source_owner'])
for i,(uv,r_uv,pos,owner) in enumerate(triangles):
    if i%15000==0:print('TRANSFER',i,flush=True)
    ru=r_uv[1]-r_uv[0];rv=r_uv[2]-r_uv[0]
    if abs(float(ru[0]*rv[1]-ru[1]*rv[0]))<1e-14:collapsed[owner]=collapsed.get(owner,0)+1
    p=uv*N-.5;lo=np.maximum(np.floor(p.min(0)).astype(int),0);hi=np.minimum(np.ceil(p.max(0)).astype(int),N-1)
    if np.any(hi<lo):continue
    X,Y=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));q=np.stack((X.ravel(),Y.ravel()),1);B=np.stack((p[1]-p[0],p[2]-p[0]),1)
    if abs(np.linalg.det(B))<1e-12:continue
    ab=(q-p[0])@np.linalg.inv(B).T;w=np.column_stack((1-ab.sum(1),ab));ok=(w>=-1e-7).all(1);w=w[ok];q=q[ok];xx=q[:,0];yy=q[:,1]
    out[yy,xx]=sample(w@r_uv);xyz[yy,xx]=w@pos;owners[yy,xx]=ids[str(owner)];cover[yy,xx]=True
if '--repair-only' in sys.argv:
    out=np.array(Image.open(A/'jill-basecolor-resampled-v005.png'));xyz=np.load(CACHE/'xyz.npy');owners=np.load(CACHE/'owners.npy');cover=owners>0;collapsed=json.loads((CACHE/'collapsed.json').read_text())
else:
    Image.fromarray(out).save(A/'jill-basecolor-resampled-v005.png');np.save(CACHE/'xyz.npy',xyz);np.save(CACHE/'owners.npy',owners);(CACHE/'collapsed.json').write_text(json.dumps(collapsed))
# Existing verified owner/host masks are authoritative for protected surfaces.
owner_mask=np.array(Image.open(OLD/'paint-owner-mask.png'));host=np.array(Image.open(ROOT/'docs/production/jill/mouth-profile-v004/mouth-host-fill-mask.png'))>0
def dilate(m,r=4):
    horizontal=m.copy()
    for k in range(1,r+1):horizontal[:,k:]|=m[:,:-k];horizontal[:,:-k]|=m[:,k:]
    result=horizontal.copy()
    for k in range(1,r+1):result[k:]|=horizontal[:-k];result[:-k]|=horizontal[k:]
    return result
def median(mask):
    assert mask.sum()>20
    return np.rint(np.median(out[mask],axis=0)).astype(np.uint8)
body=owners==ids['body_skin'];x=xyz[:,:,0];height=xyz[:,:,1];front=xyz[:,:,2]
green=median(body&(abs(x)<.055)&(height>.69)&(height<.72)&(front>.32))
cream=median(body&(abs(x)>.072)&(abs(x)<.10)&(height>.57)&(height<.60)&(front>.35))
canonical=np.array(Image.open(ROOT/'assets/grimo/source/jill/jill-Identity-canonical.png').convert('RGB'))
oral=canonical[380,1100];tongue=canonical[430,1100];teeth=canonical[395,1077]
fills={'lids-L':green.tolist(),'lids-R':green.tolist(),'mouth-skin':cream.tolist(),'mouth-host-skin':cream.tolist(),'mouth-inner':oral.tolist(),'tongue':tongue.tolist(),'teeth':teeth.tolist()}
report={'palette_authority':'PROVISIONAL skin samples from actual 4K Tripo BaseColor; oral/tongue/teeth are directly sampled from approved Canonical. No new Human RGB swatch approval inferred. No diagnostic palette used.','canonical_samples_xy':{'mouth-inner':[1100,380],'tongue':[1100,430],'teeth':[1077,395]},'sampled_rgb':fills,'collapsed_return_uv_triangles_by_source_owner':collapsed,'resampled_surface_pixels':int(cover.sum()),'changes':[],'human_visual_go':False}
def fill_mask(label,mask,colour):
    expanded=dilate(mask);expanded&=(owner_mask==0)|mask
    out[expanded]=colour;report['changes'].append({'mask':label,'surface_pixels':int(mask.sum()),'with_gutter':int(expanded.sum()),'colour':'local sampled gradient' if not isinstance(colour,list) else colour})
for name in ['mouth-skin','mouth-inner','tongue','teeth']:
    fill_mask(name,(owner_mask==ids[name])|(owners==ids[name]),fills[name])
fill_mask('v004-mouth-host',host,fills['mouth-host-skin'])
# Closed lids inherit the nearby green-to-cream face transition. The original
# eye owners and their full artwork remain unchanged.
closed_height=height.copy();lid=np.load(E/'lid-closed-height.npz')
for ti,hs in zip(lid['source_triangle'],lid['closed_height']):
    uv=d['source_uv'][ti];p=uv*N-.5;lo=np.maximum(np.floor(p.min(0)).astype(int),0);hi=np.minimum(np.ceil(p.max(0)).astype(int),N-1);X,Y=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));q=np.stack((X.ravel(),Y.ravel()),1);B=np.stack((p[1]-p[0],p[2]-p[0]),1)
    if abs(np.linalg.det(B))<1e-12:continue
    ab=(q-p[0])@np.linalg.inv(B).T;w=np.column_stack((1-ab.sum(1),ab));ok=(w>=-1e-7).all(1);q=q[ok];closed_height[q[:,1],q[:,0]]=w[ok]@hs
alpha=np.clip((closed_height-.635)/.055,0,1)[...,None]
skin=np.rint(cream[None,None,:]*(1-alpha)+green[None,None,:]*alpha).astype(np.uint8)
for name in ['lids-L','lids-R']:
    mask=owners==ids[name];out[mask]=skin[mask];grown=mask.copy();region=dilate(mask| (owner_mask==ids[name]));region&=(owner_mask==0)|(owner_mask==ids[name])
    for step in range(5):
        additions=np.zeros_like(mask)
        for dy,dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]:
            valid=np.roll(grown,(dy,dx),(0,1))&region&~grown&~additions
            if dy>0:valid[:dy]=False
            if dy<0:valid[dy:]=False
            if dx>0:valid[:,:dx]=False
            if dx<0:valid[:,dx:]=False
            shifted=np.roll(out,(dy,dx),(0,1));out[valid]=shifted[valid];additions|=valid
        grown|=additions
    report['changes'].append({'mask':name,'surface_pixels':int(mask.sum()),'filled_with_gutter':int(grown.sum()),'colour':'actual-face-sampled green/cream vertical blend; explicit source/raster mask union and gutter'})
# Remove fixed eyeliner only on surrounding host skin. Actual eye-owner art is
# retained; region uses the existing lid envelope expanded by <=12mm.
eye_host=body&(front>.278)&(abs(x)>.056)&(abs(x)<.180)&(height>.595)&(height<.750)
ell=((abs(x)-.114)/.068)**2+((height-.674)/.087)**2
eye_host&=ell<1
out[eye_host]=skin[eye_host];report['changes'].append({'mask':'host-eye-ring','surface_pixels':int(eye_host.sum()),'colour':'same local sampled skin field; avoids a fixed second eyeliner'})
Image.fromarray((eye_host*255).astype('uint8')).save(E/'host-eye-ring-mask.png')
mouth_upper=body&(front>.37)&(abs(x)<.071)&(height>.618)&(height<.648)
# Exclude the actual triangular nose immediately above the original mouth art.
mouth_upper&=~((abs(x)<.023)&(height>.641))
out[mouth_upper]=cream;Image.fromarray((mouth_upper*255).astype('uint8')).save(E/'host-upper-mouth-mask.png');report['changes'].append({'mask':'host-upper-mouth-mask.png','surface_pixels':int(mouth_upper.sum()),'colour':'same sampled muzzle cream; fixed upper-mouth lines only, nose excluded'})
# Horns are body-owned geometry at the two top lateral tips. The boundary is
# deliberately exported for review; no leaf, eye or wing owner can be changed.
horn=body&(height>.80)&(abs(x)>.155)&(front>-.15)&(front<.22)
horn&=(out[:,:,0].astype(float)>out[:,:,1]*.92)&(out[:,:,0]>120)&(out[:,:,2]>65)
# Preserve the returned shading value while rotating the cream base toward the
# Canonical tongue's pink hue. This is a local provisional colour repair.
pink=out[horn].astype(float);lum=np.clip(pink.mean(1)/max(float(np.mean(tongue)),1),.65,1.30);pink=np.clip(tongue[None,:]*lum[:,None],0,255).astype('uint8');out[horn]=pink
Image.fromarray((horn*255).astype('uint8')).save(E/'horn-review-mask.png');report['changes'].append({'mask':'horn-review-mask.png','surface_pixels':int(horn.sum()),'colour':'Canonical tongue pink hue, preserves horn luminance; Human boundary/colour review required'})
# Record every underside/root owner's actual coverage. Do not flatten the wing
# frame/cream membrane art using a whole-owner solid fill.
report['hidden_owner_coverage']={n:{'mask_pixels':int((owner_mask==ids[n]).sum()),'resampled_pixels':int((owners==ids[n]).sum()),'action':'retained actual returned art; real posed renders required'} for n in ids if 'root' in n or 'wing_' in n}
report['clover']='HOLD: verify rendered thighs against canonical; no invented or mirrored clover artwork.'
# Extend every covered island by four pixels; never overwrite another owner.
filled=cover.copy()
for iteration in range(4):
    additions=np.zeros_like(filled)
    for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
        valid=np.roll(filled,(dy,dx),(0,1))&~filled&~additions
        if dy>0:valid[:dy]=False
        if dy<0:valid[dy:]=False
        if dx>0:valid[:,:dx]=False
        if dx<0:valid[:,dx:]=False
        shifted=np.roll(out,(dy,dx),(0,1));out[valid]=shifted[valid];additions|=valid
    filled|=additions
Image.fromarray(out).save(A/'jill-basecolor-v005.png')
Image.fromarray(owners).save(E/'resampled-owner-mask.png')
report['output_sha256']=hashlib.sha256((A/'jill-basecolor-v005.png').read_bytes()).hexdigest()
(E/'texture-repair.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,indent=2),flush=True)
