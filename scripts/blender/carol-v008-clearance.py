"""Disposable geometry clearance probes, not poses, rigging or animation.

blender -b assets/grimo/production/carol/blender/carol-v008.blend \
  --python scripts/blender/carol-v008-clearance.py
Renders both locked cameras, restores exact matrices, and never saves a blend.
Interpret the images: contact counts alone cannot approve motion or geometry.
"""
import hashlib
import json
import math
import runpy
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
BUILD = runpy.run_path(str(ROOT/'scripts/blender/build-carol-v008.py'))
OUTPUT = ROOT/'tmp-carol-v008/clearance-selected'
CASES = [
    ('head-yaw-minus','head','Z',-8), ('head-yaw-plus','head','Z',8),
    ('head-pitch-minus','head','Y',-6), ('head-pitch-plus','head','Y',6),
    ('head-roll-minus','head','X',-5), ('head-roll-plus','head','X',5),
    ('ear-sweep-minus','ear','Z',-8), ('ear-sweep-plus','ear','Z',8),
]


def main():
    scene = bpy.context.scene
    assert scene.get('saved_pose') == 'NEUTRAL'
    assert not any(o.type == 'ARMATURE' or o.animation_data for o in scene.objects)
    asset_hash = hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()
    neutral = BUILD['geometry_digest']()
    measurements = json.loads((ROOT/'tmp-carol-v008/revision-9/measurements.json').read_text())
    assert neutral == measurements['geometry_digest']
    OUTPUT.mkdir(parents=True,exist_ok=True)
    head = [o for o in scene.objects if o.name == 'HEAD_CAGE' or
            o.name.startswith(('EYE_','EYELID_','IRIS_','GLINT_','EAR_')) or
            o.name in {'NOSE','MOUTH_closed','PHILTRUM'}]
    original = {o.name:o.matrix_world.copy() for o in head}
    # Restoring matrix_world decomposes matrices and can round Euler/scale
    # channels. Restore their original values for bit-identical neutral geometry.
    channels = {o.name:(o.location.copy(),o.rotation_euler.copy(),o.scale.copy()) for o in head}
    assert all(o.rotation_mode == 'XYZ' for o in head)

    def restore():
        for obj in head:
            obj.location,obj.rotation_euler,obj.scale = channels[obj.name]
        bpy.context.view_layer.update()

    old_camera,old_path = scene.camera,scene.render.filepath
    results = []
    try:
        for name,part,axis,degrees in CASES:
            targets = head if part == 'head' else [bpy.data.objects['EAR_R']]
            pivot_name = 'DEBUG_HEAD_PIVOT' if part == 'head' else 'DEBUG_EAR_ROOT_R'
            pivot = Vector(bpy.data.objects[pivot_name].location)
            transform = (Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(degrees),4,axis)
                         @ Matrix.Translation(-pivot))
            for obj in targets:
                obj.matrix_world = transform@original[obj.name]
            bpy.context.view_layer.update()
            posed = BUILD['geometry_digest']()
            assert posed != neutral
            views = {}
            for view in ['front','side']:
                scene.camera = bpy.data.objects['CAM '+view]
                views[view] = BUILD['geometry_digest']()
                assert views[view] == posed
                scene.render.filepath = str(OUTPUT/(name+'-'+view+'.png'))
                bpy.ops.render.render(write_still=True)
            restore()
            assert BUILD['geometry_digest']() == neutral, 'Exact neutral restoration failed'
            results.append(dict(name=name,part=part,axis=axis,degrees=degrees,
                                pivot=list(pivot),objects=[o.name for o in targets],
                                view_geometry_digests=views,neutral_restored=True))
    finally:
        restore()
        scene.camera,scene.render.filepath = old_camera,old_path
        bpy.context.view_layer.update()
    assert BUILD['geometry_digest']() == neutral
    assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == asset_hash
    report = dict(neutral_geometry_digest=neutral,selected_revision=9,
                  method='Rigid disposable head assembly and independent right-ear root rotations; no skinning.',
                  diagnostic_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  head_pivot_scope='Head, face and both ears; torso/socket/support/tail stay neutral.',
                  cases=results,exact_neutral_restored=True,asset_file_unchanged=True,
                  production_poses_saved=False,automatic_motion_pass=False,
                  interpretation='Read the four clearance image sheets and README visual findings. No Human PASS.')
    (OUTPUT/'motion-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
    print('CLEARANCE_PROBES_COMPLETE; exact neutral restored; asset unchanged')


if __name__ == '__main__':
    main()
