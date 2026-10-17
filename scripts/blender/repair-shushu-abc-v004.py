"""Identity-preserving candidate: rooted short arms, obsolete close-shape removal,
and physical lower-abdomen fairing. Never writes source v003/v004 assets.
"""
import bpy,sys,json,importlib.util,re
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging';sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);b=g.r.b
ASSET=B/'shushu-v004-motion-gate-v004.blend'
def coords(k):return np.array([v.co[:] for v in k.data])
def put(k,p):k.data.foreach_set('co',np.asarray(p,dtype=np.float32).ravel())
def fair_surface(o,p,mask,iterations=30,lowpass=False):
 base=np.array([v.co[:] for v in o.data.vertices]);unique,ids=np.unique(np.round(base,6),axis=0,return_inverse=True);counts=np.bincount(ids);n=len(unique);grouped=np.zeros((n,3));np.add.at(grouped,ids,p);grouped/=counts[:,None]
 edges=np.unique(np.sort(ids[np.array([e.vertices[:] for e in o.data.edges])],axis=1),axis=0);edges=edges[edges[:,0]!=edges[:,1]];aa=np.r_[edges[:,0],edges[:,1]];bb=np.r_[edges[:,1],edges[:,0]];degree=np.bincount(aa,minlength=n);w=np.zeros(n);np.add.at(w,ids,mask);w/=counts;w[degree==0]=0;degree=degree.clip(1)
 q=grouped.copy()
 for j in range(iterations):
  sums=np.stack([np.bincount(aa,weights=q[bb,c],minlength=n) for c in range(3)],axis=1);q+=(sums/degree[:,None]-q)*(w*(.35 if lowpass else .50 if j%2==0 else -.50))[:,None]
 return p+(q-grouped)[ids]
def lowpass_field(o,field,steps=4):
 p=np.array([v.co[:] for v in o.data.vertices]);_,ids=np.unique(np.round(p,6),axis=0,return_inverse=True);count=np.bincount(ids);n=len(count);values=np.zeros((n,3));np.add.at(values,ids,field);values/=count[:,None];edges=np.unique(np.sort(ids[np.array([e.vertices[:] for e in o.data.edges])],axis=1),axis=0);edges=edges[edges[:,0]!=edges[:,1]];a=np.r_[edges[:,0],edges[:,1]];c=np.r_[edges[:,1],edges[:,0]];degree=np.bincount(a,minlength=n).clip(1)
 for _ in range(steps):
  sums=np.zeros_like(values);np.add.at(sums,a,values[c]);values+=(sums/degree[:,None]-values)*.5
 return values[ids]

def corrective_field(rig):
 o=bpy.data.objects['ShushuStatic_Torso'];p=coords(o.data.shape_keys.key_blocks[0]);x,y,z=p.T;mask=b.smooth(.10,.16,z)*(1-b.smooth(.30,.37,z))*(1-b.smooth(.14,.21,np.abs(x)))*(1-b.smooth(-.05,.025,y));drivers=[fc for fc in o.data.shape_keys.animation_data.drivers if 'Corrective.TrueSeat.' in fc.data_path];keys=[k for k in o.data.shape_keys.key_blocks if k.name.startswith('Corrective.TrueSeat.')];records=[]
 for key in keys:
  match=re.fullmatch(r'Corrective.TrueSeat.S([\d.]+).W(-?[\d.]+)',key.name);seat,shift=map(float,match.groups());b.state(rig,{'Seat':seat,'WeightShift':shift});q,_=b.evaluated(o)
  for fc in drivers:fc.mute=True
  for k in keys:k.value=0
  o.update_tag();bpy.context.view_layer.update();raw,_=b.evaluated(o)
  for fc in drivers:fc.mute=False
  b.state(rig,{'Seat':seat,'WeightShift':shift});delta=(raw+lowpass_field(o,q-raw)-q)*mask[:,None];size=np.linalg.norm(delta,axis=1);delta*=np.minimum(1,.012/np.maximum(size,1e-12))[:,None];mat=b.skin_matrices(rig,o);put(key,coords(key)+np.linalg.solve(mat[:,:3,:3],delta[:,:,None])[:,:,0]);o.data.update();o.update_tag();after,_=b.evaluated(o);records.append({'key':key.name,'max_world_repair':float(np.linalg.norm(delta,axis=1).max()),'target_evaluation_error':float(abs(after-(q+delta)).max())})
 b.reset(rig);return records

