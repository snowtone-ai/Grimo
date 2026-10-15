"""Local annular mouth retopology, retaining the exact W/outer constraints."""
from pathlib import Path
from collections import defaultdict
import numpy as np,triangle,json
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import spsolve
from scipy.interpolate import RBFInterpolator
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
s=np.load(D/'face-source.npz');o=np.load(R/'docs/production/shushu/evidence/production-rig-v004-mouth-b/head-edit-mask.npz');p=o['original'];tri=s['tri'];u,ix=np.unique(p.round(6),axis=0,return_inverse=True)
c=p[tri].mean(1);remove=((c[:,0]/.09)**2+((c[:,2]-.602)/.072)**2<1)&(c[:,1]<-.20)
e=np.sort(ix[np.concatenate([tri[~remove][:,[0,1]],tri[~remove][:,[1,2]],tri[~remove][:,[2,0]]])],axis=1);e,n=np.unique(e,axis=0,return_counts=True);e=e[(n==1)&(e[:,0]!=e[:,1])];adj=defaultdict(list)
for a,b in e:adj[a].append(b);adj[b].append(a)
seen=set();loops=[]
for a in adj:
 if a in seen:continue
 loop=[a];prev=None
 while True:
  nxt=next(x for x in adj[loop[-1]] if x!=prev)
  if nxt==a:break
  prev=loop[-1];loop.append(nxt)
 seen.update(loop);loops.append(loop)
outer=min(loops,key=lambda x:abs(u[x,0].mean()));outer=np.array([np.flatnonzero(ix==v)[0] for v in outer]);inner=o['ring_indices'];ids=np.r_[outer,inner];n0=len(outer);nb=len(ids)
param=s['MouthOpen'][ids][:,[0,2]]
segments=np.r_[np.c_[np.arange(n0),np.roll(np.arange(n0),-1)],np.c_[np.arange(n0,nb),np.roll(np.arange(n0,nb),-1)]]
result=triangle.triangulate({'vertices':param,'segments':segments,'holes':[s['MouthOpen'][inner][:,[0,2]].mean(0)]},'pYqa0.000005')
v=result['vertices'];t=result['triangles'];edges=np.unique(np.sort(np.r_[t[:,[0,1]],t[:,[1,2]],t[:,[2,0]]],axis=1),axis=0)
row=np.r_[edges[:,0],edges[:,1]];col=np.r_[edges[:,1],edges[:,0]];w=1/np.maximum(1e-6,np.linalg.norm(v[row]-v[col],axis=1));A=coo_matrix((w,(row,col)),shape=(len(v),len(v))).tocsr();L=diags(np.array(A.sum(1)).ravel())-A
free=np.arange(nb,len(v));bound=np.arange(nb)
near_inner=set(range(n0,nb))
for _ in range(2):
 previous=set(near_inner);near_inner.update(int(b) for a,b in zip(row,col) if int(a) in previous)
near_outer=set(range(n0))
for _ in range(3):
 previous=set(near_outer);near_outer.update(int(b) for a,b in zip(row,col) if int(a) in previous)
outer_band=np.array(sorted(near_outer-set(range(nb))))
fixed=np.array(sorted(set(range(nb))|near_inner|near_outer));smoothfree=np.setdiff1d(np.arange(len(v)),fixed);B=(L.T@L).tocsc()
pp=p[(p[:,1]<-.20)&(abs(p[:,0])<.15)&(p[:,2]>.48)&(p[:,2]<.70)][::16]
unique,inv=np.unique(pp[:,[0,2]].round(7),axis=0,return_inverse=True)
fit=RBFInterpolator(unique,np.bincount(inv,weights=pp[:,1])/np.bincount(inv),kernel='thin_plate_spline',smoothing=1e-9,neighbors=64)
def surface(key):
 q=np.zeros((len(v),3));q[:nb]=s[key][ids];q[free]=spsolve(L[free][:,free],-L[free][:,bound]@q[bound])
 if key=='MouthOpen':q[:,0]=v[:,0];q[:,2]=v[:,1]
 # The analytic lip surface supplies a continuous tangent across the W rim.
 # Extend only the outer cheek depth correction with a smooth biharmonic field.
 x,z=q[:,0],q[:,2];baseline=-.268+3.1*x*x+.34*(.616-z)+3.2*(.616-z)**2
 if key=='MouthOpen':baseline+=np.where(z<.612,.003*np.maximum(0,1-(x/.043)**2),0)
 correction=np.zeros(len(v));correction[:nb]=q[:nb,1]-baseline[:nb]
 correction[outer_band]=fit(q[outer_band][:,[0,2]])-baseline[outer_band]
 correction[smoothfree]=spsolve(B[smoothfree][:,smoothfree],-B[smoothfree][:,fixed]@correction[fixed])
 q[:,1]=baseline+correction;q[:nb]=s[key][ids]
 return q
closed=surface('Basis');opened=surface('MouthOpen')
np.savez_compressed(D/'muzzle-retopo.npz',retained=tri[~remove],boundary_ids=ids,outer_count=n0,patch_tri=t,param=v,closed=closed,opened=opened)
(D/'muzzle-retopo-plan.json').write_text(json.dumps({'removed_triangles':int(remove.sum()),'patch_vertices':len(v),'patch_triangles':len(t),'outer_constraints':n0,'exact_W_constraints':len(inner),'outer_tangent_band_vertices':len(outer_band),'method':'Local annulus with exact outer/W boundaries. Open XZ is constrained triangulation; closed XZ harmonic. Analytic lip depth plus biharmonic outer correction; three outer adjacency layers match source depth fit and two inner layers retain lip tangent. Crown correction is separate. No skeleton or other mesh changes.'},indent=2)+'\n')
