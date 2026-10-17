"""Synchronize v005 UV into the v004 portable GLBs without changing skin/morph/normal payloads."""
from pathlib import Path
import importlib.util,json,hashlib,copy
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'artifacts/pino-pretexture-v005'
OUT=ROOT/'docs/production/pino/evidence/pretexture-reliability-v005'
OLD=ROOT/'assets/grimo/production/pino/candidate-c/texture-handoff-v004'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/pretexture-reliability-v005'
s=importlib.util.spec_from_file_location('gl',ROOT/'scripts/3d/package-pino-texture-ready-v003.py');gl=importlib.util.module_from_spec(s);s.loader.exec_module(gl)
NAMES=['PINO_C_BASE_RIG_V001','PinoSoftLids_L','PinoSoftLids_R','PinoOralLiner']
def write_accessor(g,blob,index,values):
 a=g['accessors'][index];assert 'sparse' not in a
 bv=g['bufferViews'][a['bufferView']];dt=np.dtype(gl.DT[a['componentType']]);n=gl.SZ[a['type']]
 view=np.ndarray((a['count'],n),dtype=dt,buffer=blob,offset=bv.get('byteOffset',0)+a.get('byteOffset',0),strides=(bv.get('byteStride',n*dt.itemsize),dt.itemsize));view[:]=values
 if 'min' in a:a['min']=values.min(0).tolist()
 if 'max' in a:a['max']=values.max(0).tolist()
def main():
 d=np.load(TMP/'mesh-data.npz');inspect=json.loads((TMP/'inspect.json').read_text());source=np.load(OLD/'pino-c-v004-return-map.npz')
 mapping={k:source[k] for k in source.files};checks=[]
 for i,name in enumerate(NAMES):
  j=next(r['i'] for r in inspect if r['name']==name)
  assert np.array_equal(mapping[f'{i}_position'],d[f'{j}_p'].astype('<f4'))
  mapping[f'{i}_uv']=d[f'{j}_uv'].astype('<f4')
 np.savez_compressed(DEST/'pino-c-v005-return-map.npz',**mapping)
 for kind in ['tripo-input','rigged-review']:
  g,b=gl.read(OLD/f'pino-c-v004-{kind}.glb');before=copy.deepcopy(g);original=bytes(b);allowed=set();uv_indices=set()
  for node in g['nodes']:
   if 'mesh' not in node:continue
   name=node['name'].removesuffix('_TRIPO_INPUT');i=NAMES.index(name)
   for pr in g['meshes'][node['mesh']]['primitives']:
    ci=gl.accessor(g,b,pr['attributes']['_PINO_CORNER_ID']).ravel().round().astype(int);vi=gl.accessor(g,b,pr['attributes']['_PINO_VERTEX_ID']).ravel().round().astype(int)
    assert np.array_equal(mapping[f'{i}_corner_vertex'][ci],vi)
    uv=mapping[f'{i}_uv'][ci].copy();uv[:,1]=1-uv[:,1];idx=pr['attributes']['TEXCOORD_0'];uv_indices.add(idx)
    a=g['accessors'][idx];bv=g['bufferViews'][a['bufferView']];start=bv.get('byteOffset',0)+a.get('byteOffset',0);stride=bv.get('byteStride',8)
    for n in range(a['count']):allowed.update(range(start+n*stride,start+n*stride+8))
    write_accessor(g,b,idx,uv)
  changed=np.flatnonzero(np.frombuffer(original,'u1')!=np.frombuffer(b,'u1'))
  assert all(int(i) in allowed for i in changed)
  for idx in uv_indices:before['accessors'][idx]=g['accessors'][idx]
  assert before==g
  for node in g['nodes']:
   if 'mesh' in node:
    node.setdefault('extras',{})['UV_contract']='PinoUV_v005; synchronized Blend/input/review/map'
    node['extras']['v005_policy']='UV-only revision; Basis/topology/rig/weights/morph/normal/material ownership retained from v004'
  if 'PinoTextureContract' in g.get('extras',{}):g['extras']['PinoTextureContract']['uv']='PinoUV_v005'
  g.setdefault('extras',{})['PinoPreTextureV005']=dict(HumanGate='PENDING',uv='PinoUV_v005',rig_morph_normal_payload='v004 unchanged',texture='none')
  path=DEST/f'pino-c-v005-{kind}.glb';gl.write(path,g,b)
  checks.append(dict(file=path.name,changed_binary_bytes=len(changed),only_texcoord_bytes_changed=True,all_other_json_except_uv_bounds_and_v005_metadata_equal=True,uv_metadata_synchronized=True,meshes=len(g['meshes']),skins=len(g.get('skins',[])),animations=len(g.get('animations',[])),image_textures=len(g.get('images',[]))))
 (OUT/'delivery-consistency.json').write_text(json.dumps(dict(source='fe39c6d8aab1e550ee31823ca29e85b9b2658632',uv='PinoUV_v005',records=checks),indent=2), encoding='utf8', newline='\n')
 print(json.dumps(checks))
if __name__=='__main__':main()
