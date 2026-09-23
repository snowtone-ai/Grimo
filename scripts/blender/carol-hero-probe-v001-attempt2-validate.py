"""Targeted saved-blend checks for the Carol donor reuse experiment."""
import bpy

scene = bpy.context.scene
fleece = bpy.data.objects['DONOR Carol_Fleece_Continuous']
assert fleece.type == 'MESH' and len(fleece.data.vertices) == 164272
assert not any(o.name.startswith('PROXY ') for o in scene.objects)
assert all(bpy.data.objects[name].parent == bpy.data.objects['PROBE head base owner']
           for name in ('EYE_L','EYE_R','EAR_L','DONOR Carol_Moon_Attached',
                        'DONOR Carol_Star_CrownStar','DONOR Carol_Star_TopStar'))
assert bpy.data.objects['EAR_R'].parent == bpy.data.objects['PROBE near ear secondary']
assert all(name in fleece.data.shape_keys.key_blocks for name in
           ('DONOR local cheek ACK','DONOR head-owned lean','DONOR upper-body delay'))
assert scene.frame_start == 1 and scene.frame_end == 120
assert scene.camera.name == 'CAM front'
hooves = [o for o in scene.objects if o.name.startswith('HOOF_')]
assert len(hooves) == 4
scene.frame_set(1)
base = [[list(row) for row in o.matrix_world] for o in hooves]
scene.frame_set(45)
peak = [[list(row) for row in o.matrix_world] for o in hooves]
assert base == peak, 'Hoof world transform changed during contact motion'
assert fleece.data.shape_keys.key_blocks['DONOR head-owned lean'].value > .99
assert bpy.data.objects['PROBE head base owner'].animation_data is not None
print('ATTEMPT2_BLEND_VALIDATION_PASS')
