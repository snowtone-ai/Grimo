"""Read-only v002 derivative. Local support/eye corrections; source identity is frozen."""
import bpy, sys, json, hashlib, subprocess, importlib.util, math
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
def module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT/file)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
v = module('v002', 'scripts/blender/build-shushu-production-rig-v002.py')
b = v.b
OUT = ROOT/'docs/production/shushu/evidence/production-rig-v003'
SOURCE = v.ASSET
ASSET = SOURCE.with_name('shushu-v006-production-rig-v003.blend')
PROOF = ASSET.with_name(ASSET.stem+'-proof.blend')
GLB = ASSET.with_suffix('.glb')
b.OUT = OUT
VIEWS = [('front',(0,-1,0)),('left',(-1,0,0)),('3q-L',(-.65,-.76,0)),('3q-R',(.65,-.76,0))]
STATES = [('neutral',{}),('shift-L',{'WeightShift':1}),('shift-R',{'WeightShift':-1}),
          ('seat-entry',{'Seat':.25}),('seat-mid',{'Seat':.5}),('seat-three-quarter',{'Seat':.75}),
          ('seat',{'Seat':1}),('seat-rest',{'Seat':1,'Rest':1}),
          ('recovery-mid',{'Seat':.5}),('standing-return',{}),
          ('seat-lowhead',{'Seat':1,'HeadPitch':1,'Rest':.4,'Blink.L':.5,'Blink.R':.5}),
          ('seat-shift-L',{'Seat':1,'WeightShift':1,'HeadRoll':-.5,'Joy':.6})]
def snapshot():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT/'protected-inputs.json').exists(): return
    paths = subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    paths += subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    paths = [p for p in sorted(set(paths)) if p and (ROOT/p).is_file() and 'production-rig-v003' not in p]
    b.write('protected-inputs.json',{p:b.sha(ROOT/p) for p in paths})
    b.write('start-state.json',{'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'status':subprocess.check_output(['git','status','--short'],cwd=ROOT).decode(),'v002_sha256':b.sha(SOURCE)})
def load(path=SOURCE):
    rig, meshes = v.load(path); b.reset(rig); return rig, meshes
def camera(cam,d,target=(0,0,.5),scale=1.14):
    d=Vector(d).normalized();cam.location=Vector(target)+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
def render_states(path,tag,names=None,size=640,samples=16):
    rig,meshes=load(path);scene,cam=b.setup_review(size,samples);folder=OUT/'renders'/tag;folder.mkdir(parents=True,exist_ok=True)
    for name,controls in STATES:
        if names and name not in names:continue
        b.state(rig,controls)
        for view,d in VIEWS:
            camera(cam,d);scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
        print('RENDER',tag,name,flush=True)
def trace():
    snapshot();rows=[]
    sources=[('v006', b.BASE/'texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb'),('lowpoly',b.BASE/'rigprep/shushu-v006-rigprep-lowpoly-v001.glb'),('autorig',b.SOURCE),('v001',v.V001),('v002',SOURCE)]
    for tag,path in sources:
        if path.suffix=='.blend':rig,meshes=load(path)
        else:
            bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path));meshes=[o for o in bpy.data.objects if o.type=='MESH'];rig=next((o for o in bpy.data.objects if o.type=='ARMATURE'),None)
        torso=next(o for o in meshes if o.name=='ShushuStatic_Torso');p,t=b.evaluated(torso)
        slices=[]
        for z in [.025,.05,.075,.10,.125,.15,.175,.20,.225,.25]:
            q=p[(abs(p[:,2]-z)<.006)&(p[:,0]>.05)]
            slices.append({'z':z,'n':len(q),'bounds':[q.min(0).tolist(),q.max(0).tolist()] if len(q) else None})
        rows.append({'stage':tag,'path':str(path.relative_to(ROOT)),'sha256':b.sha(path),'torso_vertices':len(p),'leg_slices':slices,'bones':[{'name':bo.name,'head':list(bo.head_local),'tail':list(bo.tail_local)} for bo in rig.data.bones if any(n in bo.name for n in ['UpLeg','Leg','Foot','ToeBase'])] if rig else []})
        np.savez_compressed(OUT/f'trace-{tag}.npz',positions=p,triangles=t)
        scene,cam=b.setup_review(640,16);folder=OUT/'renders'/tag;folder.mkdir(parents=True,exist_ok=True)
        for view,d in VIEWS:
            camera(cam,d);scene.render.filepath=str(folder/f'neutral-{view}.png');bpy.ops.render.render(write_still=True)
        print('TRACE',tag,flush=True)
    b.write('lineage.json',rows)
    rig,meshes=load();o=bpy.data.objects['ShushuStatic_Torso'];p=np.array([q.co for q in o.data.vertices]);rec=[]
    for name,controls in STATES:
        b.state(rig,controls);q,_=b.evaluated(o)
        rec.append({'state':name,'bones':{pb.name:{'head':list(pb.head),'tail':list(pb.tail)} for pb in rig.pose.bones if any(n in pb.name for n in ['Hips','UpLeg','Leg','Foot'])},'foot_bounds':[q[(p[:,2]<.10)&(p[:,0]>.05)].min(0).tolist(),q[(p[:,2]<.10)&(p[:,0]>.05)].max(0).tolist()]})
    b.write('v002-support-diagnostic.json',rec)
    head=bpy.data.objects['ShushuStatic_Head'];eyes={}
    for o in meshes:
        if not o.data.shape_keys or not o.data.shape_keys.animation_data:continue
        eyes[o.name]=[{'path':fc.data_path,'expr':fc.driver.expression,'vars':{var.name:var.targets[0].data_path for var in fc.driver.variables}} for fc in o.data.shape_keys.animation_data.drivers if any(s in fc.data_path for s in ['Blink','JoyLids','Closed','Gaze'])]
    b.write('v002-eye-drivers.json',eyes)
