"""Carol v008 structured cage prototype, built from an empty Blender scene.

blender -b --python scripts/blender/build-carol-v008.py -- --revision 2
Only Skin is implemented until its dual-orthographic internal gate is resolved.
No previous generator is imported. Controls are normalized by H=1.
Continues the pushed selected cycle-2 controls, never the rejected cycle 3.
Selected NEW revision 2; revision 3 worsened the rear jaw and ear-root read.
The revision argument labels output only. It does not switch geometry.
"""
import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
ASSET = ROOT / 'assets/grimo/production/carol/blender/carol-v008.blend'
TMP = ROOT / 'tmp-carol-v008'
REFERENCE = ROOT / 'assets/grimo/source/carol/approved-3d'

# Longitudinal stations: region, X, bottom Z, top Z, half width Y, exponent.
# Independent chest, abdomen and rump controls; these are not the v007 arrays.
TORSO_STATIONS = [
    ('chest', .240, .215, .350, .070, 1.0),
    ('chest', .280, .158, .414, .176, .9),
    ('chest', .365, .118, .458, .253, .9),
    ('chest', .450, .098, .460, .291, .9),
    ('abdomen', .575, .082, .435, .311, .9),
    ('abdomen', .730, .085, .419, .320, .9),
    ('pelvis_rump', .865, .103, .433, .310, .85),
    ('pelvis_rump', .980, .153, .411, .255, .85),
    ('pelvis_rump', 1.043, .228, .357, .125, 1.0),
    ('pelvis_rump', 1.052, .280, .307, .030, 1.0),
]
# Horizontal cranial sections: Z, center X, depth radius X, half width Y.
# Flattened cheek frontage with a rounded deep skull; fixed head placement.
HEAD_SECTIONS = [
    (.223, .285, .040, .060),
    (.233, .265, .145, .175),
    (.266, .263, .236, .279),
    (.322, .268, .262, .309),
    (.408, .285, .270, .301),
    (.492, .300, .265, .283),
    (.577, .321, .243, .266),
    (.651, .331, .190, .219),
    (.695, .332, .100, .133),
    (.703, .332, .020, .025),
]
# The socket is deliberately broad, short and overlapped by head and chest.
SOCKET_STATIONS = [
    ('socket', .345, .231, .334, .148, .8),
    ('socket', .390, .223, .367, .219, .8),
    ('socket', .460, .220, .374, .231, .8),
    ('socket', .510, .246, .350, .185, .8),
]
SUPPORT = {'FORE': {'x': .390, 'y': .145}, 'HIND': {'x': .920, 'y': .245}}
# Z, X offset, inward Y offset, radius X, radius Y. Only the fore transverse
# placement is fitted to Skin Front; the locked longitudinal centers do not move.
FORE_LIMB_SECTIONS = [
    (.074, 0, 0, .065, .071), (.108, 0, 0, .082, .082),
    (.155, .005, .004, .095, .090), (.210, .012, .015, .117, .103),
    (.274, .016, .026, .136, .112), (.335, .023, .040, .123, .098),
    (.385, .030, .050, .064, .060),
]
HIND_LIMB_SECTIONS = [
    (.074, 0, 0, .065, .069), (.110, 0, .004, .080, .077),
    (.163, -.009, .014, .106, .091), (.226, -.028, .042, .133, .111),
    (.286, -.039, .070, .140, .119), (.338, -.047, .090, .106, .089),
    (.370, -.053, .105, .040, .040),
]
TAIL = {'pivot': (.985, 0, .355), 'base': .985, 'center': 1.032,
        'length': .085, 'diameter': .095, 'angle_degrees': 20}
