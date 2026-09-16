"""Freeze A and inspect the exact historical binary before any B deformation."""
import bpy, json, hashlib, os
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'assets/grimo/production/carol/blender'
OUT=ROOT/'docs/production/carol/evidence/hero-geometry-v005'
REVIEW=ROOT/'artifacts/carol-v005/ab'; REVIEW.mkdir(parents=True,exist_ok=True)
frozen=DEST/'carol-a-v005.blend'
bpy.ops.wm.open_mainfile(filepath=str(frozen if frozen.exists() else ROOT/'artifacts/carol-v005/parts.blend'))
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene['status']='Carol A: frozen exploratory sculpt, not approved; user requested alternative B'
if not frozen.exists():bpy.ops.wm.save_as_mainfile(filepath=str(frozen))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
    if o.type in {'MESH','CURVE'} and not any(c.hide_render for c in o.users_collection):o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(REVIEW/'carol-a.preview.glb'),use_selection=True,export_animations=False,export_cameras=False,export_lights=False)
src=ROOT/'assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(src))
bpy.context.view_layer.update()
items=[]
for o in bpy.context.scene.objects:
    if o.type!='MESH':continue
    if o.data.shape_keys:
        for k in o.data.shape_keys.key_blocks:k.value=0
    coords=[o.matrix_world@v.co for v in o.data.vertices]
    items.append({'name':o.name,'vertices':len(coords),'min':[min(v[i] for v in coords) for i in range(3)],'max':[max(v[i] for v in coords) for i in range(3)],'materials':[m.name for m in o.data.materials],'uv':len(o.data.uv_layers),'morphs':list(o.data.shape_keys.key_blocks.keys()) if o.data.shape_keys else []})
report={'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'objects':items}
(OUT/'historical-b-source-inspection.json').write_text(json.dumps(report,indent=2),encoding='utf8')
bpy.ops.wm.save_as_mainfile(filepath=str(REVIEW/'historical-import.blend'))
print(json.dumps(report,indent=2))
