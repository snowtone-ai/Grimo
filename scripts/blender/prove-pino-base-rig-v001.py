"""Small, reproducible pose proof. --preview limits rendering to representative poses.
Only a bounded scratch set (one test, <=15*3 low-resolution frames) exists at once;
package-pino-base-rig-v001.py composes and removes that scratch set immediately.
"""
import bpy,math,json,sys,subprocess
import numpy as np
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/pino/candidate-c/rig-v001';OUT=ROOT/'docs/production/pino/evidence/rig-v001'
PY='C:/Users/chidj/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
PACK=ROOT/'scripts/3d/package-pino-base-rig-v001.py'
bpy.ops.wm.open_mainfile(filepath=str(A/'pino-c-base-rig-v001.blend'))
mesh=bpy.data.objects['PINO_C_BASE_RIG_V001'];rig=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];scene=bpy.context.scene;cam=scene.camera
arr=np.load(OUT/'reference-arrays.npz');V=arr['vertices'];L=arr['components'];H=float(np.ptp(V[:,2]));N=len(V)
def dump(name,x):(OUT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def evaluated():
 bpy.context.view_layer.update();o=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get());return np.array([tuple(o.matrix_world@p.co) for p in o.data.vertices])
def rot(name,axis,degrees):
 p=rig.pose.bones[name];p.rotation_mode='QUATERNION';rest=p.bone.matrix_local.to_quaternion();p.rotation_quaternion=rest.inverted()@Quaternion(Vector(axis),math.radians(degrees))@rest
def move(name,worldvec):
 p=rig.pose.bones[name];p.location=p.bone.matrix_local.to_3x3().inverted()@Vector(worldvec)
def neutral():
 for p in rig.pose.bones:p.matrix_basis=Matrix.Identity(4)
 for k in mesh.data.shape_keys.key_blocks:k.value=0
 for c in constraints.values():c.influence=0
 for o in fixtures.values():o.hide_render=True;o.hide_viewport=True
 bpy.context.view_layer.update()
targets={};constraints={};anchors={};rest_hand={};foot_orient={};fixtures={}
for side,sign in [('L',1),('R',-1)]:
 full='Left' if side=='L' else 'Right'
 for part,bone,chain in [('paw','ForeArm',2),('foot','Leg',2)]:
  p=rig.pose.bones[f'mixamorig:{full}{bone}'];b=p.bone
  empty=bpy.data.objects.new(f'Pino_{side}_{part}_IK',None);scene.collection.objects.link(empty);empty.empty_display_size=.035
  empty.location=rig.matrix_world@b.tail_local;targets[(side,part)]=empty
  c=p.constraints.new('IK');c.name=f'Pino_{part}_no_stretch';c.target=empty;c.chain_count=chain;c.use_stretch=False;c.influence=0;constraints[(side,part)]=c
  p.ik_stretch=0
  if p.parent:p.parent.ik_stretch=0
  if part=='foot':
   orientation=bpy.data.objects.new(f'Pino_{side}_sole_orientation',None);scene.collection.objects.link(orientation)
   orientation.matrix_world=rig.matrix_world@rig.data.bones[f'mixamorig:{full}Foot'].matrix_local
   c=rig.pose.bones[f'mixamorig:{full}Foot'].constraints.new('COPY_ROTATION');c.target=orientation;c.target_space='WORLD';c.owner_space='WORLD';c.influence=0
   constraints[(side,'sole')]=c;targets[(side,'sole')]=orientation
 ids=np.where((L==0)&(sign*V[:,0]>.285)&(V[:,2]>.25)&(V[:,2]<.37))[0]
 anchors[side]=int(ids[np.argmin(V[ids,1])]);rest_hand[side]=(rig.matrix_world@rig.data.bones[f'mixamorig:{full}ForeArm'].tail_local).copy()
FIX={'L':Vector((.23,-.325,.435)),'R':Vector((-.23,-.325,.435))}
for side,point in FIX.items():
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.018,location=point+Vector((0,-.018,0)))
 o=bpy.context.object;o.name=f'DIAGNOSTIC_FIXED_CONTACT_{side}';o.hide_render=True;o.hide_viewport=True;fixtures[side]=o
 mat=bpy.data.materials.new(f'Fixed_contact_{side}');mat.diffuse_color=(.7,.22,.08,1);o.data.materials.append(mat)
