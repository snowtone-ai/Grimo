"""Build Carol Blockout v001 and its camera evidence package.

This is deliberately a small, deterministic Blender source generator.  It creates
diagnostic clay/flat-color materials only; it is not a rig, export, or runtime
asset pipeline.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view


ROOT = "Carol_Model"
FRONT = Vector((0.0, -1.0, 0.0))


def material(name, color, roughness=0.72, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m


def smooth(obj):
    if obj.type == "MESH":
        for p in obj.data.polygons:
            p.use_smooth = True
    return obj


def parent(obj, root):
    obj.parent = root
    return obj


def uv(name, loc, scale, mat, root, segments=32, rings=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    smooth(obj)
    return parent(obj, root)


def capsule(name, loc, scale, mat, root):
    return uv(name, loc, scale, mat, root, 24, 16)


def extruded_polygon(name, points, depth, mat, root, y=-0.45):
    # points are x,z pairs; front is the negative-y side for the review cameras.
    verts = [(x, y - depth / 2, z) for x, z in points] + [(x, y + depth / 2, z) for x, z in points]
    n = len(points)
    faces = [tuple(range(n)), tuple(range(n, 2 * n))[::-1]]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new("Blockout bevel", "BEVEL")
    bevel.width = min(depth * 0.22, 0.055)
    bevel.segments = 3
    return parent(obj, root)


def star(name, x, z, size, mat, root):
    points = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        r = size if i % 2 == 0 else size * 0.44
        points.append((x + math.cos(a) * r, z + math.sin(a) * r))
    return extruded_polygon(name, points, 0.055, mat, root, -0.49)


def crescent(name, x, z, size, mat, root):
    points = []
    for i in range(25):
        a = math.radians(132 + (360 - 132) * i / 24)
        points.append((x + math.cos(a) * size, z + math.sin(a) * size))
    # Inner arc is offset right, leaving a recognizable crescent cutout.
    for i in range(24, -1, -1):
        a = math.radians(132 + (360 - 132) * i / 24)
        points.append((x + size * 0.42 + math.cos(a) * size * 0.73, z + math.sin(a) * size * 0.73))
    return extruded_polygon(name, points, 0.06, mat, root, -0.50)


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def camera(name, projection, loc, target, root):
    data = bpy.data.cameras.new(name)
    data.type = projection
    data.lens = 58.0
    data.sensor_width = 36.0
    data.clip_start = 0.01
    data.clip_end = 100.0
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    look_at(obj, target)
    parent(obj, root)
    return obj


def build_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.materials, bpy.data.cameras, bpy.data.meshes, bpy.data.curves):
        # Keep the file deterministic and avoid inherited default scene data.
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)

    root = bpy.data.objects.new(ROOT, None)
    bpy.context.collection.objects.link(root)

    fleece = material("Carol_Blockout_Fleece", (0.82, 0.84, 1.0))
    fleece_light = material("Carol_Blockout_Fleece_Light", (1.0, 0.94, 0.88))
    fleece_blue = material("Carol_Blockout_Fleece_Blue", (0.48, 0.57, 0.98))
    cream = material("Carol_Blockout_Face", (1.0, 0.78, 0.60))
    dark = material("Carol_Blockout_Eye", (0.055, 0.025, 0.045), 0.25)
    brown = material("Carol_Blockout_Hoof_Ear", (0.25, 0.10, 0.075))
    pink = material("Carol_Blockout_Ear_Inner", (0.9, 0.28, 0.30))
    gold = material("Carol_Blockout_Moon_Star", (1.0, 0.64, 0.08), 0.42)

    # Hidden low chassis, kept visible in clay/side views only through the shell gaps.
    capsule("Carol_Chassis_Hidden", (0.0, 0.10, 0.72), (1.44, 0.58, 0.43), brown, root)

    # Primary broad envelope: a few deliberately unequal regional masses, not wool beads.
    uv("Fleece_Primary_Shell", (0.0, 0.05, 1.32), (1.62, 0.62, 1.20), fleece, root)
    uv("Fleece_Crown_Large", (-0.30, -0.12, 2.15), (1.02, 0.46, 0.58), fleece_light, root)
    uv("Fleece_Left_Region", (-1.16, 0.02, 1.38), (0.63, 0.48, 0.80), fleece_blue, root)
    uv("Fleece_Right_Region", (1.15, 0.03, 1.35), (0.62, 0.48, 0.76), fleece_light, root)
    uv("Fleece_Lower_Collar", (0.0, -0.16, 0.64), (1.40, 0.42, 0.47), fleece_light, root)
    uv("Fleece_Rear_Terminal", (1.55, 0.18, 1.10), (0.48, 0.48, 0.55), fleece_blue, root)

    # Shallow embedded acting region and face-center marker.
    uv("Carol_Face", (0.0, -0.59, 1.22), (0.78, 0.16, 0.52), cream, root)
    face_center = bpy.data.objects.new("Carol_Face_Center", None)
    face_center.empty_display_type = "SPHERE"
    face_center.empty_display_size = 0.045
    face_center.location = (0.0, -0.78, 1.25)
    bpy.context.collection.objects.link(face_center)
    parent(face_center, root)
    for x in (-0.30, 0.30):
        uv("Carol_Eye_L" if x < 0 else "Carol_Eye_R", (x, -0.79, 1.34), (0.16, 0.055, 0.23), dark, root)
    uv("Carol_Nose", (0.0, -0.80, 1.17), (0.075, 0.035, 0.045), dark, root)
    uv("Carol_Mouth", (0.0, -0.805, 1.08), (0.13, 0.025, 0.07), pink, root)

    # Broad sideways ears with separate inner proxies.
    for side in (-1, 1):
        x = side * 0.91
        uv(f"Carol_Ear_{'L' if side < 0 else 'R'}", (x, -0.33, 1.35), (0.42, 0.13, 0.19), brown, root)
        uv(f"Carol_Ear_Inner_{'L' if side < 0 else 'R'}", (x, -0.47, 1.34), (0.27, 0.035, 0.095), pink, root)

    # Four short supports and visible hoof ends; upper limbs remain hidden.
    for i, (x, y) in enumerate(((-0.90, -0.20), (0.90, -0.20), (-0.78, 0.28), (0.78, 0.28)), 1):
        capsule(f"Carol_Support_{i}", (x, y, 0.36), (0.23, 0.25, 0.36), brown, root)
        uv(f"Carol_Hoof_{i}", (x, y - 0.08, 0.16), (0.27, 0.28, 0.18), brown, root)

    # Subordinate, separate rear tuft/tail.
    uv("Carol_Rear_Tuft", (1.57, 0.42, 1.00), (0.34, 0.30, 0.38), fleece_light, root)

    # Body-relative identity motifs: shallow attached proxy plates.
    crescent("Carol_Moon_Attached", -0.77, 1.80, 0.36, gold, root)
    for i, (x, z, s) in enumerate(((-0.70, 2.45, 0.16), (0.0, 2.53, 0.17), (0.66, 2.16, 0.14), (-0.72, 0.86, 0.14), (0.63, 0.71, 0.13)), 1):
        star(f"Carol_Star_Attached_{i}", x, z, s, gold, root)

    # Review cameras. The alias is intentionally the perspective candidate.
    persp = camera("Carol_Camera_front_perspective", "PERSP", (0.0, -10.00, 1.24), (0.0, 0.0, 1.47), root)
    persp.data.lens = 58.0
    ortho = camera("Carol_Camera_front_orthographic", "ORTHO", (0.0, -6.0, 1.25), (0.0, 0.0, 1.55), root)
    ortho.data.ortho_scale = 6.40
    alias = persp.copy()
    alias.data = persp.data.copy()
    alias.name = "Carol_Camera_front"
    bpy.context.collection.objects.link(alias)
    parent(alias, root)
    alias.location = persp.location
    alias.rotation_euler = persp.rotation_euler
    for name, loc, yaw in (("Carol_Camera_three_quarter", (7.0, -8.0, 1.35), 0), ("Carol_Camera_side", (8.0, 0.0, 1.30), 0), ("Carol_Camera_back", (0.0, 8.0, 1.30), 0), ("Carol_Camera_silhouette", (-8.0, -8.0, 1.25), 0), ("Carol_Camera_clay", (0.0, -10.0, 1.24), 0)):
        cam = camera(name, "PERSP", loc, (0.0, 0.0, 1.55), root)
        cam.data.lens = 58.0
    return root, persp, ortho


def setup_render(scene, width, height):
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    scene.render.filepath = ""
    scene.world.color = (0.015, 0.02, 0.05)
    scene.render.image_settings.color_depth = "8"


def alpha_metrics(path, image, camera_obj, face_obj, width, height):
    bpy.data.images.load(str(path), check_existing=False)
    px = list(image.pixels)
    xs, ys = [], []
    for y in range(height):
        row = y * width
        for x in range(width):
            if px[(row + x) * 4 + 3] > 0.04:
                xs.append(x)
                ys.append(y)
    if not xs:
        raise RuntimeError(f"transparent render has no visible pixels: {path}")
    left, right = min(xs) / width, (max(xs) + 1) / width
    bottom_px, top_px = min(ys), max(ys) + 1
    top = 1.0 - top_px / height
    bottom = 1.0 - bottom_px / height
    face = world_to_camera_view(bpy.context.scene, camera_obj, face_obj.location)
    return {"bbox": {"left": left, "right": right, "top": top, "bottom": bottom}, "width": right-left, "height": bottom-top, "topMargin": top, "bottomMargin": 1-bottom, "leftMargin": left, "rightMargin": 1-right, "faceCenter": {"x": face.x, "y": face.y}}


def render_and_measure(scene, cam, face, out_dir, label, width, height):
    scene.camera = cam
    setup_render(scene, width, height)
    path = out_dir / f"carol-front-{label}.png"
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    image = bpy.data.images.load(str(path), check_existing=False)
    metrics = alpha_metrics(path, image, cam, face, width, height)
    return str(path), metrics


def render_standard(scene, out_dir):
    names = ("front", "three-quarter", "side", "back", "silhouette", "clay")
    for name in names:
        cam = bpy.data.objects[f"Carol_Camera_{name.replace('-', '_')}"]
        scene.camera = cam
        scene.render.filepath = str(out_dir / f"carol-{name}.png")
        bpy.ops.render.render(write_still=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend-path", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    cli = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    args = parser.parse_args(cli)
    args.blend_path.parent.mkdir(parents=True, exist_ok=True)
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    root, persp, ortho = build_scene()
    face = bpy.data.objects["Carol_Face_Center"]
    setup_render(scene, 1920, 1080)
    # Lighting is restrained diagnostic lighting, not production shading.
    bpy.ops.object.light_add(type="AREA", location=(-3.0, -4.0, 5.0))
    key = bpy.context.object
    key.name = "Carol_Blockout_Key"
    key.data.energy = 850
    key.data.shape = "DISK"
    key.data.size = 4.0
    look_at(key, (0.0, 0.0, 1.0))
    parent(key, root)
    bpy.ops.object.light_add(type="AREA", location=(3.0, 1.0, 2.0))
    fill = bpy.context.object
    fill.name = "Carol_Blockout_Fill"
    fill.data.energy = 350
    fill.data.size = 3.0
    look_at(fill, (0.0, 0.0, 1.1))
    parent(fill, root)

    render_standard(scene, args.evidence_dir)
    records = {}
    for projection, cam in (("perspective", persp), ("orthographic", ortho)):
        _, m169 = render_and_measure(scene, cam, face, args.evidence_dir, f"{projection}-16x9", 1920, 1080)
        _, mp = render_and_measure(scene, cam, face, args.evidence_dir, f"{projection}-portrait-diagnostic", 412, 915)
        records[projection] = {"camera": {"type": cam.data.type, "location": list(cam.location), "lens": cam.data.lens, "orthoScale": cam.data.ortho_scale}, "benchmark_16x9": m169, "portrait_412x915_diagnostic": mp}
    metrics_path = args.evidence_dir / "framing-metrics.json"
    metrics_path.write_text(json.dumps({"schema": "grimo.carol.blockout-framing-metrics", "version": 1, "source": "carol-blockout-v001.blend", "note": "16:9 is benchmark calibration; portrait is diagnostic only.", "candidates": records}, indent=2), encoding="utf-8")
    bpy.ops.wm.save_as_mainfile(filepath=str(args.blend_path))
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
