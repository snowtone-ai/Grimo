"""Pack one local mouth island into UV space unused by retained Head faces."""
from pathlib import Path
import numpy as np,json
from PIL import Image,ImageDraw
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
s=np.load(D/'muzzle-source-uv.npz');patch=np.load(D/'muzzle-retopo.npz');source=np.load(D/'face-source.npz');tri=s['tri'];tex=Image.open(D/'Head-mouth-b-local.png').convert('RGB');pixels=np.array(tex);size=tex.width
lookup={tuple(t):i for i,t in enumerate(tri)};keep=[lookup[tuple(t)] for t in patch['retained']]
mask=Image.new('1',(size,size));draw=ImageDraw.Draw(mask)
for uv in s['uvs'][keep]:draw.polygon([(int(u*(size-1)),int((1-v)*(size-1))) for u,v in uv],fill=1)
occupied=np.asarray(mask,dtype=np.int32);integral=np.pad(occupied,((1,0),(1,0))).cumsum(0).cumsum(1);allocation=None
for box in [512,384,256,192,128]:
 sums=integral[box:,box:]-integral[:-box,box:]-integral[box:,:-box]+integral[:-box,:-box];ys,xs=np.where(sums==0)
 if len(xs):allocation=(int(xs[0]),int(ys[0]),box);break
assert allocation,'No unused local atlas region'
left,top,box=allocation;padding=8;param=patch['param'];lo=param.min(0);hi=param.max(0);local=(param-lo)/(hi-lo);uvpx=np.c_[left+padding+local[:,0]*(box-2*padding-1),top+box-padding-1-local[:,1]*(box-2*padding-1)];uv=np.c_[uvpx[:,0]/(size-1),1-uvpx[:,1]/(size-1)]
# Sample the exact retained boundary colour. The local cream field replaces old
# mouth pigment only inside the new island; all retained texels stay untouched.
outer=int(patch['outer_count']);ids=patch['boundary_ids'];colours=[]
for idx in ids[:outer]:
 hits=np.argwhere(tri==idx);samples=[]
 for fi,corner in hits:
  u,v=s['uvs'][fi,corner];samples.append(pixels[round((1-v)*(size-1)),round(u*(size-1))])
 colours.append(np.mean(samples,axis=0))
colours=np.array(colours);cream=np.median(colours[(colours[:,0]-colours[:,1]<25)&(colours.min(1)>180)],axis=0)
control=np.r_[param[:outer],param[outer:len(ids)]];values=np.r_[colours,np.tile(cream,(len(ids)-outer,1))]
unique,inv=np.unique(np.round(control,7),axis=0,return_inverse=True);values=np.column_stack([np.bincount(inv,weights=values[:,c])/np.bincount(inv) for c in range(3)]);fit=RBFInterpolator(unique,values,kernel='thin_plate_spline',smoothing=1e-8,neighbors=48)
yy,xx=np.mgrid[0:box,0:box];xz=np.c_[lo[0]+(xx.ravel()-padding)/(box-2*padding-1)*(hi[0]-lo[0]),lo[1]+(box-padding-1-yy.ravel())/(box-2*padding-1)*(hi[1]-lo[1])];rgb=np.clip(fit(xz),0,255).reshape(box,box,3)
# Lip pigment follows the physical upper/lower W boundary at every aperture.
ring=param[outer:len(ids)];points=[]
for a,b in zip(ring,np.roll(ring,-1,axis=0)):
 points.extend(a+(b-a)*np.linspace(0,1,max(3,int(np.linalg.norm(b-a)/.00015)))[:,None])
distance=cKDTree(np.array(points)).query(xz)[0].reshape(box,box);alpha=np.clip((.00125-distance)/.0005,0,1);rgb=rgb*(1-alpha[:,:,None])+np.array([106,41,47])*alpha[:,:,None]
pixels[top:top+box,left:left+box]=np.rint(rgb).astype(np.uint8);Image.fromarray(pixels).save(D/'Head-mouth-gate-retopo.png');np.savez_compressed(D/'muzzle-atlas.npz',uv=uv)
assert not occupied[top:top+box,left:left+box].any()
(D/'muzzle-texture-authoring.json').write_text(json.dumps({'allocation_pixels':allocation,'outside_allocation_pixels_exact':True,'retained_Head_faces_use_allocation':False,'cream_rgb':cream.tolist(),'method':'Existing atlas, one local island in unused retained-Head UV space; boundary colours retained, W pigment on physical ring. No painted cavity/tongue.'},indent=2)+'\n')
