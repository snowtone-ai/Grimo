"""Bounded Carol v012 Phase A probes from the immutable v011 diagnostic blend.

Run in background Blender with -- --transition 1|2 --ocular 0|1|2 --render side,3q.
Ocular 0 retains the v011 eye for a transition-only probe. Ocular 1 uses an
anatomical-axis cap with a conformal outer rim. Ocular 2 adds a tiny local
X-only socket seat and follows it with the existing lid rings. No source file
is overwritten.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/grimo/production/carol/blender/carol-v011.blend'
TEMP = ROOT / 'tmp-carol-v012'
EVIDENCE = ROOT / 'docs/production/carol/evidence/reconstruction-v012'
ASSET = SOURCE.with_name('carol-v012.blend')
SOURCE_HEAD = 'e95654fae3dc8434cbe651e7d6467aafe59dc667'
SOURCE_SHA = '568fb4378b6ca3093ba5134d8d082f37a6723c9d5b5cf0b491a7c8e5f757aed3'
spec = importlib.util.spec_from_file_location('v011', Path(__file__).with_name('build-carol-v011.py'))
v11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v11)
v10, v8 = v11.v10, v11.v8


def smooth(a, b, x):
    t = min(1.0, max(0.0, (x-a)/(b-a)))
    return t*t*(3-2*t)


def transition(ob, magnitude):
    """Compress only the posterior ventral head/short neck/anterior chest in X."""
    before = [v.co.copy() for v in ob.data.vertices]
    for vertex in ob.data.vertices:
        x, _, z = vertex.co
        posterior = smooth(.205, .345, x) * (1-smooth(.46, .575, x))
        low_head = 1-smooth(.285, .425, z)
        vertex.co.x -= magnitude * posterior * low_head
    ob.data.update()
    return before


def orbital_seat(ob):
    """O2 only: recess the lateral socket edge without touching aperture Y/Z."""
    old_surface, _ = v10.facial_frame(ob)
    for vertex in ob.data.vertices:
        x, y, z = vertex.co
        lateral = smooth(.125, .19, abs(y)) * (1-smooth(.235, .285, abs(y)))
        vertical = smooth(.31, .36, z) * (1-smooth(.49, .535, z))
        anterior = 1-smooth(.205, .275, x)
        vertex.co.x += .015*lateral*vertical*anterior
    ob.data.update()
    new_surface, _ = v10.facial_frame(ob)
    for name in ('EYELID_L', 'EYELID_R'):
        lid = bpy.data.objects[name]
        for vertex in lid.data.vertices:
            y, z = vertex.co.y, vertex.co.z
            vertex.co.x += new_surface(y,z)[0].x-old_surface(y,z)[0].x
        lid.data.update()


def cap_vertices(ob, depth, blend_start=.80):
    """Inner cap has anatomical X axis; only its outer band meets facial seat."""
    surface, _ = v10.facial_frame(ob)
    seats = {}
    result = {}
    for name in ('EYE_L', 'EYE_R'):
        eye = bpy.data.objects[name]
        center_y = .162 if name.endswith('L') else -.162
        center_x = surface(center_y, .418)[0].x
        points = []
        for vertex in eye.data.vertices:
            p = vertex.co
            r = min(1.0, math.hypot((p.y-center_y)/.0685, (p.z-.418)/.0745))
            axis_x = center_x-depth*math.sqrt(max(0.0, 1-r*r))
            if r > blend_start:
                key = (round(p.y, 8), round(p.z, 8))
                if key not in seats:
                    seats[key] = surface(p.y, p.z)[0].x - .0005
                axis_x = axis_x*(1-smooth(blend_start, 1, r)) + seats[key]*smooth(blend_start, 1, r)
            points.append(Vector((axis_x, p.y, p.z)))
        result[name] = points
    return result


def cap_metrics(points):
    rotation = (Vector((.62,0,.40))-Vector((-3,-3,1.3))).to_track_quat('-Z','Y')
    axes = {'front': (Vector((0,-1,0)), Vector((0,0,1))),
            'side': (Vector((1,0,0)), Vector((0,0,1))),
            '3q': (rotation @ Vector((1,0,0)), rotation @ Vector((0,1,0)))}
    out = {}
    for name, vertices in points.items():
        out[name] = {}
        for view, (right, up) in axes.items():
            width = max(p.dot(right) for p in vertices)-min(p.dot(right) for p in vertices)
            height = max(p.dot(up) for p in vertices)-min(p.dot(up) for p in vertices)
            out[name][view] = dict(width_H=width, height_H=height, width_height_ratio=width/height)
    return out


def select_cap(ob, prefer_shallow=False):
    trials = []
    selected = None
    for depth in (.050, .055, .060, .065, .070, .075, .080):
        points = cap_vertices(ob, depth)
        metrics = cap_metrics(points)
        side = metrics['EYE_R']['side']['width_H']
        ratio = metrics['EYE_R']['3q']['width_height_ratio']
        trial = dict(depth_H=depth, side_span_H=side, near_3q_ratio=ratio)
        trials.append(trial)
        if .128 <= side <= .138 and .95 <= ratio <= 1.15:
            score = depth if prefer_shallow else abs(side-.133)/.01 + abs(ratio-1.05)
            if selected is None or score < selected[0]:
                selected = (score, depth, points, metrics)
    return trials, selected


def render_views(directory, views):
    scene = bpy.context.scene
    digest = v8.geometry_digest()
    scene.render.resolution_x = scene.render.resolution_y = 480
    scene.cycles.samples = 16
    for view in views:
        if view in ('front', 'side'):
            camera = bpy.data.objects['CAM '+view]
        else:
            camera = v8.camera('TEMP '+view, (-3,-3,1.3) if view == '3q' else (.55,0,4),
                               (.62,0,.40) if view == '3q' else (.55,0,0))
        scene.camera = camera
        assert v8.geometry_digest() == digest
        scene.render.filepath = str(directory / (('skin-' if view in ('front','side') else 'diagnostic-')+view+'.png'))
        bpy.ops.render.render(write_still=True)
        if view in ('3q', 'top'):
            bpy.data.objects.remove(camera, do_unlink=True)
    scene.camera = bpy.data.objects['CAM front']


def finalize_failure():
    """Save the inspected T2/O2 diagnostic, preserving the rejected status."""
    directory = TEMP / 'T2-O2'
    result = json.loads((directory/'measurements.json').read_text())
    assert result['technical_static_gate'] == 'PASS'
    assert result['ocular_depth_H'] == .075
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    changed = {'CENTRAL_CHASSIS','EYE_L','EYE_R','EYELID_L','EYELID_R'}
    frozen = {ob.name:v11.frozen_record(ob) for ob in bpy.context.scene.objects if ob.name not in changed}
    source_faces = [tuple(p.vertices) for p in bpy.data.objects['CENTRAL_CHASSIS'].data.polygons]
    bpy.ops.wm.open_mainfile(filepath=str(directory/'candidate.blend'))
    v11.verify_registration()
    assert v8.geometry_digest() == result['geometry_digest']
    assert [tuple(p.vertices) for p in bpy.data.objects['CENTRAL_CHASSIS'].data.polygons] == source_faces
    fixed = {name:v11.frozen_record(bpy.data.objects[name]) == record for name,record in frozen.items()}
    assert all(fixed.values())
    eye_contract = {}
    for name in ('EYE_L','EYE_R'):
        vertices = [v.co for v in bpy.data.objects[name].data.vertices]
        lo = [min(p[i] for p in vertices) for i in range(3)]
        hi = [max(p[i] for p in vertices) for i in range(3)]
        eye_contract[name] = dict(width_H=hi[1]-lo[1], height_H=hi[2]-lo[2], center_y_H=(lo[1]+hi[1])/2)
        assert abs(eye_contract[name]['width_H']-.137)<1e-6
        assert abs(eye_contract[name]['height_H']-.149)<1e-6
        assert abs(abs(eye_contract[name]['center_y_H'])-.162)<1e-6
    result.update(eye_contract_H=eye_contract, frozen_objects=fixed,
                  executor_visual_precheck='FAIL',
                  visual_views=dict(skin_front='Front aperture and chassis Front projection preserved; under-chin transition reads more sharply than intended.',
                                    skin_side='FAIL: long dominant oblique under-jaw surface remains; eye reads as exposed/protruding despite measured span.',
                                    diagnostic_3q='Near-eye whole-cap ratio in target range; the socket/eye still looks exposed.',
                                    diagnostic_top='Rounded posterior shoulders retained; anterior taper not clearly improved.'),
                  motion_clearance='NOT_RUN_EXECUTOR_VISUAL_PRECHECK_FAILED',
                  human_geometry_gate='NOT_REVIEW_READY',
                  candidate_role='DIAGNOSTIC ONLY — NOT PROMOTED',
                  status='BLOCKED_AT_V012_PHASE_A_VISUAL_RECONSTRUCTION',
                  blockers=['Side lower-cheek/chest retains the dominant oblique turn instead of the locked very short rounded transition; Front under-chin crease is also too sharp.',
                            'Side eye reaches the numeric span but remains exposed/protruding; measured whole-cap width does not establish socket integration.'],
                  phase_b='NOT_STARTED', phase_c='NOT_STARTED',
                  production_rig=False, animation=False, fleece=False, glb=False, runtime=False,
                  source_v011_unchanged=True)
    scene = bpy.context.scene
    for key in ('candidate_role','status','executor_visual_precheck','motion_clearance','human_geometry_gate'):
        scene['stage' if key == 'status' else key] = result[key]
    scene.camera = bpy.data.objects['CAM front']
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    bpy.ops.wm.open_mainfile(filepath=str(ASSET))
    assert v8.geometry_digest() == result['geometry_digest']
    fixed_reload = {name:v11.frozen_record(bpy.data.objects[name]) == record for name,record in frozen.items()}
    assert all(fixed_reload.values())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    for name in ('skin-front.png','skin-side.png','diagnostic-3q.png','diagnostic-top.png'):
        shutil.copy2(directory/name, EVIDENCE/name)
    v10.write(EVIDENCE/'measurements.json', result)
    validation = {key:result[key] for key in (
        'candidate','source_commit','source_v011_sha256','selected_transition','selected_ocular',
        'topology','identical_face_connectivity','chassis_yz_max_delta_H','transition_max_x_delta_H',
        'orbital_seat_max_x_delta_H','chassis_575_plus_max_delta_H','technical_static_gate',
        'adjacency_audit','reference_hashes_verified','reference_registration_verified','geometry_digest',
        'ocular_depth_H','ocular_projection','eye_contract_H','executor_visual_precheck',
        'visual_views','motion_clearance','human_geometry_gate','candidate_role','status','blockers',
        'phase_b','phase_c','source_v011_unchanged')}
    validation.update(control_disjoint_intersections=result['control']['count'],
                      evaluated_disjoint_intersections=result['evaluated']['count'],
                      frozen_objects_after_reload=fixed_reload,
                      diagnostic_v012_sha256=hashlib.sha256(ASSET.read_bytes()).hexdigest())
    v10.write(EVIDENCE/'validation.json', validation)
    print('FINAL_DIAGNOSTIC '+json.dumps(dict(asset=str(ASSET), status=result['status'],
                                                frozen=all(fixed_reload.values()))), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--transition', type=int, choices=(1,2))
    parser.add_argument('--ocular', type=int, choices=(0,1,2), default=0)
    parser.add_argument('--render', default='')
    parser.add_argument('--finalize-failure', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.finalize_failure:
        finalize_failure()
        return
    assert args.transition is not None
    candidate = f'T{args.transition}-O{args.ocular}'
    directory = TEMP / candidate
    directory.mkdir(parents=True, exist_ok=True)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    hashes = {name: hashlib.sha256((v8.REFERENCE/name).read_bytes()).hexdigest() == expected
              for name, expected in v8.REFERENCE_HASHES.items()}
    assert all(hashes.values())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    v11.verify_registration()
    scene = bpy.context.scene
    changed = {'CENTRAL_CHASSIS', 'EYE_L', 'EYE_R'}
    if args.ocular == 2:
        changed |= {'EYELID_L', 'EYELID_R'}
    frozen = {ob.name: v11.frozen_record(ob) for ob in scene.objects if ob.name not in changed}
    chassis = bpy.data.objects['CENTRAL_CHASSIS']
    faces = [tuple(poly.vertices) for poly in chassis.data.polygons]
    before = transition(chassis, .035 if args.transition == 1 else .050)
    transition_max_x = max(abs(a.x-v.co.x) for a,v in zip(before,chassis.data.vertices))
    after_transition = [v.co.copy() for v in chassis.data.vertices]
    if args.ocular == 2:
        orbital_seat(chassis)
    orbital_max_x = max(abs(a.x-v.co.x) for a,v in zip(after_transition,chassis.data.vertices))
    bpy.context.view_layer.update()
    after = [v.co for v in chassis.data.vertices]
    max_x = max(abs(a.x-b.x) for a,b in zip(before,after))
    max_yz = max(max(abs(a.y-b.y),abs(a.z-b.z)) for a,b in zip(before,after))
    rear = max((a-b).length for a,b in zip(before,after) if a.x >= .575-1e-7)
    assert max_yz == 0 and rear == 0 and transition_max_x <= (.035 if args.transition == 1 else .050)+1e-7
    assert orbital_max_x <= (.015+1e-7 if args.ocular == 2 else 1e-7)
    assert faces == [tuple(poly.vertices) for poly in chassis.data.polygons]
    topology = v10.topology(chassis)
    control = v10.intersections(chassis.data)
    evaluated_data = chassis.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    evaluated = v10.intersections(evaluated_data)
    adjacency = dict(control=v10.adjacency_audit(chassis.data),
                     evaluated=v10.adjacency_audit(evaluated_data))
    passed = (topology['vertices'] == 533 and topology['edges'] == 1062 and topology['faces'] == 531
              and topology['components'] == 1 and topology['nonmanifold_edges'] == 0
              and topology['all_quads'] and topology['euler'] == 2 and topology['degenerate_faces'] == 0
              and control['count'] == evaluated['count'] == 0
              and all(a['improper_contacts'] == 0 for a in adjacency.values()))
    result = dict(candidate='v012-'+candidate, source_commit=SOURCE_HEAD, source_v011_sha256=SOURCE_SHA,
                  selected_transition=f'T{args.transition}', selected_ocular=f'O{args.ocular}' if args.ocular else 'V011_UNCHANGED',
                  topology=topology, identical_face_connectivity=True,
                  chassis_yz_max_delta_H=max_yz, transition_max_x_delta_H=transition_max_x,
                  chassis_total_max_x_delta_H=max_x, orbital_seat_max_x_delta_H=orbital_max_x,
                  chassis_575_plus_max_delta_H=rear, control=control, evaluated=evaluated,
                  adjacency_audit=adjacency, technical_static_gate='PASS' if passed else 'FAIL',
                  reference_hashes=v8.REFERENCE_HASHES, reference_hashes_verified=hashes,
                  reference_registration=v8.REGISTRATION, reference_registration_verified=True)
    print('TECHNICAL_GATE '+json.dumps({k:result[k] for k in ('candidate','technical_static_gate','control','evaluated','adjacency_audit','transition_max_x_delta_H')}), flush=True)
    if not passed:
        v10.write(directory/'measurements.json', result)
        return
    if args.ocular:
        trials, selected = select_cap(chassis, prefer_shallow=args.ocular == 2)
        result['ocular_search'] = trials
        if selected is None:
            result['ocular_search_result'] = 'NO_ACCEPTABLE_DEPTH'
            v10.write(directory/'measurements.json', result)
            print('OCULAR_SEARCH '+json.dumps(trials), flush=True)
            return
        _, depth, points, metrics = selected
        for name, vertices in points.items():
            for vertex, point in zip(bpy.data.objects[name].data.vertices, vertices):
                vertex.co.x = point.x
            bpy.data.objects[name].data.update()
        result['ocular_depth_H'] = depth
        result['ocular_projection'] = metrics
    else:
        result['ocular_projection'] = v11.projection_metrics()
    for name, record in frozen.items():
        assert v11.frozen_record(bpy.data.objects[name]) == record, name
    scene['selected_candidate'] = result['candidate']
    scene['stage'] = 'V012_PHASE_A_DIAGNOSTIC'
    scene['candidate_role'] = 'UNREVIEWED DIAGNOSTIC'
    scene['human_geometry_gate'] = 'NOT_REVIEW_READY'
    scene['motion_clearance'] = 'NOT_RUN'
    scene['saved_pose'] = 'NEUTRAL'
    scene.camera = bpy.data.objects['CAM front']
    result['geometry_digest'] = v8.geometry_digest()
    v10.write(directory/'measurements.json', result)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(directory/'candidate.blend'))
    if args.render:
        render_views(directory, args.render.split(','))


if __name__ == '__main__':
    main()