def belly(rig):
 o=bpy.data.objects['ShushuStatic_Torso'];p=coords(o.data.shape_keys.key_blocks[0]);x,y,z=p.T
 # The Human scope includes latent bumps on feet, flanks and rump as well.
 # Fair the actual posed surface; preserve the ground-contact strip.
 records=[]
 for key in o.data.shape_keys.key_blocks:
  m=re.fullmatch(r'Corrective.TrueSeat.S([\d.]+).W(-?[\d.]+)',key.name)
  if not m:continue
  seat,shift=map(float,m.groups());b.state(rig,{'Seat':seat,'WeightShift':shift});q,_=b.evaluated(o);mask=b.smooth(.003,.018,q[:,2]);target=fair_surface(o,q,mask,192);delta=target-q;mat=b.skin_matrices(rig,o);local=np.linalg.solve(mat[:,:3,:3],delta[:,:,None])[:,:,0]
  put(key,coords(key)+local);o.data.update();o.update_tag();records.append({'key':key.name,'seat':seat,'shift':shift,'changed':int((np.linalg.norm(delta,axis=1)>1e-7).sum()),'max_world_repair':float(np.linalg.norm(delta,axis=1).max()),'condition_max':float(np.linalg.cond(mat[:,:3,:3][mask>0]).max())})
 b.reset(rig);return records

def rest_surface_cleanup():
 records=[]
 for name,iterations,limit in [('Head',48,.006),('Ear_L',32,.003),('Ear_R',32,.003),('Torso',48,.006),('Paw_L',24,.003),('Paw_R',24,.003)]:
  o=bpy.data.objects['ShushuStatic_'+name];ks=o.data.shape_keys.key_blocks if o.data.shape_keys else [];p=coords(ks[0]) if ks else np.array([v.co[:] for v in o.data.vertices]);mask=np.ones(len(p))
  if name=='Head':
   x,y,z=p.T
   # Preserve the W boundary, nose junction, eyelid rims and approved eye opening.
   mouth=(1-b.smooth(.065,.09,np.abs(x)))*(1-b.smooth(.025,.05,np.abs(z-.632)))*(1-b.smooth(-.16,-.10,y))
   eyes=(1-b.smooth(.045,.075,np.abs(np.abs(x)-.105)))*(1-b.smooth(.06,.09,np.abs(z-.73)))*(1-b.smooth(-.13,-.07,y))
   mask*=1-np.maximum(mouth,eyes)
   patch=np.load(D.parent/'muzzle-retopo.npz');rim=np.arange(34667+int(patch['outer_count']),34667+len(patch['boundary_ids']));mask[rim]=0
  if name=='Torso':mask*=b.smooth(.04,.075,p[:,2])
  delta=fair_surface(o,p,mask,iterations,lowpass=True)-p;size=np.linalg.norm(delta,axis=1);delta*=(limit*np.tanh(size/limit)/np.maximum(size,1e-12))[:,None]
  if name=='Head':
   _,ids=np.unique(np.round(p,6),axis=0,return_inverse=True);delta[np.isin(ids,np.unique(ids[rim]))]=0
  if ks:
   for key in ks:put(key,coords(key)+delta)
  o.data.vertices.foreach_set('co',(p+delta).astype(np.float32).ravel());o.data.update();o.update_tag()
  records.append({'mesh':o.name,'changed':int((np.linalg.norm(delta,axis=1)>1e-7).sum()),'max_rest_delta':float(np.linalg.norm(delta,axis=1).max()),'protected_features':'W/eye/nose on Head; soles on Torso','iterations':iterations})
 return records
POSE_PARAMETERS={'Hold':{'start':(.45,-.98,-.65),'end':(.05,-.75,.4),'begin':.05,'end_at':.7},'SelfContact':{'start':(.45,-.98,-.35),'end':(.35,-.75,1.2),'begin':.05,'end_at':.7},'Offer':{'start':(.85,-.98,-.7),'end':(.75,-.98,-.3),'begin':.05,'end_at':.7}}

