"""Separate v003 candidate; geometry authoring and proof use the same repair."""
import bpy,sys,json,importlib.util,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
asset=B/'shushu-v004-motion-gate-v003.blend'
if '--build' in sys.argv:
 bpy.ops.wm.open_mainfile(filepath=str(B/'shushu-v004-motion-gate-v002.blend'));o=bpy.data.objects['ShushuStatic_Head'];d=np.load(D/'local-repair.npz');rows=[]
 for k in o.data.shape_keys.key_blocks:
  p=g.r.coords(k);q=p.copy()
  if k.name=='Corrective.MouthCavity':q=g.r.coords(o.data.shape_keys.key_blocks['Basis']).copy();q[:,1]-=d['muzzle_delta'];q[:,2]-=d['crown_delta']
  q[:,1]+=d['muzzle_open_delta' if k.name=='MouthOpen' else 'muzzle_delta'];q[:,2]+=d['crown_delta'];k.data.foreach_set('co',q.ravel());rows.append({'key':k.name,'changed':int((np.linalg.norm(q-p,axis=1)>1e-8).sum()),'max_delta':float(np.linalg.norm(q-p,axis=1).max()),'retired_exterior_cavity':k.name=='Corrective.MouthCavity'})
 o.data.update()
 if (D/'crown-retopo.npz').exists():
  assert json.loads((D/'crown-retopo.json').read_text())['planner_sha256']==hashlib.sha256((R/'scripts/3d/rebuild-shushu-crown-v003.py').read_bytes()).hexdigest(),'Stale crown plan'
  sp=importlib.util.spec_from_file_location('crown',R/'scripts/blender/apply-shushu-crown-retopo-v003.py');crown=importlib.util.module_from_spec(sp);sp.loader.exec_module(crown);report=crown.apply(o,np.load(D/'crown-retopo.npz'));(D/'crown-retopo-applied.json').write_text(json.dumps(report,indent=2))
 bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(asset));(D/'authored-repair.json').write_text(json.dumps(rows,indent=2))
elif '--export' in sys.argv:
 g.ASSET=asset;g.PROOF=asset.with_name(asset.stem+'-proof.blend');g.GLB=asset.with_suffix('.glb');g.OUT=D
 extra={1005:{'Hold.L':1,'Hold.R':1,'MouthOpen':.55},1017:{'Hold.L':1,'Hold.R':1,'MouthOpen':1,'Blink.L':.35},1029:{'Hold.L':1,'SelfContact.R':1,'MouthOpen':.2,'Blink.R':.7,'CheekPressure.R':.6},1041:{'Offer.L':.5,'Offer.R':.5,'MouthOpen':.55},1053:{'Offer.L':1,'Offer.R':1,'Wrist.L':1,'Wrist.R':-1},1065:{'SelfContact.L':.5,'SelfContact.R':.5},1077:{'SelfContact.L':1,'SelfContact.R':1},1089:{'Seat':.5,'Hold.L':.5,'Hold.R':.5,'MouthOpen':.55},1101:{'Seat':1,'Hold.L':1,'Hold.R':1,'MouthOpen':1},1113:{'Seat':1,'Hold.L':1,'SelfContact.R':1,'MouthClose':1,'Blink.R':.7},1125:{'Seat':1,'Hold.L':1,'Hold.R':1,'Tongue':1},1137:{'Seat':.5},1149:{}}
 g.proof(extra)
elif '--verify' in sys.argv:
 g.GLB=asset.with_suffix('.glb');g.OUT=D;g.verify()
elif '--render' in sys.argv or '--video' in sys.argv:
 g.PROOF=asset.with_name(asset.stem+'-proof.blend');g.GLB=asset.with_suffix('.glb');g.OUT=D;g.video() if '--video' in sys.argv else g.render()
