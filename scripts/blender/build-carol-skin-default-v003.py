"""Extract v004's saved internal Skin and refine the v001 ear on that character."""
import hashlib
import importlib.util
import json
import math
import struct
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'assets/grimo/production/carol/blender'
V004 = ASSETS / 'carol-normal-fleece-v004.blend'
EAR = ASSETS / 'carol-skin-ear-correction-v001.blend'
OUTPUT = ASSETS / 'carol-skin-default-v003.blend'
EVIDENCE = ROOT / 'docs/production/carol/evidence/skin-default-v003'
SKIN_MESHES = {'CENTRAL_CHASSIS', 'EAR_L', 'EAR_R', 'EYELID_L', 'EYELID_R',
               'EYE_L', 'EYE_R', 'FORE_L', 'FORE_R', 'HIND_L', 'HIND_R',
               'HOOF_FORE_L', 'HOOF_FORE_R', 'HOOF_HIND_L', 'HOOF_HIND_R',
               'NOSE', 'SKIN_TAIL_CORE'}
SKIN_CURVES = {'MOUTH_closed', 'PHILTRUM'}
SKIN_EMPTIES = {'TAIL_PIVOT', 'PIGMENT_SPACE'}
REVIEW_FIXTURES = {'Key', 'Fill', 'Rear', 'Low', 'VIEW_front', 'VIEW_side',
                   'VIEW_rear', 'VIEW_top', 'VIEW_yaw-30'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(ob):
    h = hashlib.sha256()
    if ob.type == 'MESH':
        for v in ob.data.vertices:
            h.update(struct.pack('<3f', *v.co))
        for p in ob.data.polygons:
            h.update(struct.pack('<II', len(p.vertices), p.material_index))
            for i in p.vertices:
                h.update(struct.pack('<I', i))
        for attr in ob.data.color_attributes:
            h.update((attr.name + attr.data_type + attr.domain).encode())
            for item in attr.data:
                if hasattr(item, 'color'):
                    h.update(struct.pack('<4f', *item.color))
                elif hasattr(item, 'value'):
                    h.update(struct.pack('<f', item.value))
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
    return {'data': h.hexdigest(), 'matrix': [round(x, 8) for row in ob.matrix_world for x in row],
            'parent': ob.parent.name if ob.parent else None,
            'materials': [m.name for m in ob.data.materials] if ob.type == 'MESH' else [],
            'modifiers': [(m.name, m.type) for m in ob.modifiers]}


def smooth(t):
    t = max(0., min(1., t))
    return t*t*(3-2*t)


def refine(ob, sign):
    """Stationwise volume, buried saddle and a continuous soft inner trough."""
    assert len(ob.data.vertices) == 95*24 and not ob.data.shape_keys
    c, s = math.cos(math.radians(35)), math.sin(math.radians(35))
    pigment = ob.data.color_attributes.new(name='SoftInnerBowl', type='FLOAT', domain='POINT')
    for start in range(0, len(ob.data.vertices), 24):
        ring = ob.data.vertices[start:start+24]
        local = [Vector(((v.co.x-.386)*c-(sign*v.co.y-.235)*s,
                         (v.co.x-.386)*s+(sign*v.co.y-.235)*c,
                         v.co.z-.579)) for v in ring]
        station = start//24
        if station >= 74:
            # v001 pinched all seven bowl vertices onto one line near station
            # 85. Spread them between the unchanged lower/upper brown rims.
            weight = .40*smooth((station-74)/10)
            lower, upper = local[10].copy(), local[18].copy()
            margin = min(.003, (upper.z-lower.z)*.12)
            for j in range(11,18):
                q = (j-10)/8
                target_z = lower.z+margin+(upper.z-lower.z-2*margin)*q
                local[j].z += weight*(target_z-local[j].z)
        u = sum(p.y for p in local)/24
        t = max(0., min(1., (u+.0202)/.435))
        root = math.exp(-(t/.24)**2)
        middle = math.sin(math.pi*t)**2
        tip = math.exp(-((t-.84)/.13)**2)
        mid_z = (local[0].z+local[8].z)/2
        center_x = sum(p.x for p in local)/24
        for j, (v, p) in enumerate(zip(ring, local)):
            # Keep the root deep inside the head and broaden the emerging section.
            x = center_x+(p.x-center_x)*(1+.19*root+.045*middle+.045*tip)
            z = mid_z+(p.z-mid_z)*(1-.055*middle-.065*tip)
            z += -.010*math.sin(math.pi*t*.9)+.012*smooth((t-.76)/.22)
            # Recess the pink trough gradually; surrounding brown rim is untouched.
            proximal_cross = {10:.10, 11:.40, 12:.78, 13:1., 14:1., 15:1.,
                              16:.88, 17:.58, 18:.38, 19:.21, 20:.08, 21:.02}.get(j, 0.)
            distal_cross = {7:.03, 8:.24, 9:.64, 10:.90, 11:1., 12:1.,
                            13:.95, 14:.82, 15:.65, 16:.44, 17:.25, 18:.08}.get(j, 0.)
            shift = smooth((t-.55)/.32)
            cross = proximal_cross*(1-shift)+distal_cross*shift
            longitudinal = smooth((t-.055)/.17)*(1-smooth((t-.68)/.30))
            x += .005*cross*longitudinal
            new_u = u-.028*root+.017*smooth((t-.55)/.45)
            v.co = (.386+x*c+new_u*s,
                    sign*(.235-x*s+new_u*c), .579+z)
            # The center extends farther than the rim, closing the pink bowl
            # on a rounded arc while leaving brown around the distal tip.
            end = .99-.05*min(1.,abs(j-11.5)/5.)**1.5
            pigment.data[v.index].value = cross*smooth((t-.055)/.17)*(1-smooth((t-(end-.16))/.16))
    ob.data.update()
    # One continuous material lets the coral trough close softly at its tip.
    brown, coral = ob.data.materials[:2]
    brown_bsdf = next(n for n in brown.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    coral_bsdf = next(n for n in coral.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    combined = brown.copy()
    combined.name = 'Carol ear cocoa and recessed coral v003'
    nodes, links = combined.node_tree.nodes, combined.node_tree.links
    bsdf = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
    attr = nodes.new('ShaderNodeAttribute')
    attr.attribute_name = 'SoftInnerBowl'
    blend = nodes.new('ShaderNodeMixRGB')
    blend.blend_type = 'MIX'
    blend.inputs['Color1'].default_value = brown_bsdf.inputs['Base Color'].default_value
    blend.inputs['Color2'].default_value = coral_bsdf.inputs['Base Color'].default_value
    links.new(attr.outputs['Fac'], blend.inputs['Fac'])
    links.new(blend.outputs['Color'], bsdf.inputs['Base Color'])
    ob.data.materials.clear()
    ob.data.materials.append(combined)
    for face in ob.data.polygons:
        face.material_index = 0


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    before_sha = {'v004': sha(V004), 'ear_v001': sha(EAR),
                  'skin_v002': sha(ASSETS/'carol-skin-final-v002.blend')}
    bpy.ops.wm.open_mainfile(filepath=str(V004))
    retained = SKIN_MESHES | SKIN_CURVES | SKIN_EMPTIES
    assert retained <= set(bpy.data.objects.keys())
    baseline = {n: snapshot(bpy.data.objects[n]) for n in retained if n not in {'EAR_L', 'EAR_R'}}
    excluded = sorted(o.name for o in bpy.context.scene.objects if o.name not in retained | REVIEW_FIXTURES)
    for name in excluded:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    with bpy.data.libraries.load(str(EAR), link=False) as (src, dst):
        dst.objects = ['EAR_L', 'EAR_R']
    for source in dst.objects:
        target = bpy.data.objects[source.name.removesuffix('.001')]
        target.data = source.data.copy()
        sign = 1 if target.name == 'EAR_L' else -1
        refine(target, sign)
        bpy.data.objects.remove(source, do_unlink=True)
    scene = bpy.context.scene
    scene['skin_default_source'] = 'carol-normal-fleece-v004.blend / saved internal Skin'
    scene['ear_source'] = 'carol-skin-ear-correction-v001.blend / refined ears'
    scene['default_baseline'] = 'PROMOTED'
    scene['ear_visual_human_review'] = 'PENDING'
    scene['phase1_state'] = 'SKIN_DEFAULT_V003_HUMAN_EAR_REVIEW_PENDING'
    scene.camera = bpy.data.objects['VIEW_front']
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))
    after = {n: snapshot(bpy.data.objects[n]) for n in baseline}
    assert baseline == after, [n for n in baseline if baseline[n] != after[n]]
    assert all(n not in bpy.data.objects for n in excluded)
    assert set(o.name for o in bpy.context.scene.objects if o.type in {'MESH','CURVE'}) == SKIN_MESHES | SKIN_CURVES
    assert {k: sha(p) for k,p in [('v004',V004),('ear_v001',EAR),('skin_v002',ASSETS/'carol-skin-final-v002.blend')]} == before_sha
    report = {'output': OUTPUT.relative_to(ROOT).as_posix(), 'sha256': sha(OUTPUT),
              'sources': {k: {'sha256': v} for k,v in before_sha.items()},
              'saved_reopened': True, 'retained_skin_objects': sorted(retained),
              'excluded_v004_objects': excluded, 'non_ear_snapshots_identical': baseline == after,
              'non_ear_object_count': len(baseline), 'ear_visual_human_review': 'PENDING',
              'default_baseline': 'PROMOTED'}
    (EVIDENCE/'composition.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print('SKIN_DEFAULT_BUILT', json.dumps({'sha256': report['sha256'], 'non_ear_objects':len(baseline)}))


if __name__ == '__main__':
    main()
