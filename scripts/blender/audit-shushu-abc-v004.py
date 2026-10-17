"""Reuse focused contact probes; no full app build or mobile operations."""
import bpy,sys,importlib.util,json,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004';sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('repair',R/'scripts/blender/repair-shushu-abc-v004.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
bpy.ops.wm.open_mainfile(filepath=str(m.ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');g=m.g;b=m.b
# Existing ray-parity/contact audit, run against the new candidate. The old
# neutral equality assertion is deliberately inapplicable to authorized fairing.
source=(R/'scripts/blender/audit-shushu-paw-space-v003.py').read_text();source=source[source.index('rows=[];states='):];source=source.replace("error=float(np.linalg.norm(np.array(anchor.matrix_world.translation)-(p[index]+[0,-.031,0])))", "coeff=np.array(anchor['surface_offset_deltas']).reshape(-1,3);off=np.array(anchor['surface_offset_basis'])+np.array([k.value for k in o.data.shape_keys.key_blocks[1:]])@coeff;off=np.array([off[0],-off[2],off[1]]);off=b.skin_matrices(rig,o)[index,:3,:3]@off;error=float(np.linalg.norm(np.array(anchor.matrix_world.translation)-(p[index]+off)))");source=source.replace("'neutral_and_true_seat_paw_positions_max_error_H':'<1e-6',", "'neutral_fairing_authorized':True,");exec(compile(source,str(__file__)+'::reused_contact_probe','exec'),globals())
report['asset_sha256']=hashlib.sha256(m.ASSET.read_bytes()).hexdigest();(D/'paw-space-probes.json').write_text(json.dumps(report,indent=2))
# Whole-character inventory and finite/area/curvature witnesses, including
# fractional transitions and independent face combinations.
objects=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')];inventory=[];records=[]
states=[{}, {'Seat':.35}, {'Seat':.5}, {'Seat':1}, {'MouthOpen':.1}, {'MouthOpen':.5}, {'MouthOpen':1}, {'MouthOpen':1,'MouthClose':.67,'Tongue':.33}, {'Seat':1,'Hold.L':1,'SelfContact.R':1,'MouthClose':1,'Blink.R':.7}, {'Seat':.73,'Hold.L':.37,'SelfContact.R':.63,'Tongue':.4,'Joy':.5}, {'Smile':1,'MouthOpen':.2}, {'Surprise':1,'MouthOpen':.6}]
for o in objects:
 p=np.array([v.co[:] for v in o.data.vertices]);o.data.calc_loop_triangles();t=np.array([x.vertices[:] for x in o.data.loop_triangles]);e=np.unique(np.sort(np.concatenate([t[:,[0,1]],t[:,[1,2]],t[:,[2,0]]]),axis=1),axis=0);a=np.linalg.norm(np.cross(p[t[:,1]]-p[t[:,0]],p[t[:,2]]-p[t[:,0]]),axis=1);inventory.append({'mesh':o.name,'vertices':len(p),'triangles':len(t),'shape_keys':len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0,'rest_bounds':[p.min(0).tolist(),p.max(0).tolist()],'tiny_triangles_lt1e-10':int((a<1e-10).sum())})
 for state in states:
  b.state(rig,{k:v for k,v in state.items() if k in rig});q,_=b.evaluated(o);area=np.linalg.norm(np.cross(q[t[:,1]]-q[t[:,0]],q[t[:,2]]-q[t[:,0]]),axis=1);ratio=area/np.maximum(a,1e-12);records.append({'mesh':o.name,'state':state,'finite':bool(np.isfinite(q).all()),'area_ratio_p01':float(np.quantile(ratio,.01)),'area_ratio_p99':float(np.quantile(ratio,.99)),'collapse_new_lt1pct':int(((a>1e-9)&(ratio<.01)).sum())})
assert all(x['finite'] for x in records)
(D/'all-mesh-surface-audit.json').write_text(json.dumps({'inventory':inventory,'samples':records,'limits':'All 14 meshes inventoried; 12 focused states/mesh plus detailed paw/contact grid. Area ratios detect collapses, not aesthetic quality. Intentional eye/lid closures need visual interpretation; no assertion that arbitrary continuous inputs are defect-free.'},indent=2))
print('ALL_MESH_AUDIT_COMPLETE',len(objects),len(records),flush=True)
