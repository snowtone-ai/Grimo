"""v001 derivative: support silhouette, readable lids, owned stroke, reach arbitration.

Only v002 files are written. v001 and approved sources remain read only.
"""
import bpy, sys, json, hashlib, subprocess, importlib.util, math
from pathlib import Path
import numpy as np
from mathutils import Vector
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('shushu_v001', ROOT/'scripts/blender/build-shushu-production-rig-v001.py')
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
V001 = b.ASSET
OUT = ROOT/'docs/production/shushu/evidence/production-rig-v002'
ASSET = V001.with_name('shushu-v006-production-rig-v002.blend')
PROOF = ASSET.with_name(ASSET.stem+'-proof.blend')
GLB = ASSET.with_suffix('.glb')
b.OUT = OUT

def snapshot():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT/'protected-inputs.json').exists(): return
    paths = subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    paths += subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    protected = {p:b.sha(ROOT/p) for p in sorted(set(paths)) if p and (ROOT/p).is_file() and 'production-rig-v002' not in p}
    b.write('protected-inputs.json', protected)
    b.write('start-state.json', {'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'status':subprocess.check_output(['git','status','--short'],cwd=ROOT).decode(),'v001_sha256':b.sha(V001)})

def load(path=V001):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    rig = next(o for o in bpy.data.objects if o.type=='ARMATURE')
    meshes = sorted([o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')],key=lambda o:o.name)
    return rig, meshes

def inspect():
    snapshot(); rig, meshes=load(); b.reset(rig)
    rows=[]
    for o in meshes:
        p=np.array([v.co for v in o.data.vertices]); rows.append({'name':o.name,'bounds':[p.min(0).tolist(),p.max(0).tolist()],'keys':[k.name for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else [],'drivers':len(o.data.shape_keys.animation_data.drivers) if o.data.shape_keys and o.data.shape_keys.animation_data else 0})
    b.write('v001-inventory.json',{'meshes':rows,'bone_count':len(rig.data.bones),'properties':{k:rig[k] for k in rig.keys() if isinstance(rig[k],(int,float))}})
    torso=bpy.data.objects['ShushuStatic_Torso']; p=np.array([v.co for v in torso.data.vertices])
    np.savez_compressed(OUT/'v001-rest.npz',positions=p)
    print(json.dumps(rows,ensure_ascii=False),flush=True)

def remove_key(o,key):
    if o.data.shape_keys.animation_data:
        for d in list(o.data.shape_keys.animation_data.drivers):
            if d.data_path==key.path_from_id('value'): o.data.shape_keys.driver_remove(d.data_path)
    o.shape_key_remove(key)

def support(rig,meshes):
    o=bpy.data.objects['ShushuStatic_Torso']
    p=np.array([v.co for v in o.data.vertices]); x,y,z=p.T
    # Retain v001's support and anatomical ownership. Relax only the lower-body
    # crease corridor on the evaluated pose; do not replace it with a new body.
    # UV seams duplicate surface vertices. Relax a position-equivalence graph,
    # then apply one world displacement to every member; retain original mesh/UV.
    unique,ids=np.unique(np.round(p,6),axis=0,return_inverse=True)
    members=np.bincount(ids);edges=np.array([e.vertices[:] for e in o.data.edges],dtype=int)
    edges=np.unique(np.sort(ids[edges],axis=1),axis=0);edges=edges[edges[:,0]!=edges[:,1]]
    aa=np.r_[edges[:,0],edges[:,1]];bb=np.r_[edges[:,1],edges[:,0]]
    count=np.bincount(aa,minlength=len(unique)).clip(1)
    corridor=b.smooth(.065,.125,unique[:,2])*(1-b.smooth(.27,.36,unique[:,2]))
    rows=[]
    for t in [.125,.25,.375,.5,.625,.75,.875,1]:
        b.state(rig,{'Seat':t}); actual,_=b.evaluated(o)
        grouped=np.zeros_like(unique);np.add.at(grouped,ids,actual);grouped/=members[:,None]
        relaxed=grouped.copy();mask=corridor*b.smooth(.005,.035,grouped[:,2])*t
        for iteration in range(12):
            sums=np.zeros_like(relaxed);np.add.at(sums,aa,relaxed[bb]);avg=sums/count[:,None]
            gain=.50 if iteration%2==0 else -.45
            relaxed+=(avg-relaxed)*(mask*gain)[:,None]
        target=actual+(relaxed-grouped)[ids]
        matrices=b.skin_matrices(rig,o)
        delta=np.linalg.solve(matrices[:,:3,:3],(target-actual)[:,:,None])[:,:,0]
        k=b.shape(o,f'Corrective.SeatFlow{int(t*1000):04d}',delta)
        expr=f'max(0,1-abs(s-{t})/.125)' if t<1 else 'max(0,(s-.875)/.125)'
        b.driver(k,'value',rig,expr,{'s':'Seat'})
        rows.append({'seat':t,'correction_max':float(np.linalg.norm(target-actual,axis=1).max()),'affected_vertices':int((np.linalg.norm(target-actual,axis=1)>1e-5).sum())})
    b.reset(rig);b.write('seat-flow.json',{'method':'v001 evaluated lower-body crease corridor / UV-seam-coherent Taubin relaxation with protected sole and support / inverse LBS, eight bounded seat samples','samples':rows})

def reach(rig,meshes):
    # Holding owns the occupied paw. Self contact owns the remaining amount;
    # offer uses only the free amount. All three requests remain editable.
    h='min(1,max(0,h))'; c=f'min(1,max(0,c))*(1-{h})'; o=f'min(1,max(0,o))*(1-{h})*(1-min(1,max(0,c)))'
    for side,longname in [('L','Left'),('R','Right')]:
        vars={'h':'Hold.'+side,'c':'SelfContact.'+side,'o':'Offer.'+side,'s':'Seat'}
        for owner in [bpy.data.objects['CTRL_Paw.'+side],rig]:
            if not owner.animation_data: continue
            for fc in owner.animation_data.drivers:
                if owner==rig and longname+'Shoulder' not in fc.data_path and longname+'ForeArm' not in fc.data_path: continue
                d=fc.driver
                # Replace bare names, leaving their associated destinations intact.
                import re
                expression=d.expression.replace('/max(1,h+o+c)','')
                d.expression=re.sub(r'\b(h|c|o)\b',lambda m:{'h':h,'c':c,'o':o}[m[0]],expression)
        paw=bpy.data.objects['ShushuStatic_Paw_'+side]
        for fc in list(paw.data.shape_keys.animation_data.drivers):
            mode=next((m for m in ['Hold','SelfContact','Offer'] if f'Corrective.{m}' in fc.data_path),None)
            if not mode:continue
            expression=fc.driver.expression.replace('v',{'Hold':h,'SelfContact':c,'Offer':o}[mode])
            k=paw.data.shape_keys.path_resolve(fc.data_path.rsplit('.',1)[0])
            paw.data.shape_keys.driver_remove(fc.data_path)
            b.driver(k,'value',rig,expression,vars)
    b.write('reach-policy.json',{'priority':['Hold','SelfContact','Offer'],'method':'Bounded residual weights applied to targets, shoulder/IK and all corresponding correctives','product_policy':'Deferred offer scheduling and item ownership are outside rig scope'})

def eyelids(rig,meshes):
    # Re-time the inherited blink geometry, preserving the exact closed endpoint.
    # Half-lid reduces the sharp donor half corrective; Joy gets a clear lid arc.
    for obj in meshes:
        sk=obj.data.shape_keys
        if not sk or not sk.animation_data: continue
        for fc in list(sk.animation_data.drivers):
            key=sk.path_resolve(fc.data_path.rsplit('.',1)[0])
            name=key.name
            if name.startswith(('Blink.','Corrective.HalfBlink.','Corrective.ClosedRetraction.','Corrective.ClosedSeal.','Gaze')):
                side='L' if '.L' in name else 'R'
                blink='max(b*.78+max(0,b-.5)*.44,r*.40,j)'
                expression=fc.driver.expression.replace('max(b,r*.55)',blink)
                if name.startswith('Corrective.HalfBlink.'): expression=f'.35*max(0,1-abs({blink}-.5)*2)'
                if name.startswith('Gaze'): expression=expression.replace('max(b,r*.55)',blink)
                sk.driver_remove(fc.data_path)
                variables={'b':'Blink.'+side,'r':'Rest','j':'Joy'}
                if name.startswith('Gaze'):
                    variables['v']='Gaze'+('X' if name.startswith(('GazeLeft','GazeRight')) else 'Y')+'.'+side
                b.driver(key,'value',rig,expression,variables)
            elif name=='JoyLids':
                fc.driver.expression='j*.55'
    b.write('eye-affect-policy.json',{'half_blink_effective':.39,'rest_lid':.4,'joy_lid':1,'half_corrective_gain':.35,'joy_lids_gain':.55,'closed_endpoint_unchanged':True,'gate':'Visual candidate, Human PENDING'})

def rigid_grip(rig):
    # The two occupied paws share one fixed-span item. Correct only the small
    # distal contact discrepancy; do not lengthen limbs or animate item scale.
    b.state(rig,{'Hold.L':1,'Hold.R':1});anchors={side:bpy.data.objects['ANCHOR_Hold.'+side] for side in ['L','R']}
    span=(anchors['L'].matrix_world.translation-anchors['R'].matrix_world.translation).length
    offsets={side:[] for side in anchors};rows=[]
    for seat in [0,.5,1]:
        for shift in np.linspace(-1,1,9):
            shift=float(shift)
            b.state(rig,{'Seat':seat,'WeightShift':shift,'Hold.L':1,'Hold.R':1});L=anchors['L'].matrix_world.translation.copy();R=anchors['R'].matrix_world.translation.copy();center=(L+R)/2;axis=(L-R).normalized()
            for side,sign,point in [('L',1,L),('R',-1,R)]:
                correction=center+axis*(sign*span/2)-point;obj=bpy.data.objects['ShushuStatic_Paw_'+side]
                longname='Left' if side=='L' else 'Right';root=rig.data.bones[b.PREFIX+longname+'Shoulder'].head_local;hand=rig.data.bones[b.PREFIX+longname+'Hand'].head_local
                a=np.array([q.co for q in obj.data.vertices]);along=((a-np.array(root))@np.array((hand-root).normalized()))/(hand-root).length;mask=b.smooth(.30,.85,along)
                matrices=b.skin_matrices(rig,obj);delta=np.linalg.solve(matrices[:,:3,:3],(mask[:,None]*np.array(correction))[:,:,None])[:,:,0]
                key=b.shape(obj,f'Corrective.RigidGrip_{seat}_{shift}',delta);hat=f'max(0,1-abs(s-{seat})/.5)*max(0,1-abs(w-({shift}))/.25)';b.driver(key,'value',rig,'min(l,r)*'+hat,{'l':'Hold.L','r':'Hold.R','s':'Seat','w':'WeightShift'})
                anchor=anchors[side];parent=anchor.matrix_world@anchor.matrix_basis.inverted();local=parent.to_3x3().inverted()@correction;offsets[side].append((hat,list(local)))
                rows.append({'seat':seat,'shift':shift,'side':side,'distal_correction':list(correction),'magnitude':correction.length})
    for side,anchor in anchors.items():
        weights=[]
        for number,(hat,offset) in enumerate(offsets[side]):
            prop='GripFit.'+side+'.'+str(number);b.prop(rig,prop,description='Computed fixed-span contact weight');b.driver(rig,'["'+prop+'"]',rig,'min(l,r)*'+hat,{'s':'Seat','w':'WeightShift','l':'Hold.L','r':'Hold.R'});weights.append(prop)
        for index in range(3):
            fc=next(fc for fc in anchor.animation_data.drivers if fc.data_path=='location' and fc.array_index==index);old=fc.driver.expression
            rowsum=[]
            for group in range(3):
                start=group*9;terms='+'.join(f'({offset[index]:.7g})*{chr(97+n)}' for n,(hat,offset) in enumerate(offsets[side][start:start+9]));prop=f'GripOffset.{side}.{index}.{group}'
                b.prop(rig,prop,minimum=-.1,maximum=.1,description='Computed contact offset');b.driver(rig,'["'+prop+'"]',rig,terms,{chr(97+n):p for n,p in enumerate(weights[start:start+9])});rowsum.append(prop)
            anchor.driver_remove('location',index);b.driver(anchor,'location',rig,f'({old})+a+b+c',{'s':'Seat','a':rowsum[0],'b':rowsum[1],'c':rowsum[2]},index=index)
    b.reset(rig);b.write('rigid-grip-correction.json',{'span':span,'samples':rows,'activation':'min(Hold.L,Hold.R); fixed wrists 0; Seat 3 x WeightShift 9 grid, refined after measured intermediate mismatch','limits':'Calibrated fixed-span proxy only. Different item spans or arbitrary regrasp need item-specific fitting.'})

ZONES=[('Forehead','Head',(-.10,.10),(.77,.83),.010,.048),('Cheek.L','Head',(.18,.25),(.565,.63),.010,.042),('Cheek.R','Head',(-.25,-.18),(.565,.63),.010,.042),('Belly','Torso',(-.15,.15),(.225,.395),.014,.065)]
def stroke(rig):
    for n,lo,hi in [('StrokePressure',0,1),('StrokeZone',0,3),('StrokeU',-1,1),('StrokeV',-1,1)]: b.prop(rig,n,minimum=lo,maximum=hi,description='Owned soft-surface stroke; zone boundary is documented in README')
    rows=[]
    for zone,(label,role,xs,zs,depth,radius) in enumerate(ZONES):
        obj=bpy.data.objects['ShushuStatic_'+role];p=np.array([v.co for v in obj.data.vertices]);x,y,z=p.T
        mask=b.smooth(.04,.14,-y)
        if role=='Head':
            # Keep the pink eye enclosure, actual eyes, nose and mouth untouched.
            eyes=np.maximum(1-b.smooth(1,1.25,((x-.13)/.085)**2+((z-.67)/.095)**2),1-b.smooth(1,1.25,((x+.13)/.085)**2+((z-.67)/.095)**2))
            mouth=np.exp(-2*((x/.065)**2+((z-.595)/.055)**2))
            mask*=np.clip((1-eyes)*2-1,0,1)*np.clip((1-mouth)*2-1,0,1)
            for key in obj.data.shape_keys.key_blocks:
                if key.name.startswith(('Blink.','Corrective.HalfBlink.','MouthOpen')):
                    q=np.empty(p.size,dtype=np.float32);key.data.foreach_get('co',q)
                    mask[np.linalg.norm(q.reshape(-1,3)-p,axis=1)>1e-5]=0
        else: mask*=b.smooth(.16,.21,z)*(1-b.smooth(.4,.44,z))
        for ix,cx in enumerate(np.linspace(*xs,3)):
            for iz,cz in enumerate(np.linspace(*zs,3)):
                w=np.exp(-2*(((x-cx)/radius)**2+((z-cz)/radius)**2))*mask
                w[w<.003]=0
                delta=np.c_[np.zeros(len(p)),depth*w,np.zeros(len(p))]
                k=b.shape(obj,f'Stroke.{label}.{ix}.{iz}',delta)
                expr=f'p*max(0,1-abs(z-{zone}))*max(0,1-abs(min(2,max(0,u+1))-{ix}))*max(0,1-abs(min(2,max(0,v+1))-{iz}))'
                b.driver(k,'value',rig,expr,{'p':'StrokePressure','z':'StrokeZone','u':'StrokeU','v':'StrokeV'})
        rows.append({'zone':zone,'name':label,'owner':role,'local_x':xs,'local_z':zs,'depth_max':depth,'radius':radius,'eye_nose_mouth_exclusion':role=='Head'})
    b.write('stroke-domain.json',{'method':'Bilinear moving local Gaussian displacement fields on current Basis; skin follows current owner, no lag or global scale','zones':rows,'limits':'Bounded continuous paths within each safe zone. Crossing eyes/mouth/accessory contact or arbitrary rear surfaces requires domain-specific authoring.'})

def build():
    snapshot();rig,meshes=load();b.reset(rig);rig.name='Shushu_ProductionRig_v002'
    support(rig,meshes);reach(rig,meshes);rigid_grip(rig);eyelids(rig,meshes);stroke(rig)
    rig['Rig guide']='v002: Hold > SelfContact > Offer residual arbitration. StrokeZone 0 forehead / 1 cheek L / 2 cheek R / 3 belly. See v002 README; Human PENDING.'
    guide=bpy.data.texts.get('SHUSHU_RIG_README')
    if guide: guide.clear();guide.write(rig['Rig guide']+'\nAll v001 controls retained. Numeric controls zero restores Neutral. Direct FK and foot target rotation remain outside support guarantee.\n')
    b.reset(rig);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));print('V002_SAVED',flush=True)

if __name__=='__main__': inspect() if '--inspect' in sys.argv else build()
