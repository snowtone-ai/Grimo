"""Render disposable 3Q/Top views from the saved neutral v008 model."""
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
scene = bpy.context.scene
revision = scene['selected_revision']
directory = ROOT / 'tmp-carol-v008' / f'revision-{revision}'
directory.mkdir(parents=True, exist_ok=True)
original_camera = scene.camera
for name, position, target in [
    ('3q', (-3.0, -3.0, 1.3), (.62, 0, .40)),
    ('top', (.65, 0, 4.0), (.65, 0, .20)),
]:
    data = bpy.data.cameras.new('TEMP '+name)
    camera = bpy.data.objects.new('TEMP '+name, data)
    scene.collection.objects.link(camera)
    camera.location = position
    camera.rotation_euler = (Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    data.type = 'ORTHO'
    data.ortho_scale = 1.52
    scene.camera = camera
    scene.render.filepath = str(directory / f'diagnostic-{name}.png')
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera, do_unlink=True)
scene.camera = original_camera
