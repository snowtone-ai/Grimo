import bpy,sys,importlib.util,json
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from collections import defaultdict
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2];sp=importlib.util.spec_from_file_location('g',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
bpy.ops.wm.open_mainfile(filepath=str(g.ASSET));o=bpy.data.objects['ShushuStatic_Head'];old=o.data;old.calc_loop_triangles();patch=np.load(g.OUT/'muzzle-retopo.npz');source=np.load(g.OUT/'face-source.npz')
oldweights=[{g.group:g.weight for g in v.groups} for v in old.vertices]
tris=np.array([t.vertices[:] for t in old.loop_triangles]);uvdata=old.uv_layers.active.data;uvflat=np.empty(len(uvdata)*2,dtype=np.float32);uvdata.foreach_get('uv',uvflat);uvflat=uvflat.reshape(-1,2);uvs=np.array([uvflat[list(t.loops)] for t in old.loop_triangles]);trimap={tuple(t.vertices):i for i,t in enumerate(old.loop_triangles)}
np.savez_compressed(g.OUT/'muzzle-source-uv.npz',uvs=uvs,tri=tris)
base=source['Basis'];opened=source['MouthOpen'];bvh=BVHTree.FromPolygons(opened.tolist(),tris.tolist(),all_triangles=True);groupnames=[v.name for v in o.vertex_groups]
crown=np.load(g.OUT/'crown-local-delta.npz')['delta'] if (g.OUT/'crown-local-delta.npz').exists() else np.zeros_like(base)
def weights(point,tri):
 a,b,c=opened[tri];v0=b-a;v1=c-a;v2=point-a;d00=v0@v0;d01=v0@v1;d11=v1@v1;d20=v2@v0;d21=v2@v1;den=d00*d11-d01*d01
 if abs(den)<1e-24:return np.array([1.,0,0])
 v=(d11*d20-d01*d21)/den;w=(d00*d21-d01*d20)/den;return np.array([1-v-w,v,w])
count=len(base);npatch=len(patch['opened']);maps=[];bary=[];newuv=[]
for i,point in enumerate(patch['opened']):
 hit,_,index,_=bvh.find_nearest(Vector(point));t=tris[index];w=weights(np.array(hit),t);maps.append(t);bary.append(w);newuv.append(w@uvs[index])
maps=np.array(maps);bary=np.array(bary);newuv=np.array(newuv);nb=len(patch['boundary_ids']);outer=int(patch['outer_count'])
if (g.OUT/'muzzle-atlas.npz').exists():newuv=np.load(g.OUT/'muzzle-atlas.npz')['uv']
print('RETOPO projection ready',flush=True)
# Existing outside vertices remain referenced, with the patch's outer boundary
# sharing those exact vertex indices. W boundary is retained as exact coordinates.
mapping=np.arange(npatch)+count;mapping[:outer]=patch['boundary_ids'][:outer]
faces=patch['retained'].tolist();patchfaces=mapping[patch['patch_tri']]
# Orient toward the front (-Y).
for t in patchfaces:
 pp=np.vstack([base,patch['closed']])[t]
 if np.cross(pp[1]-pp[0],pp[2]-pp[0])[1]>0:t[[1,2]]=t[[2,1]]
faces+=patchfaces.tolist();mesh=bpy.data.meshes.new(old.name+'_LocalMuzzle');mesh.from_pydata(np.vstack([base+crown,patch['closed']]),[],faces);mesh.update();o.data=mesh
o.vertex_groups.clear()
for name in groupnames:o.vertex_groups.new(name=name)
for m in old.materials:mesh.materials.append(m)
if (g.OUT/'Head-mouth-gate-retopo.png').exists():
 im=bpy.data.images.load(str(g.OUT/'Head-mouth-gate-retopo.png'),check_existing=False);im.pack()
 next(n for m in mesh.materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE').image=im
uv=mesh.uv_layers.new(name=old.uv_layers.active.name)
print('RETOPO mesh ready',flush=True)
textures=[uvs[trimap[tuple(t)]] for t in patch['retained']]
for pt,ft in zip(patch['patch_tri'],patchfaces):
 tex=newuv[pt]
 if tuple(mapping[pt])!=tuple(ft):tex=tex[[0,2,1]]
 textures.append(tex)
uv.data.foreach_set('uv',np.array(textures,dtype=np.float32).ravel());mesh.polygons.foreach_set('use_smooth',np.ones(len(faces),dtype=bool))
drivers=[]
print('RETOPO UV ready',flush=True)
for fc in old.shape_keys.animation_data.drivers:
 drivers.append((fc.data_path,fc.driver.expression,[(v.name,v.type,[(t.id,t.data_path) for t in v.targets]) for v in fc.driver.variables]))
for name in source.files:
 if name=='tri':continue
 q=source[name]
 if name=='Basis':a=patch['closed']
 elif name=='MouthOpen':a=patch['opened']
 else:a=patch['closed']+np.sum((q-base)[maps]*bary[:,:,None],axis=1)
 # Outer coordinates stay exact in every key; boundary duplicates also match.
 a[:nb]=q[patch['boundary_ids']]
 key=o.shape_key_add(name=name);key.data.foreach_set('co',np.vstack([q+crown,a]).astype(np.float32).ravel())
for path,expression,variables in drivers:
 fc=mesh.shape_keys.driver_add(path);fc.driver.expression=expression
 for name,typ,targets in variables:
  v=fc.driver.variables.new();v.name=name;v.type=typ
  for target,(ident,dp) in zip(v.targets,targets):target.id=ident;target.data_path=dp
print('RETOPO keys ready',flush=True)
assignments=defaultdict(list)
for i,ws in enumerate(oldweights):
 for group,w in ws.items():assignments[group,w].append(i)
for i in range(npatch):
 if i<outer:ws=oldweights[int(patch['boundary_ids'][i])]
 else:
  ws={}
  for idx,w in zip(maps[i],bary[i]):
   for group,weight in oldweights[idx].items():ws[group]=ws.get(group,0)+w*weight
 for group,w in ws.items():
  if w>1e-8:assignments[group,float(w)].append(count+i)
for (group,w),indices in assignments.items():o.vertex_groups[group].add(indices,w,'REPLACE')
mesh.update()
print('RETOPO weights ready',flush=True)
if '--save' in sys.argv:
 target=g.ASSET.with_name('shushu-v004-motion-gate-v002.blend')
 bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(target))
 if '--save-only' in sys.argv:sys.exit(0)
rig=next(x for x in bpy.data.objects if x.type=='ARMATURE');scene,cam=g.r.b.setup_review(640,16);cam.data.type='ORTHO';cam.data.ortho_scale=.56
folder=g.OUT/('tangent-review' if '--quick' in sys.argv else 'final-surface-review');folder.mkdir(exist_ok=True)
for name,controls in g.r.STATES.items():
 if '--quick' in sys.argv and name not in ['closed','large']:continue
 g.r.b.state(rig,controls)
 for view,loc in g.r.VIEWS.items():
  if '--quick' in sys.argv and view!='front':continue
  cam.location=loc;cam.rotation_euler=(Vector((0,-.02,.69))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
