"""Render matched v004 Skin and unchanged v004 Fleece occlusion diagnostics."""
import importlib.util
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'assets/grimo/production/carol/blender'
EVIDENCE = ROOT / 'docs/production/carol/evidence/skin-default-v004'
V003 = ASSETS / 'carol-skin-default-v003.blend'
V004 = ASSETS / 'carol-skin-default-v004.blend'
FLEECE = ASSETS / 'carol-normal-fleece-v004.blend'

spec = importlib.util.spec_from_file_location(
    'skin_builder_v004', Path(__file__).with_name('build-carol-skin-default-v004.py'))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
spec = importlib.util.spec_from_file_location(
    'ear_util', Path(__file__).with_name('build-carol-ear-production-v002.py'))
util = importlib.util.module_from_spec(spec)
spec.loader.exec_module(util)

SKIN = builder.SKIN_MESHES | builder.SKIN_CURVES
FLEECE_OBJECTS = {'HeadFleece', 'BodyFleece', 'HeadFleeceBacking', 'TailFleece'}
FULL_VIEWS = [
    ('front', (-4, 0, 0), (.52, 0, .395), 1.29),
    ('side', (0, -4, 0), (.53, 0, .395), 1.34),
    ('front-3q', (-4, -2, .35), (.52, 0, .395), 1.34),
]
CLOSE_VIEWS = [
    ('ear-side', (0, -4, 0), (.47, -.30, .535), .65),
    ('ear-top', (0, 0, 4), (.49, -.40, .52), .58),
]


def set_render_state():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 16
    scene.cycles.use_denoising = True
    scene.render.use_compositing = False
    scene.view_settings.view_transform = 'AgX'
    if scene.world and scene.world.use_nodes:
        background = next((n for n in scene.world.node_tree.nodes if n.type == 'BACKGROUND'), None)
        if background:
            background.inputs['Strength'].default_value = .5
    scene.frame_set(1)


def open_skin(path, load_fleece_lights=True):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    if load_fleece_lights:
        for ob in list(bpy.context.scene.objects):
            if ob.type == 'LIGHT':
                bpy.data.objects.remove(ob, do_unlink=True)
        with bpy.data.libraries.load(str(FLEECE), link=False) as (src, dst):
            dst.objects = ['Key', 'Fill', 'Rear', 'Low']
        for ob in dst.objects:
            bpy.context.scene.collection.objects.link(ob)
    set_render_state()


def attach_ears(source, refine):
    with bpy.data.libraries.load(str(source), link=False) as (src, dst):
        dst.objects = ['EAR_L', 'EAR_R']
    for source_object in dst.objects:
        target = bpy.data.objects[source_object.name.removesuffix('.001')]
        target.data = source_object.data.copy()
        if refine:
            sign = 1 if target.name == 'EAR_L' else -1
            builder.refine(target, sign)
        bpy.data.objects.remove(source_object, do_unlink=True)
    bpy.context.view_layer.update()


def render_group(folder, views, visible):
    util.TMP = EVIDENCE / folder
    util.TMP.mkdir(parents=True, exist_ok=True)
    for name, direction, target, scale in views:
        print('RENDER', folder, name, flush=True)
        util.render(name, direction, target, scale, visible, size=(760, 670))


