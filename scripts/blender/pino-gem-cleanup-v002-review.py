"""Identical saved-GLB cameras for donor diagnosis and local cleanup review."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/pino/evidence/tripo-gem-cleanup-v002'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v002'
tag=sys.argv[sys.argv.index('--tag')+1] if '--tag' in sys.argv else 'before'
asset=DEST/'pino-c-v005-tripo-gem-cleaned-v002.glb' if tag=='after' else ROOT/'artifacts/pino-gem-cleanup-v002/pino-c-v005-oral-texture-only-v002.glb'
if tag=='before':asset=DEST.parent/'tripo-gem-cleanup-v001/pino-c-v005-tripo-donor-original.glb'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(asset))
if tag=='without-oral':bpy.data.objects['PinoOralLiner_TRIPO_INPUT'].hide_render=True
for mat in ([] if '--lit' in sys.argv else bpy.data.materials):
 if not mat.use_nodes:continue
 nodes=mat.node_tree.nodes;links=mat.node_tree.links;tex=next((n for n in nodes if n.type=='TEX_IMAGE'),None)
 if tex:
  em=nodes.new('ShaderNodeEmission');links.new(tex.outputs['Color'],em.inputs[0]);links.new(em.outputs[0],nodes.get('Material Output').inputs['Surface'])
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.use_denoising=False;s.render.resolution_x=900;s.render.resolution_y=900;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Neutral');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.7,.7,.7,1)
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
if '--lit' in sys.argv:
 s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;s.cycles.samples=64;s.cycles.use_denoising=True
 for name,loc,power,size in [('Key',(-1,-2,2),25,2),('Fill',(1,-1,1),12,2)]:
  bpy.ops.object.light_add(type='AREA',location=loc);lamp=bpy.context.object;lamp.name=name;lamp.data.energy=power;lamp.data.shape='DISK';lamp.data.size=size;lamp.rotation_euler=(Vector((0,0,.6))-lamp.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO'
views=[('front',(0,-3,0),.71,(0,0,.67)),('face-close',(0,-3,0),.25,(0,-.38,.603)),('left-3q',(-1.5,-2.6,0),.71,(0,0,.67)),('right-3q',(1.5,-2.6,0),.71,(0,0,.67))]
if tag=='without-oral':views=views[1:2]
if tag=='texture-only':views=views[1:2]
suffix='-lit' if '--lit' in sys.argv else ''
if '--lit' in sys.argv:views=[views[1],views[2]]
for name,d,scale,t in views:
 target=Vector(t);cam.data.ortho_scale=scale;cam.location=target+Vector(d);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(OUT/f'{tag}-{name}{suffix}.png');bpy.ops.render.render(write_still=True)
