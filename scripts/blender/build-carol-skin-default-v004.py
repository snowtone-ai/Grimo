"""Build the v004 Carol Skin default from the hash-pinned v003 asset only."""
import hashlib
import json
import math
import struct
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'assets/grimo/production/carol/blender'
SOURCE = ASSETS / 'carol-skin-default-v003.blend'
FLEECE_SOURCE = ASSETS / 'carol-normal-fleece-v004.blend'
V002_SOURCE = ASSETS / 'carol-skin-final-v002.blend'
OUTPUT = ASSETS / 'carol-skin-default-v004.blend'
EVIDENCE = ROOT / 'docs/production/carol/evidence/skin-default-v004'

EXPECTED = {
    'v003': '4f4661b672f8b2022ca819241c0624f36693e36505775736042fe821b703915a',
    'fleece_v004': 'a73426d8483e5431e60bc5949b96506c447928682ad92ead6af3cbd1d1092420',
    'skin_v002': '321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a',
}
SKIN_MESHES = {
    'CENTRAL_CHASSIS', 'EAR_L', 'EAR_R', 'EYELID_L', 'EYELID_R',
    'EYE_L', 'EYE_R', 'FORE_L', 'FORE_R', 'HIND_L', 'HIND_R',
    'HOOF_FORE_L', 'HOOF_FORE_R', 'HOOF_HIND_L', 'HOOF_HIND_R',
    'NOSE', 'SKIN_TAIL_CORE',
}
SKIN_CURVES = {'MOUTH_closed', 'PHILTRUM'}
SKIN_EMPTIES = {'TAIL_PIVOT', 'PIGMENT_SPACE'}
RETAINED = SKIN_MESHES | SKIN_CURVES | SKIN_EMPTIES
EARS = {'EAR_L', 'EAR_R'}
RING_SIZE = 24
STATION_COUNT = 95
# One bounded Pass-B adjustment after the Pass-A render: reduce the fullness
# and droop coefficients by at most 25% (the stated .075/.050 fullness fallback
# applies after the combined field exceeded the per-vertex displacement limit).
PASS_B = {
    'vertical_mid': .075,
    'vertical_distal': .050,
    'vertical_tip_end': -.010,
    'center_mid': -.004875,
    'center_distal': -.0030,
    'center_tip_recovery': .001125,
    'lower_rim': -.00225,
    'depth_mid': .009,
    'depth_tip': -.025,
    'du': -.0030,
    'trough_recess': .0055,
}
DISPLACEMENT_CAP = .0199


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def smooth(a, b, t):
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    q = (t - a) / (b - a)
    return q * q * (3.0 - 2.0 * q)


def smooth_cap(magnitude):
    """C1-smooth compliance cap; unchanged below .018 H, bounded at .0199 H."""
    low = .018
    high = DISPLACEMENT_CAP
    if magnitude <= low:
        return magnitude
    if magnitude >= high:
        return high
    q = (magnitude - low) / (high - low)
    # Cubic Hermite: slope 1 at low, slope 0 at high.
    return low + (high - low) * (q + q * q - q * q * q)


def snapshot(ob):
    """Match the v003 retention snapshot for all non-ear Skin structures."""
    h = hashlib.sha256()
    if ob.type == 'MESH':
        for v in ob.data.vertices:
            h.update(struct.pack('<3f', *v.co))
        for p in ob.data.polygons:
            h.update(struct.pack('<II', len(p.vertices), p.material_index))
            for i in p.vertices:
                h.update(struct.pack('<I', i))
        for attr in ob.data.attributes:
            h.update((attr.name + attr.data_type + attr.domain).encode())
            for item in attr.data:
                for field in ('value', 'vector', 'color', 'byte_color', 'uv'):
                    if hasattr(item, field):
                        value = getattr(item, field)
                        if hasattr(value, '__iter__') and not isinstance(value, str):
                            value = tuple(value)
                        h.update(repr(value).encode())
                        break
        if ob.data.shape_keys:
            for key in ob.data.shape_keys.key_blocks:
                h.update(key.name.encode())
                for v in key.data:
                    h.update(struct.pack('<3f', *v.co))
    else:
        for spline in ob.data.splines if ob.type == 'CURVE' else []:
            for p in spline.bezier_points:
                for co in (p.co, p.handle_left, p.handle_right):
                    h.update(struct.pack('<3f', *co))
    return {
        'data': h.hexdigest(),
        'matrix': [round(x, 8) for row in ob.matrix_world for x in row],
        'parent': ob.parent.name if ob.parent else None,
        'materials': [m.name for m in ob.data.materials] if ob.type == 'MESH' else [],
        'modifiers': [(m.name, m.type) for m in ob.modifiers],
    }


