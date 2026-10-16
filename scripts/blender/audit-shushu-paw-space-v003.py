"""Cheap candidate probes before a full 1149-frame export."""
import bpy,sys,importlib.util,json,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging';sys.dont_write_bytecode=True
if '--proposal' in sys.argv:D=R/'output/playwright/shushu-v003/selfcontact-tangent'
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);b=g.r.b
old={}
for version in ['v002','v003']:
 source=D/'proposal.blend' if '--proposal' in sys.argv and version=='v003' else B/('shushu-v004-motion-gate-'+version+'.blend')
 bpy.ops.wm.open_mainfile(filepath=str(source));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
 for seat in [0,.5,1]:
  b.state(rig,{'Seat':seat})
  for side in ['L','R']:
   name='ShushuStatic_Paw_'+side;p=g.evaluate(bpy.data.objects[name]);key=(side,seat)
   if version=='v002':old[key]=p
   else:assert np.max(abs(p-old[key]))<1e-6,('Neutral/seat changed',key,np.max(abs(p-old[key])))
rows=[];states=[{}]
for side in ['L','R']:
 for mode in ['Hold','SelfContact','Offer']:
  for t in [.125,.375,.5,.625,.875,1]:
   for seat in [0,.5,1]:states.append({mode+'.'+side:t,'Seat':seat})
