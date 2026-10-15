"""Immutable Mixamo input -> Pino rig candidate. No source writes or texture work.

Run with Blender 5.2 --background --factory-startup --python this-file.
Original GLB tessellation/normals/material policy follows geometry-c-v001.
All new controls are zero at Neutral; proof poses are diagnostic, not final Motion.
"""
import bpy, json, math, hashlib, sys
import numpy as np
from pathlib import Path
from collections import Counter
from collections import defaultdict
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets/grimo/production/pino/candidate-c'
DEST=A/'rig-v001'; OUT=ROOT/'docs/production/pino/evidence/rig-v001'
OUT.mkdir(parents=True,exist_ok=True)
def dump(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def coords(o,evaluated=False):
 if evaluated:
  bpy.context.view_layer.update(); o=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
 return np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices])
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
bpy.ops.wm.read_factory_settings(use_empty=True)
src=DEST/'input/pino-c-tripo-mixamo-original.fbx'
bpy.ops.import_scene.fbx(filepath=str(src),use_anim=False)
rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
raw=next(o for o in bpy.context.scene.objects if o.type=='MESH')
rawv=coords(raw);weights=[[(raw.vertex_groups[g.group].name,float(g.weight)) for g in v.groups] for v in raw.data.vertices]
audit={'input_sha256':sha(src),'blender':bpy.app.version_string,'import':{'use_anim':False,'automatic_bone_orientation':False},
 'mesh_matrix_world':[list(r) for r in raw.matrix_world],'armature_matrix_world':[list(r) for r in rig.matrix_world],
 'vertices':len(rawv),'polygons':len(raw.data.polygons),'bone_count':len(rig.data.bones),
 'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'head':list(b.head_local),'tail':list(b.tail_local),'matrix_local':[list(r) for r in b.matrix_local],'use_deform':b.use_deform} for b in rig.data.bones],
 'unassigned':[i for i,w in enumerate(weights) if not w],
 'weight_sum_range':[min(sum(w for _,w in a) for a in weights),max(sum(w for _,w in a) for a in weights)],
 'max_influences':max(map(len,weights)), 'group_weight_totals':dict(Counter({g.name:sum(w for a in weights for n,w in a if n==g.name) for g in raw.vertex_groups})),
 'uv_layers':len(raw.data.uv_layers),'shape_keys':bool(raw.data.shape_keys)}
audit['input_raw_evaluated_max_delta']=float(np.linalg.norm(coords(raw,True)-rawv,axis=1).max())
audit['input_pose_basis']={p.name:[list(r) for r in p.matrix_basis] for p in rig.pose.bones}
np.savez_compressed(OUT/'input-skin.npz',vertices=rawv,group_names=np.array([g.name for g in raw.vertex_groups]),
 weights=np.array([(v.index,g.group,g.weight) for v in raw.data.vertices for g in v.groups]))
bpy.ops.wm.save_as_mainfile(filepath=str(DEST/'pino-c-tripo-import-unaltered.blend'))
# Import the fixed Geometry Master for indexed polygon and position checks.
before=set(bpy.data.objects);bpy.ops.import_scene.fbx(filepath=str(A/'source/cute blue creature 3d model.fbx'),use_anim=False)
master=next(o for o in set(bpy.data.objects)-before if o.type=='MESH')
audit['geometry_master_sha256']=sha(A/'source/cute blue creature 3d model.fbx')
masterv=coords(master)
audit['unmapped_index_max_world_delta']=float(np.linalg.norm(masterv-rawv,axis=1).max())
audit['polygon_indices_exact']=([tuple(p.vertices) for p in master.data.polygons]==[tuple(p.vertices) for p in raw.data.polygons])
def signatures(o,v,q):
 incident=[[] for _ in v];faces=[]
 for p in o.data.polygons:
  sig=tuple(sorted(q[i] for i in p.vertices));faces.append(sig)
  for i in p.vertices:incident[i].append(sig)
 return [(q[i],tuple(sorted(incident[i]))) for i in range(len(v))],Counter(faces)