def material_state(names):
    """Capture non-ear and ear shader topology plus all socket defaults."""
    materials = {
        mat for name in names
        for mat in (bpy.data.objects[name].data.materials if bpy.data.objects[name].type == 'MESH' else [])
        if mat
    }
    result = {}
    for material in materials:
        nodes = []
        links = []
        if material.use_nodes:
            for node in material.node_tree.nodes:
                sockets = []
                for direction, collection in (('in', node.inputs), ('out', node.outputs)):
                    for index, socket in enumerate(collection):
                        value = getattr(socket, 'default_value', None)
                        if hasattr(value, '__iter__') and not isinstance(value, str):
                            value = tuple(round(float(x), 8) for x in value)
                        elif isinstance(value, (int, float)):
                            value = round(float(value), 8)
                        elif value is not None:
                            value = str(value)
                        sockets.append((direction, index, socket.name, socket.identifier, value))
                props = []
                for key in ('operation', 'blend_type', 'data_type', 'attribute_name', 'label', 'mute'):
                    if hasattr(node, key):
                        value = getattr(node, key)
                        if isinstance(value, (str, int, float, bool)):
                            props.append((key, value))
                nodes.append((node.name, node.bl_idname, tuple(sockets), tuple(props)))
            links = sorted((l.from_node.name, l.from_socket.name, l.to_node.name, l.to_socket.name)
                           for l in material.node_tree.links)
        result[material.name] = {
            'use_nodes': material.use_nodes,
            'nodes': sorted(nodes),
            'links': links,
        }
    return result


def topology_state(ob):
    mesh = ob.data
    return {
        'vertices': len(mesh.vertices),
        'edges': [tuple(e.vertices) for e in mesh.edges],
        'polygons': [tuple(p.vertices) for p in mesh.polygons],
        'material_indices': [p.material_index for p in mesh.polygons],
    }


def root_check(name):
    ear = bpy.data.objects[name]
    tree = BVHTree.FromObject(
        bpy.data.objects['CENTRAL_CHASSIS'], bpy.context.evaluated_depsgraph_get())
    ring = ear.data.vertices[:RING_SIZE]
    center = sum((ear.matrix_world @ v.co for v in ring), Vector()) / RING_SIZE
    hit, normal, _, distance = tree.find_nearest(center)
    return {'inside_head': (center - hit).dot(normal) < 0.0, 'surface_distance_H': distance}


def ear_field(t):
    free = smooth(.28, .38, t)
    mid = smooth(.30, .48, t) * (1.0 - smooth(.72, .86, t))
    distal = smooth(.62, .78, t) * (1.0 - smooth(.92, .985, t))
    tip = smooth(.80, .96, t)
    tip_end = smooth(.94, 1.00, t)
    long_shorten = smooth(.72, .96, t)
    vertical_scale = 1.0 + free * (
        PASS_B['vertical_mid'] * mid + PASS_B['vertical_distal'] * distal
        + PASS_B['vertical_tip_end'] * tip_end)
    dz_center = free * (
        PASS_B['center_mid'] * mid + PASS_B['center_distal'] * distal
        + PASS_B['center_tip_recovery'] * tip_end)
    depth_scale = 1.0 + free * (PASS_B['depth_mid'] * mid + PASS_B['depth_tip'] * tip)
    du = PASS_B['du'] * free * long_shorten
    longitudinal_pink = smooth(.04, .20, t) * (1.0 - smooth(.75, 1.03, t))
    return vertical_scale, dz_center, depth_scale, du, longitudinal_pink, free, mid


