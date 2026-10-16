"""Surface/volume probes on actual evaluated pose witnesses, not a visual GO."""
from pathlib import Path
import numpy as np,json,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(__file__).resolve().parents[2]/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';s=np.load(D/'diagnostic-source.npz');r=np.load(D/'saved-reference.npz');c=np.load(D/'crown-retopo.npz');rows=[]
frames=sorted({int(k.rsplit('__',1)[1]) for k in r.files});headtri=c['faces'];assert len(r['ShushuStatic_Head__1'])==len(c['points']),'Stale pose reference'
def segment_triangle(origin,end,tri):
 direction=end-origin;e1=tri[1]-tri[0];e2=tri[2]-tri[0];h=np.cross(direction,e2);det=float(e1@h)
 if abs(det)<1e-12:return False
 delta=origin-tri[0];u=float(delta@h)/det;q=np.cross(delta,e1);v=float(direction@q)/det;t=float(e2@q)/det
 return u>=-1e-7 and v>=-1e-7 and u+v<=1+1e-7 and 1e-7<t<1-1e-7
def crossing(a,b):
 return any(segment_triangle(x[i],x[(i+1)%3],y) for x,y in [(a,b),(b,a)] for i in range(3))
for f in frames:
 targets=[]
 for name,tri in [('ShushuStatic_Torso',s['ShushuStatic_Torso__tri']),('ShushuStatic_Head',headtri)]:
  p=r[name+'__'+str(f)];targets.append((name,BVHTree.FromPolygons(p.tolist(),tri.tolist(),all_triangles=True),p,tri))
 for name in ['ShushuStatic_Paw_L','ShushuStatic_Paw_R']:
  p=r[name+'__'+str(f)].astype(float);basis=s[name+'__Basis'];tri=s[name+'__tri'];a,b,c0=p[tri].transpose(1,0,2);A,B,C=basis[tri].transpose(1,0,2);area=np.linalg.norm(np.cross(b-a,c0-a),axis=1);basearea=np.linalg.norm(np.cross(B-A,C-A),axis=1);live=basearea>1e-9;ratio=area[live]/basearea[live]
  volume=lambda x:abs(float(np.einsum('ij,ij->i',x[tri[:,0]],np.cross(x[tri[:,1]],x[tri[:,2]])).sum()/6))
  # Anatomical rest reach is along X, not Z (the original arms are splayed).
  # Same distal threshold as the original grip calibration excludes the roots.
  distal=np.where(abs(basis[:,0])>.26)[0];penetration=[]
  pawtree=BVHTree.FromPolygons(p.tolist(),tri.tolist(),all_triangles=True)
  for target,tree,target_points,target_tri in targets:
   depth=[];negative_examples=[]
   for i in distal:
    point=Vector(p[i]);co,n,index,distance=tree.find_nearest(point)
    if co is not None and (point-co).dot(n)<-1e-7:
     depth.append(float(distance))
     if len(negative_examples)<6:negative_examples.append({'vertex':int(i),'point':p[i].tolist(),'nearest':list(co),'normal':list(n),'outside_target_AABB':bool(((p[i]<target_points.min(0)-1e-7)|(p[i]>target_points.max(0)+1e-7)).any())})
   pairs=pawtree.overlap(tree);distal_faces=set(np.where((abs(basis[tri][:,:,0])>.26).all(1))[0]);intersections=[]
   for pawface,targetface in pairs:
    if pawface in distal_faces and crossing(p[tri[pawface]],target_points[target_tri[targetface]]):intersections.append([int(pawface),int(targetface)])
   penetration.append({'target':target,'negative_side_vertices':len(depth),'max_depth_H':max(depth,default=0),'nearest_negative_examples':negative_examples,'distal_triangle_crossings':intersections,'bvh_candidate_pairs':len(pairs)})
  rows.append({'frame':f,'mesh':name,'finite':bool(np.isfinite(p).all()),'area_ratio_p01':float(np.quantile(ratio,.01)),'area_ratio_p99':float(np.quantile(ratio,.99)),'oriented_volume_ratio_proxy':volume(p)/volume(basis),'distal_nearest_signed_probes':penetration})
report={'reference_sha256':hashlib.sha256((D/'saved-reference.npz').read_bytes()).hexdigest(),'rows':rows,'scope':'Actual evaluated vertices for saved-roundtrip witnesses. Nearest-triangle signed distances can misclassify external points below the chin against an internal rim; retain raw values and witnesses. Distal triangle segment-crossing test after BVH broad phase excludes intentional shoulder attachment. Complement with 264-state ray parity and tip-gap audit. Volume is an oriented closed-surface proxy, not Human approval or all-space collision certification.'};(D/'contact-surface-audit.json').write_text(json.dumps(report,indent=2));assert all(x['finite'] for x in rows);assert all(not t['distal_triangle_crossings'] for x in rows for t in x['distal_nearest_signed_probes']);print('CONTACT_PROBES',len(rows),'signed_max',max(t['max_depth_H'] for x in rows for t in x['distal_nearest_signed_probes']),'triangle_crossings',sum(len(t['distal_triangle_crossings']) for x in rows for t in x['distal_nearest_signed_probes']))
