"""Separately named v003 derivative: rump-supported seat with forward short legs."""
import bpy, sys, json, importlib.util, math, hashlib, subprocess
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix, Quaternion
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sp=importlib.util.spec_from_file_location('v003',ROOT/'scripts/blender/build-shushu-production-rig-v003.py')
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
b=v.b
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004'
SOURCE=v.ASSET
ASSET=SOURCE.with_name('shushu-v006-production-rig-v004.blend')
PROOF=ASSET.with_name(ASSET.stem+'-proof.blend')
GLB=ASSET.with_suffix('.glb')
b.OUT=OUT
def write(n,d):
    OUT.mkdir(parents=True,exist_ok=True);(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def snapshot():
    if (OUT/'protected-inputs.json').exists():return
    paths=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')+subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    write('protected-inputs.json',{p:b.sha(ROOT/p) for p in sorted(set(paths)) if p and (ROOT/p).is_file() and 'production-rig-v004' not in p})
    write('start-state.json',{'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'status':subprocess.check_output(['git','status','--short'],cwd=ROOT).decode(),'source_sha256':b.sha(SOURCE)})
def load(path=ASSET):
    rig,meshes=v.load(path);b.reset(rig);return rig,meshes
def inspect():
    snapshot();rig,meshes=load(SOURCE);o=bpy.data.objects['ShushuStatic_Torso'];p=np.array([x.co for x in o.data.vertices]);rows=[]
    for z in np.arange(0,.41,.02):
        q=p[(abs(p[:,2]-z)<.01)];rows.append({'z':float(z),'n':len(q),'bounds':[q.min(0).tolist(),q.max(0).tolist()] if len(q) else None})
    write('source-inspection.json',{'bones':{x.name:{'head':list(x.head_local),'tail':list(x.tail_local),'matrix':list(map(list,x.matrix_local))} for x in rig.data.bones if any(s in x.name for s in ['Hips','Leg','Foot'])},'slices':rows,'props':{k:rig[k] for k in rig.keys() if isinstance(rig[k],(int,float))},'keys':list(o.data.shape_keys.key_blocks.keys()),'objects':[(x.name,x.type) for x in bpy.data.objects]})
    print(json.dumps(json.loads((OUT/'source-inspection.json').read_text())['bones']),flush=True)
VIEWS=[('front',(0,-1,.03)),('3q-L',(-.65,-.76,.03)),('3q-R',(.65,-.76,.03)),('left',(-1,0,.02)),('right',(1,0,.02)),('back',(0,1,.03)),('rear-L',(-.65,.76,.03)),('rear-R',(.65,.76,.03))]
STATES=[('neutral',{}),('weight-transfer',{'Seat':.15,'WeightShift':.3}),('legs-forward',{'Seat':.4}),('rump-descending',{'Seat':.65}),('rump-contact',{'Seat':.85}),('seat',{'Seat':1}),('seat-rest',{'Seat':1,'Rest':1}),('recover-load',{'Seat':.85}),('recover-feet',{'Seat':.4}),('standing-return',{})]
COMPOSE=[('seat-half',{'Seat':1,'Blink.L':.5,'Blink.R':.5}),('seat-closed',{'Seat':1,'Blink.L':1,'Blink.R':1}),('seat-joy',{'Seat':1,'Joy':1,'Blink.L':.3,'Blink.R':.3}),('seat-lowhead',{'Seat':1,'HeadPitch':1,'Rest':.4,'Blink.L':.5,'Blink.R':.5}),('seat-shift-L',{'Seat':1,'WeightShift':1,'HeadRoll':-.5,'Joy':.6}),('seat-shift-R',{'Seat':1,'WeightShift':-1,'HeadRoll':.5,'Blink.L':1,'Blink.R':.5}),('seat-offer-L',{'Seat':1,'Offer.L':1}),('seat-hold-R',{'Seat':1,'Hold.R':1}),('seat-both-hold',{'Seat':1,'Hold.L':1,'Hold.R':1})]
def controls(rig,o):
    p=np.array([x.co for x in o.data.vertices]);hip=rig.pose.bones[b.PREFIX+'Hips'];inv=hip.bone.matrix_local.to_3x3().inverted()
    # Smooth load transfer; body descends independently of the feet's forward sweep.
    offset=inv@Vector((0,.015,-.116));shift=inv@Vector((.024,0,0))
    for i in range(3):
        anticip=inv@Vector((0,-.045,0))
        hip.driver_remove('location',i);b.driver(hip,'location',rig,f'{offset[i]}*(s*s*(3-2*s))+{anticip[i]}*sin(pi*s)+{shift[i]}*w',{'s':'Seat','w':'WeightShift'},i)
    records=[]
    for side,short,sign in [('Left','L',1),('Right','R',-1)]:
        target=bpy.data.objects['CTRL_Foot.'+side];foot=rig.data.bones[b.PREFIX+side+'Foot'];origin=np.array(foot.head_local)
        # Three ordinary computed channels make contact-height interpolation explicit.
        # The sole envelope is measured for each rigid foot rotation, never clamped per vertex.
        footpoints=p[(p[:,0]*sign>0)&(p[:,2]<.095)]-origin
        zvals=[]
        for s in np.linspace(0,1,33):
            phase=float(b.smooth(.15,.85,s));angle=-math.radians(65)*phase;rot=np.array(Matrix.Rotation(angle,3,'X'))
            q=footpoints@rot.T
            zvals.append(float(-q[:,2].min()+.0005*phase))
        # Neutral inherits the original slight per-foot sole offset exactly.
        zvals[0]=float(origin[2])
        phase='(min(1,max(0,(s-.15)/.7))**2*(3-2*min(1,max(0,(s-.15)/.7))))'
        for i in range(3):target.driver_remove('location',i)
        b.driver(target,'location',rig,f'{origin[0]}+{sign*.018}*{phase}+.025*v',{'s':'Seat','v':'FootSide.'+short},0)
        b.driver(target,'location',rig,f'{origin[1]}-.180*{phase}-.025*v',{'s':'Seat','v':'FootForward.'+short},1)
        # 33 samples of the continuous rigid-foot floor envelope, plus intentional lift.
        for k in range(11):
            prop=f'SeatFootHeight.{short}.{k}';b.prop(rig,prop,minimum=-1,maximum=1)
            a=k*3;terms=[f'({zvals[j]:.9g})*max(0,1-abs(s-{j/32})*32)' for j in range(a,min(a+3,33))]
            b.driver(rig,'["'+prop+'"]',rig,'+'.join(terms),{'s':'Seat'})
        b.driver(target,'location',rig,'+'.join(chr(97+k) for k in range(11))+'+.040*v',{**{chr(97+k):f'SeatFootHeight.{short}.{k}' for k in range(11)},'v':'FootLift.'+short},2)
        # Preserve the original target's freely editable orientation. Its child
        # contributes only the seat pitch in the target's original local axes.
        target.rotation_mode='QUATERNION';quat=foot.matrix_local.to_quaternion()
        sole=b.empty('CTRL_SeatSole.'+side,(0,0,0));sole.parent=target;sole.matrix_basis=Matrix.Identity(4);sole.rotation_mode='QUATERNION'
        axis=quat.inverted()@Vector((1,0,0))
        for i in range(4):
            expr=f'cos({math.radians(65)/2}*{phase})' if i==0 else f'{-axis[i-1]}*sin({math.radians(65)/2}*{phase})'
            b.driver(sole,'rotation_quaternion',rig,expr,{'s':'Seat'},i)
        next(c for c in rig.pose.bones[b.PREFIX+side+'Foot'].constraints if c.type=='COPY_ROTATION').target=sole
        records.append({'side':side,'angle_degrees':-65,'forward_travel':.18,'lateral_travel':sign*.018,'floor_envelope':zvals,'bone_lengths_preserved':True})
    write('seat-control-design.json',{'hip_translation':[0,.015,-.116],'forward_anticipation':'-.045*sin(pi*Seat) in Y, before posterior settlement','feet':records,'support':'Heels during forward sweep; rump joins at settlement. Forward travel and sole pitch replace old fixed foot premise. No rest shape edit or per-vertex floor clamp.'})
def support(rig,o):
    p=np.array([x.co for x in o.data.vertices]);x,y,z=p.T
    for key in list(o.data.shape_keys.key_blocks):
        if key.name.startswith('Corrective.SupportVolume'):v.v.remove_key(o,key)
    # Give the full approved foot to its Foot bone; the small shank blends into the thigh.
    old=[{o.vertex_groups[g.group].name:g.weight for g in q.groups} for q in o.data.vertices];nw=[]
    for point,ww in zip(p,old):
        own=float(1-b.smooth(.095,.155,point[2]));side='Left' if point[0]>=0 else 'Right'
        ww={n:w*(1-own) for n,w in ww.items()};name=b.PREFIX+side+'Foot';ww[name]=ww.get(name,0)+own;nw.append(ww)
    b.weights_replace(o,nw)
    modifier=next(m for m in o.modifiers if m.type=='ARMATURE');rows=[]
    unique,ids=np.unique(np.round(p,6),axis=0,return_inverse=True);members=np.bincount(ids)
    edges=np.array([e.vertices[:] for e in o.data.edges]);edges=np.unique(np.sort(ids[edges],axis=1),axis=0);edges=edges[edges[:,0]!=edges[:,1]]
    aa=np.r_[edges[:,0],edges[:,1]];bb=np.r_[edges[:,1],edges[:,0]];count=np.bincount(aa,minlength=len(unique)).clip(1)
    for shift in [-1.,0.,1.]:
        for seat in np.linspace(0,1,17):
            if seat==0:continue
            b.state(rig,{'Seat':float(seat),'WeightShift':shift});modifier.use_deform_preserve_volume=False;actual,_=b.evaluated(o)
            modifier.use_deform_preserve_volume=True;target,_=b.evaluated(o);modifier.use_deform_preserve_volume=False;bpy.context.view_layer.update()
            mask=1-b.smooth(.22,.34,z);target=actual+(target-actual)*mask[:,None]
            grouped=np.zeros_like(unique);np.add.at(grouped,ids,target);grouped/=members[:,None];relaxed=grouped.copy()
            corridor=b.smooth(.095,.145,unique[:,2])*(1-b.smooth(.24,.32,unique[:,2]))*seat
            for it in range(36):
                sums=np.zeros_like(relaxed);np.add.at(sums,aa,relaxed[bb]);relaxed+=(sums/count[:,None]-relaxed)*(corridor*(.55 if it%2==0 else -.30))[:,None]
            target+=(relaxed-grouped)[ids]
            matrices=b.skin_matrices(rig,o);delta=np.linalg.solve(matrices[:,:3,:3],(target-actual)[:,:,None])[:,:,0]
            k=b.shape(o,f'Corrective.TrueSeat.S{seat:.4f}.W{shift}',delta);b.driver(k,'value',rig,f'max(0,1-abs(s-{seat})*16)*max(0,1-abs(w-({shift})))',{'s':'Seat','w':'WeightShift'})
            rows.append({'seat':float(seat),'shift':shift,'min_z':float(target[:,2].min()),'max_corrective':float(np.linalg.norm(target-actual,axis=1).max())})
    b.reset(rig);write('support-authoring.json',rows)
def grip(rig):
    # Keep the inherited fixed-span item contract along the new hips trajectory.
    # Add distal corrections; preserve every original paw morph and driver.
    anchors={s:bpy.data.objects['ANCHOR_Hold.'+s] for s in ['L','R']}
    b.state(rig,{'Hold.L':1,'Hold.R':1})
    span=(anchors['L'].matrix_world.translation-anchors['R'].matrix_world.translation).length
    offsets={s:[] for s in anchors};rows=[]
    for seat in [.25,.5,.75,1.]:
        for shift in np.linspace(-1,1,9):
            shift=float(shift);b.state(rig,{'Seat':seat,'WeightShift':shift,'Hold.L':1,'Hold.R':1})
            left=anchors['L'].matrix_world.translation.copy();right=anchors['R'].matrix_world.translation.copy();center=(left+right)/2;axis=(left-right).normalized()
            for side,sign,point in [('L',1,left),('R',-1,right)]:
                correction=center+axis*(sign*span/2)-point;obj=bpy.data.objects['ShushuStatic_Paw_'+side]
                longname='Left' if side=='L' else 'Right';root=rig.data.bones[b.PREFIX+longname+'Shoulder'].head_local;hand=rig.data.bones[b.PREFIX+longname+'Hand'].head_local
                a=np.array([x.co for x in obj.data.vertices]);along=((a-np.array(root))@np.array((hand-root).normalized()))/(hand-root).length;mask=b.smooth(.30,.85,along)
                matrices=b.skin_matrices(rig,obj);delta=np.linalg.solve(matrices[:,:3,:3],(mask[:,None]*np.array(correction))[:,:,None])[:,:,0]
                hat=f'max(0,1-abs(s-{seat})*4)*max(0,1-abs(w-({shift}))*4)'
                key=b.shape(obj,f'Corrective.TrueSeatGrip.S{seat}.W{shift}',delta);b.driver(key,'value',rig,'min(l,r)*'+hat,{'l':'Hold.L','r':'Hold.R','s':'Seat','w':'WeightShift'})
                anchor=anchors[side];parent=anchor.matrix_world@anchor.matrix_basis.inverted();local=parent.to_3x3().inverted()@correction;offsets[side].append((hat,list(local)))
                rows.append({'seat':seat,'shift':shift,'side':side,'distal_correction':list(correction),'magnitude':correction.length})
    for side,anchor in anchors.items():
        weights=[]
        for number,(hat,offset) in enumerate(offsets[side]):
            prop=f'TrueSeatGripFit.{side}.{number}';b.prop(rig,prop);b.driver(rig,'["'+prop+'"]',rig,'min(l,r)*'+hat,{'s':'Seat','w':'WeightShift','l':'Hold.L','r':'Hold.R'});weights.append(prop)
        for index in range(3):
            fc=next(fc for fc in anchor.animation_data.drivers if fc.data_path=='location' and fc.array_index==index);extra=[]
            for group in range(4):
                start=group*9;prop=f'TrueSeatGripOffset.{side}.{index}.{group}';terms='+'.join(f'({offset[index]:.7g})*{chr(97+n)}' for n,(hat,offset) in enumerate(offsets[side][start:start+9]))
                b.prop(rig,prop,minimum=-.1,maximum=.1);b.driver(rig,'["'+prop+'"]',rig,terms,{chr(97+n):p for n,p in enumerate(weights[start:start+9])})
                name=chr(106+group);variable=fc.driver.variables.new();variable.name=name;variable.type='SINGLE_PROP';variable.targets[0].id=rig;variable.targets[0].data_path='["'+prop+'"]';extra.append(name)
            fc.driver.expression='('+fc.driver.expression+')+'+'+'.join(extra)
    b.reset(rig);write('true-seat-grip-authoring.json',{'span':span,'samples':rows,'scope':'Additive distal paw/contact correction for inherited fixed-span item, both occupied hands only; original keys and single-hand poses retained.'})

def build():
    snapshot();rig,meshes=load(SOURCE);o=bpy.data.objects['ShushuStatic_Torso'];rig.name='Shushu_ProductionRig_v004'
    controls(rig,o);support(rig,o);grip(rig);b.reset(rig)
    rig['Rig guide']='v004 true-seat candidate. Seat 0 standing, .15 load shift, .4 feet forward, .85 rump settlement, 1 seat. Existing face keys unchanged. Human PENDING; see evidence.'
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));print('V004_SAVED',flush=True)
def render():
    rig,meshes=load(SOURCE if '--before' in sys.argv else ASSET);scene,cam=b.setup_review(512,16)
    tag='before' if '--before' in sys.argv else 'candidate';folder=OUT/'renders'/tag;folder.mkdir(parents=True,exist_ok=True)
    chosen=sys.argv[sys.argv.index('--names')+1].split(',') if '--names' in sys.argv else None
    views=[v for v in VIEWS if v[0] in sys.argv[sys.argv.index('--views')+1].split(',')] if '--views' in sys.argv else VIEWS
    for name,values in STATES+COMPOSE:
        if chosen and name not in chosen:continue
        b.state(rig,values)
        for view,d in views:
            v.camera(cam,d);scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
        print('RENDERED',name,flush=True)
if __name__=='__main__':
    if '--build' in sys.argv:build()
    elif '--render' in sys.argv:render()
    else:inspect()
