"""Independent, lit saved-GLB mouth review. No production blend is opened."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/tripo-mouth-depth-v006'
config=json.loads((OUT/'repair-config.json').read_text());candidate='--candidate' in sys.argv
path=ROOT/config['candidate' if candidate else 'base'];tag='candidate' if candidate else 'before'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False
scene.render.resolution_x=scene.render.resolution_y=768;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Soft review');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.8
scene.view_settings.view_transform='AgX';scene.view_settings.look='None';scene.view_settings.exposure=-.5
cams=json.loads((OUT/'before-cameras.json').read_text());reference=cams['front'];target=Vector(reference['target'])
camera=bpy.data.objects.new('MouthReviewCamera',bpy.data.cameras.new('MouthReviewCamera'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=reference['orthographic_scale']
for name,loc,energy,size in [('key',(-1,-2,2),90,1.5),('fill',(1,-1,1),40,1.5)]:
 light=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));scene.collection.objects.link(light);light.location=target+Vector(loc);light.rotation_euler=(target-light.location).to_track_quat('-Z','Y').to_euler();light.data.energy=energy;light.data.shape='DISK';light.data.size=size
folder=OUT/'shaded';folder.mkdir(exist_ok=True);records={}
for name in ['front','left-three-quarter','right-three-quarter','left-side','right-side']:
 d=Vector(cams[name]['direction']);camera.location=target+d*3;camera.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/f'{tag}-{name}.png');bpy.ops.render.render(write_still=True);records[name]={'direction':list(d),'target':list(target),'scale':camera.data.ortho_scale}
(OUT/f'{tag}-shaded-render.json').write_text(json.dumps({'asset_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'cameras':records,'resolution':768,'samples':24,'engine':'CYCLES','color':'AgX / exposure -0.5 (avoid clipping cream highlights)','lighting':'same soft area key/fill; original GLB materials'},indent=2)+'\n')
print('SHADED_MOUTH_REVIEW_COMPLETE',tag,flush=True)
