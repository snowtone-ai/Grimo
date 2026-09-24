"""Build Carol's approved localized ear/hoof modules from the exact v011 source.

Run: blender -b -t 4 --python scripts/blender/build-carol-hero-modules-v002.py
Only the six ear/hoof mesh objects are replaced. The reference sheets are never edited.
"""
import hashlib
import json
import math
import struct
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/grimo/production/carol/blender/carol-v011.blend'
OUTPUT = SOURCE.with_name('carol-hero-modules-v002.blend')
EVIDENCE = ROOT / 'docs/production/carol/evidence/hero-modules-v002'
SOURCE_SHA = '568fb4378b6ca3093ba5134d8d082f37a6723c9d5b5cf0b491a7c8e5f757aed3'
MODULES = {'EAR_L', 'EAR_R', 'HOOF_FORE_L', 'HOOF_FORE_R', 'HOOF_HIND_L', 'HOOF_HIND_R'}
EAR_IMAGE = ROOT / 'assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.png'
HOOF_IMAGE = ROOT / 'assets/grimo/source/carol/approved-3d/modules/carol-hoof-module-authority.png'
IMAGE_HASHES = {'ear': 'ca348f895689aefeea1844b12d7fb5a4af953e114859a552b6328311295e8563',
                'hoof': '00412f74458450d785b262403192979309e2b6d4ee5f33c6b1445cb36c4dbb7a'}


def digest_mesh(ob):
    h = hashlib.sha256()
    if ob.type == 'MESH':
        for v in ob.data.vertices:
            h.update(struct.pack('<3f', *v.co))
        for p in ob.data.polygons:
            h.update(struct.pack('<II', len(p.vertices), p.material_index))
            for i in p.vertices:
                h.update(struct.pack('<I', i))
    return h.hexdigest()


def record(ob):
    bounds = None
    if ob.type == 'MESH' and ob.data.vertices:
        points = [ob.matrix_world @ v.co for v in ob.data.vertices]
        bounds = {'min': [round(min(p[i] for p in points), 6) for i in range(3)],
                  'max': [round(max(p[i] for p in points), 6) for i in range(3)]}
    return {'name': ob.name, 'type': ob.type,
            'matrix_world': [round(c, 8) for row in ob.matrix_world for c in row],
            'vertices': len(ob.data.vertices) if ob.type == 'MESH' else None,
            'faces': len(ob.data.polygons) if ob.type == 'MESH' else None,
            'mesh_sha256': digest_mesh(ob) if ob.type == 'MESH' else None,
            'world_bounds': bounds,
            'material_slots': [m.name if m else None for m in ob.data.materials] if ob.type == 'MESH' else []}


def replace_mesh(name, verts, faces, material_indices, materials):
    ob = bpy.data.objects[name]
    old = ob.data
    mesh = bpy.data.meshes.new(name + '_v002')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for mat in materials:
        mesh.materials.append(mat)
    for poly, mi in zip(mesh.polygons, material_indices):
        poly.material_index = mi
        poly.use_smooth = True
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    ob.data = mesh
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


def smooth(t):
    return t * t * (3 - 2 * t)


def gaussian(x, mu, sigma):
    return math.exp(-((x-mu)/sigma)**2)


