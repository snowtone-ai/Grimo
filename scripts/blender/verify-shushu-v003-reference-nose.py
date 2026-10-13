"""Saved-file checks focused on the new nose and preserved v003 functions."""
import sys
sys.dont_write_bytecode=True
import bpy,json,importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector,Quaternion
def module(name,file):
 spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file));value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
n=module('reference_nose','refine-shushu-v003-reference-nose.py')
c=module('previous_checks','verify-shushu-v003-muzzle.py')
c.m=n;c.a=n.a;c.r=n.r;c.v=n.v;n.profile=n.m.profile
original_snapshot=c.saved_snapshot
inventories=[]
def snapshot(path):
 result=original_snapshot(path);names=set(result['objects']);current=path.parent!=n.BACK
 if current:
  assert 'Shushu_Nose' in names
  inventories.append({'file':path.name,'new_object':'Shushu_Nose','total_character_and_donor_objects':len(names)})
  result['objects'].pop('Shushu_Nose')
 else:assert 'Shushu_Nose' not in names
 return result
c.saved_snapshot=snapshot
def nose_binding(path):
 n.a.load(path);head=n.v.parts['Head'];nose=bpy.data.objects['Shushu_Nose'];hk=head.data.shape_keys.key_blocks;nk=nose.data.shape_keys.key_blocks
 assert list(hk.keys())==list(nk.keys())
 assert c.drivers(head.data.shape_keys)==c.drivers(nose.data.shape_keys)
 ha=head.data.shape_keys.animation_data;na=nose.data.shape_keys.animation_data
 assert ((ha.action.name,ha.action_slot.identifier) if ha and ha.action else None)==((na.action.name,na.action_slot.identifier) if na and na.action else None)
 triangles=json.loads(nose['HeadAnchorTriangles']);weights=json.loads(nose['HeadAnchorWeights'])
 hbase=c.coords(hk['Basis']);base=c.coords(nk['Basis']);errors={}
 for name in hk.keys():
  if name.startswith(('Head','Corrective.Compose.')):continue
  hd=c.coords(hk[name])-hbase;expected=np.array([sum((w*hd[j] for j,w in zip(tri,ws)),np.zeros(3)) for tri,ws in zip(triangles,weights)])
  error=float(np.max(np.abs(c.coords(nk[name])-base-expected)));assert error<1e-7,(name,error);errors[name]=error
 pivot=np.array((0,.02,.52));composition_error={}
 poses=[('HeadTurn.L',(0,0,1),22),('HeadTurn.R',(0,0,1),-22),('HeadTilt.L',(0,1,0),12),('HeadTilt.R',(0,1,0),-12),('HeadRest',(1,0,0),10)]
 for name,axis,angle in poses:
  rotation=np.array(Quaternion(axis,np.deg2rad(angle)).to_matrix());expected=(base-pivot)@rotation.T+pivot
  error=float(np.max(np.abs(c.coords(nk[name])-expected)));assert error<2e-7;composition_error[name]=error
  for key in nk:
   prefix='Corrective.Compose.'+name+'.'
   if not key.name.startswith(prefix):continue
   delta=c.coords(nk[key.name[len(prefix):]])-base;expected=base+delta@rotation.T-delta
   error=float(np.max(np.abs(c.coords(key)-expected)));assert error<2e-7;composition_error[key.name]=error
 edge_use={}
 for polygon in nose.data.polygons:
  for i,j in zip(polygon.vertices,list(polygon.vertices[1:])+[polygon.vertices[0]]):
   edge=tuple(sorted((i,j)));edge_use[edge]=edge_use.get(edge,0)+1
 assert all(value==2 for value in edge_use.values())
 verts,tris=c.fixed_surface(nose);area=np.linalg.norm(np.cross(verts[tris[:,1]]-verts[tris[:,0]],verts[tris[:,2]]-verts[tris[:,0]]),axis=1)
 assert np.isfinite(verts).all() and np.min(area)>1e-12
 count=nose['CapVertexCount'];cap=base[:count]
 return {'object':'Shushu_Nose','keys_drivers_and_action_match_head':True,'closed_surface_edges':len(edge_use),'new_collapsed_triangles':0,
  'source_cap_bounds':[cap.min(0).tolist(),cap.max(0).tolist()], 'source_cap_width':float(np.ptp(cap[:,0])),'source_cap_height':float(np.ptp(cap[:,2])),
  'relative_binding_errors':errors,'composition_errors':composition_error,'diagnostic_colour_saved_as_final_texture':False}