def pose_spec(mode,side,seat):
 spec=dict(POSE_PARAMETERS[mode])
 if mode=='Hold':spec['end']=(.05+.1*float(seat),-.75,.4)
 if mode=='SelfContact' and side=='R':spec['start']=(.45,-.98,-.38);spec['end']=(.45,-.75,.98)
 return spec

def curve_surface(base,old,root,axis,wrist,mode='NeutralWrist',amount=0.,spec=None):
 if spec is not None and 'start' in spec or spec is None and mode in POSE_PARAMETERS and 'start' in POSE_PARAMETERS[mode]:
  return elbow_surface(base,root,axis,wrist,amount,spec or POSE_PARAMETERS[mode])
 # Shoulder rotates about its actual attached support. Elbow curvature remains
 # mild and distributed; it never fits an unreachable old translated endpoint.
 sign=1 if axis[0]>0 else -1;spec=spec or POSE_PARAMETERS.get(mode);goal=np.array(tuple(axis) if mode=='NeutralWrist' else (sign*spec['goal'][0],*spec['goal'][1:]));goal/=np.linalg.norm(goal);angle=float(np.arccos(np.clip(axis@goal,-1,1)))*amount
 along=(base-root)@axis;length=float(np.ptp(along));radial=base-root-along[:,None]*axis
 if angle>1e-7:
  full=float(np.arccos(np.clip(axis@goal,-1,1)));bend=(goal-axis*np.cos(full))/np.sin(full);normal=np.cross(axis,bend);theta=spec['bend']*amount;beta=theta*along/length;start=axis*np.cos(angle)+bend*np.sin(angle);crossbend=-axis*np.sin(angle)+bend*np.cos(angle)
  center=root+start*(length*np.sin(beta)/theta)[:,None]+crossbend*(length*(1-np.cos(beta))/theta)[:,None];phase=angle+beta;cs=np.cos(phase)[:,None];sn=np.sin(phase)[:,None];transport=radial*cs+np.cross(normal,radial)*sn+normal*(radial@normal)[:,None]*(1-cs);tangent=axis*np.cos(phase)[:,None]+bend*np.sin(phase)[:,None]
 else:center=root+along[:,None]*axis;transport=radial.copy();tangent=np.broadcast_to(axis,base.shape).copy()
 twist=.35*wrist*b.smooth(.55,.90,along/np.linalg.norm(np.array([.17,-.094,-.094])));cs=np.cos(twist)[:,None];sn=np.sin(twist)[:,None];transport=transport*cs+np.cross(tangent,transport)*sn+tangent*np.einsum('ij,ij->i',tangent,transport)[:,None]*(1-cs)
 return center+transport,{'shoulder_angle':angle,'distributed_bend_angle':0 if mode=='NeutralWrist' else spec['bend']*amount,'root':root.tolist(),'rest_length':length}

