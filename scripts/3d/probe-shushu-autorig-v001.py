"""Independent, byte-preserving Auto Rig diagnostic. Never edits source/rest/weights."""
import copy, hashlib, io, json, math, struct, subprocess, sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/production/shushu/evidence/tripo-autorig-v001'
SOURCE = ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-tripo-autorig-v001.glb'
SAVED = SOURCE.with_name('shushu-v006-autorig-deformation-probe-v001.glb')
LOW = ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigprep/shushu-v006-rigprep-lowpoly-v001.glb'
V006 = ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb'

def sha(data): return hashlib.sha256(data).hexdigest()
def write(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def load(path):
    r=path.read_bytes(); assert struct.unpack_from('<4sII',r)==(b'glTF',2,len(r))
    n=struct.unpack_from('<I',r,12)[0]; return r,json.loads(r[20:20+n]),r[28+n:]
def accessor(j,b,i):
    ac=j['accessors'][i]; v=j['bufferViews'][ac['bufferView']]
    n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[ac['type']]
    dt=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[ac['componentType']])
    a=np.ndarray((ac['count'],n),dtype=dt,buffer=b,offset=v.get('byteOffset',0)+ac.get('byteOffset',0),strides=(v.get('byteStride',dt.itemsize*n),dt.itemsize)).copy()
    if ac.get('normalized'): a=a.astype(float)/np.iinfo(dt).max
    return a
def qmul(a,b):
    av=np.array(a[:3]);bv=np.array(b[:3]); return np.r_[a[3]*bv+b[3]*av+np.cross(av,bv),a[3]*b[3]-np.dot(av,bv)]
def qconj(q): return np.r_[-np.array(q[:3]),q[3]]
def qaxis(axis,degrees):
    a=math.radians(degrees)/2; return np.r_[np.array(axis)*math.sin(a),math.cos(a)]
def qmatrix(q):
    x,y,z,w=np.array(q)/np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def hierarchy(j,rotations=None,translations=None):
    parents={c:i for i,n in enumerate(j['nodes']) for c in n.get('children',[])}; worlds={};qs={}
    def visit(i,trail=()):
        assert i not in trail,'cycle'
        if i in worlds:return
        n=j['nodes'][i];q=(rotations or {}).get(i,n.get('rotation',[0,0,0,1]));t=(translations or {}).get(i,n.get('translation',[0,0,0]))
        local=np.eye(4);local[:3,:3]=qmatrix(q)@np.diag(n.get('scale',[1,1,1]));local[:3,3]=t
        if 'matrix' in n:local=np.array(n['matrix']).reshape(4,4).T
        if i in parents:
            visit(parents[i],trail+(i,));worlds[i]=worlds[parents[i]]@local;qs[i]=qmul(qs[parents[i]],q)
        else:worlds[i]=local;qs[i]=np.array(q)
    for i in range(len(j['nodes'])):visit(i)
    return parents,worlds,qs
