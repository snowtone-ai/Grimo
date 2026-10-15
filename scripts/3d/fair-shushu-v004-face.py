"""Bounded local surface fairing; W contact ring and eye/nose domains pinned.

Produces an explicit coordinate patch for every existing key. Blender applies it
to a separate candidate; topology/UV/weights are retained for this iteration.
"""
from pathlib import Path
import json,numpy as np
from scipy.sparse import coo_matrix,diags,eye
from scipy.sparse.linalg import factorized
from scipy.interpolate import RBFInterpolator
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
s=np.load(OUT/'face-source.npz');p=s['Basis'];tri=s['tri']
old=np.load(ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b/head-edit-mask.npz')
original=old['original'];u,ix=np.unique(original.round(6),axis=0,return_inverse=True)
count=np.bincount(ix);base=np.column_stack([np.bincount(ix,weights=original[:,c])/count for c in range(3)])
edge=np.unique(np.sort(ix[np.concatenate([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]])],axis=1),axis=0);edge=edge[edge[:,0]!=edge[:,1]]
rows=np.r_[edge[:,0],edge[:,1]];cols=np.r_[edge[:,1],edge[:,0]]
adj=coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(u),len(u))).tocsr();avg=diags(1/np.maximum(1,np.array(adj.sum(1)).ravel()))@adj
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
x,y,z=base.T
# Biharmonic displacement extends the same rim target smoothly into the original
# cheek, instead of squeezing the upper transition into the old narrow band.
domain=(abs(x)<.10)&(y<-.20)&(z>.505)&(z<.674)
domain[(abs(x)<.024)&(z>.630)]=False
ring=np.unique(ix[old['ring_indices']]);free=np.flatnonzero(domain&~np.isin(np.arange(len(u)),ring));fixed=np.setdiff1d(np.arange(len(u)),free)
lap=(eye(len(u),format='csr')-avg).tocsc();solve=factorized(lap[free][:,free]);couple=lap[free][:,fixed]
def displacement(target):
 mapped=base.copy()
 for i in old['ring_indices']:mapped[ix[i]]=target[i]
 mapped[free]=solve(-(couple@mapped[fixed]))
 return (mapped-base)[ix]
def smooth_surface(source):
 # Fit a smooth depth surface through the exact W ring and unchanged cheek
 # samples. This removes inherited mouth-side folds without flattening texture.
 mapped=original+displacement(source);mapped[old['ring_indices']]=source[old['ring_indices']]
 xyz=original;xx,yy,zz=xyz.T
 surround=(abs(xx)<.15)&(yy<-.20)&(zz>.48)&(zz<.70)&((abs(xx)>.082)|(zz<.525)|(zz>.652))
 ids=np.flatnonzero(surround)[::8]
 control=np.r_[source[old['ring_indices']],xyz[ids]]
 xz=np.round(control[:,[0,2]],7);unique,inv=np.unique(xz,axis=0,return_inverse=True)
 values=np.bincount(inv,weights=control[:,1])/np.bincount(inv)
 fit=RBFInterpolator(unique,values,kernel='thin_plate_spline',smoothing=1e-10,neighbors=min(128,len(unique)))
 out=mapped.copy();x,y,z=out.T
 fade=(1-smooth(.066,.105,abs(x)))*smooth(.20,.24,-y)*smooth(.505,.54,z)*(1-smooth(.638,.670,z))
 active=np.flatnonzero(fade>0)
 out[active,1]+=fade[active]*(fit(out[active][:,[0,2]])-out[active,1])
 out[old['ring_indices']]=source[old['ring_indices']]
 return out
closed=smooth_surface(old['closed']);opened=smooth_surface(old['opened'])
data={};stats=[]
for name in s.files:
 if name=='tri':continue
 q=s[name];d=(opened-old['opened']) if name=='MouthOpen' else (closed-old['closed']);d[old['ring_indices']]=0
 out=q+d;data[name]=out.astype(np.float32);stats.append({'key':name,'max_displacement':float(np.linalg.norm(d,axis=1).max()),'changed_vertices':int((np.linalg.norm(d,axis=1)>1e-8).sum()),'rim_exact':bool(np.array_equal(out[old['ring_indices']],q[old['ring_indices']]))})
np.savez_compressed(OUT/'face-fair-patch.npz',**data)
(OUT/'face-fair-authoring.json').write_text(json.dumps({'method':'Local thin-plate depth surface constrained by exact W ring and unchanged cheek; X/Z exact; all existing keys/UV/topology/weights','region':{'abs_x_max':.105,'z':[.505,.670],'front_y':-.20},'rows':stats},indent=2)+'\n')