kd=KDTree(len(masterv))
for i,p in enumerate(masterv):kd.insert(Vector(p),i)
kd.balance();nearest=[kd.find(Vector(p)) for p in rawv]
audit['nearest_master_max_world_delta']=max(d for p,i,d in nearest)
mq=[tuple(p) for p in np.round(masterv,7)];rq=[mq[i] for p,i,d in nearest]
rs,rf=signatures(raw,rawv,rq);ms,mf=signatures(master,masterv,mq);lookup=defaultdict(list)
for i,s in enumerate(rs):lookup[s].append(i)
audit['coincident_signature_groups']=sum(len(g)>1 for g in lookup.values())
audit['face_position_signature_exact']=rf==mf
dump('input-and-build.json',audit)
mapping=np.array([lookup[s].pop() for s in ms]);assert all(len(g)==0 for g in lookup.values())
audit['polygon_position_signature_exact_1e5']=rf==mf
audit['indexed_master_max_world_delta']=float(np.linalg.norm(masterv-rawv[mapping],axis=1).max())
audit['vertex_order_remapped']=int(np.sum(mapping!=np.arange(len(mapping))))
assert rf==mf and audit['indexed_master_max_world_delta']<1e-6
weights=[weights[i] for i in mapping];rawv=rawv[mapping]
audit['unassigned_master_indices']=[i for i,w in enumerate(weights) if not w]
np.savez_compressed(OUT/'input-to-master-map.npz',master_to_input=mapping)
for o in set(bpy.data.objects)-before:bpy.data.objects.remove(o,do_unlink=True)
# Geometry Master vertices with appearance-reference output policy established in prior gate.
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(A/'delivery/pino-c-master-derived-neutral.glb'))
mesh=next(o for o in set(bpy.data.objects)-before if o.type=='MESH')
mesh.name='PINO_C_BASE_RIG_V001';rig.name='PINO_C_TRIPO_PLUS_CONTROLS_V001'
V=coords(mesh);base_local=np.array([tuple(v.co) for v in mesh.data.vertices]);N=len(V)
audit['appearance_reference_max_world_delta']=float(np.linalg.norm(V-rawv,axis=1).max())
assert audit['appearance_reference_max_world_delta']<1e-6
audit['appearance_policy']='FBX indexed vertices verified; GLB reference tessellation, corner normals, material retained per geometry-c-v001. No UV/Texture added.'
groups={n:mesh.vertex_groups.new(name=n) for n in [g.name for g in raw.vertex_groups]}
for i,ws in enumerate(weights):
 for n,w in ws:groups[n].add([i],w,'REPLACE')
