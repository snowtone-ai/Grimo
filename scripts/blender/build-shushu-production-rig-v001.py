"""Independent editable Shushu rig derivative. Original files are read only."""
import bpy, sys, json, hashlib, subprocess, math
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from mathutils import Vector, Quaternion, Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v001'
BASE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003'
SOURCE=BASE/'rigging/shushu-v006-tripo-autorig-v001.glb'
ASSET=BASE/'rigging/shushu-v006-production-rig-v001.blend'
GLB=BASE/'rigging/shushu-v006-production-rig-v001.glb'
PROOF=BASE/'rigging/shushu-v006-production-rig-v001-proof.blend'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(n,d):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def protect():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'protected-inputs.json').exists():return
    paths=subprocess.check_output(['git','ls-files','-z','assets/grimo','docs/production/shushu'],cwd=ROOT).decode().split('\0')
    paths += subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    paths += ['docs/production/Handoff.md','docs/grimo/knowledge/Goal√map.md']
    write('protected-inputs.json',{p:sha(ROOT/p) for p in sorted(set(paths)) if p and (ROOT/p).is_file() and 'production-rig-v001' not in p})
    write('start-state.json',{'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip(),'status':subprocess.check_output(['git','status','--short'],cwd=ROOT).decode(),'input_sha256':sha(SOURCE)})
def fresh():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(SOURCE))
    meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')]
    rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
    return rig,meshes
def inventory():
    protect();rig,meshes=fresh()
    rows={'blender':bpy.app.version_string,'rig_matrix':list(map(list,rig.matrix_world)), 'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'head':list(rig.matrix_world@b.head_local),'tail':list(rig.matrix_world@b.tail_local)} for b in rig.data.bones], 'meshes':[]}
    for o in meshes:
        p=np.array([o.matrix_world@v.co for v in o.data.vertices]);tot={}
        for v in o.data.vertices:
            for g in v.groups:tot[o.vertex_groups[g.group].name]=tot.get(o.vertex_groups[g.group].name,0)+g.weight/len(p)
        rows['meshes'].append({'name':o.name,'vertices':len(p),'triangles':len(o.data.polygons),'bounds':[p.min(0).tolist(),p.max(0).tolist()],'matrix':list(map(list,o.matrix_world)),'weights':tot,'materials':[m.name for m in o.data.materials]})
    write('input-inventory.json',rows)
    print(json.dumps(rows,ensure_ascii=False),flush=True)
def donor_inventory():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/grimo/production/shushu/blender/shushu-geometry-v003.blend'))
    print(json.dumps({'controls':{o.name:{k:str(o[k])[:250] for k in o.keys()} for o in bpy.data.objects if o.keys()},'keys':{o.name:[(k.name,k.value) for k in o.data.shape_keys.key_blocks if not k.name.startswith(('Seat','Corrective.Compose','Head'))] for o in bpy.data.objects if o.type=='MESH' and o.data.shape_keys}},ensure_ascii=False),flush=True)
def evaluated(o):
    bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles()
    p=np.array([ev.matrix_world@v.co for v in m.vertices]);t=np.array([list(f.vertices) for f in m.loop_triangles]);ev.to_mesh_clear();return p,t
def extract_donor():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/grimo/production/shushu/blender/shushu-geometry-v003.blend'))
    objs=[o for o in bpy.data.objects if o.name.startswith('Shushu_') and o.type=='MESH' and o.data.shape_keys and o.get('part') not in ['Torso','Leg.L','Leg.R','Paw.L','Paw.R']]
    for o in objs:
        if o.data.shape_keys.animation_data:o.data.shape_keys.animation_data.action=None
        for k in o.data.shape_keys.key_blocks:k.value=0
        o.data.update();o.update_tag()
    bpy.context.view_layer.update()
    output={};record={}
    wanted=['Blink.L','Blink.R','Corrective.HalfBlink.L','Corrective.HalfBlink.R','GentleSmile','HappyLids','MouthOpen','MouthDonorOpen','Surprise','CheekPressure.L','GazeLeft','GazeRight','GazeUp','GazeDown','Breath']
    # Store evaluated DIFFERENCES, never old absolute key coordinates.
    for o in objs:
        name=o.name.replace('Shushu_','').replace('.','_');base,t=evaluated(o)
        output[name+'__base']=base;output[name+'__tri']=t;record[name]={'bounds':[base.min(0).tolist(),base.max(0).tolist()],'vertices':len(base),'keys':[]}
        sk=o.data.shape_keys
        if sk.animation_data:
            for d in sk.animation_data.drivers:d.mute=True
        for label in wanted:
            if label not in sk.key_blocks:continue
            sk.key_blocks[label].value=1;o.data.update();o.update_tag();p,tt=evaluated(o)
            assert len(p)==len(base),(name,label,'vertex count change',len(p),len(base))
            output[name+'__'+label]=p-base;record[name]['keys'].append(label)
            sk.key_blocks[label].value=0;o.data.update();o.update_tag()
    np.savez_compressed(OUT/'donor-displacements.npz',**output)
    write('donor-displacements.json',{'source_sha256':sha(ROOT/'assets/grimo/production/shushu/blender/shushu-geometry-v003.blend'),'method':'read-only evaluated displacement fields with stable vertex count per key; no old absolute coordinates copied; triangulation can change','objects':record})
    print('DONOR_EXTRACTED',flush=True)
PREFIX='mixamorig:'
def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def driver(owner,path,rig,expression,variables,index=None):
    d=(owner.driver_add(path) if index is None else owner.driver_add(path,index)).driver
    for name,property_name in variables.items():
        v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["'+property_name+'"]'
    d.expression=expression
def prop(rig,name,value=0,minimum=0,maximum=1,description=''):
    rig[name]=float(value);rig.id_properties_ui(name).update(min=minimum,max=maximum,soft_min=minimum,soft_max=maximum,description=description)
def shape(o,name,delta):
    if not o.data.shape_keys:o.shape_key_add(name='Basis')
    k=o.shape_key_add(name=name);base=np.array([v.co for v in o.data.vertices]);k.data.foreach_set('co',(base+np.asarray(delta)).astype(np.float32).ravel());return k
def empty(name,location):
    o=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(o);o.location=location;o.empty_display_type='SPHERE';o.empty_display_size=.022;return o
def weights_replace(o,assign):
    for vg in list(o.vertex_groups):o.vertex_groups.remove(vg)
    groups={}
    for i,weights in enumerate(assign):
        # Match the Blender glTF round-trip minimum; retain every meaningful influence.
        weights={n:float(w) for n,w in weights.items() if w>1e-4};total=sum(weights.values());assert total>0
        for n,w in weights.items():
            if n not in groups:groups[n]=o.vertex_groups.new(name=n)
            groups[n].add([i],w/total,'REPLACE')
def repair_weights(rig,meshes):
    records=[]
    for o in meshes:
        old=[{o.vertex_groups[g.group].name:g.weight for g in v.groups} for v in o.data.vertices];new=[];role=o.name.removeprefix('ShushuStatic_')
        for v,ww in zip(o.data.vertices,old):
            x,y,z=v.co
            if role.startswith('Paw_'):
                side='Left' if role.endswith('L') else 'Right';nw={}
                for n,w in ww.items():
                    if n.startswith(PREFIX+side+'Hand'):dest=PREFIX+side+'Hand'
                    elif n in [PREFIX+side+k for k in ['Shoulder','Arm','ForeArm']]:dest=n
                    else:dest=PREFIX+side+'Shoulder'
                    nw[dest]=nw.get(dest,0)+w
                root=float(smooth(.405,.470,z)*(1-smooth(.26,.32,abs(x))))
                nw={n:w*(1-root) for n,w in nw.items()};nw[PREFIX+'Spine2']=root
                new.append(nw)
            elif role=='Torso':
                nw={}
                for n,w in ww.items():
                    dest=PREFIX+'Spine2' if any(token in n for token in ['Shoulder','Arm','Hand']) else n;nw[dest]=nw.get(dest,0)+w
                leg_release=float(smooth(.23,.34,z));owned={}
                for n,w in nw.items():
                    if any(token in n for token in ['UpLeg','Leg','Foot','ToeBase']):
                        owned[n]=owned.get(n,0)+w*(1-leg_release);owned[PREFIX+'Hips']=owned.get(PREFIX+'Hips',0)+w*leg_release
                    else:owned[n]=owned.get(n,0)+w
                nw=owned
                abdomen=float(smooth(.135,.215,z)*(1-smooth(.30,.37,z))*(1-smooth(.17,.245,abs(x))))
                posterior=float(smooth(.025,.12,y)*smooth(.11,.17,z)*(1-smooth(.24,.30,z))*(1-smooth(.10,.23,abs(x))))
                owner=max(abdomen,posterior);nw={n:w*(1-owner) for n,w in nw.items()};nw[PREFIX+'Hips']=nw.get(PREFIX+'Hips',0)+owner
                sole=float(1-smooth(.085,.140,z));side='Left' if x>=0 else 'Right';nw={n:w*(1-sole) for n,w in nw.items()};nw[PREFIX+side+'Foot']=nw.get(PREFIX+side+'Foot',0)+sole
                new.append(nw)
            elif role=='Head':
                h=float(smooth(.478,.528,z));new.append({PREFIX+'Head':h,PREFIX+'Neck':1-h})
            elif role.startswith('Ear_'):
                side=role[-1];w=float(smooth(.785,.850,z));new.append({'Ear.'+side:w,PREFIX+'Head':1-w})
            else:new.append({PREFIX+'Head':1})
        weights_replace(o,new)
        records.append({'mesh':o.name,'changed_vertices':sum(any(abs(a.get(k,0)-b.get(k,0)/sum(b.values()))>1e-6 for k in set(a)|set(b)) for a,b in zip(old,new)),'groups_after':list(o.vertex_groups.keys())})
    write('weight-repair.json',{'minimum_retained_weight':1e-4,'reason':'Exporter/importer omit very small bone influences; normalize before authoring inverse LBS correctives so saved GLB matches editable rig.','meshes':records})
def edit_skeleton(rig):
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT');changes=[]
    for side,s in [('Left',1),('Right',-1)]:
        up=rig.data.edit_bones[PREFIX+side+'UpLeg'];leg=rig.data.edit_bones[PREFIX+side+'Leg'];foot=rig.data.edit_bones[PREFIX+side+'Foot']
        changes.append({'bone':up.name,'old_head':list(up.head),'old_tail':list(up.tail),'reason':'Thigh root surface near Z .21; original .127 joint inside lower leg cannot support the short seated thigh.'})
        up.use_connect=False;leg.use_connect=False;foot.use_connect=False;up.head=(s*.132,0,.213);up.tail=(s*.135,-.020,.120);leg.head=up.tail;leg.tail=foot.head
    for side,s in [('L',1),('R',-1)]:
        b=rig.data.edit_bones.new('Ear.'+side);b.head=(s*.202,.074,.827);b.tail=(s*.237,.080,.936);b.parent=rig.data.edit_bones[PREFIX+'Head'];b.use_deform=True
        changes.append({'bone':b.name,'head':list(b.head),'tail':list(b.tail),'reason':'Independent existing ear mesh owner, rooted within attached ear volume.'})
    bpy.ops.object.mode_set(mode='OBJECT');rig.name='Shushu_ProductionRig_v001';rig.show_in_front=True;write('skeleton-repair.json',changes)
def add_controls(rig):
    for name in ['Seat','Rest','Blink.L','Blink.R','Smile','Joy','Surprise','Hesitate','Discomfort','MouthClose','MouthOpen','Tongue','CheekPressure.L','CheekPressure.R','BellyPressure','Breath','Hold.L','Hold.R','Offer.L','Offer.R','SelfContact.L','SelfContact.R','FootLift.L','FootLift.R']:
        prop(rig,name,description='Independent bounded local rig channel')
    for name in ['WeightShift','HeadYaw','HeadPitch','HeadRoll','NeckPitch','Ear.L','Ear.R','Wrist.L','Wrist.R','FootSide.L','FootSide.R','FootForward.L','FootForward.R','GazeX.L','GazeX.R','GazeY.L','GazeY.R']:prop(rig,name,minimum=-1)
    hips=rig.pose.bones[PREFIX+'Hips'];inv=hips.bone.matrix_local.to_3x3().inverted();seat=inv@Vector((0,.055,-.115));shift=inv@Vector((.024,0,0))
    for i in range(3):driver(hips,'location',rig,f'{seat[i]}*s+{shift[i]}*w',{'s':'Seat','w':'WeightShift'},i)
    for name,variables in [('Head',{'yaw':'HeadYaw','pitch':'HeadPitch','roll':'HeadRoll'}),('Neck',{'pitch':'NeckPitch','rest':'Rest'})]:
        b=rig.pose.bones[PREFIX+name];b.rotation_mode='XYZ';axes=b.bone.matrix_local.to_3x3().inverted()
        terms=[(axes@Vector((0,0,1)),math.radians(18),'yaw'),(axes@Vector((1,0,0)),math.radians(12),'pitch'),(axes@Vector((0,1,0)),math.radians(12),'roll')] if name=='Head' else [(axes@Vector((1,0,0)),math.radians(10),'pitch'),(axes@Vector((1,0,0)),math.radians(8),'rest')]
        for i in range(3):driver(b,'rotation_euler',rig,'+'.join(f'{a[i]*angle}*{v}' for a,angle,v in terms),variables,i)
    for side in ['L','R']:
        b=rig.pose.bones['Ear.'+side];b.rotation_mode='XYZ';axis=b.bone.matrix_local.to_3x3().inverted()@Vector((0,1,0))
        for i in range(3):driver(b,'rotation_euler',rig,f'{axis[i]*math.radians(12)}*e',{'e':'Ear.'+side},i)
    for side,s in [('Left',1),('Right',-1)]:
        foot=rig.data.bones[PREFIX+side+'Foot'];target=empty('CTRL_Foot.'+side,foot.head_local);target.rotation_mode='QUATERNION';target.rotation_quaternion=foot.matrix_local.to_quaternion()
        # Keep the planted soles at their existing support coordinates throughout the low-seat transition.
        short='L' if side=='Left' else 'R'
        driver(target,'location',rig,f'{foot.head_local.x}+.025*v',{'v':'FootSide.'+short},0);driver(target,'location',rig,f'{foot.head_local.y}-.025*v',{'v':'FootForward.'+short},1);driver(target,'location',rig,f'{foot.head_local.z}+.040*v',{'v':'FootLift.'+short},2)
        pole=empty('CTRL_KneePole.'+side,(s*.135,-.4,.22));ik=rig.pose.bones[PREFIX+side+'Leg'].constraints.new('IK');ik.name='Supported ankle no stretch';ik.target=target;ik.pole_target=pole;ik.chain_count=2;ik.use_stretch=False;ik.iterations=100;ik.pole_angle=math.pi/2 if side=='Left' else -math.pi/2
        driver(ik,'influence',rig,'min(1,max(s,abs(w),l,abs(x),abs(y))*50)',{'s':'Seat','w':'WeightShift','l':'FootLift.'+short,'x':'FootSide.'+short,'y':'FootForward.'+short})
        for suffix in ['UpLeg','Leg']:rig.pose.bones[PREFIX+side+suffix].ik_stretch=0
        pb=rig.pose.bones[PREFIX+side+'Foot'];location=pb.constraints.new('COPY_LOCATION');location.name='World sole pin independent of leg IK blend';location.target=target;location.owner_space='WORLD';location.target_space='WORLD'
        rotation=pb.constraints.new('COPY_ROTATION');rotation.name='Sole orientation';rotation.target=target;rotation.owner_space='WORLD';rotation.target_space='WORLD'
def reset(rig):
    for k in rig.keys():
        if isinstance(rig[k],float):rig[k]=0.
    for b in rig.pose.bones:b.location=(0,0,0);b.rotation_mode='XYZ';b.rotation_euler=(0,0,0);b.scale=(1,1,1)
    rig.update_tag();bpy.context.view_layer.update()
def authoring_setup(rig):
    labels=['Body and support','Head and ears','Left arm','Right arm','Compatibility fingers']
    for c in list(rig.data.collections):rig.data.collections.remove(c)
    collections={name:rig.data.collections.new(name) for name in labels}
    for bone in rig.data.bones:
        name=bone.name
        if any(x in name for x in ['Thumb','Index','Middle','Ring','Pinky']):group='Compatibility fingers'
        elif name in [PREFIX+'Head',PREFIX+'Neck','Ear.L','Ear.R']:group='Head and ears'
        elif 'Left' in name and any(x in name for x in ['Shoulder','Arm','Hand']):group='Left arm'
        elif 'Right' in name and any(x in name for x in ['Shoulder','Arm','Hand']):group='Right arm'
        else:group='Body and support'
        collections[group].assign(bone)
    collections['Compatibility fingers'].is_visible=False;rig.data.display_type='STICK'
    rig['Rig guide']='Object Properties > Custom Properties. Neutral = all numeric controls zero. Pose bones remain editable. Foot targets stay planted; choose one reach purpose per paw. See production-rig-v001/REVIEW.md for measured domain and HOLDs.'
    text=bpy.data.texts.new('SHUSHU_RIG_README');text.write('Shushu v006 production rig v001\n\nEditable source, not Human approval.\nNeutral: all numeric rig properties = 0.\n\nHeadYaw/Pitch/Roll, NeckPitch and Ear.L/R: independent small attention.\nBlink.L/R: 0 open / .5 half / 1 closed. GazeX/Y.L/R retained through blink.\nSmile/Joy/Surprise/Hesitate/Discomfort: bounded affect layers.\nMouthClose wins over MouthOpen/Tongue; small oral cavity + separate tongue.\nSeat: 0 standing / 1 supported low seat. Rest: small neck/drowsy layer.\nWeightShift: -1..1, planted sole targets. Spine/Hips/limb FK remains editable.\nFootLift.L/R: 0..1 = up to .040m; FootSide/Forward.L/R: -1..1 = .025m.\nFoot bones follow world sole pins; edit CTRL_Foot.L/R rotation for orientation.\nOffer/Hold/SelfContact.L/R: choose one reach purpose per paw. Opposite paws independent.\nWrist.L/R: separate small hand rotation. CheekPressure.L/R/BellyPressure/Breath: local.\nANCHOR_Hold.L/R: calibrated radius .030 fixture center, .031 forward of distal paw.\nANCHOR_Crown is head-owned crown reference only, not ordinary head-top Wear approval.\nWearEar.L/R, WearChest and Mouth are editable owner references; item clearance needs QA.\n\nBody/ear/arm collections organize the original hierarchy. Unweighted compatibility finger bones hidden.\nProof .blend keeps drivers/IK + 24fps markers. GLB bakes ordinary skin/morph/anchor channels.\nRead evidence/production-rig-v001/REVIEW.md and capability matrix before adoption.\n')
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                space=area.spaces.active;space.shading.type='MATERIAL';space.region_3d.view_location=(0,0,.5);space.region_3d.view_distance=1.5;space.region_3d.view_rotation=Vector((-.65,-.76,.12)).to_track_quat('Z','Y');space.region_3d.view_perspective='ORTHO'
    for o in bpy.data.objects:
        if o.name=='Icosphere':o.hide_set(True)
def bary_mapping(source,tri,target):
    tree=BVHTree.FromPolygons(source.tolist(),tri.tolist(),all_triangles=True);ids=[];weights=[];distance=[]
    for p in target:
        co,_,i,d=tree.find_nearest(Vector(p));a,b,c=source[tri[i]];v0=b-a;v1=c-a;v2=np.array(co)-a
        d00=np.dot(v0,v0);d01=np.dot(v0,v1);d11=np.dot(v1,v1);den=d00*d11-d01*d01
        if abs(den)<1e-20:w=np.array([1.,0,0])
        else:
            v=(d11*np.dot(v2,v0)-d01*np.dot(v2,v1))/den;w2=(d00*np.dot(v2,v1)-d01*np.dot(v2,v0))/den;w=np.clip([1-v-w2,v,w2],0,1);w/=sum(w)
        ids.append(tri[i]);weights.append(w);distance.append(d)
    return np.array(ids),np.array(weights),np.array(distance)
def transfer_faces(rig,meshes):
    data=np.load(OUT/'donor-displacements.npz');record=[]
    for o in meshes:
        role=o.name.removeprefix('ShushuStatic_');key=role
        if key+'__base' not in data or role.startswith(('Torso','Paw_','Ear_')):continue
        p=np.array([v.co for v in o.data.vertices]);source=data[key+'__base'];tri=data[key+'__tri']
        scale=np.array([1.008,1.008,1.008]);registered=source*scale
        ids,w,dist=bary_mapping(registered,tri,p);changed={}
        for entry in data.files:
            if not entry.startswith(key+'__') or entry.endswith(('__base','__tri')):continue
            label=entry.split('__')[1];delta=(data[entry][ids]*w[:,:,None]).sum(1)*scale
            if label in ['CheekPressure.L','MouthDonorOpen','Corrective.ClosedRetraction.L','Corrective.ClosedRetraction.R']:continue
            if label=='GentleSmile':label='Smile'
            if label=='HappyLids':label='JoyLids'
            if label.startswith('Blink.') and role.startswith(('Head','LidWall')):
                matched=(registered[ids]*w[:,:,None]).sum(1);strength=smooth(.005,.035,np.linalg.norm(delta,axis=1));delta-=(p-matched)*strength[:,None]
            if np.linalg.norm(delta,axis=1).max()<1e-6:continue
            if label.startswith('Gaze'):
                if not role.startswith('Eye_'):continue
                side=role[-1];axis='X' if label in ['GazeLeft','GazeRight'] else 'Y';sign=-1 if label in ['GazeLeft','GazeDown'] else 1
                sk=shape(o,label+'.'+side,delta);driver(sk,'value',rig,f'max(0,{sign}*v)*(1-max(0,(max(b,r*.55)-.9)/.1))',{'v':f'Gaze{axis}.{side}','b':'Blink.'+side,'r':'Rest'})
            else:
                sk=shape(o,label,delta)
                if label.startswith('Corrective.HalfBlink.'):
                    side=label[-1];driver(sk,'value',rig,'max(0,1-abs(max(b,r*.55)-.5)*2)',{'b':'Blink.'+side,'r':'Rest'})
                elif label.startswith('Blink.'):
                    driver(sk,'value',rig,'max(b,r*.55)',{'b':label,'r':'Rest'})
                elif label=='Smile':driver(sk,'value',rig,'min(1,s+j*.65)',{'s':'Smile','j':'Joy'})
                elif label=='JoyLids':driver(sk,'value',rig,'j*.15',{'j':'Joy'})
                elif label=='MouthOpen':driver(sk,'value',rig,'v*(1-c)',{'v':label,'c':'MouthClose'})
                elif label=='Surprise':driver(sk,'value',rig,'v',{'v':label})
            changed[label]=float(np.linalg.norm(delta,axis=1).max())
        record.append({'mesh':o.name,'mapping':'nearest triangle barycentric displacement / current Basis unchanged','registration_scale':scale.tolist(),'surface_distance_max':float(dist.max()),'surface_distance_p95':float(np.percentile(dist,95)),'keys':changed})
    write('morph-transfer.json',record)
def local_faces(rig,meshes):
    for o in meshes:
        role=o.name.removeprefix('ShushuStatic_');p=np.array([v.co for v in o.data.vertices]);x,y,z=p.T
        if role=='Head':
            for side,s in [('L',1),('R',-1)]:
                w=np.exp(-2*(((x-s*.23)/.065)**2+((y+.19)/.08)**2+((z-.575)/.07)**2));sk=shape(o,'CheekPressure.'+side,np.c_[-s*.012*w,.007*w,np.zeros(len(p))]);driver(sk,'value',rig,'p',{'p':'CheekPressure.'+side})
            for name,amplitude in [('Hesitate',.006),('Discomfort',-.006)]:
                w=np.exp(-2*(((np.abs(x)-.13)/.065)**2+((z-.708)/.045)**2))*smooth(.04,.12,-y);sk=shape(o,name,np.c_[np.zeros(len(p)),np.zeros(len(p)),amplitude*w]);driver(sk,'value',rig,'v',{'v':name})
            w=(1-smooth(.034,.055,np.abs(x)))*smooth(.545,.570,z)*(1-smooth(.607,.617,z))*smooth(.17,.23,-y);seam=.601+.005*(x/.035)**2;sk=shape(o,'MouthClose',np.c_[np.zeros(len(p)),np.zeros(len(p)),(seam-z)*w*.985]);driver(sk,'value',rig,'c',{'c':'MouthClose'})
            w=np.exp(-2*((x/.025)**2+((z-.588)/.016)**2))*smooth(.18,.23,-y);sk=shape(o,'Corrective.MouthCavity',np.c_[np.zeros(len(p)),.045*w,np.zeros(len(p))]);driver(sk,'value',rig,'max(o,t)*(1-c)',{'o':'MouthOpen','t':'Tongue','c':'MouthClose'})
        elif role=='MouthInterior':
            w=np.ones(len(p));sk=shape(o,'MouthClose',np.c_[np.zeros(len(p)),.004*w,(.612-z)*.8]);driver(sk,'value',rig,'c',{'c':'MouthClose'})
            w=1-smooth(.602,.605,z);sk=shape(o,'Tongue',np.c_[np.zeros(len(p)),-.008*w,-.003*w]);driver(sk,'value',rig,'t*(1-c)',{'t':'Tongue','c':'MouthClose'})
        elif role.startswith('Eye_'):
            side=role[-1];sk=shape(o,'Corrective.ClosedRetraction.'+side,np.tile((0,.018,0),(len(p),1)));driver(sk,'value',rig,'max(0,(max(b,r*.55)-.55)/.45)',{'b':'Blink.'+side,'r':'Rest'})
            center=np.array((.11 if side=='L' else -.11,.10,.80));sk=shape(o,'Corrective.ClosedSeal.'+side,(center-p)*.98);driver(sk,'value',rig,'max(0,(max(b,r*.55)-.9)/.1)',{'b':'Blink.'+side,'r':'Rest'})
        elif role=='Torso':
            w=np.exp(-2*((x/.09)**2+((y+.21)/.065)**2+((z-.30)/.10)**2));sk=shape(o,'BellyPressure',np.c_[np.zeros(len(p)),.014*w,np.zeros(len(p))]);driver(sk,'value',rig,'v',{'v':'BellyPressure'})
            w=np.exp(-2*((x/.20)**2+((y+.13)/.2)**2+((z-.32)/.12)**2));sk=shape(o,'Breath',np.c_[.001*x*w,-.002*w,np.zeros(len(p))]);driver(sk,'value',rig,'v',{'v':'Breath'})
def paw_controls(rig):
    for side,s,longname in [('L',1,'Left'),('R',-1,'Right')]:
        bone=rig.data.bones[PREFIX+longname+'Hand'];base=bone.head_local.copy();target=empty('CTRL_Paw.'+side,base);pole=empty('CTRL_ElbowPole.'+side,(s*.45,.17,.40))
        pole.location=(s*.40,-.30,.27);dest={'h':Vector((s*.14,-.205,.38)),'o':Vector((s*.26,-.145,.35)),'c':Vector((s*.16,-.19,.40))}
        shoulder=rig.pose.bones[PREFIX+longname+'Shoulder'];shift=shoulder.bone.matrix_local.to_3x3().inverted()@Vector((0,-.045,0))
        for i in range(3):driver(shoulder,'location',rig,f'{shift[i]}*min(1,h+c)',{'h':'Hold.'+side,'c':'SelfContact.'+side},i)
        for i in range(3):
            extra=['0','.055*s','-.115*s'][i]
            expression=f'{base[i]}+('+'+'.join(f'{v[i]-base[i]}*{k}' for k,v in dest.items())+')/max(1,h+o+c)+'+extra
            driver(target,'location',rig,expression,{'h':'Hold.'+side,'o':'Offer.'+side,'c':'SelfContact.'+side,'s':'Seat'},i)
        ik=rig.pose.bones[PREFIX+longname+'ForeArm'].constraints.new('IK');ik.name='Reachable low paw / hold / self contact';ik.target=target;ik.pole_target=pole;ik.chain_count=2;ik.use_stretch=False;ik.iterations=80
        driver(ik,'influence',rig,'min(1,h+o+c)',{'h':'Hold.'+side,'o':'Offer.'+side,'c':'SelfContact.'+side})
        hand=rig.pose.bones[bone.name];hand.rotation_mode='XYZ';driver(hand,'rotation_euler',rig,'w*.35',{'w':'Wrist.'+side},1)
        anchor=empty('ANCHOR_Hold.'+side,(s*.13,-.255,.38));anchor.parent=rig;anchor.parent_type='BONE';anchor.parent_bone=bone.name
        anchor.matrix_world=Matrix.Translation(base+Vector((0,-.075,0)));anchor['purpose']='Paw-owned fixture transform. Prop release must preserve evaluated world transform.'
    crown=empty('ANCHOR_Crown',(0,.0,.93));crown.parent=rig;crown.parent_type='BONE';crown.parent_bone=PREFIX+'Head';crown.matrix_world=Matrix.Translation((0,0,.93));crown['purpose']='Head-owned attachment; no accessory appearance or product ownership decision.'
def setup_review(size=512,samples=8):
    import importlib.util
    spec=importlib.util.spec_from_file_location('autorig_review',ROOT/'scripts/blender/review-shushu-autorig-v001.py');u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
    scene,cam=u.setup();scene.render.resolution_x=scene.render.resolution_y=size;scene.cycles.samples=samples;return scene,cam
STATES=[('neutral',{}),('head-left',{'HeadYaw':.83}),('head-right',{'HeadYaw':-.83}),('head-tilt-blink',{'HeadRoll':.83,'Blink.L':1,'Blink.R':.5}),('ear-L',{'Ear.L':1}),('ear-R',{'Ear.R':-1}),('half',{'Blink.L':.5,'Blink.R':.5}),('closed',{'Blink.L':1,'Blink.R':1}),('wink-L',{'Blink.L':1}),('wink-R',{'Blink.R':1}),('gaze-L',{'GazeX.L':-1,'GazeX.R':-1}),('gaze-R',{'GazeX.L':1,'GazeX.R':1}),('smile',{'Smile':1}),('joy',{'Joy':1,'Blink.L':.25,'Blink.R':.25}),('surprise',{'Surprise':1}),('hesitate',{'Hesitate':1,'Blink.L':.15,'GazeX.L':-.4,'GazeX.R':-.4}),('discomfort',{'Discomfort':1,'Blink.L':.2,'Blink.R':.2}),('mouth-close',{'MouthClose':1}),('mouth-open-tongue',{'MouthOpen':.6,'Tongue':1}),('pressure-L',{'CheekPressure.L':1,'BellyPressure':1}),('pressure-R',{'CheekPressure.R':1}),('shift-L',{'WeightShift':1}),('shift-R',{'WeightShift':-1}),('seat-entry',{'Seat':.25}),('seat-mid',{'Seat':.5}),('seat',{'Seat':1}),('seat-rest',{'Seat':1,'Rest':1}),('seat-joy',{'Seat':1,'Joy':1,'Blink.L':.3,'Blink.R':.3}),('offer-L',{'Offer.L':1,'WeightShift':-.5}),('offer-R',{'Offer.R':1,'WeightShift':.5}),('self-L',{'SelfContact.L':1}),('self-R',{'SelfContact.R':1}),('hold-L-touch-R',{'Hold.L':1,'CheekPressure.R':.7,'HeadYaw':-.2}),('hold-both',{'Hold.L':1,'Hold.R':1}),('seat-hold-interrupt',{'Seat':1,'Hold.L':1,'SelfContact.R':1,'Blink.R':.7,'CheekPressure.R':.6}),('release',{})]
def state(rig,values):
    reset(rig)
    for k,v in values.items():rig[k]=float(v)
    rig.update_tag();bpy.context.view_layer.update()
def preview():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')];scene,cam=setup_review();iteration=sys.argv[sys.argv.index('--iteration')+1] if '--iteration' in sys.argv else '01';folder=OUT/'iterations'/iteration;folder.mkdir(parents=True,exist_ok=True);records=[]
    for name,values in STATES:
        if '--names' in sys.argv and name not in sys.argv[sys.argv.index('--names')+1].split(','):continue
        if '--all' not in sys.argv and name not in ['neutral','closed','half','smile','mouth-close','mouth-open-tongue','seat-mid','seat','offer-L','self-L','hold-both']:continue
        state(rig,values);points=evaluated(next(o for o in meshes if o.name.endswith('Torso')))[0];records.append({'name':name,'torso_min_z':float(points[:,2].min()),'below_floor':int((points[:,2]<-.001).sum())})
        for view,d in [('front',(0,-1,0)),('side',(-1,0,0))] if name in ['seat','seat-mid','closed','mouth-close','mouth-open-tongue','offer-L','self-L','hold-both'] else [('front',(0,-1,0))]:
            direction=Vector(d);cam.location=Vector((0,0,.5))+direction*3;cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/(name+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
        print('PREVIEW',name,records[-1],flush=True)
    write('iteration-'+iteration+'.json',records)
def tongue_mesh(rig,meshes):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1,location=(0,-.240,.595));o=bpy.context.object;o.name='ShushuStatic_Tongue';o.scale=(.011,.007,.0035);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    # New local oral control only. Existing 12 textures/UVs remain untouched.
    mat=bpy.data.materials.new('Shushu controlled tongue');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.8,.15,.23,1);bs.inputs['Roughness'].default_value=.65;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    o.parent=rig;o.matrix_parent_inverse=rig.matrix_world.inverted();modifier=o.modifiers.new('Head owner','ARMATURE');modifier.object=rig;weights_replace(o,[{PREFIX+'Head':1} for _ in o.data.vertices]);sk=shape(o,'Tongue',np.tile((0,-.029,-.015),(len(o.data.vertices),1)));driver(sk,'value',rig,'t*(1-c)',{'t':'Tongue','c':'MouthClose'})
    sk=shape(o,'Corrective.ClosedOralRetraction',np.tile((0,.06,0),(len(o.data.vertices),1)));driver(sk,'value',rig,'c',{'c':'MouthClose'});meshes.append(o)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=1,location=(0,-.245,.587));o=bpy.context.object;o.name='ShushuStatic_OralBowl';o.scale=(.023,.012,.016);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    mat=bpy.data.materials.new('Shushu local oral cavity');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.16,.018,.023,1);bs.inputs['Roughness'].default_value=.8;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    o.parent=rig;o.matrix_parent_inverse=rig.matrix_world.inverted();modifier=o.modifiers.new('Head owner','ARMATURE');modifier.object=rig;weights_replace(o,[{PREFIX+'Head':1} for _ in o.data.vertices]);sk=shape(o,'Corrective.ClosedOralRetraction',np.tile((0,.06,0),(len(o.data.vertices),1)));driver(sk,'value',rig,'c',{'c':'MouthClose'});meshes.append(o)