def support(rig,meshes):
    o=bpy.data.objects['ShushuStatic_Torso'];p=np.array([q.co for q in o.data.vertices]);x,y,z=p.T
    pole_rows=[]
    for side in ['Left','Right']:
        ik=next(c for c in rig.pose.bones[b.PREFIX+side+'Leg'].constraints if c.type=='IK')
        b.state(rig,{'Seat':.5});old_angle=float(ik.pole_angle);trials=[]
        for angle in np.linspace(-math.pi,math.pi,73):
            ik.pole_angle=float(angle);bpy.context.view_layer.update();knee=rig.pose.bones[b.PREFIX+side+'Leg'].head.copy()
            trials.append((float(knee.y),float(angle),list(knee)))
        best=min(trials);ik.pole_angle=best[1]
        pole_rows.append({'side':side,'old_angle':old_angle,'new_angle':best[1],'mid_knee':best[2],'criterion':'Knee points forward (-Y) rather than into medial groin; original bone lengths and foot pin unchanged.'})
    b.write('knee-plane-repair.json',pole_rows)
    for key in list(o.data.shape_keys.key_blocks):
        if key.name.startswith(('Corrective.SeatVolume','Corrective.SeatFlow')):v.remove_key(o,key)
    # The whole existing foot, not only the sole, belongs to the planted foot.
    # Blend into the short shank above the foot crown. Basis and UV are untouched.
    old=[{o.vertex_groups[g.group].name:g.weight for g in q.groups} for q in o.data.vertices];new=[]
    for point,weights in zip(p,old):
        sole=float(1-b.smooth(.095,.145,point[2]));side='Left' if point[0]>=0 else 'Right'
        if '--thigh-owner' in sys.argv:
            domain=float(b.smooth(.035,.075,abs(point[0]))*(1-b.smooth(.135,.185,point[2]))*(1-b.smooth(.10,.16,abs(point[1]))))
            up=float(b.smooth(.12,.165,point[2]));anatomic={b.PREFIX+side+'UpLeg':up,b.PREFIX+side+'Leg':1-up}
            weights={n:w*(1-domain) for n,w in weights.items()}
            for n,w in anatomic.items():weights[n]=weights.get(n,0)+w*domain
        nw={name:w*(1-sole) for name,w in weights.items()};name=b.PREFIX+side+'Foot';nw[name]=nw.get(name,0)+sole;new.append(nw)
    b.weights_replace(o,new)
    modifier=next(m for m in o.modifiers if m.type=='ARMATURE');rows=[];samples=[]
    unique,ids=np.unique(np.round(p,6),axis=0,return_inverse=True);members=np.bincount(ids)
    edges=np.array([e.vertices[:] for e in o.data.edges],dtype=int)
    edges=np.unique(np.sort(ids[edges],axis=1),axis=0);edges=edges[edges[:,0]!=edges[:,1]]
    aa=np.r_[edges[:,0],edges[:,1]];bb=np.r_[edges[:,1],edges[:,0]];count=np.bincount(aa,minlength=len(unique)).clip(1)
    for shift in [-1.,0.,1.]:
        for seat in np.linspace(0,1,9):
            if seat==0 and shift==0:continue
            b.state(rig,{'Seat':float(seat),'WeightShift':shift})
            modifier.use_deform_preserve_volume=False;actual,_=b.evaluated(o)
            modifier.use_deform_preserve_volume=True;target,_=b.evaluated(o)
            modifier.use_deform_preserve_volume=False;bpy.context.view_layer.update()
            # Limit the volume correction to the actual lower-body articulation.
            mask=1-b.smooth(.24,.34,z);target=actual+(target-actual)*mask[:,None]
            grouped=np.zeros_like(unique);np.add.at(grouped,ids,target);grouped/=members[:,None];relaxed=grouped.copy()
            corridor=b.smooth(.095,.135,unique[:,2])*(1-b.smooth(.245,.31,unique[:,2]))*float(seat)
            corridor*=b.smooth(.008,.025,grouped[:,2])
            for iteration in range(32):
                sums=np.zeros_like(relaxed);np.add.at(sums,aa,relaxed[bb]);avg=sums/count[:,None]
                relaxed+=(avg-relaxed)*(corridor*(.58 if iteration%2==0 else -.28))[:,None]
            target+=(relaxed-grouped)[ids]
            # A broad posterior support envelope settles as one smooth field.
            # No floor-clamping of individual vertices, and no foot flattening.
            rump=b.smooth(.025,.12,y)*b.smooth(.11,.17,z)*(1-b.smooth(.24,.30,z))*(1-b.smooth(.10,.23,abs(x)))
            phase=float(b.smooth(.5,1,seat));eligible=rump>.10
            amplitude=min(.06,float(np.min((target[eligible,2]-.0005)/rump[eligible]))) if eligible.any() else 0
            target[:,2]-=amplitude*phase*rump
            matrices=b.skin_matrices(rig,o);delta=np.linalg.solve(matrices[:,:3,:3],(target-actual)[:,:,None])[:,:,0]
            samples.append((float(seat),shift,delta));rows.append({'seat':float(seat),'shift':shift,'max_correction':float(np.linalg.norm(target-actual,axis=1).max()),'floor':float(target[:,2].min()),'rump_sag':float(amplitude*phase)})
    for seat,shift,delta in samples:
        key=b.shape(o,f'Corrective.SupportVolume.S{seat:.3f}.W{shift:.1f}',delta)
        b.driver(key,'value',rig,f'max(0,1-abs(s-{seat})/.125)*max(0,1-abs(w-({shift})))',{'s':'Seat','w':'WeightShift'})
    b.reset(rig);b.write('support-authoring.json',{'thigh_ownership_trial':'--thigh-owner' in sys.argv,'method':'Preserve whole approved foot via local weights; lower-body dual-quaternion evaluated volume transferred as inverse-linear-skin correctives, 9x3 Seat/Shift grid and seam-coherent local relaxation; no Basis, topology, UV or texture edit.','samples':rows})
