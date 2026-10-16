"""Geometric seam audit of the reconstruction plan at glTF float tolerance."""
from pathlib import Path
from collections import Counter
import numpy as np,json,hashlib
D=Path(__file__).resolve().parents[2]/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003'
r=np.load(D/'crown-retopo.npz');v,ix=np.unique(np.round(r['points'],6),axis=0,return_inverse=True);tri=ix[r['faces']];tri=tri[np.array([len(set(t))==3 for t in tri])]
edges=Counter(tuple(sorted(e)) for t in tri for e in [(t[0],t[1]),(t[1],t[2]),(t[2],t[0])]);local=lambda a,b:min(v[a,2],v[b,2])>.85 and np.linalg.norm(((v[a,:2]+v[b,:2])/2-[-.087,.037])/[.065,.11])<1.15
boundary=[e for e,n in edges.items() if n==1 and local(*e)];nonmanifold=[e for e,n in edges.items() if n>2 and local(*e)]
report={'plan_sha256':hashlib.sha256((D/'crown-retopo.npz').read_bytes()).hexdigest(),'geometric_weld_tolerance_H':1e-6,'local_open_boundary_edges':len(boundary),'local_nonmanifold_edges':len(nonmanifold),'scope':'Cut and exterior seam through 1.15 ellipse radius, upper head only. Original seam-split IDs are compared geometrically; this is not a collision or visual gate.'}
(D/'crown-topology-audit.json').write_text(json.dumps(report,indent=2));assert not boundary and not nonmanifold,report;print(report)
