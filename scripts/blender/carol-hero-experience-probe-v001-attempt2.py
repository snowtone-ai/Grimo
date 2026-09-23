"""Reuse v004's Full-3D fleece and motifs on unchanged v011-A3 for one Hero probe."""
import bpy
import math
import os
import sys
from mathutils import Vector, Matrix

root = sys.argv[sys.argv.index('--') + 1]
mode = sys.argv[sys.argv.index('--') + 2]
out = os.path.join(root, 'docs', 'production', 'carol', 'evidence', 'hero-experience-probe-v001')
donor = os.path.join(root, 'assets', 'grimo', 'production', 'carol', 'blender', 'carol-blockout-v004.blend')
scene = bpy.context.scene

# Registration measured against the two source blends: v004 front is -Y,
# lateral is X, ground is Z=.025; v011 front is -X, lateral is Y, ground Z=0.
# A single .30 uniform scale gives a .82-high fleece above the hoof clearance.
# v004's geometric fleece center (X about -.06) maps close to v011 Y=0.
S = .30
def register(v):
    return Vector((.48 + S*v.y, S*v.x, S*v.z - .0075))

names = ['Carol_Fleece_Continuous', 'Carol_Moon_Attached',
         'Carol_Star_CrownStar', 'Carol_Star_TopStar',
         'Carol_Star_WoolStar', 'Carol_Star_ChestStar']
with bpy.data.libraries.load(donor, link=False) as (src, dst):
    dst.objects = [name for name in names if name in src.objects]
assert len(dst.objects) == len(names), [o.name for o in dst.objects]
objects = {}
for obj in dst.objects:
    obj.parent = None
    obj.matrix_world = Matrix.Identity(4)
    obj.data = obj.data.copy()
    scene.collection.objects.link(obj)
    obj.name = 'DONOR ' + obj.name
    objects[obj.name] = obj
    for v in obj.data.vertices:
        v.co = register(v.co)
    obj.data.update()

fleece = objects['DONOR Carol_Fleece_Continuous']
assert len(fleece.data.vertices) == 164272

# One donor-only low-order facial clearance. The continuous fleece is retained;
# its front sheet recedes under the larger v011 face and oversized eyes.
# No v011 source vertex, donor source file, or donor topology changes.
for v in fleece.data.vertices:
    x,y,z = v.co
    face = math.exp(-((y/.345)**4 + ((z-.425)/.205)**4))
    front = max(0.0, min(1.0, (.31-x)/.31))
    v.co.x += .235*face*front
fleece.data.update()

# The original crescent was placed beside a right-shifted v004 face. Move its
# copied motif above the left side of v011's centered face; keep spatial depth.
moon = objects['DONOR Carol_Moon_Attached']
for v in moon.data.vertices:
    v.co.x -= .08
    v.co.y += .50
    v.co.z += .12
moon.data.update()

def material(name, color, rough=.78):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = rough
    return m

ivory = material('PROBE donor warm ivory', (.90,.89,.99))
gold = material('PROBE donor warm gold', (1.0,.72,.23), .45)
fleece.data.materials.clear(); fleece.data.materials.append(ivory)
for obj in objects.values():
    if obj != fleece:
        obj.data.materials.clear(); obj.data.materials.append(gold)

cam = bpy.data.objects['CAM front']; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = 1.25
scene.render.engine = 'CYCLES'; scene.cycles.samples = 12
scene.render.resolution_x = 720; scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
scene.world.color = (.8,.8,.8)
scene.world.use_nodes = True
background = scene.world.node_tree.nodes.get('Background')
background.inputs['Color'].default_value = (.72,.72,.76,1)
background.inputs['Strength'].default_value = .8
scene.view_settings.view_transform = 'AgX'
scene.frame_set(1)
if mode == 'precheck':
    scene.render.filepath = os.path.join(out, 'hero-neutral-precheck.png')
    bpy.ops.render.render(write_still=True)
    print('DONOR_PRECHECK_COMPLETE')
    sys.exit(0)

def empty(name, pos, parent=None):
    o = bpy.data.objects.new(name, None)
    scene.collection.objects.link(o)
    o.location = pos
    o.empty_display_size = .035
    if parent:
        bpy.context.view_layer.update()
        o.parent = parent
        o.matrix_parent_inverse = parent.matrix_world.inverted()
    return o

head = empty('PROBE head base owner', (.35,0,.44))
ear_secondary = empty('PROBE near ear secondary', (.42,-.27,.48), head)
bpy.context.view_layer.update()

def parent_keep(obj, owner):
    obj.parent = owner
    obj.matrix_parent_inverse = owner.matrix_world.inverted()

for name in ('EYE_L','EYE_R','EYELID_L','EYELID_R','NOSE','PHILTRUM',
             'MOUTH_closed','EAR_L'):
    parent_keep(bpy.data.objects[name], head)
