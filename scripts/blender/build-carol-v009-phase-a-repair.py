"""Bounded A3 local jaw/portal repair of retained A2; no exterior union.

Run in Blender background. Failed gates never overwrite the retained blend.
"""
import importlib.util
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

spec = importlib.util.spec_from_file_location('v9', Path(__file__).with_name('build-carol-v009.py'))
v9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v9)
ATTEMPT = 3
OUT = v9.OUT / 'phase-a-attempt-3'


def intersections(data):
    pts = [v.co.copy() for v in data.vertices]
    polys = [list(p.vertices) for p in data.polygons]
    tree = BVHTree.FromPolygons(pts, polys)
    pairs = sorted({tuple(sorted((a, b))) for a, b in tree.overlap(tree)
                    if a != b and set(polys[a]).isdisjoint(polys[b])})
    regions = {n: dict(count=0, centroids=[], minimum=[1e9]*3, maximum=[-1e9]*3) for n in
               ['FACE/LOWER_CHEEK', 'NECK_TRANSITION', 'CHEST', 'OTHER']}
    for a, b in pairs:
        ids = polys[a] + polys[b]
        c = sum((pts[i] for i in ids), Vector()) / len(ids)
        region = ('OTHER' if c.x >= .575 else 'FACE/LOWER_CHEEK' if c.z >= .29
                  else 'NECK_TRANSITION' if c.x < .4 else 'CHEST')
        r = regions[region]
        r['count'] += 1
        r['minimum'] = [min(r['minimum'][i], round(c[i], 5)) for i in range(3)]
        r['maximum'] = [max(r['maximum'][i], round(c[i], 5)) for i in range(3)]
        if len(r['centroids']) < 3:
            r['centroids'].append([round(x, 5) for x in c])
    return dict(count=len(pairs), regions=regions)


def topology(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    seen = set()
    components = 0
    for v in bm.verts:
        if v in seen:
            continue
        components += 1
        stack = [v]
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v)
            stack.extend(e.other_vert(v) for e in v.link_edges)
    result = dict(components=components, nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),
                  all_quads=all(len(f.verts) == 4 for f in bm.faces),
                  euler=len(bm.verts)-len(bm.edges)+len(bm.faces))
    bm.free()
    return result


