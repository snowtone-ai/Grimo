"""Build Carol's local v003 ear, hoof and recessed eye candidate from v002.

Run: blender -b -t 4 --python scripts/blender/build-carol-hero-modules-v003.py
"""
import hashlib
import json
import math
import os
import struct
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from carol_hero_v003_geometry import EAR, HOOF, ear as make_ear, hoof as make_hoof

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/grimo/production/carol/blender/carol-hero-modules-v002.blend'
OUTPUT = SOURCE.with_name('carol-hero-modules-v003.blend')
EVIDENCE = ROOT / 'docs/production/carol/evidence/hero-modules-v003'
PARAMETERS = ROOT / 'docs/production/carol/CAROL_HERO_MODULES_AND_EYE_PARAMETERS.md'
FIT = EVIDENCE / 'parameters.json'
SOURCE_SHA = '5731cc9064fec4907e8ed8c95ce8b9ff0b0d097159328588850645ce4394744a'
MODULES = {'EAR_L', 'EAR_R', 'HOOF_FORE_L', 'HOOF_FORE_R', 'HOOF_HIND_L', 'HOOF_HIND_R',
           'EYE_L', 'EYE_R', 'EYELID_L', 'EYELID_R'}
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
    mesh = bpy.data.meshes.new(name + '_v003')
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


def eye_surface(chassis):
    bpy.context.view_layer.update()
    data=chassis.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    tree=BVHTree.FromPolygons([v.co for v in data.vertices],
                              [list(p.vertices) for p in data.polygons])
    def surface(y,z):
        p,n,_,_=tree.ray_cast(Vector((-1,y,z)),Vector((1,0,0)))
        if p is None: raise ValueError('eye aperture left facial surface')
        if n.x>0: n=-n
        return p,n
    def offset(y,z,d):
        yy,zz=y,z
        for _ in range(5):
            p,n=surface(yy,zz)
            yy=y-n.y*d;zz=z-n.z*d
        p,n=surface(yy,zz)
        return p+n*d
    return surface,offset


def rebuild_eyes():
    # The opening remains .137 x .149 H. The hidden peripheral cap passes
    # under the lid; the central optical relief is .013 H from the local skin.
    surface,offset=eye_surface(bpy.data.objects['CENTRAL_CHASSIS'])
    n,rings=64,12
    for side,sign in [('L',1),('R',-1)]:
        center_y=sign*.162
        old=bpy.data.objects['EYE_'+side]
        pigment=old.data.materials[0]
        vertices=[tuple(offset(center_y,.418,.013))]
        uv=[(.5,.5)]
        for k in range(1,rings+1):
            r=k/rings
            for j in range(n):
                t=2*math.pi*j/n
                y=center_y+sign*.0685*r*math.cos(t)
                z=.418+.0745*r*math.sin(t)
                # Peripheral optical surface recedes behind its socket rim.
                d=.001+(.012)*(1-r*r)**1.5
                vertices.append(tuple(offset(y,z,d)))
                uv.append(((1+r*math.cos(t))/2,(1+r*math.sin(t))/2))
        faces=[(0,1+j,1+(j+1)%n) for j in range(n)]
        for k in range(rings-1):
            for j in range(n):
                a=1+k*n+j;b=1+k*n+(j+1)%n
                faces.append((a,b,b+n,a+n))
        eye=replace_mesh('EYE_'+side,vertices,faces,[0]*len(faces),[pigment])
        eye['normal_relief_H']=.013
        layer=eye.data.uv_layers.new(name='APERTURE_UV')
        for poly in eye.data.polygons:
            for i in poly.loop_indices:
                layer.data[i].uv=uv[eye.data.loops[i].vertex_index]
        old_lid=bpy.data.objects['EYELID_'+side]
        skin,brown=list(old_lid.data.materials)
        vertices=[]
        for r,d in [(1,.0018),(1.025,.0032),(1.07,.0013),(1.13,-.0006)]:
            for j in range(n):
                t=2*math.pi*j/n
                vertices.append(tuple(offset(center_y+sign*.0685*r*math.cos(t),
                                             .418+.0745*r*math.sin(t),d)))
        faces=[]
        for k in range(3):
            for j in range(n):
                a=k*n+j;b=k*n+(j+1)%n
                faces.append((a,b,b+n,a+n))
        lid=replace_mesh('EYELID_'+side,vertices,faces,
                         [1 if i<n else 0 for i in range(len(faces))],[skin,brown])
        # Keep the v011 upper/lower vertex group contracts for future blink.
        for label,above in [('UPPER_LID',True),('LOWER_LID',False)]:
            group=lid.vertex_groups.get(label) or lid.vertex_groups.new(name=label)
            group.add([i for i,p in enumerate(vertices) if (p[2]>=.418)==above],1,'REPLACE')
    return {'visible_aperture_width_H':.137,'visible_aperture_height_H':.149,
            'visible_centers_y_H':[-.162,.162],
            'central_relief_H':.013,'edge_relief_H':.001,
            'side_bulge_upper_bound_H':.013}


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