def refine(ob, sign):
    assert len(ob.data.vertices) == STATION_COUNT * RING_SIZE
    assert not ob.data.shape_keys
    attr = ob.data.attributes.get('SoftInnerBowl')
    assert attr and attr.data_type == 'FLOAT' and attr.domain == 'POINT'
    c, s = math.cos(math.radians(35.0)), math.sin(math.radians(35.0))
    original = [v.co.copy() for v in ob.data.vertices]
    maximum_center_drop = 0.0
    largest_vertex = None

    proximal_cross = {
        10: .10, 11: .40, 12: .78, 13: 1., 14: 1., 15: 1.,
        16: .88, 17: .58, 18: .38, 19: .21, 20: .08, 21: .02,
    }
    distal_cross = {
        7: .03, 8: .24, 9: .64, 10: .90, 11: 1., 12: 1.,
        13: .95, 14: .82, 15: .65, 16: .44, 17: .25, 18: .08,
    }

    for start in range(0, len(ob.data.vertices), RING_SIZE):
        ring = ob.data.vertices[start:start + RING_SIZE]
        local = [Vector((
            (v.co.x - .386) * c - (sign * v.co.y - .235) * s,
            (v.co.x - .386) * s + (sign * v.co.y - .235) * c,
            v.co.z - .579,
        )) for v in ring]
        u = sum(p.y for p in local) / RING_SIZE
        t = max(0.0, min(1.0, (u + .0202) / .435))
        vertical_scale, dz_center, depth_scale, du, longitudinal_pink, free, mid = ear_field(t)
        mid_z = (local[0].z + local[8].z) * .5
        center_x = sum(p.x for p in local) / RING_SIZE
        section_half_height = max(abs(p.z - mid_z) for p in local)
        pigment_root = smooth(.04, .20, t)

        for j, (vertex, p) in enumerate(zip(ring, local)):
            lower_weight = max(0.0, min(1.0,
                (mid_z - p.z) / max(section_half_height, 1e-8)))
            dz_lower = PASS_B['lower_rim'] * free * mid * lower_weight
            local_x = center_x + (p.x - center_x) * depth_scale
            dz_full = (p.z - mid_z) * (vertical_scale - 1.0)
            dz_total = dz_full + dz_center + dz_lower
            local_z = p.z + dz_total
            new_u = p.y + du

            proximal = proximal_cross.get(j, 0.0)
            distal = distal_cross.get(j, 0.0)
            shift = smooth(.50, .84, t)
            cross = proximal * (1.0 - shift) + distal * shift
            local_x += PASS_B['trough_recess'] * cross * longitudinal_pink
            local_delta_x = local_x - p.x
            local_delta_u = du
            distance = math.sqrt(local_delta_x ** 2 + dz_total ** 2 + local_delta_u ** 2)
            capped = smooth_cap(distance)
            if distance > 0.0:
                compliance = capped / distance
                local_delta_x *= compliance
                dz_total *= compliance
                local_delta_u *= compliance
            local_x = p.x + local_delta_x
            local_z = p.z + dz_total
            new_u = p.y + local_delta_u
            if largest_vertex is None or distance > largest_vertex['displacement_H']:
                largest_vertex = {
                    'station': start // RING_SIZE, 'ring_vertex': j, 't': t,
                    'raw_displacement_H': distance, 'displacement_H': capped,
                    'depth_delta_H': local_delta_x,
                    'vertical_fullness_delta_H': dz_full,
                    'centerline_delta_H': dz_center, 'lower_rim_delta_H': dz_lower,
                    'longitudinal_delta_H': du,
                }

            end = .995 - .035 * min(1.0, abs(j - 11.5) / 5.0) ** 1.5
            pigment = cross * pigment_root * (1.0 - smooth(end - .19, end, t))
            attr.data[vertex.index].value = pigment

            vertex.co = (
                .386 + local_x * c + new_u * s,
                sign * (.235 - local_x * s + new_u * c),
                .579 + local_z,
            )
        maximum_center_drop = max(maximum_center_drop, max(0.0, -dz_center))

    ob.data.update()
    distances = [(v.co - before).length for v, before in zip(ob.data.vertices, original)]
    return {
        'max_displacement_H': max(distances),
        'mean_displacement_H': sum(distances) / len(distances),
        'centerline_downward_offset_max_H': maximum_center_drop,
        'max_displacement_location': largest_vertex,
    }


