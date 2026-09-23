"""One bounded v011-A3 Hero appearance and cheek-touch motion probe.

Run with Blender 5.2: blender --background carol-v011.blend --python this_file -- <repo-root>
The source blend is read only. This script writes the separate probe blend and six
Hero frames; ffmpeg composes the review video from rendered animation frames.
"""
import bpy
import math
import os
import sys
from mathutils import Vector

root = sys.argv[sys.argv.index('--') + 1]
out = os.path.join(root, 'docs', 'production', 'carol', 'evidence', 'hero-experience-probe-v001')
os.makedirs(out, exist_ok=True)
scene = bpy.context.scene

def mat(name, rgb, rough=0.75):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*rgb, 1)
    p.inputs['Roughness'].default_value = rough
    return m

cream = mat('PROXY fleece warm ivory', (0.94, 0.91, 0.96))
blue = mat('PROXY fleece periwinkle', (0.56, 0.68, 1.0))
lavender = mat('PROXY fleece soft lilac', (0.77, 0.73, 0.97))
gold = mat('PROXY motif warm gold', (1.0, 0.65, 0.16), .45)

def empty(name, pos):
    o = bpy.data.objects.new(name, None)
    scene.collection.objects.link(o)
    o.location = pos
    o.empty_display_size = .05
    return o

head = empty('PROBE head pivot / cheek seeking', (.40, 0, .36))
chest = empty('PROBE upper body participation', (.56, 0, .31))
touch = empty('PROBE contacted cheek local ACK', (-.035, -.29, .37))
follow = empty('PROBE delayed adjacent fleece', (.07, -.36, .47))
ear = empty('PROBE near ear', (.40, -.22, .56))

def sphere(name, pos, scale, material, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, location=pos)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(material)
    for p in o.data.polygons: p.use_smooth = True
    if parent:
        o.parent = parent
        o.matrix_parent_inverse = parent.matrix_world.inverted()
    return o

# Large spatial masses, then a small number of scallops. The face and ear tips
# stay clear. Torso fleece is stationary; only a few front/cheek pieces follow.
sphere('PROXY deep torso cloud', (.66, 0, .43), (.41, .37, .29), blue)
sphere('PROXY upper torso cloud', (.48, 0, .58), (.36, .37, .24), lavender, chest)
sphere('PROXY crown volume', (.28, 0, .66), (.30, .34, .22), blue, head)
for i, (x,y,z,s,m) in enumerate([
    (.09,-.23,.72,.145,cream),(.08,0,.78,.16,cream),(.09,.23,.72,.145,cream),
    (.27,-.32,.75,.16,blue),(.27,.32,.75,.16,blue),(.52,-.32,.69,.17,lavender),(.52,.32,.69,.17,lavender),
    (.78,-.30,.59,.17,blue),(.78,.30,.59,.17,blue),(.94,-.22,.47,.15,cream),(.94,.22,.47,.15,cream),
    (.83,-.28,.30,.15,lavender),(.83,.28,.30,.15,lavender),(.61,-.34,.29,.16,cream),(.61,.34,.29,.16,cream),
    (.37,-.33,.31,.13,blue),(.37,.33,.31,.13,blue),
]):
    sphere('PROXY body puff %02d'%i,(x,y,z),(s,s*1.05,s*.83),m)
for i,(y,z,s) in enumerate([(-.29,.55,.115),(-.33,.40,.105),(-.27,.25,.11),(.29,.55,.115),(.33,.40,.105),(.27,.25,.11),(-.17,.21,.13),(0,.20,.14),(.17,.21,.13)]):
    parent = touch if i in (0,1,2) else (follow if i==6 else head)
    sphere('PROXY face framing fleece %02d'%i,(-.015,y,z),(s*.80,s,s*.90),cream,parent)
for i,(y,z) in enumerate([(-.25,.69),(-.12,.71),(0,.72),(.12,.71),(.25,.69)]):
    sphere('PROXY brow scallop %02d'%i,(-.035,y,z),(.105,.11,.075),cream,head)

# One shallow star motif is enough to make the provisional identity readable.
def star(name, pos, r, parent=None):
    verts=[]
    for k in range(10):
        a=math.pi/2+k*math.pi/5
        rr=r if k%2==0 else r*.47
        verts.append((pos[0],pos[1]+rr*math.cos(a),pos[2]+rr*math.sin(a)))
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts, [], [tuple(range(10))]); mesh.update()
    o=bpy.data.objects.new(name,mesh); scene.collection.objects.link(o)
    o.data.materials.append(gold)
    solid=o.modifiers.new('shallow motif depth','SOLIDIFY'); solid.thickness=.012
    bevel=o.modifiers.new('rounded motif edge','BEVEL'); bevel.width=.006; bevel.segments=2
    if parent:
        o.parent=parent; o.matrix_parent_inverse=parent.matrix_world.inverted()
