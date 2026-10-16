"""Export v004 without remeshing or altering the v003 UV/material contract."""
import bpy,sys,importlib.util,json,hashlib
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sp=importlib.util.spec_from_file_location('v4',ROOT/'scripts/blender/pino-texture-handoff-v004.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)

def digest(a,dtype):return hashlib.sha256(np.asarray(a,dtype=dtype).tobytes()).hexdigest()
def contract(o):
 m=o.data
 return dict(vertices=len(m.vertices),polygons=len(m.polygons),loops=len(m.loops),basis_sha256=digest([p.co[:] for p in m.vertices],'<f4'),corner_vertex_sha256=digest([l.vertex_index for l in m.loops],'<u4'),polygon_sizes_sha256=digest([p.loop_total for p in m.polygons],'<u4'),uv_sha256=digest([u.uv[:] for u in m.uv_layers.active.data],'<f4'),uv_name=m.uv_layers.active.name,materials=[x.name for x in m.materials],material_ownership_sha256=digest([p.material_index for p in m.polygons],'<u4'),normal_sha256=digest([x.vector[:] for x in m.corner_normals],'<f4'))
def main():
 o,r,sc=v.load();v.reset(r);names=[o.name,'PinoSoftLids_L','PinoSoftLids_R','PinoOralLiner'];source={n:contract(bpy.data.objects[n]) for n in names}
 o,r,sc=v.load(True);v.reset(r);meshes=[bpy.data.objects[n] for n in names];audit={};bank={};meta=[];mapping={}
 for i,ob in enumerate(meshes):
  m=ob.data
  for mod in ob.modifiers:
   if mod.type=='NODES':mod.show_viewport=False;mod.show_render=False
  audit[ob.name]={'source_v003':source[ob.name],'v004':contract(ob),'all_rest_contract_fields_equal':source[ob.name]==contract(ob)}
  assert audit[ob.name]['all_rest_contract_fields_equal'],audit[ob.name]
  loops=np.array([l.vertex_index for l in m.loops]);base=np.array([x.vector[:] for x in m.corner_normals]);keys=list(m.shape_keys.key_blocks)[1:]
  bank[f'{i}_vid']=loops;bank[f'{i}_base']=base;meta.append(dict(mesh=m.name,object=ob.name,keys=[k.name for k in keys]))
  for ki,k in enumerate(keys):bank[f'{i}_target{ki}']=np.array([a.vector[:] for a in m.attributes['PinoDN_'+k.name].data])
  mapping[f'{i}_position']=np.array([p.co[:] for p in m.vertices],dtype='<f4');mapping[f'{i}_corner_vertex']=loops.astype('<u4');mapping[f'{i}_uv']=np.array([u.uv[:] for u in m.uv_layers.active.data],dtype='<f4');mapping[f'{i}_polygon_sizes']=np.array([p.loop_total for p in m.polygons],dtype='<u4');mapping[f'{i}_material_id']=np.array([p.material_index for p in m.polygons],dtype='<u4')
 np.savez_compressed(v.TMP/'normal-bank.npz',**bank);(v.TMP/'normal-meta.json').write_text(json.dumps(meta),encoding='utf8')
 np.savez_compressed(v.DEST/'pino-c-v004-return-map.npz',**mapping)
 def export(path,objects,rigged):
  bpy.ops.object.select_all(action='DESELECT')
  for ob in objects:ob.select_set(True)
  bpy.context.view_layer.objects.active=objects[0]
  bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_animations=False,export_apply=False,export_normals=True,export_morph=rigged,export_morph_normal=False,export_skins=rigged,export_all_influences=False,export_attributes=True,export_extras=True,export_materials='EXPORT')
 export(v.DEST/'pino-c-v004-rigged-review.glb',[o,r,*meshes[1:]],True)
 # Explicit neutral mesh copy. Never use a Tripo-generated mesh as rig master.
 copies=[]
 for ob in meshes:
  dup=ob.copy();dup.data=ob.data.copy();dup.name=ob.name+'_TRIPO_INPUT';sc.collection.objects.link(dup);dup.parent=None;dup.matrix_world=ob.matrix_world.copy();dup.shape_key_clear();dup.modifiers.clear();dup.vertex_groups.clear();dup['editing_master']=ob.name;copies.append(dup)
 export(v.DEST/'pino-c-v004-tripo-input.glb',copies,False)
 v.dump('saved-rest-contract.json',audit)
 v.dump('delivery-contract.json',dict(Human_Pre_Texture_Gate='PENDING',Texture_GO=False,source_commit='1dd7980f57419dd3a4ee5fbb4adc9c1dfac207b2',latest_main_authority='73617ce2d3c724c86aed82dfc2a09cd220e5d194',meshes=[dict(index=i,**rec) for i,rec in enumerate(meta)],rig_bones=len(r.data.bones),uv='PinoUV_v003 unchanged',mapping='pino-c-v004-return-map.npz: per mesh position, corner_vertex, uv, polygon_sizes, material_id',note='Tripo input is static. Reproject/bake texture to retained atlas; never replace editing-master geometry/rig.'))
if __name__=='__main__':main()
