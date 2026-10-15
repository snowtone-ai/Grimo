"""Jill-specific six-limb authoring rig. Run only after committed Plan.md.

Inputs are immutable byte copies. This script never saves to an input path.
The Basis comes from v002; FBX contributes verified corresponding UVs/limb weights.
"""
import bpy, json, math, hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'assets/grimo/production/jill/tripo/rig-other-v001'
SRC=ASSET/'source'; E=ROOT/'docs/production/jill/rig-other-v001'
ASSET.mkdir(parents=True,exist_ok=True); (E/'renders').mkdir(exist_ok=True)
assert (E/'Plan.md').is_file(), 'Research/Plan gate missing'
EXPECTED={'tripo-other-original.fbx':'1d9ecfae60f0fcb1a8bbffeb81fd2a931b1dba0907af43487bf0d1f1e3a7dc14',
 'tripo-other-original.glb':'a93cd56d4b9658596284288ef8f5ebabffae0d3c5f7024e591269ce95eff0378',
 'jill-v002-authority-donor.blend':'8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97'}
for name,sha in EXPECTED.items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==sha,name
def write(name,x): (E/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def smooth(a,b,x):
    u=np.clip((x-a)/(b-a),0,1);return u*u*(3-2*u)
def xyz(o):
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh()
    a=np.array([tuple(o.matrix_world@v.co) for v in m.vertices]);ev.to_mesh_clear();return a
def components(m):
    parent=list(range(len(m.vertices)))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for e in m.edges:
        a,b=map(root,e.vertices);parent[b]=a
    g={}
    for v in m.vertices:g.setdefault(root(v.index),[]).append(v.index)
    return sorted(g.values(),key=lambda v:-len(v))

bpy.ops.wm.open_mainfile(filepath=str(SRC/'jill-v002-authority-donor.blend'))
body=bpy.data.objects['JILL_GEOMETRY_MASTER'];s=bpy.context.scene;s.frame_set(1)
authority=np.array([tuple(body.matrix_world@v.co) for v in body.data.vertices])
old_parts=components(body.data)
diag={g.name:np.array([next((x.weight for x in v.groups if x.group==g.index),0) for v in body.data.vertices]) for g in body.vertex_groups}
body.shape_key_clear();body.animation_data_clear()
body.data.transform(body.matrix_world);body.matrix_world=Matrix.Identity(4)
for o in list(bpy.data.objects):
    if o!=body:bpy.data.objects.remove(o,do_unlink=True)
body.name='Jill_Body';body.data.name='Jill_v002_PreservedSurface'
before=set(bpy.data.objects);bpy.ops.import_scene.fbx(filepath=str(SRC/'tripo-other-original.fbx'))
fbx=next(o for o in bpy.data.objects if o not in before and o.type=='MESH')
fa=next(o for o in bpy.data.objects if o not in before and o.type=='ARMATURE')
corr=json.loads((E/'source-correspondence.json').read_text())
assert corr['topology_indexed_equal'] and corr['indexed_position_max_error']<2e-7
assert len(fbx.data.vertices)==len(body.data.vertices)
source_bones={b.name:((np.array(fa.matrix_world@b.head_local)*corr['scale_fbx_to_authority']+corr['offset_fbx_to_authority']).tolist(),
 (np.array(fa.matrix_world@b.tail_local)*corr['scale_fbx_to_authority']+corr['offset_fbx_to_authority']).tolist()) for b in fa.data.bones}
rawweights=[{fbx.vertex_groups[g.group].name:g.weight for g in v.groups} for v in fbx.data.vertices]
# Same indexed polygon loops were verified; preserve the FBX UV without resampling.
uv=body.data.uv_layers.new(name='Tripo_Original_UV')
uv.data.foreach_set('uv',np.array([tuple(x.uv) for x in fbx.data.uv_layers[0].data],dtype=np.float32).ravel())
uv_reference=np.array([tuple(x.uv) for x in uv.data])
for o in list(bpy.data.objects):
    if o!=body:bpy.data.objects.remove(o,do_unlink=True)
for g in list(body.vertex_groups):body.vertex_groups.remove(g)
for mod in list(body.modifiers):body.modifiers.remove(mod)
body.hide_render=False;body.hide_set(False)
v=np.array([tuple(x.co) for x in body.data.vertices]);n=len(v);parts=components(body.data)
body.shape_key_add(name='Basis')
rig=bpy.data.objects.new('JILL_RIG',bpy.data.armatures.new('Jill_SixLimb_Skeleton'))
s.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bones={};spec=[]
def bone(name,h,t,parent=None,deform=True,category='Body'):
    b=rig.data.edit_bones.new(name);b.head=h;b.tail=t
    if (b.tail-b.head).length<.001:b.tail=b.head+Vector((0,0,.02))
    if parent:b.parent=rig.data.edit_bones[parent]
    b.use_deform=deform;spec.append({'name':name,'parent':parent,'head':list(b.head),'tail':list(b.tail),'deform':deform,'category':category})
    return name
bone('ROOT',(0,0,0),(0,0,.10),deform=False)
bone('DEF_pelvis',(0,-.11,.22),(0,-.13,.29),'ROOT')
bone('DEF_spine',(0,-.13,.29),(0,-.17,.40),'DEF_pelvis')
bone('DEF_chest',(0,-.17,.40),(0,-.19,.52),'DEF_spine')
bone('DEF_neck',(0,-.19,.52),(0,-.205,.565),'DEF_chest')
bone('DEF_head',(0,-.205,.565),(0,-.23,.77),'DEF_neck')
for side,sign in [('L',1),('R',-1)]:
    for src,name,parent in [('Clavicle','scapula','DEF_chest'),('Upperarm','upperarm',f'DEF_scapula.{side}'),('Forearm','forearm',f'DEF_upperarm.{side}'),('Hand','paw',f'DEF_forearm.{side}'),('Thigh','thigh','DEF_pelvis'),('Calf','shin',f'DEF_thigh.{side}'),('Foot','foot',f'DEF_shin.{side}')]:
        h,t=source_bones[f'{side}_{src}'];bone(f'DEF_{name}.{side}',h,t,parent,category='Limbs')
    # Explicit wing girdles are fictional design for Jill's extra limb pair.
    bone(f'DEF_wing_girdle.{side}',(sign*.035,-.09,.50),(sign*.07,-.125,.49),'DEF_chest',category='Wings')
    bone(f'DEF_wing_root.{side}',(sign*.07,-.125,.49),(sign*.225,-.015,.57),f'DEF_wing_girdle.{side}',category='Wings')
    bone(f'DEF_wing_outer.{side}',(sign*.225,-.015,.57),(sign*.405,.025,.61),f'DEF_wing_root.{side}',category='Wings')
    bone(f'DEF_wing_membrane.{side}',(sign*.225,-.015,.57),(sign*.25,.125,.46),f'DEF_wing_root.{side}',category='Wings')
    ids=parts[99 if side=='L' else 98];center=v[ids].mean(0);normal=Vector((sign*.52,-.85,0)).normalized()
    pivot=Vector(center)-normal*.022
    bone(f'DEF_eye.{side}',pivot,pivot+normal*.04,'DEF_head',category='Face')
tailpath=np.array([(0,.075,.225),(0,.16,.205),(0,.25,.22),(0,.325,.275),(0,.365,.355),(0,.36,.44),(0,.325,.515)])
for i in range(len(tailpath)-1):bone(f'DEF_tail_{i:02d}',tailpath[i],tailpath[i+1],'DEF_pelvis' if i==0 else f'DEF_tail_{i-1:02d}',category='Tail')
def tail_blend(points):
    points=np.atleast_2d(points);best=np.full(len(points),1e10);arc=np.zeros(len(points));lens=np.linalg.norm(np.diff(tailpath,axis=0),axis=1);cum=np.r_[0,np.cumsum(lens)]
    for j,(a,b) in enumerate(zip(tailpath[:-1],tailpath[1:])):
        d=b-a;t=np.clip(((points-a)@d)/(d@d),0,1);dist=np.linalg.norm(points-(a+t[:,None]*d),axis=1);m=dist<best
        best[m]=dist[m];arc[m]=cum[j]+t[m]*lens[j]
    centers=(cum[:-1]+cum[1:])/2
    out=np.zeros((len(points),len(centers)))
    for row,x in enumerate(arc):
        hi=int(np.searchsorted(centers,x));lo=max(0,hi-1);hi=min(len(centers)-1,hi)
        if lo==hi:out[row,lo]=1
        else:u=np.clip((x-centers[lo])/(centers[hi]-centers[lo]),0,1);out[row,lo]=1-u;out[row,hi]=u
    return out
leafinfo=[]
for ci,ids in enumerate(parts):
    if ci in [0,1,2,4,98,99] or len(ids)<5:continue
    q=v[ids];center=q.mean(0);owner='DEF_head';region='head'
    if q[:,1].min()>.09 and q[:,2].max()<.52:
        owner=f'DEF_tail_{int(np.argmax(tail_blend(center)[0])):02d}';region='tail'
    elif center[2]<.57:owner='DEF_chest';region='neck'
    elif center[2]<.62:owner='DEF_neck';region='neck'
    # Infer attached end toward owner, retaining every original vertex.
    own=rig.data.edit_bones[owner].head;ds=np.linalg.norm(q-np.array(own),axis=1)
    anchor=q[np.argsort(ds)[:max(3,len(q)//8)]].mean(0)
    tip=q[np.argsort(ds)[-max(3,len(q)//8):]].mean(0)
    name=f'DEF_leaf_{ci:03d}';bone(name,anchor,tip,owner,category='Leaves')
    leafinfo.append({'component':ci,'bone':name,'owner':owner,'region':region,'side':'L' if center[0]>=0 else 'R','ids':ids})
bpy.ops.object.mode_set(mode='OBJECT')
rig.show_in_front=True;rig.data.display_type='BBONE'
for x in spec:
    col=rig.data.collections.get(x['category']) or rig.data.collections.new(x['category']);col.assign(rig.data.bones[x['name']])
    rig.data.bones[x['name']].color.palette='THEME04' if x['category']=='Wings' else 'THEME03'
for b in rig.pose.bones:b.rotation_mode='QUATERNION'

controls={}
def prop(name,lo=-1,hi=1,description=''):
    rig[name]=0.0;rig.id_properties_ui(name).update(min=lo,max=hi,soft_min=lo,soft_max=hi,description=description)
    controls[name]={'range':[lo,hi],'default':0,'description':description}
for name in ['chest_lift','breath','head_yaw','head_nod','head_tilt','tail_sway','tail_curl','leaves_head.L','leaves_head.R','leaves_neck.L','leaves_neck.R','leaves_tail']:
    prop(name,description='Bounded authoring channel; Human appearance approval pending')
for side in ['L','R']:
    for ch in ['wing_open','wing_flap','wing_camber','paw_offer','paw_turn','gaze_x','gaze_y']:
        prop(f'{ch}.{side}',description='Independent anatomical '+side)
    for ch in ['blink','smile','cheek_touch','paw_ik','foot_ik']:
        prop(f'{ch}.{side}',0,1,description='Independent anatomical '+side)
prop('mouth_close',0,1,'Close existing small open mouth, preserve neutral face outline')
prop('mouth_open',0,1,'Small additional opening, not a full food performance library')
prop('chest_touch',0,1,'Local chest surface compression, independent of support')
def driver(data,path,index,expression,variables):
    fc=data.driver_add(path,index) if index is not None else data.driver_add(path)
    d=fc.driver;d.type='SCRIPTED';d.expression=expression
    for short,p in variables.items():
        a=d.variables.new();a.name=short;a.type='SINGLE_PROP';a.targets[0].id=rig;a.targets[0].data_path='["'+p+'"]'
    return fc
def rotation(name,world_axis,angle,variables):
    b=rig.pose.bones[name];axis=rig.data.bones[name].matrix_local.to_3x3().inverted()@Vector(world_axis);axis.normalize()
    driver(b,'rotation_quaternion',0,'cos(('+angle+')/2)',variables)
    for i in range(3):driver(b,'rotation_quaternion',i+1,f'{axis[i]:.10f}*sin(({angle})/2)',variables)
def translate(name,world_axis,amount,variables):
    axis=rig.data.bones[name].matrix_local.to_3x3().inverted()@Vector(world_axis)
    for i in range(3):driver(rig.pose.bones[name],'location',i,f'{axis[i]:.10f}*({amount})',variables)
rotation('DEF_chest',(1,0,0),'-.065*c',{'c':'chest_lift'})
rotation('DEF_neck',(0,0,1),'.055*h',{'h':'head_yaw'})
# Head composite quaternion via Euler-to-quaternion sampled expressions (small authored ranges).
hb=rig.pose.bones['DEF_head'];hb.rotation_mode='XYZ'
axes=[rig.data.bones['DEF_head'].matrix_local.to_3x3().inverted()@Vector(a) for a in [(1,0,0),(0,1,0),(0,0,1)]]
for i in range(3):driver(hb,'rotation_euler',i,f'{axes[0][i]*.14}*n+{axes[1][i]*.12}*t+{axes[2][i]*.16}*h',{'n':'head_nod','t':'head_tilt','h':'head_yaw'})
for side,sign in [('L',1),('R',-1)]:
    rotation(f'DEF_wing_girdle.{side}',(0,0,1),f'{-sign*.035}*max(w,0)',{'w':f'wing_open.{side}'})
    rotation(f'DEF_wing_root.{side}',(0,0,1),f'{-sign}*(.27*max(w,0)+.48*min(w,0))',{'w':f'wing_open.{side}'})
    translate(f'DEF_wing_root.{side}',(0,1,0),'.035*max(w,0)',{'w':f'wing_open.{side}'})
    rotation(f'DEF_wing_outer.{side}',(0,1,0),f'{-sign}*.28*f',{'f':f'wing_flap.{side}'})
    rotation(f'DEF_wing_membrane.{side}',(1,0,0),'.12*c',{'c':f'wing_camber.{side}'})
    rotation(f'DEF_scapula.{side}',(1,0,0),'-.06*p',{'p':f'paw_offer.{side}'})
    rotation(f'DEF_upperarm.{side}',(1,0,0),'-.36*p',{'p':f'paw_offer.{side}'})
    rotation(f'DEF_forearm.{side}',(1,0,0),'-.20*p',{'p':f'paw_offer.{side}'})
    rotation(f'DEF_paw.{side}',(0,0,1),f'{sign}*.25*t',{'t':f'paw_turn.{side}'})
    eb=rig.pose.bones[f'DEF_eye.{side}'];eb.rotation_mode='XYZ'
    # Surface eye pivot behind the original eye, a deliberately bounded gaze candidate.
    driver(eb,'rotation_euler',0,'.055*y',{'y':f'gaze_y.{side}'})
    driver(eb,'rotation_euler',2,'.055*x',{'x':f'gaze_x.{side}'})
for i in range(6):
    rotation(f'DEF_tail_{i:02d}',(0,0,1),f'{[.06,.07,.07,.06,.04,.03][i]}*t',{'t':'tail_sway'})
    # Tail curl remains direct FK on optional X Euler channel via a child-free location-free shape below.
for axis in [0,2]:driver(rig.pose.bones['DEF_chest'],'scale',axis,'1+.008*b',{'b':'breath'})
for info in leafinfo:
    region=info['region'];ch='leaves_tail' if region=='tail' else f'leaves_{region}.{info["side"]}'
    b=rig.pose.bones[info['bone']];b['local_bend']=0.0;b.id_properties_ui('local_bend').update(min=-1,max=1)
    rotation(info['bone'],(1,0,0),'.055*l',{'l':ch})
    # The per-leaf term is added explicitly to every quaternion component.
    axis=rig.data.bones[info['bone']].matrix_local.to_3x3().inverted()@Vector((1,0,0));axis.normalize()
    for j in range(4):
        fc=next(f for f in rig.animation_data.drivers if f.data_path==b.path_from_id('rotation_quaternion') and f.array_index==j)
        a=fc.driver.variables.new();a.name='local';a.type='SINGLE_PROP';a.targets[0].id=rig;a.targets[0].data_path=b.path_from_id('["local_bend"]')
        fc.driver.expression='cos((.055*l+.12*local)/2)' if j==0 else f'{axis[j-1]:.10f}*sin((.055*l+.12*local)/2)'

# Collapse human-only fingers/twists to Jill's plush limb segments; torso weights retained locally.
def mapped(name):
    simple={'BoneRoot':'DEF_pelvis','Hip':'DEF_pelvis','Pelvis':'DEF_pelvis','Waist':'DEF_spine','Spine01':'DEF_spine','Spine02':'DEF_chest','NeckTwist01':'DEF_neck','NeckTwist02':'DEF_neck','Head':'DEF_head','FacialBone':'DEF_head','L_Eye':'DEF_head','R_Eye':'DEF_head'}
    if name in simple:return simple[name]
    side=name[:1]
    if side not in 'LR':return 'DEF_chest'
    token=name[2:]
    target='paw'
    for stem,out in [('Clavicle','scapula'),('Upperarm','upperarm'),('Forearm','forearm'),('Elbow','forearm'),('Thigh','thigh'),('Calf','shin'),('Knee','shin'),('Foot','foot'),('Toe','foot')]:
        if token.startswith(stem):target=out;break
    return f'DEF_{target}.{side}'
deforms=[x['name'] for x in spec if x['deform']];index={name:i for i,name in enumerate(deforms)}
W=np.zeros((n,len(deforms)),dtype=np.float64)
for i,weights in enumerate(rawweights):
    for name,w in weights.items():W[i,index[mapped(name)]]+=w
W[W.sum(1)<1e-8,index['DEF_chest']]=1
W/=W.sum(1)[:,None]
# Face/upper head must not inherit human-eye or finger noise.
main=np.zeros(n,dtype=bool);main[parts[0]]=True
# A hard z cut produced 12.24x stretch on a .00229 edge at the shoulder/head
# boundary in the first compound proof. Blend ownership through the lower head;
# the forward face remains rigid while the neck/shoulder has a continuous falloff.
headblend=main*np.maximum(smooth(.50,.615,v[:,2]),smooth(-.28,-.34,v[:,1])*smooth(.49,.57,v[:,2]))
W*=1-headblend[:,None];W[:,index['DEF_head']]+=headblend
# Tail follows arc order rather than straight distance across its curled shape.
tail=diag['DIAGNOSTIC_Tail'].copy();tail[~main]=0
tw=tail_blend(v)
W*=1-tail[:,None]
for i in range(6):W[:,index[f'DEF_tail_{i:02d}']]+=tail*tw[:,i]
for side,ids in [('L',parts[2]+parts[4]),('R',parts[1])]:
    q=v[ids];r=smooth(.055,.14,abs(q[:,0]));u=smooth(.18,.35,abs(q[:,0]));t=smooth(-.015,.14,q[:,1])*.42
    W[ids]=0
    for name,weight in [('DEF_chest',1-r),(f'DEF_wing_root.{side}',r*(1-u)),(f'DEF_wing_outer.{side}',r*u*(1-t)),(f'DEF_wing_membrane.{side}',r*u*t)]:W[ids,index[name]]=weight
for info in leafinfo:
    W[info['ids']]=0;W[info['ids'],index[info['bone']]]=1
for side,ci in [('L',99),('R',98)]:W[parts[ci]]=0;W[parts[ci],index[f'DEF_eye.{side}']]=1
# Keep four strongest influences to make LBS contracts identical in Blender and glTF.
for i in range(n):
    keep=np.argsort(W[i])[-4:];row=np.zeros(W.shape[1]);row[keep]=W[i,keep];row[row<1e-5]=0;W[i]=row/row.sum()
for name,j in index.items():
    g=body.vertex_groups.new(name=name)
    for i in np.flatnonzero(W[:,j]):g.add([int(i)],float(W[i,j]),'REPLACE')
body.parent=rig
mod=body.modifiers.new('Jill export LBS','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=False

def newshape(name,delta,propname=None,expr='p'):
    k=body.shape_key_add(name=name);k.data.foreach_set('co',(v+delta).astype(np.float32).ravel())
    if propname:driver(k,'value',None,expr,{'p':propname})
    return k
# Existing small mouth, local cheeks and chest; no neutral face redesign.
x,y,z=v.T
mouth=np.exp(-((x/.052)**4+((z-.605)/.043)**4))*smooth(-.32,-.37,y)
delta=np.zeros_like(v);delta[:,2]=-(z-.605)*.78*mouth
newshape('FACE_MouthClose',delta,'mouth_close')
delta=np.zeros_like(v);delta[:,2]=-.009*mouth*(1-smooth(.590,.615,z))
newshape('FACE_MouthOpen',delta,'mouth_open')
for side,sign in [('L',1),('R',-1)]:
    mask=np.exp(-(((x-sign*.045)/.025)**2+((z-.609)/.025)**2))*smooth(-.32,-.38,y)
    delta=np.zeros_like(v);delta[:,2]=.0035*mask
    newshape(f'FACE_Smile.{side}',delta,f'smile.{side}')
    mask=np.exp(-(((x-sign*.16)/.05)**2+((z-.63)/.045)**2))*smooth(-.20,-.29,y)
    delta=np.zeros_like(v);delta[:,1]=.003*mask
    newshape(f'TOUCH_Cheek.{side}',delta,f'cheek_touch.{side}')
delta=np.zeros_like(v);delta[:,1]=.004*np.exp(-((x/.10)**2+((z-.41)/.07)**2))*smooth(-.20,-.29,y)
newshape('TOUCH_Chest',delta,'chest_touch')
delta=np.zeros_like(v)
for i in range(6):
    ids=np.flatnonzero(tail>0);pivot=tailpath[i];mask=tail[ids]*tw[ids,i]
    for ii,w in zip(ids,mask):delta[ii]+=(np.array(Matrix.Rotation(-.08*float(w),3,'X')@Vector(v[ii]-pivot))+pivot-v[ii])
newshape('TAIL_Curl',delta,'tail_curl','max(p,0)')
for side,ids in [('L',parts[2]+parts[4]),('R',parts[1])]:
    delta=np.zeros_like(v);q=v[ids];mask=smooth(.10,.19,abs(q[:,0]))*(1-smooth(.32,.40,abs(q[:,0])))*smooth(-.13,.00,q[:,1])
    delta[ids,1]=-.012*mask
    newshape(f'WING_Camber.{side}',delta,f'wing_camber.{side}','max(p,0)')

def update():
    rig.update_tag();bpy.context.view_layer.update()
def reset():
    for key in controls:rig[key]=0.0
    update()
# Pose-dependent local corrections are pulled back through the actual blended LBS matrix.
corrections=[]
requests=[]
for side in ['L','R']:
    wm=np.zeros(n);wm[parts[2]+parts[4] if side=='L' else parts[1]]=1
    requests.extend([(f'COR_WingOpen.{side}',f'wing_open.{side}',1,wm*(1-smooth(.15,.24,abs(x)))),
      (f'COR_WingFold.{side}',f'wing_open.{side}',-1,wm*(1-smooth(.15,.24,abs(x)))),
      (f'COR_Shoulder.{side}',f'paw_offer.{side}',1,diag['DIAGNOSTIC_Arm'+side]*(1-diag['DIAGNOSTIC_Arm'+side]) *4)])
requests.extend([('COR_TailLeft','tail_sway',1,tail*(1-smooth(.20,.30,y))),('COR_TailRight','tail_sway',-1,tail*(1-smooth(.20,.30,y)))])
for name,ch,value,mask in requests:
    reset();rig[ch]=float(value);update();a=xyz(body)
    mod.use_deform_preserve_volume=True;update();desired=xyz(body);mod.use_deform_preserve_volume=False;update()
    delta=np.zeros_like(v);ids=np.flatnonzero(mask>1e-5)
    mats=np.array([np.array(rig.pose.bones[bn].matrix@rig.data.bones[bn].matrix_local.inverted()) for bn in deforms])
    for i in ids:
        M=np.einsum('j,jkl->kl',W[i],mats)[:3,:3]
        d=np.linalg.solve(M,(desired[i]-a[i])*mask[i]);length=np.linalg.norm(d)
        if length>.012:d*=.012/length
        delta[i]=d
    reset();newshape(name,delta,ch,'min(max(p,0),1)' if value>0 else 'min(max(-p,0),1)')
    corrections.append({'name':name,'control':ch,'peak':value,'changed_vertices':int(np.sum(np.linalg.norm(delta,axis=1)>1e-9)),'max_rest_delta':float(np.linalg.norm(delta,axis=1).max()),'method':'Local DQ target minus LBS, inverse blended LBS pullback, bounded .012. Human visual pending.'})

# Independent physical eyelid patches, folded into the existing upper/lower rims at open.
# Patches cover the original curved eye, rather than flattening that eye into a line.
lidinfo=[]
for side,ci,sign in [('L',99,1),('R',98,-1)]:
    eye=v[parts[ci]];center=eye.mean(0);normal=np.array((sign*.52,-.85,0));normal/=np.linalg.norm(normal)
    tangent=np.array((.85,sign*.52,0));tangent/=np.linalg.norm(tangent)
    u=(eye-center)@tangent;zz=eye[:,2]-center[2];depth=(eye-center)@normal
    ru=max(abs(u));rz=max(abs(zz));A=np.c_[np.ones(len(u)),u,zz,u*u,u*zz,zz*zz];coef=np.linalg.lstsq(A,depth,rcond=None)[0]
    verts=[];closed=[];faces=[]
    for half in [1,-1]:
        offset=len(verts)
        for ix in range(25):
            U=-.998+1.996*ix/24;Upos=U*ru;arc=rz*math.sqrt(max(0,1-U*U));seam=-.003*(1-U*U)
            for iy in range(7):
                t=iy/6;edge=half*arc
                Z0=edge-half*.00035*t;Z1=edge+(seam-edge)*t
                def point(Z,lift):
                    D=np.dot([1,Upos,Z,Upos*Upos,Upos*Z,Z*Z],coef)+lift
                    return center+tangent*Upos+np.array((0,0,Z))+normal*D
                # The coarse source eye exceeds the quadratic fit by .002024.
                # Closed clearance includes that measured residual plus grid interpolation.
                # A shallow crease meets both lids without leaving an eye-exposing seam.
                verts.append(point(Z0,.0013));closed.append(point(Z1,.0036-.0006*t**8))
        for ix in range(24):
            for iy in range(6):
                a=offset+ix*7+iy;b=a+7;faces.append((a,b,b+1,a+1) if half==1 else (a,a+1,b+1,b))
    mesh=bpy.data.meshes.new(f'Jill_CurvedLids.{side}');mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new(f'Jill_Lids.{side}',mesh);s.collection.objects.link(ob);ob.parent=rig
    for p in mesh.polygons:p.use_smooth=True
    ob.shape_key_add(name='Basis');key=ob.shape_key_add(name=f'FACE_Blink.{side}');key.data.foreach_set('co',np.array(closed,dtype=np.float32).ravel())
    driver(key,'value',None,'min(max(b,0),1)',{'b':f'blink.{side}'})
    g=ob.vertex_groups.new(name='DEF_head');g.add(list(range(len(verts))),1,'REPLACE')
    am=ob.modifiers.new('Lid head ownership','ARMATURE');am.object=rig
    ob['status']='Local added eyelid candidate. Human approval pending. Original eye surface preserved.'
    lidinfo.append({'object':ob.name,'vertices':len(verts),'faces':len(faces),'source_eye_component':ci,'normal':normal.tolist(),'center':center.tolist(),'source_fit_max_residual':float(max(depth-A@coef)),'closed_surface_clearance_over_fit':'.0030-.0036; measured source fit residual .002024 maximum','neutral_addition':'Folded .00035-wide upper/lower rim strips; no Basis edits to body.'})

# Animator targets and semantic anchors are explicit exported objects with bone ownership.
body.data.calc_loop_triangles()
triangle_ids=np.array([tuple(t.vertices) for t in body.data.loop_triangles])
component_id=np.load(E/'authority-parts.npz')['component']
def surface_bvh(region):
    t=triangle_ids;center=v[t].mean(1)
    if region.startswith('wing'):
        mask=np.isin(component_id[t[:,0]],[2,4] if region.endswith('L') else [1])
    else:
        mask=component_id[t[:,0]]==0
        if region.startswith('foot'):
            normal=np.cross(v[t[:,1]]-v[t[:,0]],v[t[:,2]]-v[t[:,0]])
            mask&=(center[:,2]<.04)&(center[:,0]*(1 if region.endswith('L') else -1)>0)&(normal[:,2]<0)
    assert mask.any(),region
    return BVHTree.FromPolygons([Vector(p) for p in v],t[mask].tolist(),all_triangles=True)
surfaces={key:surface_bvh(key) for key in ['body','wingL','wingR','footL','footR']}
anchors=[]
def anchor(name,position,parentbone,size=.012):
    requested=list(position);mode='Authored stand-off / mouth or holding target; equipment/prop fit pending'
    if 'Touch' in name or 'PawContact' in name or 'FootSupport' in name:
        side=name[-1]
        region='wing'+side if 'WingRoot' in name else 'foot'+side if 'FootSupport' in name else 'body'
        query=Vector(position)
        if 'FootSupport' in name:query.z=-.005
        hit,normal,tri,dist=surfaces[region].find_nearest(query)
        position=list(hit);mode='Nearest preserved surface, '+region+(' / downward sole triangles' if 'FootSupport' in name else '')
    ob=bpy.data.objects.new(name,None);s.collection.objects.link(ob);ob.empty_display_type='SPHERE';ob.empty_display_size=size
    ob.parent=rig;ob.parent_type='BONE';ob.parent_bone=parentbone
    update();ob.matrix_world=Matrix.Translation(Vector(position));anchors.append({'name':name,'bone':parentbone,'rest_position':list(position),'requested_position':requested,'placement':mode})
    ob['semantic_owner']=parentbone;ob['approval']='Human PENDING';return ob
for side,sign in [('L',1),('R',-1)]:
    for limb,tipname in [('paw','paw'),('foot','foot')]:
        p=rig.data.bones[f'DEF_{tipname}.{side}'].head_local.copy()
        target=bpy.data.objects.new(f'CTRL_{limb}_IK.{side}',None);s.collection.objects.link(target);target.location=p;target.empty_display_type='CUBE';target.empty_display_size=.025
        target.rotation_mode='QUATERNION';target.rotation_quaternion=rig.data.bones[f'DEF_{tipname}.{side}'].matrix_local.to_quaternion()
        target['usage']='World target; influence controlled on JILL_RIG. Zero disables IK without changing FK.'
        end=rig.pose.bones[f'DEF_{"forearm" if limb=="paw" else "shin"}.{side}']
        c=end.constraints.new('IK');c.name=f'{limb} target';c.target=target;c.chain_count=2;c.use_stretch=False;c.use_tail=True;c.iterations=64
        driver(c,'influence',None,'p',{'p':f'{limb}_ik.{side}'})
        if limb=='foot':
            lock=rig.pose.bones[f'DEF_foot.{side}'].constraints.new('COPY_ROTATION');lock.name='Foot world orientation lock';lock.target=target;lock.owner_space='WORLD';lock.target_space='WORLD'
            driver(lock,'influence',None,'p',{'p':f'foot_ik.{side}'})
    anchor(f'ANCHOR_PawContact.{side}',(sign*.29,-.21,.36),f'DEF_paw.{side}')
    anchor(f'ANCHOR_FootSupport.{side}',(sign*.14,-.13,.013),f'DEF_foot.{side}')
    anchor(f'ANCHOR_CheekTouch.{side}',(sign*.155,-.325,.63),'DEF_head')
    anchor(f'ANCHOR_WingRootTouch.{side}',(sign*.09,-.11,.50),f'DEF_wing_girdle.{side}')
    anchor(f'ANCHOR_Holding.{side}',(sign*.29,-.225,.36),f'DEF_paw.{side}')
anchor('ANCHOR_HeadWear',(0,-.205,.887),'DEF_head')
anchor('ANCHOR_ChestWear',(0,-.305,.445),'DEF_chest')
anchor('ANCHOR_ChestTouch',(0,-.30,.41),'DEF_chest')
anchor('ANCHOR_Mouth',(0,-.410,.605),'DEF_head')
anchor('ANCHOR_TailRootTouch',(0,.11,.30),'DEF_tail_00')
anchor('ANCHOR_GiftAssist',(0,-.27,.37),'DEF_chest')

reset();s.frame_set(1)
rig['status']='IMPLEMENTED_REVIEW_CANDIDATE / Human visual PENDING. Check Evidence.md before use.'
rig['anatomy']='Fictional six-limb Jill: separate wing girdles and forelimb scapulae. No claimed real six-limb vertebrate anatomy.'
rig['runtime']='Blender drivers/IK are authoring only. GLB contains deform skeleton, morphs, anchors, sampled proof; see control-contract.json.'
rig['plan_commit']='832e1e89bcbfadb74f14154a87211056b997497c'
body['authority_sha256']=EXPECTED['jill-v002-authority-donor.blend'];body['texture_status']='No formal Texture. Original FBX UV copied exactly; material unchanged from v002.'
body['human_visual_gate']='PENDING / v002 existing geometry issues remain subject to review'
text=bpy.data.texts.new('READ_ME_JILL_RIG')
text.write('Jill rig-other-v001 REVIEW CANDIDATE\nSelect JILL_RIG > Object Properties > Custom Properties for semantic controls.\nPositive wing_open opens, negative folds. Each paw and wing is independent.\nWorld CTRL_*_IK targets: enable corresponding paw_ik/foot_ik.\nLeaf bones: local_bend plus regional leaves controls.\nOriginal v002 body Basis retained. Added physical upper/lower lid patches.\nGLB constraints/drivers are sampled, not portable logic. See control-contract.json and Evidence.md.\nHuman approval PENDING; no completed full Motion library or formal Texture.\n')
bpy.context.view_layer.objects.active=rig
for o in bpy.context.selected_objects:o.select_set(False)
rig.select_set(True)
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=720;s.render.resolution_y=720;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Jill_ReviewWorld');s.world.color=(.80,.80,.80)
s.view_settings.view_transform='Standard'
sh=s.display.shading;sh.light='STUDIO';sh.studiolight_rotate_z=.4;sh.color_type='MATERIAL';sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH';sh.background_type='WORLD'
cam=bpy.data.objects.new('Jill_ReviewCamera',bpy.data.cameras.new('Jill_ReviewCamera'));s.collection.objects.link(cam);s.camera=cam
cam.location=(1.4,-2.8,1.1);cam.rotation_euler=(Vector((0,0,.50))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.18
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_distance=1.65;area.spaces.active.region_3d.view_location=Vector((0,0,.5))
bpy.context.preferences.filepaths.save_version=0
output=ASSET/'jill-rig-other-v001.blend';bpy.ops.wm.save_as_mainfile(filepath=str(output))
base_error=float(np.linalg.norm(v-authority,axis=1).max())
write('build-report.json',{'blender':bpy.app.version_string,'plan_commit':rig['plan_commit'],'inputs':EXPECTED,'basis_max_delta_v002':base_error,
 'basis_vertices':n,'polygons':len(body.data.polygons),'uv_loop_max_delta':float(np.max(abs(np.array([tuple(x.uv) for x in uv.data])-uv_reference))),
 'deform_bones':len(deforms),'bones':len(spec),'leaves':[{k:v for k,v in info.items() if k!='ids'} for info in leafinfo],
 'correctives':corrections,'added_lids':lidinfo,'max_weight_sum_error':float(np.max(abs(W.sum(1)-1))),
 'max_influences':int(np.max((W>0).sum(1))),'unweighted_vertices':int(np.sum(W.sum(1)<.99999)),
 'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'human_visual':'PENDING'})
write('control-contract.json',{'status':'Review candidate, not approved performance','coordinates':'Blender Z up, front -Y, anatomical L +X; glTF Y up exported by Blender',
 'authoring_properties':controls,'deform_skeleton':spec,'anchors':anchors,'correctives':corrections,
 'portable_boundary':'IK constraints and property/pose readers are not glTF logic. Baked proof reproduces sampled outputs; arbitrary runtime combinations require reimplementing the mapping and corrective activation.',
 'layers':['support','chest','head/gaze','face','forelimbs','wings/membrane','leaves','tail','touch/holding anchors'],
 'limitations':['Human appearance approval pending','No formal Texture','No full Motion library','No PlayCanvas/phone performance claim','No flight or wing/ tail weight-bearing guarantee']})
np.savez_compressed(E/'rig-bind-data.npz',basis=v,authority=authority,weights=W,bone_names=np.array(deforms),edges=np.array([tuple(e.vertices) for e in body.data.edges]))
print('JILL_BUILD_COMPLETE',json.dumps({'bones':len(spec),'leaves':len(leafinfo),'correctives':len(corrections),'basis_error':base_error,'blend':str(output)}))
