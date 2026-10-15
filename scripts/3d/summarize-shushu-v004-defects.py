"""Compare saved eight-weight oracle to Blender evaluation; extract original texture bytes."""
import json,struct,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-skin-compat'
src=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.glb'
b=src.read_bytes();length=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+length]);binary=b[28+length:]
def norm(x):return x/np.maximum(np.linalg.norm(x,axis=1,keepdims=True),1e-15)
def stats(x):return {'max':float(np.max(x)),'p95':float(np.percentile(x,95)),'median':float(np.median(x))}
def convert(x):return np.array(x)[:,[0,2,1]]*np.array([1,-1,1])
surfaces=json.loads((OUT/'surface-oracle.json').read_text());maps={};rows=[]
for row in surfaces:
 f=row['frame'];a=np.load(OUT/f'blender-author/normals-{f}.npz');s=np.load(OUT/f'blender-saved/normals-{f}.npz')
 for m in row['meshes']:
  name=m['name']
  if 'Paw' not in name:continue
  p=convert(m['position']);n=convert(m['normal'])
  if f==1:
   maps[name]={}
   for label,v in [('author',a),('saved',s)]:
    base=v[name+'-p'];ids=[]
    for chunk in np.array_split(p,20):ids.extend(np.argmin(((chunk[:,None,:]-base[None,:,:])**2).sum(2),axis=1).tolist())
    maps[name][label]=np.array(ids)
  result={'frame':f,'mesh':name}
  for label,v in [('author',a),('saved',s)]:
   ids=maps[name][label];result[label+'PositionH']=stats(np.linalg.norm(p-v[name+'-p'][ids],axis=1))
   result[label+'NormalDeg']=stats(np.degrees(np.arccos(np.clip((norm(n)*norm(v[name+'-n'][ids])).sum(1),-1,1))))
  rows.append(result)
images=[]
for name in ['ShushuStatic_Head','ShushuStatic_MouthInterior']:
 mesh=next(m for m in j['meshes'] if m['name']==name);material=j['materials'][mesh['primitives'][0]['material']];im=j['images'][j['textures'][material['pbrMetallicRoughness']['baseColorTexture']['index']]['source']];bv=j['bufferViews'][im['bufferView']];raw=binary[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']];filename=name+'-original-basecolor.'+('png' if im['mimeType']=='image/png' else 'jpg');(OUT/filename).write_bytes(raw);images.append({'mesh':name,'file':filename,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'method':'Exact embedded image bytes, no decode/re-encode or color transform','material':material})
report={'units':'H = approved neutral height about 1; angles compare exported glTF eight-weight normal against evaluated Blender vertex normal. Neutral nearest-position maps include duplicated UV vertices. Maximum is not a Human score.','rows':rows,'textures':images}
(OUT/'local-defects-numeric.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(rows,indent=2))