def ear(side):
    # A closed swept shell, not a card. Each section is an elliptical soft rim;
    # a modest concavity is authored into the same front surface as the inset.
    nl, na, nb, nc_outer = 48, 12, 24, 12
    nc = na + nb + nc_outer
    verts, faces, mats = [], [], []
    for i in range(nl + 1):
        t = i / nl
        s = smooth(t)
        x = .352 + .244*t + .018*math.sin(math.pi*t)
        y = side*(.205 + .382*t)
        z = .566 - .180*s + .018*math.sin(math.pi*t)
        # Full-spatial width and vertical cushion; rounded root and tip remain
        # thick enough to rotate without a razor-thin leaf.
        profile = math.sin(math.pi*(.015 + .97*t))**.70
        taper = smooth(max(0, min(1, (t-.78)/.22)))
        w = (.012 + .101*profile) * (1 - .34*taper)
        h = (.035 + .092*profile) * (1 - .36*taper)
        dx, dy = .244 + .018*math.pi*math.cos(math.pi*t), .382
        norm = math.hypot(dx, dy)
        px, py = -dy/norm, dx/norm
        oval = max(.001, 1-((t-.55)/.47)**2)
        half = 1.18*math.sqrt(oval)
        lower, upper = -.64-half, -.64+half
        angles = ([-math.pi+(-math.pi-lower)*(-j/na) for j in range(na)]
                  +[lower+(upper-lower)*j/nb for j in range(nb)]
                  +[upper+(math.pi-upper)*j/nc_outer for j in range(nc_outer)])
        for a in angles:
            c, q = math.cos(a), math.sin(a)
            # Pink sits on the face/lower quarter of the same shell. Its shallow
            # recess and rolled rim are geometric, not another floating mesh.
            inset = gaussian(t, .54, .34) * max(0, c)**3 * max(0, -q)**2
            verts.append((x + px*w*c + .009*inset,
                          y + side*py*w*c,
                          z + h*q - .004*inset))
    for i in range(nl):
        for j in range(nc):
            a = i*nc+j
            b = i*nc+(j+1)%nc
            c = (i+1)*nc+(j+1)%nc
            d = (i+1)*nc+j
            faces.append((a,b,c,d))
            # Both inset borders are vertex strips, so the color transition
            # curves smoothly along the surface without a material staircase.
            pink = na <= j < na+nb
            mats.append(1 if pink else 0)
    faces.extend([tuple(reversed(tuple(range(nc)))), tuple(nl*nc+j for j in range(nc))])
    mats.extend([0,0])
    return verts, faces, mats


def hoof(cx, cy):
    # One closed ring loft. Three toe prominences and two shallow recessed
    # clefts modify the same continuous front surface and sole silhouette.
    nr = 64
    stations = [
        (0.000, .085, .101), (.008, .091, .107), (.025, .095, .1095),
        (.052, .094, .1095), (.078, .088, .105), (.101, .075, .087),
        (.111, .066, .071), (.130, .053, .055), (.147, .041, .044)]
    verts, faces = [], []
    for z, rx, ry in stations:
        for j in range(nr):
            a = 2*math.pi*j/nr
            c, s = math.cos(a), math.sin(a)
            yy = ry*s
            front = max(0, c)**5
            lobes = sum(gaussian(yy, v, .021) for v in (-.071, 0, .071))
            clefts = sum(gaussian(yy, v, .009) for v in (-.036, .036))
            toe_zone = math.exp(-((z-.034)/.063)**4)
            xx = cx - rx*c*(1+.34*front) - front*toe_zone*(.006*lobes - .014*clefts)
            # The front cleft sole rises slightly, while three lobes still
            # touch the ground. Two valleys are visible without deep splitting.
            zz = z + (front*.009*clefts if z < .009 else 0)
            if z >= .078:
                zz += .018*front*math.exp(-((z-.103)/.033)**2)
                zz -= .008*max(0,-c)
            verts.append((xx, cy+yy, zz))
    for i in range(len(stations)-1):
        for j in range(nr):
            faces.append((i*nr+j, i*nr+(j+1)%nr,
                          (i+1)*nr+(j+1)%nr, (i+1)*nr+j))
    faces.append(tuple(reversed(tuple(range(nr)))))
    faces.append(tuple((len(stations)-1)*nr+j for j in range(nr)))
    return verts, faces, [0]*len(faces)


def aim(ob, location, target):
    ob.location = location
    ob.rotation_euler = (Vector(target)-ob.location).to_track_quat('-Z', 'Y').to_euler()


def render_isolated(name, view, ob_name, target):
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.new('TEMP module camera')
    cam = bpy.data.objects.new('TEMP module camera', cam_data)
    scene.collection.objects.link(cam)
    direction = {'front': (-4,0,0), 'side': (0,-4,0),
                 'top': (0,0,4), '3q': (-3,-3,2)}[view]
    aim(cam, Vector(target)+Vector(direction), target)
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = .67 if name == 'ear' else .34
    old_camera = scene.camera
    old_hide = {ob.name: ob.hide_render for ob in bpy.data.objects if ob.type == 'MESH'}
    visible = {ob_name}
    if name == 'hoof' and view != 'top':
        visible.add('FORE_R')  # actual frozen limb provides the integration mask
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            ob.hide_render = ob.name not in visible
    scene.camera = cam
    scene.render.film_transparent = True
    scene.render.resolution_x = scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.filepath = str(EVIDENCE / f'{name}-{view}-candidate.png')
    bpy.ops.render.render(write_still=True)
    for key, val in old_hide.items():
        bpy.data.objects[key].hide_render = val
    scene.camera = old_camera
    bpy.data.objects.remove(cam, do_unlink=True)