def eyes(rig,meshes):
    # Pose-local repair only. Keep all existing expressions outside these support
    # compositions, and fade the repair to zero at full blink to retain closure.
    gates=[('LowHead','s*max(0,p)*max(0,1-abs(r-.4)/.4)*max(0,1-abs(b-.5)/.5)*max(0,1-abs(c-.5)/.5)*(1-j)',{'s':'Seat','p':'HeadPitch','r':'Rest','b':'Blink.L','c':'Blink.R','j':'Joy'}),
           ('ShiftL','s*max(0,w)*min(1,max(0,-h*2))*max(0,1-abs(j-.6)/.4)*(1-max(l,r))',{'s':'Seat','w':'WeightShift','h':'HeadRoll','j':'Joy','l':'Blink.L','r':'Blink.R'})]
    records=[]
    for label,expr,variables in gates:
        values=dict(next(c for name,c in STATES if name==('seat-lowhead' if label=='LowHead' else 'seat-shift-L')))
        b.state(rig,values)
        for o in meshes:
            if not (o.name.startswith(('ShushuStatic_Eye_','ShushuStatic_LidWall_')) or o.name=='ShushuStatic_Head'):continue
            actual,_=b.evaluated(o);sk=o.data.shape_keys;muted=[]
            if not sk or not sk.animation_data:continue
            for fc in sk.animation_data.drivers:
                if any(k in fc.data_path for k in ['Blink','ClosedRetraction','JoyLids']):
                    key=sk.path_resolve(fc.data_path.rsplit('.',1)[0]);muted.append((fc,key,key.value));fc.mute=True;key.value=0
            o.data.update();o.update_tag();target,_=b.evaluated(o)
            if o.name=='ShushuStatic_Head':
                pp=np.array([q.co for q in o.data.vertices]);xx,yy,zz=pp.T
                mask=b.smooth(.035,.065,abs(xx))*(1-b.smooth(.18,.215,abs(xx)))*b.smooth(.625,.65,zz)*(1-b.smooth(.77,.80,zz))*b.smooth(.07,.15,-yy)
                target=actual+(target-actual)*mask[:,None]
            for fc,key,value in muted:fc.mute=False;key.value=value
            o.data.update();o.update_tag();bpy.context.view_layer.update()
            matrices=b.skin_matrices(rig,o);delta=np.linalg.solve(matrices[:,:3,:3],(target-actual)[:,:,None])[:,:,0]
            k=b.shape(o,'Corrective.EyeIntegrity.'+label,delta);b.driver(k,'value',rig,expr,variables)
            records.append({'mesh':o.name,'context':label,'correction':float(np.linalg.norm(target-actual,axis=1).max()),'method':'Remove nonrigid pupil/globe flattening in this composition; retain surrounding lids and rigid head pose.'})
    b.reset(rig);b.write('eye-authoring.json',records)
