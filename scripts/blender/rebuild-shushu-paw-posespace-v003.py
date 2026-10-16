"""Stable carrier skin + bounded pose-space surfaces for the candidate paws.
Old inverse multi-bone correctives can amplify mixed controls. Evaluate the
volume-preserving donor, keep one rigid carrier, and interpolate actual surfaces.
Ordinary morph/skin channels bake to glTF; no Blender callback is needed.
"""
import bpy,numpy as np,json
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree

def apply(rig,g,D,self_contact=None):
 self_contact=self_contact or {'aim':(-.6,-.5,.35),'shift':(-.07,.095,.04)}
 b=g.r.b;carrier='mixamorig:Spine2';torso=bpy.data.objects['ShushuStatic_Torso'];records=[];samples={};anchor_samples={};collision_trees={}
 prefixes=('PawEffective.','PawSpace.','PawSpaceAnchor.','PawAnchorSum.')
 for key in list(rig.keys()):
  if key.startswith(prefixes):rig.driver_remove('["'+key+'"]');del rig[key]
 paws={side:bpy.data.objects['ShushuStatic_Paw_'+side] for side in ['L','R']}
 for o in paws.values():
  if o.data.shape_keys.animation_data:
   for fc in o.data.shape_keys.animation_data.drivers:fc.mute=True
  for k in o.data.shape_keys.key_blocks:k.value=0
  next(m for m in o.modifiers if m.type=='ARMATURE').use_deform_preserve_volume=True
 for side,o in paws.items():
  base=np.array([v.co[:] for v in o.data.vertices]);root=rig.data.bones['mixamorig:'+('Left' if side=='L' else 'Right')+'Shoulder'].head_local;hand=rig.data.bones['mixamorig:'+('Left' if side=='L' else 'Right')+'Hand'].head_local;axis=np.array((hand-root).normalized());u=(base-np.array(root))@axis/(hand-root).length;fade=b.smooth(.15,.65,u);distal=abs(base[:,0])>.26;anchor=bpy.data.objects['ANCHOR_Hold.'+side];index=int(anchor['surface_vertex']);samples[side]=[];anchor_samples[side]=[]
  for mode in ['Hold','SelfContact','Offer']:
   for t in np.arange(1,9)/8:
    for seat in [0,.5,1]:
     for wrist in [-1,0,1]:
      b.state(rig,{mode+'.'+side:float(t),'Seat':seat,'Wrist.'+side:wrist})
      matrix=np.array(rig.pose.bones[carrier].matrix@rig.data.bones[carrier].matrix_local.inverted());inv=np.linalg.inv(matrix)
      # The inherited IK endpoint crossed the seated torso during transitions.
      # Author a local purpose arc relative to the preserved body carrier.
      sign=1 if side=='L' else -1;aim={'Hold':(sign*.08,-.98,-.18),'SelfContact':(sign*self_contact['aim'][0],*self_contact['aim'][1:]),'Offer':(sign*.65,-.63,-.42)}[mode];goal=Vector(aim).normalized();full=Vector(axis).rotation_difference(goal);rotation=Matrix.Identity(3).to_quaternion().slerp(full,float(t));direction=np.array(rotation@Vector(axis));angle=float(np.arccos(np.clip(axis@direction,-1,1)));center_rest=base.mean(0);along=(base-center_rest)@axis;length=float(np.ptp(along));radial=base-center_rest-along[:,None]*axis
      # A curved centerline retains the short plush cross section. A rigid
      # swung donor made a long straight cylinder in the actual side view.
      if angle>1e-6:
       bend=(direction-axis*np.cos(angle))/np.sin(angle);normal=np.cross(axis,bend);theta=.7*t;initial=angle;startaxis=axis*np.cos(initial)+bend*np.sin(initial);startbend=-axis*np.sin(initial)+bend*np.cos(initial);beta=theta*along/length;cs=np.cos(beta)[:,None];sn=np.sin(beta)[:,None]
       center=center_rest+startaxis*(length*np.sin(beta)/theta)[:,None]+startbend*(length*(1-np.cos(beta))/theta)[:,None]
       cs0=np.cos(beta+initial)[:,None];sn0=np.sin(beta+initial)[:,None];rotated_radial=radial*cs0+np.cross(normal,radial)*sn0+normal*(radial@normal)[:,None]*(1-cs0);tangent=startaxis*cs+startbend*sn
       localtarget=center+rotated_radial
      else:localtarget=base.copy();tangent=np.broadcast_to(axis,base.shape).copy()
      twist=.35*wrist*b.smooth(.55,.9,u);radial=localtarget-(center if angle>1e-6 else center_rest+along[:,None]*axis);cs=np.cos(twist)[:,None];sn=np.sin(twist)[:,None];localtarget+=radial*(cs-1)+np.cross(tangent,radial)*sn+tangent*np.einsum('ij,ij->i',tangent,radial)[:,None]*(1-cs)
      shift={'Hold':(-sign*.06587,-.10,.005),'SelfContact':(sign*self_contact['shift'][0],*self_contact['shift'][1:]),'Offer':(sign*.025,-.07,0)}[mode];localtarget+=np.array(shift)*t
      p=(np.c_[localtarget,np.ones(len(base))]@matrix.T)[:,:3]
      if seat not in collision_trees:
       tp,tt=b.evaluated(torso);hp,ht=b.evaluated(bpy.data.objects['ShushuStatic_Head']);collision_trees[seat]=(BVHTree.FromPolygons(tp.tolist(),tt.tolist(),all_triangles=True),BVHTree.FromPolygons(hp.tolist(),ht.tolist(),all_triangles=True))
      tree,headtree=collision_trees[seat]
      # A coherent distal translation avoids flattening each colliding vertex
      # independently. The attachment fades smoothly into the unchanged root.
      need=0.
      for i in np.where(distal)[0]:
       co,_,_,_=tree.ray_cast(Vector((p[i,0],-1,p[i,2])),Vector((0,1,0)),2)
       if co is not None:need=max(need,float(p[i,1]-co.y+.002))
      # Translate the whole closed limb: a distal fade inflated its volume and
      # length. The closed proximal cap remains embedded in the shoulder.
      for i in np.where(distal)[0]:
       co,_,_,_=headtree.ray_cast(Vector((p[i,0],-1,p[i,2])),Vector((0,1,0)),2)
       if co is not None:need=max(need,float(p[i,1]-co.y+.002))
      need=max(0.,need);p[:,1]-=need
      local=(np.c_[p,np.ones(len(p))]@inv.T)[:,:3];samples[side].append((mode,float(t),seat,wrist,local-base));anchor_samples[side].append((mode,float(t),seat,wrist,(np.r_[p[index]+[0,-.031,0],1]@np.linalg.inv(np.array(rig.matrix_world@rig.pose.bones[carrier].matrix)).T)[:3]))
      records.append({'side':side,'mode':mode,'amount':float(t),'seat':seat,'wrist':wrist,'coherent_forward_clearance_H':need,'maximum_local_delta_H':float(np.linalg.norm(local-base,axis=1).max())})
  print('PAW_SURFACES_SAMPLED',side,flush=True)
 # A linear blend of two differently rotated plush surfaces loses volume.
 # Fit each sampled surface's rotation and add the midpoint rotation residual.
 # The correction vanishes at either mode endpoint and at neutral.
 for side,o in paws.items():
  base=np.array([v.co[:] for v in o.data.vertices]);centered=base-base.mean(0);lookup={(mode,t,seat,wrist):delta for mode,t,seat,wrist,delta in samples[side]};index=int(bpy.data.objects['ANCHOR_Hold.'+side]['surface_vertex']);b.reset(rig);rest_inverse=np.array(rig.data.bones[carrier].matrix_local.inverted());origin=(np.r_[base[index]+[0,-.031,0],1]@rest_inverse.T)[:3]
  for first,second in [('Hold','SelfContact'),('Hold','Offer'),('SelfContact','Offer')]:
   for t in np.arange(1,9)/8:
    for seat in [0,.5,1]:
     for wrist in [-1,0,1]:
      rotations=[]
      for mode in [first,second]:
       target=base+lookup[(mode,float(t),seat,wrist)];u,_,vh=np.linalg.svd(centered.T@(target-target.mean(0)));rotation=vh.T@u.T
       if np.linalg.det(rotation)<0:vh[-1]*=-1;rotation=vh.T@u.T
       rotations.append(rotation)
      qa,qb=[Matrix(r.tolist()).to_quaternion() for r in rotations];mid=np.array(qa.slerp(qb,.5).to_matrix());delta=centered@(mid-(rotations[0]+rotations[1])*.5).T;mode=first+'~'+second;samples[side].append((mode,float(t),seat,wrist,delta));anchor_samples[side].append((mode,float(t),seat,wrist,origin+rest_inverse[:3,:3]@delta[index]))
  root=np.array(rig.data.bones['mixamorig:'+('Left' if side=='L' else 'Right')+'Shoulder'].head_local);tip=np.array(rig.data.bones['mixamorig:'+('Left' if side=='L' else 'Right')+'Hand'].head_local);axis=(tip-root)/np.linalg.norm(tip-root);u=(base-root)@axis/np.linalg.norm(tip-root);radial=base-root-((base-root)@axis)[:,None]*axis
  for wrist in [-1,1]:
   twist=.35*wrist*b.smooth(.55,.9,u);cs=np.cos(twist)[:,None];sn=np.sin(twist)[:,None];delta=radial*(cs-1)+np.cross(axis,radial)*sn
   for seat in [0,.5,1]:samples[side].append(('NeutralWrist',0.,seat,wrist,delta));anchor_samples[side].append(('NeutralWrist',0.,seat,wrist,origin+rest_inverse[:3,:3]@delta[index]))
 # Install after both sides were sampled with the untouched donor skin.
 for side,o in paws.items():
  base=np.array([v.co[:] for v in o.data.vertices]);o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));[setattr(poly,'use_smooth',True) for poly in o.data.polygons];o.shape_key_clear();o.shape_key_add(name='Basis');b.weights_replace(o,[{carrier:1} for _ in base]);next(m for m in o.modifiers if m.type=='ARMATURE').use_deform_preserve_volume=False
  raw={}
  for mode,expr,variables in [('Hold','min(1,max(0,v))',{'v':'Hold.'+side}),('SelfContact','(1-h)*min(1,max(0,v))',{'h':'PawEffective.'+side+'.Hold','v':'SelfContact.'+side}),('Offer','(1-h)*(1-min(1,max(0,c)))*min(1,max(0,v))',{'h':'PawEffective.'+side+'.Hold','c':'SelfContact.'+side,'v':'Offer.'+side})]:
   prop=f'PawEffective.{side}.{mode}';b.prop(rig,prop);b.driver(rig,'["'+prop+'"]',rig,expr,variables);raw[mode]=prop
  amount='PawSpace.'+side+'.Amount';b.prop(rig,amount);b.driver(rig,'["'+amount+'"]',rig,'h+c+o',{'h':raw['Hold'],'c':raw['SelfContact'],'o':raw['Offer']})
  for number,(mode,t,seat,wrist,delta) in enumerate(samples[side]):
   # Keep expressions below Blender's driver string limit with computed mode
   # weights stored as ordinary rig properties, then bake them like other props.
   prop=f'PawSpace.{side}.{mode}';
   if prop not in rig:
    b.prop(rig,prop)
    if mode=='NeutralWrist':b.driver(rig,'["'+prop+'"]',rig,'1',{})
    elif '~' in mode:
     first,second=mode.split('~');b.driver(rig,'["'+prop+'"]',rig,'4*a*b/max(.000001,m*m)',{'a':raw[first],'b':raw[second],'m':amount})
    else:b.driver(rig,'["'+prop+'"]',rig,'a/max(.000001,m)',{'a':raw[mode],'m':amount})
   key=b.shape(o,f'PoseSpace.{mode}.{int(t*1000)}.S{seat}.W{wrist}',delta);b.driver(key,'value',rig,f'a*max(0,1-abs(m-{t})*8)*max(0,1-abs(s-{seat})*2)*max(0,1-abs(w-({wrist})))',{'a':prop,'m':amount,'s':'Seat','w':'Wrist.'+side})
  anchor=bpy.data.objects['ANCHOR_Hold.'+side];anchor.animation_data_clear();anchor.parent=rig;anchor.parent_type='BONE';anchor.parent_bone=carrier;anchor.matrix_parent_inverse=Matrix.Identity(4);anchor.rotation_euler=(0,0,0);anchor.scale=(1,1,1)
  # A bone-parented object has its origin at the parent's tail in Blender.
  tail=np.array([0,rig.data.bones[carrier].length,0]);b.reset(rig);rest=anchor.location.copy()
  # Anchor drivers reuse exactly the surface basis coefficients. Each index is
  # a calibrated distal vertex; the offset is 31mm forward in world space.
  b.state(rig,{});p=g.evaluate(o);index=int(anchor['surface_vertex']);origin=(np.r_[p[index]+[0,-.031,0],1]@np.linalg.inv(np.array(rig.matrix_world@rig.pose.bones[carrier].matrix)).T)[:3]-tail
  anchor.location=origin
  for number,((mode,t,seat,wrist,position),key) in enumerate(zip(anchor_samples[side],list(o.data.shape_keys.key_blocks)[1:])):
   prop=f'PawSpaceAnchor.{side}.{number}';b.prop(rig,prop);fc=next(x for x in o.data.shape_keys.animation_data.drivers if x.data_path==key.path_from_id('value'));b.driver(rig,'["'+prop+'"]',rig,fc.driver.expression,{v.name:v.targets[0].data_path[2:-2] for v in fc.driver.variables})
  # Group terms to keep expressions within the driver's length limit.
  for component in range(3):
   groups=[]
   for start in range(0,len(anchor_samples[side]),12):
    prop=f'PawAnchorSum.{side}.{component}.{start}';rows=anchor_samples[side][start:start+12];b.prop(rig,prop,minimum=-1,maximum=1);b.driver(rig,'["'+prop+'"]',rig,'+'.join(f'({position[component]-tail[component]-origin[component]:.8g})*{chr(97+j)}' for j,(*_,position) in enumerate(rows)),{chr(97+j):f'PawSpaceAnchor.{side}.{start+j}' for j in range(len(rows))});groups.append(prop)
   b.driver(anchor,'location',rig,str(float(origin[component]))+'+'+'+'.join('v'+str(j) for j in range(len(groups))),{'v'+str(j):prop for j,prop in enumerate(groups)},component)
 b.reset(rig);(D/'paw-posespace-authoring.json').write_text(json.dumps({'method':'Single Spine2 carrier; arc centerline with transported original plush cross sections; old inverse-LBS corrective stack retired; coherent distal clearance; continuous bounded purpose arbitration; same coefficients on calibrated Hold anchors. Surface samples at 1/8 reach, Seat 0/0.5/1, Wrist -1/0/1. All ordinary drivers bake to morph/anchor channels.','samples':records,'gate':'PREVIEW_PENDING','limits':'Independent arm FK and unsampled arbitrary control combinations require separate validation; original neutral topology/UV/texture retained.'},indent=2));print('PAW_POSESPACE_APPLIED',flush=True)

if __name__=='__main__':
 import sys,importlib.util
 from pathlib import Path
 sys.dont_write_bytecode=True;R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';asset=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v003.blend'
 sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);bpy.ops.wm.open_mainfile(filepath=str(asset));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');apply(rig,g,D);bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(asset))