def measure_visible_ears(direction, target, scale):
    """Measure exposed ear silhouettes in camera-plane units under Fleece."""
    scene = bpy.context.scene
    target = Vector(target)
    cam_data = bpy.data.cameras.new('TEMP front-axis diagnostic')
    cam = bpy.data.objects.new('TEMP front-axis diagnostic', cam_data)
    scene.collection.objects.link(cam)
    cam.location = target + Vector(direction)
    cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = scale
    scene.camera = cam
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    ray = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
    result = {}

    for name in sorted(builder.EARS):
        ear = bpy.data.objects[name]
        stations = {}
        for index, vertex in enumerate(ear.data.vertices):
            world = ear.matrix_world @ vertex.co
            camera_local = cam.matrix_world.inverted() @ world
            origin = cam.matrix_world @ Vector((camera_local.x, camera_local.y, 0.0))
            hit, _, _, _, hit_object, _ = scene.ray_cast(depsgraph, origin, ray, distance=10.0)
            if hit and hit_object and hit_object.name == name:
                stations.setdefault(index // builder.RING_SIZE, []).append(
                    (camera_local.x, camera_local.y))

        # Use each exposed station's complete ring center for the ear axis.
        # Averaging only front-facing surface vertices biases ring centers
        # toward the camera and can erase the vertical centerline change.
        centers = []
        for station in sorted(stations):
            start = station * builder.RING_SIZE
            ring = ear.data.vertices[start:start + builder.RING_SIZE]
            center = sum((ear.matrix_world @ v.co for v in ring), Vector()) / builder.RING_SIZE
            camera_center = cam.matrix_world.inverted() @ center
            centers.append((station, camera_center.x, camera_center.y))
        if len(centers) >= 2:
            first, last = centers[0], centers[-1]
            dx, dy = last[1] - first[1], last[2] - first[2]
            # Camera-space Y increases upward, so a lower tip has negative dy.
            # The horizontal axis may run either left or right on screen for
            # mirrored ears; that must not reverse the sign of downward slope.
            downward = -dy
            angle = math.degrees(math.atan2(downward, abs(dx)))
            result[name] = {
                'visible_stations': [first[0], last[0]],
                'visible_vertex_samples': sum(len(points) for points in stations.values()),
                'camera_plane_axis_endpoints_H': [first[1:], last[1:]],
                'axis_deltas_H': [dx, dy],
                'downward_axis_angle_degrees': angle,
                'visible_silhouette_ratio_height_to_width': (
                    (max(p[1] for ps in stations.values() for p in ps)
                     - min(p[1] for ps in stations.values() for p in ps))
                    / max(1e-12,
                          max(p[0] for ps in stations.values() for p in ps)
                          - min(p[0] for ps in stations.values() for p in ps))
                ),
            }
        else:
            result[name] = {'visible_stations': sorted(stations), 'downward_axis_angle_degrees': None}

    scene.camera = None
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cam_data)
    return result


def measure_axis_comparison():
    results = {}
    for label, source in (('v003', V003), ('v004', V004)):
        open_skin(FLEECE, load_fleece_lights=False)
        attach_ears(source, refine=False)
        results[label] = {
            'front': measure_visible_ears((-4, 0, 0), (.52, 0, .395), 1.29),
            'side': measure_visible_ears((0, -4, 0), (.53, 0, .395), 1.34),
        }
    output = {
        'method': ('Camera-plane centerline uses complete ear ring centers only at stations '
                   'with at least one visible surface vertex after ray tests against unchanged '
                   'v004 Fleece. Silhouette ratio is exposed-vertex camera-plane height/width.'),
        'front_downward_angle_target_degrees': [13, 23],
        'front_visible_silhouette_ratio_target': [0.70, 0.84],
        'side_visible_silhouette_ratio_target': [0.74, 0.90],
        'comparison': results,
    }
    path = EVIDENCE / 'front-axis-diagnostic.json'
    path.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print('FRONT_AXIS_DIAGNOSTIC', json.dumps(output), flush=True)
    return output


def render_preview_a():
    """Render the unbounded numeric pass from memory; never writes a Blend."""
    open_skin(V003)
    for name, sign in (('EAR_L', 1), ('EAR_R', -1)):
        result = builder.refine(bpy.data.objects[name], sign)
        print('PASS_A_PREVIEW_METRICS', name, result, flush=True)
    render_group('preview-pass-a/skin', FULL_VIEWS + CLOSE_VIEWS, SKIN)

    open_skin(FLEECE, load_fleece_lights=False)
    attach_ears(V003, refine=True)
    render_group('preview-pass-a/fleece', FULL_VIEWS, SKIN | FLEECE_OBJECTS)


def render_final():
    open_skin(V004)
    render_group('renders/skin-v004', FULL_VIEWS + CLOSE_VIEWS, SKIN)

    open_skin(FLEECE, load_fleece_lights=False)
    attach_ears(V004, refine=False)
    print('VISIBLE_FRONT_EAR_AXIS',
          measure_visible_ears((-4, 0, 0), (.52, 0, .395), 1.29), flush=True)
    render_group('renders/fleece-occlusion', FULL_VIEWS, SKIN | FLEECE_OBJECTS)


if __name__ == '__main__':
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if '--preview-a' in sys.argv:
        render_preview_a()
    elif '--axis-comparison' in sys.argv:
        measure_axis_comparison()
    else:
        render_final()
