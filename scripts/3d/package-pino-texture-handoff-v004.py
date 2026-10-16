"""Portable normal targets, UV/provenance audit, and runtime probe controls."""
from pathlib import Path
import sys,importlib.util,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('gl',ROOT/'scripts/3d/package-pino-texture-ready-v003.py');gl=importlib.util.module_from_spec(sp);sp.loader.exec_module(gl)
DEST=ROOT/'assets/grimo/production/pino/candidate-c/texture-handoff-v004';OUT=ROOT/'docs/production/pino/evidence/texture-handoff-v004';TMP=ROOT/'artifacts/pino-texture-v004'
def dump(n,x):(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def main():
 p=DEST/'pino-c-v004-rigged-review.glb';g,blob=gl.read(p);bank=np.load(TMP/'normal-bank.npz');meta=json.loads((TMP/'normal-meta.json').read_text());recs=[]
 for mesh in g['meshes']:
  idx=next(i for i,m in enumerate(meta) if m['mesh']==mesh['name']);rec=meta[idx];vid=bank[f'{idx}_vid'];base=bank[f'{idx}_base']
  for prim in mesh['primitives']:
   ids=gl.accessor(g,blob,prim['attributes']['_PINO_VERTEX_ID']).ravel().round().astype(int);loops=gl.accessor(g,blob,prim['attributes']['_PINO_CORNER_ID']).ravel().round().astype(int)
   assert np.array_equal(vid[loops],ids)
   nn=gl.accessor(g,blob,prim['attributes']['NORMAL']);bl=np.c_[nn[:,0],-nn[:,2],nn[:,1]];valid=np.linalg.norm(base[loops],axis=1)>.5;err=float(np.linalg.norm(base[loops][valid]-bl[valid],axis=1).max(initial=0));assert err<1e-4
   for ki,name in enumerate(rec['keys']):
    dn=bank[f'{idx}_target{ki}'][loops];prim['targets'][ki]['NORMAL']=gl.append(g,blob,np.c_[dn[:,0],dn[:,2],-dn[:,1]])
   recs.append(dict(object=rec['object'],split_vertices=len(ids),base_normal_max_error=err,targets=len(rec['keys']),source_zero_normal_fallback=int((~valid).sum())))
 g.setdefault('extras',{})['PinoTextureContract']=dict(Human_Pre_Texture_Gate='PENDING',Texture_GO=False,uv='PinoUV_v003',skin='LBS4',normal='Morph normal plus mat3(skinMatrix); pose-dependent correction targets must accompany probe poses',geometry_replacement=False)
 gl.write(p,g,blob);dump('glb-normal-patch.json',recs)
 # Verify the static input really has no skin, morph or animation, and has the
 # exact master positions/UV/material face ownership by stable provenance.
 mapping=np.load(DEST/'pino-c-v004-return-map.npz');audits=[];uvtri=[]
 for path in [p,DEST/'pino-c-v004-tripo-input.glb']:
  gg,bb=gl.read(path);static='tripo-input' in path.name
  if static:assert not gg.get('skins') and not gg.get('animations') and all('targets' not in pr for m in gg['meshes'] for pr in m['primitives'])
  for node in gg['nodes']:
   if 'mesh' not in node:continue
   name=node['name'].removesuffix('_TRIPO_INPUT');i=next(i for i,m in enumerate(meta) if m['object']==name)
   for pr in gg['meshes'][node['mesh']]['primitives']:
    vi=gl.accessor(gg,bb,pr['attributes']['_PINO_VERTEX_ID']).ravel().round().astype(int);ci=gl.accessor(gg,bb,pr['attributes']['_PINO_CORNER_ID']).ravel().round().astype(int)
    xyz=gl.accessor(gg,bb,pr['attributes']['POSITION']);xyz=np.c_[xyz[:,0],-xyz[:,2],xyz[:,1]];uv=gl.accessor(gg,bb,pr['attributes']['TEXCOORD_0']);uv[:,1]=1-uv[:,1]
    err=float(np.linalg.norm(xyz-mapping[f'{i}_position'][vi],axis=1).max());ue=float(np.linalg.norm(uv-mapping[f'{i}_uv'][ci],axis=1).max());assert err<1e-5 and ue<1e-6
    inds=gl.accessor(gg,bb,pr['indices']).ravel().astype(int)
    if static:uvtri.extend(uv[inds].reshape(-1,3,2))
    audits.append(dict(file=path.name,mesh=name,position_max_error=err,uv_max_error=ue))
 sp=importlib.util.spec_from_file_location('uvcheck',ROOT/'scripts/3d/pino-uv-overlap.py');uvc=importlib.util.module_from_spec(sp);sp.loader.exec_module(uvc);overlap,zero=uvc.overlaps(uvtri)
 dump('glb-input-uv-audit.json',dict(records=audits,static_input_no_skin_morph_animation=True,uv_triangles=len(uvtri),positive_area_overlap_pairs=len(overlap),zero_area_uv_triangles=len(zero)))
 # Derive glTF LOCAL bone transforms from exported rest hierarchy and world skin
 # deltas, avoiding assumptions about Blender/imported bone orientation.

 def local(n):
  if 'matrix' in n:return np.array(n['matrix']).reshape(4,4).T
  x,y,z,w=n.get('rotation',[0,0,0,1]);rot=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]]);m=np.eye(4);m[:3,:3]=rot@np.diag(n.get('scale',[1,1,1]));m[:3,3]=n.get('translation',[0,0,0]);return m
 parent={c:i for i,n in enumerate(g['nodes']) for c in n.get('children',[])};world={}
 def W(i):
  if i not in world:world[i]=(W(parent[i]) if i in parent else np.eye(4))@local(g['nodes'][i])
  return world[i]
 for i in range(len(g['nodes'])):W(i)
 C=np.array([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1.]])
 controls=json.loads((OUT/'probe-controls.json').read_text());runtime=[]
 for state in controls:
  target={i:(C@np.array(state['skin_delta'][n['name']])@C.T@world[i] if n.get('name') in state['skin_delta'] else world[i]) for i,n in enumerate(g['nodes'])}
  transforms={}
  for i,n in enumerate(g['nodes']):
   if n.get('name') not in state['skin_delta']:continue
   mat=np.linalg.inv(target[parent[i]])@target[i] if i in parent else target[i];transforms[n['name']]=mat.T.ravel().tolist()
  runtime.append(dict(name=state['name'],local_matrices=transforms,morphs=state['morphs']))
 dump('runtime-controls.json',runtime)
if __name__=='__main__':main()
