"""Preserve approved feature coordinates/UV/images and audit the changed surface."""
import bpy,sys,json,importlib.util,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging';sys.dont_write_bytecode=True
source=(R/'scripts/blender/audit-shushu-motion-v003.py').read_text();prefix=source[:source.index('old,bones=')];scope={"__file__":str(R/"scripts/blender/audit-shushu-motion-v003.py")};exec(compile(prefix,'preservation_helpers','exec'),scope);old,bones=scope['snapshot'](B/'shushu-v004-motion-gate-v003.blend');new,newbones=scope['snapshot'](B/'shushu-v004-motion-gate-v004.blend');g=scope['g'];patch=np.load(D.parent/'muzzle-retopo.npz');rim=np.arange(34667+int(patch['outer_count']),34667+len(patch['boundary_ids']));rows=[]
for name,a in old.items():
 c=new[name];p=a['keys']['Basis'];q=c['keys']['Basis'];delta=q-p
 rows.append({'mesh':name,'topology_exact':a['topology']==c['topology'],'uv_exact':a['uv']==c['uv'],'weight_exact':a['weight']==c['weight'],'images_exact':a['images']==c['images'],'basis_delta_max':float(np.linalg.norm(delta,axis=1).max()),'basis_bounds_old':[p.min(0).tolist(),p.max(0).tolist()],'basis_bounds_new':[q.min(0).tolist(),q.max(0).tolist()],'key_names_exact':list(a['keys'])==list(c['keys']),'W_ring_count':len(rim) if name.endswith('_Head') else None,'W_all_keys_max_error':max(float(abs(a['keys'][k][rim]-c['keys'][k][rim]).max()) for k in a['keys']) if name.endswith('_Head') else None})
assert bones==newbones
assert all(r[k] for r in rows for k in ['topology_exact','uv_exact','weight_exact','images_exact','key_names_exact'])
assert all(r['W_all_keys_max_error']==0 for r in rows if r['W_ring_count']), 'Protected W coordinates must match exactly'
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');head=bpy.data.objects['ShushuStatic_Head'];ks=head.data.shape_keys.key_blocks;close_error=float(abs(g.r.coords(ks['MouthClose'])-g.r.coords(ks['Basis'])).max());assert close_error==0
sweep=[]
for phase in np.linspace(0,2,81):
 amount=float(phase if phase<=1 else 2-phase);state={'MouthOpen':amount,'MouthClose':0 if phase<=1 else 1-amount,'Tongue':amount*.4,'Smile':.4,'Joy':.2,'Hold.L':.6,'SelfContact.R':.5}
 g.r.b.state(rig,state);samples={}
 for name in ['ShushuStatic_Head','ShushuStatic_MouthInterior','ShushuStatic_OralBowl','ShushuStatic_Tongue']:
  o=bpy.data.objects.get(name)
  if o is None:continue
  q,n,t=g.evaluate(o,True);samples[name]={'finite':bool(np.isfinite(q).all()),'mouth_weights':{k.name:k.value for k in o.data.shape_keys.key_blocks if 'Mouth' in k.name or k.name=='Tongue'}}
 sweep.append({'phase':float(phase),'state':state,'samples':samples})
assert all(r['finite'] for x in sweep for r in x['samples'].values())
(D/'preservation-and-mouth.json').write_text(json.dumps({'meshes':rows,'bone_rest_and_parent_exact':True,'obsolete_close_equals_basis_error':close_error,'mouth_sweep':sweep,'limits':'Full W boundary, UV, texture bytes, weights and topology compared; rest surface fairing intentionally changes Basis. Finite samples and preserved coordinates do not grant Human visual GO or prove every continuous combination.'},indent=2));print('PRESERVATION_COMPLETE',[(r['mesh'],r['W_all_keys_max_error']) for r in rows if r['W_ring_count']],flush=True)
