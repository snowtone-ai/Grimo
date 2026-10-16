"""Validate saved GLB from its own embedded attributes and morph normals."""
import bpy,sys,json,importlib.util
from pathlib import Path
import numpy as np
from mathutils import Matrix
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sp=importlib.util.spec_from_file_location('v4',ROOT/'scripts/blender/pino-texture-handoff-v004.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
sp=importlib.util.spec_from_file_location('gl',ROOT/'scripts/3d/package-pino-texture-ready-v003.py');gl=importlib.util.module_from_spec(sp);sp.loader.exec_module(gl)
def main():
 o,r,sc=v.load(True);expected=np.load(v.TMP/'expected.npz');mapping=np.load(v.DEST/'pino-c-v004-return-map.npz');states=json.loads((v.OUT/'probe-controls.json').read_text());names=[o.name,'PinoSoftLids_L','PinoSoftLids_R','PinoOralLiner']
 for ob in list(sc.objects):
  if ob.type in ['MESH','ARMATURE']:bpy.data.objects.remove(ob,do_unlink=True)
 path=v.DEST/'pino-c-v004-rigged-review.glb';g,blob=gl.read(path);bpy.ops.import_scene.gltf(filepath=str(path));r=next(x for x in sc.objects if x.type=='ARMATURE');objects={n:bpy.data.objects[n] for n in names}
 for name,ob in objects.items():
  node=next(n for n in g['nodes'] if n.get('name')==name);mesh=g['meshes'][node['mesh']];keys=mesh['extras']['targetNames'];size=max(int(gl.accessor(g,blob,p['attributes']['_PINO_CORNER_ID']).max()) for p in mesh['primitives'])+1
  base=np.zeros((size,3));bank={k:np.zeros((size,3)) for k in keys}
  for p in mesh['primitives']:
   ids=gl.accessor(g,blob,p['attributes']['_PINO_CORNER_ID']).ravel().round().astype(int)
   def convert(a):return np.c_[a[:,0],-a[:,2],a[:,1]]
   base[ids]=convert(gl.accessor(g,blob,p['attributes']['NORMAL']))
   for k,t in zip(keys,p['targets']):bank[k][ids]=convert(gl.accessor(g,blob,t['NORMAL']))
  ids=np.array([a.value for a in ob.data.attributes['_PINO_CORNER_ID'].data]).round().astype(int);loops=ids[np.array([l.vertex_index for l in ob.data.loops])]
  v.v3.normal_controller(ob,base[loops],{k:a[loops] for k,a in bank.items()})
 rows=[]
 for state in states:
  v.reset(r)
  for p in sorted(r.pose.bones,key=lambda p:len(p.parent_recursive)):
   p.matrix=r.matrix_world.inverted()@Matrix(state['skin_delta'][p.name])@r.matrix_world@p.bone.matrix_local;bpy.context.view_layer.update()
  for name,values in state['morphs'].items():
   for k,w in values.items():objects[name].data.shape_keys.key_blocks[k].value=w
  bpy.context.view_layer.update();v.refresh_preview_normals(objects[names[0]],r)
  for i,(name,ob) in enumerate(objects.items()):
   ids=np.array([a.value for a in ob.data.attributes['_PINO_VERTEX_ID'].data]).round().astype(int);cornerids=np.array([a.value for a in ob.data.attributes['_PINO_CORNER_ID'].data]).round().astype(int);loops=cornerids[np.array([l.vertex_index for l in ob.data.loops])]
   P=v.evaluated(ob);ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());N=np.array([n.vector[:] for n in ev.data.corner_normals]);EN=expected[f'{state["name"]}_{i}_normal'][loops];valid=np.linalg.norm(EN,axis=1)>.5
   rows.append(dict(state=state['name'],object=name,max_position_error=float(np.linalg.norm(P-expected[f'{state["name"]}_{i}_position'][ids],axis=1).max()),max_normal_error=float(np.linalg.norm(N[valid]-EN[valid],axis=1).max(initial=0)),max_uv_error=float(np.linalg.norm(np.array([u.uv[:] for u in ob.data.uv_layers.active.data])-mapping[f'{i}_uv'][loops],axis=1).max())))
  if state['name'] in ['neutral','contact','rest','wink']:
   v.render(sc,'reimport-'+state['name'])
 v.dump('reimport-audit.json',dict(note='Uses GLB-embedded normals and stable IDs. Native Blender glTF import alone does not bind NORMAL morphs. refresh_preview_normals is required after pose edits in Blender.',comparisons=rows))
if __name__=='__main__':main()
