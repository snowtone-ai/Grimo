"""Geometric feasibility search for short-arm support, not aesthetic approval."""
import bpy,sys,importlib.util,json,itertools,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004';sp=importlib.util.spec_from_file_location('repair',R/'scripts/blender/repair-shushu-abc-v004.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
bpy.ops.wm.open_mainfile(filepath=str(m.ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');m.b.state(rig,{'Seat':float(sys.argv[-1]) if sys.argv[-1] in ['0','1'] else 0});targets=[]
for name in ['Head','Torso']:
 p,t=m.b.evaluated(bpy.data.objects['ShushuStatic_'+name]);targets.append((name,BVHTree.FromPolygons(p.tolist(),t.tolist(),all_triangles=True),p,t))

def segment(a,b,t):
 d=b-a;e=t[1]-t[0];f=t[2]-t[0];h=np.cross(d,f);det=float(e@h)
 if abs(det)<1e-12:return False
 v=a-t[0];u=float(v@h)/det;k=np.cross(v,e);w=float(d@k)/det;s=float(f@k)/det;return u>=-1e-7 and w>=-1e-7 and u+w<=1+1e-7 and 1e-7<s<1-1e-7
def crossing(a,b):return any(segment(x[i],x[(i+1)%3],y) for x,y in [(a,b),(b,a)] for i in range(3))
vol=lambda q:abs(float(np.einsum('ij,ij->i',q[tri[:,0]],np.cross(q[tri[:,1]],q[tri[:,2]])).sum()/6))

rows=[]
for side in ['L','R']:
 o=bpy.data.objects['ShushuStatic_Paw_'+side];p=np.array([v.co[:] for v in o.data.vertices]);o.data.calc_loop_triangles();tri=np.array([t.vertices[:] for t in o.data.loop_triangles]);root=np.array(rig.data.bones['mixamorig:'+('Left' if side=='L' else 'Right')+'Shoulder'].head_local);hand=np.array(rig.data.bones['mixamorig:'+('Left' if side=='L' else 'Right')+'Hand'].head_local);axis=(hand-root)/np.linalg.norm(hand-root);faces=set(np.where((abs(p[tri][:,:,0])>.26).all(1))[0]);tips=np.where(((p-root)@axis)>np.quantile((p-root)@axis,.75))[0];skin=m.b.skin_matrices(rig,o)
 for mode,x,z,ex,ez in [('SelfContact',.45,-.35,ex,ez) for ex,ez in itertools.product([.35,.45],[.9,1.,1.1,1.2])]+[('Hold',x,-.65,ex,.4) for x,ex in itertools.product([.45,.55,.65],[.05,.15])]:
  spec={'start':(x,-.98,z),'end':(ex,-.75,ez),'begin':.05,'end_at':.7};q,_=m.curve_surface(p,p,root,axis,0,mode,1,spec);q=np.einsum('nij,nj->ni',skin[:,:3,:3],q)+skin[:,:3,3];tree=BVHTree.FromPolygons(q.tolist(),tri.tolist(),all_triangles=True);crosses={};gap={}
  for name,target,tp,tt in targets:
   crosses[name]=sum(crossing(q[tri[a]],tp[tt[b]]) for a,b in tree.overlap(target) if name=='Head' or a in faces);gap[name]=min(float(target.find_nearest(Vector(q[i]))[3]) for i in tips)
  rows.append({'side':side,'mode':mode,'spec':spec,'crosses':crosses,'tip_gap':gap})
for side,mode in itertools.product(['L','R'],['SelfContact','Hold']):
 safe=[r for r in rows if r['side']==side and r['mode']==mode and not any(r['crosses'].values())];safe.sort(key=lambda r:r['tip_gap']['Head'] if mode=='SelfContact' else r['spec']['start'][0]+r['spec']['end'][0]);print('CONTACT_SAFE',side,mode,json.dumps(safe[:3]),flush=True)
(D/('contact-feasibility-seat'+str(rig['Seat'])+'.json')).write_text(json.dumps(rows,indent=2))