def paw_contact(side,strength,point=None):
 target=targets[(side,'paw')];c=constraints[(side,'paw')]
 point=FIX[side] if point is None else Vector(point)
 desired=Vector(V[anchors[side]])*(1-strength)+point*strength
 target.location=rest_hand[side]+(desired-Vector(V[anchors[side]]));c.influence=1 if strength>0 else 0
 if strength:
  # Solve actual skin contact against a predeclared world point, keeping bone lengths.
  for _ in range(10):
   actual=Vector(evaluated()[anchors[side]]);error=desired-actual
   if error.length<.0001:break
   target.location+=error*.8
def tail(strength):
 for j in range(5):rot(f'PinoTail{j+1:02d}',(0,0,1),4*strength)
def eyes(l,r):
 mesh.data.shape_keys.key_blocks['PinoBlink_L'].value=l;mesh.data.shape_keys.key_blocks['PinoBlink_R'].value=r
def lowrest(s):
 # Bounded, feet-supported low relaxation. Deep belly rest is still HOLD.
 rot('mixamorig:Hips',(1,0,0),18*s);move('mixamorig:Hips',(0,.012*s,-.032*s))
 rot('mixamorig:Neck',(1,0,0),-12*s)
 for side in ['L','R']:
  # Keep the support solver enabled through the zero-strength endpoint too.
  # Blending it out during the final recovery interval drops the soles.
  constraints[(side,'foot')].influence=1;constraints[(side,'sole')].influence=1
 rot('PinoTail01',(1,0,0),-18*s)
def bothcontact(s):
 for side,sign,full in [('L',1,'Left'),('R',-1,'Right')]:
  rot(f'mixamorig:{full}Shoulder',(0,0,1),-sign*35*s)
  paw_contact(side,s,Vector((sign*.005,-.30,.385)))
def pose(kind,args):
 neutral()
 if kind=='tail':tail(args)
 elif kind=='eyes':eyes(*args)
 elif kind=='paws':
  for side,s in zip(['L','R'],args):
   paw_contact(side,s);fixtures[side].hide_render=s==0;fixtures[side].hide_viewport=s==0
 elif kind=='rest':lowrest(args)
 elif kind=='contact':bothcontact(args)
 bpy.context.view_layer.update()
edges=np.array([list(e.vertices) for e in mesh.data.edges]);length=np.linalg.norm(V[edges[:,0]]-V[edges[:,1]],axis=1);valid=length>1e-7
mesh.data.calc_loop_triangles();T=np.array([t.vertices[:] for t in mesh.data.loop_triangles]);tailtris=T[np.isin(L[T[:,0]],[2,5])]
def volume(v):
 p=v[tailtris];return float(np.einsum('ij,ij->i',p[:,0],np.cross(p[:,1],p[:,2])).sum()/6)
basevol=volume(V);foot=(L==0)&(V[:,2]<.045);belly=(L==0)&(abs(V[:,0])<.17)&(V[:,2]>.15)&(V[:,2]<.4)
def metrics(kind,args):
 v=evaluated();ratio=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1)[valid]/length[valid]
 pawids=[np.where((L==0)&(sg*V[:,0]>.265)&(V[:,2]>.24)&(V[:,2]<.38))[0] for sg in [1,-1]]
 return {'kind':kind,'args':args,'z_min':float(v[:,2].min()),'below_floor_vertices':int(np.sum(v[:,2]<-.001)),
 'edge_ratio_max':float(ratio.max()),'edge_ratio_p99':float(np.percentile(ratio,99)),
 'tail_volume_ratio':volume(v)/basevol,'tail_max_displacement':float(np.linalg.norm(v[np.isin(L,[2,5])]-V[np.isin(L,[2,5])],axis=1).max()),
 'opposite_eye_displacement':{s:float(np.linalg.norm(v[L==comp]-V[L==comp],axis=1).max()) for s,comp in [('L',9),('R',8)]},
 'paw_contact_error':{s:float(np.linalg.norm(v[anchors[s]]-FIX[s])) for s in ['L','R']},
 'distal_paw_gap':float(np.linalg.norm(v[pawids[0]][:,None,:]-v[pawids[1]][None,:,:],axis=2).min()),
 'floor_contacts':{'hindfeet':int(np.sum(abs(v[foot,2])<.003)),'belly':int(np.sum(abs(v[belly,2])<.003))},
 'neutral_max_delta':float(np.linalg.norm(v-V,axis=1).max()) if (args==0 or args==[0,0]) else None}