def elbow_surface(base,root,axis,wrist,amount,spec):
 sign=1 if axis[0]>0 else -1
 def side(v):
  q=np.array([sign*v[0],v[1],v[2]],dtype=float);return q/np.linalg.norm(q)
 def rotate(v,n,a):
  a=np.asarray(a);cs=np.cos(a)[...,None];sn=np.sin(a)[...,None]
  return v*cs+np.cross(n,v)*sn+np.einsum('...i,i->...',v,n)[...,None]*n*(1-cs)
 start=side(spec['start']);end=side(spec['end']);rn=np.cross(axis,start);rn/=np.linalg.norm(rn);ra=float(np.arccos(np.clip(axis@start,-1,1)));localend=rotate(end,rn,-ra);en=np.cross(axis,localend);en/=np.linalg.norm(en);ea=float(np.arccos(np.clip(axis@localend,-1,1)))
 along=(base-root)@axis;length=float(np.ptp(along));radial=base-root-along[:,None]*axis;grid=np.linspace(min(0,along.min()),max(0,along.max()),513);phase=ea*amount*b.smooth(spec.get('begin',.05),spec.get('end_at',.80),grid/length);tangent=rotate(np.broadcast_to(axis,(len(grid),3)),en,phase);center=np.zeros_like(tangent);center[1:]=np.cumsum((tangent[1:]+tangent[:-1])*.5*np.diff(grid)[:,None],axis=0);center-=np.array([np.interp(0,grid,center[:,j]) for j in range(3)]);center=np.array([np.interp(along,grid,center[:,j]) for j in range(3)]).T
 phase=ea*amount*b.smooth(spec.get('begin',.05),spec.get('end_at',.80),along/length);transport=rotate(radial,en,phase);tangent=rotate(np.broadcast_to(axis,base.shape),en,phase);twist=.35*wrist*b.smooth(.55,.90,along/.215);transport=transport*np.cos(twist)[:,None]+np.cross(tangent,transport)*np.sin(twist)[:,None]+tangent*np.einsum('ij,ij->i',tangent,transport)[:,None]*(1-np.cos(twist))[:,None]
 # Internal shoulder cap stays with the trunk. Rotation spreads across the
 # short proximal flesh instead of swinging that cap upward into the chin.
 shoulder_profile=b.smooth(-.005,.09,along)
 return root+rotate(center+transport,rn,ra*amount*shoulder_profile),{'shoulder_angle':ra*amount,'distributed_bend_angle':ea*amount,'root':root.tolist(),'rest_length':length,'structure':'attached internal shoulder cap, distributed shoulder flesh and separate elbow flexion','spec':spec}

def arms(rig):
 records=[]
 for side,longname in [('L','Left'),('R','Right')]:
  o=bpy.data.objects['ShushuStatic_Paw_'+side];ks=o.data.shape_keys.key_blocks;base=coords(ks[0]);root=np.array(rig.data.bones['mixamorig:'+longname+'Shoulder'].head_local);hand=np.array(rig.data.bones['mixamorig:'+longname+'Hand'].head_local);axis=(hand-root)/np.linalg.norm(hand-root)
  index=int(bpy.data.objects['ANCHOR_Hold.'+side]['surface_vertex']);o.data.calc_loop_triangles();tri=np.array([t.vertices[:] for t in o.data.loop_triangles]);same=np.where(np.linalg.norm(base-base[index],axis=1)<1e-6)[0];fan=tri[np.isin(tri,same).any(1)]
  def offset(q):
   ns=np.zeros(3)
   for t in fan:
    corner=next(j for j,i in enumerate(t) if i in same);a=q[t[(corner+1)%3]]-q[t[corner]];c=q[t[(corner+2)%3]]-q[t[corner]];n=np.cross(a,c);size=np.linalg.norm(n)
    if size>1e-12:ns+=n/size*np.arctan2(size,a@c)
   return .031*ns/max(np.linalg.norm(ns),1e-12)
  base_offset=offset(base);lookup={};offsets={}
  for key in ks[1:]:
   m=re.fullmatch(r'PoseSpace.NeutralWrist.0.S([\d.]+).W(-?[\d.]+)',key.name)
   if m:
    target,report=curve_surface(base,coords(key),root,axis,float(m.group(2)));put(key,target);offsets[key.name]=offset(target)-base_offset
  root_taper=b.smooth(.05,.35,((base-root)@axis-((base-root)@axis).min())/np.ptp((base-root)@axis))
  for key in ks[1:]:
   m=re.fullmatch(r'PoseSpace.(Hold|SelfContact|Offer).(\d+).S([\d.]+).W(-?[\d.]+)',key.name)
   if not m:continue
   mode,amount,seat,wrist=m.groups();old=coords(key);spec=pose_spec(mode,side,seat)
   target,report=curve_surface(base,old,root,axis,float(wrist),mode,float(amount)/1000,spec);put(key,target);lookup[(mode,amount,seat,wrist)]=target;offsets[key.name]=offset(target)-base_offset;records.append({'side':side,'key':key.name,**report})
  for key in ks[1:]:
   m=re.fullmatch(r'PoseSpace.(Hold|SelfContact|Offer)~(Hold|SelfContact|Offer).(\d+).S([\d.]+).W(-?[\d.]+)',key.name)
   if not m:continue
   first,second,amount,seat,wrist=m.groups();specs=[pose_spec(mode,side,seat) for mode in [first,second]];spec={k:(np.array(specs[0][k])+np.array(specs[1][k]))*.5 for k in ['start','end']};spec.update(begin=.05,end_at=.7)
   midpoint,_=curve_surface(base,base,root,axis,float(wrist),first,float(amount)/1000,spec)
   average=(lookup[(first,amount,seat,wrist)]+lookup[(second,amount,seat,wrist)])*.5
   put(key,base+midpoint-average)
   offsets[key.name]=offset(midpoint)-.5*(offset(lookup[(first,amount,seat,wrist)])+offset(lookup[(second,amount,seat,wrist)]))
  # Rebuild existing anchor-sum coefficients from the SAME new surface keys.
  inv=np.array(rig.data.bones['mixamorig:Spine2'].matrix_local.inverted());delta=[inv[:3,:3]@(coords(k)[index]-base[index]+offsets[k.name]) for k in ks[1:]]
  for fc in rig.animation_data.drivers:
   m=re.fullmatch(r'\["PawAnchorSum.'+side+r'.(\d).(\d+)"\]',fc.data_path)
   if m:
    component,start=map(int,m.groups());fc.driver.expression='+'.join(f'({row[component]:.9g})*{chr(97+j)}' for j,row in enumerate(delta[start:start+12]))
  anchor=bpy.data.objects['ANCHOR_Hold.'+side];origin=(inv@np.r_[base[index]+base_offset,1])[:3]-[0,rig.data.bones['mixamorig:Spine2'].length,0]
  for fc in anchor.animation_data.drivers:
   if fc.data_path=='location':fc.driver.expression=str(float(origin[fc.array_index]))+fc.driver.expression[fc.driver.expression.index('+v'):]
  gltf=lambda v:[float(v[0]),float(v[2]),float(-v[1])]
  anchor['surface_offset_contract']='pose-space-normal-v004';anchor['surface_rest_point']=gltf(base[index]);anchor['surface_offset_basis']=gltf(base_offset);anchor['surface_offset_deltas']=[x for k in ks[1:] for x in gltf(offsets[k.name])];anchor['purpose']='Radius .030 fixture; .031 along calibrated posed surface normal, interpolated with the same dense pose space. v004 loader required.'
  o.data.update();o.update_tag();print('ROOTED_PAW_COMPLETE',side,flush=True)
 b.reset(rig);return records
