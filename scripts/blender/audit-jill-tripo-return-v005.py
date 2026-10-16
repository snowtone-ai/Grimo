"""Read-only bidirectional face/corner audit; no returned geometry is adopted."""
import bpy, json, struct, hashlib, itertools
from pathlib import Path
import numpy as np
from mathutils.kdtree import KDTree
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets/grimo/production/jill/tripo'
E=ROOT/'docs/production/jill/texture-return-v005'; E.mkdir(exist_ok=True)
S=A/'mouth-profile-v004/jill-texture-input-neutral-v004.glb'
R=A/'texture-return-v005/source/tripo-return-original.glb'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    b=p.read_bytes(); n=struct.unpack_from('<I',b,12)[0]; g=json.loads(b[20:20+n]); off=20+n; size=struct.unpack_from('<I',b,off)[0]; buf=b[off+8:off+8+size]
    def acc(i):
        a=g['accessors'][i]; v=g['bufferViews'][a['bufferView']]; dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]; c={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]; start=v.get('byteOffset',0)+a.get('byteOffset',0)
        return np.ndarray((a['count'],c),dtype=dt,buffer=buf,offset=start,strides=(v.get('byteStride',np.dtype(dt).itemsize*c),np.dtype(dt).itemsize)).copy()
    xyz=[];uv=[];tri=[];owners=[];prims=[];offset=0
    for mesh in g['meshes']:
        for p in mesh['primitives']:
            x=acc(p['attributes']['POSITION']); u=acc(p['attributes']['TEXCOORD_0']); t=acc(p['indices']).reshape(-1,3); mat=g['materials'][p.get('material',0)]; owner=mat.get('extras',{}).get('paint_owner',mat.get('name','UNKNOWN').removeprefix('JILL_'))
            xyz.append(x);uv.append(u);tri.append(t+offset);owners.extend([owner]*len(t));offset+=len(x);prims.append({'vertices':len(x),'triangles':len(t),'owner':owner,'attributes':list(p['attributes'])})
    # Input exports must have identity mesh-node transforms; explicitly check.
    nodes=[n for n in g['nodes'] if 'mesh' in n]
    transforms=[{k:n[k] for k in ['matrix','translation','rotation','scale'] if k in n} for n in nodes]
    return g,buf,np.concatenate(xyz),np.concatenate(uv),np.concatenate(tri),owners,prims,transforms
sg,sb,sx,su,st,so,sp,snt=read(S);rg,rb,rx,ru,rt,ro,rp,rnt=read(R)
print('BOUNDS',json.dumps({'source_xyz':[sx.min(0).tolist(),sx.max(0).tolist()],'returned_xyz':[rx.min(0).tolist(),rx.max(0).tolist()],'source_uv':[su.min(0).tolist(),su.max(0).tolist()],'returned_uv':[ru.min(0).tolist(),ru.max(0).tolist()],'source_samples':[sx[:3].tolist(),su[:3].tolist()],'return_samples':[rx[:3].tolist(),ru[:3].tolist()]}),flush=True)
report={'source':{'path':str(S.relative_to(ROOT)),'sha256':sha(S),'vertices':len(sx),'triangles':len(st),'primitives':sp,'transforms':snt},'returned':{'actual_intake_filename':'jill-texture-input-neutral-v004.glb.glb','sha256':sha(R),'bytes':R.stat().st_size,'vertices':len(rx),'triangles':len(rt),'primitives':rp,'transforms':rnt,'skins':len(rg.get('skins',[])),'morphs':sum(len(p.get('targets',[])) for m in rg['meshes'] for p in m['primitives']),'materials':len(rg['materials'])},'method':'UV-radius candidates filtered by position; then ordered triangle corner bijection, winding, full source/return face multiset and unique source owner. Position-only nearest neighbour is never acceptance.'}
def mapping(ax,au,bx,bu,ptol=2e-6,utol=2e-6):
    kd=KDTree(len(au))
    for i,(u,v) in enumerate(au):kd.insert((u,v,0),i)
    kd.balance(); rows=[];missing=[];ambiguous=[];pmax=umax=0.
    for i,(x,uv) in enumerate(zip(bx,bu)):
        candidates=[j for co,j,d in kd.find_range((float(uv[0]),float(uv[1]),0),utol) if np.linalg.norm(ax[j]-x)<ptol]
        rows.append(candidates)
        if not candidates:missing.append(i)
        elif len(candidates)>1:ambiguous.append(i)
        if candidates:
            pmax=max(pmax,float(max(np.linalg.norm(ax[j]-x) for j in candidates)));umax=max(umax,float(max(np.linalg.norm(au[j]-uv) for j in candidates)))
    return rows,{'unmatched':len(missing),'unmatched_examples':missing[:12],'multiple_seam_equivalents':len(ambiguous),'position_max_m':pmax,'uv_max':umax}