def view(v,rest=False):
 d=Vector({'front':(0,-1,.04),'side':(1,0,.025),'threequarter':(1,-1,.10)}[v]).normalized()
 target=Vector((0,-.08,.47));cam.location=target+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.34
 bpy.context.view_layer.update()
def render(path,v):
 view(v);scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
preview='--preview' in sys.argv
if preview:
 records=[]
 for label,kind,args in [('neutral','tail',0),('tail','tail',1),('blink','eyes',[1,0]),('highfive','paws',[1,0]),('contact','contact',1),('rest','rest',1)]:
  pose(kind,args);records.append(metrics(kind,args))
  for v in ['front','side','threequarter']:render(OUT/f'preview-{label}-{v}.png',v)
 dump('preview-metrics.json',records)
else:
 neutral();bpy.ops.wm.save_as_mainfile(filepath=str(A/'pino-c-base-rig-v001.blend'))
 tests={'tail':[('tail',s) for s in [0,.5,1,.5,0,-.5,-1,-.5,0]],
 'eyes':[('eyes',s) for s in [[0,0],[.5,0],[1,0],[0,0],[0,1],[0,0],[.5,.5],[1,1],[0,0]]],
 'paws':[('paws',s) for s in [[0,0],[.5,0],[1,0],[.5,0],[0,0],[0,.5],[0,1],[0,.5],[0,0]]]+[('contact',s) for s in [.5,1,.5,0]],
 'rest':[('rest',s) for s in [0,.25,.5,.75,1,.75,.5,.25,0]]}
 scratch=OUT/'_scratch';scratch.mkdir(exist_ok=True);records=[];timeline=1;markers=[];channels={}
 def capture(owner,path,values):
  bank=channels.setdefault(owner,{})
  for index,value in enumerate(values):bank.setdefault((path,index),[]).append((timeline,float(value)))
 for family,poses in tests.items():
  start=timeline
  for index,(kind,args) in enumerate(poses):
   pose(kind,args);r=metrics(kind,args);r.update(family=family,index=index,frame=timeline);records.append(r)
   for v in ['front','side','threequarter']:render(scratch/f'{index:02d}-{v}.png',v)
   for p in rig.pose.bones:
    p.rotation_mode='QUATERNION';capture(rig,p.path_from_id('location'),p.location);capture(rig,p.path_from_id('rotation_quaternion'),p.rotation_quaternion)
   for k in list(mesh.data.shape_keys.key_blocks)[1:]:capture(mesh.data.shape_keys,k.path_from_id('value'),[k.value])
   for key,c in constraints.items():
    capture(rig,c.path_from_id('influence'),[c.influence]);capture(targets[key],'location',targets[key].location)
   for o in fixtures.values():capture(o,'hide_render',[o.hide_render]);capture(o,'hide_viewport',[o.hide_viewport])
   timeline+=6
  markers.append((family,start))
  subprocess.run([PY,str(PACK),'--family',family],check=True)
 scene.frame_start=1;scene.frame_end=timeline-6;scene.render.fps=24
 for label,frame in markers:scene.timeline_markers.new(label,frame=frame)
 # Author curves only AFTER every render. Inserting live keys while sampling at
 # frame 1 causes Blender's render evaluation to restore frame 1 before capture.
 for owner,bank in channels.items():
  action=bpy.data.actions.new('Pino_Diagnostic_'+owner.name);slot=action.slots.new(id_type='OBJECT' if isinstance(owner,bpy.types.Object) else 'KEY',name=owner.name)
  layer=action.layers.new('Diagnostic');strip=layer.strips.new(type='KEYFRAME');bag=strip.channelbag(slot,ensure=True)
  for (path,index),samples in bank.items():
   fc=bag.fcurves.new(data_path=path,index=index);fc.keyframe_points.add(len(samples));fc.keyframe_points.foreach_set('co',[v for sample in samples for v in sample])
   for kp in fc.keyframe_points:kp.interpolation='CONSTANT' if path.startswith('hide_') else 'LINEAR'
   fc.update()
  owner.animation_data_create();owner.animation_data.action=action;owner.animation_data.action_slot=slot
 scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(A/'pino-c-base-rig-v001-proof.blend'))
 dump('deformation-metrics.json',records);dump('proof-timeline.json',{'fps':24,'frame_end':scene.frame_end,'markers':markers,'note':'Sparse diagnostic keyframes; GIFs show evaluated samples, no final Motion.'})
print('PINO_PROOF_DONE',preview)
