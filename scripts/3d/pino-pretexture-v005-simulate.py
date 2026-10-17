"""Representative local donor fixtures and bounded image-return checks."""
from pathlib import Path
import importlib.util,json,copy,io
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'artifacts/pino-pretexture-v005'
OUT=ROOT/'docs/production/pino/evidence/pretexture-reliability-v005'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/pretexture-reliability-v005'
s=importlib.util.spec_from_file_location('ret',ROOT/'scripts/3d/pino-pretexture-v005-return.py');ret=importlib.util.module_from_spec(s);s.loader.exec_module(ret)
gl=ret.gl
d=importlib.util.spec_from_file_location('delivery',ROOT/'scripts/3d/pino-pretexture-v005-delivery.py');delivery=importlib.util.module_from_spec(d);d.loader.exec_module(delivery)
SOURCE=DEST/'pino-c-v005-tripo-input.glb'
def fixture(path,image,changed=False,wrong_material=False,geometry_changed=False):
 g,b=gl.read(SOURCE);g=copy.deepcopy(g)
 image=Image.open(image).convert('RGB');n=image.width
 if changed:
  scale=.84;off=.08*(n-1)
  image=image.transform(image.size,Image.Transform.AFFINE,(0,1/scale,-off/scale,-1/scale,0,n-1+off/scale),resample=Image.Resampling.BILINEAR,fillcolor=(255,0,255))
  done=set()
  for m in g['meshes']:
   for pr in m['primitives']:
    idx=pr['attributes']['TEXCOORD_0']
    if idx in done:continue
    uv=gl.accessor(g,b,idx);q=uv.copy();q[:,1]=1-q[:,1]
    q=np.c_[.08+.84*q[:,1],.08+.84*(1-q[:,0])];q[:,1]=1-q[:,1]
    delivery.write_accessor(g,b,idx,q);done.add(idx)
 # Deliberately strip custom IDs and reorder primitives: return must work from
 # exact geometry and ownership, not hidden fixture-only attributes.
 for m in g['meshes']:
  m['primitives'].reverse()
  for pr in m['primitives']:
   for k in list(pr['attributes']):
    if k.startswith('_PINO_'):del pr['attributes'][k]
 if wrong_material:
  mats={m['name']:i for i,m in enumerate(g['materials'])}
  for m in g['meshes']:
   for pr in m['primitives']:
    if g['materials'][pr['material']]['name']=='Pino_Eye_L':pr['material']=mats['Pino_Skin']
 if geometry_changed:
  idx=g['meshes'][0]['primitives'][0]['attributes']['POSITION'];pos=gl.accessor(g,b,idx);pos[0,0]+=.002;delivery.write_accessor(g,b,idx,pos)
 stream=io.BytesIO();image.save(stream,format='PNG');raw=stream.getvalue()
 while len(b)%4:b.append(0)
 off=len(b);b.extend(raw);bi=len(g['bufferViews']);g['bufferViews'].append(dict(buffer=0,byteOffset=off,byteLength=len(raw)))
 g['images']=[dict(bufferView=bi,mimeType='image/png')];g['textures']=[dict(source=0)]
 for m in g['materials']:
  pbr=m.setdefault('pbrMetallicRoughness',{});pbr['baseColorTexture']=dict(index=0);pbr['baseColorFactor']=[1,1,1,1]
 gl.write(path,g,b)
def metrics(source_image,returned):
 a=np.asarray(Image.open(source_image).convert('RGB'))[::-1];b=np.asarray(Image.open(returned).convert('RGB'))[::-1]
 _,_,tri=ret.triangles(SOURCE);rows={}
 for mat in ['Pino_Skin','Pino_Eye_L','Pino_Eye_R','Pino_OralInterior','Pino_LidSkin']:
  uv=np.array([t['q'].mean(0) for t in tri if t['material']==mat]);aa=ret.bilinear(a,uv);bb=ret.bilinear(b,uv);err=np.abs(aa-bb)
  rows[mat]=dict(samples=len(uv),rgb_abs_mean=float(err.mean()),max_channel_p95=float(np.percentile(err.max(1),95)),max_channel=float(err.max()))
 return rows
def seams(path):
 im=np.asarray(Image.open(path).convert('RGB'))[::-1];_,_,tri=ret.triangles(SOURCE);edges={};samples=[]
 for t in tri:
  if t['material'] not in ['Pino_Skin','Pino_Eye_L','Pino_Eye_R']:continue
  for a,b in [(0,1),(1,2),(2,0)]:
   key=(t['material'],tuple(sorted(tuple(v) for v in np.round(t['p'][[a,b]]*1e6).astype(int))))
   uv=t['q'][[a,b]].mean(0);edges.setdefault(key,[]).append(uv)
 for key,uv in edges.items():
  if len(uv)==2 and np.linalg.norm(uv[0]-uv[1])>1e-5:samples.append((key[0],uv))
 result={}
 for mat in ['Pino_Skin','Pino_Eye_L','Pino_Eye_R']:
  q=np.array([u for m,u in samples if m==mat])
  if not len(q):continue
  col=ret.bilinear(im,q.reshape(-1,2)).reshape(-1,2,3);err=np.abs(col[:,0]-col[:,1]).max(1)
  result[mat]=dict(shared_seam_edges=len(q),max_channel_p50_p95_max=np.percentile(err,[50,95,100]).tolist(),edges_above_20=int((err>20).sum()))
 return result