# Region, center XYZ (positive-Y ear), profile radius, thickness, local major.
# The changing frame opens the Side bowl; no rotation of the old global frame.
EAR_STATIONS = [
    ('ROOT', (.397,.221,.565), .028,.023, (.40,.10,.91)),
    ('ROOT', (.420,.275,.533), .071,.025, (.51,.14,.85)),
    ('MID',  (.459,.340,.477), .117,.025, (.61,.18,.77)),
    ('MID',  (.510,.415,.414), .143,.024, (.65,.20,.73)),
    ('MID',  (.566,.484,.382), .127,.023, (.65,.20,.73)),
    ('TIP',  (.619,.543,.377), .085,.021, (.60,.18,.78)),
    ('TIP',  (.651,.573,.385), .040,.016, (.55,.14,.82)),
    ('TIP',  (.661,.581,.388), .008,.007, (.50,.10,.86)),
]
REGISTRATION = {
    'normal-front': dict(file='carol_front.png', h=1011, ground=1162, origin=626.5, view='front'),
    'normal-side': dict(file='carol_side.png', h=916, ground=998, origin=144, view='side'),
    'skin-front': dict(file='carol_skin_front.png', h=994, ground=1075, origin=626.5, view='front'),
    'skin-side': dict(file='carol_skin_side.png', h=1019, ground=1037, origin=64, view='side'),
}
REFERENCE_HASHES = {
    'carol_front.png': '164a646fbb2f335029e875a09ee4c337f52d8a09f650437420a6f1f83e024197',
    'carol_side.png': '9484b7ac49b9d53a517e7f05af6ca4f67f8cc8907cfbfedffe6d51cda2d829b8',
    'carol_skin_front.png': 'be21b4ae23578deaca664e77ded2bd225a10693f5b2c01ad0c53e6ae49f9c6b2',
    'carol_skin_side.png': 'bd16825f4e43fd0f6a22f425b5d32f322b83739dd00967cda40fb2c0a2c7b816',
}


def material(name, color, roughness=.65):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value = (*color, 1)
    node.inputs['Roughness'].default_value = roughness
    return mat


