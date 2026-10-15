"""Render every frame of the bounded proof in three views; never save the rig."""
import bpy
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'docs/production/jill/rig-pretexture-v002'
bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'assets/grimo/production/jill/tripo/rig-pretexture-v002/jill-rig-pretexture-v002.blend'))
s = bpy.context.scene
camera = s.camera
s.render.engine = 'BLENDER_WORKBENCH'
s.render.resolution_x = 320
s.render.resolution_y = 320
s.render.resolution_percentage = 100
s.render.image_settings.file_format = 'JPEG'
s.render.image_settings.quality = 90
s.display.shading.light = 'STUDIO'
s.display.shading.color_type = 'MATERIAL'
s.display.shading.show_shadows = True
s.display.shading.show_cavity = True
s.display.shading.cavity_type = 'BOTH'
s.display.shading.show_object_outline = False
target = Vector((0, 0, .5))
views = {'front': (0, -1, 0), 'side': (1, 0, 0), '3q': (1, -2, .12)}
for name in views:
    (E / '.proof-frames' / name).mkdir(parents=True, exist_ok=True)
for frame in range(1, 306):
    s.frame_set(frame)
    bpy.context.view_layer.update()
    for name, direction in views.items():
        camera.location = target + Vector(direction).normalized() * 5
        camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
        camera.data.type = 'ORTHO'
        camera.data.ortho_scale = 1.16
        s.render.filepath = str(E / '.proof-frames' / name / f'{frame:04d}.jpg')
        bpy.ops.render.render(write_still=True)
    if frame % 24 == 0:
        print('CONTINUOUS_FRAME', frame, flush=True)
print('CONTINUOUS_COMPLETE', 305, flush=True)