def surface():
 n.a.load(n.BACK/n.v.ASSET.name);before,tris=c.fixed_surface(n.v.parts['Head'])
 n.a.load(n.v.ASSET);after,at=c.fixed_surface(n.v.parts['Head']);assert np.array_equal(tris,at)
 old=np.cross(before[tris[:,1]]-before[tris[:,0]],before[tris[:,2]]-before[tris[:,0]]);new=np.cross(after[tris[:,1]]-after[tris[:,0]],after[tris[:,2]]-after[tris[:,0]])
 collapsed=int(np.sum((np.linalg.norm(old,axis=1)>1e-10)&(np.linalg.norm(new,axis=1)<1e-12)))
 useful=np.abs(old[:,1])>1e-10;flips=int(np.sum(old[useful,1]*new[useful,1]<0));xz=float(np.max(np.abs(after[:,[0,2]]-before[:,[0,2]])))
 assert collapsed==0 and flips==0 and xz<1e-7
 return {'head_new_collapsed_triangles':collapsed,'head_front_projection_orientation_changes':flips,'head_evaluated_xz_max_error':xz}
def interaction_poses():
 n.a.load(n.v.ASSET);rows=[]
 for state in ['neutral','small','full','smile','happy-closed','half','companion']:
  n.a.pose(state)
  if state in ['small','full']:n.v.key('HeadTilt.R',.4)
  if state=='happy-closed':n.v.sit(.5);n.v.key('HeadTurn.L',.3)
  surface=n.v.tree(n.v.parts['Head']);nose=bpy.data.objects['Shushu_Nose'];positions,_=n.v.evaluated(nose)
  assert np.isfinite(positions).all()
  # Attachments are sampled on the saved cage. Check their transformed
  # positions lie close to the subdivided head, including seat/turn/open.
  head=n.v.parts['Head'];flags=[(modifier,modifier.show_viewport) for modifier in head.modifiers]
  for modifier,flag in flags:modifier.show_viewport=False
  bpy.context.view_layer.update();evaluated_head=head.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated_head.to_mesh();points=np.array([p.co[:] for p in mesh.vertices]);evaluated_head.to_mesh_clear()
  assert len(points)==len(head.data.vertices)
  for modifier,flag in flags:modifier.show_viewport=flag
  bpy.context.view_layer.update()
  bindings=json.loads(nose['HeadAnchorTriangles']);weights=json.loads(nose['HeadAnchorWeights']);distances=[]
  for i in range(0,len(bindings),24):
   point=sum((float(w)*Vector(points[j]) for j,w in zip(bindings[i],weights[i])),Vector())
   hit,normal,face,distance=surface.find_nearest(point);distances.append(distance)
  # The cage is intentionally coarser than the rendered head; this is an
  # attachment proximity diagnostic, not a cuteness or exact-contact PASS.
  rows.append({'state':state,'finite_nose_surface':True,'sampled_head_cage_to_render_max_distance':max(distances)})
 return rows
def main():
 report={'base':n.BASE,'Human':'PENDING','Tripo':'HOLD','saved_assets':{},'nose_binding':{},'profile_scope':'Saved asset profile arrays refer to the original Head surface only. The added nose cap bounds and dimensions are in nose_binding.'}
 for path in [n.v.ASSET,n.v.PROOF]:
  report['saved_assets'][path.name]=c.compare(path);report['nose_binding'][path.name]=nose_binding(path)
 report['inventory']=inventories;report['surface']=surface();report['mouth_rays']=c.expressions();report['proof']=c.proof_returns();report['nose_pose_checks']=interaction_poses()
 inputs=json.loads((n.BACK/'inputs.json').read_text());outputs={p.relative_to(n.ROOT).as_posix() for p in [n.v.ASSET,n.v.PROOF,n.v.STATIC.with_suffix('.fbx'),n.v.STATIC.with_suffix('.glb')]};protected={p:h for p,h in inputs.items() if p not in outputs}
 assert all(n.sha(n.ROOT/p)==h for p,h in protected.items());report['protected_inputs_preserved']=len(protected);n.write('protected-inputs.json',protected);n.write('targeted-checks.json',report)
 print('REFERENCE_NOSE_TARGETED_CHECKS_COMPLETE',flush=True)
if __name__=='__main__':main()