star('PROXY crown star',(-.16,0,.805),.053,head)

# A smooth, local shape key moves only the front cranial portion of the single
# v011 chassis. The rear torso and all four hoof meshes retain world support.
chassis=bpy.data.objects['CENTRAL_CHASSIS']
base=chassis.shape_key_add(name='PROBE neutral',from_mix=False)
lean=chassis.shape_key_add(name='PROBE head cheek lean',from_mix=False)
for i,v in enumerate(chassis.data.vertices):
    co=v.co.copy()
    front=max(0,min(1,(.54-co.x)/.37))
    front=front*front*(3-2*front)
    # Contact at camera-right cheek (negative Y). Small local bend, no root slide.
    lean.data[i].co=co+Vector((-.018*front,-.055*front,.012*front))

# The face lives on separate source objects; group it with the head pivot.
for name in ['EYE_L','EYE_R','EYELID_L','EYELID_R','NOSE','PHILTRUM','MOUTH_closed']:
    o=bpy.data.objects[name]; o.parent=head
    o.matrix_parent_inverse=head.matrix_world.inverted()
# One ear receives a subtle delayed response. Other ear remains source geometry.
o=bpy.data.objects['EAR_R']; o.parent=ear
o.matrix_parent_inverse=ear.matrix_world.inverted()

def key(obj, channel, frames):
    for f,value in frames:
        setattr(obj,channel,value)
        obj.keyframe_insert(data_path=channel,frame=f)

scene.render.fps=24; scene.frame_start=1; scene.frame_end=120
key(touch,'scale',[(1,(1,1,1)),(3,(.85,.90,.93)),(8,(.91,.94,.95)),(18,(1,1,1)),(120,(1,1,1))])
key(head,'location',[(1,(.40,0,.36)),(5,(.40,0,.36)),(12,(.39,-.009,.36)),(27,(.375,-.036,.365)),(45,(.375,-.040,.363)),(68,(.393,-.015,.359)),(88,(.395,-.012,.359)),(120,(.40,0,.36))])
key(head,'rotation_euler',[(1,(0,0,0)),(9,(0,0,0)),(25,(.018,-.025,-.030)),(45,(.025,-.030,-.032)),(70,(.008,-.008,-.010)),(120,(0,0,0))])
key(chest,'location',[(1,(.56,0,.31)),(17,(.56,0,.31)),(39,(.56,-.013,.31)),(67,(.56,-.006,.31)),(120,(.56,0,.31))])
key(follow,'location',[(1,(.07,-.36,.47)),(12,(.07,-.36,.47)),(31,(.065,-.377,.475)),(50,(.07,-.371,.47)),(76,(.07,-.36,.47)),(120,(.07,-.36,.47))])
key(ear,'rotation_euler',[(1,(0,0,0)),(15,(0,0,0)),(30,(.04,0,-.025)),(51,(.02,0,-.01)),(75,(0,0,0)),(120,(0,0,0))])
for f,v in [(1,0),(7,0),(26,.78),(45,1),(70,.33),(90,.18),(120,0)]:
    lean.value=v; lean.keyframe_insert(data_path='value',frame=f)

# Fixed, front-weighted source camera, widened only to contain the fleece.
cam=bpy.data.objects['CAM front']; scene.camera=cam
cam.data.type='ORTHO'; cam.data.ortho_scale=1.35
scene.render.engine='CYCLES'; scene.cycles.samples=12
scene.render.resolution_x=720; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
scene.world.color=(.8,.8,.8)
scene.view_settings.view_transform='AgX'
scene.frame_set(1)
probe=os.path.join(root,'assets','grimo','production','carol','blender','carol-hero-experience-probe-v001.blend')
bpy.ops.wm.save_as_mainfile(filepath=probe)

frames=[(1,'neutral'),(3,'ack'),(25,'head'),(45,'peak'),(72,'settle'),(95,'afterglow')]
for f,label in frames:
    scene.frame_set(f); scene.render.filepath=os.path.join(out,'frame-%s.png'%label)
    bpy.ops.render.render(write_still=True)
os.replace(os.path.join(out,'frame-neutral.png'),os.path.join(out,'hero-neutral.png'))
for f in range(1,121,2):
    scene.frame_set(f); scene.render.resolution_percentage=75
    scene.render.filepath=os.path.join(out,'motion-%03d.png'%f)
    bpy.ops.render.render(write_still=True)
print('PROBE_COMPLETE',probe)
