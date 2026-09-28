"""Validate the reopened v004 Skin against v003, authority, and hard guards."""
import importlib.util
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'skin_builder_v004', HERE / 'build-carol-skin-default-v004.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
spec = importlib.util.spec_from_file_location(
    'ear_util', HERE / 'build-carol-ear-production-v002.py')
util = importlib.util.module_from_spec(spec)
spec.loader.exec_module(util)


def scene_state():
    names = builder.RETAINED - builder.EARS
    return {
        'non_ear': {n: builder.snapshot(bpy.data.objects[n]) for n in sorted(names)},
        'non_ear_materials': builder.material_state(names),
        'ear_materials': builder.material_state(builder.EARS),
        'topology': {n: builder.topology_state(bpy.data.objects[n]) for n in sorted(builder.EARS)},
        'ear_coords': {n: [v.co.copy() for v in bpy.data.objects[n].data.vertices]
                       for n in sorted(builder.EARS)},
    }


def root_check(name):
    ear = bpy.data.objects[name]
    tree = BVHTree.FromObject(
        bpy.data.objects['CENTRAL_CHASSIS'], bpy.context.evaluated_depsgraph_get())
    ring = ear.data.vertices[:builder.RING_SIZE]
    center = sum((ear.matrix_world @ v.co for v in ring), Vector()) / builder.RING_SIZE
    hit, normal, _, distance = tree.find_nearest(center)
    return {'inside_head': (center - hit).dot(normal) < 0.0, 'surface_distance_H': distance}


def main():
    paths = {
        'v003': builder.SOURCE,
        'fleece_v004': builder.FLEECE_SOURCE,
        'skin_v002': builder.V002_SOURCE,
    }
    before_sha = {name: builder.sha(path) for name, path in paths.items()}
    assert before_sha == builder.EXPECTED, before_sha

    bpy.ops.wm.open_mainfile(filepath=str(builder.SOURCE))
    source = scene_state()
    source_hash = before_sha['v003']
    bpy.ops.wm.open_mainfile(filepath=str(builder.OUTPUT))
    target = scene_state()

    non_ear_differences = [n for n in source['non_ear']
                           if source['non_ear'][n] != target['non_ear'][n]]
    assert not non_ear_differences, non_ear_differences
    assert source['non_ear_materials'] == target['non_ear_materials']
    assert source['ear_materials'] == target['ear_materials']
    assert source['topology'] == target['topology']
    assert len(source['non_ear']) == 19

    ears = {n: bpy.data.objects[n] for n in sorted(builder.EARS)}
    checks = {n: util.mesh_check(ob) for n, ob in ears.items()}
    roots = {n: root_check(n) for n in ears}
    displacement = {}
    for name, ob in ears.items():
        source_coords = source['ear_coords'][name]
        distances = [(v.co - initial).length for v, initial in zip(ob.data.vertices, source_coords)]
        displacement[name] = {
            'max_H': max(distances),
            'mean_H': sum(distances) / len(distances),
        }

    left, right = ears['EAR_L'], ears['EAR_R']
    mirror_error = max((Vector((a.co.x, -a.co.y, a.co.z)) - b.co).length
                       for a, b in zip(left.data.vertices, right.data.vertices))
    finite = all(math.isfinite(value) for name in builder.SKIN_MESHES
                 for vertex in bpy.data.objects[name].data.vertices for value in vertex.co)
    visible_geometry = {o.name for o in bpy.context.scene.objects if o.type in {'MESH', 'CURVE'}}
    exact_skin_subset = visible_geometry == builder.SKIN_MESHES | builder.SKIN_CURVES

    pigment = {}
    for name, ob in ears.items():
        attr = ob.data.attributes.get('SoftInnerBowl')
        assert attr and attr.data_type == 'FLOAT' and attr.domain == 'POINT'
        values = [item.value for item in attr.data]
        outer_indices = [j for j in range(builder.RING_SIZE) if j <= 6 or j >= 22]
        outer_values = [values[station * builder.RING_SIZE + j]
                        for station in range(builder.STATION_COUNT) for j in outer_indices]
        tip_values = values[-builder.RING_SIZE:]
        pigment[name] = {
            'single_mesh_attribute': True,
            'max_value': max(values),
            'outer_brown_perimeter_max': max(outer_values),
            'distal_tip_max': max(tip_values),
        }

    after_sha = {name: builder.sha(path) for name, path in paths.items()}
    report = {
        'asset': builder.OUTPUT.relative_to(builder.ROOT).as_posix(),
        'asset_sha256': builder.sha(builder.OUTPUT),
        'saved_reopened': True,
        'default_baseline': bpy.context.scene.get('default_baseline'),
        'ear_visual_human_review': bpy.context.scene.get('ear_visual_human_review'),
        'non_ear_skin_objects_identical_to_v003': len(source['non_ear']),
        'non_ear_differences': non_ear_differences,
        'non_ear_material_node_trees_identical_to_v003': True,
        'ear_material_node_trees_identical_to_v003': True,
        'ear_topology_unchanged_from_v003': True,
        'base_vertices_per_ear': {n: len(ob.data.vertices) for n, ob in ears.items()},
        'station_structure': {'stations': builder.STATION_COUNT, 'vertices_per_station': builder.RING_SIZE},
        'ear_checks': checks,
        'root_checks': roots,
        'bilateral_max_mirror_error_H': mirror_error,
        'displacement_vs_v003': displacement,
        'finite_skin_geometry': finite,
        'visible_geometry_exact_skin_subset': exact_skin_subset,
        'pigment_checks': pigment,
        'source_sha256_unchanged': after_sha == before_sha == builder.EXPECTED,
        'source_sha256': after_sha,
    }

    assert report['saved_reopened']
    assert report['non_ear_skin_objects_identical_to_v003'] == 19
    assert report['non_ear_differences'] == []
    assert report['default_baseline'] == 'PROMOTED'
    assert report['ear_visual_human_review'] == 'PENDING'
    assert report['ear_topology_unchanged_from_v003']
    assert all(count == builder.STATION_COUNT * builder.RING_SIZE
               for count in report['base_vertices_per_ear'].values())
    assert report['bilateral_max_mirror_error_H'] < 1e-6
    assert report['finite_skin_geometry'] and report['visible_geometry_exact_skin_subset']
    assert report['source_sha256_unchanged']
    assert all(c['finite'] and c['nonmanifold_edges'] == 0
               and c['nonadjacent_triangle_intersections'] == 0 and c['outward_normals']
               for c in checks.values())
    assert all(r['inside_head'] and .047 <= r['surface_distance_H'] <= .059
               for r in roots.values())
    assert all(.0110 <= c['volume_H3'] <= .0121 for c in checks.values())
    assert all(v['max_H'] <= .020 and v['mean_H'] <= .006 for v in displacement.values())
    assert all(v['outer_brown_perimeter_max'] <= 1e-6 and v['distal_tip_max'] <= 1e-6
               for v in pigment.values())

    report['technical_checks_pass'] = True
    out = builder.EVIDENCE / 'validation.json'
    out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('SKIN_DEFAULT_V004_VALIDATED', json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