def main():
 reports={};base=TMP/'diagnostic-color-4k.png'
 for label,changed in [('preserved',False),('changed',True)]:
  path=TMP/f'donor-{label}.glb';fixture(path,base,changed)
  out=TMP/f'returned-{label}-4k.png'
  report=ret.transfer(SOURCE,path,out);report['surface_error']=metrics(base,out);report['seams']=seams(out);reports[label]=report
 for label,kw in [('wrong-eye-owner',dict(wrong_material=True)),('geometry-drift',dict(geometry_changed=True))]:
  path=TMP/f'donor-rejected-{label}.glb';fixture(path,base,**kw)
  try:ret.mapping(SOURCE,path);raise AssertionError('Guard failed: '+label)
  except ret.Hold as e:reports[label]=dict(result='HOLD as intended',reason=str(e))
 # Probe hidden tail surfaces independently. No nearest transfer exists.
 surface=np.load(TMP/'surface.npz');idx=surface['triangle_image'];comp=surface['component'];xyz=surface['p'];owner=surface['owner']
 col=np.tile([30,80,180],(len(comp),1));col[comp==9]=[230,30,30];col[comp==8]=[20,220,40]
 # Join tail triangles only across manifold edges. The original pair shares
 # a nonmanifold root, so vertex connectivity alone hides one nested shell.
 par=np.arange(len(comp));edges={}
 def find(i):
  while par[i]!=i:par[i]=par[par[i]];i=par[i]
  return i
 for i in np.flatnonzero(np.isin(comp,[2,5])):
  for a,b in [(0,1),(1,2),(2,0)]:
   key=tuple(sorted(tuple(v) for v in xyz[i,[a,b]]));edges.setdefault(key,[]).append(i)
 for fs in edges.values():
  if len(fs)==2:par[find(fs[1])]=find(fs[0])
 roots=np.array([find(i) for i in range(len(comp))]);tailroots=np.unique(roots[np.isin(comp,[2,5])])
 groups=[np.isin(comp,[2,5])&(roots==r) for r in tailroots]
 assert len(groups)==3 and all(g.sum()==1476 for g in groups)
 for mask,c in zip(groups,[[220,30,200],[240,170,15],[15,220,220]]):col[mask]=c
 col[owner>0]=[255,0,255] # deliberately poisoned hidden lids/oral donor color
 rgb=np.full((*idx.shape,3),150,np.uint8);ok=idx>=0;rgb[ok]=col[idx[ok]]
 rgb=ret.pad(rgb,ok);sentinel=TMP/'sentinel-4k.png';Image.fromarray(rgb[::-1]).save(sentinel)
 path=TMP/'donor-sentinel.glb';fixture(path,sentinel,True);out=TMP/'returned-sentinel-4k.png';rep=ret.transfer(SOURCE,path,out)
 _,dq,_,_=ret.mapping(SOURCE,path);_,_,tris=ret.triangles(SOURCE)
 # Source source/returned comparison at real triangle centers, including occluded shells.
 rep['surface_error']=metrics(sentinel,out)
 a=np.asarray(Image.open(sentinel))[::-1];b=np.asarray(Image.open(out))[::-1]
 shell=[]
 # Surface and glTF ordering differ: use geometric matching, never row index.
 lookup={ret.triangle_key(np.c_[p[:,0],p[:,2],-p[:,1]],'Pino_Skin'):i for i,p in enumerate(xyz)}
 for group in groups:
  us=[t['q'].mean(0) for t in tris if t['material']=='Pino_Skin' and (j:=lookup.get(ret.triangle_key(t['p'],'Pino_Skin'))) is not None and group[j]]
  q=np.array(us);diff=np.abs(ret.bilinear(a,q)-ret.bilinear(b,q))
  shell.append(dict(triangles=len(q),mean_abs_rgb=float(diff.mean()),p95_max_channel=float(np.percentile(diff.max(1),95))))
 rep['three_tail_surface_partitions']=shell
 rep['hidden_fallback_policy']='Donor magenta is ignored for oral/lids; explicit original-owner fallback colors returned.'
 reports['sentinel']=rep
 reports['original_seams']=seams(base)
 reports['scope']='Local synthetic donors only; unchanged exact triangles. Real Tripo topology/UV/paint/4Mesh acceptance UNVERIFIED.'
 (OUT/'return-simulation.json').write_text(json.dumps(reports,indent=2)+'\n', encoding='utf8', newline='\n')
 print(json.dumps({k:v.get('result',v.get('surface_error')) for k,v in reports.items() if isinstance(v,dict)}))
if __name__=='__main__':main()