states += [{'Hold.L':1,'Hold.R':h,'SelfContact.R':1,'Seat':seat} for h in [.125,.375,.625,.875] for seat in [0,.5,1]]
states += [{**reach,'Wrist.L':w,'Wrist.R':-w} for reach in [{},{'Offer.L':1,'Offer.R':1}] for w in [-1,.5,1]]
states += [{'Hold.L':h,'Offer.L':.6,'SelfContact.L':c} for h,c in [(0,.5),(.25,.5),(.5,1),(.5,.5),(.75,.5)]]
if '--quick' in sys.argv:states=[{}, {'Seat':1}, *[{mode+'.L':t,mode+'.R':t,'Seat':seat} for mode in ['Hold','SelfContact','Offer'] for t in [.5,1] for seat in [0,1]], {'Hold.L':.5,'SelfContact.L':1,'Seat':1}]
for state in states:
 b.state(rig,state);tp,tt=b.evaluated(bpy.data.objects['ShushuStatic_Torso']);tree=BVHTree.FromPolygons(tp.tolist(),tt.tolist(),all_triangles=True);hp,ht=b.evaluated(bpy.data.objects['ShushuStatic_Head']);headtree=BVHTree.FromPolygons(hp.tolist(),ht.tolist(),all_triangles=True)
 span=float((bpy.data.objects['ANCHOR_Hold.L'].matrix_world.translation-bpy.data.objects['ANCHOR_Hold.R'].matrix_world.translation).length)
 for side in ['L','R']:
  o=bpy.data.objects['ShushuStatic_Paw_'+side];p,n,tri=g.evaluate(o,True);base=np.array([v.co[:] for v in o.data.vertices]);distal=np.where(abs(base[:,0])>.26)[0];penetration=[];confirmed=[];witness=[]
  for i in distal:
   co,no,_,distance=tree.find_nearest(Vector(p[i]))
   if co is not None and (Vector(p[i])-co).dot(no)<-1e-7:
    penetration.append(distance);votes=0
    for direction in [Vector((.923,.271,.273)).normalized(),Vector((-.311,.871,.38)).normalized(),Vector((.137,-.41,.902)).normalized()]:
     origin=Vector(p[i])+direction*1e-6;hits=0
     for attempt in range(30):
      hit,_,_,_=tree.ray_cast(origin,direction,2)
      if hit is None:break
      hits+=1;origin=hit+direction*1e-6
     votes+=hits%2
    if votes>=2:confirmed.append(distance);witness.append({'index':int(i),'depth_H':float(distance),'rest':base[i].tolist(),'world':p[i].tolist()})
  volume=lambda p:abs(float(np.einsum('ij,ij->i',p[tri[:,0]],np.cross(p[tri[:,1]],p[tri[:,2]])).sum()/6))
  anchor=bpy.data.objects['ANCHOR_Hold.'+side];index=int(anchor['surface_vertex']);error=float(np.linalg.norm(np.array(anchor.matrix_world.translation)-(p[index]+[0,-.031,0])))
  invalid=[fc.data_path for owner in [rig,o.data.shape_keys,anchor] if owner.animation_data for fc in owner.animation_data.drivers if not fc.driver.is_valid]
  proximal=np.where(abs(base[:,0])<np.quantile(abs(base[:,0]),.12))[0];rootinside=sum((Vector(p[i])-co).dot(no)<-1e-5 for i in proximal for co,no,_,_ in [tree.find_nearest(Vector(p[i]))] if co is not None);headnegative=[];headconfirmed=[]
  for i in distal:
   co,no,_,distance=headtree.find_nearest(Vector(p[i]))
   if co is not None and (Vector(p[i])-co).dot(no)<-1e-5:
    headnegative.append(distance);votes=0
    for direction in [Vector((.923,.271,.273)).normalized(),Vector((-.311,.871,.38)).normalized(),Vector((.137,-.41,.902)).normalized()]:
     origin=Vector(p[i])+direction*1e-6;hits=0
     for attempt in range(30):
      hit,_,_,_=headtree.ray_cast(origin,direction,2)
      if hit is None:break
      hits+=1;origin=hit+direction*1e-6
     votes+=hits%2
    if votes>=2:headconfirmed.append({'index':int(i),'depth_H':float(distance),'point':p[i].tolist()})
  pawtree=BVHTree.FromPolygons(p.tolist(),tri.tolist(),all_triangles=True);fixture_distance=float(pawtree.find_nearest(anchor.matrix_world.translation)[3])
  shoulder=rig.data.bones['mixamorig:'+('Left' if side=='L' else 'Right')+'Shoulder'];hand=rig.data.bones['mixamorig:'+('Left' if side=='L' else 'Right')+'Hand'];axis=np.array((hand.head_local-shoulder.head_local).normalized());along=(base-np.array(shoulder.head_local))@axis;tips=np.where(along>np.quantile(along,.8))[0]
  contact={name:min(float(target.find_nearest(Vector(p[i]))[3]) for i in tips) for name,target in [('Torso',tree),('Head',headtree)]}
  rows.append({'state':state,'side':side,'fixture_radius_003_clearance_H':fixture_distance-.030,'volume_proxy':volume(p)/volume(base),'distal_negative_side_count':len(penetration),'distal_max_negative_depth_H':float(max(penetration,default=0)),'confirmed_inside_vertices':len(confirmed),'confirmed_max_depth_H':float(max(confirmed,default=0)),'deepest_confirmed_torso_witness':max(witness,key=lambda x:x['depth_H'],default=None),'head_negative_side_vertices':len(headnegative),'head_max_negative_depth_H':float(max(headnegative,default=0)),'proximal_inside_torso_count':rootinside,'proximal_sample_count':len(proximal),'hold_anchor_span_H':span,'anchor_gap_error_H':error,'invalid_drivers':invalid})
  rows[-1]['tip_surface_clearance_H']=contact
  rows[-1]['head_confirmed_inside']=headconfirmed
report={'neutral_and_true_seat_paw_positions_max_error_H':'<1e-6','rows':rows,'limits':'Nearest signed surface is a penetration probe. Volume is an oriented triangle proxy, not a Human appearance gate; exact cross sections do not prove a natural bent silhouette.'};(D/'paw-space-probes.json').write_text(json.dumps(report,indent=2));print('PAW_PROBES',len(rows),'depth',max(x['distal_max_negative_depth_H'] for x in rows),'anchor',max(x['anchor_gap_error_H'] for x in rows),'volume_range',min(x['volume_proxy'] for x in rows),max(x['volume_proxy'] for x in rows),'invalid',sum(len(x['invalid_drivers']) for x in rows),flush=True)