def paw_correctives(rig,meshes):
    records=[];torso=next(o for o in meshes if o.name=='ShushuStatic_Torso')
    for side,longname in [('L','Left'),('R','Right')]:
        o=next(o for o in meshes if o.name=='ShushuStatic_Paw_'+side);p=np.array([v.co for v in o.data.vertices]);root=rig.data.bones[PREFIX+longname+'Shoulder'].head_local.copy();hand=rig.data.bones[PREFIX+longname+'Hand'].head_local.copy();axis=(hand-root).normalized();length=(hand-root).length
        u=((p-np.array(root))@np.array(axis))/length;attached=smooth(.10,.75,u)
        for mode in ['Hold','Offer','SelfContact']:
            for t in [.25,.5,.75,1.]:
                for seat in [0,1]:
                    state(rig,{mode+'.'+side:t,'Seat':seat});actual,_=evaluated(o);offset=Vector((0,.055*seat,-.115*seat));endpoint=rig.pose.bones[PREFIX+longname+'Hand'].head.copy();direction=(endpoint-root-offset).normalized();rotation=np.array(axis.rotation_difference(direction).to_matrix());q=(p-np.array(root))@rotation.T+np.array(root)
                    # Retain the existing plush cross section and length; bend around a fixed attached root.
                    target=p+(q-p)*attached[:,None]+np.array(offset);tp,tt=evaluated(torso);tree=BVHTree.FromPolygons(tp.tolist(),tt.tolist(),all_triangles=True);collision=smooth(.4,.85,u)
                    for i,point in enumerate(target):
                        if collision[i]<=0:continue
                        co,_,_,_=tree.ray_cast(Vector((point[0],-1,point[2])),Vector((0,1,0)),2)
                        if co is not None and point[1]>co.y-.001:target[i,1]+=(co.y-.001-point[1])*collision[i]
                    matrices=skin_matrices(rig,o);delta=np.linalg.solve(matrices[:,:3,:3],(target-actual)[:,:,None])[:,:,0]
                    name=f'Corrective.{mode}{int(t*100):03d}.Seat{seat}';sk=shape(o,name,delta)
                    expression=f'max(0,1-abs(v-{t})/.25)' if t<1 else 'max(0,(v-.75)/.25)';expression=f'({expression})*'+('s' if seat else '(1-s)')
                    driver(sk,'value',rig,expression,{'v':mode+'.'+side,'s':'Seat'})
                    records.append({'side':side,'mode':mode,'value':t,'seat':seat,'world_correction_max':float(np.linalg.norm(target-actual,axis=1).max()),'local_max':float(np.linalg.norm(delta,axis=1).max()),'skin_condition_max':float(np.linalg.cond(matrices[:,:3,:3]).max()),'method':'Current neutral surface displacement; smooth attached-root rotation, plush cross section retained, distal surface contact clearance, inverse LBS corrective.'})
    reset(rig);write('paw-correctives.json',records)