def mesh(name, vertices, faces, mat, subdivision=0):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    bm = bmesh.new()
    bm.from_mesh(data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(data)
    bm.free()
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    data.materials.append(mat)
    for polygon in data.polygons:
        polygon.use_smooth = True
    if subdivision:
        sub = obj.modifiers.new('Editable Catmull-Clark surface', 'SUBSURF')
        sub.subdivision_type = 'CATMULL_CLARK'
        sub.levels = subdivision
        sub.render_levels = subdivision
    return obj


def ring_faces(count, n):
    faces = []
    for i in range(count - 1):
        for j in range(n):
            a, b = i * n + j, i * n + (j + 1) % n
            faces.append((a, b, b + n, a + n))
    # Tiny end disks have quad fan caps (no huge concave ngon).
    for start in [0, (count - 1) * n]:
        for j in range(1, n - 2, 2):
            faces.append((start, start+j, start+j+1, start+j+2))
    return faces


def signed_power(value, exponent):
    return math.copysign(abs(value) ** exponent, value)


def longitudinal_cage(name, stations, mat, n=16):
    vertices = []
    for region, x, bottom, top, width, exponent in stations:
        for j in range(n):
            theta = 2 * math.pi * j / n
            vertices.append((x, width * signed_power(math.sin(theta), exponent),
                             (bottom+top)/2 + (top-bottom)/2 * signed_power(math.cos(theta), exponent)))
    obj = mesh(name, vertices, ring_faces(len(stations), n), mat, 2)
    for region in dict.fromkeys(station[0] for station in stations):
        group = obj.vertex_groups.new(name=region)
        for i, station in enumerate(stations):
            if station[0] == region:
                group.add(list(range(i*n, (i+1)*n)), 1.0, 'REPLACE')
    return obj


def horizontal_cage(name, sections, mat, y=0, face=False, n=16):
    vertices = []
    for z, center, rx, ry in sections:
        for j in range(n):
            theta = 2 * math.pi * j / n
            c, s = math.cos(theta), math.sin(theta)
            power = (2.7 if c < 0 else .85) if face else 1.0
            vertices.append((center + rx*signed_power(c, power),
                             y + ry*signed_power(s, .90 if face else 1), z))
    obj = mesh(name, vertices, ring_faces(len(sections), n), mat, 2)
    if face:
        for region,indices in [('LOWER_CHEEK',range(4)),('FACE',range(3,6)),
                               ('FOREHEAD',range(5,8)),('SKULL',range(7,len(sections)))]:
            group = obj.vertex_groups.new(name=region)
            for i in indices:
                group.add(list(range(i*n,(i+1)*n)),1,'REPLACE')
    return obj


def limb(name, row, x, y, sign, mat):
    sections = FORE_LIMB_SECTIONS if row == 'FORE' else HIND_LIMB_SECTIONS
    n = 16
    vertices = []
    for z, dx, inward, rx, ry in sections:
        for j in range(n):
            theta = 2*math.pi*j/n
            vertices.append((x+dx+rx*math.cos(theta),
                             y-sign*inward+ry*math.sin(theta),z))
    obj = mesh(name,vertices,ring_faces(len(sections),n),mat,2)
    for region,indices in [('DISTAL',range(2)),('SHORT_TAPER',range(2,4)),
                           ('BURIED_PROXIMAL',range(4,len(sections)))]:
        group = obj.vertex_groups.new(name=region)
        for i in indices:
            group.add(list(range(i*n,(i+1)*n)),1,'REPLACE')
    return obj


def ellipsoid(name, location, scale, mat):
    # Reserved for the small eye/nose modules, never primary body construction.
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=24, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    return obj


def tube(name, points, radius, mat):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = radius
    curve.bevel_resolution = 3
    spline = curve.splines.new('POLY')
    spline.points.add(len(points)-1)
    for point, co in zip(spline.points, points):
        point.co = (*co, 1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.scene.collection.objects.link(obj)
    curve.materials.append(mat)
    return obj


def hoof(name, x, y, mat):
    # Retains v007's successful planted, broad two-toe concept.
    vertices = []
    n = 32
    for z, radius in [(0,.85), (.004,.96), (.030,1.03), (.070,.99), (.102,.70), (.111,.18)]:
        for j in range(n):
            theta = 2*math.pi*j/n
            yy = .1095*math.sin(theta)*radius
            xx = .109*math.cos(theta)*radius
            if xx < 0:
                xx += .017*math.exp(-(yy/.018)**2)
            vertices.append((x+xx, y+yy, z))
    obj = mesh(name, vertices, ring_faces(6,n), mat, 2)
    # All bottom cap vertices lie on ground and a close support ring holds them.
    return obj


def ear(name, sign, brown, pink):
    vertices = []
    count, n = len(EAR_STATIONS), 16
    for i, (_, xyz, width, thickness, direction) in enumerate(EAR_STATIONS):
        center = Vector((xyz[0], sign*xyz[1], xyz[2]))
        major = Vector((direction[0],sign*direction[1],direction[2])).normalized()
        before = Vector(EAR_STATIONS[max(0,i-1)][1])
        after = Vector(EAR_STATIONS[min(count-1,i+1)][1])
        tangent = after-before
        tangent.y *= sign
        normal = tangent.cross(major).normalized()*(-sign)
        for j in range(n):
            theta = 2*math.pi*j/n
            # A soft closed bowl: its lower half cups toward the front/side.
            bowl = .012*math.sin(math.pi*i/(count-1))*max(0,-math.cos(theta))
            vertices.append(tuple(center+major*width*math.cos(theta)
                                  +normal*(thickness*math.sin(theta)+bowl)))
    obj = mesh(name, vertices, ring_faces(count,n), brown, 2)
    obj.data.materials.append(pink)
    for polygon in obj.data.polygons:
        if polygon.index < (count-1)*n:
            i,j = divmod(polygon.index,n)
            if 1 <= i <= 5 and 4 <= j <= 6:
                polygon.material_index = 1
    for region in ['ROOT','MID','TIP']:
        group = obj.vertex_groups.new(name=region)
        for i, station in enumerate(EAR_STATIONS):
            if station[0] == region:
                group.add(list(range(i*n,(i+1)*n)),1,'REPLACE')
    return obj


def debug_landmark(name, location):
    obj = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    obj.empty_display_size = .025
    obj.hide_render = True
    obj['DEBUG'] = obj['NON_EXPORT'] = obj['NON_PRODUCTION'] = True
    return obj


def camera(name, location, target):
    data = bpy.data.cameras.new(name)
    obj = bpy.data.objects.new(name,data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
    data.type = 'ORTHO'
    data.ortho_scale = 1.52
    return obj


def geometry_digest():
    payload = []
    for obj in sorted(bpy.context.scene.objects, key=lambda ob: ob.name):
        if obj.type in {'MESH', 'CURVE'}:
            payload.append((obj.name, [list(row) for row in obj.matrix_world],
                            [list(v.co) for v in obj.data.vertices] if obj.type=='MESH'
                            else [[list(p.co) for p in s.points] for s in obj.data.splines]))
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def attachment_diagnostics():
    """Disposable evaluated-surface probes; no scene mutation or approval score.

    Surface intersections establish contact, not acceptable penetration or
    deformation. Tail rotation uses its real pivot and the evaluated neutral
    core. Visual motion clearance remains gated by unresolved neutral Skin.
    """
    depsgraph = bpy.context.evaluated_depsgraph_get()

    def surface(name, transform=None):
        obj = bpy.data.objects[name].evaluated_get(depsgraph)
        coords = [obj.matrix_world@v.co for v in obj.data.vertices]
        if transform is not None:
            coords = [transform@point for point in coords]
        return BVHTree.FromPolygons(coords,[list(p.vertices) for p in obj.data.polygons])

    torso = surface('TORSO_CAGE')
    tail = {}
    pivot = Vector(TAIL['pivot'])
    for name,axis,degrees in [('neutral','Y',0),('up_20','Y',-20),
                              ('down_20','Y',20),('lateral_L_7','Z',7),
                              ('lateral_R_7','Z',-7)]:
        transform = (Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(degrees),4,axis)
                     @ Matrix.Translation(-pivot))
        tail[name] = {'surface_intersection_pairs':len(torso.overlap(surface('SKIN_TAIL_CORE',transform)))}
    neutral_contacts = {}
    for name in ['HEAD_CAGE','FORE_L','FORE_R','HIND_L','HIND_R']:
        neutral_contacts[name] = {'torso_surface_intersection_pairs':len(torso.overlap(surface(name)))}
    return dict(method='Evaluated mesh BVH surface intersections; virtual tail pivot transforms; no scene changes.',
                tail_pivot_probes=tail,neutral_torso_contacts=neutral_contacts,
                interpretation='Contact diagnostic only. Pair counts do not measure penetration quality or grant clearance.',
                visual_motion_clearance='NOT REACHED: neutral Skin revision gate blocked')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision', type=int, choices=[1,2,3], default=2)
    parser.add_argument('--resolution', type=int, default=640)
    options = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    output = TMP / ('revision-'+str(options.revision))
    output.mkdir(parents=True, exist_ok=True)
    for name, expected in REFERENCE_HASHES.items():
        actual = hashlib.sha256((REFERENCE/name).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError('Locked reference changed: '+name)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.seed = 0
    scene.cycles.use_animated_seed = False
    scene.cycles.use_denoising = True
    scene.render.resolution_x = scene.render.resolution_y = options.resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'AgX'
    scene.world.color = (.4,.4,.4)
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 12
    scene['authority'] = 'Four FINAL LOCKED references + CAROL_GEOMETRY_PARAMETERS.md'
    scene['coordinate_contract'] = 'H=1; X front to rear; Y bilateral; Z up; ground Z=0'
    scene['stage'] = 'BLOCKED_AT_V008_SKIN_REVISION_GATE; selected revision 2; Human Gate PENDING'
    scene['saved_pose'] = 'NEUTRAL'
    cream = material('DEBUG warm skin',(.83,.67,.55))
    brown = material('DEBUG cocoa',(.19,.075,.039))
    pink = material('DEBUG ear inset',(.64,.23,.20))
    dark = material('DEBUG eye',(.022,.012,.018),.16)
    amber = material('DEBUG amber',(.32,.13,.033),.25)
    white = material('DEBUG glint',(.98,.98,1),.18)
    longitudinal_cage('TORSO_CAGE', TORSO_STATIONS, cream)
    horizontal_cage('HEAD_CAGE', HEAD_SECTIONS, cream, face=True, n=24)
    longitudinal_cage('SHORT_NECK_SOCKET', SOCKET_STATIONS, cream)
    for side, sign in [('L',1),('R',-1)]:
        for row, control in SUPPORT.items():
            x, y = control['x'], sign*control['y']
            limb(row+'_'+side,row,x,y,sign,cream)
            hoof('HOOF_'+row+'_'+side,x,y,brown)
        ear('EAR_'+side,sign,brown,pink)
        eye = ellipsoid('EYE_'+side,(.104,sign*.162,.398),(.038,.089,.0745),dark)
        eye.rotation_euler.z = sign*math.radians(-45)
        rim = []
        for j in range(65):
            t = 2*math.pi*j/64
            rim.append((.104+.063*math.sin(t),sign*(.162+.063*math.sin(t)),.398+.0745*math.cos(t)))
        tube('EYELID_'+side,rim,.0055,brown)
        glint = ellipsoid('GLINT_'+side,(.075,sign*.170,.432),(.010,.015,.016),white)
        glint.rotation_euler = eye.rotation_euler.copy()
        iris = ellipsoid('IRIS_'+side,(.080,sign*.186,.36),(.006,.029,.020),amber)
        iris.rotation_euler = eye.rotation_euler.copy()
    ellipsoid('NOSE',(.011,0,.378),(.017,.0195,.0105),brown)
    mouth = []
    for j in range(49):
        y = -.0455+.091*j/48
        mouth.append((.009+.009*(y/.0455)**2,y,.35-.010*math.sin(math.pi*abs(y)/.0455)))
    tube('MOUTH_closed',mouth,.0028,brown)
    tube('PHILTRUM',[(.007,0,.370),(.008,0,.350)],.0025,brown)
    pivot = debug_landmark('TAIL_PIVOT', TAIL['pivot'])
    debug_landmark('DEBUG_HEAD_PIVOT', (.410,0,.370))
    debug_landmark('DEBUG_COM', (.630,0,.255))
    debug_landmark('DEBUG_FOREHEAD', (.090,0,.535))
    for side,sign in [('L',1),('R',-1)]:
        debug_landmark('DEBUG_EAR_ROOT_'+side, (.397,sign*.221,.565))
        debug_landmark('DEBUG_CHEEK_'+side, (.090,sign*.250,.320))
        for row,control in SUPPORT.items():
            debug_landmark('DEBUG_'+row+'_SUPPORT_'+side, (control['x'],sign*control['y'],0))
    tuft_stations = []
    for dx, radius in [(-.0425,.008),(-.034,.031),(-.014,.049),(.014,.049),(.034,.031),(.0425,.006)]:
        z = .355+dx*math.tan(math.radians(TAIL['angle_degrees']))
        tuft_stations.append(('tuft',TAIL['center']+dx,z-radius,z+radius,radius,1.0))
    tuft = longitudinal_cage('SKIN_TAIL_CORE',tuft_stations,cream,12)
    for obj in [tuft]:
        obj.parent = pivot
        obj.matrix_parent_inverse = Matrix.Translation(-pivot.location)
    reference_collection = bpy.data.collections.new('REFERENCES locked H-registered')
    scene.collection.children.link(reference_collection)
    for reg in REGISTRATION.values():
        path = REFERENCE/reg['file']
        im = bpy.data.images.load(str(path),check_existing=True)
        width,height = im.size[:]
        obj = bpy.data.objects.new('REFERENCE '+reg['file'],None)
        reference_collection.objects.link(obj)
        obj.empty_display_type = 'IMAGE'
        obj.data = im
        obj.empty_display_size = width/reg['h']
        obj.color[3] = .35
        horizontal = (width/2-reg['origin'])/reg['h']
        vertical = (reg['ground']-height/2)/reg['h']
        if reg['view']=='front':
            obj.matrix_world = Matrix(((0,0,-1,1.4),(-1,0,0,-horizontal),(0,1,0,vertical),(0,0,0,1)))
        else:
            obj.matrix_world = Matrix(((1,0,0,horizontal),(0,0,-1,1),(0,1,0,vertical),(0,0,0,1)))
        obj.hide_render = True
        for key in ['h','ground','origin']:
            obj[key] = reg[key]
        im.filepath = '//'+os.path.relpath(path,ASSET.parent).replace('\\','/')
    reference_collection.hide_viewport = True
    cameras = {'front':camera('CAM front',(-4,0,.5),(.5,0,.5)),
               'side':camera('CAM side',(.65,-4,.5),(.65,0,.5))}
    for name,loc,power,size in [('key',(-3,-4,5),450,4),('fill',(-2,3,2),250,3),
                                 ('rim',(3,0,4),350,3),('low fill',(-3,0,.2),90,3)]:
        data = bpy.data.lights.new(name,'AREA')
        data.energy, data.size, data.shape = power,size,'DISK'
        obj = bpy.data.objects.new(name,data)
        scene.collection.objects.link(obj)
        obj.location = loc
        obj.rotation_euler = (Vector((.5,0,.4))-obj.location).to_track_quat('-Z','Y').to_euler()
    bpy.context.view_layer.update()
    neutral_digest = geometry_digest()
    view_digests = {}
    for view in ['front','side']:
        scene.camera = cameras[view]
        view_digests[view] = geometry_digest()
        assert view_digests[view] == neutral_digest
        scene.render.filepath = str(output/('skin-'+view+'.png'))
        bpy.ops.render.render(write_still=True)
    scene.camera = cameras['front']
    diagnostics = attachment_diagnostics()
    assert geometry_digest() == neutral_digest, 'Diagnostic changed the neutral scene'
    assert SUPPORT['FORE']['x'] == .390 and SUPPORT['HIND']['x'] == .920
    assert all(probe['surface_intersection_pairs'] > 0
               for probe in diagnostics['tail_pivot_probes'].values()), 'Tail/rump contact lost'
    assert not any(obj.type == 'ARMATURE' or obj.animation_data for obj in scene.objects)
    assert not any(mod.type in {'BOOLEAN','REMESH','ARMATURE'}
                   for obj in scene.objects for mod in obj.modifiers)
    ASSET.parent.mkdir(parents=True,exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    depsgraph = bpy.context.evaluated_depsgraph_get()
    meshes = {}
    for obj in scene.objects:
        if obj.type != 'MESH':
            continue
        evaluated = obj.evaluated_get(depsgraph)
        coords = [evaluated.matrix_world@v.co for v in evaluated.data.vertices]
        meshes[obj.name] = dict(control_vertices=len(obj.data.vertices),
            control_faces=len(obj.data.polygons), all_quads=all(len(p.vertices)==4 for p in obj.data.polygons),
            modifiers=[mod.type for mod in obj.modifiers],
            min=[min(p[i] for p in coords) for i in range(3)],
            max=[max(p[i] for p in coords) for i in range(3)])
    result = dict(blender=bpy.app.version_string,revision=options.revision,
        stage='Skin revision gate',human_geometry_gate='PENDING; not ready for submission',
        executor_disposition='BLOCKED_AT_V008_SKIN_REVISION_GATE',
        selected_geometry_revision=2,skin_revision_render_cycles_completed=3,
        baseline_commit='601296e8e44f7eb4e6f9843bedcca61f940d7abb',
        generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        reference_hashes=REFERENCE_HASHES,reference_registration=REGISTRATION,
        geometry_digest=neutral_digest,view_geometry_digests=view_digests,
        support_targets=SUPPORT,tail_controls=TAIL,ear_stations=EAR_STATIONS,meshes=meshes,
        tail_core_rump_X_overlap_H=meshes['TORSO_CAGE']['max'][0]-meshes['SKIN_TAIL_CORE']['min'][0],
        tail_fleece_shell='NOT CONSTRUCTED; Skin gate prerequisite',
        debug_landmarks={obj.name:list(obj.location) for obj in scene.objects if obj.get('NON_PRODUCTION')},
        attachment_diagnostics=diagnostics,
        motion_clearance={
            'head_yaw_clearance':'NOT REACHED; head/chest neutral fitting blocked',
            'head_pitch_clearance':'NOT REACHED; head/chest neutral fitting blocked',
            'head_tilt_clearance':'NOT REACHED; head/chest neutral fitting blocked',
            'cheek_lean_clearance':'NOT REACHED; neutral Skin gate blocked',
            'ear_clearance':'NOT REACHED; neutral ear shape blocked; ROOT/MID/TIP groups only',
            'com_shift_clearance':'NOT REACHED; neutral contact diagnostics do not prove weight transfer',
            'fore_support_clearance':'NOT REACHED; buried root and planted neutral geometry only',
            'tail_clearance':'Evaluated core/rump surfaces intersect at neutral, +/-20 vertical and +/-7 lateral; visual motion not approved',
            'fleece_regional_clearance':'NOT REACHED; fleece not constructed'},
        saved_pose='NEUTRAL',
        fleece_representation='NOT CONSTRUCTED; Skin gate prerequisite',
        voxel_remesh_fleece=False,boolean_ear_recess=False,view_specific_geometry=False,
        normal_skin_identity='Normal not constructed; one neutral underbody only',
        production_rig=False,animation=False,final_retopology=False,
        limitations=['Ear Side still reads triangular instead of a broad soft bowl; Front inset/rim differs.',
                     'Head/chest transition remains visibly segmented; articulation clearance unproven.',
                     'Proximal roots improved but support silhouettes remain insufficiently reference-fitted.',
                     'Skin Side support registration and Skin Front imply different skull heights.',
                     'Technical diagnostics do not grant Human approval.'])
    (output/'measurements.json').write_text(json.dumps(result,indent=2)+'\n')
    print('V008_BUILD_COMPLETE '+str(output))


if __name__ == '__main__':
    main()
