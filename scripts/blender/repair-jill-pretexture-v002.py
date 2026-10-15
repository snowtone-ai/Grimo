"""Local derivative of Jill v001. Never overwrites source assets or old evidence.

Preserves skeleton/semantic controls/anchors. Consolidates the two physical lid
patches into the body so the same 20 morphs can also recess eyes and soften sockets.
"""
import bpy, json, math, hashlib, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'assets/grimo/production/jill/tripo/rig-other-v001'
A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-v002';A.mkdir(exist_ok=True)
E=ROOT/'docs/production/jill/rig-pretexture-v002';(E/'renders').mkdir(parents=True,exist_ok=True)
OE=ROOT/'docs/production/jill/rig-other-v001'
def write(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
bpy.ops.wm.open_mainfile(filepath=str(OLD/'jill-rig-other-v001.blend'))
s=bpy.context.scene;r=bpy.data.objects['JILL_RIG'];old=bpy.data.objects['Jill_Body']
contract=json.loads((OE/'control-contract.json').read_text());channels=list(contract['authoring_properties'])
r.animation_data.action=None
for k in channels:r[k]=0.
r.pose.bones['DEF_pelvis'].location=(0,0,0)
r.update_tag();bpy.context.view_layer.update()
v=np.array([tuple(x.co) for x in old.data.vertices]);original_v=v.copy();N=len(v)
comp=np.load(OE/'authority-parts.npz')['component']
keys={k.name:np.array([tuple(x.co) for x in k.data]) for k in old.data.shape_keys.key_blocks}
keynames=list(keys)+['FACE_Blink.L','FACE_Blink.R']
keydata={k:[p.copy() for p in keys.get(k,v)] for k in keynames}
polys=[list(p.vertices) for p in old.data.polygons]
uvs=[[list(old.data.uv_layers[0].data[i].uv) for i in p.loop_indices] for p in old.data.polygons]
weights=[{old.vertex_groups[g.group].name:g.weight for g in x.groups} for x in old.data.vertices]
norm=np.array([tuple(x.normal) for x in old.data.vertices])
groupnames=[g.name for g in old.vertex_groups]
matids=[0]*len(polys);regions=['original']*len(polys)
report={'source_sha256':hashlib.sha256((OLD/'jill-rig-other-v001.blend').read_bytes()).hexdigest(),
 'inherited_head':'379fe79ac2561b9a5796a4657c36d503d248cf04','plan_commit':'202eae9',
 'method':'Local geometry/shape/weights derivative; no remesh or regeneration','local_changes':[]}

# Preserve v002 UV verbatim in a second layer. The active Texture atlas applies
# one reversible uniform affine packing to inherited islands and adds a strip.
# Original islands are fragmented across the entire tile (47% coverage, no useful
# padded rectangle), so inserting full eyelids into the old tile is unsafe.
sourceuvs=[[list(q) for q in p] for p in uvs]
uvs=[[[.006+.88*q[0],.006+.88*q[1]] for q in p] for p in uvs]
atlas=[]
def uvrect(rect,u,w):return [rect[0]+u*rect[2],rect[1]+w*rect[3]]
def addvertex(coords,owner='DEF_head',shape=None):
 i=len(weights);weights.append({owner:1.})
 for k in keynames:keydata[k].append(np.array(shape.get(k,coords) if shape else coords,dtype=float))
 return i
def face(ids,uv,mat,region):polys.append(ids);uvs.append(uv);matids.append(mat);regions.append(region)

# Fixed-boundary local facial grafts, preserving the inherited exterior.
sys.path.insert(0,str(Path(__file__).parent))
from jill_pretexture_face_v002 import repair_face
polys,uvs,matids,regions,origins,atlas=repair_face(v,comp,norm,r,keydata,keynames,polys,uvs,matids,regions,weights,report)

# Smooth only the original shoulder/root weight transition, preserving neutral.
# Neck leaf roots blend into their owner; tips retain independent leaf bones.
leafmods=[]
for item in json.loads((OE/'build-report.json').read_text())['leaves']:
 ci=item['component'];ids=np.flatnonzero(comp==ci);bone=item['bone'];owner=item['owner'];b=r.data.bones[bone]
 axis=np.array(b.tail_local-b.head_local);axis/=np.linalg.norm(axis)
 along=(v[ids]-np.array(b.head_local))@axis;length=(b.tail_local-b.head_local).length
 if item['region']=='neck' or item['region']=='tail':
  u=smooth(.03,.45,along/max(length,1e-6))
  for i,w in zip(ids,u):weights[i]={owner:float(1-w),bone:float(w)}
  leafmods.append({'component':ci,'root_owner':owner,'root_follow_blend':True})
# Clamp fold to the documented safe posterior sweep and distribute its turn.
# Source wings are separate surfaces, with the inner root owned by the chest.
for side,sgn,cis in [('L',1,[2,4]),('R',-1,[1])]:
 ids=np.flatnonzero(np.isin(comp,cis));q=v[ids];root=smooth(.045,.125,abs(q[:,0]));outer=smooth(.19,.34,abs(q[:,0]));mem=smooth(-.01,.14,q[:,1])*.30
 for i,a,b,c in zip(ids,root,outer,mem):
  weights[i]={'DEF_chest':float(1-a),f'DEF_wing_root.{side}':float(a*(1-b)),f'DEF_wing_outer.{side}':float(a*b*(1-c)),f'DEF_wing_membrane.{side}':float(a*b*c)}
 # Existing quaternion drivers are preserved except the bounded fold angle.
 bn=f'DEF_wing_root.{side}'
 for f in r.animation_data.drivers:
  if f.data_path.startswith('pose.bones["'+bn+'"].rotation_quaternion'):
   f.driver.expression=f.driver.expression.replace('.48*min(w,0)','.30*min(w,0)')
 # Root corrective authored for old weighting is reduced pending visual proof.
 for k in ['COR_WingFold.'+side,'COR_WingOpen.'+side]:
  d=np.array(keydata[k][:N])-v;keydata[k][:N]=list(v+d*.5)
report['local_changes'].append({'roots':{'leaf_root_blends':leafmods,'wing_fold_root_radians':.30,'weights': 'chest->root->outer/membrane smooth local transition; no cross-side influences'}})

# Reconstruct a single morphable surface, with original vertices first and exact
# original loop UVs for retained faces. New UV islands occupy empty original space.
mesh=bpy.data.meshes.new('Jill_Pretexture_LocalSurface_v002');mesh.from_pydata(keydata['Basis'],[],polys);mesh.update()
body=bpy.data.objects.new('Jill_Pretexture_Body',mesh);s.collection.objects.link(body);body.parent=r
uv=mesh.uv_layers.new(name='Tripo_Input_UV')
for p,coords in zip(mesh.polygons,uvs):
 for li,co in zip(p.loop_indices,coords):uv.data[li].uv=co
sourceuv=mesh.uv_layers.new(name='v002_Source_UV_Preserved')
for p,originalpi in zip(mesh.polygons,origins):
 coords=sourceuvs[originalpi] if originalpi is not None else [list(uv.data[li].uv) for li in p.loop_indices]
 for li,co in zip(p.loop_indices,coords):sourceuv.data[li].uv=co
mesh.uv_layers.active_index=0;uv.active_render=True
import bmesh
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();mesh.update()
# Repair a donor degenerate UV triangle in the reserved inter-atlas gutter.
# The exact inherited UV remains in the second layer.
mesh.calc_loop_triangles();uvrepairs=[]
for tri in mesh.loop_triangles:
 q=np.array([tuple(uv.data[li].uv) for li in tri.loops]);a=q[1]-q[0];d=q[2]-q[0]
 if abs(a[0]*d[1]-a[1]*d[0])<2e-12:
  x=.894;y=.935+.009*len(uvrepairs)
  for li,p in zip(tri.loops,[(x,y),(x+.006,y),(x+.003,y+.006)]):uv.data[li].uv=p
  uvrepairs.append({'polygon':tri.polygon_index,'loops':list(tri.loops),'original_active_uv':q.tolist(),'replacement_bounds':[x,y,.006,.006]})
report['local_uv_repairs']=uvrepairs
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.78
 return m
for m in [mat('Jill_Clay_Skin',(.59,.69,.53)),mat('Jill_Clay_Eye',(.022,.048,.030)),mat('Jill_Clay_Oral',(.16,.026,.037)),mat('Jill_Clay_Tongue',(.58,.19,.22)),mat('Jill_Clay_Teeth',(.88,.86,.72))]:mesh.materials.append(m)
for p,mi,region in zip(mesh.polygons,matids,regions):
 p.use_smooth=True;p.material_index=mi
 if region=='original':
  if comp[p.vertices[0]] in [98,99]:p.material_index=1
  q=np.mean(v[list(p.vertices)],axis=0)
for name in keynames:
 k=body.shape_key_add(name=name);k.data.foreach_set('co',np.array(keydata[name],dtype=np.float32).ravel())
for src in old.data.shape_keys.animation_data.drivers:
 k=body.data.shape_keys.driver_add(src.data_path);k.driver.type='SCRIPTED';k.driver.expression=src.driver.expression
 for var in src.driver.variables:
  n=k.driver.variables.new();n.name=var.name;n.type=var.type
  for a,b in zip(n.targets,var.targets):a.id=b.id;a.data_path=b.data_path
for side in ['L','R']:
 k=mesh.shape_keys.key_blocks['FACE_Blink.'+side];fc=k.driver_add('value');fc.driver.expression='min(max(b,0),1)';fc.driver.type='SCRIPTED'
 var=fc.driver.variables.new();var.name='b';var.type='SINGLE_PROP';var.targets[0].id=r;var.targets[0].data_path='["blink.'+side+'"]'
for name in groupnames:body.vertex_groups.new(name=name)
for i,ws in enumerate(weights):
 total=sum(ws.values())
 for name,w in ws.items():
  if w>1e-7:body.vertex_groups[name].add([i],w/total,'REPLACE')
mod=body.modifiers.new('Jill export LBS','ARMATURE');mod.object=r;mod.use_deform_preserve_volume=False
for ob in [old]+[bpy.data.objects.get('Jill_Lids.'+side) for side in ['L','R']]:
 if ob:bpy.data.objects.remove(ob,do_unlink=True)
body.name='Jill_Body'
for k in body.data.shape_keys.key_blocks:k.value=0
body['basis_contract']='All 28050 inherited Basis vertices exact. Local deep oral faces removed; new 3D lid/lip/cavity/tongue surfaces documented. No exterior boundary fairing in delivered version.'
body['texture_status']='Inspection clay only, no generated Texture. Active UV=.006+.88*source UV for inherited faces, new strip for additions. Exact source UV retained in second layer.'
r['status']='PRETEXTURE_IMPLEMENTED_REPAIR_REVIEW / HOLD: facial collars require further sculpting; Human PENDING'
r['pretexture_plan_commit']='202eae9';r['fold_limit']='wing_open=-1: bounded .30 rad root fold; not fully body-hugging storage'
s.frame_start=1;s.frame_end=1;s.frame_set(1);r.update_tag();bpy.context.view_layer.update()
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100
s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(A/'jill-rig-pretexture-v002.blend'))
assert len(r.data.bones)==130 and len(channels)==39 and len(mesh.shape_keys.key_blocks)-1==20
assert len([o for o in s.objects if o.name.startswith('ANCHOR_')])==16
report.update({'vertices':len(mesh.vertices),'polygons':len(mesh.polygons),'bones':130,'semantic_channels':39,'morphs':keynames[1:],'anchors':16,
 'original_vertices':N,'original_basis_max_delta':float(np.linalg.norm(np.array(keydata['Basis'][:N])-original_v,axis=1).max()),'original_basis_changed_vertices':int(np.count_nonzero(np.linalg.norm(np.array(keydata['Basis'][:N])-original_v,axis=1)>1e-8)),
 'retained_original_polygons':len(polys)-len([x for x in regions if x!='original']),
 'new_uv_islands':atlas,'source_uv_occupancy_512':.4676437378,
 'texture_uv_repacking':{'scale':.88,'offset':[.006,.006],'inverse':'source=(texture-.006)/.88','original_layer':'v002_Source_UV_Preserved','active_layer':'Tripo_Input_UV','reason':'No sufficiently sized padded empty rectangle in fragmented v002 atlas; preserve island shapes and relative layout, reserve right strip'},
 'human_visual':'HOLD: facial collar blending and identity in motion unresolved; Human PENDING','final_go':False})
write('repair-report.json',report)
contract['status']='Pretexture v002 implemented review; HOLD, Human PENDING'
contract['morph_consolidation']='20 morphs on Jill_Body; blink also drives eye recess/socket skin and physical eyelids'
contract['limitations'].append('Fold bounded to safe posterior sweep; full body-hugging storage unproven')
write('control-contract.json',contract)
np.savez_compressed(E/'surface-contract.npz',basis=np.array(keydata['Basis']),original_basis=original_v,
 polygons=np.array([list(p.vertices) for p in mesh.loop_triangles],dtype=int) if False else np.array([x.vertex_index for x in mesh.loops]),
 uv=np.array([tuple(x.uv) for x in uv.data]),material=np.array([p.material_index for p in mesh.polygons]),regions=np.array(regions))
print('JILL_LOCAL_REPAIR_SAVED',len(mesh.vertices),len(mesh.polygons),'20 morphs')