def calibrate_anchors(rig,meshes):
    record=[]
    for side in ['L','R']:
        o=next(o for o in meshes if o.name=='ShushuStatic_Paw_'+side);anchor=bpy.data.objects['ANCHOR_Hold.'+side];base=np.array([v.co for v in o.data.vertices]);mask=np.abs(base[:,0])>.26;index=None;local=[]
        for seat in [0,1]:
            state(rig,{'Hold.'+side:1,'Seat':seat});p,_=evaluated(o)
            if index is None:ids=np.where(mask)[0];index=int(ids[np.argmin(p[ids,1])])
            center=Vector(p[index])+Vector((0,-.031,0));anchor.matrix_world=Matrix.Translation(center);bpy.context.view_layer.update();local.append(anchor.location.copy())
        for i in range(3):driver(anchor,'location',rig,f'{local[0][i]}+({local[1][i]-local[0][i]})*s',{'s':'Seat'},i)
        anchor['surface_vertex']=index;anchor['purpose']='Calibrated distal paw tangent fixture center: 0.031 forward for radius 0.030. Seat surface corrective follows independently.';record.append({'side':side,'surface_vertex':index,'local_seat_0':list(local[0]),'local_seat_1':list(local[1])})
    for name,bone,loc in [('WearEar.L','Ear.L',(.25,.08,.88)),('WearEar.R','Ear.R',(-.25,.08,.88)),('WearChest',PREFIX+'Spine2',(0,-.18,.45)),('Mouth',PREFIX+'Head',(0,-.278,.585))]:
        reset(rig);o=empty('ANCHOR_'+name,loc);o.parent=rig;o.parent_type='BONE';o.parent_bone=bone;o.matrix_world=Matrix.Translation(loc);o['purpose']='Editable reference owner anchor; actual Wear/Food object clearance still requires its own gate.'
    reset(rig);write('anchor-calibration.json',record)
