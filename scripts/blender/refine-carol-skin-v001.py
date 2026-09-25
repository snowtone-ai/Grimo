"""Final Skin geometry refinement on the latest face/ear authority-fit candidate.

All changes are made to the neutral 3D mesh, independent of the review camera.
The source .blend and all approved references are read-only inputs.
"""
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/grimo/production/carol/blender/carol-face-ear-authority-match-v001.blend'
OUTPUT = SOURCE.with_name('carol-skin-final-v001.blend')
EVIDENCE = ROOT / 'docs/production/carol/evidence/skin-final-v001'
EVIDENCE.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location(
    'carol_ear_util', Path(__file__).with_name('build-carol-ear-production-v002.py'))
util = importlib.util.module_from_spec(spec)
spec.loader.exec_module(util)
util.TMP = EVIDENCE / 'renders'
util.TMP.mkdir(parents=True, exist_ok=True)


def soften_profile():
    """Advance the upper forehead to form the approved short-muzzle turn.

    The source face's lower muzzle already reaches the Side reference. The
    upper forehead sits behind it; moving that surface forward creates the
    characteristic turn while holding nose, chin, and lateral silhouette.
    """
    head = bpy.data.objects['CENTRAL_CHASSIS']
    before = [v.co.copy() for v in head.data.vertices]
    maximum = 0.0
    for v in head.data.vertices[:351]:
        x, y, z = v.co
        frontal = max(0.0, min(1.0, (.27 - x) / .16))
        # Keep the established eye sockets clear on either side of the bridge.
        lateral = math.exp(-(abs(y) / .08) ** 4)
        lower = max(0.0, min(1.0, (z - .39) / .13))
        upper = max(0.0, min(1.0, (.68 - z) / .055))
        lower = lower * lower * (3 - 2 * lower)
        upper = upper * upper * (3 - 2 * upper)
        delta = .025 * frontal * lateral * lower * upper
        v.co.x -= delta
        maximum = max(maximum, delta)
    head.data.update()
    return before, maximum


def blend_neck_and_chest():
    """Ease the narrow dorsal neck seam and tuck the flat ventral chest cap."""
    head = bpy.data.objects['CENTRAL_CHASSIS']
    for v in head.data.vertices[351:379]:
        # This strip connects the reconstructed head to the chest. Widening it
        # retains the head/body topology while removing the top-view V pinch.
        v.co.y *= 1.11
        upper = max(0.0, min(1.0, (v.co.z - .26) / .15))
        v.co.z += .012 * upper
    for v in head.data.vertices[379:407]:
        medial = max(0.0, 1 - abs(v.co.y) / .16)
        low = max(0.0, min(1.0, (.23 - v.co.z) / .12))
        v.co.x += .016 * medial * low
    for v in head.data.vertices[428:437]:
        v.co.x += .036
    for v in head.data.vertices[379:437]:
        # Draw the lowest chest patch into the body so it reads as one soft
        # underbody arch in Front instead of a small projecting bib.
        v.co.x += .020 * max(0.0, min(1.0, (.49 - v.co.x) / .17))
    head.data.update()


FORE = [
    (.052, .008, .000, .040, .045),
    (.118, .006, .000, .073, .077),
    (.177, .007, .007, .094, .093),
    (.239, .012, .018, .119, .107),
    (.302, .018, .030, .136, .113),
    (.362, .026, .045, .112, .095),
    (.405, .032, .057, .075, .070),
]
HIND = [
    (.052, .008, .000, .040, .045),
    (.118, .004, .003, .074, .074),
    (.181, -.012, .018, .107, .094),
    (.249, -.033, .050, .137, .112),
    (.312, -.043, .071, .143, .118),
    (.365, -.051, .090, .109, .090),
    (.403, -.055, .100, .071, .065),
]


def round_limbs():
    for row, stations, center_x, center_y in [('FORE', FORE, .390, .145),
                                                ('HIND', HIND, .920, .200)]:
        for side, sign in [('L', 1), ('R', -1)]:
            ob = bpy.data.objects[row + '_' + side]
            assert len(ob.data.vertices) == len(stations) * 16
            for k, (z, dx, inward, rx, ry) in enumerate(stations):
                for j in range(16):
                    theta = math.tau * j / 16
                    ob.data.vertices[k * 16 + j].co = (
                        center_x + dx + rx * math.cos(theta),
                        sign * center_y - sign * inward + .90 * ry * math.sin(theta), z)
            ob.data.update()