forward,report['returned_to_source_corners']=mapping(sx,su,rx,ru)
reverse,report['source_to_returned_corners']=mapping(rx,ru,sx,su)
report['strict_original_numeric_match']={'forward':report['returned_to_source_corners'],'reverse':report['source_to_returned_corners']}
# The returned static asset was normalized to exactly 1m high. This hypothesis
# is verified against every corner/face, never used to move the authoring rig.
scale=float(np.ptp(rx[:,1])/np.ptp(sx[:,1])); aligned=rx/scale
report['normalization']={'returned_per_source_uniform_scale':scale,'translation':[0,0,0],'axis':'identity glTF Y-up','position_tolerance_m':4e-5,'uv_tolerance':0.0004,'uv_tolerance_pixels_at_4k':1.6384,'rationale':'Explicit bounded numerical-rounding hypothesis; independently verify full bidirectional face ownership and UV corners.'}
forward,report['returned_to_source_corners']=mapping(sx,su,aligned,ru,4e-5,.0004)
reverse,report['source_to_returned_corners']=mapping(aligned,ru,sx,su,4e-5,.0004)
source_faces={}
for i,t in enumerate(st):source_faces.setdefault(tuple(sorted(map(int,t))),[]).append(i)
matched=[];missing=[];ambiguous=[];winding=0;used={};face_map=[];ambiguous_details=[]
for i,t in enumerate(rt):
    hits=set()
    candidates=[forward[int(v)] for v in t]
    if all(candidates):
        for comb in itertools.product(*candidates):hits.update(source_faces.get(tuple(sorted(comb)),[]))
    if len(hits)!=1:
        if hits:ambiguous_details.append({'returned_face':i,'candidates':[{'source_face':j,'owner':so[j],'xyz':sx[st[j]].tolist(),'uv':su[st[j]].tolist()} for j in sorted(hits)],'returned_xyz':aligned[t].tolist(),'returned_uv':ru[t].tolist()})
        (missing if not hits else ambiguous).append(i);face_map.append(-1);continue
    j=next(iter(hits));face_map.append(j);used[j]=used.get(j,0)+1
    target=st[j];valid=any(all(int(target[(k+shift)%3]) in candidates[k] for k in range(3)) for shift in range(3))
    if not valid:winding+=1
    matched.append(j)
initial_ambiguous=len(ambiguous)
# Enforce the global face bijection. Tiny tongue-tip faces have quantized UV
# corners; already uniquely owned adjacent faces disambiguate their candidates.
resolved=[]
for item in ambiguous_details:
    available=[v['source_face'] for v in item['candidates'] if v['source_face'] not in used]
    if len(available)==1:
        i=item['returned_face'];j=available[0];face_map[i]=j;used[j]=1;matched.append(j);resolved.append(i)
ambiguous=[i for i in ambiguous if i not in resolved]
report['global_bijection_resolution']={'initial_ambiguous':initial_ambiguous,'resolved_by_unused_source_face':resolved,'remaining':ambiguous}
uncovered=[i for i in range(len(st)) if i not in used];duplicate=[i for i,n in used.items() if n!=1]
report['faces']={'matched':len(matched),'unmatched':len(missing),'ambiguous':len(ambiguous),'winding_reversed':winding,'uncovered_source':len(uncovered),'duplicate_source':len(duplicate),'unmatched_examples':missing[:12],'ambiguous_examples':ambiguous[:12],'uncovered_examples':uncovered[:12]}
report['ambiguous_details']=ambiguous_details
report['coordinate_hypothesis']='Same glTF Y-up, explicit uniform returned-height normalization; no axis swaps or anisotropic/deform fit.'
report['pass']=not any([report['returned_to_source_corners']['unmatched'],report['source_to_returned_corners']['unmatched'],len(missing),len(ambiguous),winding,len(uncovered),len(duplicate)]) and snt==rnt
report['owner_reconstruction']='UNIQUE_FACE_BIJECTION' if report['pass'] else 'HOLD'
if report['pass']:
    returned_uv_in_source_order=np.empty((len(st),3,2));maxpos=0.;maxuv=0.
    for i,j in enumerate(face_map):
        options=[]
        for shift in range(3):
            ids=[(k+shift)%3 for k in range(3)];pd=np.linalg.norm(aligned[rt[i]][ids]-sx[st[j]],axis=1);ud=np.linalg.norm(ru[rt[i]][ids]-su[st[j]],axis=1)
            if pd.max()<4e-5 and ud.max()<.0004:options.append((float(pd.sum()),ids,pd,ud))
        assert options,('No winding-preserving corner permutation',i,j)
        _,ids,pd,ud=min(options,key=lambda v:v[0]);returned_uv_in_source_order[j]=ru[rt[i]][ids];maxpos=max(maxpos,float(pd.max()));maxuv=max(maxuv,float(ud.max()))
    report['verified_face_corner_error']={'max_position_m':maxpos,'max_uv':maxuv,'max_uv_pixels_4k':maxuv*4096}
    np.savez_compressed(E/'face-owner-correspondence.npz',returned_to_source_face=np.array(face_map),returned_face_owner=np.array([so[j] for j in face_map]),source_xyz=sx[st],source_uv=su[st],source_owner=np.array(so),returned_uv_in_source_order=returned_uv_in_source_order)
    report['owner_counts']={o:sum(so[j]==o for j in face_map) for o in sorted(set(so))}
for i,img in enumerate(rg.get('images',[])):
    v=rg['bufferViews'][img['bufferView']]; data=rb[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']];p=A/'texture-return-v005/source'/f'original-basecolor-{i}.jpg';p.write_bytes(data);report.setdefault('images',[]).append({'path':str(p.relative_to(ROOT)),'mime':img.get('mimeType'),'sha256':sha(p),'bytes':len(data)})
(E/'correspondence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k not in ['source','returned']},indent=2),flush=True)