def build():
 bpy.ops.wm.open_mainfile(filepath=str(B/'shushu-v004-motion-gate-v003.blend'));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');o=bpy.data.objects['ShushuStatic_Head'];ks=o.data.shape_keys.key_blocks;put(ks['MouthClose'],coords(ks['Basis']));o.data.update();o.update_tag()
 report={'mouth':'Retire obsolete additive MouthClose chin displacement. MouthOpen arbitration already implements close priority. W/UV/texture unchanged.','rest_surfaces':rest_surface_cleanup(),'belly':belly(rig),'corrective_field':corrective_field(rig),'arms':arms(rig)}
 report['normals']=clear_stale_normals()
 b.reset(rig);bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));(D/'repair-authoring.json').write_text(json.dumps(report,indent=2));render_preview(rig)

def clear_stale_normals():
 rows=[]
 for name in ['Head','Torso','Paw_L','Paw_R','Ear_L','Ear_R']:
  o=bpy.data.objects['ShushuStatic_'+name];mesh=o.data;before=mesh.has_custom_normals
  if mesh.attributes.get('custom_normal'):mesh.attributes.remove(mesh.attributes['custom_normal'])
  if mesh.attributes.get('sharp_edge'):mesh.attributes.remove(mesh.attributes['sharp_edge'])
  mesh.update();mesh.calc_loop_triangles();p=np.array([v.co[:] for v in mesh.vertices]);tri=np.array([t.vertices[:] for t in mesh.loop_triangles]);_,ids=np.unique(np.round(p,6),axis=0,return_inverse=True);normal=np.zeros((ids.max()+1,3))
  a=p[tri[:,1]]-p[tri[:,0]];c=p[tri[:,2]]-p[tri[:,0]];face=np.cross(a,c);face/=np.maximum(1e-12,np.linalg.norm(face,axis=1))[:,None]
  for corner in range(3):
   e1=p[tri[:,(corner+1)%3]]-p[tri[:,corner]];e2=p[tri[:,(corner+2)%3]]-p[tri[:,corner]];angle=np.arctan2(np.linalg.norm(np.cross(e1,e2),axis=1),np.einsum('ij,ij->i',e1,e2));np.add.at(normal,ids[tri[:,corner]],face*angle[:,None])
  normal/=np.maximum(1e-12,np.linalg.norm(normal,axis=1))[:,None];mesh.normals_split_custom_set_from_vertices(normal[ids].tolist());mesh.update();rows.append({'mesh':o.name,'stale_custom_normals_before':before,'method':'Rebuilt angle-weighted normals from repaired actual triangles, welded across UV-equivalent points; geometry repair remains separate.'})
 return rows