def round_hoof_crowns():
    """Round the planted toe profile without changing the three-toe layout."""
    rings = [(0, .70, .78), (.006, .81, .89), (.018, .94, .98),
             (.040, 1, 1), (.066, .96, .97), (.087, .83, .87),
             (.101, .67, .73), (.111, .48, .54), (.112, .04, .04)]
    for row, center_x, center_y in [('FORE', .390, .145), ('HIND', .920, .200)]:
        for side, sign in [('L', 1), ('R', -1)]:
            ob = bpy.data.objects['HOOF_' + row + '_' + side]
            assert len(ob.data.vertices) == 864
            for k, (z, sx, sy) in enumerate(rings):
                for j in range(96):
                    theta = math.tau * j / 96
                    c = math.cos(theta)
                    yy = .1095 * math.sin(theta) * sy
                    xx = (.075 if c < 0 else .076) * c * sx
                    frontness = max(0, -c) ** 1.25
                    lobe = .5 + .5 * math.cos(math.tau * yy / .073)
                    rise = max(0, min(1, (z - .008) / .016))
                    fall = max(0, min(1, (.088 - z) / .025))
                    rise = rise * rise * (3 - 2 * rise)
                    fall = fall * fall * (3 - 2 * fall)
                    crown = frontness * rise * fall
                    xx -= .029 * lobe * crown
                    zz = z - .004 * (1 - lobe) * crown
                    ob.data.vertices[k * 96 + j].co = (
                        center_x + .70 * xx, sign * center_y + .55 * yy,
                        .70 * zz)
            ob.data.update()
            bm = bmesh.new()
            bm.from_mesh(ob.data)
            # The inherited hoof winding points inward despite a closed sole.
            # Correct it while retaining the three distal lobes and topology.
            bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
            bm.to_mesh(ob.data)
            bm.free()


def warm_underbody():
    # The inherited neutral studio material renders the body gray against the
    # approved warm Skin painting. Keep a single cream material across torso
    # and all four limbs so the actual form is easier to judge.
    skin = bpy.data.objects['FORE_L'].data.materials[0]
    assert skin is bpy.data.objects['CENTRAL_CHASSIS'].data.materials[0]
    skin.diffuse_color = (.94, .68, .63, 1)
    skin.use_nodes = True
    shader = skin.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (.94, .68, .63, 1)
    shader.inputs['Roughness'].default_value = .73
    shader.inputs['Subsurface Weight'].default_value = .09
    return skin.name


def scene_review():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 12
    scene.render.use_compositing = False
    scene.render.use_sequencer = False
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.view_settings.exposure = -1.2
    scene.view_settings.gamma = 1


def render_all():
    scene_review()
    # These absolute cameras see the complete Skin geometry, including hooves.
    for name, direction, target, scale, size in [
        ('front', (-4, 0, 0), (.52, 0, .395), 1.23, (1200, 1050)),
        ('side', (0, -4, 0), (.53, 0, .395), 1.34, (1300, 1050)),
        ('three-quarter', (-3, -3, .50), (.54, 0, .395), 1.33, (1200, 1050)),
        ('rear', (4, 0, .15), (.53, 0, .395), 1.23, (1100, 1000)),
        ('top', (0, 0, 4), (.53, 0, .34), 1.36, (1100, 1000)),
    ]:
        util.render(name, direction, target, scale, size=size)
    visible = {'CENTRAL_CHASSIS', 'EYE_L', 'EYE_R', 'EYELID_L', 'EYELID_R',
               'NOSE', 'MOUTH_closed', 'PHILTRUM'}
    for name, direction in [('front', (-4, 0, 0)), ('side', (0, -4, 0)),
                            ('three-quarter', (-3, -3, .35))]:
        util.render('face-' + name, direction, (.30, 0, .45), .64,
                    visible=visible, size=(950, 950))


def main():
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    bpy.context.scene.frame_set(1)
    original = {o.name: util.snapshot(o) for o in bpy.data.objects}
    before, delta = soften_profile()
    blend_neck_and_chest()
    round_limbs()
    round_hoof_crowns()
    skin_material = warm_underbody()
    scene_review()
    bpy.context.scene['stage'] = 'SKIN_FINAL_CANDIDATE__HUMAN_REVIEW_PENDING'
    bpy.context.scene['skin_source'] = str(SOURCE.relative_to(ROOT)).replace('\\', '/')
    bpy.context.scene['skin_authority'] = 'assets/grimo/source/carol/approved-3d/authority.json'
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))
    changed = sorted(n for n, prior in original.items()
                     if util.snapshot(bpy.data.objects[n]) != prior)
    expected = {'CENTRAL_CHASSIS', 'FORE_L', 'FORE_R', 'HIND_L', 'HIND_R',
                'HOOF_FORE_L', 'HOOF_FORE_R', 'HOOF_HIND_L', 'HOOF_HIND_R'}
    assert set(changed) == expected, changed
    checks = {n: util.mesh_check(bpy.data.objects[n]) for n in expected}
    assert all(c['finite'] and c['outward_normals'] and
               c['nonmanifold_edges'] == 0 and
               c['nonadjacent_triangle_intersections'] == 0
               for c in checks.values()), checks
    assert all((bpy.data.objects['CENTRAL_CHASSIS'].data.vertices[i].co - before[i]).length < 1e-7
               for i in range(437, len(before)))
    authority = json.loads((ROOT / 'assets/grimo/source/carol/approved-3d/authority.json').read_text())
    hashes = {}
    for ref in authority['authorityOrder']:
        path = ROOT / ref['path']
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        assert digest == ref['sha256'].upper(), ref['path']
        hashes[ref['path']] = digest
    validation = {'source': str(SOURCE.relative_to(ROOT)).replace('\\', '/'),
                  'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  'saved_asset_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  'changed_geometry_objects': changed,
                  'max_forehead_advance_H': delta,
                  'underbody_material': skin_material,
                  'rear_body_control_vertices_unchanged': True,
                  'mesh_checks': checks, 'authority_hashes': hashes,
                  'human_skin_approval': 'PENDING'}
    (EVIDENCE / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
    render_all()
    print('SKIN_FINAL_VALIDATION', json.dumps(validation))


if __name__ == '__main__':
    main()
