"""Apply the same isolated donor-UV repair to the existing saved proof.

Avoid repeating geometry/motion generation when only the UV gutter changes.
"""
import bpy,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-v002';E=ROOT/'docs/production/jill/rig-pretexture-v002'
bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-pretexture-v002.blend'))
s=bpy.context.scene;b=bpy.data.objects['Jill_Body'];r=bpy.data.objects['JILL_RIG'];mesh=b.data;uv=mesh.uv_layers[0];mesh.calc_loop_triangles();repairs=[]
for t in mesh.loop_triangles:
 q=np.array([tuple(uv.data[li].uv) for li in t.loops]);a=q[1]-q[0];d=q[2]-q[0]
 if abs(a[0]*d[1]-a[1]*d[0])<2e-12:
  x=.894;y=.935+.009*len(repairs)
  for li,p in zip(t.loops,[(x,y),(x+.006,y),(x+.003,y+.006)]):uv.data[li].uv=p
  repairs.append({'polygon':t.polygon_index,'loops':list(t.loops),'original_active_uv':q.tolist(),'replacement_bounds':[x,y,.006,.006]})
b['basis_contract']='All 28050 inherited Basis vertices exact. Local deep oral faces removed; physical lid/lip/cavity/tongue additions. Delivered version uses no exterior boundary fairing.'
bpy.context.preferences.filepaths.save_version=0;s.frame_set(13);bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(A/'jill-rig-pretexture-v002.blend'))
for o in s.objects:o.select_set(o.type not in ['CAMERA','LIGHT'] and not o.name.startswith('CTRL_'))
bpy.context.view_layer.objects.active=r
bpy.ops.export_scene.gltf(filepath=str(A/'jill-rig-pretexture-v002.glb'),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_force_sampling=True,export_frame_range=True,export_frame_step=1,export_bake_animation=True,export_skins=True,export_def_bones=False,export_morph=True,export_morph_animation=True,export_all_influences=False,export_influence_nb=4,export_extras=True,export_cameras=False,export_lights=False)
report=json.loads((E/'repair-report.json').read_text());report['local_uv_repairs']=repairs;(E/'repair-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
data=np.load(E/'surface-contract.npz');saved={k:data[k] for k in data.files};saved['uv']=np.array([tuple(x.uv) for x in uv.data]);np.savez_compressed(E/'surface-contract.npz',**saved)
print('UV_LOCAL_REPAIR',len(repairs))
