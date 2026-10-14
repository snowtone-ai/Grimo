"""Reload saved GLBs into separate factory scenes; cameras never depend on candidate bounds."""
import bpy, sys, json, hashlib, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/tripo-rigprep-v006-lowpoly'
SOURCE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb'
CANDIDATE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigprep/shushu-v006-rigprep-lowpoly-v001.glb'
tag='candidate' if '--candidate' in sys.argv else 'source'
asset=CANDIDATE if tag=='candidate' else SOURCE
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(asset))
objects=[o for o in bpy.data.objects if o.type=='MESH']
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16
scene.cycles.use_denoising=False;scene.cycles.seed=0
scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Neutral soft review');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.8
scene.view_settings.view_transform='AgX';scene.view_settings.look='None';scene.view_settings.exposure=-.5
camera=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'))
scene.collection.objects.link(camera);scene.camera=camera;camera.data.type='ORTHO'
for name,loc,energy,size in [('key',(-1,-2,2),90,1.5),('fill',(1,-1,1),40,1.5)]:
 light=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));scene.collection.objects.link(light)
 light.location=Vector((0,0,.65))+Vector(loc);light.rotation_euler=(Vector((0,0,.65))-light.location).to_track_quat('-Z','Y').to_euler()
 light.data.energy=energy;light.data.shape='DISK';light.data.size=size
views={'front':(0,-1,0),'left-three-quarter':(-math.sqrt(.5),-math.sqrt(.5),0),'right-three-quarter':(math.sqrt(.5),-math.sqrt(.5),0),'left-side':(-1,0,0),'right-side':(1,0,0)}
records={};folder=OUT/'renders';folder.mkdir(parents=True,exist_ok=True)
def render(name,target,scale,direction,resolution):
 camera.data.ortho_scale=scale;d=Vector(direction);camera.location=Vector(target)+d*3
 camera.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
 scene.render.resolution_x=scene.render.resolution_y=resolution
 scene.render.filepath=str(folder/f'{tag}-{name}.png');bpy.ops.render.render(write_still=True)
 records[name]={'target':target,'scale':scale,'direction':direction,'resolution':resolution,'samples':16,'seed':0,'engine':'CYCLES','mode':'original materials / AgX -0.5' if not name.startswith('face-') else 'base color emission / Standard'}
for view,d in views.items():render('body-'+view,(0,0,.5),1.14,d,768)
render('eyes-front',(0,-.17,.67),.48,views['front'],1024)
for view in ['front','left-side','right-side']:render('mouth-'+view,(0,-.22,.58),.185,views[view],1024)
# Flat color isolates UV interpolation from lighting and normal changes.
for mat in bpy.data.materials:
 if not mat.use_nodes:continue
 tex=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE')
 output=next(n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL')
 emission=mat.node_tree.nodes.new('ShaderNodeEmission')
 mat.node_tree.links.new(tex.outputs['Color'],emission.inputs['Color']);mat.node_tree.links.new(emission.outputs[0],output.inputs['Surface'])
scene.view_settings.view_transform='Standard';scene.view_settings.exposure=0
for view,d in views.items():render('face-'+view,(0,0,.712),.72,d,1024)
(OUT/f'{tag}-render.json').write_text(json.dumps({'asset_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'blender':bpy.app.version_string,'cameras':records},indent=2)+'\n',encoding='utf-8')
print('RIGPREP_REVIEW_COMPLETE',tag,flush=True)
