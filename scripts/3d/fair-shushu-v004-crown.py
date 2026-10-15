"""Remove the ray-identified crown spike with a bounded local Z correction."""
from pathlib import Path
import numpy as np,json
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
p=np.load(D/'face-source.npz')['Basis'];x,y,z=p.T;r=((x+.092)/.025)**2+((y-.015)/.055)**2
sel=(abs(x+.092)<.065)&(abs(y-.015)<.10)&(z>.905)&(r>1)
def design(x,y):return np.c_[np.ones(len(x)),x,y,x*x,x*y,y*y]
c=np.linalg.lstsq(design(x[sel],y[sel]),z[sel],rcond=None)[0];target=design(x,y)@c;mask=(r<1)&(z>.92)
d=np.zeros_like(p);d[:,2]=np.where(mask,np.clip(np.minimum(0,target-z)*np.clip((1-r)*3,0,1),-.015,0),0)
np.savez_compressed(D/'crown-local-delta.npz',delta=d)
(D/'crown-local-authoring.json').write_text(json.dumps({'changed_vertices':int((np.linalg.norm(d,axis=1)>1e-8).sum()),'max_delta':float(np.linalg.norm(d,axis=1).max()),'source_bounds':[p[mask].min(0).tolist(),p[mask].max(0).tolist()],'method':'Crown ray-identified Head spike; bounded Z cap against local quadratic surface; same delta in every key. No eye/ear/nose/rest bone edit.'},indent=2)+'\n')