def read_glb(path):
    import struct
    raw=Path(path).read_bytes();length=struct.unpack_from('<I',raw,12)[0];return json.loads(raw[20:20+length]),raw[28+length:]
def glb_accessor(j,b,i):
    a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];dtype={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
    return np.ndarray((a['count'],n),dtype=dtype,buffer=b,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',np.dtype(dtype).itemsize*n),np.dtype(dtype).itemsize)).copy()
def restore_eye_depth(meshes):
    reference=BASE/'rigprep/shushu-v006-rigprep-lowpoly-v001.glb';j,b=read_glb(reference);records=[]
    for side in ['L','R']:
        name='ShushuStatic_Eye_'+side;node=next(n for n in j['nodes'] if n.get('name')==name);a=j['meshes'][node['mesh']]['primitives'][0]['attributes'];p=glb_accessor(j,b,a['POSITION']);o=next(o for o in meshes if o.name==name);current=np.array([v.co for v in o.data.vertices]);offset=float((-p[:,2].min()-p[:,2].max()-current[:,1].min()-current[:,1].max())/2)
        for v in o.data.vertices:v.co.y+=offset
        records.append({'mesh':name,'blender_y_offset':offset,'reference_sha256':sha(reference),'method':'Uniform eye-depth shift matching approved static reference bounds; no old shape-key coordinates.'})
    write('eye-depth-restoration.json',records)
def diagnose():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');o=bpy.data.objects['ShushuStatic_Torso'];base=np.array([v.co for v in o.data.vertices]);rows=[]
    for t in np.linspace(0,1,21):
        state(rig,{'Seat':float(t)});p,_=evaluated(o);bad=np.argsort(p[:,2])[:8]
        rows.append({'seat':float(t),'min_z':float(p[:,2].min()),'bad':[{'index':int(i),'rest':base[i].tolist(),'pose':p[i].tolist(),'weights':{o.vertex_groups[g.group].name:g.weight for g in o.data.vertices[i].groups}} for i in bad]})
    write('support-diagnostic.json',rows);print(json.dumps(rows[-1],ensure_ascii=False),flush=True)
def skin_matrices(rig,o):
    bpy.context.view_layer.update();matrices={b.name:np.array(b.matrix@b.bone.matrix_local.inverted()) for b in rig.pose.bones};result=np.zeros((len(o.data.vertices),4,4))
    for v in o.data.vertices:
        for g in v.groups:
            n=o.vertex_groups[g.group].name
            if n in matrices:result[v.index]+=g.weight*matrices[n]
    return result
def seat_correctives(rig,meshes):
    o=next(o for o in meshes if o.name=='ShushuStatic_Torso');p=np.array([v.co for v in o.data.vertices]);x,y,z=p.T;records=[]
    belly=smooth(.135,.215,z)*(1-smooth(.30,.37,z))*(1-smooth(.17,.245,np.abs(x)))
    rump=smooth(.025,.12,y)*smooth(.11,.17,z)*(1-smooth(.24,.30,z))*(1-smooth(.10,.23,np.abs(x)))
    for t in [.25,.5,.75,1.]:
        state(rig,{'Seat':t});actual,_=evaluated(o);desired=p+np.array((0,.055*t,-.115*t));target=actual+(desired-actual)*belly[:,None]
        eligible=(rump>.01)&(target[:,2]>.0003);amplitude=min(.075,float(np.min((target[eligible,2]-.0003)/rump[eligible]))) if eligible.any() else 0
        target[:,2]-=max(0,amplitude)*smooth(.5,1,t)*rump
        matrices=skin_matrices(rig,o);delta=np.linalg.solve(matrices[:,:3,:3],(target-actual)[:,:,None])[:,:,0];name=f'Corrective.SeatVolume{int(t*100):03d}';k=shape(o,name,delta)
        expression=f'max(0,1-abs(s-{t})/.25)' if t<1 else 'max(0,(s-.75)/.25)';driver(k,'value',rig,expression,{'s':'Seat'})
        worst=int(np.argmax(np.linalg.norm(delta,axis=1)))
        records.append({'seat':t,'local_corrective_max':float(np.linalg.norm(delta,axis=1).max()),'world_correction_max':float(np.linalg.norm(target-actual,axis=1).max()),'worst_vertex_rest':p[worst].tolist(),'max_skin_condition':float(np.linalg.cond(matrices[:,:3,:3]).max()),'rump_smooth_sag':float(amplitude*smooth(.5,1,t)),'method':'inverse LBS / preserve round lower abdomen, smooth posterior support bulge; no per-vertex floor flattening'})
    reset(rig);write('seat-correctives.json',records)
def build():
    protect();rig,meshes=fresh();restore_eye_depth(meshes);edit_skeleton(rig);repair_weights(rig,meshes);add_controls(rig);paw_controls(rig);transfer_faces(rig,meshes);local_faces(rig,meshes);tongue_mesh(rig,meshes);reset(rig);seat_correctives(rig,meshes);paw_correctives(rig,meshes);calibrate_anchors(rig,meshes)
    for o in meshes:o.data.name=o.name
    authoring_setup(rig)
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));print('BUILD_SAVED',flush=True)
if __name__=='__main__':
    diagnose() if '--diagnose' in sys.argv else preview() if '--preview' in sys.argv else build() if '--build' in sys.argv else extract_donor() if '--extract' in sys.argv else donor_inventory() if '--donor' in sys.argv else inventory()
