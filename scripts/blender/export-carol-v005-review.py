"""Reopen frozen A/B, check finite coordinates, export diagnostic GLBs only."""
import bpy,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/carol-v005/ab';OUT.mkdir(parents=True,exist_ok=True)
rows=[]
for key in ['a','b']:
 path=ROOT/f'assets/grimo/production/carol/blender/carol-{key}-v005.blend'
 bpy.ops.wm.open_mainfile(filepath=str(path));bpy.context.view_layer.update()
 bpy.ops.object.select_all(action='DESELECT');meshes=[]
 for o in bpy.context.scene.objects:
  if o.type not in {'MESH','CURVE'} or o.hide_render or any(c.hide_render for c in o.users_collection):continue
  o.select_set(True)
  if o.type=='MESH':
   coords=[o.matrix_world@v.co for v in o.data.vertices]
   meshes.append({'name':o.name,'vertices':len(coords),'finite':all(math.isfinite(x) for v in coords for x in v),
    'min':[min(v[i] for v in coords) for i in range(3)],'max':[max(v[i] for v in coords) for i in range(3)]})
 assert all(x['finite'] for x in meshes)
 bpy.ops.export_scene.gltf(filepath=str(OUT/f'carol-{key}.preview.glb'),use_selection=True,export_animations=False,export_cameras=False,export_lights=False)
 rows.append({'variant':key,'blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'meshes':meshes,'status':'reopened and finite; not topology or visual approval'})
(ROOT/'docs/production/carol/evidence/hero-geometry-v005/saved-artifact-check.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print('Frozen A and B reopened; finite geometry; preview exports complete')
