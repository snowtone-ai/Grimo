"""Image-only donor return for the fixed Pino v005 master.

Exact triangles + material ownership are required. Reordered/split vertices and
changed UV are supported; missing/ambiguous topology correspondence is a HOLD.
This intentionally does not guess nearest surfaces or import donor rigs.
"""
from pathlib import Path
import argparse, importlib.util, json, io, hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
gl=module('pino_gl','scripts/3d/package-pino-texture-ready-v003.py')
atlas=module('pino_atlas','scripts/3d/pino-pretexture-v005-atlas.py')
class Hold(ValueError):pass
def triangle_key(p,material):
 return (material,tuple(sorted(tuple(v) for v in np.round(np.asarray(p,dtype=np.float64)*1e6).astype(np.int64))))
def triangles(path):
 g,b=gl.read(Path(path));rows=[]
 names=[m.get('name') for m in g['materials']]
 if None in names or len(names)!=len(set(names)):raise Hold('Material names must be unique and explicit.')
 # No hidden parent transform or active posed skin may change the neutral frame.
 for node in g['nodes']:
  if 'skin' in node:raise Hold('Use a static neutral donor, not posed/skinned geometry.')
  mat=node.get('matrix',np.eye(4).T.ravel().tolist())
  if not np.allclose(np.array(mat),np.eye(4).T.ravel(),atol=1e-6) or node.get('translation',[0,0,0])!=[0,0,0] or node.get('rotation',[0,0,0,1])!=[0,0,0,1] or node.get('scale',[1,1,1])!=[1,1,1]:raise Hold('Nonidentity scene/parent transform: normalize and verify explicitly.')
 for node in g['nodes']:
  if 'mesh' not in node:continue
  for pr in g['meshes'][node['mesh']]['primitives']:
   if pr.get('mode',4)!=4:raise Hold('Only explicit triangle primitives are supported.')
   material=g['materials'][pr['material']]['name']
   p=gl.accessor(g,b,pr['attributes']['POSITION'])
   if not np.isfinite(p).all():raise Hold('Nonfinite donor positions.')
   uv=gl.accessor(g,b,pr['attributes']['TEXCOORD_0'])
   ids=gl.accessor(g,b,pr['indices']).astype(int).ravel().reshape(-1,3)
   if not np.isfinite(uv).all() or ((uv<0)|(uv>1)).any():raise Hold('Nonfinite/out-of-0-1 donor UV.')
   # glTF texture v-down. Geometry is kept in glTF coordinates for comparison.
   q=uv.copy();q[:,1]=1-q[:,1]
   for tri in ids:rows.append(dict(p=p[tri],q=q[tri],material=material,primitive=pr))
 return g,b,rows
def embedded_image(g,b,material,path):
 m=next(m for m in g['materials'] if m['name']==material)
 pbr=m.get('pbrMetallicRoughness',{});tex=pbr.get('baseColorTexture')
 if tex is None:raise Hold('Missing baseColorTexture: '+material)
 if tex.get('texCoord',0)!=0 or tex.get('extensions'):raise Hold('Only TEXCOORD_0 without texture transforms/extensions is supported.')
 if not np.allclose(pbr.get('baseColorFactor',[1,1,1,1]),[1,1,1,1],atol=1e-6):raise Hold('Bake/verify nonwhite baseColorFactor explicitly before image return.')
 if m.get('alphaMode','OPAQUE')!='OPAQUE' or m.get('extensions'):raise Hold('Only opaque standard BaseColor is supported; review material extensions explicitly.')
 ti=g['textures'][tex['index']]['source'];im=g['images'][ti]
 if 'bufferView' in im:
  view=g['bufferViews'][im['bufferView']];off=view.get('byteOffset',0);raw=bytes(b[off:off+view['byteLength']]);return np.asarray(Image.open(io.BytesIO(raw)).convert('RGB'))[::-1]
 uri=im.get('uri','')
 if not uri or ':' in uri or uri.startswith(('/', '\\')) or '..' in Path(uri).parts:raise Hold('Only embedded or local sibling images supported.')
 return np.asarray(Image.open(Path(path).parent/uri).convert('RGB'))[::-1]
def bilinear(im,uv):
 h,w=im.shape[:2];x=np.clip(uv[:,0]*w-.5,0,w-1);y=np.clip(uv[:,1]*h-.5,0,h-1)
 x0=x.astype(int);y0=y.astype(int);x1=np.minimum(x0+1,w-1);y1=np.minimum(y0+1,h-1);a=(x-x0)[:,None];b=(y-y0)[:,None]
 return im[y0,x0]*(1-a)*(1-b)+im[y0,x1]*a*(1-b)+im[y1,x0]*(1-a)*b+im[y1,x1]*a*b