def repair(old):
    verts, faces = [], []
    def loop(points):
        ids = list(range(len(verts), len(verts)+len(points)))
        verts.extend(tuple(p) for p in points)
        return ids
    def bridge(a, b):
        assert len(a) == len(b)
        for j in range(len(a)):
            k = (j+1) % len(a)
            faces.append((a[j], a[k], b[k], b[j]))
    def cap(a):
        faces.extend((a[0], a[j], a[j+1], a[j+2]) for j in range(1, len(a)-2, 2))

    # Copy accepted upper head through the original .315 cheek ring verbatim.
    head_count = len(v9.v8.HEAD_SECTIONS[3:])
    head = []
    for i in range(head_count):
        a = loop([old.data.vertices[64*i+j].co for j in range(64)])
        if head:
            bridge(head[-1], a)
        head.append(a)
    cap(head[0])
    # Round the visible jaw and close its underside toward a posterior portal.
    # These are local head-owned annuli, not head-to-torso transition sections.
    for fx, rx, width, front_z, rear_z in [
        (.050, .522, .282, .282, .352),
        (.115, .520, .249, .256, .354),
        (.235, .517, .211, .275, .350),
        (.320, .512, .175, .320, .348),
    ]:
        pts = []
        for j in range(64):
            t = 2*math.pi*j/64
            c, s = math.cos(t), math.sin(t)
            z = ((front_z+rear_z)/2+(rear_z-front_z)/2*c)
            if ATTEMPT == 4 and fx < .320:
                z = front_z+(rear_z-front_z)*max(c, 0)**2
            pts.append(((fx+rx)/2+(rx-fx)/2*c, width*s, z))
        a = loop(pts)
        bridge(head[-1], a)
        head.append(a)
    head_portal = head[-1]

    # Retain the warped A2 .450 seam and every rear station exactly. A dense
    # local chest grid supplies a dorsal opening; reduction is lateral chest.
    seam_start = head_count*64 + 64 + 4*64 + 32
    seam = [old.data.vertices[seam_start+j].co.copy() for j in range(16)]
    chest = []
    for i in range(29):
        u = .96*i/28
        pts = []
        for j in range(32):
            t = 2*math.pi*j/32
            c, s = math.cos(t), math.sin(t)
            # Front chest rounds shut below the jaw. Back boundary meets A2.
            x = .252 + (.450-.252)*u + .145*u*max(c, 0)**2
            z0 = .246 + .026*c
            z1 = .2715 + .1685*v9.v8.signed_power(c, .9)-.024*max(c, 0)**2
            z = z0*(1-u)+z1*u
            y = (.040*(1-u)+.284*u)*v9.v8.signed_power(s, .9)
            pts.append((x, y, z))
        chest.append(loop(pts))
    cap(chest[0])
    # A3: 24 longitudinal + 8 angular; A4: 20 + 12 => 64 boundary edges.
    # Preserve head's existing 64 sectors to avoid jaw-center reduction poles.
    lo, hi = 3, (23 if ATTEMPT == 4 else 27)
    angular = 6 if ATTEMPT == 4 else 4
    for i in range(28):
        for j in range(32):
            if lo <= i < hi and (j < angular or j >= 32-angular):
                continue
            k = (j+1) % 32
            faces.append((chest[i][j], chest[i][k], chest[i+1][k], chest[i+1][j]))
    portal = ([chest[hi][j] for j in range(angular)]
              + [chest[i][angular] for i in range(hi, lo, -1)]
              + [chest[lo][j % 32] for j in range(angular, -angular, -1)]
              + [chest[i][32-angular] for i in range(lo, hi)]
              + [chest[hi][j] for j in range(32-angular, 32)])
    assert len(portal) == 64
    if ATTEMPT == 4:
        # Known A3 defect: the chest opening climbed inside the closed head.
        # Seat it immediately below the head portal with matching anchors.
        for j, idx in enumerate(portal):
            p = Vector(verts[head_portal[j]])
            p.z -= .032
            p.x += .003
            verts[idx] = tuple(p)
        # Lower the adjacent lateral chest below the rounded jaw; a short
        # transition behind the opening recovers the frozen dorsal seam.
        for i in range(lo, hi+1):
            for j in range(angular+1, 32-angular):
                idx = chest[i][j]
                p = Vector(verts[idx])
                if p.x < .5 and p.z > .24:
                    p.z -= .065*max(0, 1-abs(j-16)/11)
                verts[idx] = tuple(p)
        # Retain every frozen coordinate on the old local upper-chest seam,
        # including the two transition rows that extend past X=.575.
        for row, start, count in [(24, seam_start-96, 64), (25, seam_start-32, 32)]:
            for j in range(count):
                p = old.data.vertices[start+j].co
                if p.x >= .575:
                    target = j if j <= count//2 else 32-(count-j)
                    verts[chest[row][target]] = tuple(p)
    # Align four semantic anchors with the local head opening, retaining the
    # ordered chest boundary. Interior rows use bounded smoothstep Hermite.
    a = head_portal
    for t in [.25, .5, .75]:
        s = t*t*(3-2*t)
        b = loop([Vector(verts[h]).lerp(Vector(verts[c]), s)
                  for h, c in zip(head_portal, portal)])
        bridge(a, b)
        a = b
    bridge(a, portal)
    seam_ids = loop(seam)
    a, b = chest[-1], seam_ids
    for j in range(0, 16, 2):
        p = [a[(2*j+k) % 32] for k in range(5)]
        q = [b[(j+k) % 16] for k in range(3)]
        faces.extend([(p[0], p[1], q[1], q[0]), (p[1], p[2], p[3], q[1]),
                      (p[3], p[4], q[2], q[1])])
    a = seam_ids
    for offset in range(seam_start+16, len(old.data.vertices), 16):
        b = loop([old.data.vertices[offset+j].co for j in range(16)])
        bridge(a, b)
        a = b
    cap(a)
    # Remove unused grid interior vertices, without merging or remeshing.
    used = sorted({v for f in faces for v in f})
    remap = {v: i for i, v in enumerate(used)}
    skin = old.data.materials[0]
    bpy.data.objects.remove(old, do_unlink=True)
    obj = v9.v8.mesh('CENTRAL_CHASSIS', [verts[i] for i in used],
                     [tuple(remap[i] for i in f) for f in faces], skin, 2)
    obj['architecture'] = 'retained head; rounded jaw closure; posterior underside portal; three-row local neck; dorsal chest portal; retained rear torso'
    return obj


