"""Saved GLB raster orbit: test visible oral competition against oral-hidden control."""
import bpy,sys,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/tripo-gem-cleanup-v002'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v002'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(DEST/'pino-c-v005-tripo-gem-cleaned-v002.glb'))
oral=bpy.data.objects['PinoOralLiner_TRIPO_INPUT']
for mat in bpy.data.materials:
 if not mat.use_nodes:continue
 nodes=mat.node_tree.nodes;links=mat.node_tree.links;tex=next((n for n in nodes if n.type=='TEX_IMAGE'),None)
 if tex:
  em=nodes.new('ShaderNodeEmission');links.new(tex.outputs['Color'],em.inputs[0]);links.new(em.outputs[0],nodes.get('Material Output').inputs['Surface'])
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Neutral');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.7,.7,.7,1)
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=.29
folder=ROOT/'artifacts/pino-gem-cleanup-v002/orbit';folder.mkdir(parents=True,exist_ok=True);rows=[]
def pixels():
 # Read the actual saved raster: Blender's Render Result can be empty headless.
 im=bpy.data.images.load(s.render.filepath,check_existing=False);a=np.array(im.pixels[:]).reshape(512,512,4);bpy.data.images.remove(im);return a
for i,angle in enumerate(np.linspace(-35,35,15)):
 a=math.radians(angle);target=Vector((0,-.395,.600));cam.location=target+Vector((3*math.sin(a),-3*math.cos(a),.03*math.sin(a*2)));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 oral.hide_render=False;s.render.filepath=str(folder/f'{i:02d}-final.png');bpy.ops.render.render(write_still=True);visible=pixels()
 oral.hide_render=True;s.render.filepath=str(folder/f'{i:02d}-control.png');bpy.ops.render.render(write_still=True);control=pixels()
 diff=np.max(abs(visible-control),2);rows.append({'angle_degrees':float(angle),'pixels_different_from_hidden_control':int((diff>1/255).sum()),'max_channel_difference':float(diff.max())})
(OUT/'orbit-raster-audit.json').write_text(json.dumps({'engine':'BLENDER_EEVEE','resolution':512,'views':rows,'control':'oral-hidden diagnostic only; final GLB retains all meshes'},indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(rows,indent=2))