def mapping(source,donor):
 sg,sb,target=triangles(source);dg,db,ds=triangles(donor)
 if len(ds)!=len(target):raise Hold('Triangle coverage/topology changed; explicit correspondence required.')
 lookup={}
 for j,t in enumerate(ds):lookup.setdefault(triangle_key(t['p'],t['material']),[]).append(j)
 matched=[];used=set()
 for t in target:
  candidates=lookup.get(triangle_key(t['p'],t['material']),[])
  if len(candidates)!=1:raise Hold('Missing/ambiguous exact triangle or material ownership; no nearest projection.')
  j=candidates[0];d=ds[j]
  if j in used:raise Hold('Duplicate triangle correspondence.')
  used.add(j);perm=[]
  for p in t['p']:
   dist=np.linalg.norm(d['p']-p,axis=1);k=int(dist.argmin())
   if dist[k]>1e-6 or k in perm:raise Hold('Ambiguous vertex in exact triangle.')
   perm.append(k)
  matched.append(d['q'][perm])
 return target,np.array(matched),dg,db
def pad(rgb,coverage,steps=5):
 known=coverage.copy()
 for step in range(steps):
  new=known.copy()
  for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
   h,w=known.shape;a=(slice(max(0,dy),min(h,h+dy)),slice(max(0,dx),min(w,w+dx)));b=(slice(max(0,-dy),min(h,h-dy)),slice(max(0,-dx),min(w,w-dx)))
   fill=(~new[a])&known[b];part=rgb[a];part[fill]=rgb[b][fill];new[a]|=fill
  known=new
 rgb[~known]=[154,205,246];return rgb
def transfer(source,donor,output,size=4096):
 target,dq,g,b=mapping(source,donor);rgb=np.zeros((size,size,3),np.uint8);coverage=np.zeros((size,size),bool);images={};counts={}
 fallback={'Pino_OralInterior':[57,27,39],'Pino_LidSkin':[150,201,242]}
 for ti,(t,uv) in enumerate(zip(target,dq)):
  material=t['material'];xx,yy,bc=atlas.raster(t['q'],size)
  counts[material]=counts.get(material,0)+len(xx)
  # Include exact boundary samples for subpixel target triangles. These are
  # gutter support only; later true interior raster samples take precedence.
  bary=np.array([[1,0,0],[0,1,0],[0,0,1],[.5,.5,0],[0,.5,.5],[.5,0,.5],[1/3,1/3,1/3]])
  support=np.clip(np.floor((bary@t['q'])*size).astype(int),0,size-1)
  if material in fallback:support_color=np.tile(fallback[material],(len(bary),1))
  else:
   if material not in images:images[material]=embedded_image(g,b,material,donor)
   support_color=bilinear(images[material],bary@uv)
  sx,sy=support.T;missing=~coverage[sy,sx];rgb[sy[missing],sx[missing]]=np.uint8(np.clip(np.round(support_color[missing]),0,255));coverage[sy[missing],sx[missing]]=True
  if not len(xx):continue
  if material in fallback:color=np.tile(fallback[material],(len(xx),1))
  else:
   if material not in images:images[material]=embedded_image(g,b,material,donor)
   color=bilinear(images[material],bc@uv)
  rgb[yy,xx]=np.uint8(np.clip(np.round(color),0,255));coverage[yy,xx]=True
 Image.fromarray(pad(rgb,coverage)[::-1]).save(output)
 return dict(triangles=len(target),covered_pixels=int(coverage.sum()),samples_by_material=counts,fallback=fallback,geometry_replacement=False,matching='whole neutral triangle + material; 1 micrometer tolerance; permutation validated',tripo_compatibility='UNVERIFIED',baseColor_only=True,source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),donor_sha256=hashlib.sha256(Path(donor).read_bytes()).hexdigest(),output_sha256=hashlib.sha256(Path(output).read_bytes()).hexdigest())
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--donor',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--size',type=int,default=4096);a=p.parse_args()
 try:
  r=transfer(a.source,a.donor,a.output,a.size)
  a.output.with_suffix('.return.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8', newline='\n')
  print(json.dumps(r,indent=2))
 except Hold as e:raise SystemExit('HOLD: '+str(e))
if __name__=='__main__':main()
