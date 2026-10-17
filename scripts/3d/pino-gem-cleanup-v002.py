"""UV-authored oral repaint plus isolated donor-liner depth repair; no Master return."""
from pathlib import Path
import sys,json,importlib.util,io,hashlib,copy
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/pino/evidence/tripo-gem-cleanup-v002'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v002'
DONOR=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v001/pino-c-v005-tripo-donor-original.glb'
def module(n,path):
 s=importlib.util.spec_from_file_location(n,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
gl=module('gl','scripts/3d/package-pino-texture-ready-v003.py')
atlas=module('atlas','scripts/3d/pino-pretexture-v005-atlas.py')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,d):(OUT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def colors(p):
 # Spatial tissue colour, evaluated at every UV triangle sample. No decal copy.
 x,y,z=p.T
 tongue=(1-smooth(.577,.598,z))*(1-smooth(-.412,-.391,y))
 oral=np.tile([112.,34.,37.],(len(p),1))
 front=1-smooth(-.414,-.391,y)
 oral=oral*(1-front[:,None])+np.array([174.,55.,50.])*front[:,None]
 pink=np.tile([238.,124.,119.],(len(p),1))
 pink+= np.exp(-(x/.027)**2-((z-.568)/.019)**2)[:,None]*np.array([5.,8.,7.])
 return np.uint8(np.clip(np.round(oral*(1-tongue[:,None])+pink*tongue[:,None]),0,255))
def paint(p,ids,uv,size=2048):
 rgb=np.zeros((size,size,3),np.uint8);rgb[:]=[101,33,34];covered=np.zeros((size,size),bool)
 bary=np.array([[1,0,0],[0,1,0],[0,0,1],[.5,.5,0],[0,.5,.5],[.5,0,.5],[1/3,1/3,1/3]])
 for tri in ids:
  q=uv[tri];xyz=p[tri];xx,yy,bc=atlas.raster(q,size)
  support=np.clip(np.floor((bary@q)*size).astype(int),0,size-1);sx,sy=support.T;missing=~covered[sy,sx]
  rgb[sy[missing],sx[missing]]=colors(bary@xyz)[missing];covered[sy[missing],sx[missing]]=True
  rgb[yy,xx]=colors(bc@xyz);covered[yy,xx]=True
 # Guard UV sampling and mip borders using only oral tissue colours.
 known=covered.copy()
 for step in range(8):
  new=known.copy()
  for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
   h,w=known.shape;a=(slice(max(0,dy),min(h,h+dy)),slice(max(0,dx),min(w,w+dx)));b=(slice(max(0,-dy),min(h,h-dy)),slice(max(0,-dx),min(w,w-dx)))
   fill=(~new[a])&known[b];rgb[a][fill]=rgb[b][fill];new[a]|=fill
  known=new
 return rgb[::-1],int(covered.sum())
def image_bytes(g,b,index):
 v=g['bufferViews'][g['images'][index]['bufferView']];return bytes(b[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']])
def build():
 g,b=gl.read(DONOR);original=copy.deepcopy(g);old=bytes(b)
 node=next(n for n in g['nodes'] if n.get('name')=='PinoOralLiner_TRIPO_INPUT');pr=g['meshes'][node['mesh']]['primitives'][0]
 assert g['materials'][pr['material']]['name']=='Pino_OralInterior'
 pi=pr['attributes']['POSITION'];ni=pr['attributes']['NORMAL'];raw=gl.accessor(g,b,pi);p=np.c_[raw[:,0],-raw[:,2],raw[:,1]]
 ids=gl.accessor(g,b,pr['indices']).astype(int).reshape(-1,3);uv=gl.accessor(g,b,pr['attributes']['TEXCOORD_0'])
 rgb,coverage=paint(p,ids,uv);img=Image.fromarray(rgb);img.save(DEST/'pino-oral-basecolor-v002.png')
 png=io.BytesIO();img.save(png,format='PNG');data=png.getvalue()
 # Append replacement image; retain all original bytes and untouched image encodings.
 while len(b)%4:b.append(0)
 vi=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':len(b),'byteLength':len(data)});b.extend(data)
 tex=g['materials'][pr['material']]['pbrMetallicRoughness']['baseColorTexture']['index'];im=g['textures'][tex]['source']
 assert im==2
 g['images'][im]={'name':'Pino oral locally repainted v002','bufferView':vi,'mimeType':'image/png'}
 diagnostic=ROOT/'artifacts/pino-gem-cleanup-v002';diagnostic.mkdir(parents=True,exist_ok=True)
 gl.write(diagnostic/'pino-c-v005-oral-texture-only-v002.glb',g,b)
 contact=np.load(OUT/'oral-contact.npz');cp=contact['positions'];hit=contact['front_hits']
 lookup={tuple(np.round(v,7)):r[1] for v,r in zip(cp,contact['repaired_positions'])}
 repaired=p.copy()
 # Only donor liner vertices at or in front of the main tongue/exterior contact.
 clearance=.001
 repaired[:,1]=np.array([lookup[tuple(np.round(v,7))] for v in p])
 changed=np.linalg.norm(repaired-p,axis=1)>1e-9
 newraw=np.c_[repaired[:,0],repaired[:,2],-repaired[:,1]].astype('<f4')
 # Write only the original oral POSITION range (no index/UV/order change).
 a=g['accessors'][pi];v=g['bufferViews'][a['bufferView']];off=v.get('byteOffset',0)+a.get('byteOffset',0)
 assert v.get('byteStride',12)==12 and a['componentType']==5126
 b[off:off+newraw.nbytes]=newraw.tobytes();a['min']=newraw.min(0).tolist();a['max']=newraw.max(0).tolist()
 # Recompute normals solely for this altered oral surface, smoothing coincident UV splits.
 t=newraw[ids];fn=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);unique,inv=np.unique(newraw,axis=0,return_inverse=True);acc=np.zeros_like(unique)
 for corner in range(3):np.add.at(acc,inv[ids[:,corner]],fn)
 nn=acc[inv];length=np.linalg.norm(nn,axis=1);valid=length>1e-12;nn[valid]/=length[valid,None]
 prior=gl.accessor(g,b,ni);nn[~valid]=prior[~valid]
 a=g['accessors'][ni];v=g['bufferViews'][a['bufferView']];noff=v.get('byteOffset',0)+a.get('byteOffset',0);assert v.get('byteStride',12)==12
 b[noff:noff+nn.nbytes]=nn.astype('<f4').tobytes()
 final=DEST/'pino-c-v005-tripo-gem-cleaned-v002.glb';gl.write(final,g,b)
 fg,fb=gl.read(final);checks=[]
 for i,a in enumerate(original['accessors']):
  checks.append({'accessor':i,'equal':bool(np.array_equal(gl.accessor(original,old,i),gl.accessor(fg,fb,i))),'allowed_oral_change':i in [pi,ni]})
 assert all(c['equal'] or c['allowed_oral_change'] for c in checks)
 assert all(image_bytes(original,old,i)==image_bytes(fg,fb,i) for i in [0,1,3])
 assert np.array_equal(newraw[:,[0,1]],raw[:,[0,1]])
 assert np.all(rgb[:,:,0]>rgb[:,:,2]) and np.all(rgb[:,:,0]>rgb[:,:,1])
 write('repair-audit.json',{'donor_sha256':sha(DONOR.read_bytes()),'candidate_sha256':sha(final.read_bytes()),'oral_png_sha256':sha(data),'image_size':list(img.size),'uv_covered_texels':coverage,'oral_vertices':len(p),'oral_triangles':len(ids),'oral_depth_changed_vertices':int(changed.sum()),'max_oral_depth_change':float(np.max(repaired[:,1]-p[:,1])),'clearance_target':clearance,'oral_x_z_exact':True,'mesh_deleted':False,'uv_indices_other_accessors_exact':all(c['equal'] for c in checks if not c['allowed_oral_change']),'accessors':checks,'other_embedded_images_byte_exact':True,'all_png_pixels_red_dominant_no_blue_purple':True,'master_applied':False,'image_return':'separate stage; existing v005 ownership/position HOLD remains'})
 print('SAVED',final)
if __name__=='__main__':build()
