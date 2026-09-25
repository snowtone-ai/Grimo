"""Focused head refinement from the immutable Skin v001 candidate.

Run with Blender --background --python this-file [-- --preview].
One shared neutral mesh, no camera-dependent geometry or retouched renders.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/grimo/production/carol/blender/carol-skin-final-v001.blend'
SOURCE_SHA256 = 'fc291fd337d751c9aba025f7d589374da737927e76f271c5c99df3a35994c024'
OUTPUT = SOURCE.with_name('carol-skin-final-v002.blend')
OUT = ROOT / 'docs/production/carol/evidence/skin-final-v002'
SPEC = importlib.util.spec_from_file_location('skin_v001', Path(__file__).with_name('refine-carol-skin-v001.py'))
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
UTIL = BASE.util
PIVOT_Z, LIFT, STRETCH = .45, .027, 1.06
EYE_BAND_EXTRA = .06
CREAM = (.96, .80, .72, 1)
FACE_CREAM = (.96, .82, .74, 1)


def zmap(z):
    def smooth(t):
        t = max(0., min(1., t))
        return t * t * (3 - 2 * t)
    band = smooth((z - .25) / .07) * smooth((.57 - z) / .06)
    return PIVOT_Z + (z - PIVOT_Z) * STRETCH + LIFT + EYE_BAND_EXTRA * (z - .412) * band


def refine_geometry():
    head = bpy.data.objects['CENTRAL_CHASSIS']
    original = [v.co.copy() for v in head.data.vertices]
    for v in head.data.vertices[:351]:
        v.co.z = zmap(v.co.z)
    # Carry the existing short neck attachment halfway with the adjoining head.
    for v in head.data.vertices[351:379]:
        v.co.z += .55 * (zmap(v.co.z) - v.co.z)
    head.data.update()
    for name in ['EYE_L', 'EYE_R', 'EYELID_L', 'EYELID_R', 'NOSE', 'MOUTH_closed', 'PHILTRUM']:
        ob = bpy.data.objects[name]
        # Apply the same spatial field as the head, including the eye band.
        inverse = ob.matrix_world.inverted()
        def mapped(co):
            world = ob.matrix_world @ Vector(co[:3])
            world.z = zmap(world.z)
            return inverse @ world
        if ob.type == 'MESH':
            for v in ob.data.vertices:
                v.co = mapped(v.co)
            ob.data.update()
        else:
            for spline in ob.data.splines:
                for point in spline.points:
                    point.co = (*mapped(point.co), point.co.w)
    ear_lift = zmap(.579) - .579
    for side in ['L', 'R']:
        ear = bpy.data.objects['EAR_' + side]
        ear.location.z += ear_lift
        ear['root_H'] = [.386, .235, .579 + ear_lift]
    for name in ['DEBUG_CHEEK_L', 'DEBUG_CHEEK_R', 'DEBUG_FOREHEAD', 'DEBUG_HEAD_PIVOT']:
        bpy.data.objects[name].location.z = zmap(bpy.data.objects[name].location.z)
    for side, sign in [('L', 1), ('R', -1)]:
        bpy.data.objects['DEBUG_EAR_ROOT_' + side].location = (.386, sign * .235, .579 + ear_lift)
    return original, ear_lift


def refine_materials(move_blush=True):
    body = bpy.data.objects['FORE_L'].data.materials[0]
    body.diffuse_color = CREAM
    shader = body.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = CREAM
    shader.inputs['Emission Color'].default_value = CREAM
    shader.inputs['Emission Strength'].default_value = .16
    shader.inputs['Subsurface Weight'].default_value = .09
    shader.inputs['Specular IOR Level'].default_value = .28
    face = bpy.data.objects['CENTRAL_CHASSIS'].data.materials[1]
    face.diffuse_color = FACE_CREAM
    nodes, links = face.node_tree.nodes, face.node_tree.links
    shader = nodes.get('Principled BSDF')
    mixes = [n for n in nodes if n.type == 'MIX_RGB']
    assert len(mixes) == 2
    # Identify by graph connectivity, independent of Blender's displayed names.
    blend = shader.inputs['Base Color'].links[0].from_node
    blush = blend.inputs[2].links[0].from_node
    blend.inputs[1].default_value = CREAM
    blush.inputs[1].default_value = FACE_CREAM
    blush.inputs[2].default_value = (.96, .36, .29, 1)
    # Remove the old face-only emission boundary at the jaw.
    for link in list(shader.inputs['Emission Strength'].links):
        links.remove(link)
    shader.inputs['Emission Strength'].default_value = .16
    shader.inputs['Subsurface Weight'].default_value = .09
    shader.inputs['Specular IOR Level'].default_value = .28
    for node in nodes if move_blush else []:
        if node.type == 'VECT_MATH' and node.operation == 'SUBTRACT':
            node.inputs[1].default_value[2] = zmap(node.inputs[1].default_value[2])
        elif node.type == 'VECT_MATH' and node.operation == 'DIVIDE':
            node.inputs[1].default_value[2] *= STRETCH + EYE_BAND_EXTRA


def lighting():
    BASE.scene_review()
    scene = bpy.context.scene
    # Broad, neutral environment fill reduces gray shadow bias without an
    # exposure lift that would clip the face. Saved in the production asset.
    scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value = (1.05, 1.05, 1.05, 1)
    for name, energy in [('key', 220), ('fill', 180), ('low fill', 100), ('rim', 170)]:
        bpy.data.objects[name].data.energy = energy


VIEWS = [
    ('front', (-4, 0, 0), (.52, 0, .395), 1.23, (1200, 1050)),
    ('side', (0, -4, 0), (.53, 0, .395), 1.34, (1300, 1050)),
    ('three-quarter', (-3, -3, .50), (.54, 0, .395), 1.33, (1200, 1050)),
    ('rear', (4, 0, .15), (.53, 0, .395), 1.23, (1100, 1000)),
    ('top', (0, 0, 4), (.53, 0, .34), 1.36, (1100, 1000)),
    ('head-front', (-4, 0, 0), (.30, 0, .49), .78, (1100, 1000)),
    ('head-side', (0, -4, 0), (.31, 0, .49), .78, (1100, 1000)),
    ('head-three-quarter', (-3, -3, .35), (.31, 0, .49), .86, (1100, 1000)),
]


def renders(preview=False):
    UTIL.TMP = (ROOT / 'artifacts/carol-head-preview') if preview else OUT / 'renders'
    UTIL.TMP.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.cycles.samples = 16 if preview else 48
    for name, direction, target, scale, size in VIEWS[:3] if preview else VIEWS:
        if preview:
            size = tuple(round(x * .55) for x in size)
        UTIL.render(name, direction, target, scale, size=size)


def bounds(ob):
    points = [ob.matrix_world @ v.co for v in ob.data.vertices]
    return {'min': [min(p[i] for p in points) for i in range(3)],
            'max': [max(p[i] for p in points) for i in range(3)]}


def eye_surface_clearance():
    bpy.context.view_layer.update()
    tree = BVHTree.FromObject(bpy.data.objects['CENTRAL_CHASSIS'], bpy.context.evaluated_depsgraph_get())
    result = {}
    for name in ['EYE_L', 'EYE_R']:
        ob = bpy.data.objects[name]
        distances = []
        for v in ob.data.vertices:
            point = ob.matrix_world @ v.co
            near, normal, _, distance = tree.find_nearest(point)
            distances.append(distance if (point - near).dot(normal) >= 0 else -distance)
        result[name] = {'min_signed_H': min(distances), 'max_signed_H': max(distances)}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--comparison-source', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256, 'Skin v001 source changed; inspect authority and execution state before rebuilding'
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    bpy.context.scene.frame_set(1)
    if args.comparison_source:
        refine_materials(move_blush=False)
        lighting()
        bpy.context.scene.cycles.samples = 48
        UTIL.TMP = OUT / 'matched-source-renders'
        UTIL.TMP.mkdir(parents=True, exist_ok=True)
        for name, direction, target, scale, size in VIEWS[:2]:
            UTIL.render(name, direction, target, scale, size=size)
        return
    before = {o.name: UTIL.snapshot(o) for o in bpy.data.objects}
    eyes_before = {n: bounds(bpy.data.objects[n]) for n in ['EYE_L', 'EYE_R']}
    clearance_before = eye_surface_clearance()
    original, ear_lift = refine_geometry()
    refine_materials()
    lighting()
    if args.preview:
        renders(True)
        return
    OUT.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.cycles.samples = 48
    scene['stage'] = 'SKIN_HEAD_REFINED_CANDIDATE__HUMAN_REVIEW_PENDING'
    scene['selected_candidate'] = 'carol-skin-final-v002'
    scene['source_commit'] = '0d6f26a9554639d780f626d2466c48c23e2d9f06'
    scene['skin_source'] = str(SOURCE.relative_to(ROOT)).replace('\\', '/')
    scene['candidate_role'] = 'Final Skin head refinement candidate; not an approved authority'
    scene['human_geometry_gate'] = 'PENDING_HUMAN_PERCEPTUAL_REVIEW'
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))
    scene = bpy.context.scene
    changed = sorted(n for n, old in before.items() if UTIL.snapshot(bpy.data.objects[n]) != old)
    allowed = {'CENTRAL_CHASSIS', 'EAR_L', 'EAR_R', 'EYE_L', 'EYE_R', 'EYELID_L', 'EYELID_R', 'NOSE', 'MOUTH_closed', 'PHILTRUM', 'DEBUG_CHEEK_L', 'DEBUG_CHEEK_R', 'DEBUG_FOREHEAD', 'DEBUG_HEAD_PIVOT', 'DEBUG_EAR_ROOT_L', 'DEBUG_EAR_ROOT_R'}
    assert set(changed) == allowed, changed
    assert all((v.co - original[v.index]).length == 0 for v in bpy.data.objects['CENTRAL_CHASSIS'].data.vertices[379:])
    for n in ['EAR_L', 'EAR_R']:
        assert UTIL.snapshot(bpy.data.objects[n])['mesh_and_shape_keys'] == before[n]['mesh_and_shape_keys']
    checks = {n: UTIL.mesh_check(bpy.data.objects[n]) for n in ['CENTRAL_CHASSIS', 'EAR_L', 'EAR_R']}
    assert all(c['finite'] and c['outward_normals'] and c['nonmanifold_edges'] == 0 and c['nonadjacent_triangle_intersections'] == 0 for c in checks.values()), checks
    head_tree = BVHTree.FromObject(bpy.data.objects['CENTRAL_CHASSIS'], bpy.context.evaluated_depsgraph_get())
    roots = {}
    for side, sign in [('L', 1), ('R', -1)]:
        root = Vector((.386, sign * .235, .579 + ear_lift))
        nearest, normal, _, distance = head_tree.find_nearest(root)
        roots[side] = {'inside_head': (root - nearest).dot(normal) < 0, 'surface_distance_H': distance}
    assert all(r['inside_head'] for r in roots.values()), roots
    clearance_after = eye_surface_clearance()
    assert all(c['min_signed_H'] >= min(0., clearance_before[n]['min_signed_H']) - .0005
               for n, c in clearance_after.items()), clearance_after
    manifest = json.loads((ROOT / 'assets/grimo/source/carol/approved-3d/authority.json').read_text())
    hashes = {}
    for entry in manifest['authorityOrder']:
        p = ROOT / entry['path']
        raw = p.read_bytes()
        if p.suffix == '.md':
            raw = raw.replace(b'\r\n', b'\n')
        hashes[entry['path']] = hashlib.sha256(raw).hexdigest()
        assert hashes[entry['path']] == entry['sha256'].lower()
    packed = [im for im in bpy.data.images if im.name.startswith('eye-authority-pigment')]
    assert len(packed) == 1 and packed[0].packed_file
    report = {'source_commit': scene['source_commit'], 'source_asset': str(SOURCE.relative_to(ROOT)).replace('\\', '/'),
              'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'saved_asset_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
              'head_vertical_scale': STRETCH, 'head_pivot_Z_H': PIVOT_Z, 'head_lift_H': LIFT,
              'eye_band_additional_vertical_scale': EYE_BAND_EXTRA,
              'ear_rigid_lift_H': ear_lift, 'ear_meshes_unchanged': True,
              'torso_controls_379_onward_unchanged': True, 'limbs_hooves_tail_geometry_unchanged': True,
              'eye_bounds_before': eyes_before, 'eye_bounds_after': {n: bounds(bpy.data.objects[n]) for n in eyes_before},
              'eye_surface_clearance_before': clearance_before, 'eye_surface_clearance_after': clearance_after,
              'body_linear_rgba': CREAM, 'face_linear_rgba': FACE_CREAM, 'skin_emission_strength': .16,
              'world_gray_linear': 1.05, 'exposure_unchanged': -1.2,
              'studio_light_watts': {'key': 220, 'fill': 180, 'low fill': 100, 'rim': 170},
              'changed_objects': changed, 'mesh_checks': checks, 'ear_root_checks': roots, 'authority_hashes': hashes,
              'packed_eye_pigment': True, 'save_reload_validated': True, 'human_skin_approval': 'PENDING'}
    (OUT / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    renders()
    print('HEAD_REFINEMENT_VALIDATED', json.dumps(report))


if __name__ == '__main__':
    main()
