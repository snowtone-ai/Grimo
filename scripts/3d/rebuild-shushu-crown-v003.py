"""Replace the ray-attributed folded crown sheet by one local height-field disk.
Convex clipping retains the exact exterior and barycentric attribute mapping.
Fail closed if the cut boundary still has overlapping source layers.
"""
from pathlib import Path
import numpy as np,json,triangle,hashlib
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree
from collections import Counter
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';s=np.load(D/'diagnostic-source.npz');p=s['ShushuStatic_Head__Basis'].astype(float);tri=s['ShushuStatic_Head__tri'];repair=np.load(D/'local-repair.npz');candidate=p.copy();candidate[:,2]+=repair['crown_delta'];center=np.array([-.087,.037]);radius=np.array([.065,.11]);a=np.linspace(0,2*np.pi,64,endpoint=False);boundary=center+radius*np.c_[np.cos(a),np.sin(a)];cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
cp=p[tri].mean(1);eligible=cp[:,2]>.85;tt=tri[eligible];sourceids=np.where(eligible)[0];xy=p[tt,:2];matrix=np.stack([xy[:,1]-xy[:,0],xy[:,2]-xy[:,0]],axis=2);det=np.linalg.det(matrix);up=det>1e-12;xy=xy[up];tt=tt[up];sourceids=sourceids[up];inv=np.linalg.inv(matrix[up]);lo=xy.min(1)-1e-9;hi=xy.max(1)+1e-9
def reference(q):
 ids=np.where(((q>=lo)&(q<=hi)).all(1))[0];v=np.einsum('nij,nj->ni',inv[ids],q-xy[ids,0]);b=np.c_[1-v.sum(1),v];ok=(b.min(1)>-1e-7);ids=ids[ok];b=b[ok]
 if not len(ids):raise ValueError('No outward crown source at '+str(q))
 heights=np.einsum('ni,ni->n',b,p[tt[ids],2]);j=np.argmin(heights);return int(sourceids[ids[j]]),b[j]
def clip(poly,q0,q1,inside):
 result=[]
 for k,A in enumerate(poly):
  B=poly[(k+1)%len(poly)];da=cross(q1-q0,A[:2]-q0);db=cross(q1-q0,B[:2]-q0);ia=da>=-1e-12 if inside else da<=1e-12;ib=db>=-1e-12 if inside else db<=1e-12
  if ia:result.append(A)
  if ia!=ib:
   f=da/(da-db);result.append(A+(B-A)*f)
 return result
points=list(candidate);mapping=[None]*len(p);lookup={};faces=[];uvref=[];uvbary=[];cut_xy=[];cut_z={};removed=[];untouched=[]
def vertex(q,source):
 bary=q[2:];one=np.where(bary>1-1e-10)[0]
 if len(one):return int(tri[source,one[0]])
 position=bary@candidate[tri[source]];key=tuple(np.round(position,9))
 if key not in lookup:lookup[key]=len(points);points.append(position);mapping.append((source,bary.copy()))
 # Convex polygon boundary points have one zero signed edge distance.
 distances=[cross(boundary[(i+1)%64]-boundary[i],q[:2]-boundary[i]) for i in range(64)]
 if min(distances)>-1e-10 and min(abs(v) for v in distances)<1e-10:
  keyxy=tuple(np.round(q[:2],9));cut_z.setdefault(keyxy,[]).append(float(position[2]));cut_xy.append(q[:2])
 return lookup[key]
for i,t in enumerate(tri):
 xytri=p[t,:2];unit=(xytri-center)/radius
 if not eligible[i] or np.any(xytri.max(0)<boundary.min(0)) or np.any(xytri.min(0)>boundary.max(0)):
  faces.append(t.tolist());uvref.append([i]*3);uvbary.append(np.eye(3));untouched.append(i);continue
 poly=[np.r_[xytri[k],np.eye(3)[k]] for k in range(3)];outside=[]
 for j in range(64):
  if not poly:break
  q0,q1=boundary[j],boundary[(j+1)%64];part=clip(poly,q0,q1,False)
  if len(part)>=3:outside.append(part)
  poly=clip(poly,q0,q1,True)
 if len(poly)<3 or abs(sum(cross(poly[k][:2],poly[(k+1)%len(poly)][:2]) for k in range(len(poly))))<1e-12:
  faces.append(t.tolist());uvref.append([i]*3);uvbary.append(np.eye(3));untouched.append(i);continue
 removed.append(i)
 for polygon in outside:
  ids=[vertex(q,i) for q in polygon]
  for k in range(1,len(ids)-1):
   if len({ids[0],ids[k],ids[k+1]})<3:continue
   q=np.array([points[ids[j]] for j in [0,k,k+1]])
   if np.linalg.norm(np.cross(q[1]-q[0],q[2]-q[0]))<1e-13:continue
   faces.append([ids[0],ids[k],ids[k+1]]);uvref.append([i]*3);uvbary.append(np.array([polygon[j][2:] for j in [0,k,k+1]]))
