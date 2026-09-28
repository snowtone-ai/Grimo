"""Ear-only coordinate correction of accepted Skin; topology and shading retained."""
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/grimo/production/carol/blender/carol-skin-final-v002.blend'
OUTPUT = SOURCE.with_name('carol-skin-ear-correction-v001.blend')
OUT = ROOT / 'docs/production/carol/evidence/skin-ear-correction-v001'
SHA = '321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a'
spec = importlib.util.spec_from_file_location('ear_util', Path(__file__).with_name('build-carol-ear-production-v002.py'))
util = importlib.util.module_from_spec(spec)
spec.loader.exec_module(util)
EARS = {'EAR_L', 'EAR_R'}


def correct(ob, sign):
    c, s = math.cos(math.radians(35)), math.sin(math.radians(35))
    assert len(ob.data.vertices) == 95 * 24 and not ob.data.shape_keys
    for start in range(0, len(ob.data.vertices), 24):
        ring = ob.data.vertices[start:start+24]
        local = []
        for v in ring:
            dx, dy = v.co.x - .386, sign * v.co.y - .235
            local.append(Vector((dx*c-dy*s, dx*s+dy*c, v.co.z-.579)))
        u = sum(p.y for p in local)/24
        t = max(0., min(1., (u+.012)/.413))
        root = math.exp(-(t/.19)**2)
        body = math.sin(math.pi*t)**2
        top, bottom = local[0].z, local[8].z
        mid = (top+bottom)/2
        # A broad buried saddle; modest fuller section, same rounded silhouette.
        depth = 1.14 + .20*root
        height = 1 + .055*body
        for v, p in zip(ring, local):
            x = p.x*depth
            z = mid+(p.z-mid)*height - .006*math.sin(math.pi*t/2)**2
            # Ease the pinched pink end by widening the distal cup in-place.
            j = v.index % 24
            cup = math.exp(-((u-.342)/.042)**2)
            center = (local[11].z+local[17].z)/2
            if 9 <= j <= 22:
                weight = {9:.12,10:.45,18:.75,19:.48,20:.25,21:.10,22:.02}.get(j,1.)
                z += (p.z-center)*.18*cup*weight
            new_u = u + .016*t*t
            v.co = (.386+x*c+new_u*s,
                    sign*(.235-x*s+new_u*c-.010*root), .579+z)
    ob.data.update()


def render_set(label):
    util.TMP = OUT / label
    util.TMP.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.cycles.samples = 32
    for name, direction, target, scale, size in [
        ('front',(-4,0,0),(.52,0,.395),1.29,(1100,960)),
        ('side',(0,-4,0),(.53,0,.395),1.34,(1100,960)),
        ('front-3q',(-4,-2,.35),(.52,0,.395),1.34,(1100,960)),
        ('ear-side',(0,-4,0),(.47,-.30,.535),.65,(850,750)),
        ('ear-top',(0,0,4),(.49,-.40,.52),.58,(750,750)),
    ]:
        util.render(name,direction,target,scale,size=size)


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SHA
    OUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    before = {o.name:util.snapshot(o) for o in bpy.data.objects}
    old_checks = {n:util.mesh_check(bpy.data.objects[n]) for n in EARS}
    for side,sign in [('L',1),('R',-1)]:
        correct(bpy.data.objects['EAR_'+side], sign)
    bpy.context.view_layer.update()
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))
    after = {o.name:util.snapshot(o) for o in bpy.data.objects}
    changed = sorted(n for n in before if before[n] != after[n])
    assert set(before) == set(after) and changed == sorted(EARS), changed
    checks = {n:util.mesh_check(bpy.data.objects[n]) for n in EARS}
    for val in checks.values():
        assert val['finite'] and val['outward_normals'] and val['nonmanifold_edges']==0 and val['nonadjacent_triangle_intersections']==0, val
    tree = BVHTree.FromObject(bpy.data.objects['CENTRAL_CHASSIS'], bpy.context.evaluated_depsgraph_get())
    roots = {}
    for n in sorted(EARS):
        o = bpy.data.objects[n]
        center = sum((o.matrix_world @ v.co for v in o.data.vertices[:24]),Vector())/24
        p,normal,_,distance = tree.find_nearest(center)
        roots[n] = {'inside_head':(center-p).dot(normal)<0,'surface_distance_H':distance}
    assert all(v['inside_head'] for v in roots.values())
    report = {'source':str(SOURCE.relative_to(ROOT)), 'source_sha256':SHA,
              'candidate':str(OUTPUT.relative_to(ROOT)), 'candidate_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
              'changed_objects':changed,'unchanged_object_count':len(before)-2,
              'unchanged_object_snapshots':{n:before[n] for n in before if n not in EARS},
              'topology_material_slots_transforms_retained':all(all(before[n][k]==after[n][k] for k in ['counts','materials','matrix','modifiers','parent']) for n in EARS),
              'before_ear_checks':old_checks,'after_ear_checks':checks,'root_checks':roots,
              'save_reload_verified':True,'human_acceptance':'PENDING; ear-only candidate, not accepted Skin replacement',
              'rigging':'No rig or shape keys added; deformation readiness unverified'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    render_set('new')
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    render_set('old')


if __name__ == '__main__':
    main()