def images(j,b):
    return [b[(v:=j['bufferViews'][im['bufferView']]).get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']] for im in j['images']]
def meshes(j,b):
    return {n['name']:(i,p,accessor(j,b,p['attributes']['POSITION']),accessor(j,b,p['indices']).reshape(-1,3)) for i,n in enumerate(j['nodes']) if 'mesh' in n for p in j['meshes'][n['mesh']]['primitives']}
def skin(j,b,world):
    s=j['skins'][0];ib=accessor(j,b,s['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)
    mats=np.array([world[i]@m for i,m in zip(s['joints'],ib)]);result={}
    for name,(_,p,pos,_) in meshes(j,b).items():
        ids=accessor(j,b,p['attributes']['JOINTS_0']).astype(int);w=accessor(j,b,p['attributes']['WEIGHTS_0']);hp=np.c_[pos,np.ones(len(pos))]
        result[name]=sum(w[:,k,None]*np.einsum('nij,nj->ni',mats[ids[:,k]],hp)[:,:3] for k in range(4))
    return result
def protect():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'protected-inputs.json').exists():return
    paths=subprocess.check_output(['git','ls-files','-z','assets/grimo','docs/production/shushu'],cwd=ROOT).decode().split('\0')
    paths += [str(p.relative_to(ROOT)).replace('\\','/') for pattern in ['*.png','*18-27*'] for p in ROOT.glob(pattern) if p.is_file()]
    paths += [str(SOURCE.relative_to(ROOT)).replace('\\','/'),'docs/production/Handoff.md','docs/grimo/knowledge/Goal√map.md']
    manifest={p:sha((ROOT/p).read_bytes()) for p in sorted(set(paths)) if p and (ROOT/p).is_file()}
    write('protected-inputs.json',manifest)
    write('start-state.json',{'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip(),'status':subprocess.check_output(['git','status','--short'],cwd=ROOT).decode(),'source_sha256':sha(SOURCE.read_bytes())})
def prepare():
    protect();r,j,b=load(SOURCE);assert sha(r)=='803aeec97cb455a289e28baa9dd8cd281b97d2b54b92048a2e782228172f8932'
    par,world,qs=hierarchy(j);names={n['name'].split(':')[-1]:i for i,n in enumerate(j['nodes'])};states=[]
    def pose(name,spec=(),drop=0):
        rotations={};translations={}
        for bone,axis,degrees in spec:
            i=names[bone];rest=np.array(j['nodes'][i].get('rotation',[0,0,0,1]));local_delta=qmul(qmul(qconj(qs[i]),qaxis(axis,degrees)),qs[i]);rotations[i]=qmul(rest,local_delta).tolist()
        if drop:
            i=names['Hips'];translations[i]=(np.array(j['nodes'][i]['translation'])+np.array([0,-drop,-drop*.35])).tolist()
        states.append({'name':name,'time':len(states),'rotations':rotations,'translations':translations,'world_axis_deltas':list(spec),'pelvis_drop':drop})
    pose('neutral')
    pose('head-yaw-L',[('Head',(0,1,0),15)]);pose('return-yaw-L')
    pose('head-yaw-R',[('Head',(0,1,0),-15)]);pose('return-yaw-R')
    pose('head-tilt',[('Neck',(0,0,1),10)]);pose('return-tilt')
    pose('head-nod',[('Neck',(1,0,0),12)]);pose('return-nod')
    for side in ['Left','Right']:
        pose('paw-'+side,[(side+'Arm',(1,0,0),-25),(side+'ForeArm',(1,0,0),-25),(side+'Hand',(1,0,0),10)]);pose('return-paw-'+side)
    for name,h,k,drop in [('seat-entry',25,40,.025),('seat-attempt',50,80,.08)]:
        pose(name,[(side+bone,(1,0,0),angle) for side in ['Left','Right'] for bone,angle in [('UpLeg',-h),('Leg',k),('Foot',h-k)]],drop)
    pose('seat-recovery',[(side+bone,(1,0,0),angle) for side in ['Left','Right'] for bone,angle in [('UpLeg',-25),('Leg',40),('Foot',-15)]],.025)
    pose('return-seat')
    # Existing JSON descriptors and BIN remain untouched. Only append diagnostic animation.
    original=copy.deepcopy(j);payload=bytearray(b)
    def append(values,typ):
        arr=np.array(values,dtype='<f4');payload.extend(b'\0'*((-len(payload))%4));off=len(payload);payload.extend(arr.tobytes());vi=len(j['bufferViews']);j['bufferViews'].append({'buffer':0,'byteOffset':off,'byteLength':arr.nbytes});ai=len(j['accessors']);ac={'bufferView':vi,'componentType':5126,'count':len(arr),'type':typ}
        if typ=='SCALAR':ac.update(min=[float(arr.min())],max=[float(arr.max())])
        j['accessors'].append(ac);return ai
    time=append([s['time'] for s in states],'SCALAR');anim={'name':'Shushu_AutoRig_DIAGNOSTIC_NOT_PRODUCTION','samplers':[],'channels':[]}
    for path in ['rotation','translation']:
        field='rotations' if path=='rotation' else 'translations';ids=sorted({int(i) for s in states for i in s[field]})
        for i in ids:
            rest=j['nodes'][i].get(path,[0,0,0,1] if path=='rotation' else [0,0,0]);values=[s[field].get(i,rest) for s in states]
            ai=append(values,'VEC4' if path=='rotation' else 'VEC3');si=len(anim['samplers']);anim['samplers'].append({'input':time,'output':ai,'interpolation':'LINEAR'});anim['channels'].append({'sampler':si,'target':{'node':i,'path':path}})
    j['animations']=[anim];j['buffers'][0]['byteLength']=len(payload);payload.extend(b'\0'*((-len(payload))%4))
    jb=json.dumps(j,separators=(',',':')).encode();jb+=b' '*((-len(jb))%4);raw=struct.pack('<4sII',b'glTF',2,28+len(jb)+len(payload))+struct.pack('<I4s',len(jb),b'JSON')+jb+struct.pack('<I4s',len(payload),b'BIN\0')+payload
    SAVED.write_bytes(raw);sr,sj,sb=load(SAVED)
    assert sb[:len(b)]==b
    for key in original:
        if key not in ['buffers','accessors','bufferViews','animations']:assert sj[key]==original[key],key
    assert sj['accessors'][:len(original['accessors'])]==original['accessors'];assert sj['bufferViews'][:len(original['bufferViews'])]==original['bufferViews']
    write('poses.json',states)
    neutral=skin(sj,sb,hierarchy(sj)[1]);rows=[];joints=sj['skins'][0]['joints'];head=names['Head']
    _,lj,lb=load(LOW); lm=meshes(lj,lb)
    for name,(i,p,pos,tri) in meshes(sj,sb).items():
        ids=accessor(sj,sb,p['attributes']['JOINTS_0']).astype(int);w=accessor(sj,sb,p['attributes']['WEIGHTS_0']);assert ids.max()<len(joints)
        assert np.isfinite(w).all() and (w>=0).all() and np.max(abs(w.sum(1)-1))<1e-5
        total=np.zeros(len(joints));np.add.at(total,ids.reshape(-1),w.reshape(-1));hw=(w*(ids==joints.index(head))).sum(1)
        uv=accessor(sj,sb,p['attributes']['TEXCOORD_0']);nn=accessor(sj,sb,p['attributes']['NORMAL']);assert np.isfinite(pos).all() and np.isfinite(uv).all() and np.isfinite(nn).all()
        old=lm[name];oldpos=old[2];oldtri=old[3]
        # Independent nearest-neighbor sets handle Tripo's face/vertex reordering.
        olduv=accessor(lj,lb,old[1]['attributes']['TEXCOORD_0']);d0=cKDTree(oldpos).query(pos)[0];d1=cKDTree(pos).query(oldpos)[0]
        uv0=cKDTree(olduv).query(uv)[0];uv1=cKDTree(uv).query(olduv)[0]
        pu0=cKDTree(np.c_[oldpos,olduv]).query(np.c_[pos,uv])[0];pu1=cKDTree(np.c_[pos,uv]).query(np.c_[oldpos,olduv])[0]
        rows.append({'name':name,'vertices':len(pos),'triangles':len(tri),'bind_max_displacement':float(np.linalg.norm(neutral[name]-pos,axis=1).max()),'weight_sum_error':float(np.max(abs(w.sum(1)-1))),'head_weight_range':[float(hw.min()),float(hw.max())],'mean_weights':{sj['nodes'][joints[k]]['name']:float(total[k]/len(pos)) for k in range(len(joints)) if total[k]>1e-6},'uv_bounds':[uv.min(0).tolist(),uv.max(0).tolist()],'bounds':[pos.min(0).tolist(),pos.max(0).tolist()],'lowpoly_bidirectional_nearest_vertex_max':float(max(d0.max(),d1.max())),'lowpoly_bidirectional_UV_set_max':float(max(uv0.max(),uv1.max())),'lowpoly_bidirectional_position_UV_set_max':float(max(pu0.max(),pu1.max())),'comparison_limit':'nearest attribute sets tolerate reorder; not an exact triangle correspondence or surface-Hausdorff proof'})
    ims=images(sj,sb);oldims=images(lj,lb);textures=[]
    for i,data in enumerate(ims):
        im=Image.open(io.BytesIO(data));textures.append({'index':i,'size':list(im.size),'sha256':sha(data),'matching_lowpoly_image_bytes':any(data==v for v in oldims),'decoded_pixel_match_lowpoly':any(im.size==Image.open(io.BytesIO(v)).size and np.array_equal(np.array(im),np.array(Image.open(io.BytesIO(v)))) for v in oldims)})
    write('saved-glb-audit.json',{'source_sha256':sha(r),'saved_sha256':sha(sr),'original_BIN_prefix_exact':True,'original_nodes_skins_materials_meshes_images_UV_weights_accessors_exact':True,'joints':len(joints),'skinned_meshes':len(rows),'triangles':sum(x['triangles'] for x in rows),'textures':textures,'morph_targets':sum(len(p.get('targets',[])) for m in sj['meshes'] for p in m['primitives']),'animation_count':len(sj['animations']),'coordinate_system':'glTF Y-up / front +Z / neutral height ~1 / feet Y=0; meters by convention, no measured animal scale','hierarchy':[{'node':i,'name':sj['nodes'][i]['name'],'parent':par.get(i),'world_joint':world[i][:3,3].tolist()} for i in joints],'meshes':rows})
    measure=[]
    for state in states:
        pw=hierarchy(sj,{int(i):q for i,q in state['rotations'].items()},{int(i):t for i,t in state['translations'].items()})[1];deformed=skin(sj,sb,pw);mrows=[]
        for name,(_,p,pos,tri) in meshes(sj,sb).items():
            v=deformed[name];base=neutral[name];edge=np.concatenate([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]]);e0=np.linalg.norm(base[edge[:,0]]-base[edge[:,1]],axis=1);e1=np.linalg.norm(v[edge[:,0]]-v[edge[:,1]],axis=1);ratio=e1[e0>1e-7]/e0[e0>1e-7]
            def signed_volume(x):return float(np.einsum('ij,ij->i',x[tri[:,0]],np.cross(x[tri[:,1]],x[tri[:,2]])).sum()/6)
            one={'name':name,'max_displacement':float(np.linalg.norm(v-base,axis=1).max()),'edge_length_ratio_p01_p50_p99_extremes':np.percentile(ratio,[0,1,50,99,100]).tolist(),'finite':bool(np.isfinite(v).all())}
            if name.endswith(('Torso','Paw_L','Paw_R')):one['signed_surface_volume_ratio']=signed_volume(v)/signed_volume(base)
            if name.endswith('Torso'):
                feet=base[:,1]<.008;one.update(foot_low_band_max_shift=float(np.linalg.norm(v[feet]-base[feet],axis=1).max()),lowest_y=float(v[:,1].min()),vertices_below_ground=int((v[:,1]<-.001).sum()))
                regions={'belly':(base[:,1]>.19)&(base[:,1]<.43)&(base[:,2]>.06),'rump':(base[:,1]>.12)&(base[:,1]<.32)&(base[:,2]<-.04),'thigh':(base[:,1]>.10)&(base[:,1]<.24)&(abs(base[:,0])>.05)}
                one['regional_bbox_ratios_not_physical_volume']={k:(np.ptp(v[mask],axis=0)/np.ptp(base[mask],axis=0)).tolist() for k,mask in regions.items()}
            if name not in ['ShushuStatic_Torso','ShushuStatic_Paw_L','ShushuStatic_Paw_R']:
                # Residual against a rigid head following target, NOT a mandatory all-head assignment.
                hm=pw[head]@np.linalg.inv(world[head]);target=(np.c_[base,np.ones(len(base))]@hm.T)[:,:3];err=np.linalg.norm(v-target,axis=1)
                one['rigid_head_residual_p95_max']=np.percentile(err,[95,100]).tolist()
            mrows.append(one)
        measure.append({'name':state['name'],'time':state['time'],'meshes':mrows})
    write('deformation-measurements.json',measure)
    print('PREPARED',SAVED,'states',len(states),flush=True)
def boards():
    folder=OUT/'renders'; font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
    overview=Image.new('RGB',(1152,444),(242,241,238));draw=ImageDraw.Draw(overview)
    for col,(state,label) in enumerate([('neutral','Neutral / original weights'),('paw-Right','Right paw / repair needed'),('seat-attempt','Seat attempt / FAIL')]):
        draw.text((col*384+10,14),label,font=font(20),fill='black');overview.paste(Image.open(folder/f'{state}-3q.png').convert('RGB').resize((384,384)),(col*384,60))
    overview.save(OUT/'00-gate-overview.png')
    groups=[('01-neutral-identity',['v006','lowpoly','input-neutral','saved-neutral']),('02-head',['neutral','head-yaw-L','head-yaw-R','head-tilt','head-nod']),('03-short-forelimbs',['neutral','paw-Left','paw-Right']),('04-seat-unachieved',['neutral','seat-entry','seat-attempt','seat-recovery','return-seat']),('05-return',['neutral','return-yaw-L','return-yaw-R','return-tilt','return-nod','return-paw-Left','return-paw-Right','return-seat']),('06-contact-tangency-only',['neutral','contact-tangent','contact-release'])]
    for output,states in groups:
        canvas=Image.new('RGB',(3*384,70+len(states)*414),(242,241,238));d=ImageDraw.Draw(canvas);d.text((12,10),output+' / diagnostic / HUMAN UNVERIFIED',font=font(22),fill='black')
        for row,state in enumerate(states):
            for col,view in enumerate(['front','3q','side']):
                p=folder/f'{state}-{view}.png';pic=Image.open(p).convert('RGB');canvas.paste(pic.resize((384,384)),(col*384,70+row*414+30));d.text((col*384+8,70+row*414+4),state+' / '+view,font=font(17),fill='black')
        canvas.save(OUT/(output+'.png'))
    write('render-image-hashes.json',{p.name:sha(p.read_bytes()) for p in folder.glob('*.png')})
    checks=[]
    for view in ['front','3q','side']:
        neutral=np.array(Image.open(folder/f'neutral-{view}.png')).astype(float)
        for state in ['return-yaw-L','return-yaw-R','return-tilt','return-nod','return-paw-Left','return-paw-Right','return-seat','input-neutral','saved-neutral']:
            a=np.array(Image.open(folder/f'{state}-{view}.png')).astype(float);checks.append({'view':view,'state':state,'max_RGB_difference':float(abs(a-neutral).max()),'mean_absolute_difference':float(abs(a-neutral).mean()),'changed_pixels':int(np.any(a!=neutral,axis=2).sum())})
    write('return-image-comparison.json',checks);print('BOARDS_READY')
def verify():
    manifest=json.loads((OUT/'protected-inputs.json').read_text(encoding='utf-8'));changed=[p for p,h in manifest.items() if sha((ROOT/p).read_bytes())!=h]
    allowed=['docs/production/Handoff.md','docs/production/shushu/evidence/geometry-v003/ANATOMY_AND_DEFORMATION_NOTES.md'];assert not [p for p in changed if p not in allowed],changed
    write('protected-inputs-result.json',{'protected':len(manifest),'changes':changed,'allowed_evidence_sync_only':allowed,'source_unchanged':sha(SOURCE.read_bytes())==manifest[str(SOURCE.relative_to(ROOT)).replace('\\','/')]});print('PROTECTED',len(manifest),'changes',changed)
if __name__=='__main__':
    {'prepare':prepare,'boards':boards,'verify':verify}[sys.argv[1]]()
