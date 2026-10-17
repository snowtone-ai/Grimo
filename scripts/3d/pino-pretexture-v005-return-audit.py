"""Complete shell/fallback sampling with float64 correspondence keys."""
from pathlib import Path
import importlib.util,json,hashlib,copy,numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('sim',ROOT/'scripts/3d/pino-pretexture-v005-simulate.py');sim=importlib.util.module_from_spec(s);s.loader.exec_module(sim)
ret=sim.ret;TMP=sim.TMP;OUT=sim.OUT
def main():
 report=json.loads((OUT/'return-simulation.json').read_text());_,_,tri=ret.triangles(sim.SOURCE)
 for label in ['preserved','changed','sentinel']:
  donor=TMP/f'donor-{label}.glb';out=TMP/f'returned-{label}-4k.png';ret.mapping(sim.SOURCE,donor)
  report[label]['source_sha256']=hashlib.sha256(sim.SOURCE.read_bytes()).hexdigest();report[label]['donor_sha256']=hashlib.sha256(donor.read_bytes()).hexdigest();report[label]['baseColor_only']=True
  image=np.asarray(Image.open(out).convert('RGB'))[::-1];checks={}
  for mat,color in {'Pino_OralInterior':[57,27,39],'Pino_LidSkin':[150,201,242]}.items():
   uv=np.array([t['q'].mean(0) for t in tri if t['material']==mat]);err=np.abs(ret.bilinear(image,uv)-color)
   checks[mat]=dict(triangles=len(uv),expected_rgb=color,max_abs_error=float(err.max()))
   assert err.max()<1e-5
  report[label]['hidden_fallback_exact']=checks
 for label in ['wrong-eye-owner','geometry-drift']:
  try:ret.mapping(sim.SOURCE,TMP/f'donor-rejected-{label}.glb');raise AssertionError('Guard failure')
  except ret.Hold:pass
 guards={}
 dg,db=ret.gl.read(TMP/'donor-changed.glb')
 for label in ['basecolor-factor','texture-transform','parent-transform']:
  g=copy.deepcopy(dg);mat=next(m for m in g['materials'] if m['name']=='Pino_Skin')
  if label=='basecolor-factor':mat['pbrMetallicRoughness']['baseColorFactor']=[.5,1,1,1]
  if label=='texture-transform':mat['pbrMetallicRoughness']['baseColorTexture']['extensions']={'KHR_texture_transform':{'offset':[.1,0]}}
  if label=='parent-transform':g['nodes'].append(dict(children=[0],translation=[.1,0,0]))
  path=TMP/f'donor-rejected-{label}.glb';ret.gl.write(path,g,db)
  try:
   if label=='parent-transform':ret.mapping(sim.SOURCE,path)
   else:ret.embedded_image(g,db,'Pino_Skin',path)
   raise AssertionError('Unsupported donor configuration was accepted')
  except ret.Hold as e:guards[label]=dict(result='HOLD as intended',reason=str(e))
 report['unsupported_configuration_guards']=guards
 data=np.load(TMP/'surface.npz');xyz=data['p'];comp=data['component'];par=np.arange(len(comp));edges={}
 def find(i):
  while par[i]!=i:par[i]=par[par[i]];i=par[i]
  return i
 for i in np.flatnonzero(np.isin(comp,[2,5])):
  for a,b in [(0,1),(1,2),(2,0)]:
   key=tuple(sorted(tuple(v) for v in xyz[i,[a,b]]));edges.setdefault(key,[]).append(i)
 for fs in edges.values():
  if len(fs)==2:par[find(fs[1])]=find(fs[0])
 roots=np.array([find(i) for i in range(len(comp))]);tailroots=np.unique(roots[np.isin(comp,[2,5])]);lookup={ret.triangle_key(np.c_[p[:,0],p[:,2],-p[:,1]],'Pino_Skin'):i for i,p in enumerate(xyz)}
 a=np.asarray(Image.open(TMP/'sentinel-4k.png'))[::-1];b=np.asarray(Image.open(TMP/'returned-sentinel-4k.png'))[::-1];shell=[]
 for r in tailroots:
  mask=np.isin(comp,[2,5])&(roots==r);us=[t['q'].mean(0) for t in tri if t['material']=='Pino_Skin' and (j:=lookup.get(ret.triangle_key(t['p'],'Pino_Skin'))) is not None and mask[j]]
  assert len(us)==1476
  q=np.array(us);diff=np.abs(ret.bilinear(a,q)-ret.bilinear(b,q));verts=xyz[mask].reshape(-1,3)
  shell.append(dict(triangles=len(q),bounds_m=[verts.min(0).tolist(),verts.max(0).tolist()],mean_abs_rgb=float(diff.mean()),p95_max_channel=float(np.percentile(diff.max(1),95)),max_channel=float(diff.max())))
 report['sentinel']['three_tail_surface_partitions']=shell
 report['fallback_metric_note']='Oral/lid source-image differences are intentional fallback replacement, not donor color fidelity. hidden_fallback_exact tests the required result. All three actual tail shells are sampled by manifold-edge connectivity.'
 report['filtering_risk']='Changed-UV donor is a 0.84-scale affine image mock. Resampling high contrast details/subpixel islands is lossy; seam/texel errors are reported, not asserted as perfect or real Tripo quality.'
 (OUT/'return-simulation.json').write_text(json.dumps(report,indent=2)+'\n', encoding='utf8', newline='\n')
 print(json.dumps(dict(shells=shell,fallbacks=report['sentinel']['hidden_fallback_exact'])))
if __name__=='__main__':main()
