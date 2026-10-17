"""Orthographic distance perturbation: fixed pixels expose competing oral depth."""
import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/tripo-gem-cleanup-v002'
DEST=ROOT/'assets/grimo/production/pino/candidate-c';TMP=ROOT/'artifacts/pino-gem-cleanup-v002/depth';TMP.mkdir(parents=True,exist_ok=True)
rows=[]
for tag,path in [('before',DEST/'tripo-gem-cleanup-v001/pino-c-v005-tripo-donor-original.glb'),('after',DEST/'tripo-gem-cleanup-v002/pino-c-v005-tripo-gem-cleaned-v002.glb')]:
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
 for mat in bpy.data.materials:
  if not mat.use_nodes:continue
  nodes=mat.node_tree.nodes;links=mat.node_tree.links;tex=next((n for n in nodes if n.type=='TEX_IMAGE'),None)
  if tex:
   em=nodes.new('ShaderNodeEmission');links.new(tex.outputs['Color'],em.inputs[0]);links.new(em.outputs[0],nodes.get('Material Output').inputs['Surface'])
 s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100
 s.world=bpy.data.worlds.new('Neutral');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.7,.7,.7,1)
 s.view_settings.view_transform='Standard';s.view_settings.look='None'
 bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=.25;cam.data.clip_start=.01;cam.data.clip_end=100
 target=Vector((0,-.38,.603));frames=[]
 for i,d in enumerate([2.95,3.,3.05]):
  cam.location=target+Vector((0,-d,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(TMP/f'{tag}-{i}.png');bpy.ops.render.render(write_still=True)
  im=bpy.data.images.load(s.render.filepath,check_existing=False);frames.append(np.array(im.pixels[:]).reshape(512,512,4));bpy.data.images.remove(im)
 delta=np.max(np.stack(frames),0)-np.min(np.stack(frames),0);delta=delta[:,:,:3].max(2)
 rows.append({'tag':tag,'distances':[2.95,3.,3.05],'orthographic_projection_identical':True,'pixels_varying_over_5_of_255':int((delta>5/255).sum()),'pixels_varying_over_20_of_255':int((delta>20/255).sum()),'max_channel_variation':float(delta.max())})
(OUT/'depth-stability.json').write_text(json.dumps({'engine':'BLENDER_EEVEE','resolution':512,'tests':rows,'scope':'static donor mouth, fixed front orthographic view; no Rig/runtime claims'},indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(rows,indent=2))