parent_keep(bpy.data.objects['EAR_R'], ear_secondary)
for name in ('DONOR Carol_Moon_Attached', 'DONOR Carol_Star_CrownStar',
             'DONOR Carol_Star_TopStar', 'DONOR Carol_Star_WoolStar'):
    parent_keep(objects[name], head)

def smoothstep(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)))
    return t*t*(3-2*t)

# Donor-only animation keys retain the grounded body and displace the crown,
# adjacent cheek and upper cover in the same direction as the owned face.
fleece.shape_key_add(name='DONOR neutral', from_mix=False)
ack = fleece.shape_key_add(name='DONOR local cheek ACK', from_mix=False)
seek = fleece.shape_key_add(name='DONOR head-owned lean', from_mix=False)
body = fleece.shape_key_add(name='DONOR upper-body delay', from_mix=False)
for i,v in enumerate(fleece.data.vertices):
    x,y,z=v.co
    contact=math.exp(-(((y+.295)/.105)**2+((z-.405)/.115)**2)) * (1-smoothstep(.22,.45,x))
    head_weight=smoothstep(.36,.67,z) * (1-smoothstep(.38,.82,x))
    body_weight=smoothstep(.21,.52,z)*(1-smoothstep(.55,.95,z))
    ack.data[i].co=v.co+Vector((.022*contact,-.008*contact,-.004*contact))
    seek.data[i].co=v.co+Vector((-.013*head_weight,-.044*head_weight,.004*head_weight))
    body.data[i].co=v.co+Vector((0,-.013*body_weight,0))

chassis=bpy.data.objects['CENTRAL_CHASSIS']
chassis.shape_key_add(name='PROBE neutral',from_mix=False)
lean=chassis.shape_key_add(name='PROBE cranial lean',from_mix=False)
for i,v in enumerate(chassis.data.vertices):
    co=v.co.copy()
    weight=1-smoothstep(.20,.56,co.x)
    lean.data[i].co=co+Vector((-.012*weight,-.041*weight,.004*weight))

def key(obj, channel, values):
    for frame,value in values:
        setattr(obj,channel,value)
        obj.keyframe_insert(data_path=channel,frame=frame)
def key_value(shape, values):
    for frame,value in values:
        shape.value=value; shape.keyframe_insert(data_path='value',frame=frame)

scene.render.fps=24; scene.frame_start=1; scene.frame_end=120
key_value(ack,[(1,0),(3,1),(8,.55),(18,0),(120,0)])
key_value(seek,[(1,0),(8,0),(27,.78),(45,1),(72,.18),(95,.10),(120,0)])
key_value(body,[(1,0),(17,0),(42,1),(70,.35),(120,0)])
key_value(lean,[(1,0),(8,0),(27,.78),(45,1),(72,.18),(95,.10),(120,0)])
key(head,'location',[(1,(.35,0,.44)),(8,(.35,0,.44)),(27,(.339,-.029,.443)),
                     (45,(.337,-.039,.443)),(72,(.348,-.010,.44)),
                     (95,(.348,-.006,.44)),(120,(.35,0,.44))])
key(head,'rotation_euler',[(1,(0,0,0)),(9,(0,0,0)),(28,(.012,-.015,-.018)),
                           (45,(.018,-.020,-.020)),(72,(.004,-.005,-.005)),(120,(0,0,0))])
key(ear_secondary,'rotation_euler',[(1,(0,0,0)),(17,(0,0,0)),
                                    (34,(.032,0,-.018)),(56,(.015,0,-.008)),
                                    (80,(0,0,0)),(120,(0,0,0))])

scene.frame_set(1)
if mode == 'control_precheck':
    scene.render.filepath = os.path.join(out, 'hero-control-precheck.png')
    bpy.ops.render.render(write_still=True)
    print('CONTROL_PRECHECK_COMPLETE')
    sys.exit(0)
probe=os.path.join(root,'assets','grimo','production','carol','blender',
                   'carol-hero-experience-probe-v001.blend')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=probe)
for frame,label in [(1,'neutral'),(3,'ack'),(27,'head'),(45,'peak'),(72,'settle'),(95,'afterglow')]:
    scene.frame_set(frame)
    scene.render.resolution_percentage=100
    scene.render.filepath=os.path.join(out,'frame-'+label+'.png')
    bpy.ops.render.render(write_still=True)
os.replace(os.path.join(out,'frame-neutral.png'),os.path.join(out,'hero-neutral.png'))
for frame in range(1,121,2):
    scene.frame_set(frame)
    scene.render.resolution_percentage=75
    scene.render.filepath=os.path.join(out,'motion-%03d.png'%frame)
    bpy.ops.render.render(write_still=True)
print('ATTEMPT2_COMPLETE',probe)
