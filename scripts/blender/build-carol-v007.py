"""Zero-based Carol volume candidate. Blender 5.2, no previous Carol geometry.

blender -b --python scripts/blender/build-carol-v007.py -- --stage skin
Stages are deliberately separate: skin, skin-stress, normal, final.
Only advance after inspecting the preceding contact sheet. No production rig.
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
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--stage', choices=['skin', 'skin-stress', 'normal', 'final'], default='skin')
parser.add_argument('--resolution', type=int, default=640)
parser.add_argument('--diagnostics', default='neutral,yaw,yaw-R,pitch,lean-L,lean-R,ears,COM,forehoof,tail')
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
OUT = ROOT / 'tmp-carol-v007'
OUT.mkdir(exist_ok=True)
ASSET = ROOT / 'assets/grimo/production/carol/blender/carol-v007.blend'
EVIDENCE = ROOT / 'docs/production/carol/evidence/reconstruction-v007'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.render.resolution_x = scene.render.resolution_y = args.resolution
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = True
scene.view_settings.view_transform = 'AgX'
scene.world.color = (0.4, 0.4, 0.4)
scene.render.threads_mode = 'FIXED'
scene.render.threads = 12
scene['authority'] = 'FOUR FINAL LOCKED references + CAROL_GEOMETRY_PARAMETERS.md'
scene['production_state_source'] = 'docs/production/carol/CAROL_PRODUCTION_STATE.md'
scene['stage'] = args.stage
scene['coordinate_contract'] = 'X front to rear; Y bilateral; Z up; ground Z=0; H=1'

def mat(name, color, roughness=.65):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Roughness'].default_value = roughness
    return m

cream = mat('DEBUG warm skin', (.83, .67, .55))
brown = mat('DEBUG cocoa', (.19, .075, .039))
pink = mat('DEBUG ear inset', (.64, .23, .20))
dark = mat('DEBUG eye', (.022, .012, .018), .16)
iris = mat('DEBUG amber iris', (.32, .13, .033), .25)
white = mat('DEBUG eye glint', (.98, .98, 1), .18)
fleece_mat = mat('DEBUG fleece ivory', (.82, .82, .93))
blue = mat('DEBUG fleece lavender', (.29, .36, .74))
gold = mat('DEBUG motifs', (.94, .58, .12), .45)
body_parts, head_parts, ears, hooves, limbs, fleece_parts, anchors = [], [], {}, {}, {}, [], {}
lids={}

def mesh(name, verts, faces, material):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    if material:
        me.materials.append(material)
    for p in me.polygons:
        p.use_smooth = True
    return ob

def ellipsoid(name, loc, scale, material, segments=48, rings=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        ob.data.materials.append(material)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob

def union(name, objects, voxel=.008):
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = name
    mod = ob.modifiers.new('Editable volume union, not final topology', 'REMESH')
    mod.mode = 'VOXEL'
    mod.voxel_size = voxel
    bpy.ops.object.modifier_apply(modifier=mod.name)
    smooth = ob.modifiers.new('Soft mass transitions', 'SMOOTH')
    smooth.factor = 1.0
    smooth.iterations = 12
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob

def tube(name, points, radius, material):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = 3
    sp = cu.splines.new('POLY')
    sp.points.add(len(points)-1)
    for p, co in zip(sp.points, points):
        p.co = (*co, 1)
    ob = bpy.data.objects.new(name, cu)
    scene.collection.objects.link(ob)
    cu.materials.append(material)
    return ob

def loft(name, sections, material, n=64):
    # Sections: Z, center X, X radius, Y radius. Squared cheeks, rounded skull.
    verts, faces = [], []
    for z, cx, rx, ry in sections:
        for j in range(n):
            t = 2*math.pi*j/n
            c, s = math.cos(t), math.sin(t)
            exponent = 2.7 if c < 0 else .85
            verts.append((cx + rx*math.copysign(abs(c)**exponent, c),
                          ry*math.copysign(abs(s)**.90, s), z))
    for i in range(len(sections)-1):
        for j in range(n):
            a, b = i*n+j, i*n+(j+1)%n
            faces.append((a,b,b+n,a+n))
    faces += [tuple(reversed(range(n))), tuple((len(sections)-1)*n+j for j in range(n))]
    ob = mesh(name, verts, faces, material)
    sub = ob.modifiers.new('Editable cranial sections', 'SUBSURF')
    sub.levels = 2
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.modifier_apply(modifier=sub.name)
    return ob

# One chassis. The head section layout is derived afresh from the four locked images.
torso = loft('CHASSIS chest abdomen pelvis', [
    (.205,.295,.008,.008),(.255,.295,.11,.16),(.355,.295,.163,.265),
    (.48,.29,.155,.29),(.65,.285,.14,.285),(.82,.295,.155,.305),
    (.95,.295,.135,.265),(1.035,.295,.070,.14),(1.06,.295,.006,.008)],cream)
# Reorient the section construction: longitudinal X, section height Z.
for v in torso.data.vertices:
    v.co=Vector((v.co.z,v.co.y,v.co.x))
torso.data.update()
width=max(v.co.y for v in torso.data.vertices)-min(v.co.y for v in torso.data.vertices)
for v in torso.data.vertices:
    v.co.y *= .610/width
bm=bmesh.new(); bm.from_mesh(torso.data)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bm.to_mesh(torso.data); bm.free()
body_parts.append(torso)
head = loft('HEAD cheek muzzle cranium', [
    (.215,.29,.035,.045), (.230,.275,.12,.13),
    (.265,.255,.225,.255), (.315,.26,.255,.296),
    (.385,.275,.26,.298), (.465,.29,.26,.279),
    (.555,.32,.24,.258), (.625,.33,.19,.215),
    (.675,.33,.105,.132), (.690,.33,.008,.008)], cream)
head_parts.append(head)
transition = ellipsoid('SHORT head chest transition', (.39,0,.34), (.11,.17,.11), cream)
body_parts.append(transition)

for side, sign in [('L',1),('R',-1)]:
    for row, x, y in [('fore',.390,.175),('hind',.920,.245)]:
        name = row+'_'+side
        limb = ellipsoid('LIMB '+name, (x+.012,sign*y,.175), (.088,.083,.137), cream)
        limbs[name] = limb
        # Flat-bottom broad hoof with shallow two-toe cleft, one connected volume.
        vs, fs = [], []
        for k in range(17):
            z = .111*k/16
            r = max(.002, (1-((z-.033)/.0785)**2))**.5
            for j in range(64):
                t = 2*math.pi*j/64
                yy = .1095*math.sin(t)*r
                xx = .107*math.cos(t)*r
                if xx < 0:
                    xx += .016*math.exp(-(yy/.017)**2)*(1-k/20)
                vs.append((x+xx, sign*y+yy, z))
        for k in range(16):
            for j in range(64):
                a=k*64+j; b=k*64+(j+1)%64
                fs.append((a,b,b+64,a+64))
        fs += [tuple(reversed(range(64))),tuple(16*64+j for j in range(64))]
        hooves[name] = mesh('HOOF '+name,vs,fs,brown)
    # One tapered, closed volume per ear, rooted inside head. No paper plane.
    vs, fs = [], []
    for i in range(33):
        u=i/32
        center=Vector((.355+.28*u,sign*(.225+.355*u),.552-.11535*u-.055*math.sin(math.pi*u)))
        width=.016+.132*math.sin(math.pi*u)**.65
        thickness=.014*(.75+.25*math.sin(math.pi*u))
        for j in range(32):
            t=2*math.pi*j/32
            vs.append(tuple(center+Vector((-.50,sign*.12,.86))*width*math.cos(t)
                            +Vector((-.82,sign*.08,-.57))*thickness*math.sin(t)))
    for i in range(32):
        for j in range(32):
            a=i*32+j; b=i*32+(j+1)%32
            fs.append((a,b,b+32,a+32))
    fs += [tuple(reversed(range(32))), tuple(32*32+j for j in range(32))]
    ear=mesh('EAR '+side,vs,fs,brown)
    ear.data.materials.append(pink)
    for p in ear.data.polygons:
        if p.index < 1024:
            i,j=divmod(p.index,32)
            if 6<i<29 and 7<j<15:
                p.material_index=1
    ears[side]=ear
    head_parts.append(ear)

# Broad diagonal eye surface permits a real profile; no duplicate side eyes.
for side, sign in [('L',1),('R',-1)]:
    eye=ellipsoid('EYE '+side, (.104,sign*.162,.398),(.038,.089,.0745),dark)
    eye.rotation_euler.z=sign*math.radians(-45)
    head_parts.append(eye)
    rim=[]
    for j in range(65):
        t=2*math.pi*j/64
        rim.append((.104+.063*math.sin(t),sign*(.162+.063*math.sin(t)),.398+.0745*math.cos(t)))
    head_parts.append(tube('EYELID margin '+side,rim,.0055,brown))
    gl=ellipsoid('GLINT '+side,(.075,sign*.170,.432),(.010,.015,.016),white,32,16)
    gl.rotation_euler=eye.rotation_euler.copy()
    head_parts.append(gl)
    am=ellipsoid('IRIS lower '+side,(.080,sign*.186,.36),(.006,.029,.020),iris,32,16)
    am.rotation_euler=eye.rotation_euler.copy()
    head_parts.append(am)
    vs,fs=[],[]
    for i in range(13):
        theta=.005+.195*i/12
        for j in range(33):
            phi=-math.pi/2+math.pi*j/32
            vs.append((-.052*math.sin(theta)*math.cos(phi),
                       .101*math.sin(theta)*math.sin(phi),.080*math.cos(theta)))
    for i in range(12):
        for j in range(32):
            a=i*33+j; fs.append((a,a+1,a+34,a+33))
    lid=mesh('LID closure reserve '+side,vs,fs,cream)
    lid.location=eye.location.copy(); lid.rotation_euler=eye.rotation_euler.copy()
    lid['purpose']='Disposable closure envelope; requires later production eyelid topology'
    lids[side]=lid; head_parts.append(lid)
nose=ellipsoid('NOSE',(.011,0,.378),(.017,.0195,.0105),brown)
head_parts.append(nose)
mouth=[]
for j in range(49):
    y=-.0455+.091*j/48
    z=.35-.010*math.sin(math.pi*abs(y)/.0455)
    mouth.append((.009+.009*(y/.0455)**2,y,z))
head_parts.append(tube('MOUTH closed neutral',mouth,.0028,brown))
head_parts.append(tube('PHILTRUM',[(.007,0,.370),(.008,0,.350)],.0025,brown))
tail=union('TAIL independent hidden root and tuft',[
    ellipsoid('root', (1.105,0,.357),(.135,.030,.030),cream),
    ellipsoid('tuft',(1.247,0,.382),(.0425,.0475,.0475),cream)],.004)

def anchor(name, loc, owner):
    ob=bpy.data.objects.new('ANCHOR '+name,None)
    scene.collection.objects.link(ob)
    bpy.context.view_layer.update()
    local=owner.matrix_world.inverted()@Vector(loc)
    if owner.type=='MESH':
        hit,point,normal,_=owner.closest_point_on_mesh(local)
        if hit:
            local=point+normal*.006
        vertex=min(owner.data.vertices,key=lambda v:(v.co-local).length_squared)
        ob['bind_vertex']=vertex.index
        ob['bind_offset']=list(local-vertex.co)
    ob.parent=owner
    ob.location=local
    ob.empty_display_size=.02
    ob['owner']=owner.name
    anchors[name]=ob
    return ob

def update_anchors():
    for ob in anchors.values():
        if 'bind_vertex' in ob:
            ob.location=ob.parent.data.vertices[ob['bind_vertex']].co+Vector(ob['bind_offset'])
    bpy.context.view_layer.update()

for sign, side in [(1,'L'),(-1,'R')]:
    anchor('cheek_'+side,(.025,sign*.233,.325),head)
    anchor('ear_root_'+side,(.355,sign*.235,.55),ears[side])
anchor('forehead',(.061,0,.55),head)
anchor('head_top',(.33,0,.688),head)
anchor('mouth_food',(-.025,0,.35),head)
anchor('prop_contact',(-.03,.23,.33),head)
anchor('low_forehoof',(.285,.175,.055),hooves['fore_L'])

# Registered image empties are retained for inspection, hidden by default.
reference_collection=bpy.data.collections.new('REFERENCES locked, H-registered')
scene.collection.children.link(reference_collection)
for name,h,ground,origin,view in [
    ('carol_front.png',1011,1162,626.5,'front'),
    ('carol_side.png',916,998,144,'side'),
    ('carol_skin_front.png',994,1075,626.5,'front'),
    ('carol_skin_side.png',1019,1037,64,'side')]:
    path=ROOT/'assets/grimo/source/carol/approved-3d'/name
    im=bpy.data.images.load(str(path),check_existing=True)
    width,height=im.size[:]
    ob=bpy.data.objects.new('REFERENCE '+name,None)
    reference_collection.objects.link(ob)
    ob.empty_display_type='IMAGE'; ob.data=im
    ob.empty_display_size=width/h; ob.color[3]=.35
    horizontal=(width/2-origin)/h
    vertical=(ground-height/2)/h
    if view=='front':
        ob.matrix_world=Matrix(((0,0,-1,1.4),(-1,0,0,-horizontal),(0,1,0,vertical),(0,0,0,1)))
    else:
        ob.matrix_world=Matrix(((1,0,0,horizontal),(0,0,-1,1),(0,1,0,vertical),(0,0,0,1)))
    ob.hide_render=True
    ob['pixels_per_H']=h; ob['ground_pixel']=ground; ob['horizontal_origin_pixel']=origin
    im.filepath='//'+os.path.relpath(path,ASSET.parent).replace('\\','/')
reference_collection.hide_viewport=True

def camera(name, loc, target, scale=1.52):
    data=bpy.data.cameras.new(name)
    ob=bpy.data.objects.new(name,data)
    scene.collection.objects.link(ob)
    ob.location=loc
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    data.type='ORTHO'; data.ortho_scale=scale; data.lens=50
    return ob

cams={
    'front':camera('CAM front',(-4,0,.5),(.5,0,.5)),
    'side':camera('CAM side',(.65,-4,.5),(.65,0,.5)),
    '3q-left':camera('CAM 3Q left',(-3,-3,1.55),(.58,0,.48),1.65),
    '3q-right':camera('CAM 3Q right',(-3,3,1.55),(.58,0,.48),1.65),
    'back':camera('CAM back',(4,0,.5),(.5,0,.5)),
    'top':camera('CAM top',(.65,0,4),(.65,0,0),1.52),
}
for name, loc, power, size in [('key',(-3,-4,5),450,4),('fill',(-2,3,2),250,3),('rim',(3,0,4),350,3),('low fill',(-3,0,.2),90,3)]:
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK'; data.size=size
    ob=bpy.data.objects.new(name,data); scene.collection.objects.link(ob); ob.location=loc
    ob.rotation_euler=(Vector((.5,0,.4))-ob.location).to_track_quat('-Z','Y').to_euler()

def render(name, view='front', dest=OUT):
    scene.camera=cams[view]
    scene.render.filepath=str(dest/(name+'.png'))
    bpy.ops.render.render(write_still=True)

def save():
    ASSET.parent.mkdir(parents=True,exist_ok=True)
    scene.camera=cams['3q-left']
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))

if args.stage=='skin':
    render('skin-front'); render('skin-side','side')
    save()
    sys.exit(0)

bpy.context.view_layer.update()
base_coords={ob.name:[v.co.copy() for v in ob.data.vertices] for ob in scene.objects if ob.type=='MESH'}
base_matrices={ob.name:ob.matrix_world.copy() for ob in scene.objects}

def reset():
    for name, mat0 in base_matrices.items():
        bpy.data.objects[name].matrix_world=mat0.copy()
    for name, coords in base_coords.items():
        ob=bpy.data.objects[name]
        for v,co in zip(ob.data.vertices,coords):
            v.co=co
        ob.data.update()
    bpy.context.view_layer.update()

def rotate(objects, pivot, axis, degrees, offset=(0,0,0)):
    p=Vector(pivot)
    transform=Matrix.Translation(Vector(offset)+p) @ Matrix.Rotation(math.radians(degrees),4,axis) @ Matrix.Translation(-p)
    for ob in objects:
        ob.matrix_world=transform @ ob.matrix_world

def pose(name):
    reset()
    if name=='yaw': rotate(head_parts,(.39,0,.40),'Z',10)
    if name=='yaw-R': rotate(head_parts,(.39,0,.40),'Z',-10)
    if name=='pitch': rotate(head_parts,(.39,0,.40),'Y',7)
    if name in ['lean-L','lean-R']:
        sign=1 if name.endswith('L') else -1
        rotate(head_parts,(.39,0,.40),'X',sign*5,(0,sign*.020,-.004))
    if name=='ears':
        rotate([ears['L']],(.355,.225,.552),'X',12)
        rotate([ears['R']],(.355,-.225,.552),'X',5)
    if name in ['COM','forehoof']:
        # Analytic diagnostic warp: contact is exactly fixed at Z<=.111.
        for ob in body_parts+list(limbs.values()):
            inv=ob.matrix_world.inverted()
            for v in ob.data.vertices:
                world=ob.matrix_world@v.co
                w=max(0,min(1,(world.z-.111)/.17))
                world.x+=.018*w; world.y-=.012*w
                v.co=inv@world
        rotate(head_parts,(.39,0,.4),'Y',0,(.018,-.012,0))
    if name=='forehoof':
        hooves['fore_L'].location.z+=.022
        hooves['fore_L'].location.x-=.012
        ob=limbs['fore_L']
        for v in ob.data.vertices:
            w=max(0,min(1,(.26-(ob.matrix_world@v.co).z)/.16))
            v.co.z+=.022*w; v.co.x-=.012*w
    if name=='tail': rotate([tail],(.985,0,.355),'Y',-12)
    if name=='blink':
        for lid in lids.values():
            for i in range(13):
                theta=.005+(math.pi-.01)*i/12
                for j in range(33):
                    phi=-math.pi/2+math.pi*j/32
                    lid.data.vertices[i*33+j].co=Vector((-.052*math.sin(theta)*math.cos(phi),
                        .101*math.sin(theta)*math.sin(phi),.080*math.cos(theta)))
            lid.data.update()
    if name=='gaze':
        for ob in head_parts:
            if ob.name.startswith(('IRIS','GLINT')):
                ob.location.z+=.008
                ob.location.y+=.006
    update_anchors()
    bpy.context.view_layer.update()

if args.stage=='skin-stress':
    for name in args.diagnostics.split(','):
        pose(name); render('skin-test-'+name,'front' if name in ['blink','gaze'] else '3q-left')
    reset(); save(); sys.exit(0)

# Fleece is intentionally constructed only in later separately invoked stages.
# Continuous volume union with named regional fields; sparse sculptural lobes.
lobes=[]
def lobe(name,loc,scale,material=fleece_mat):
    ob=ellipsoid(name,loc,scale,material,40,24); lobes.append(ob); return ob

lobe('central back',(.72,0,.56),(.42,.39,.27),blue)
lobe('lower belly',(.67,0,.24),(.46,.43,.095))
lobe('rear rump',(1.03,0,.47),(.25,.43,.28),blue)
lobe('crown',(.575,0,.85),(.29,.35,.15))
for sign in [-1,1]:
    lobe('crown shoulder',(.61,sign*.225,.76),(.29,.235,.17),blue)
    lobe('upper side',(.78,sign*.32,.65),(.22,.18,.18),blue)
    lobe('lower side',(.88,sign*.38,.37),(.27,.17,.18),blue)
    lobe('rump side',(1.03,sign*.28,.43),(.23,.25,.23))
    for x,z,rx,rz in [(.52,.68,.18,.16),(.80,.77,.20,.16),(1.04,.66,.17,.17),
                       (1.12,.46,.17,.16),(.98,.29,.18,.13),(.72,.25,.18,.115),
                       (.50,.28,.15,.12)]:
        lateral=.25 if z>.7 else (.32 if z>.6 else (.34 if z<.35 else .405))
        lateral_radius=.15 if z>.7 else (.16 if z>.6 else (.14 if z<.35 else .173))
        lobe('side regional surface',(x,sign*lateral,z),(rx,lateral_radius,rz))
    # Face border leaves an actual empty aperture in front of the skull.
    for j,(y,z,r) in enumerate([(.35,.29,.081),(.36,.395,.073),(.35,.505,.085),(.29,.605,.105)]):
        lobe('face frame',(.23,sign*y,z),(.065,r,r))
    lobe('brow',(.28,sign*.105,.640),(.13,.15,.092))
    for j in range(4):
        y=sign*(.065+j*.11)
        lobe('chest scallop',(.31,y,.182+(.060 if j==3 else 0)),(.15,.093,.072))
    # A small number of secondary lobes bridge the primary masses.
    for x,y,z,rx,ry,rz in [(.43,.32,.77,.20,.14,.14),(.88,.32,.69,.22,.14,.19),
                           (1.12,.25,.60,.15,.20,.18),(.84,.34,.25,.19,.14,.095),
                           (.70,.43,.34,.19,.105,.13)]:
        lobe('regional transition',(x,sign*y,z),(rx,ry,rz))
for sign in [-1,1]:
    for y,z,r in [(.12,.80,.105),(.27,.70,.092),(.39,.59,.075),(.45,.26,.075)]:
        lobe('medium front relief',(.30,sign*y,z),(.105,r,r))
lobe('central brow',(.25,0,.644),(.12,.115,.097))
fleece=union('FLEECE_MASTER',lobes,.006)
# Volumetric ear recesses. A cut volume avoids stretched polygons in corridors.
for sign in [-1,1]:
    cutter=ellipsoid('temporary ear sweep',(.51,sign*.425,.44),(.20,.205,.107),None)
    modifier=fleece.modifiers.new('Ear clearance volume','BOOLEAN')
    modifier.operation='DIFFERENCE'; modifier.object=cutter
    bpy.context.view_layer.objects.active=fleece
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
# Drop only small boolean crumbs, never a meaningful disconnected mass.
bm=bmesh.new(); bm.from_mesh(fleece.data)
unseen=set(bm.verts); crumbs=[]
while unseen:
    stack=[unseen.pop()]; connected=[]
    while stack:
        v=stack.pop(); connected.append(v)
        for edge in v.link_edges:
            n=edge.other_vert(v)
            if n in unseen: unseen.remove(n); stack.append(n)
    if len(connected)<64: crumbs.extend(connected)
if crumbs: bmesh.ops.delete(bm,geom=crumbs,context='VERTS')
bm.to_mesh(fleece.data); bm.free()
# Uniform clay keeps region-color boundaries from masquerading as geometry seams.
clay=mat('DEBUG unified fleece clay',(.64,.67,.78))
fleece.data.materials.clear(); fleece.data.materials.append(clay)
for poly in fleece.data.polygons: poly.material_index=0
fleece_parts.append(fleece)
regions={'crown':(.575,0,.88),'face_frame':(.30,0,.57),'chest_front':(.31,0,.21),
         'central_back':(.72,0,.65),'lower_belly':(.67,0,.17),'rear_rump':(1.08,0,.45)}
for region, center in regions.items():
    group=fleece.vertex_groups.new(name=region)
    for v in fleece.data.vertices:
        d=(fleece.matrix_world@v.co-Vector(center)).length
        weight=math.exp(-(d/.28)**2)
        if weight>.001: group.add([v.index],weight,'REPLACE')
fleece['architecture']='One connected editable master; overlapping smooth regional fields; no production skinning'
anchor('fleece_front',(.075,0,.205),fleece)
anchor('front_fleece_opening',(.025,0,.49),fleece)

# Attached physical motifs; debug materials only. No floating atmosphere.
def fleece_surface(point, normal):
    n=Vector(normal).normalized()
    inv=fleece.matrix_world.inverted()
    origin=Vector(point)+n*2
    hit,loc,_,_=fleece.ray_cast(inv@origin,inv.to_3x3()@(-n))
    if not hit: raise RuntimeError('Motif surface ray missed: '+str(point))
    return fleece.matrix_world@loc+n*.012

def star(name, center, radius):
    center=fleece_surface(center,(-1,0,0))
    vs=[]
    for depth in [-.015,.015]:
        for j in range(10):
            t=2*math.pi*j/10
            r=radius if j%2==0 else radius*.5
            vs.append((center[0]+depth,center[1]+r*math.sin(t),center[2]+r*math.cos(t)))
    faces=[tuple(reversed(range(10))),tuple(range(10,20))]
    faces += [(j,(j+1)%10,(j+1)%10+10,j+10) for j in range(10)]
    ob=mesh(name,vs,faces,gold)
    bevel=ob.modifiers.new('Soft motif edge','BEVEL'); bevel.width=.009; bevel.segments=3
    fleece_parts.append(ob); anchor(name,center,fleece)
    ob['surface_anchor']=name

star('star_crown',(.305,0,.877),.061)
star('star_brow',(.006,-.045,.685),.059)
star('star_chest',(.054,0,.17),.046)
star('star_side',(.35,.48,.30),.047)
verts=[]
center=fleece_surface((.30,.34,.70),(-1,0,0))
tangent=Vector((0,-1,0))
radius=.120
outer=math.acos(.25)
for j in range(49):
    u=j/48
    a=outer+(2*math.pi-2*outer)*u
    b=(math.pi-outer)+2*outer*u
    verts.append(tuple(center+tangent*(radius*math.cos(a))+Vector((0,0,radius*math.sin(a)))))
    verts.append(tuple(center+tangent*(radius*.5+radius*math.cos(b))+Vector((0,0,radius*math.sin(b)))))
verts=[tuple(fleece_surface(p,(-1,0,0))) for p in verts]
moon=mesh('moon',verts,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(48)],gold)
solid=moon.modifiers.new('Physical motif thickness','SOLIDIFY'); solid.thickness=.018
bevel=moon.modifiers.new('Soft moon edge','BEVEL'); bevel.width=.006; bevel.segments=3
fleece_parts.append(moon); anchor('moon',center,fleece)
moon['surface_anchor']='moon'

bpy.context.view_layer.update()
base_coords.update({ob.name:[v.co.copy() for v in ob.data.vertices] for ob in fleece_parts})
base_matrices.update({ob.name:ob.matrix_world.copy() for ob in fleece_parts+list(anchors.values())})

def fleece_pose(name):
    pose(name)
    if name not in ['compress','peek']: return
    if name=='peek': rotate(head_parts,(.39,0,.40),'Y',6,(.045,0,-.022))
    inv=fleece.matrix_world.inverted()
    for v in fleece.data.vertices:
        p=fleece.matrix_world@v.co
        if name=='compress':
            w=math.exp(-((p-Vector((.15,.32,.37))).length/.13)**2)
            p.x+=.035*w; p.y+=.018*w
        else:
            w=math.exp(-((p.x-.14)/.22)**2-((p.z-.43)/.28)**2)
            p.y*=1+.075*w; p.x+=.027*w
        v.co=inv@p
    fleece.data.update()
    update_anchors()
    for ob in fleece_parts:
        if 'surface_anchor' in ob:
            marker=anchors[ob['surface_anchor']]
            old=base_matrices[marker.name].translation
            ob.location+=marker.matrix_world.translation-old
    bpy.context.view_layer.update()

if args.stage=='normal':
    render('normal-front'); render('normal-side','side'); save(); sys.exit(0)

EVIDENCE.mkdir(parents=True,exist_ok=True)
for mode in ['skin','normal']:
    for ob in fleece_parts: ob.hide_render=mode=='skin'
    render(mode+'-front','front',EVIDENCE)
    render(mode+'-side','side',EVIDENCE)
for view in ['3q-left','3q-right','back','top']:
    render('derived-'+view,view,EVIDENCE)
diagnostic_support={}
for name in ['neutral','yaw','lean-L','lean-R','ears','COM','forehoof','compress','peek','tail']:
    fleece_pose(name)
    diagnostic_support[name]={key:{'min_Z':min((ob.matrix_world@v.co).z for v in ob.data.vertices),
        'centroid_XY':[sum((ob.matrix_world@v.co)[i] for v in ob.data.vertices)/len(ob.data.vertices) for i in [0,1]]}
        for key,ob in hooves.items()}
    render('motion-'+name,'3q-left')
reset()
save()

def bbox(ob):
    coords=[ob.matrix_world@v.co for v in ob.data.vertices]
    return {'min':[min(p[i] for p in coords) for i in range(3)],
            'max':[max(p[i] for p in coords) for i in range(3)]}

authority=json.loads((ROOT/'assets/grimo/source/carol/approved-3d/authority.json').read_text())
data={'status':'AWAITING HUMAN REVIEW','blender':bpy.app.version_string,
      'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'reference_hashes':{r['path']:hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()
                          for r in authority['formalGeometryAuthority']['references']},
      'projection':'orthographic; front/side same 1.52 H camera span; no view-dependent geometry',
      'bounds':{ob.name:bbox(ob) for ob in [head,torso,tail,fleece]+list(hooves.values())},
      'support_centers':{'fore':.390,'hind':.920,'separation':.530},
      'diagnostic_support_observed':diagnostic_support,
      'surface_anchor_bindings':{name:{'owner':ob.parent.name,'vertex':ob.get('bind_vertex'),
           'neutral_world_position':list(ob.matrix_world.translation)} for name,ob in anchors.items()},
      'diagnostic_amplitudes':{'head_yaw_degrees':10,'pitch_degrees':7,'cheek_lean_H':.02,
          'COM_shift_H':[.018,-.012,0],'forehoof_lift_H':.022,'local_fleece_depth_H':.035,
          'face_nestle_H':.045,'tail_degrees':12},
      'limitations':['Disposable analytic poses, no production rig/skinning.',
                      'Visual diagnostic evidence is not a collision solver or identity approval.',
                      'Blink closure envelope and small gaze offset tested separately; expression quality and combined motion remain unproven.',
                      'Skin Side support-footprint registration implies ~0.728H skull height versus ~0.69H Skin Front; locked head height retained.',
                      'Moon remains on the front-left surface; opposite side reference motif visibility is not reproduced by duplicating the motif.']}
observed={ob.name:bbox(ob) for ob in [fleece,head,torso,tail]+list(hooves.values())+
          [ob for ob in head_parts if ob.type=='MESH' and ob.name.startswith('EYE ')]}
def extent(name,axis): return observed[name]['max'][axis]-observed[name]['min'][axis]
data['observed_locked_checks']={
    'height_H':{'target':1.0,'observed':observed[fleece.name]['max'][2]},
    'fleece_width_H':{'target':1.161,'observed':extent(fleece.name,1)},
    'eye_width_H':{'target':.137,'observed':extent('EYE L',1)},
    'eye_height_H':{'target':.149,'observed':extent('EYE L',2)},
    'forehoof_width_H':{'target':.219,'observed':extent('HOOF fore_L',1)},
    'forehoof_height_H':{'target':.111,'observed':extent('HOOF fore_L',2)},
    'chassis_width_H':{'target':.610,'observed':extent(torso.name,1)},
    'skin_head_height_max_H':{'target':.690,'observed':observed[head.name]['max'][2]},
}
for check in data['observed_locked_checks'].values():
    check['relative_error']=(check['observed']-check['target'])/check['target']
    check['within_2_percent']=abs(check['relative_error'])<=.02
adj=[[] for _ in fleece.data.vertices]
for edge in fleece.data.edges:
    a,b=edge.vertices; adj[a].append(b); adj[b].append(a)
remaining=set(range(len(adj))); components=[]
while remaining:
    stack=[remaining.pop()]; size=0
    while stack:
        v=stack.pop(); size+=1
        for n in adj[v]:
            if n in remaining: remaining.remove(n); stack.append(n)
    components.append(size)
data['fleece_connected_components']=sorted(components,reverse=True)
(EVIDENCE/'measurements.json').write_text(json.dumps(data,indent=2)+'\n')