spread=max([max(v)-min(v) for v in cut_z.values()] or [0]);assert spread<2e-5,('Cut crosses folded boundary',spread)
# Add all clipped intersections in angular order; they sew the disk to exterior.
ring=np.unique(np.round(np.vstack([boundary,*cut_xy]),9),axis=0);angles=np.arctan2((ring[:,1]-center[1])/radius[1],(ring[:,0]-center[0])/radius[0]);ring=ring[np.argsort(angles)];n=len(ring)
grid=np.array([[x,y] for x in np.arange(center[0]-radius[0],center[0]+radius[0],.009) for y in np.arange(center[1]-radius[1],center[1]+radius[1],.009) if np.linalg.norm((np.array([x,y])-center)/radius)<.88]);proposal=triangle.triangulate({'vertices':np.vstack([ring,grid]),'segments':np.c_[np.arange(n),np.roll(np.arange(n),-1)]},'pQ');qs=proposal['vertices'];refs=[reference(q) for q in qs];ringz=np.array([b@candidate[tri[i],2] for i,b in refs[:n]])
# Interior follows the lowest outward sheet; thin-plate fairing removes the
# multi-layer fold, with a second exterior ring retaining boundary tangents.
seedxy=list(ring);seedz=list(ringz)
for scale in [.92,.72,.48,0.25]:
 for angle in np.linspace(0,2*np.pi,32,endpoint=False):
  q=center+radius*scale*np.array([np.cos(angle),np.sin(angle)]);i,b=reference(q);seedxy.append(q);seedz.append(float(b@candidate[tri[i],2]))
fit=RBFInterpolator(np.array(seedxy),np.array(seedz),kernel='thin_plate_spline',smoothing=1e-8);height=fit(qs);height[:n]=ringz;patchids=[]
for q,(i,b),z in zip(qs,refs,height):
 pos=b@candidate[tri[i]];pos[2]=z;key=tuple(np.round(pos,9));existing=lookup.get(key)
 if existing is None:existing=len(points);points.append(pos);mapping.append((i,b.copy()));lookup[key]=existing
 patchids.append(existing)
for t in proposal['triangles']:
 q=qs[t]
 if cross(q[1]-q[0],q[2]-q[0])<0:t=t[::-1]
 faces.append([patchids[k] for k in t]);uvref.append([refs[k][0] for k in t]);uvbary.append(np.array([refs[k][1] for k in t]))
# Weld newly introduced coincident cut points, retaining original vertex IDs.
points=np.array(points);lookup={tuple(np.round(q,9)):i for i,q in reversed(list(enumerate(points[:len(p)])))};remap=np.arange(len(points))
for i,q in enumerate(points[len(p):],len(p)):
 key=tuple(np.round(q,9))
 if key in lookup:remap[i]=lookup[key]
 else:lookup[key]=i
