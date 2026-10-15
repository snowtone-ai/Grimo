"""Add verified portable morph normals while retaining GLB provenance attributes."""
from pathlib import Path
import json,struct,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'artifacts/pino-texture-v003'
OUT=ROOT/'docs/production/pino/evidence/texture-ready-v003'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/texture-ready-v003'

def read(path):
    raw=path.read_bytes();n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);pos=20+n
    size,kind=struct.unpack_from('<I4s',raw,pos);assert kind==b'BIN\0';return g,bytearray(raw[pos+8:pos+8+size])

DT={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1',5122:'<i2',5120:'i1'}
SZ={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def accessor(g,blob,index):
    a=g['accessors'][index];n=SZ[a['type']];dt=np.dtype(DT[a['componentType']]);out=np.zeros((a['count'],n),dtype=dt)
    if 'bufferView' in a:
        b=g['bufferViews'][a['bufferView']];offset=b.get('byteOffset',0)+a.get('byteOffset',0);stride=b.get('byteStride',dt.itemsize*n)
        out=np.ndarray((a['count'],n),dtype=dt,buffer=blob,offset=offset,strides=(stride,dt.itemsize)).copy()
    if 'sparse' in a:
        s=a['sparse'];ib=g['bufferViews'][s['indices']['bufferView']];vb=g['bufferViews'][s['values']['bufferView']]
        ii=np.frombuffer(blob,dtype=DT[s['indices']['componentType']],count=s['count'],offset=ib.get('byteOffset',0)+s['indices'].get('byteOffset',0))
        vv=np.frombuffer(blob,dtype=dt,count=s['count']*n,offset=vb.get('byteOffset',0)+s['values'].get('byteOffset',0)).reshape(-1,n);out[ii]=vv
    return out

def append(g,blob,array):
    while len(blob)%4:blob.append(0)
    a=np.asarray(array,dtype='<f4');offset=len(blob);blob.extend(a.tobytes());bi=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':a.nbytes,'target':34962})
    ai=len(g['accessors']);g['accessors'].append({'bufferView':bi,'componentType':5126,'count':len(a),'type':'VEC3'});return ai

def write(path,g,blob):
    while len(blob)%4:blob.append(0)
    g['buffers'][0]['byteLength']=len(blob);j=json.dumps(g,separators=(',',':'),ensure_ascii=False).encode();j+=b' '*((-len(j))%4)
    path.write_bytes(struct.pack('<III',0x46546c67,2,28+len(j)+len(blob))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(blob),b'BIN\0')+blob)

def patch():
    path=DEST/'pino-c-texture-ready-v003-HOLD.glb';g,blob=read(path);bank=np.load(TMP/'delivery-normal-bank.npz');meta=json.loads((TMP/'delivery-normal-meta.json').read_text());records=[]
    for mesh in g['meshes']:
        idx=next(i for i,m in enumerate(meta) if m['mesh']==mesh['name']);rec=meta[idx];vid=bank[f'{idx}_vid'];base=bank[f'{idx}_base']
        byid={}
        for li,vi in enumerate(vid):byid.setdefault(int(vi),[]).append(li)
        for prim in mesh['primitives']:
            ids=accessor(g,blob,prim['attributes']['_PINO_VERTEX_ID']).ravel().round().astype(int)
            nn=accessor(g,blob,prim['attributes']['NORMAL']);blender=np.c_[nn[:,0],-nn[:,2],nn[:,1]]
            loops=accessor(g,blob,prim['attributes']['_PINO_CORNER_ID']).ravel().round().astype(int)
            assert np.array_equal(vid[loops],ids),'corner/vertex provenance mismatch'
            valid=np.linalg.norm(base[loops],axis=1)>.5
            error=float(np.linalg.norm(base[loops][valid]-blender[valid],axis=1).max(initial=0))
            assert error<1e-4,(mesh['name'],error)
            for ki,name in enumerate(rec['keys']):
                dn=bank[f'{idx}_target{ki}'][loops];gl=np.c_[dn[:,0],dn[:,2],-dn[:,1]]
                prim['targets'][ki]['NORMAL']=append(g,blob,gl)
            records.append({'object':rec['object'],'vertices':len(ids),'base_normal_mapping_max':error,'source_zero_normals_exporter_fallback':int((~valid).sum()),'morph_normal_targets':len(rec['keys'])})
    g.setdefault('extras',{})['PinoTextureContract']={'status':'HOLD','HumanGate':'PENDING','TextureGO':False,'uv':'PinoUV_v003','skin':'LBS4','normal_policy':'canonical corner normals at Basis; local corner target deltas for morphs','provenance':'_PINO_VERTEX_ID is the editing-master vertex index per mesh'}
    write(path,g,blob)
    (OUT/'glb-normal-patch.json').write_text(json.dumps({'records':records,'glb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size},indent=2)+'\n')

if __name__=='__main__':patch()
