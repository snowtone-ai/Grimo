"""Bounded four-influence fit. No geometry, morph, rig, animation or texture changes."""
from pathlib import Path
import hashlib
import itertools
import json
import struct
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-skin-compat'
SOURCE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.glb'
data=json.loads((OUT/'fit-data.json').read_text())
raw=SOURCE.read_bytes(); length=struct.unpack_from('<I',raw,12)[0]
doc=json.loads(raw[20:20+length]); binary=bytearray(raw[28+length:]); original=bytes(binary)
def offset(accessor):
    a=doc['accessors'][accessor];v=doc['bufferViews'][a['bufferView']]
    assert not v.get('byteStride') and a['type']=='VEC4'
    return a,v.get('byteOffset',0)+a.get('byteOffset',0)
meshes={};allowed=set()
for m in doc['meshes']:
    p=m['primitives'][0];attrs=p['attributes']
    if 'WEIGHTS_1' not in attrs:continue
    wa,wo=offset(attrs['WEIGHTS_0']);ja,jo=offset(attrs['JOINTS_0'])
    assert wa['componentType']==5126 and ja['componentType'] in [5121,5123]
    weights=np.frombuffer(binary,dtype='<f4',count=wa['count']*4,offset=wo).copy().reshape(-1,4)
    joints=np.frombuffer(binary,dtype='<u2' if ja['componentType']==5123 else 'u1',count=ja['count']*4,offset=jo).copy().reshape(-1,4)
    meshes[m['name']]={'weights':weights,'joints':joints,'wo':wo,'jo':jo}

records=[]
for row in data['entries']:
    gram=np.array(row['gram']).reshape(8,8)
    active=[i for i,x in enumerate(row['influences']) if x['w']>0]
    best=None
    # Enumerate faces of the non-negative simplex, so boundary solutions are also included.
    for count in range(1,min(4,len(active))+1):
        for ids in itertools.combinations(active,count):
            g=gram[np.ix_(ids,ids)]
            kkt=np.block([[g,np.ones((count,1))],[np.ones((1,count)),np.zeros((1,1))]])
            solution=np.linalg.lstsq(kkt,np.r_[np.zeros(count),1.0],rcond=1e-13)[0][:count]
            if np.min(solution)<-1e-9:continue
            solution=np.maximum(solution,0);solution/=solution.sum()
            loss=float(solution@g@solution)
            if best is None or loss<best[0]:best=(loss,ids,solution)
    loss,ids,w=best;mesh=meshes[row['mesh']];i=row['vertex']
    mesh['weights'][i]=0;mesh['joints'][i]=0
    for k,(slot,weight) in enumerate(zip(ids,w)):
        mesh['weights'][i,k]=weight;mesh['joints'][i,k]=row['influences'][slot]['id']
    records.append({'mesh':row['mesh'],'vertex':i,'squaredPositionPlusNormalLoss':loss,'slots':list(ids)})

output={'method':'non-negative simplex least squares, all original nonzero-joint supports of size <=4; position plus 0.05H normalized normal vector residual','fitFrames':data['frames'],'meshes':{}}
for name,m in meshes.items():
    # Normalize unaffected rows too; only original JOINTS_0 / WEIGHTS_0 bytes are eligible.
    m['weights']/=m['weights'].sum(axis=1)[:,None]
    for field,size,off in [('weights',4,m['wo']),('joints',2,m['jo'])]:
        b=m[field].tobytes();binary[off:off+len(b)]=b;allowed.update(range(off,off+len(b)))
    output['meshes'][name]={'weights':m['weights'].ravel().tolist(),'joints':m['joints'].ravel().tolist()}
    attrs=next(x for x in doc['meshes'] if x['name']==name)['primitives'][0]['attributes']
    del attrs['JOINTS_1'];del attrs['WEIGHTS_1']
changed=[i for i,(a,b) in enumerate(zip(original,binary)) if a!=b]
assert all(i in allowed for i in changed)
j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
glb=struct.pack('<5I',0x46546c67,2,28+len(j)+len(binary),len(j),0x4e4f534a)+j+struct.pack('<2I',len(binary),0x004e4942)+binary
(OUT/'shushu-v004-optimized4.glb').write_bytes(glb)
(OUT/'optimized-weights.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
(OUT/'optimization.json').write_text(json.dumps({'method':output['method'],'frames':len(data['frames']),'vertices':len(records),'changedBytes':len(changed),'unexpectedBytes':0,'sourceSHA256':hashlib.sha256(raw).hexdigest(),'candidateSHA256':hashlib.sha256(glb).hexdigest(),'candidateBytes':len(glb),'records':records},indent=2)+'\n')
print('Optimized',len(records),'vertices;',len(changed),'allowed bytes changed')
