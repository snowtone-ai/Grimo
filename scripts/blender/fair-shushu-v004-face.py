import bpy,sys,importlib.util,json
from pathlib import Path
import numpy as np
from mathutils import Vector
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('gate',ROOT/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
bpy.ops.wm.open_mainfile(filepath=str(g.ASSET));o=bpy.data.objects['ShushuStatic_Head'];p=np.load(g.OUT/'face-fair-patch.npz')
for k in o.data.shape_keys.key_blocks:k.data.foreach_set('co',p[k.name].ravel())
if o.data.has_custom_normals:
 bpy.context.view_layer.objects.active=o
 bpy.ops.mesh.customdata_custom_splitnormals_clear()
o.data.update()
bpy.context.preferences.filepaths.save_version=0
if '--save' in sys.argv:bpy.ops.wm.save_as_mainfile(filepath=str(g.ASSET))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');scene,cam=g.r.b.setup_review(640,12);cam.data.type='ORTHO';cam.data.ortho_scale=.56
folder=g.OUT/'face-clean-normal-review';folder.mkdir(exist_ok=True)
for name,controls in g.r.STATES.items():
 if name not in ['closed','large']:continue
 g.r.b.state(rig,controls)
 for view,loc in g.r.VIEWS.items():
  cam.location=loc;cam.rotation_euler=(Vector((0,-.02,.69))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
