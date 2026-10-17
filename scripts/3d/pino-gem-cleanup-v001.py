"""Diagnose the exact Tripo donor; preserve GLB payload except proven local image edits."""
from pathlib import Path
import sys, json, importlib.util, hashlib, io
from collections import Counter
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/pino/evidence/tripo-gem-cleanup-v001'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v001'
SOURCE=ROOT/'assets/grimo/production/pino/candidate-c/pretexture-reliability-v005/pino-c-v005-tripo-input.glb'
DONOR=DEST/'pino-c-v005-tripo-donor-original.glb'
def module(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
gl=module('gl','scripts/3d/package-pino-texture-ready-v003.py')
ret=module('ret','scripts/3d/pino-pretexture-v005-return.py')
def write(n,d): (OUT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tris(g,b):
 rows=[]
 for node in g['nodes']:
  if 'mesh' not in node:continue
  for pr in g['meshes'][node['mesh']]['primitives']:
   p=gl.accessor(g,b,pr['attributes']['POSITION']);ids=gl.accessor(g,b,pr['indices']).reshape(-1,3)
   for t in ids:rows.append((ret.triangle_key(p[t],''),node['name'],g['materials'][pr['material']]['name']))
 return rows
def inspect():
 sg,sb=gl.read(SOURCE);dg,db=gl.read(DONOR);s=tris(sg,sb);d=tris(dg,db)
 sc=Counter(t[0] for t in s);dc=Counter(t[0] for t in d)
 ownership=Counter()
 lookup={t[0]:t[2] for t in s}
 for key,node,mat in d:ownership[(lookup.get(key,'NO MATCH'),mat)]+=1
 write('diagnosis.json',{'source_sha256':sha(SOURCE),'donor_sha256':sha(DONOR),'source_triangles':len(s),'donor_triangles':len(d),'exact_geometry_multiset_equal':sc==dc,'extra_triangles':sum((dc-sc).values()),'missing_triangles':sum((sc-dc).values()),'ownership': [{'source':a,'donor':b,'triangles':n} for (a,b),n in ownership.items()]})
 for i,im in enumerate(dg['images']):
  v=dg['bufferViews'][im['bufferView']];raw=db[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
  image=Image.open(io.BytesIO(raw))
  if i==2:image.save(OUT/f'donor-image-{i}.png')
  if i==2:image.resize((1024,1024),Image.Resampling.NEAREST).save(OUT/'oral-atlas-enlarged.png')
 try:ret.mapping(SOURCE,DONOR);result={'status':'PASS'}
 except ret.Hold as e:result={'status':'HOLD','reason':str(e)}
 write('return-contract.json',result)
if __name__=='__main__':inspect()