def main():
    global ATTEMPT, OUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, choices=[3, 4], default=3)
    parser.add_argument('--verify-retained', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.verify_retained:
        verify_retained()
        return
    ATTEMPT = args.attempt
    OUT = v9.OUT / f'phase-a-attempt-{ATTEMPT}'
    OUT.mkdir(exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(v9.ASSET))
    old = bpy.data.objects['CENTRAL_CHASSIS']
    baseline = {o.name: v9.record(o) for o in bpy.context.scene.objects if o != old}
    frozen = [tuple(v.co) for v in old.data.vertices if v.co.x >= .575]
    localization_file = v9.OUT/'phase-a-attempt-3'/'a2-localization.json'
    if localization_file.exists():
        localization = json.loads(localization_file.read_text())
    else:
        localization = intersections(old.evaluated_get(bpy.context.evaluated_depsgraph_get()).data)
        localization_file.write_text(json.dumps(localization, indent=2)+'\n')
        print('A2_LOCALIZATION', json.dumps(localization), flush=True)
    if localization['regions']['OTHER']['maximum'][0] > .65:
        raise RuntimeError('Unexpected frozen rear cluster; inspect before repair')
    obj = repair(old)
    bpy.context.view_layer.update()
    result = dict(candidate=f'v009-A{ATTEMPT}', topology=topology(obj),
                  control=intersections(obj.data),
                  evaluated=intersections(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).data),
                  frozen_vertices=all(p in {tuple(v.co) for v in obj.data.vertices} for p in frozen),
                  frozen_objects=all(v9.record(bpy.data.objects[n]) == h for n, h in baseline.items()))
    result['technical_pass'] = (result['topology'] == dict(components=1, nonmanifold_edges=0, all_quads=True, euler=2)
                                and result['control']['count'] == result['evaluated']['count'] == 0
                                and result['frozen_vertices'] and result['frozen_objects'])
    (OUT/'measurements.json').write_text(json.dumps(result, indent=2)+'\n')
    print(f'A{ATTEMPT}_FAST_GATE', json.dumps(result), flush=True)
    if not result['technical_pass']:
        return
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'candidate.blend'))
    scene = bpy.context.scene
    scene.render.resolution_x = scene.render.resolution_y = 480
    scene.cycles.samples = 16
    for view in ['front', 'side', '3q']:
        cam = v9.v8.camera('TEMP 3q', (-3, -3, 1.3), (.62, 0, .40)) if view == '3q' else bpy.data.objects['CAM '+view]
        scene.camera = cam
        scene.render.filepath = str(OUT/(('diagnostic-' if view == '3q' else 'skin-')+view+'.png'))
        bpy.ops.render.render(write_still=True)
        if view == '3q':
            bpy.data.objects.remove(cam, do_unlink=True)


def verify_retained():
    """One final reload of unchanged A2; record failures without promotion."""
    data_path = v9.OUT/'measurements.json'
    validation_path = v9.OUT/'validation.json'
    data = json.loads(data_path.read_text())
    validation = json.loads(validation_path.read_text())
    file_hash = hashlib.sha256(v9.ASSET.read_bytes()).hexdigest()
    assert file_hash == validation['retained_blend_sha256']
    bpy.ops.wm.open_mainfile(filepath=str(v9.ASSET))
    assert bpy.context.scene['selected_candidate'] == 'v009-A2'
    digest = v9.v8.geometry_digest()
    assert digest == validation['reloaded_neutral_digest']
    obj = bpy.data.objects['CENTRAL_CHASSIS']
    top = topology(obj)
    control = intersections(obj.data)
    evaluated = intersections(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).data)
    assert top == dict(components=1, nonmanifold_edges=0, all_quads=True, euler=2)
    assert evaluated['count'] == 455
    assert v9.v8.REGISTRATION == data['reference_registration']
    assert all(hashlib.sha256((v9.v8.REFERENCE/n).read_bytes()).hexdigest() == h
               for n, h in data['reference_hashes'].items())
    attempts = {f'A{i}': json.loads((v9.OUT/f'phase-a-attempt-{i}'/'measurements.json').read_text())
                for i in [3, 4]}
    recovery = dict(source_commit='01e19d27519d5731015d553cdae1acc572edf8c9',
                    selected_candidate='v009-A2', retained_asset_byte_identical=True,
                    status='BLOCKED_AT_V009_PHASE_A_ARCHITECTURE',
                    stopped_after='A4_STRUCTURAL_FAILURE; no A5',
                    attempts={name: dict(control_intersections=r['control']['count'],
                                         evaluated_intersections=r['evaluated']['count'],
                                         topology=r['topology'], frozen_vertices=r['frozen_vertices'],
                                         frozen_objects=r['frozen_objects'], technical_pass=False)
                              for name, r in attempts.items()},
                    blocker='Local portal/jaw/chest patch still intersects the head and upper-chest seam; A4 does not establish a clean exterior.',
                    visual_review='NOT_RUN_TECHNICAL_PREREQUISITE_FAILED',
                    motion_probe='NOT_RUN_TECHNICAL_PREREQUISITE_FAILED')
    for document in [data, validation]:
        document['phase_a_recovery'] = recovery
        document['central_topology']['connected_components'] = top['components']
        document['central_topology']['control_disjoint_face_intersection_pairs'] = control['count']
    validation['recovery_final_reload'] = dict(geometry_digest=digest, blend_sha256=file_hash,
                                              byte_identical_to_start=True, topology=top,
                                              control_intersections=control['count'],
                                              evaluated_intersections=evaluated['count'],
                                              reference_hashes_unchanged=True,
                                              reference_registration_unchanged=True,
                                              frozen_constraints='PASS; retained asset byte-identical')
    data_path.write_text(json.dumps(data, indent=2)+'\n')
    validation_path.write_text(json.dumps(validation, indent=2)+'\n')
    print('RETAINED_A2_FINAL_RELOAD', json.dumps(validation['recovery_final_reload']), flush=True)


if __name__ == '__main__':
    main()
