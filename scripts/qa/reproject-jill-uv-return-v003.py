"""Geometry+owner matched UV reproject proof; stop on missing/ambiguous correspondence.

Synthetic return changes UV0 by reflection. This bounded proof supports same
surface/triangle correspondence only. Remesh, changed shape or ambiguous layers
must stop; do not use unconstrained nearest-surface projection on face/wing roots.
"""
from pathlib import Path
import json,itertools,math
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/rig-pretexture-technical-v003';D=E/'roundtrip'
t=np.load(D/'target-neutral.npz');s=np.load(D/'returned-uv-changed.npz');tp=t['xyz'][t['tris']];sp=s['xyz'][s['tris']]
source_uv=s['uv'];target_uv=t['uv']
def key(p,owner):return (str(owner),tuple(sorted(map(tuple,np.round(p,4)))))
lookup={}
for i,(p,owner) in enumerate(zip(sp,s['owners'])):lookup.setdefault(key(p,owner),[]).append(i)
matched=[];bad=[];maxdelta=0
permutations=list(itertools.permutations(range(3)));source_points=sp.tolist()
for i,(p,owner) in enumerate(zip(tp,t['owners'])):
    choices=[]
    points=p.tolist()
    for j in lookup.get(key(p,owner),[]):
        source=source_points[j]
        dd=[[sum((a-b)**2 for a,b in zip(v,w)) for w in source] for v in points]
        order=min(permutations,key=lambda order:max(dd[k][order[k]] for k in range(3)))
        delta=math.sqrt(max(dd[k][order[k]] for k in range(3)))
        if delta<2e-6:choices.append((delta,source_uv[j,list(order)]))
    if not choices:bad.append(i);continue
    choices.sort(key=lambda x:x[0]);q=choices[0][1]
    if any(np.max(abs(q-x[1]))>2e-6 for x in choices[1:]):bad.append(i);continue
    maxdelta=max(maxdelta,choices[0][0]);matched.append((i,q))
    if i%10000==0:print('MATCHED',i,flush=True)
assert not bad,f'Correspondence HOLD: {len(bad)} missing/ambiguous triangles'
src=np.asarray(Image.open(E/'diagnostic-uv-changed.png').convert('RGB'));expected=np.asarray(Image.open(E/'diagnostic-uv0.png').convert('RGB'));size=len(src)
out=np.zeros_like(src);written=np.zeros((size,size),dtype=bool);skip=[]
for i,source_uv in matched:
    q=target_uv[i];p=q*np.array([size-1,-(size-1)])+np.array([0,size-1]);lo=np.maximum(np.floor(p.min(0)).astype(int),0);hi=np.minimum(np.ceil(p.max(0)).astype(int),size-1)
    M=np.stack([p[1]-p[0],p[2]-p[0]],axis=1)
    if abs(np.linalg.det(M))<1e-8:skip.append(i);continue
    yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];sample=np.stack([xx-p[0,0],yy-p[0,1]],axis=-1)@np.linalg.inv(M).T
    inside=(sample[...,0]>=-1e-6)&(sample[...,1]>=-1e-6)&(sample.sum(-1)<=1+1e-6)
    weights=np.c_[1-sample[inside].sum(-1),sample[inside]];suv=weights@source_uv
    sx=np.clip(np.rint(suv[:,0]*(size-1)).astype(int),0,size-1);sy=np.clip(np.rint((1-suv[:,1])*(size-1)).astype(int),0,size-1)
    out[yy[inside],xx[inside]]=src[sy,sx];written[yy[inside],xx[inside]]=True
err=abs(out[written].astype(int)-expected[written].astype(int));maxerr=int(err.max());meanerr=float(err.mean())
dist,index=distance_transform_edt(~written,return_indices=True);fill=(~written)&(dist<=4);out[fill]=out[index[0][fill],index[1][fill]]
Image.fromarray(out).save(D/'rebaked-uv0.png')
report={'pass':not bad and not skip and maxerr<=2,'synthetic_uv_change':'U reflected; saved GLB fresh import; image also reflected',
    'triangles_matched':len(matched),'unmatched_or_ambiguous':bad,'skipped_uv_degenerate':skip,'position_max_m':maxdelta,
    'raster_written_pixels':int(written.sum()),'pixel_max_error_255':maxerr,'pixel_mean_error_255':meanerr,
    'method':'Part-owner plus triangle geometry correspondence; barycentric source UV raster to target UV0. No ray projection between adjacent surfaces. Nearest sampling on synthetic fixture.',
    'limits':'Synthetic UV-only change with corresponding geometry and triangle topology. Tripo real return UNKNOWN. Different triangulation/remesh/deformation, missing image/UV/owner or ambiguous match STOP/HOLD. Normal/tangent rebake NOT proved.'}
(E/'uv-changed-transfer-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['pass']