world=mesh.matrix_world.copy();mesh.parent=rig;mesh.matrix_world=world
mod=mesh.modifiers.new('Pino volume-preserving skin','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
rig.show_in_front=True
bpy.data.objects.remove(raw,do_unlink=True)
L=np.load(ROOT/'docs/production/pino/evidence/geometry-c-v001/glb-diagnostic-arrays.npz')['components']
assert len(L)==N
tail=np.isin(L,[2,5]);audit['tail_input_weights']=dict(Counter({n:sum(w for i in np.where(tail)[0] for nn,w in weights[i] if nn==n) for n in groups}))
# Use the original skeleton unchanged, adding a five-segment tail with smooth skin ownership.
bpy.context.view_layer.objects.active=rig;rig.select_set(True);mesh.select_set(False);bpy.ops.object.mode_set(mode='EDIT')
inv=rig.matrix_world.inverted()
tailnodes=[Vector((0,y,.19+max(0,y-.04)*.45)) for y in [-.015,.075,.165,.255,.345,.435]]
for j in range(5):
 b=rig.data.edit_bones.new(f'PinoTail{j+1:02d}');b.head=inv@tailnodes[j];b.tail=inv@tailnodes[j+1]
 b.parent=rig.data.edit_bones['mixamorig:Hips'] if j==0 else rig.data.edit_bones[f'PinoTail{j:02d}'];b.use_connect=j>0
bpy.ops.object.mode_set(mode='OBJECT')
tailgroups=[mesh.vertex_groups.new(name=f'PinoTail{j+1:02d}') for j in range(5)]
def replace_weights(ids,fn):
 ids=list(map(int,ids))
 for g in mesh.vertex_groups:g.remove(ids)
 for i in ids:
  for name,w in fn(i):
   if w>1e-8:
    g=mesh.vertex_groups.get(name)
    if g is None:g=mesh.vertex_groups.new(name=name)
    g.add([i],float(w),'REPLACE')
def tailweights(i):
 if V[i,1]<.075:
  f=float(smooth(-.015,.075,V[i,1]));return [('mixamorig:Hips',1-f),(tailgroups[0].name,f)]
 t=np.clip((V[i,1]-.075)/.09,0,4);j=int(t);f=t-j
 return [(tailgroups[j].name,1-f),(tailgroups[min(j+1,4)].name,f)]
replace_weights(np.where(tail)[0],tailweights)
# Repair the single unassigned point using its closest assigned point's weights.
repairs=[]
for i in audit['unassigned_master_indices']:
 candidates=np.array([j for j in range(N) if weights[j]])
 j=int(candidates[np.argmin(np.linalg.norm(V[candidates]-V[i],axis=1))])
 if not tail[i]:replace_weights([i],lambda _:weights[j])
 repairs.append({'vertex':i,'nearest_assigned':j,'distance':float(np.linalg.norm(V[j]-V[i])),'weights':weights[j]})
# Compact paws have no independently authored fingers. Collapse generated finger skin
# to their own Hand (bone hierarchy retained), never adding human-like fingers.
collapsed=0
for v in mesh.data.vertices:
 acc={mesh.vertex_groups[g.group].name:float(g.weight) for g in v.groups};new={}
 for n,w in acc.items():
  nn=n
  for side in ['Left','Right']:
   if n.startswith(f'mixamorig:{side}Hand') and n!=f'mixamorig:{side}Hand':nn=f'mixamorig:{side}Hand';collapsed+=1
  new[nn]=new.get(nn,0)+w
 if new!=acc:replace_weights([v.index],lambda _,d=new:list(d.items()))
# The humanoid auto-skin couples pelvis/thighs and belly/shoulders abruptly.
# Replace the body support transition with smooth, normalized local ownership.
# Neutral coordinates are untouched. Foot soles stay foot-owned; arms retain
# their imported internal joint distribution within a bounded lateral region.
def bodyweights(i):
 x,y,z=V[i];side='Left' if x>=0 else 'Right';ws={mesh.vertex_groups[g.group].name:g.weight for g in mesh.data.vertices[i].groups}
 arm={n:w for n,w in ws.items() if n.startswith(f'mixamorig:{side}') and any(k in n for k in ['Shoulder','Arm','Hand'])}
 total=sum(arm.values());wa=float(smooth(.17,.275,abs(x))*smooth(.19,.26,z)*(1-smooth(.425,.49,z))*min(1,total*1.5))
 wh=float(smooth(.43,.50,z));wf=float(1-smooth(.055,.155,z));wsp=float(smooth(.21,.41,z))
 body={'mixamorig:Head':wh,f'mixamorig:{side}Foot':(1-wh)*wf,
       'mixamorig:Spine2':(1-wh)*(1-wf)*wsp,'mixamorig:Hips':(1-wh)*(1-wf)*(1-wsp)}
 result=[(n,w*(1-wa)) for n,w in body.items()]
 if total:result.extend((n,w/total*wa) for n,w in arm.items())
 return result
bodyids=np.where((L==0)&(V[:,2]<.50))[0]
# Compute before mutation, so each vertex's imported arm distribution is stable.
bodybank={int(i):bodyweights(int(i)) for i in bodyids}
replace_weights(bodyids,lambda i:bodybank[i])
# Rigid head-owned eye patches prevent torso/neck weights dragging the closed line.
headids=np.where((V[:,2]>.49)&~tail)[0]
replace_weights(headids,lambda i:[('mixamorig:Head',1.)])
replace_weights(np.where(np.isin(L,[8,9]))[0],lambda i:[('mixamorig:Head',1.)])
mesh.shape_key_add(name='Basis').value=0;tree=BVHTree.FromPolygons([Vector(p) for p in V],
 [list(p.vertices) for p in mesh.data.polygons if L[p.vertices[0]]==0],all_triangles=True)
eye_report={}
for side,comp in [('L',9),('R',8)]:
 ids=np.where(L==comp)[0];p=V[ids];c=(p.min(0)+p.max(0))/2;xn=np.clip((p[:,0]-c[0])/(np.ptp(p[:,0])/2),-1,1)
 target=p.copy();target[:,2]=c[2]+.009*(1-xn*xn)+.025*(p[:,2]-c[2])
 for j,pt in enumerate(target):
  hit=tree.ray_cast(Vector((pt[0],-.8,pt[2])),Vector((0,1,0)))
  if hit[0] is not None:target[j,1]=hit[0].y-.006-.004*(1-xn[j]**2)
 key=mesh.shape_key_add(name=f'PinoBlink_{side}');key.value=0;invmesh=mesh.matrix_world.inverted()
 for i,p in zip(ids,target):key.data[int(i)].co=invmesh@Vector(p)
 eye_report[side]={'component':comp,'vertices':len(ids),'method':'head-surface conforming independent closed-line patch; no new texture or full anatomical eyelid'}
audit['edits']={'tail_bones':5,'unassigned_repair':repairs,'finger_influences_collapsed':collapsed,'smooth_body_support_vertices':len(bodyids),'rigid_head_vertices':len(headids),'eyes':eye_report,'source_skeleton_preserved':True}
mesh['Human_Rig_Geometry_Gate']='PENDING';rig['Human_Rig_Geometry_Gate']='PENDING'
rig['usage']='Diagnostic base rig candidate, not approved production Motion'
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=400;scene.render.resolution_y=400;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.world=bpy.data.worlds.new('Pino proof world');scene.world.color=(.16,.18,.22)
scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True
scene.display.shading.show_cavity=False;scene.display.shading.background_type='WORLD';scene.display.shading.show_specular_highlight=True
camd=bpy.data.cameras.new('Review camera');cam=bpy.data.objects.new('Review camera',camd);scene.collection.objects.link(cam);scene.camera=cam;camd.type='ORTHO';camd.ortho_scale=1.3
cam.location=(2,-2,1);target=Vector((0,-.03,.47));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
audit['neutral_evaluated_max_world_delta']=float(np.linalg.norm(coords(mesh,True)-V,axis=1).max())
audit['original_bone_bind_max_delta']=float(max(np.abs(np.array([list(r) for r in rig.data.bones[b['name']].matrix_local])-np.array(b['matrix_local'])).max() for b in audit['bones']))
audit['basis_local_exact']=np.array_equal(base_local,np.array([v.co[:] for v in mesh.data.vertices]))
dump('input-and-build.json',audit)
print('NEUTRAL_CHECK',audit['basis_local_exact'],audit['neutral_evaluated_max_world_delta'])
assert audit['basis_local_exact'] and audit['neutral_evaluated_max_world_delta']<1e-6
dump('input-and-build.json',audit)
np.savez_compressed(OUT/'reference-arrays.npz',vertices=V,components=L,local=base_local)
bpy.ops.wm.save_as_mainfile(filepath=str(DEST/'pino-c-base-rig-v001.blend'))
print('PINO_BUILD',json.dumps({k:audit[k] for k in ['vertices','polygons','bone_count','indexed_master_max_world_delta','appearance_reference_max_world_delta','neutral_evaluated_max_world_delta','basis_local_exact']}))
