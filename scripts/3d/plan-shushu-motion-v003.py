"""Bounded geometry repair proposal. Never modifies approved inputs."""
from pathlib import Path
import json, numpy as np
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003'
s=np.load(D/'diagnostic-source.npz');p=s['ShushuStatic_Head__Basis'];x,y,z=p.T
smooth=lambda a,b,t: (lambda u:u*u*u*(10+u*(-15+6*u)))(np.clip((t-a)/(b-a),0,1))
# Reconstruct local depth from the exact approved W and three exterior rings.
# The initial analytic blend left a visible depression at its transition.
# Thin-plate fitting preserves the exterior trend without fitting that defect.
def depth(q,opened=False):
 x,y,z=q.T;uv=np.c_[x/.119,(z-.596)/.089];r=np.linalg.norm(uv,axis=1)
 # Exact W vertices are independently identified from the original retopo.
 patch=np.load(R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/muzzle-retopo.npz')
 nold=34667; outer=int(patch['outer_count']);nb=len(patch['boundary_ids']);rim=np.arange(nold+outer,nold+nb)
 live=np.unique(s['ShushuStatic_Head__tri']);valid=live[(y[live]<-.185)&(r[live]>.8)&(r[live]<1.22)]
 tree=cKDTree(uv[valid]);a=np.linspace(0,2*np.pi,100,endpoint=False)
 ring=np.unique(valid[tree.query(np.concatenate([np.c_[rr*np.cos(a),rr*np.sin(a)] for rr in [.85,1,1.15]]))[1]])
 # Constrain the upper accepted surface in the interpolant itself. A separate
 # height fade produced a visible slope discontinuity beside the W on phone.
 protected=live[(z[live]>.637)&(z[live]<.680)&(abs(x[live])<.14)&(y[live]<-.185)]
 samples=np.array([[xx,zz] for xx in np.linspace(-.13,.13,27) for zz in [.639,.65,.665,.678]])
 upper=protected[cKDTree(uv[protected]).query(samples/np.array([.119,.089])-np.array([0,.596/.089]))[1]]
 ids=np.unique(np.r_[rim,ring,upper]);coords,ix=np.unique(np.round(uv[ids],7),axis=0,return_index=True);ids=ids[ix]
 baseline=RBFInterpolator(coords,y[ids],kernel='thin_plate_spline',smoothing=1e-9)(uv)
 # Protect the accepted upper muzzle/nose region; the unconstrained fit made
 # a new horizontal shadow there under the phone's harder runtime lighting.
 amount=(1-smooth(.82,1.15,r))*(1-smooth(.650,.680,z))*(1-smooth(-.205,-.185,y))
 delta=np.clip((baseline-y)*amount,-.018,.018)
 delta[rim]=0
 return delta,amount
delta,amount=depth(p);op=s['ShushuStatic_Head__MouthOpen'];od,_=depth(op,True)
# Crown ray hit (190,51) identifies the remaining HEAD triangle 20283, not an
# ear. Fit beyond both the old 38-vertex edit and this back edge, with robust
# exterior samples and a C2 feather, applying the SAME Z delta to every key.
r=((x+.087)/.054)**2+((y-.037)/.095)**2
sel=(r>1)&(r<3.8)&(z>.875)
def design(x,y):return np.c_[np.ones(len(x)),x,y,x*x,x*y,y*y]
A=design(x[sel],y[sel]);v=z[sel];weights=np.ones(len(v))
for _ in range(5):
 c=np.linalg.lstsq(A*weights[:,None],v*weights,rcond=None)[0];res=v-A@c;scale=max(.0005,np.median(abs(res))*1.4826);weights=np.minimum(1,1.5*scale/np.maximum(abs(res),1e-12))
target=design(x,y)@c;cd=np.clip((target-z)*(1-smooth(.35,1,np.sqrt(r)))*(z>.89),-.015,.015)
np.savez_compressed(D/'local-repair.npz',muzzle_delta=delta,muzzle_open_delta=od,crown_delta=cd)
rows={'method':'Thin-plate local depth from retained W and exterior rings, C2 outer blend; signed robust crown quadratic fairing. No topology, X/Z muzzle, UV, texture, weights or rig changes.','muzzle_vertices':int((abs(delta)>1e-8).sum()),'muzzle_max_depth_delta':float(abs(delta).max()),'open_max_depth_delta':float(abs(od).max()),'muzzle_bounds':[p[abs(delta)>1e-8].min(0).tolist(),p[abs(delta)>1e-8].max(0).tolist()],'crown_vertices':int((abs(cd)>1e-8).sum()),'crown_max_z_delta':float(abs(cd).max()),'crown_fit_rms':float(np.sqrt(np.mean((A@c-v)**2))),'W_exact':True,'human':'PENDING','gate':'HOLD'}
(D/'local-repair-plan.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
