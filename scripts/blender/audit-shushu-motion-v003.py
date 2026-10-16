"""Focused preservation + continuous aperture geometry audit."""
import bpy,sys,json,hashlib,importlib.util
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging';sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def sha(value):return hashlib.sha256(value).hexdigest()
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');g.r.b.reset(rig);out={}
 for o in bpy.data.objects:
  if o.type!='MESH' or not o.name.startswith('ShushuStatic_'):continue
  m=o.data;uv=np.array([v.uv[:] for v in m.uv_layers.active.data]) if m.uv_layers.active else np.zeros((0,2));keys={k.name:g.r.coords(k) for k in m.shape_keys.key_blocks} if m.shape_keys else {'Basis':np.array([v.co[:] for v in m.vertices])}
  m.calc_loop_triangles();out[o.name]={'keys':keys,'tri':np.array([t.vertices[:] for t in m.loop_triangles]),'tri_uv':np.array([[m.uv_layers.active.data[i].uv[:] for i in t.loops] for t in m.loop_triangles]) if m.uv_layers.active else np.zeros((len(m.loop_triangles),3,2)),'topology':sha(str([p.vertices[:] for p in m.polygons]).encode()),'uv':sha(uv.tobytes()),'weight':sha(str([[(g.group,g.weight) for g in v.groups] for v in m.vertices]).encode()),'weight_prefix':sha(str([[(g.group,g.weight) for g in v.groups] for v in list(m.vertices)[:38003]]).encode()),'images':[(n.image.name,sha(bytes(n.image.packed_file.data)) if n.image.packed_file else None) for mat in m.materials for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]}
 bones={b.name:(list(b.matrix_local),b.parent.name if b.parent else None) for b in rig.data.bones}
 return out,sha(str(bones).encode())
old,bones=snapshot(B/'shushu-v004-motion-gate-v002.blend');new,newbones=snapshot(B/'shushu-v004-motion-gate-v003.blend');patch=np.load(D.parent/'muzzle-retopo.npz');rim=np.arange(34667+int(patch['outer_count']),34667+len(patch['boundary_ids']));rows=[]
for name,a in old.items():
 b=new[name];head=name=='ShushuStatic_Head';paw=name.startswith('ShushuStatic_Paw_');errors={k:float(np.abs(a['keys'][k]-b['keys'][k][:len(a['keys'][k])]).max()) for k in (['Basis'] if paw else a['keys'])}
 rows.append({'mesh':name,'key_max_error':max(errors.values()),'all_keys_exact':all(v==0 for v in errors.values()),'topology_exact':a['topology']==b['topology'],'uv_exact':a['uv']==b['uv'],'weight_exact':a['weight']==b['weight'],'images_exact':a['images']==b['images'],'W_all_keys_max_error':max(float(np.abs(a['keys'][k][rim]-b['keys'][k][rim]).max()) for k in a['keys']) if head else None})
assert bones==newbones
assert all(r['all_keys_exact'] for r in rows if r['mesh']!='ShushuStatic_Head')
assert all(r[k] for r in rows if r['mesh']!='ShushuStatic_Head' for k in ['topology_exact','uv_exact','images_exact'])
assert all(r['weight_exact'] for r in rows if r['mesh']!='ShushuStatic_Head' and not r['mesh'].startswith('ShushuStatic_Paw_'))
assert all(r['images_exact'] for r in rows)
source_head=old['ShushuStatic_Head'];target_head=new['ShushuStatic_Head'];assert source_head['weight_prefix']==target_head['weight_prefix']
lookup={tuple(t):(uv) for t,uv in zip(target_head['tri'],target_head['tri_uv'])};unchanged_uv=0
for t,uv in zip(source_head['tri'],source_head['tri_uv']):
 if tuple(t) in lookup:assert np.array_equal(uv,lookup[tuple(t)]);unchanged_uv+=1
assert next(r for r in rows if r['mesh']=='ShushuStatic_Head')['W_all_keys_max_error']==0
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');head=bpy.data.objects['ShushuStatic_Head'];closed=new[head.name]['keys']['Basis'];cavity=new[head.name]['keys']['Corrective.MouthCavity'];sweep=[]
for t in np.linspace(0,1,101):
 g.r.b.state(rig,{'MouthOpen':float(t)});p,n,tri=g.evaluate(head,True);a,b,c=p[tri].transpose(1,0,2);cross=np.cross(b-a,c-a);center=(a+b+c)/3;mask=(abs(center[:,0])<.046)&(center[:,1]<-.23)&(center[:,2]>.565)&(center[:,2]<.622);area=np.linalg.norm(cross,axis=1);back=int(((cross[:,1]>1e-10)&mask).sum());sweep.append({'open':float(t),'finite':bool(np.isfinite(p).all()),'back_facing_local_triangles':back,'minimum_area2':float(area[mask].min())})
assert all(r['finite'] and r['back_facing_local_triangles']==0 for r in sweep)
report={'meshes':rows,'head_original_weight_prefix_exact':True,'head_retained_triangles_UV_exact':unchanged_uv,'head_upper_muzzle_original_exact_above_z_0630':all(np.array_equal(source_head['keys'][k][source_head['keys']['Basis'][:,2]>.630][:,:2],target_head['keys'][k][:38003][source_head['keys']['Basis'][:,2]>.630][:,:2]) for k in source_head['keys'] if k!='Corrective.MouthCavity'),'bone_rest_and_parent_exact':bones==newbones,'cavity_equals_basis_max_error':float(abs(cavity-closed).max()),'aperture_sweep':sweep,'scope':'preservation and local finite/orientation checks only; no Human appearance/collision approval'}
(D/'preservation-and-aperture.json').write_text(json.dumps(report,indent=2));print('AUDIT_PASS',max(r['back_facing_local_triangles'] for r in sweep),flush=True)
