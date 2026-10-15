"""Physical lid/lip collars preserve the inherited exterior. Visual HOLD.

Rejected cut/fairing trials are retained as evidence; delivered Basis is exact.
"""
import numpy as np
import math
from collections import Counter,defaultdict
from mathutils import Vector

def repair_face(v,comp,norm,r,keydata,keynames,polys,uvs,matids,regions,weights,report):
 N=len(v);origins=list(range(len(polys)));atlas=[];muzzlecoef=None
 def design(u,z):return np.array([np.ones_like(u),u,z,u*u,u*z,z*z]).T
 def add(p,shape=None):
  i=len(weights);weights.append({'DEF_head':1.})
  for k in keynames:keydata[k].append(np.array((shape or {}).get(k,p),dtype=float))
  return i
 def uvrect(rect,u,w):return [rect[0]+rect[2]*u,rect[1]+rect[3]*w]
 def face(ids,uv,mi,region):
  polys.append(ids);uvs.append(uv);matids.append(mi);regions.append(region);origins.append(None)
 def cut(test,label):
  nonlocal polys,uvs,matids,regions,origins,muzzlecoef
  # Preserve the approved coarse exterior. The lid collar sits within the
  # original socket; its outside edge is buried beneath the original skin.
  if label.startswith('socket'):
   loop=[]
   for j in range(64):
    theta=2*math.pi*j/64;U=ru*1.18*math.cos(theta);Z=rz*1.18*math.sin(theta)
    loop.append(add(center+tangent*U+np.array([0,0,Z])+normal*(float(design(U,Z)@coef)-.002)))
   report['local_changes'].append({'graft':label,'method':'3D lid collar buried under inherited socket exterior; no exterior cut','removed_original_polygons':[],'boundary_vertices':loop,'extra_boundary_loops':[]})
   return loop
  if label=='mouth':
   removed=[i for i,p in enumerate(polys) if origins[i] is not None and comp[p[0]]==0 and (np.mean(v[p],axis=0)[0]/.044)**2+((np.mean(v[p],axis=0)[2]-.603)/.027)**2<1 and np.mean(v[p],axis=0)[1]>-.397 and np.mean(v[p],axis=0)[1]<-.325]
   rr=[origins[i] for i in removed];keep=[i for i in range(len(polys)) if i not in set(removed)]
   polys=[polys[i] for i in keep];uvs=[uvs[i] for i in keep];matids=[matids[i] for i in keep];regions=[regions[i] for i in keep];origins=[origins[i] for i in keep]
   # A continuous 3D muzzle collar covers the old recess and retracts inward at
   # close. Its outer edge is inside the original skin, never a painted mouth.
   loop=[]
   for j in range(64):
    theta=2*math.pi*j/64;X=.067*math.cos(theta);Z=.607+.047*math.sin(theta)
    # analytic round muzzle, buried at perimeter; open rim remains forward.
    Y=-.408+2.3*X*X+2.0*(Z-.625)**2+.005
    loop.append(add(np.array([X,Y,Z])))
   p=np.array([keydata['Basis'][i] for i in loop]);muzzlecoef=np.linalg.lstsq(design(p[:,0],p[:,2]-.609),p[:,1],rcond=None)[0]
   report['local_changes'].append({'graft':label,'method':'physical lip collar over inherited recess; only deep old oral faces removed','removed_original_polygons':rr,'boundary_vertices':loop,'extra_boundary_loops':[]})
   return loop
 def hull(points):
  pts=sorted([(float(p[0]),float(p[1]),i) for i,p in enumerate(points)])
  def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
  lo=[];hi=[]
  for p in pts:
   while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
   lo.append(p)
  for p in reversed(pts):
   while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
   hi.append(p)
  return [p[2] for p in lo[:-1]+hi[:-1]]
 def angles(loop,coords):
  p=coords[loop];d=np.linalg.norm(np.roll(p,-1,axis=0)-p,axis=1)
  direction=1 if np.sum(p[:,0]*np.roll(p[:,1],-1)-p[:,1]*np.roll(p[:,0],-1))>0 else -1
  return math.atan2(p[0,1],p[0,0])+direction*2*math.pi*np.r_[0,np.cumsum(d[:-1])]/sum(d)
 # Discard original blink effects on original vertices; the graft is the lid.
 for side,ci,sgn in [('L',99,1),('R',98,-1)]:
  blink='FACE_Blink.'+side;keydata[blink][:N]=[p.copy() for p in v]
  eye=v[comp==ci];center=eye.mean(0);normal=np.array([sgn*.52,-.85,0]);normal/=np.linalg.norm(normal);tangent=np.array([.85,sgn*.52,0]);tangent/=np.linalg.norm(tangent)
  q=np.c_[(v-center)@tangent,v[:,2]-center[2],(v-center)@normal];eu=q[comp==ci];ru=max(abs(eu[:,0]));rz=max(abs(eu[:,1]));rho=np.sqrt((q[:,0]/ru)**2+(q[:,1]/rz)**2)
  fit=(comp==0)&(rho>1.25)&(rho<1.90)&(abs(q[:,2])<.08)&((norm@normal)>.45)
  coef=np.linalg.lstsq(design(q[fit,0],q[fit,1]),q[fit,2],rcond=None)[0]
  def local(p):
   a=p-center;return np.array([a@tangent,a[2],a@normal])
  def test(p):
   a=local(p);return (a[0]/ru)**2+(a[1]/rz)**2<1.28**2 and a[2]>-.085
  loop=cut(test,'socket-'+side)
  allv=np.array(keydata['Basis']);q=np.c_[(allv-center)@tangent,allv[:,2]-center[2],(allv-center)@normal]
  hullids=hull(eu[:,:2]);hp=eu[hullids];he=eye[hullids]
  def eyeedge(theta):
   d=np.array([ru*math.cos(theta),rz*math.sin(theta)])
   for i in range(len(hp)):
    j=(i+1)%len(hp);a=hp[i,:2];edge=hp[j,:2]-a
    M=np.c_[d,-edge]
    if abs(np.linalg.det(M))<1e-10:continue
    t,h=np.linalg.solve(M,a)
    if t>=0 and -.0001<=h<=1.0001:return he[i]*(1-h)+he[j]*h+normal*.00065
   raise RuntimeError('eye hull ray missing')
  rect=(.91,.03 if side=='L' else .25,.075,.18);atlas.append({'region':'lids-'+side,'rect':rect})
  # One periodic annulus: no disconnected corner seams or uniform-index
  # correspondence across an irregular inherited boundary.
  grid=[];ny=14;nt=len(loop)
  for originali,theta in zip(loop,angles(loop,q[:,:2]/[ru,rz])):
   outer=keydata['Basis'][originali];oq=local(outer)
   inner=eyeedge(theta);iq=local(inner);U=iq[0]/ru
   seamZ=.0045-.010*abs(U)**1.7
   sq=np.array([iq[0],seamZ,0.]);row=[originali]
   outerres=oq[2]-float(design(oq[0],oq[1])@coef)
   innerres=iq[2]-float(design(iq[0],iq[1])@coef)
   for iy in range(1,ny+1):
    t=iy/ny;pq=(1-t)*oq+t*iq;cq=(1-t)*oq+t*sq
    pq[2]=float(design(pq[0],pq[1])@coef)+(1-t)**3*outerres+t**3*innerres
    cq[2]=float(design(cq[0],cq[1])@coef)+(1-t)**3*outerres-.00055*t**6
    cq[1]+=math.sin(theta)*.00010*t**6
    p=center+tangent*pq[0]+np.array([0,0,pq[1]])+normal*pq[2]
    closed=center+tangent*cq[0]+np.array([0,0,cq[1]])+normal*cq[2]
    row.append(add(p,{blink:closed}))
   grid.append(row)
  for ix in range(nt):
   k=(ix+1)%nt
   for iy in range(ny):
    ids=[grid[ix][iy],grid[k][iy],grid[k][iy+1],grid[ix][iy+1]]
    coords=[uvrect(rect,u,w) for u,w in [(ix/nt,iy/ny),((ix+1)/nt,iy/ny),((ix+1)/nt,(iy+1)/ny),(ix/nt,(iy+1)/ny)]]
    face(ids,coords,0,'lids-'+side)
  # Delay eyeball retreat to the last fifth of closure; no half-blink shrink.
  bone=r.pose.bones['DEF_eye.'+side];axis=r.data.bones[bone.name].matrix_local.to_3x3().inverted()@Vector(normal)
  for i in range(3):
   fc=bone.driver_add('location',i);fc.driver.type='SCRIPTED';fc.driver.expression='0*b'
   var=fc.driver.variables.new();var.name='b';var.type='SINGLE_PROP';var.targets[0].id=r;var.targets[0].data_path='["blink.'+side+'"]'
  for i in np.flatnonzero(comp==ci):keydata[blink][i]=v[i]-normal*.034

 # A new lip skin/cavity replaces only the oral recess and malformed teeth.
 x,y,z=v.T
 loop=cut(lambda p:(p[0]/.068)**2+((p[2]-.609)/.045)**2<1 and p[1]<-.325 and p[2]<.644,'mouth')
 keydata['FACE_MouthClose'][:N]=[p.copy() for p in v];keydata['FACE_MouthOpen'][:N]=[p.copy() for p in v]
 rect=(.91,.47,.075,.20);atlas.append({'region':'mouth-skin-inner','rect':rect})
 # Fit surrounding muzzle so both open and shut lips join the existing volume.
 rho=np.sqrt((x/.068)**2+((z-.609)/.045)**2)
 fit=(comp==0)&(rho>1.05)&(rho<1.9)&(y<-.31)&(norm[:,1]<-.45)
 coefm=np.linalg.lstsq(design(x[fit],z[fit]-.609),y[fit],rcond=None)[0]
 def muzzle(X,Z):return float(design(X,Z-.609)@coefm)
 def muzzle(X,Z):return -.408+2.3*X*X+2.0*(Z-.625)**2
 oral=(comp==0)&((x/.048)**2+((z-.606)/.028)**2<1)&(y<-.335)&(z<.630)
 for i in np.flatnonzero(oral):keydata['FACE_MouthClose'][i]=v[i]+np.array([0,.035,0])
 def lip(U,half,amount):
  upperZ=.622+.004*np.exp(-(U/.30)**2)-.001*(1-U*U)
  lowerZ=.575+.047*abs(U)**1.80
  Z=upperZ if half==1 else lowerZ
  if amount=='closed':Z=.614+.008*abs(U)**1.6+half*.00012
  if amount=='big' and half==-1:Z-=.013*(1-U*U)
  return np.array([.045*U,-.398+.004*U*U-.10*(Z-.605),Z])
 grid=[];ny=12;nt=len(loop)
 allv=np.array(keydata['Basis'])
 for originali,theta in zip(loop,angles(loop,np.c_[allv[:,0]/.067,(allv[:,2]-.607)/.047])):
   outer=keydata['Basis'][originali];U=math.cos(theta);half=1 if math.sin(theta)>=0 else -1
   p0=lip(U,half,'smile');pc=lip(U,half,'closed');po=lip(U,half,'big');pc[1]=muzzle(pc[0],pc[2])-.0003
   row=[originali]
   for iy in range(1,ny+1):
    t=iy/ny;p=(1-t)*outer+t*p0;c=(1-t)*outer+t*pc;o=(1-t)*outer+t*po
    for a,inner in [(p,p0),(c,pc),(o,po)]:
     a[1]=muzzle(a[0],a[2])+(1-t)**3*(outer[1]-muzzle(outer[0],outer[2]))+t**3*(inner[1]-muzzle(inner[0],inner[2]))
    shapes={'FACE_MouthClose':c,'FACE_MouthOpen':o}
    # Keep existing corner-smile channels and the inherited fixed graft boundary.
    for side,sgn in [('L',1),('R',-1)]:
     shapes['FACE_Smile.'+side]=p+np.array([0,0,.0025*t*max(sgn*U,0)**2])
    row.append(add(p,shapes))
   grid.append(row)
 for ix in range(nt):
  k=(ix+1)%nt
  for iy in range(ny):
   ids=[grid[ix][iy],grid[k][iy],grid[k][iy+1],grid[ix][iy+1]]
   coords=[uvrect(rect,u,w*.5) for u,w in [(ix/nt,iy/ny),((ix+1)/nt,iy/ny),((ix+1)/nt,(iy+1)/ny),(ix/nt,(iy+1)/ny)]]
   face(ids,coords,0,'mouth-skin')
 rim=[row[-1] for row in grid];nr=8;nt=len(rim);grid=[rim]
 centers={'Basis':np.array([0,-.352,.600]),'FACE_MouthClose':np.array([0,-.350,.614]),'FACE_MouthOpen':np.array([0,-.352,.595])}
 for j in range(1,nr+1):
  t=j/(nr+1);row=[]
  for originali in rim:
   shape={}
   for key in keynames:
    p=keydata[key][originali];c=centers.get(key,centers['Basis']);shape[key]=(1-t)*p+t*c
    shape[key][1]+=.006*math.sin(math.pi*t)
   row.append(add(shape['Basis'],shape))
  grid.append(row)
 for j in range(nr):
  for i in range(nt):
   k=(i+1)%nt
   face([grid[j][i],grid[j][k],grid[j+1][k],grid[j+1][i]],
    [uvrect(rect,.5+.45*(1-a/(nr+1))*math.cos(2*math.pi*b/nt),.75+.24*(1-a/(nr+1))*math.sin(2*math.pi*b/nt)) for a,b in [(j,i),(j,k),(j+1,k),(j+1,i)]],2,'mouth-inner')
 centerid=add(centers['Basis'],centers)
 for i in range(nt):
  k=(i+1)%nt
  face([grid[-1][i],grid[-1][k],centerid],[uvrect(rect,.5+.05*math.cos(2*math.pi*a/nt),.75+.026*math.sin(2*math.pi*a/nt)) for a in [i,k]]+[uvrect(rect,.5,.75)],2,'mouth-inner')
 # Short tongue has a rounded closed surface; it retracts fully behind closed lips.
 rect=(.91,.72,.075,.16);atlas.append({'region':'tongue','rect':rect});nu=32;nv=12;grid=[]
 for j in range(nv+1):
  lat=-math.pi/2+math.pi*(j+.04)/(nv+.08);row=[]
  for i in range(nu):
   lon=2*math.pi*i/nu;p=np.array([.023*math.cos(lat)*math.cos(lon),-.382+.012*math.cos(lat)*math.sin(lon),.586+.006*math.sin(lat)])
   pc=p.copy();pc[1]+=.023;pc[2]=.612+(p[2]-.586)*.2
   po=p.copy();po[2]-=.012
   row.append(add(p,{'FACE_MouthClose':pc,'FACE_MouthOpen':po}))
  grid.append(row)
 for j in range(nv):
  for i in range(nu):
   k=(i+1)%nu
   face([grid[j][i],grid[j][k],grid[j+1][k],grid[j+1][i]],
    [uvrect(rect,u,w) for u,w in [(i/nu,j/nv),((i+1)/nu,j/nv),((i+1)/nu,(j+1)/nv),(i/nu,(j+1)/nv)]],3,'tongue')
 for j in [0,nv]:
  ids=grid[j][::-1] if j==0 else grid[j]
  caprect=(.91+(.04 if j==nv else 0),.895,.035,.025)
  face(ids,[uvrect(caprect,.5+.45*math.cos(2*math.pi*i/nu),.5+.45*math.sin(2*math.pi*i/nu)) for i in range(nu)],3,'tongue')
 # Two small 3D fangs; hide within the oral pocket at close.
 rect=(.91,.95,.075,.035);atlas.append({'region':'teeth','rect':rect})
 for tooth,sgn in enumerate([-1,1]):
  top=.623;pts=[np.array([sgn*.025+dx,-.403+dy,top+dz]) for dx,dy,dz in [(-.003,.001,0),(.003,.001,0),(0,-.002,-.009),(0,.004,-.003)]]
  ids=[]
  for p in pts:
   pc=p.copy();pc[1]+=.018;pc[2]=.616
   ids.append(add(p,{'FACE_MouthClose':pc}))
  for ti,tri in enumerate([(0,2,1),(0,1,3),(1,2,3),(2,0,3)]):
   tr=(rect[0]+tooth*.039,rect[1]+ti*.008,.034,.006)
   face([ids[i] for i in tri],[uvrect(tr,a,b) for a,b in [(.04,.04),(.96,.04),(.5,.96)]],4,'teeth')
 report['local_changes'].append({'face_grafts':'inherited exterior unchanged, deep oral faces removed; physical overlapping collars, no global remesh; visual HOLD','20_morphs':'two lid morphs consolidated into body; eye recession in same blink morphs','tongue':'short rounded oral surface','mouth_close':'physical lip contact, cavity/teeth/tongue retract; muzzle blending remains HOLD'})
 return polys,uvs,matids,regions,origins,atlas