faces=remap[np.array(faces)];uvref=np.array(uvref);uvbary=np.array(uvbary);live=np.unique(faces);local=live[(live>=len(p))&(points[live,2]>.84)&(np.linalg.norm((points[live,:2]-center)/radius,axis=1)<1.6)];tree=cKDTree(points[local]);clean=[];cleanref=[];cleanbary=[];split=0
for face,refs0,bary0 in zip(faces,uvref,uvbary):
 if len(set(face))<3:continue
 normal=np.cross(points[face[1]]-points[face[0]],points[face[2]]-points[face[0]])
 if np.linalg.norm(normal)<1e-13:continue
 polygon=[]
 for j,A in enumerate(face):
  B=face[(j+1)%3];v=points[B]-points[A];length=np.linalg.norm(v);ids=local[tree.query_ball_point((points[A]+points[B])/2,length/2+2e-7)] if points[A,2]>.84 and points[B,2]>.84 else [];along=[]
  for k in ids:
   if len(set(refs0))!=1:continue
   source=mapping[k][0]
   f=np.dot(points[k]-points[A],v)/(length*length)
   if 1e-7<f<1-1e-7 and np.linalg.norm(points[k]-points[A]-f*v)<2e-7:along.append((f,int(k)))
  unique={tuple(np.round(points[k],9)):(f,k) for f,k in along};polygon.append(int(A));polygon.extend(k for f,k in sorted(unique.values()))
 if len(polygon)==3:clean.append(face);cleanref.append(refs0);cleanbary.append(bary0);continue
 split+=1;origin=points[face[0]];u=(points[face[1]]-origin);u/=np.linalg.norm(u);nrm=normal/np.linalg.norm(normal);v=np.cross(nrm,u);q=np.c_[(points[polygon]-origin)@u,(points[polygon]-origin)@v];tess=triangle.triangulate({'vertices':q,'segments':np.c_[np.arange(len(q)),np.roll(np.arange(len(q)),-1)]},'pQ');assert len(tess['vertices'])==len(polygon)
 for inds in tess['triangles']:
  row=[polygon[k] for k in inds];refl=[];barl=[]
  for k in row:
   if k in face:
    j=list(face).index(k);refl.append(refs0[j]);barl.append(bary0[j])
   elif len(set(refs0))==1:
    source=int(refs0[0]);coords=candidate[tri[source]];ab=np.linalg.lstsq(np.stack([coords[1]-coords[0],coords[2]-coords[0]],axis=1),points[k]-coords[0],rcond=None)[0];refl.append(source);barl.append(np.r_[1-ab.sum(),ab])
   else:
    source,bar=reference(points[k,:2]);refl.append(source);barl.append(bar)
  xyz=points[row]
  if np.linalg.norm(np.cross(xyz[1]-xyz[0],xyz[2]-xyz[0]))<1e-11:continue
  clean.append(row);cleanref.append(refl);cleanbary.append(barl)
faces=np.array(clean);uvref=np.array(cleanref);uvbary=np.array(cleanbary);edges=Counter(tuple(sorted(e)) for t in faces for e in [(t[0],t[1]),(t[1],t[2]),(t[2],t[0])]);bad=[(e,n) for e,n in edges.items() if n>2]
if bad:
 np.savez_compressed(D/'crown-retopo-rejected.npz',points=points,faces=faces)
 (D/'crown-retopo-rejected.json').write_text(json.dumps({'reason':'New nonmanifold edge after junction split','edges':[[[int(x) for x in e],n,points[list(e)].tolist(),[faces[i].tolist() for i in range(len(faces)) if set(e)<=set(faces[i])]] for e,n in bad[:10]]},indent=2));raise ValueError('New nonmanifold edge '+str(len(bad)))
newmap=mapping[len(p):];newref=np.array([i for i,b in newmap]);newbary=np.array([b for i,b in newmap]);base_interpolated=np.einsum('ni,nij->nj',newbary,candidate[tri[newref]]);offset=points[len(p):]-base_interpolated
np.savez_compressed(D/'crown-retopo.npz',faces=np.array(faces),points=points,new_reference=newref,new_barycentric=newbary,new_offset=offset,uv_reference=np.array(uvref),uv_barycentric=np.array(uvbary),untouched=np.array(untouched),removed=np.array(removed),old_triangles=tri)
report={'planner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'method':'Convex local crown cut through all folded layers; one outward height-field triangulation; barycentric shape/weight/UV transfer; unchanged exterior triangles','ellipse_center':center.tolist(),'ellipse_radius':radius.tolist(),'removed_triangles':len(removed),'source_vertices':len(p),'new_vertices':len(points)-len(p),'result_triangles':len(faces),'patch_triangles':len(proposal['triangles']),'boundary_points':n,'cut_layer_max_spread':spread,'T_junction_faces_split':split,'new_nonmanifold_edges':sum(k>2 for k in edges.values()),'gate':'PREVIEW_PENDING'};(D/'crown-retopo.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