def render_integrated(view):
    scene = bpy.context.scene
    old_camera = scene.camera
    cam = None
    if view in ('front', 'side'):
        cam = bpy.data.objects['CAM '+view]
    else:
        cam_data = bpy.data.cameras.new('TEMP whole camera')
        cam = bpy.data.objects.new('TEMP whole camera', cam_data)
        scene.collection.objects.link(cam)
        v = Vector((-3,-3,1.7) if view == '3q-left' else (-3,3,1.7))
        aim(cam, Vector((.53,0,.34))+v, (.53,0,.34))
        cam_data.type = 'ORTHO'
        cam_data.ortho_scale = 1.53
    scene.camera = cam
    scene.render.film_transparent = False
    scene.render.resolution_x = 840
    scene.render.resolution_y = 630
    scene.render.resolution_percentage = 100
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.filepath = str(EVIDENCE / f'carol-{view}.png')
    bpy.ops.render.render(write_still=True)
    scene.camera = old_camera
    if view not in ('front','side'):
        bpy.data.objects.remove(cam, do_unlink=True)


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    for key, path in [('ear', EAR_IMAGE), ('hoof', HOOF_IMAGE)]:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == IMAGE_HASHES[key]
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    before = {o.name: record(o) for o in bpy.data.objects}
    frozen = {k:v for k,v in before.items() if k not in MODULES}
    cocoa = bpy.data.materials['DEBUG cocoa']
    inset = bpy.data.materials['DEBUG ear inset'].copy()
    inset.name = 'CAROL ear blush v002'
    inset.diffuse_color = (.98,.54,.52,1)
    if inset.use_nodes:
        for node in inset.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                node.inputs['Base Color'].default_value = (.98,.54,.52,1)
    for side, suffix in [(1,'L'),(-1,'R')]:
        replace_mesh('EAR_'+suffix, *ear(side), [cocoa,inset])
    for front, key in [(True,'FORE'),(False,'HIND')]:
        for side, suffix in [(1,'L'),(-1,'R')]:
            cx = .390 if front else .920
            cy = side*(.145 if front else .245)
            replace_mesh('HOOF_'+key+'_'+suffix, *hoof(cx,cy), [cocoa])
    after = {o.name: record(o) for o in bpy.data.objects}
    assert all(after[k] == v for k,v in frozen.items()), 'frozen object changed in memory'
    bpy.context.scene.camera = bpy.data.objects['CAM front']
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))
    reloaded = {o.name: record(o) for o in bpy.data.objects}
    assert all(reloaded[k] == v for k,v in frozen.items()), 'frozen object changed after save/reload'
    assert set(reloaded) == set(before)
    data = {'source_blend': str(SOURCE.relative_to(ROOT)).replace('\\','/'),
            'source_blend_sha256': SOURCE_SHA,
            'output_blend': str(OUTPUT.relative_to(ROOT)).replace('\\','/'),
            'output_blend_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
            'authority_images': {key: {'path': str(path.relative_to(ROOT)).replace('\\','/'),
                                       'sha256': IMAGE_HASHES[key]}
                                 for key,path in [('ear',EAR_IMAGE),('hoof',HOOF_IMAGE)]},
            'changed_objects': sorted(MODULES),
            'frozen_objects': {'count':len(frozen), 'verified': True,
                               'names': sorted(frozen), 'before': frozen,
                               'after_reload': {k:reloaded[k] for k in frozen}},
            'module_records': {k:reloaded[k] for k in sorted(MODULES)},
            'numeric_contract': {'ear_front_angle_degrees':18,
                                 'ear_thickness_intent_H':.028,
                                 'hoof_width_H':.219,'hoof_height_H':.111,
                                 'front_support_x_H':.390,'hind_support_x_H':.920}}
    (EVIDENCE/'validation.json').write_text(json.dumps(data, indent=2)+'\n', encoding='utf8')
    for name, obj, target in [('ear','EAR_R',(.51,-.41,.46)),
                              ('hoof','HOOF_FORE_R',(.39,-.145,.064))]:
        for view in ('front','side','top','3q'):
            render_isolated(name,view,obj,target)
    for view in ('front','side','3q-left','3q-right'):
        render_integrated(view)
    print('HERO_MODULES_V002_COMPLETE', json.dumps({'frozen':len(frozen),'changed':sorted(MODULES)}), flush=True)


if __name__ == '__main__':
    main()