def base_mesh_volume(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    result = abs(bm.calc_volume(signed=True))
    bm.free()
    return result


def evaluated_volume(ob):
    evaluated = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    result = abs(bm.calc_volume(signed=True))
    bm.free()
    evaluated.to_mesh_clear()
    return result


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    before_sha = {
        'v003': sha(SOURCE),
        'fleece_v004': sha(FLEECE_SOURCE),
        'skin_v002': sha(V002_SOURCE),
    }
    assert before_sha == EXPECTED, before_sha

    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    assert RETAINED <= set(bpy.data.objects.keys())
    non_ear_names = RETAINED - EARS
    baseline = {n: snapshot(bpy.data.objects[n]) for n in sorted(non_ear_names)}
    baseline_materials = material_state(non_ear_names)
    ear_materials = material_state(EARS)
    baseline_topology = {n: topology_state(bpy.data.objects[n]) for n in sorted(EARS)}
    assert len(baseline) == 19

    displacement = {}
    for name, sign in (('EAR_L', 1), ('EAR_R', -1)):
        displacement[name] = refine(bpy.data.objects[name], sign)

    print('PRE_SAVE_DISPLACEMENT', json.dumps(displacement, sort_keys=True), flush=True)
    assert max(v['max_displacement_H'] for v in displacement.values()) <= .020
    assert max(v['mean_displacement_H'] for v in displacement.values()) <= .006
    assert max(v['centerline_downward_offset_max_H'] for v in displacement.values()) <= .012
    assert {n: topology_state(bpy.data.objects[n]) for n in sorted(EARS)} == baseline_topology

    base_volumes = {n: base_mesh_volume(bpy.data.objects[n]) for n in sorted(EARS)}
    assert all(.0110 <= v <= .0121 for v in base_volumes.values()), base_volumes
    roots = {n: root_check(n) for n in sorted(EARS)}
    assert all(r['inside_head'] and .047 <= r['surface_distance_H'] <= .059 for r in roots.values()), roots

    scene = bpy.context.scene
    scene['skin_default_source'] = SOURCE.name
    scene['default_baseline'] = 'PROMOTED'
    scene['ear_visual_human_review'] = 'PENDING'
    scene['phase1_state'] = 'SKIN_DEFAULT_V004_HUMAN_EAR_REVIEW_PENDING'
    scene['ear_refinement'] = 'distributed section fullness, centerline droop, lower-rim arc, distal taper and trough continuation'
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))

    after = {n: snapshot(bpy.data.objects[n]) for n in sorted(non_ear_names)}
    assert baseline == after, [n for n in baseline if baseline[n] != after[n]]
    assert baseline_materials == material_state(non_ear_names)
    assert ear_materials == material_state(EARS)
    assert {n: topology_state(bpy.data.objects[n]) for n in sorted(EARS)} == baseline_topology
    evaluated_volumes = {n: evaluated_volume(bpy.data.objects[n]) for n in sorted(EARS)}
    assert all(.0110 <= v <= .0121 for v in evaluated_volumes.values()), evaluated_volumes
    visible_geometry = {o.name for o in bpy.context.scene.objects if o.type in {'MESH', 'CURVE'}}
    assert visible_geometry == SKIN_MESHES | SKIN_CURVES, sorted(visible_geometry)
    after_sha = {
        'v003': sha(SOURCE),
        'fleece_v004': sha(FLEECE_SOURCE),
        'skin_v002': sha(V002_SOURCE),
    }
    assert after_sha == before_sha == EXPECTED

    report = {
        'source': SOURCE.relative_to(ROOT).as_posix(),
        'source_sha256': before_sha['v003'],
        'output': OUTPUT.relative_to(ROOT).as_posix(),
        'output_sha256': sha(OUTPUT),
        'saved_reopened': True,
        'non_ear_objects': len(baseline),
        'non_ear_differences': [],
        'non_ear_material_node_trees_identical': True,
        'ear_material_node_trees_identical': True,
        'topology_unchanged': True,
        'base_mesh_volumes_H3': base_volumes,
        'evaluated_volumes_H3': evaluated_volumes,
        'root_checks': roots,
        'displacement_vs_v003': displacement,
        'source_sha256_unchanged': after_sha,
        'default_baseline': 'PROMOTED',
        'ear_visual_human_review': 'PENDING',
    }
    (EVIDENCE / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('SKIN_DEFAULT_V004_BUILT', json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
