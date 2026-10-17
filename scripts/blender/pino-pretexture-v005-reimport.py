"""Focused saved Blender/GLB audit; geometry/motion payload is byte-protected."""
import bpy,sys,json,importlib.util,hashlib
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('proof',ROOT/'scripts/blender/pino-pretexture-v005.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
d=p.module('delivery','scripts/3d/pino-pretexture-v005-delivery.py');gl=d.gl
def main():
 refs={}
 for label,path in [('v004',p.SRC),('v005',p.DEST/'pino-c-pretexture-v005.blend')]:
  bpy.ops.wm.open_mainfile(filepath=str(path));sc=bpy.context.scene
  p.v.v3.f.display(sc,400)
  for view in ['front','side','3q']:
   p.v.v3.f.view(sc,view,target=(0,-.015,.47),scale=1.32);f=p.TMP/f'protected-{label}-{view}.png';sc.render.filepath=str(f);bpy.ops.render.render(write_still=True)
 mapping=np.load(p.DEST/'pino-c-v005-return-map.npz');records=[]
 for kind in ['tripo-input','rigged-review']:
  bpy.ops.wm.read_factory_settings(use_empty=True)
  path=p.DEST/f'pino-c-v005-{kind}.glb';bpy.ops.import_scene.gltf(filepath=str(path))
  helpers={pb.custom_shape for arm in bpy.context.scene.objects if arm.type=='ARMATURE' for pb in arm.pose.bones if pb.custom_shape}
  objects=[x for x in bpy.context.scene.objects if x.type=='MESH' and x not in helpers];assert len(objects)==4
  for ob in objects:
   name=ob.name.removesuffix('_TRIPO_INPUT');i=p.NAMES.index(name);m=ob.data
   ids=np.array([x.value for x in m.attributes['_PINO_VERTEX_ID'].data]).round().astype(int);cid=np.array([x.value for x in m.attributes['_PINO_CORNER_ID'].data]).round().astype(int);loops=np.array([x.vertex_index for x in m.loops]);corners=cid[loops]
   pos=np.array([x.co[:] for x in m.vertices]);uv=np.array([x.uv[:] for x in m.uv_layers.active.data]);pe=float(np.linalg.norm(pos-mapping[f'{i}_position'][ids],axis=1).max());ue=float(np.linalg.norm(uv-mapping[f'{i}_uv'][corners],axis=1).max())
   assert pe<1e-5 and ue<1e-6
   row=dict(file=path.name,object=name,max_position_error_m=pe,max_uv_error=ue,vertices=len(m.vertices),shape_keys=len(m.shape_keys.key_blocks)-1 if m.shape_keys else 0)
   # Import can split vertices; verify face ownership against actual corner map.
   sizes=mapping[f'{i}_polygon_sizes'];starts=np.r_[0,np.cumsum(sizes)];faceindex=np.searchsorted(starts,corners,side='right')-1
   loopmat=np.array([poly.material_index for poly in m.polygons for _ in poly.loop_indices]);actual=[m.materials[int(k)].name for k in loopmat]
   # Master material index -> stable slot name (v005 slots unchanged).
   mats=json.loads((p.OUT/'master-preservation.json').read_text())['fields'][name]['slots'];expected=[mats[int(mapping[f'{i}_material_id'][f])] for f in faceindex]
   assert actual==expected;row['material_face_ownership_exact']=True;records.append(row)
  assert (sum(x.type=='ARMATURE' for x in bpy.context.scene.objects)==(1 if kind=='rigged-review' else 0))
 p.dump('saved-reimport.json',dict(records=records,note='Focused neutral and UV/material reimport. v004 POSITION/NORMAL/morph/skin bytes unchanged; no duplicate full-motion/runtime claim. Blender import alone still needs v004 morph-normal bridge.'))
if __name__=='__main__':main()