def build():
    snapshot();rig,meshes=load();rig.name='Shushu_ProductionRig_v003'
    support(rig,meshes);eyes(rig,meshes);b.reset(rig)
    rig['Rig guide']='v003 local support/eye candidate. Original v002 controls retained. See production-rig-v003/REVIEW.md for visual HOLDs and verified domain.'
    guide=bpy.data.texts.get('SHUSHU_RIG_README')
    if guide:guide.clear();guide.write(rig['Rig guide']+'\nNeutral: all numeric controls 0. Support volume is exported as ordinary sampled Morph; Armature remains linear skin. Full source identity/UV/Texture retained. Human approval is pending.\nAll inherited controls remain editable. See the evidence README for verification limits.\n')
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));print('V003_SAVED',flush=True)
def face_details():
    cases=[row for row in STATES if row[0] in ['neutral','seat-lowhead','seat-shift-L','seat-rest']]
    cases += [('half',{'Blink.L':.5,'Blink.R':.5}),('closed',{'Blink.L':1,'Blink.R':1}),('seat-joy',{'Seat':1,'Joy':1,'Blink.L':.3,'Blink.R':.3})]
    for tag,path in [('v002',SOURCE),('candidate',ASSET)]:
        rig,meshes=load(path);scene,cam=b.setup_review(768,24);folder=OUT/'detail'/tag;folder.mkdir(parents=True,exist_ok=True)
        for name,controls in cases:
            b.state(rig,controls);target=(0,-.01,.715-.115*controls.get('Seat',0))
            for view,d in [VIEWS[i] for i in [0,2,3]]:
                camera(cam,d,target,.56);scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
            print('DETAIL',tag,name,flush=True)
def trace_pose():
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(b.BASE/'rigging/shushu-v006-autorig-deformation-probe-v001.glb'));bpy.context.scene.render.fps=24
    poses=json.loads((OUT.parent/'tripo-autorig-v001/poses.json').read_text(encoding='utf-8'));scene,cam=b.setup_review(640,16);folder=OUT/'renders/autorig-probe';folder.mkdir(parents=True,exist_ok=True)
    for row in poses:
        if row['name'] not in ['seat-entry','seat-attempt']:continue
        scene.frame_set(row['time']*24)
        for view,d in VIEWS:
            camera(cam,d);scene.render.filepath=str(folder/f'{row["name"]}-{view}.png');bpy.ops.render.render(write_still=True)
if __name__=='__main__':
    if '--trace' in sys.argv:trace()
    elif '--render-before' in sys.argv:render_states(SOURCE,'v002',sys.argv[sys.argv.index('--names')+1].split(',') if '--names' in sys.argv else None)
    elif '--build' in sys.argv:build()
    elif '--faces' in sys.argv:face_details()
    elif '--trace-pose' in sys.argv:trace_pose()
    elif '--render' in sys.argv:render_states(ASSET,sys.argv[sys.argv.index('--tag')+1] if '--tag' in sys.argv else 'candidate',sys.argv[sys.argv.index('--names')+1].split(',') if '--names' in sys.argv else None)