def render_eye(view):
    scene=bpy.context.scene
    old_camera=scene.camera
    cam_data=bpy.data.cameras.new('TEMP eye camera')
    cam=bpy.data.objects.new('TEMP eye camera',cam_data)
    scene.collection.objects.link(cam)
    direction={'front':(-4,0,0),'side':(0,-4,0),
               '3q-left':(-3,-3,1.2),'3q-right':(-3,3,1.2)}[view]
    target=(.15,0,.43)
    aim(cam,Vector(target)+Vector(direction),target)
    cam_data.type='ORTHO';cam_data.ortho_scale=.59
    scene.camera=cam
    scene.render.film_transparent=False
    scene.render.resolution_x=800;scene.render.resolution_y=640
    scene.render.resolution_percentage=100
    scene.render.image_settings.color_mode='RGB'
    scene.render.filepath=str(EVIDENCE/f'eye-{view}.png')
    bpy.ops.render.render(write_still=True)
    scene.camera=old_camera
    bpy.data.objects.remove(cam,do_unlink=True)


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    assert PARAMETERS.exists(), 'PARAMETER_FILE_MISSING'
    chosen=json.loads(FIT.read_text(encoding='utf8')) if FIT.exists() else {}
    ear_p={**EAR,**chosen.get('ear',{})}
    hoof_p={**HOOF,**chosen.get('hoof',{})}
    for key, path in [('ear', EAR_IMAGE), ('hoof', HOOF_IMAGE)]:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == IMAGE_HASHES[key]
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    before = {o.name: record(o) for o in bpy.data.objects}
    frozen = {k:v for k,v in before.items() if k not in MODULES}
    cocoa = bpy.data.materials['DEBUG cocoa']
    inset = bpy.data.materials['CAROL ear blush v002']
    for side, suffix in [(1,'L'),(-1,'R')]:
        replace_mesh('EAR_'+suffix, *make_ear(side,ear_p), [cocoa,inset])
    for front, key in [(True,'FORE'),(False,'HIND')]:
        for side, suffix in [(1,'L'),(-1,'R')]:
            cx = .390 if front else .920
            cy = side*(.145 if front else .245)
            replace_mesh('HOOF_'+key+'_'+suffix, *make_hoof(cx,cy,hoof_p), [cocoa])
    eye_metrics=rebuild_eyes()
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
            'starting_branch':'codex/carol-hero-modules-v002',
            'starting_head':'c85b9ab202c5a9a9c663f246300b225ca47b617a',
            'parameter_file_sha256':hashlib.sha256(PARAMETERS.read_bytes()).hexdigest(),
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
            'eye_metrics':eye_metrics,
            'ear_parameters':ear_p,'hoof_parameters':hoof_p,
            'numeric_contract': {'ear_front_angle_degrees':18,
                                 'ear_thickness_intent_H':.028,
                                 'hoof_width_H':.219,'hoof_height_H':.111,
                                 'front_support_x_H':.390,'hind_support_x_H':.920}}
    (EVIDENCE/'validation.json').write_text(json.dumps(data, indent=2)+'\n', encoding='utf8')
    if os.environ.get('CAROL_SKIP_RENDER') == '1':
        print('HERO_MODULES_V003_ASSET_ONLY',flush=True)
        return
    for name, obj, target in [('ear','EAR_R',(.51,-.41,.46)),
                              ('hoof','HOOF_FORE_R',(.39,-.145,.064))]:
        for view in ('front','side','top','3q'):
            render_isolated(name,view,obj,target)
    for view in ('front','side','3q-left','3q-right'):
        render_integrated(view)
        render_eye(view)
    print('HERO_MODULES_V003_COMPLETE', json.dumps({'frozen':len(frozen),'changed':sorted(MODULES)}), flush=True)


if __name__ == '__main__':
    main()
