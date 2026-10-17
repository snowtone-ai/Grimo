"""Geometric feasibility search for short-arm support, not aesthetic approval."""
import bpy,sys,importlib.util,json,itertools,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004';sp=importlib.util.spec_from_file_location('repair',R/'scripts/blender/repair-shushu-abc-v004.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
bpy.ops.wm.open_mainfile(filepath=str(m.ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');m.b.reset(rig);targets=[]
for name in ['Head','Torso']:
 p,t=m.b.evaluated(bpy.data.objects['ShushuStatic_'+name]);targets.append((name,BVHTree.FromPolygons(p.tolist(),t.tolist(),all_triangles=True),p,t))
o=bpy.data.objects['ShushuStatic_Paw_L'];p=np.array([v.co[:] for v in o.data.vertices]);o.data.calc_loop_triangles();tri=np.array([t.vertices[:] for t in o.data.loop_triangles]);root=np.array(rig.data.bones['mixamorig:LeftShoulder'].head_local);hand=np.array(rig.data.bones['mixamorig:LeftHand'].head_local);axis=(hand-root)/np.linalg.norm(hand-root);distal=np.where(abs(p[:,0])>.26)[0];faces=set(np.where((abs(p[tri][:,:,0])>.26).all(1))[0]);tips=np.where(((p-root)@axis)>np.quantile((p-root)@axis,.75))[0]
def segment(a,b,t):
 d=b-a;e=t[1]-t[0];f=t[2]-t[0];h=np.cross(d,f);det=float(e@h)
 if abs(det)<1e-12:return False
 v=a-t[0];u=float(v@h)/det;k=np.cross(v,e);w=float(d@k)/det;s=float(f@k)/det;return u>=-1e-7 and w>=-1e-7 and u+w<=1+1e-7 and 1e-7<s<1-1e-7
def crossing(a,b):return any(segment(x[i],x[(i+1)%3],y) for x,y in [(a,b),(b,a)] for i in range(3))
vol=lambda q:abs(float(np.einsum('ij,ij->i',q[tri[:,0]],np.cross(q[tri[:,1]],q[tri[:,2]])).sum()/6))
rows=[]
for x,z,bend in itertools.product([.12,.3,.5,.65],[-.42,-.3,-.18,-.04,.12],[.2,.35,.5,.65,.8]):
 spec={'goal':(x,-.98,z),'bend':bend};q,_=m.curve_surface(p,p,root,axis,0,'Hold',1,spec);tree=BVHTree.FromPolygons(q.tolist(),tri.tolist(),all_triangles=True);crosses={};gap={}
 for name,target,tp,tt in targets:
  crosses[name]=sum(crossing(q[tri[a]],tp[tt[b]]) for a,b in tree.overlap(target) if a in faces);gap[name]=min(float(target.find_nearest(Vector(q[i]))[3]) for i in tips)
 rows.append({'spec':spec,'crosses':crosses,'tip_gap':gap,'volume_proxy':vol(q)/vol(p),'tip_center':q[tips].mean(0).tolist()})
safe=[r for r in rows if not any(r['crosses'].values()) and .95<r['volume_proxy']<1.1]
for mode,target in [('Hold',np.array([.19,-.25,.40])),('SelfContact',np.array([.17,-.25,.49])),('Offer',np.array([.33,-.17,.34]))]:
 def score(r):return float(np.linalg.norm(np.array(r['tip_center'])-target))+(r['tip_gap']['Head']*3 if mode=='SelfContact' else 0)
 best=sorted(safe,key=score)[:5];print('FEASIBLE',mode,json.dumps(best),flush=True)
(D/'shoulder-feasibility.json').write_text(json.dumps({'scope':'Neutral body, L, full reach, W0; actual distal triangle crossings. Final bilateral/intermediate/seat checks still required.','safe_count':len(safe),'rows':rows},indent=2))
