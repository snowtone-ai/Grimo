"""Locality and saved expression/return verification for the lower mouth edit."""
import sys
sys.dont_write_bytecode=True
import bpy,json,importlib.util
from pathlib import Path
import numpy as np
def module(name,file):
 spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
l=module('lower','refine-shushu-v003-lower-mouth.py');c=module('checks','verify-shushu-v003-muzzle.py')
c.a=l.a;c.r=l.r;c.v=l.v;c.m=l;l.profile=l.n.m.profile
def compare(path):
 before=c.saved_snapshot(l.BACK/path.name);after=c.saved_snapshot(path)
 assert before['actions']==after['actions'] and before['objects'].keys()==after['objects'].keys()
 for name,old in before['objects'].items():
  assert old['structure']==after['objects'][name]['structure'],name
  if name not in ['Shushu_Head','Shushu_MouthInterior']:assert old['geometry']==after['objects'][name]['geometry'],name
 # Read saved coordinate arrays for both edited objects, never a transient preview.
 arrays=[]
 for p in [l.BACK/path.name,path]:
  l.a.load(p);arrays.append({name:{k.name:c.coords(k) for k in bpy.data.objects[name].data.shape_keys.key_blocks} for name in ['Shushu_Head','Shushu_MouthInterior']})
 result={}
 for name,old in arrays[0].items():
  new=arrays[1][name];rows={};basis=old['Basis'];mask=np.zeros(len(basis),bool)
  for key in old:
   permitted=key in ['MouthOpen','MouthDonorOpen'] or (key.startswith('Corrective.Compose.') and key.endswith(('.MouthOpen','.MouthDonorOpen')))
   if not permitted:assert np.array_equal(old[key],new[key]),(name,key)
   error=new[key]-old[key];ids=np.flatnonzero(np.max(np.abs(error),axis=1)>1e-9)
   if key in ['MouthOpen','MouthDonorOpen']:
    assert np.array_equal(new[key][:,[0,2]],old[key][:,[0,2]])
    assert np.all(error[:,1]>=-1e-8)
    if name=='Shushu_Head':
     b=basis[ids];assert np.all(np.abs(b[:,0])<.074) and np.all((b[:,2]>.525)&(b[:,2]<.601)) and np.all(b[:,1]<-.180)
    mask[ids]=True
   if len(ids):rows[key]={'vertices':len(ids),'max_difference':float(np.max(np.abs(error)))}
  # Recreate the edit from the baseline and compare every key, including rotated correctives.
  result[name]={'changed_keys':rows,'changed_source_vertices':int(mask.sum()),'neutral_and_other_expressions_exact':True,'opening_xz_exact':True}
 l.a.load(l.BACK/path.name);l.refine()
 for name,new in arrays[1].items():
  for key in bpy.data.objects[name].data.shape_keys.key_blocks:
   assert np.max(np.abs(c.coords(key)-new[key.name]))<1e-7,(name,key.name,'saved differs from intended local edit')
 return {'all_actions_topology_controls_modifiers_weights_identical':True,'other_objects_all_shapes_exact':True,'local_edits':result}
def surfaces():
 rows=[]
 for state in ['neutral','small','full','smile']:
  records=[]
  for path in [l.BACK/l.v.ASSET.name,l.v.ASSET]:
   l.a.load(path);l.a.pose(state);records.append({name:c.fixed_surface(bpy.data.objects[name]) for name in ['Shushu_Head','Shushu_MouthInterior']})
  result={'state':state,'objects':{}}
  for name,(old,tris) in records[0].items():
   new,nt=records[1][name];assert np.array_equal(tris,nt) and np.isfinite(new).all()
   on=np.cross(old[tris[:,1]]-old[tris[:,0]],old[tris[:,2]]-old[tris[:,0]]);nn=np.cross(new[tris[:,1]]-new[tris[:,0]],new[tris[:,2]]-new[tris[:,0]])
   collapsed=int(np.sum((np.linalg.norm(on,axis=1)>1e-10)&(np.linalg.norm(nn,axis=1)<1e-12)))
   useful=np.abs(on[:,1])>1e-10;flips=int(np.sum(on[useful,1]*nn[useful,1]<0))
   assert collapsed==0 and flips==0
   xz=float(np.max(np.abs(old[:,[0,2]]-new[:,[0,2]])));assert xz<1e-7
   result['objects'][name]={'new_collapsed_triangles':collapsed,'front_projected_winding_changes':flips,'evaluated_xz_max_error':xz}
  rows.append(result)
 return rows
def main():
 report={'base':l.BASE,'Human':'PENDING','Tripo':'HOLD','saved':{p.name:compare(p) for p in [l.v.ASSET,l.v.PROOF]}}
 report['surface']=surfaces();report['expressions']=c.expressions();report['proof']=c.proof_returns()
 inputs=json.loads((l.BACK/'inputs.json').read_text());outputs={p.relative_to(l.ROOT).as_posix() for p in [l.v.ASSET,l.v.PROOF,l.v.STATIC.with_suffix('.fbx'),l.v.STATIC.with_suffix('.glb')]}
 protected={p:h for p,h in inputs.items() if p not in outputs};assert all(l.sha(l.ROOT/p)==h for p,h in protected.items())
 report['protected_inputs_unchanged']=len(protected);l.write('protected-inputs.json',protected);l.write('targeted-checks.json',report);print('LOWER_MOUTH_CHECKS_COMPLETE',flush=True)
if __name__=='__main__':main()
