"""Disposable rejection probes. Never saves a rig, pose, shape key or .blend.

blender -b assets/grimo/production/carol/blender/carol-v008.blend \
  --python scripts/blender/carol-v008-clearance.py
"""
import hashlib
import json
import math
import runpy
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
BUILD = runpy.run_path(str(ROOT/'scripts/blender/build-carol-v008.py'))
OUTPUT = ROOT/'tmp-carol-v008/clearance-selected'
CASES = [
    ('head-yaw-minus','head','Z',-8), ('head-yaw-plus','head','Z',8),
    ('head-pitch-minus','head','Y',-6), ('head-pitch-plus','head','Y',6),
    ('head-roll-minus','head','X',-5), ('head-roll-plus','head','X',5),
    ('ear-sweep-minus','ear','Z',-8), ('ear-sweep-plus','ear','Z',8),
    ('gaze-horizontal-minus','gaze','U',-.14), ('gaze-horizontal-plus','gaze','U',.14),
    ('gaze-vertical-minus','gaze','V',-.12), ('gaze-vertical-plus','gaze','V',.12),
    ('blink-closed','blink',None,1),
    ('support-shift-minus','support','X',-.010), ('support-shift-plus','support','X',.010),
]


def main():
    scene = bpy.context.scene
    revision = scene['selected_revision']
    assert scene.get('saved_pose') == 'NEUTRAL'
    assert not any(o.type == 'ARMATURE' or o.animation_data for o in scene.objects)
    assert len(bpy.data.actions)==0
    asset_hash = hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()
    neutral = BUILD['geometry_digest']()
    measurements = json.loads((ROOT/f'tmp-carol-v008/revision-{revision}/measurements.json').read_text())
    assert neutral == measurements['geometry_digest']
    OUTPUT.mkdir(parents=True,exist_ok=True)
    objects = [o for o in scene.objects if o.type in {'MESH','CURVE'}]
    head = [o for o in objects if o.name == 'HEAD_CAGE' or
            o.name.startswith(('EYE_','EYELID_','EAR_')) or
            o.name in {'NOSE','MOUTH_closed','PHILTRUM'}]
    original = {o.name:o.matrix_world.copy() for o in objects}
    channels = {o.name:(o.location.copy(),o.rotation_euler.copy(),o.scale.copy()) for o in objects}
    vertices = {o.name:[v.co.copy() for v in o.data.vertices] for o in objects if o.type=='MESH'}
    eye_image=bpy.data.images['EYE pigment diagnostic packed']
    pixels=np.array(eye_image.pixels[:],dtype=np.float32)
    pigment_hash=hashlib.sha256(pixels.tobytes()).hexdigest()
    sample=BUILD['facial_surface'](bpy.data.objects['HEAD_CAGE'])
    hoof_names=[o.name for o in objects if o.name.startswith('HOOF_')]
    depsgraph=bpy.context.evaluated_depsgraph_get()
    def ground():
        return {name:min((o.matrix_world@v.co).z for v in o.data.vertices)
                for name in hoof_names
                for o in [bpy.data.objects[name].evaluated_get(depsgraph)]}
    neutral_ground=ground()

    def restore():
        for obj in objects:
            obj.location,obj.rotation_euler,obj.scale = channels[obj.name]
            if obj.type=='MESH':
                for v,co in zip(obj.data.vertices,vertices[obj.name]): v.co=co
                obj.data.update()
        eye_image.pixels.foreach_set(pixels)
        eye_image.update()
        bpy.context.view_layer.update()

    old_camera,old_path = scene.camera,scene.render.filepath
    results = []
    try:
        for name,part,axis,value in CASES:
            targets=[]
            details={}
            if part in {'head','ear'}:
                targets=head if part=='head' else [bpy.data.objects['EAR_R']]
                pivot=Vector(bpy.data.objects['DEBUG_HEAD_PIVOT' if part=='head' else 'DEBUG_EAR_ROOT_R'].location)
                transform=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(value),4,axis)@Matrix.Translation(-pivot)
                for obj in targets: obj.matrix_world=transform@original[obj.name]
                details=dict(degrees=value,pivot=list(pivot))
            elif part=='gaze':
                offset=(value,0) if axis=='U' else (0,value)
                eye_image.pixels.foreach_set(BUILD['eye_pixels'](offset).ravel())
                eye_image.update()
                targets=[bpy.data.objects['EYE_L'],bpy.data.objects['EYE_R']]
                details=dict(iris_UV_offset=offset,aperture_unchanged=True,
                             limitation='Bilateral shared pigment tests attention range, not convergent target tracking.')
            elif part=='blink':
                targets=[o for o in objects if o.name.startswith(('EYE_','EYELID_'))]
                for obj in targets:
                    for vert,co in zip(obj.data.vertices,vertices[obj.name]):
                        u=(abs(co.y)-.162)/.0685
                        v=(co.z-.418)/.0745
                        z=.418+.001*v-.008*max(0,1-u*u)
                        vert.co=sample(co.y,z,.0015 if obj.name.startswith('EYE_') else .002)
                    obj.data.update()
                details=dict(method='Compress conformal aperture to a shallow curved closed line; underlying skull remains present.',
                             limitation='Closed endpoint only; eyelid tissue travel and intermediate blink are not validated.')
            elif part=='support':
                targets=[o for o in objects if not o.name.startswith(('HOOF_','FORE_','HIND_'))]
                transform=Matrix.Translation((value,0,-.004))
                for obj in targets: obj.matrix_world=transform@original[obj.name]
                for obj in objects:
                    if obj.name.startswith(('FORE_','HIND_')):
                        targets.append(obj)
                        for vert,co in zip(obj.data.vertices,vertices[obj.name]):
                            w=max(0,min(1,(co.z-.110)/.220));w=w*w*(3-2*w)
                            vert.co=co+Vector((value*w,0,-.004*w))
                        obj.data.update()
                details=dict(body_shift_H=[value,0,-.004],planted_hooves=hoof_names,
                             limitation='Imposed support deformation; not a mass-weighted COM simulation.')
            bpy.context.view_layer.update()
            posed=BUILD['geometry_digest']()
            if part!='gaze': assert posed!=neutral
            appearance=hashlib.sha256(np.array(eye_image.pixels[:],dtype=np.float32).tobytes()).hexdigest()
            if part=='gaze': assert appearance!=pigment_hash
            views={}
            for view in ['front','side']:
                scene.camera=bpy.data.objects['CAM '+view]
                views[view]=BUILD['geometry_digest']()
                assert views[view]==posed
                scene.render.filepath=str(OUTPUT/(name+'-'+view+'.png'))
                bpy.ops.render.render(write_still=True)
            if part=='support':
                assert ground()==neutral_ground
                details['evaluated_hoof_min_Z_H']=ground()
            restore()
            assert BUILD['geometry_digest']()==neutral
            assert hashlib.sha256(np.array(eye_image.pixels[:],dtype=np.float32).tobytes()).hexdigest()==pigment_hash
            results.append(dict(name=name,part=part,objects=[o.name for o in targets],
                                view_geometry_digests=views,pigment_digest=appearance,
                                neutral_restored=True,**details))
    finally:
        restore()
        scene.camera,scene.render.filepath=old_camera,old_path
        bpy.context.view_layer.update()
    assert BUILD['geometry_digest']()==neutral
    assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==asset_hash
    report=dict(neutral_geometry_digest=neutral,selected_revision=revision,
        method='Disposable rigid head/ear transforms, iris pigment offsets, conformal blink endpoint and graded support shift. No rig.',
        diagnostic_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        cases=results,exact_neutral_restored=True,neutral_pigment_restored=True,asset_file_unchanged=True,
        production_poses_saved=False,automatic_motion_pass=False,
        interpretation='Rejection probes only. Read image sheets and README findings; no Human or motion PASS.')
    (OUTPUT/'motion-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
    print('CLEARANCE_PROBES_COMPLETE; exact neutral and pigment restored; asset unchanged')


if __name__=='__main__': main()
