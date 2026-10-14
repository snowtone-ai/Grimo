"""Local mouth-depth deformation in a separate GLB; preserve UVs and image bytes."""
import argparse, hashlib, json, struct
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v005.glb'
OUT=ROOT/'docs/production/shushu/evidence/tripo-mouth-depth-v006'
MIDLINE=None
def sha(b): return hashlib.sha256(b).hexdigest()
def read(path):
 raw=path.read_bytes(); length=struct.unpack_from('<I',raw,12)[0]
 assert raw[:4]==b'glTF' and struct.unpack_from('<I',raw,8)[0]==len(raw)
 return raw,json.loads(raw[20:20+length]),bytearray(raw[28+length:]),28+length
def accessor(j,b,i):
 a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3}[a['type']];dtype={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']]
 return np.ndarray((a['count'],n),dtype=dtype,buffer=b,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',np.dtype(dtype).itemsize*n),np.dtype(dtype).itemsize))
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def displacement(p,amount):
 x,h,z=p.T
 # The mouth width/height stay fixed. Recess the commissures and their cheek
 # transition, so the central smile has a rounded visible profile.
 w=(1-smooth(.050,.100,abs(x)))*smooth(.505,.568,h)*(1-smooth(.613,.635,h))*smooth(.17,.21,z)
 centre=np.interp(h,MIDLINE[0],MIDLINE[1])
 target=centre-(amount/.020)*.78*(np.sqrt(x*x+.020**2)-np.sqrt(.010**2+.020**2))
 # Fit a bounded transverse lip curve instead of adding a steep slope to
 # the existing cheek. The far lip must remain visible at 45 degrees.
 t=np.maximum(z-target,0)
 positive=np.where(t<.001,t*t/.002,t-.0005)
 return positive*smooth(.010,.014,abs(x))*w
def main():
 global MIDLINE
 ap=argparse.ArgumentParser();ap.add_argument('--amount',type=float,default=.020);ap.add_argument('--output',required=True);args=ap.parse_args()
 assert 0<=args.amount<=.05
 raw,j,b,offset=read(BASE);original=bytes(b);records={};allowed=np.zeros(len(b),dtype=bool)
 node=next(n for n in j['nodes'] if n.get('name')=='ShushuStatic_Head');pr=j['meshes'][node['mesh']]['primitives'][0];head=accessor(j,b,pr['attributes']['POSITION'])
 samples=[]
 for h in np.linspace(.495,.645,301):
  score=((abs(head[:,0])-.010)/.003)**2+((head[:,1]-h)/.0015)**2;score[head[:,2]<.10]=1e9
  ids=np.argsort(score)[:6];samples.append(float(np.average(head[ids,2],weights=np.exp(-score[ids]/2))))
 heights=np.linspace(.495,.645,301)
 curve=np.polynomial.polynomial.polyfit((heights-.57)/.075,samples,7)
 MIDLINE=(heights,np.polynomial.polynomial.polyval((heights-.57)/.075,curve))
 for name in ['ShushuStatic_Head','ShushuStatic_MouthInterior']:
  node=next(n for n in j['nodes'] if n.get('name')==name);pr=j['meshes'][node['mesh']]['primitives'][0]
  a=pr['attributes'];p=accessor(j,b,a['POSITION']);n=accessor(j,b,a['NORMAL']);before=p.copy();oldn=n.copy()
  delta=displacement(before,args.amount);changed=delta>1e-9;p[:,2]-=delta
  # Transform the source smooth normals with the deformation cofactor.
  # This stays finite when the fitted surface is independent of source Z,
  # and approaches the original normal smoothly at the support boundary.
  grad=[];eps=1e-5
  for axis in range(3):
   plus=before.astype(float).copy();minus=before.astype(float).copy();plus[:,axis]+=eps;minus[:,axis]-=eps
   grad.append((displacement(plus,args.amount)-displacement(minus,args.amount))/(2*eps))
  new=np.column_stack((oldn[:,0]*(1-grad[2])+grad[0]*oldn[:,2],oldn[:,1]*(1-grad[2])+grad[1]*oldn[:,2],oldn[:,2]))
  length=np.linalg.norm(new,axis=1);assert np.all(length[changed]>1e-12);normal_changed=changed.copy()
  new[changed]/=length[changed,None];n[changed]=new[changed]
  for key in ['POSITION','NORMAL']:
   ac=j['accessors'][a[key]];v=j['bufferViews'][ac['bufferView']];start=v.get('byteOffset',0)+ac.get('byteOffset',0);stride=v.get('byteStride',12)
   for i in np.flatnonzero(changed if key=='POSITION' else normal_changed): allowed[start+i*stride:start+i*stride+12]=True
  assert np.array_equal(p[:,:2],before[:,:2]);assert np.array_equal(p[~changed],before[~changed]);assert np.array_equal(n[~normal_changed],oldn[~normal_changed])
  records[name]={'changed_vertices':int(sum(changed)),'changed_normals':int(sum(normal_changed)),'max_depth_change':float(delta.max()),'before_bounds':[before.min(0).tolist(),before.max(0).tolist()],'after_bounds':[p.min(0).tolist(),p.max(0).tolist()], 'vertices':np.flatnonzero(changed).tolist(),'normal_vertices':np.flatnonzero(normal_changed).tolist()}
  if name=='ShushuStatic_Head':
   assert np.array_equal(before.min(0),p.min(0)) and np.array_equal(before.max(0),p.max(0))
 final=raw[:offset]+b;changed_bytes=np.frombuffer(original,dtype=np.uint8)!=np.frombuffer(b,dtype=np.uint8)
 assert not np.any(changed_bytes&~allowed)
 path=ROOT/args.output;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(final)
 OUT.mkdir(parents=True,exist_ok=True)
 record={'base':BASE.relative_to(ROOT).as_posix(),'base_sha256':sha(raw),'candidate':path.relative_to(ROOT).as_posix(),'candidate_sha256':sha(final),'amount':args.amount,'changed_bytes':int(sum(changed_bytes)),'json_chunk_byte_identical':True,'outside_local_position_normal_bytes_identical':True,'front_XY_identical':True,'all_textures_UV_topology_nodes_materials_identical':True,'meshes':records}
 (OUT/'geometry-validation.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k!='meshes'}))
if __name__=='__main__':main()
