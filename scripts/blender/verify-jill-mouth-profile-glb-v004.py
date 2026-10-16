"""Focused fresh-GLB morph checks for the changed mouth; no full motion rerun."""
import bpy,json,ast
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/mouth-profile-v004'
tree=ast.parse((ROOT/'scripts/blender/prove-jill-texture-transfer-v003.py').read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['corners','check']],type_ignores=[]),'<v003 corner proof functions>','exec'),globals())
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/grimo/production/jill/tripo/mouth-profile-v004/jill-rig-mouth-profile-v004.blend'))
r=bpy.data.objects['JILL_RIG'];o=bpy.data.objects['Jill_Body'];r.animation_data.action=None
channels=json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())['authoring_properties'];expected={}
states=[('close-mid','mouth_close','FACE_MouthClose',.5),('closed','mouth_close','FACE_MouthClose',1.),('open','mouth_open','FACE_MouthOpen',1.)]
for name,channel,key,value in states:
    for k in channels:r[k]=value if k==channel else 0.
    r.update_tag();bpy.context.view_layer.update();expected[name]=corners([o])
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(E/'roundtrip/rig-image-only-glb.glb'))
meshes=[x for x in bpy.context.scene.objects if x.type=='MESH' and any(mod.type=='ARMATURE' for mod in x.modifiers)]
rows=[]
for name,channel,key,value in states:
    for ob in meshes:
        for k in ob.data.shape_keys.key_blocks:k.value=value if k.name==key else 0.
        ob.data.update();ob.update_tag()
    bpy.context.view_layer.update();row={'state':name,**check(expected[name],corners(meshes))};rows.append(row);assert row['pass']
(E/'posed-glb-proof.json').write_text(json.dumps({'pass':True,'states':rows,'scope':'Fresh rig GLB changed mouth morphs at close .5/1 and open 1. Does not prove Blender semantic solver or full runtime.'},indent=2)+'\n')
