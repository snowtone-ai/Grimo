"""Carol v008 structured cage prototype, built from an empty Blender scene.

blender -b --python scripts/blender/build-carol-v008.py -- --revision 14
Only Skin is implemented until its dual-orthographic internal gate is resolved.
No previous generator is imported. Controls are normalized by H=1.
Continues pushed revision 12 at 4c3e55b. Local Human appeal fit, Skin only.
The revision argument labels the selected output; no historical geometry switch.
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
import numpy as np
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
    ('chest', .365, .118, .458, .248, .9),
    ('chest', .450, .103, .440, .284, .9),
    ('abdomen', .575, .089, .414, .303, .9),
    ('abdomen', .730, .092, .410, .305, .9),
    ('pelvis_rump', .865, .102, .417, .300, .85),
    ('pelvis_rump', .980, .145, .392, .248, .85),
    ('pelvis_rump', 1.043, .228, .357, .125, 1.0),
    ('pelvis_rump', 1.052, .280, .307, .030, 1.0),
]
# Horizontal cranial sections: Z, center X, depth radius X, half width Y.
# Rounded skull with local muzzle and orbital housing; one shared placement.
HEAD_SECTIONS = [
    (.235, .285, .040, .070),
    (.248, .266, .145, .173),
    (.272, .260, .212, .256),
    (.315, .266, .247, .300),
    (.340, .275, .256, .303),
    (.375, .288, .260, .304),
    (.400, .296, .257, .302),
    (.430, .304, .253, .296),
    (.460, .311, .254, .288),
    (.500, .320, .257, .277),
    (.570, .334, .253, .253),
    (.630, .344, .210, .218),
    (.674, .345, .148, .164),
    (.697, .342, .072, .080),
    (.703, .340, .015, .018),
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
    (.074, .008, 0, .059, .063), (.108, .005, 0, .075, .076),
    (.155, .005, .004, .095, .090), (.210, .012, .015, .117, .103),
    (.274, .016, .026, .136, .112), (.335, .023, .040, .123, .098),
    (.385, .030, .050, .064, .060),
]
HIND_LIMB_SECTIONS = [
    (.074, .008, 0, .059, .062), (.110, .005, .004, .073, .073),
    (.163, -.009, .014, .106, .091), (.226, -.028, .042, .133, .111),
    (.286, -.039, .070, .140, .119), (.338, -.047, .090, .106, .089),
    (.370, -.053, .105, .040, .040),
]
TAIL = {'pivot': (.985, 0, .355), 'base': .985, 'center': 1.032,
        'length': .085, 'diameter': .095, 'angle_degrees': 20}
# One 3D perimeter, independently controlled inner lip, and finite shell depth.
# Positive-Y controls mirrored for the other ear; neither camera affects them.
EAR_PERIMETER = [
    (.390,.220,.611), (.440,.295,.600), (.530,.400,.540),
    (.630,.510,.465), (.680,.570,.430), (.700,.590,.390),
    (.697,.590,.353), (.675,.561,.323), (.640,.520,.305),
    (.585,.460,.294), (.530,.402,.298), (.475,.341,.322),
    (.430,.295,.362), (.398,.260,.428), (.375,.225,.510),
    (.375,.215,.577),
]
EAR_INNER_LIP = [
    (.402,.245,.530), (.445,.300,.468), (.515,.380,.430),
    (.595,.470,.429), (.655,.540,.420), (.670,.554,.388),
    (.661,.546,.350), (.637,.518,.329), (.608,.485,.317),
    (.565,.436,.310), (.518,.382,.320), (.475,.334,.344),
    (.444,.302,.383), (.425,.275,.440), (.400,.255,.490),
    (.395,.240,.525),
]
EAR_ROOT_SADDLE = {
    13:(.385,.240,.445),14:(.360,.210,.500),15:(.360,.210,.560),
    0:(.380,.220,.590),1:(.415,.260,.590),
}
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


def cranial_depth(c):
    """C1 cheek-to-skull join; central frontage and rear apex stay fixed.

    The old 2.7/.85 powers met at c=0 with zero/infinite slopes. Match their
    values and derivatives outside the local side band instead of retracting
    entire jaw rings or changing the face/eye frontage.
    """
    edge = .70
    if c <= -edge:
        return signed_power(c,2.7)
    if c >= edge:
        return signed_power(c,.85)
    t = (c+edge)/(2*edge)
    a,b = -edge**2.7,edge**.85
    da,db = 2.7*edge**1.7,.85*edge**(-.15)
    return ((2*t**3-3*t*t+1)*a+(t**3-2*t*t+t)*2*edge*da
            +(-2*t**3+3*t*t)*b+(t**3-t*t)*2*edge*db)


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
            depth = cranial_depth(c) if face else c
            # Smoothly lift only the rear lower cranial quadrant. Face center,
            # skull top, muzzle and primary facial modules are untouched.
            rear = max(0,min(1,(c+.50)/1.50))
            rear = rear*rear*(3-2*rear)
            low = max(0,min(1,(.43-z)/.20)) if face else 0
            muzzle = (.020*math.exp(-((z-.368)/.049)**2)
                      *math.exp(-(ry*s/.080)**2)*max(0,-c)**8) if face else 0
            yy=y + ry*signed_power(s, .90 if face else 1)
            xx=center + rx*depth-muzzle
            if face and c<0:
                # Orbital housing belongs to the head itself. A nearly upright
                # oblique surface explains both eyes without a separate globe.
                u=(abs(yy)-.162)/.0685
                v=(z-.418)/.0745
                r=math.sqrt(u*u+v*v)
                t=max(0,min(1,(1.75-r)/.65))
                weight=t*t*(3-2*t)
                target=.145+(abs(yy)-.162)*1.02+.006*v*v
                xx=xx*(1-weight)+target*weight
            vertices.append((xx, yy, z+.065*rear*low*low))
    obj = mesh(name, vertices, ring_faces(len(sections), n), mat, 2)
    if face:
        for region,indices in [('LOWER_CHEEK',range(4)),('FACE',range(3,10)),
                               ('FOREHEAD',range(9,13)),('SKULL',range(12,len(sections)))]:
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
    # Reserved for the tiny nose, never primary body or eye construction.
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
    # One planted sole and one crown, with three shallow anterior toe lobes.
    vertices = []
    n = 96
    rings = [(0,.80,.80),(.006,.90,.90),(.018,.98,.98),(.040,1,1),
             (.066,.98,.98),(.087,.90,.90),(.101,.76,.76),
             (.111,.56,.56),(.112,.04,.04)]
    for z, x_scale, y_scale in rings:
        for j in range(n):
            theta = 2*math.pi*j/n
            c = math.cos(theta)
            yy = .1095*math.sin(theta)*y_scale
            xx = (.105 if c < 0 else .085)*c*x_scale
            frontness = max(0,-c)**1.5
            cleft_signal = min(1,math.exp(-.5*((yy+.0365)/.010)**2)
                               +math.exp(-.5*((yy-.0365)/.010)**2))
            rise = min(1,max(0,(z-.010)/.015))
            fall = min(1,max(0,(.105-z)/.030))
            height_mask = rise*rise*(3-2*rise)*fall*fall*(3-2*fall)
            cleft = cleft_signal*frontness*height_mask
            xx += .011*cleft
            zz = z+.0025*cleft
            vertices.append((x+xx, y+yy, zz))
    obj = mesh(name, vertices, ring_faces(len(rings),n), mat, 2)
    obj['toe_lobe_count'] = 3
    obj['cleft_count'] = 2
    return obj


def eye_pixels(gaze=(0,0)):
    """Neutral pigment, with optional disposable iris-only gaze offset."""
    size = 512
    v,u = np.mgrid[-1:1:complex(size),-1:1:complex(size)]
    radius = np.sqrt(u*u+v*v)
    iris_u,iris_v=u-gaze[0],v-gaze[1]
    color = np.zeros((size,size,3),dtype=np.float32)
    color[:] = (.019,.010,.018)
    def mix(rgb, mask):
        nonlocal color
        color = color*(1-mask[...,None])+np.array(rgb)*mask[...,None]
    lower = np.clip((-v+.10)/1.05,0,1)*np.clip((.97-radius)/.18,0,1)
    mix((.21,.065,.024), lower*.85)
    for cx,cy,rx,ry,opacity in [(-.38,-.32,.28,.33,.30),(.40,-.37,.28,.30,.37),
                                 (-.12,-.08,.25,.30,.35)]:
        q=((iris_u-cx)/rx)**2+((iris_v-cy)/ry)**2
        mix((.42,.15,.047),np.clip((1-q)*5,0,1)*opacity)
    q=(iris_u/.39)**2+((iris_v+.62)/.30)**2
    glow=np.clip((1-q)*6,0,1)
    mix((.95,.46,.070),glow)
    mix((1,.70,.19),glow*np.clip((-.4-v)/.55,0,1)*.65)
    # Narrow warm limbal edge stays on the eye surface.
    rim=np.clip((radius-.89)/.09,0,1)*np.clip((1.02-radius)/.04,0,1)
    mix((.27,.078,.033),rim*.70)
    for cx,cy,rx,ry in [(-.28,.53,.22,.22),(-.07,.27,.067,.065)]:
        q=((u-cx)/rx)**2+((v-cy)/ry)**2
        mix((1,1,1),np.clip((1-q)*12,0,1))
    star=(np.abs((u-.42)/.20)**.55+np.abs((v+.20)/.20)**.55)
    mix((1,.96,.88),np.clip((1-star)*15,0,1))
    pixels=np.ones((size,size,4),dtype=np.float32)
    pixels[:,:,:3]=color
    return pixels


def eye_material():
    """One packed UV pigment on a curved aperture; no iris/glint solids."""
    pixels=eye_pixels()
    size=pixels.shape[0]
    im=bpy.data.images.new('EYE pigment diagnostic packed',width=size,height=size)
    im.colorspace_settings.name='Non-Color'
    im.pixels.foreach_set(pixels.ravel())
    im.pack()
    mat=material('DEBUG conformal eye pigment',(.04,.02,.02),.24)
    nodes=mat.node_tree.nodes
    texture=nodes.new('ShaderNodeTexImage')
    texture.image=im
    shader=nodes.get('Principled BSDF')
    shader.inputs['Specular IOR Level'].default_value=.32
    shader.inputs['Coat Weight'].default_value=.20
    shader.inputs['Coat Roughness'].default_value=.20
    mat.node_tree.links.new(texture.outputs['Color'],shader.inputs['Base Color'])
    return mat


def facial_surface(head):
    bpy.context.view_layer.update()
    evaluated=head.evaluated_get(bpy.context.evaluated_depsgraph_get())
    tree=BVHTree.FromPolygons([evaluated.matrix_world@v.co for v in evaluated.data.vertices],
                             [list(p.vertices) for p in evaluated.data.polygons])
    def sample(y,z,relief=0):
        hit=tree.ray_cast(Vector((-1,y,z)),Vector((1,0,0)))
        if hit[0] is None:
            raise RuntimeError('Facial patch left cranial surface')
        return (hit[0].x-relief,y,z)
    return sample


def conformal_eye(side,sign,sample,pigment,skin,brown):
    n, rings = 96,24
    verts=[sample(sign*.162,.418,.014)]
    uv=[(.5,.5)]
    for k in range(1,rings+1):
        r=k/rings
        for j in range(n):
            angle=2*math.pi*j/n
            u,v=r*math.cos(angle),r*math.sin(angle)
            verts.append(sample(sign*(.162+.0685*u),.418+.0745*v,
                                .0008+.0132*(1-r*r)))
            uv.append(((u+1)/2,(v+1)/2))
    faces=[(0,1+j,1+(j+1)%n) for j in range(n)]
    for k in range(rings-1):
        for j in range(n):
            a=1+k*n+j;b=1+k*n+(j+1)%n
            faces.append((a,b,b+n,a+n))
    obj=mesh('EYE_'+side,verts,faces,pigment)
    layer=obj.data.uv_layers.new(name='APERTURE_UV')
    for polygon in obj.data.polygons:
        for loop in polygon.loop_indices:
            layer.data[loop].uv=uv[obj.data.loops[loop].vertex_index]
    obj['architecture']='head-conformal shallow patch; no globe'
    obj['maximum_relief_H']=.014
    # A broad, skin-colored transition with a very narrow pigmented inner edge.
    verts=[]
    for r,relief in [(1,.0012),(1.025,.0020),(1.065,.0010),(1.13,-.0003)]:
        for j in range(n):
            a=2*math.pi*j/n
            verts.append(sample(sign*(.162+.0685*r*math.cos(a)),
                                .418+.0745*r*math.sin(a),relief))
    faces=[]
    for k in range(3):
        for j in range(n):
            a=k*n+j;b=k*n+(j+1)%n
            faces.append((a,b,b+n,a+n))
    lid=mesh('EYELID_'+side,verts,faces,skin)
    lid.data.materials.append(brown)
    for p in lid.data.polygons:
        if p.index<n: p.material_index=1
    return obj


def ear(name, sign, brown, pink):
    normal = Vector((-.76,.65,0)).normalized()
    outside = [Vector(p) for p in EAR_PERIMETER]
    inside = [Vector(p) for p in EAR_INNER_LIP]
    center = Vector((.543,.408,.377))
    # Walk from tiny back cap, across back shell and rolled perimeter, into
    # the recessed bowl. The inset is part of this mesh, never an overlay card.
    loops = [
        [center+(p-center)*.025-normal*.018 for p in outside],
        [center+(p-center)*.55-normal*.021 for p in outside],
        [p-normal*.009 for p in outside],
        [p+normal*.009 for p in outside],
        [p+normal*.012 for p in inside],
        [center+(p-center)*.60-normal*.001 for p in inside],
        [center+(p-center)*.025-normal*.006 for p in inside],
    ]
    # The back shell has a buried, rounded saddle under the skull. Its distal
    # perimeter and bowl stay unchanged; the rim fades into this wider root.
    for index,co in EAR_ROOT_SADDLE.items():
        loops[1][index] = Vector(co)
    vertices = [(p.x,sign*p.y,p.z) for loop in loops for p in loop]
    n = len(outside)
    obj = mesh(name, vertices, ring_faces(len(loops),n), brown, 2)
    obj.data.materials.append(pink)
    for polygon in obj.data.polygons:
        if 4*n <= polygon.index < 6*n or polygon.index >= 6*n+(n-2)//2:
            polygon.material_index = 1
    for region in ['ROOT','MID','TIP']:
        group = obj.vertex_groups.new(name=region)
        for i,vertex in enumerate(vertices):
            u = max(0,min(1,(abs(vertex[1])-.24)/.33))
            weights = {'ROOT':max(0,1-2*u),'MID':1-abs(2*u-1),'TIP':max(0,2*u-1)}
            if weights[region] > 0:
                group.add([i],weights[region],'REPLACE')
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
                visual_motion_clearance='Separate disposable visual probes: carol-v008-clearance.py; no automatic PASS')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision', type=int, choices=[14], default=14)
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
    scene['stage'] = 'BLOCKED_AT_V008_SKIN_IDENTITY_FIT; Human Gate PENDING'
    scene['selected_revision'] = options.revision
    scene['saved_pose'] = 'NEUTRAL'
    cream = material('DEBUG warm skin',(.83,.67,.55))
    brown = material('DEBUG cocoa',(.19,.075,.039))
    pink = material('DEBUG ear inset',(.64,.23,.20))
    pigment = eye_material()
    longitudinal_cage('TORSO_CAGE', TORSO_STATIONS, cream)
    head = horizontal_cage('HEAD_CAGE', HEAD_SECTIONS, cream, face=True, n=64)
    sample = facial_surface(head)
    longitudinal_cage('SHORT_NECK_SOCKET', SOCKET_STATIONS, cream)
    for side, sign in [('L',1),('R',-1)]:
        for row, control in SUPPORT.items():
            x, y = control['x'], sign*control['y']
            limb(row+'_'+side,row,x,y,sign,cream)
            hoof('HOOF_'+row+'_'+side,x,y,brown)
        ear('EAR_'+side,sign,brown,pink)
        conformal_eye(side,sign,sample,pigment,cream,brown)
    # Retain the exact revision-12 nose placement despite lower-cheek smoothing.
    nose_x=.004725804552435875
    ellipsoid('NOSE',(nose_x,0,.378),(.017,.0195,.0105),brown)
    mouth = []
    for j in range(49):
        y = -.0455+.091*j/48
        z=.3542-.0065*math.sin(math.pi*abs(y)/.0455)
        mouth.append(sample(y,z,.002))
    tube('MOUTH_closed',mouth,.0028,brown)
    tube('PHILTRUM',[sample(0,.370,.002),sample(0,.3542,.002)],.0025,brown)
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
    for dx, radius in [(-.0425,.004),(-.036,.025),(-.027,.0365),(-.014,.0445),
                       (0,.0475),(.014,.0445),(.027,.0365),(.036,.025),(.0425,.004)]:
        z = .355
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
    baseline = json.loads((ROOT/'docs/production/carol/evidence/reconstruction-v008/baseline-revision-12/measurements.json').read_text())
    previous_contacts = baseline['attachment_diagnostics']['neutral_torso_contacts']
    contact_ratios = {name:diagnostics['neutral_torso_contacts'][name]['torso_surface_intersection_pairs']
                      /previous_contacts[name]['torso_surface_intersection_pairs']
                      for name in previous_contacts}
    torso_bbox = meshes['TORSO_CAGE']
    hoof_bbox = meshes['HOOF_FORE_L']
    tail_bbox = meshes['SKIN_TAIL_CORE']
    hoof_width = hoof_bbox['max'][1]-hoof_bbox['min'][1]
    hoof_height = hoof_bbox['max'][2]-hoof_bbox['min'][2]
    hoof_depth = hoof_bbox['max'][0]-hoof_bbox['min'][0]
    tail_spans = [tail_bbox['max'][i]-tail_bbox['min'][i] for i in range(3)]
    mouth_z = [.3542-.0065*math.sin(math.pi*abs(-.0455+.091*j/48)/.0455)
               for j in range(49)]
    fit = dict(
        torso=dict(stations=TORSO_STATIONS,
                   maximum_evaluated_width_H=torso_bbox['max'][1]-torso_bbox['min'][1],
                   central_control_vertical_thickness_H={'x_0_575':.414-.089,'x_0_730':.410-.092},
                   central_control_maximum_width_H=2*.305,
                   evaluated_bbox=torso_bbox,
                   intersection_ratios_vs_revision_12=contact_ratios),
        lower_face=dict(half_width_Y_H={str(z):HEAD_SECTIONS[i][3]
                         for i,z in enumerate([.235,.248,.272,.315])}),
        mouth=dict(width_H=.091,base_Z_H=.3542,curve_depth_H=.0065,
                   minimum_Z_H=min(mouth_z),mean_curve_Z_H=sum(mouth_z)/len(mouth_z)),
        hoof=dict(toe_lobe_count=3,cleft_count=2,evaluated_width_H=hoof_width,
                  evaluated_height_H=hoof_height,evaluated_depth_X_H=hoof_depth,
                  evaluated_min_Z_H=hoof_bbox['min'][2],
                  front_extent_H=.390-hoof_bbox['min'][0],
                  rear_extent_H=hoof_bbox['max'][0]-.390,
                  cleft_centers_local_Y_H=[-.0365,.0365],max_cleft_depth_H=.011,
                  sole_continuous=True,support_centers_unchanged=True),
        tail=dict(pivot=TAIL['pivot'],center_X_H=TAIL['center'],
                  nominal_length_H=TAIL['length'],nominal_diameter_H=TAIL['diameter'],
                  evaluated_bbox=tail_bbox,evaluated_spans_XYZ_H=tail_spans,
                  X_Z_aspect=tail_spans[0]/tail_spans[2],
                  motion_contact_result=diagnostics['tail_pivot_probes']))
    result = dict(blender=bpy.app.version_string,revision=options.revision,
        stage='Skin identity reconstruction',human_geometry_gate='PENDING; not ready for submission',
        executor_disposition='BLOCKED_AT_V008_SKIN_IDENTITY_FIT',
        selected_geometry_revision=options.revision,
        task_geometry_attempts=[13,14],prior_selected_revision=12,
        baseline_commit='4c3e55b6f37f5491bf20a9bf95bbe6ea0b42ed3e',
        generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        reference_hashes=REFERENCE_HASHES,reference_registration=REGISTRATION,
        geometry_digest=neutral_digest,view_geometry_digests=view_digests,
        support_targets=SUPPORT,tail_controls=TAIL,human_fit=fit,
        eye_architecture=dict(representation='head-conformal curved aperture + packed UV pigment',
                              maximum_X_relief_H=.014,front_span_H=[.137,.149],
                              bilateral_centers_Y_H=[-.162,.162],center_Z_H=.418,
                              independent_globes=False,production_facial_rig=False),
        head_controls=HEAD_SECTIONS,
        ear_controls=dict(perimeter=EAR_PERIMETER,inner_lip=EAR_INNER_LIP,
                          root_saddle=EAR_ROOT_SADDLE),meshes=meshes,
        tail_core_rump_X_overlap_H=meshes['TORSO_CAGE']['max'][0]-meshes['SKIN_TAIL_CORE']['min'][0],
        tail_fleece_shell='NOT CONSTRUCTED; Skin gate prerequisite',
        debug_landmarks={obj.name:list(obj.location) for obj in scene.objects if obj.get('NON_PRODUCTION')},
        attachment_diagnostics=diagnostics,
        motion_clearance={
            'status':'NOT_RUN_STATIC_GATE_BLOCKED',
            'head_yaw_pitch':'NOT RUN on revision 14',
            'blink':'NOT RUN on revision 14',
            'support_shift':'NOT RUN on revision 14',
            'tail_visual':'NOT RUN on revision 14; virtual surface intersections only',
            'ear_gaze_roll':'NOT RUN; frozen area and no selected valid static candidate',
            'cheek_lean_clearance':'NOT REACHED; neutral Skin gate blocked',
            'fleece_regional_clearance':'NOT REACHED; fleece not constructed'},
        saved_pose='NEUTRAL',
        fleece_representation='NOT CONSTRUCTED; Skin gate prerequisite',
        voxel_remesh_fleece=False,boolean_ear_recess=False,view_specific_geometry=False,
        normal_skin_identity='Normal not constructed; one neutral underbody only',
        production_rig=False,animation=False,final_retopology=False,
        limitations=['Side eye has broad washed-out reflection and less vertical dominance than the locked image.',
                     'Three hoof clefts exist in one mesh but remain weak in the rendered Front; tire read persists.',
                     'Head/chest still has separate exterior owners; no continuous articulation solution adopted.',
                     'Ear root remains narrow/abrupt; revision-9 distal bowl and root are unchanged.',
                     'Skin Front/Side registered skull/feature heights differ; no per-view correction used.',
                     'Technical diagnostics do not grant Human approval.'])
    (output/'measurements.json').write_text(json.dumps(result,indent=2)+'\n')
    print('V008_BUILD_COMPLETE '+str(output))


if __name__ == '__main__':
    main()
