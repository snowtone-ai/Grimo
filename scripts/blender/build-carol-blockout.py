"""Carol structural blockout v002, Blender 5.2.1 LTS.

Reproducible volume study, not production topology. Front = -Y; up = +Z.
--pass-number 1/2/3 exposes macro, hierarchy and character-structure iterations.
The default is the final study. No rig, animation, UV work or export is performed.
v001 is read for provenance and must never be an output destination.
"""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

REPO = Path(__file__).resolve().parents[2]
CANONICAL = REPO / "assets/grimo/source/carol/carol-Identity-canonical.png"
V001 = REPO / "assets/grimo/production/carol/blender/carol-blockout-v001.blend"
VIEWS = ("front-perspective", "front-orthographic", "three-quarter", "side", "back", "silhouette", "clay")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = .8
    return mat


def smooth(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def empty(name, loc=(0, 0, 0), parent=None):
    obj = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.parent = parent
    obj.empty_display_size = .08
    return obj


def uv(name, loc, scale, mat, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=28, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    obj.parent = parent
    return smooth(obj)


def fuse(name, parts, mat, parent, voxel=.028, iterations=5):
    """Union overlapping design volumes into one continuous sculpt surface."""
    bpy.ops.object.select_all(action="DESELECT")
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    remesh = obj.modifiers.new("Design volume union; not final retopology", "REMESH")
    remesh.mode = "VOXEL"
    remesh.voxel_size = voxel
    remesh.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    relax = obj.modifiers.new("Soft transitions", "SMOOTH")
    relax.factor = 1.25
    relax.iterations = iterations
    bpy.ops.object.modifier_apply(modifier=relax.name)
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    obj.parent = parent
    return smooth(obj)


# Deliberately authored regions. Depth is continuous across front/side/rear.
# No uniform rings, random scatter, or one-object-per-final-wool-ball system.
MAJOR = [
    ("Core", (0, .22, 1.27), (1.43, 1.10, .96)),
    ("CrownLeft", (-.43, .02, 2.12), (.73, .72, .60)),
    ("CrownRight", (.47, .30, 2.12), (.64, .72, .59)),
    ("MoonShoulder", (-1.03, -.12, 1.68), (.65, .86, .67)),
    ("RightShoulder", (1.09, .06, 1.55), (.57, .65, .49)),
    ("RearCrown", (-.12, .94, 1.79), (.92, .64, .68)),
    ("RearLeft", (-.81, .84, .99), (.68, .68, .68)),
    ("RearRight", (.76, .93, 1.02), (.71, .64, .66)),
    ("BrowLeft", (-.37, -.85, 1.91), (.51, .48, .43)),
    ("BrowRight", (.44, -.85, 1.86), (.52, .46, .43)),
    ("LowerLeft", (-.78, -.48, .72), (.57, .63, .35)),
    ("LowerRight", (.77, -.44, .69), (.57, .67, .35)),
    ("Chin", (.04, -.84, .55), (.50, .36, .23)),
]

MEDIUM = [
    ("CrownPeak", (-.26, -.35, 2.51), (.44, .48, .39)),
    ("CrownBridge", (.59, -.36, 2.41), (.43, .48, .39)),
    ("LeftRise", (-.94, .08, 2.25), (.47, .55, .44)),
    ("MoonLower", (-1.36, -.40, 1.38), (.40, .50, .45)),
    ("LeftLow", (-1.30, .04, .80), (.44, .63, .39)),
    ("RightRise", (1.17, -.23, 2.04), (.43, .53, .43)),
    ("RightFlank", (1.40, .58, 1.30), (.40, .50, .43)),
    ("RightHaunch", (1.08, .99, .79), (.44, .48, .42)),
    ("RearLow", (.12, 1.20, .69), (.61, .44, .40)),
    ("RearHighL", (-.50, 1.25, 1.81), (.52, .39, .48)),
    ("RearHighR", (.50, 1.23, 1.91), (.48, .39, .43)),
    ("RearMidL", (-1.05, 1.10, 1.40), (.41, .41, .49)),
    ("RearMidR", (.91, 1.22, 1.36), (.49, .37, .42)),
    ("BrowCenter", (.04, -1.12, 1.88), (.36, .37, .35)),
    ("BrowSweepL", (-.60, -1.13, 1.75), (.34, .35, .32)),
    ("BrowSweepR", (.62, -1.12, 1.71), (.31, .34, .31)),
    ("CheekL", (-.81, -1.12, 1.03), (.27, .33, .29)),
    ("CheekR", (.82, -1.11, 1.04), (.26, .33, .29)),
    ("ChinL", (-.49, -1.08, .62), (.31, .33, .27)),
    ("ChinR", (.51, -1.06, .59), (.32, .35, .27)),
    ("LowerTurnL", (-1.01, -.76, .64), (.38, .40, .32)),
    ("LowerTurnR", (1.11, -.70, .72), (.36, .45, .33)),
]

SMALL = [
    ("TempleL", (-.85, -1.05, 1.47), (.24, .30, .25)),
    ("TempleR", (.88, -1.00, 1.44), (.23, .28, .24)),
    ("LowScallopL", (-.25, -1.12, .44), (.23, .23, .19)),
    ("LowScallopR", (.24, -1.08, .46), (.22, .25, .18)),
    ("FlankBreakL", (-1.58, .34, 1.05), (.22, .31, .28)),
    ("FlankBreakR", (1.48, -.23, .97), (.24, .33, .27)),
    ("RearBreak", (-.34, 1.46, .92), (.29, .23, .28)),
    ("CrownBreak", (-.76, -.49, 2.45), (.26, .32, .27)),
    ("CheekTurnL", (-.77, -1.12, .79), (.24, .28, .24)),
    ("CheekTurnR", (.77, -1.12, .80), (.25, .29, .22)),
    ("SideBridge", (1.40, -.04, 1.68), (.33, .41, .33)),
    ("RearSupportCoverL", (-.73, 1.12, .54), (.37, .37, .28)),
    ("RearSupportCoverR", (.73, 1.16, .56), (.37, .34, .28)),
]


def ear(name, side, mat, inner, root, refined):
    """Closed thick leaf with a recessed bowl and a concealed narrow root."""
    verts, faces = [], []
    rows, cols = 16, 32
    for i in range(rows + 1):
        t = i / rows
        width = .055 + (.235 if refined else .13) * math.sin(math.pi*t)**.8
        for j in range(cols):
            a = 2*math.pi*j/cols
            x = side * (.69 + (.96 if refined else .66)*t)
            z = 1.40 - .17*t - .055*math.sin(math.pi*t) + width*math.cos(a)
            # Bowl recessed at the center, substantial soft back and edge lip.
            y = -1.02 + .08*t + .10*math.sin(a)
            if math.sin(a) < 0:
                y += .055*math.sin(math.pi*t)*(-math.sin(a))**3
            verts.append((x, y, z))
    for i in range(rows):
        for j in range(cols):
            faces.append((i*cols+j, i*cols+(j+1)%cols,
                          (i+1)*cols+(j+1)%cols, (i+1)*cols+j))
    faces += [tuple(range(cols-1, -1, -1)), tuple(rows*cols+j for j in range(cols))]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj.data.materials.append(inner)
    for index, poly in enumerate(mesh.polygons):
        row, col = divmod(index, cols)
        if 2 <= row <= 13 and 18 <= col <= 25:
            poly.material_index = 1
    sub = obj.modifiers.new("Soft ear volume", "SUBSURF")
    sub.levels = 2
    obj.parent = root
    return smooth(obj)


def attached_polygon(name, points, shell, mat, root):
    """A shallow solid motif follows actual fleece depth, never a common plane."""
    verts = [Vector((x, 0, z)) for x, z in points]
    faces = tessellate_polygon([verts])  # Blender 5.2 returns vertex indices.
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.subdivide_edges(bm, edges=list(bm.edges), cuts=4, use_grid_fill=True)
    for v in bm.verts:
        hit, loc, _, _ = shell.ray_cast(Vector((v.co.x, -5, v.co.z)), Vector((0, 1, 0)))
        if not hit:
            raise RuntimeError(f"Unattached motif: {name}")
        v.co.y = loc.y - .04
    # Relax only depth to avoid sawtooth tips across voxel-sized surface changes.
    bmesh.ops.smooth_vert(bm, verts=list(bm.verts), factor=.6,
                          use_axis_x=False, use_axis_y=True, use_axis_z=False)
    boundary = [e for e in bm.edges if e.is_boundary]
    original_faces = list(bm.faces)
    copied = bmesh.ops.duplicate(bm, geom=list(bm.verts)+list(bm.edges)+original_faces)
    for v in copied["geom"]:
        if isinstance(v, bmesh.types.BMVert):
            v.co.y += .055
    vertex_map = copied["vert_map"]
    # duplicate maps copied vertices to original vertices in Blender 5.2.
    copies = {original: duplicate for duplicate, original in vertex_map.items()}
    for edge in boundary:
        a, b = edge.verts
        bm.faces.new((a, b, copies[b], copies[a]))
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj.parent = root
    return smooth(obj)


def motifs(shell, mat, root):
    # One moon only. Front-visible map is provisional; hidden packet conflicts
    # are not resolved by inventing more motifs on the back.
    x, z, r = -1.15, 1.96, .33
    pts = [(x+r*math.cos(math.radians(60+240*i/40)),
            z+r*math.sin(math.radians(60+240*i/40))) for i in range(41)]
    inner_r = math.hypot(.5-.62, math.sin(math.pi/3))
    angle = math.degrees(math.atan2(math.sin(math.pi/3), .5-.62))
    pts += [(x+r*(.62+inner_r*math.cos(math.radians(-angle-(360-2*angle)*i/40))),
             z+r*inner_r*math.sin(math.radians(-angle-(360-2*angle)*i/40))) for i in range(1, 40)]
    attached_polygon("Carol_Moon_Attached", pts, shell, mat, root)
    for i, (x, z, r) in enumerate(((-.18, 2.52, .20), (.16, 1.97, .18),
                                  (-1.16, .83, .16), (.39, .55, .15), (-.30, .54, .10)), 1):
        pts = []
        for j in range(10):
            a = math.pi/2 + j*math.pi/5
            radius = r if j%2 == 0 else r*.48
            pts.append((x+radius*math.cos(a), z+radius*math.sin(a)))
        attached_polygon(f"Carol_Star_Attached_{i}", pts, shell, mat, root)


def look_at(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat("-Z", "Y").to_euler()


def cameras(root):
    # Equal review distance and useful all-body margin, independent of portrait UI.
    targets = {
        "front-perspective": (0, -10, 2.35),
        "front-orthographic": (0, -10, 2.35),
        "three-quarter": (7.1, -7.1, 2.75),
        "side": (10, 0, 2.35), "back": (0, 10, 2.35),
        "silhouette": (-7.1, -7.1, 2.75), "clay": (7.1, -7.1, 2.75),
    }
    for label, loc in targets.items():
        data = bpy.data.cameras.new(label)
        data.type = "ORTHO" if label == "front-orthographic" else "PERSP"
        data.lens = 60
        data.ortho_scale = 5.7
        obj = bpy.data.objects.new("Carol_Camera_"+label.replace("-", "_"), data)
        bpy.context.collection.objects.link(obj)
        obj.location = loc
        look_at(obj, (0, .1, 1.43))
        obj.parent = root
    alias = bpy.data.objects["Carol_Camera_front_perspective"].copy()
    alias.data = alias.data.copy()
    alias.name = "Carol_Camera_front"
    bpy.context.collection.objects.link(alias)


def build_scene(pass_number):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    root = empty("Carol_Model")
    root["stage"] = "v002 structural study / Human Gate pending"
    fleece = material("Diagnostic_Fleece", (.79, .82, .94))
    cream = material("Diagnostic_Face", (.94, .76, .56))
    brown = material("Diagnostic_Ear_Hoof", (.21, .095, .06))
    pink = material("Diagnostic_Ear_Inner", (.65, .25, .22))
    dark = material("Diagnostic_Face_Landmarks", (.052, .028, .022))
    gold = material("Diagnostic_Motifs", (.95, .62, .13))

    uv("Carol_Chassis_Hidden", (0, .12, .73), (.92, 1.06, .40), brown, root)
    regions = MAJOR + (MEDIUM if pass_number >= 2 else []) + (SMALL if pass_number >= 3 else [])
    shell = fuse("Carol_Fleece_Continuous", [uv("Volume_"+n, p, s, fleece) for n, p, s in regions], fleece, root)
    shell["design_regions"] = json.dumps(regions)
    shell["topology_status"] = "voxel design surface; production retopology deferred"

    face = uv("Carol_Face", (0, -1.08, 1.15), (.84, .37, .53), cream, root)
    for v in face.data.vertices:
        t = v.co.z/.53
        v.co.x *= 1-.08*t  # fuller low cheeks, narrower brow, no spherical head
    empty("Carol_Face_Center", (0, -1.46, 1.19), root)
    for side in (-1, 1):
        eye = uv("Carol_Eye_"+("L" if side < 0 else "R"),
                 (side*.32, -1.427, 1.23), (.165, .027, .205), dark, root)
        eye.rotation_euler.z = side*math.radians(12)
        ear("Carol_Ear_"+("L" if side < 0 else "R"), side, brown, pink, root, pass_number >= 3)
        empty("Carol_Ear_Root_"+("L" if side < 0 else "R"), (side*.72, -1.01, 1.40), root)
    uv("Carol_Nose", (0, -1.455, 1.09), (.054, .024, .035), dark, root)
    uv("Carol_Mouth", (0, -1.441, 1.00), (.087, .018, .047), dark, root)

    # Four independent short support members. Flattened hoof soles meet z=.025.
    for i, (x, y) in enumerate(((-.68, -.69), (.68, -.69), (-.73, .91), (.73, .91)), 1):
        support = uv(f"Carol_Support_{i}", (x, y, .43), (.22, .25, .36), brown, root)
        support["role"] = "fore" if i <= 2 else "rear"
        hoof = uv(f"Carol_Hoof_{i}", (x, y-.035, .20), (.265, .31, .23), brown, root)
        for v in hoof.data.vertices:
            v.co.z = max(v.co.z, -.175)
        empty(f"Carol_Support_Root_{i}", (x, y, .69), root)

    tailparts = [uv("TailCore", (0, 1.64, 1.05), (.29, .39, .29), fleece)]
    if pass_number >= 3:
        tailparts += [uv("TailLobeL", (-.14, 1.82, 1.12), (.20, .22, .21), fleece),
                      uv("TailLobeR", (.14, 1.82, 1.10), (.20, .21, .20), fleece),
                      uv("TailLobeTop", (0, 1.81, 1.27), (.20, .20, .19), fleece)]
    tail = fuse("Carol_Rear_Tuft", tailparts, fleece, root, voxel=.023, iterations=3)
    # Independent root at its actual rear attachment, not the body origin.
    bpy.context.scene.cursor.location = (0, 1.43, 1.02)
    bpy.context.view_layer.objects.active = tail
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    empty("Carol_Rear_Tuft_Root", (0, 1.43, 1.02), root)
    motifs(shell, gold, root)
    cameras(root)
    return root


def render_evidence(out_dir, width):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = width
    scene.render.resolution_y = int(width*.85)
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    scene.world = bpy.data.worlds.new("Review World")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (.32, .36, .44, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = .45
    for name, loc, energy, size in (("Key", (-3, -4, 6), 750, 4),
                                    ("Fill", (4, -2, 3), 450, 4),
                                    ("Rear", (1, 5, 5), 650, 4)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        obj = bpy.context.object
        obj.name = "Carol_Review_"+name
        obj.data.energy = energy
        obj.data.shape = "DISK"
        obj.data.size = size
        look_at(obj, (0, 0, 1.3))
    clay = material("Review_Clay_Override", (.55, .55, .55))
    silhouette = material("Review_Silhouette_Override", (0, 0, 0))
    # Swap slots explicitly: the evidence must actually be clay / silhouette.
    saved = {obj.name: list(obj.data.materials) for obj in scene.objects if obj.type == "MESH"}
    silhouette.use_nodes = True
    nodes = silhouette.node_tree.nodes
    nodes.clear()
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs[0].default_value = (.025, .028, .035, 1)
    output = nodes.new("ShaderNodeOutputMaterial")
    silhouette.node_tree.links.new(emission.outputs[0], output.inputs[0])
    for label in VIEWS:
        for name, mats in saved.items():
            slots = bpy.data.objects[name].data.materials
            for i, mat in enumerate(mats):
                slots[i] = clay if label == "clay" else silhouette if label == "silhouette" else mat
        scene.camera = bpy.data.objects["Carol_Camera_"+label.replace("-", "_")]
        scene.render.filepath = str(out_dir / f"carol-v002-{label}.png")
        bpy.ops.render.render(write_still=True)
        image = bpy.data.images.load(scene.render.filepath, check_existing=False)
        pixels = np.empty(len(image.pixels), dtype=np.float32)
        image.pixels.foreach_get(pixels)
        alpha = pixels.reshape(image.size[1], image.size[0], 4)[:, :, 3]
        ys, xs = np.where(alpha > .05)
        assert len(xs) > 0, label
        assert xs.min() > 10 and xs.max() < image.size[0]-10, label+" horizontal crop"
        assert ys.min() > 10 and ys.max() < image.size[1]-10, label+" vertical crop"
        bpy.data.images.remove(image)
    for name, mats in saved.items():
        for i, mat in enumerate(mats):
            bpy.data.objects[name].data.materials[i] = mat
    scene.camera = bpy.data.objects["Carol_Camera_front_perspective"]


def validate():
    objects = bpy.data.objects
    for name in ("Carol_Model", "Carol_Face_Center", "Carol_Rear_Tuft"):
        assert name in objects, name
    for view in VIEWS:
        assert "Carol_Camera_"+view.replace("-", "_") in objects
    supports = [o.name for o in objects if o.name.startswith("Carol_Support_") and o.type == "MESH"]
    assert len(supports) == 4
    assert not any(o.type == "ARMATURE" for o in objects)
    assert not bpy.data.actions
    assert not any(o.animation_data for o in objects)
    assert not bpy.data.shape_keys
    assert objects["Carol_Rear_Tuft"].parent == objects["Carol_Model"]
    mesh = objects["Carol_Fleece_Continuous"].data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    assert all(e.is_manifold for e in bm.edges), "Fleece must be a closed volume"
    remaining = set(bm.verts)
    components = 0
    while remaining:
        components += 1
        pending = [remaining.pop()]
        while pending:
            for edge in pending.pop().link_edges:
                for vertex in edge.verts:
                    if vertex in remaining:
                        remaining.remove(vertex)
                        pending.append(vertex)
    bm.free()
    assert components == 1, "Fleece must form one connected organism"
    bounds = {}
    for name in ("Carol_Fleece_Continuous", "Carol_Face", "Carol_Rear_Tuft", "Carol_Chassis_Hidden"):
        obj = objects[name]
        points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        bounds[name] = {"min": [min(p[i] for p in points) for i in range(3)],
                        "max": [max(p[i] for p in points) for i in range(3)]}
    return {"supports": supports, "armatures": 0, "actions": 0, "shapeKeys": 0,
            "rearTuftIndependent": True, "fleeceConnectedComponents": components,
            "fleeceClosedVolume": True, "boundsXYZ": bounds,
            "reviewCameras": list(VIEWS), "allRendersUncropped": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend-path", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--pass-number", type=int, choices=(1, 2, 3), default=3)
    parser.add_argument("--width", type=int, default=1400)
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    args.blend_path = args.blend_path.resolve()
    args.evidence_dir = args.evidence_dir.resolve()
    assert bpy.app.version == (5, 2, 1), bpy.app.version_string
    assert args.blend_path.resolve() != V001.resolve(), "v001 is immutable"
    hashes = {"canonical": sha(CANONICAL), "v001": sha(V001)}
    bpy.ops.wm.open_mainfile(filepath=str(V001))
    baseline = {"objectCount": len(bpy.data.objects), "modelExists": "Carol_Model" in bpy.data.objects}
    assert baseline["modelExists"]
    build_scene(args.pass_number)
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    args.blend_path.parent.mkdir(parents=True, exist_ok=True)
    render_evidence(args.evidence_dir, args.width)
    result = validate()
    # Structural part selection is convenient when the Human opens the source.
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects["Carol_Fleece_Continuous"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["Carol_Fleece_Continuous"]
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(args.blend_path))
    # Reopen the actual saved artifact, not only the in-memory scene.
    bpy.ops.wm.open_mainfile(filepath=str(args.blend_path))
    validate()
    assert hashes == {"canonical": sha(CANONICAL), "v001": sha(V001)}
    manifest = {"schema": "grimo.carol.structural-blockout", "version": 2,
                "pass": args.pass_number, "blenderVersion": bpy.app.version_string,
                "baseline": baseline, "preservedHashes": hashes,
                "blendSha256": sha(args.blend_path), "generatorSha256": sha(Path(__file__)),
                "checks": result, "status": "awaiting Human Gate",
                "renders": {v: sha(args.evidence_dir / f"carol-v002-{v}.png") for v in VIEWS}}
    (args.evidence_dir / "validation.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