def render_preview(rig):
 scene,cam=b.setup_review(640,8);scene.render.engine='BLENDER_EEVEE';cam.data.type='ORTHO';cam.data.ortho_scale=1.18
 states=[('neutral',{}),('hold',{'Hold.L':1,'Hold.R':1}),('seat-hold',{'Seat':1,'Hold.L':1,'Hold.R':1}),('seat-close',{'Seat':1,'Hold.L':1,'SelfContact.R':1,'MouthClose':1,'Blink.R':.7}),('self',{'SelfContact.L':1,'SelfContact.R':1}),('offer',{'Offer.L':1,'Offer.R':1})]
 for name,state in states:
  b.state(rig,state)
  for view,loc in {'3q':(-2,-2.5,.65),'side':(-3,0,.5),'front':(0,-3,.5)}.items():
   cam.location=loc;cam.rotation_euler=(Vector((0,0,.5))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(D/f'preview-{name}-{view}.png');bpy.ops.render.render(write_still=True)
if __name__=='__main__':
 if '--feature-lock-only' in sys.argv:
  bpy.ops.wm.open_mainfile(filepath=str(ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');o=bpy.data.objects['ShushuStatic_Head'];source=np.load(D/'source-diagnosis.npz');patch=np.load(D.parent/'muzzle-retopo.npz');rim=np.arange(34667+int(patch['outer_count']),34667+len(patch['boundary_ids']));p=source['ShushuStatic_Head__key__Basis'];_,ids=np.unique(np.round(p,6),axis=0,return_inverse=True);locked=np.isin(ids,np.unique(ids[rim]))
  for k in o.data.shape_keys.key_blocks:
   q=coords(k);q[locked]=source['ShushuStatic_Head__key__'+k.name][locked];put(k,q)
  q=np.array([v.co[:] for v in o.data.vertices]);q[locked]=source['ShushuStatic_Head__base'][locked];o.data.vertices.foreach_set('co',q.astype(np.float32).ravel());o.data.update();o.update_tag();report=json.loads((D/'repair-authoring.json').read_text());report['exact_feature_lock']={'W_boundary_vertices':len(rim),'including_UV_equivalents':int(locked.sum()),'error':0,'reason':'Protection must be exact after adjacency-group averaging.'};report['normals']=clear_stale_normals();b.reset(rig);bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));(D/'repair-authoring.json').write_text(json.dumps(report,indent=2))
 elif '--corrective-field-only' in sys.argv:
  bpy.ops.wm.open_mainfile(filepath=str(ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');report=json.loads((D/'repair-authoring.json').read_text());report['corrective_field']=corrective_field(rig);report['normals']=clear_stale_normals();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));(D/'repair-authoring.json').write_text(json.dumps(report,indent=2));render_preview(rig)
 elif '--arms-only' in sys.argv:
  bpy.ops.wm.open_mainfile(filepath=str(ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');report=json.loads((D/'repair-authoring.json').read_text());report['arms']=arms(rig);report['normals']=clear_stale_normals();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));(D/'repair-authoring.json').write_text(json.dumps(report,indent=2));render_preview(rig)
 elif '--normals-only' in sys.argv:
  bpy.ops.wm.open_mainfile(filepath=str(ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');report=json.loads((D/'repair-authoring.json').read_text());report['normals']=clear_stale_normals();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));(D/'repair-authoring.json').write_text(json.dumps(report,indent=2));render_preview(rig)
 else:build()
