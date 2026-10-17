"""640px native renders, fixed cameras, actual continuous evaluated frames."""
import bpy,sys,json,hashlib,importlib.util,subprocess
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging';sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
label='saved' if '--saved' in sys.argv else 'approved-v004' if '--approved' in sys.argv else 'source-v003' if '--source' in sys.argv else 'author'
source=B/('shushu-v004-motion-gate-v004.glb' if label=='saved' else 'shushu-v006-production-rig-v004-proof.blend' if label=='approved-v004' else 'shushu-v004-motion-gate-v003-proof.blend' if label=='source-v003' else 'shushu-v004-motion-gate-v004-proof.blend')
if label=='saved':g.GLB=source;g.imported()
else:bpy.ops.wm.open_mainfile(filepath=str(source))
scene,cam=g.r.b.setup_review(640,8);scene.render.engine='BLENDER_EEVEE';scene.render.fps=24;cam.data.type='ORTHO';folder=D/label;folder.mkdir(exist_ok=True);ledger=[]
def camera(view,mouth=False):
 cam.data.ortho_scale=.56 if mouth else 1.18;cam.location={'front':(0,-3,.615 if mouth else .5),'side':(-3,0,.615 if mouth else .5),'3q':(-2,-2.5,.65),'3qR':(2,-2.5,.65),'back':(0,3,.5),'top':(0,-.3,3)}[view];cam.rotation_euler=(Vector((0,-.02,.69) if mouth else (0,0,.5))-cam.location).to_track_quat('-Z','Y').to_euler()
def shot(path,f):
 scene.frame_set(f);scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);ledger.append({'file':path.relative_to(R).as_posix(),'frame':f,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
if '--video' in sys.argv:
 camera('3q');frames=R/'output/shushu-abc-v004'/label;frames.mkdir(exist_ok=True)
 for f in range(993,1150):shot(frames/f'{f:04}.png',f)
 subprocess.run(['ffmpeg','-y','-framerate','24','-start_number','993','-i',str(frames/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18',str(D/(label+'-composition-3q.mp4'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
else:
 rows=[1,103] if label=='approved-v004' else [1089,1101,1113] if label=='source-v003' else [1,103,1041,1053,1077,1089,1101,1113,1117,1125,1149]
 for f in rows:
  for view in ['front','side','3q','3qR']:camera(view);shot(folder/f'f{f}-{view}.png',f)
 if label in ['author','saved']:
  for f in [825,837,849,861,885,897,969,1113,1117]:camera('front',True);shot(folder/f'mouth-f{f}.png',f)
  for f in [1,103]:
   for view in ['back','top']:camera(view);shot(folder/f'f{f}-{view}.png',f)
(D/(label+('-video-ledger.json' if '--video' in sys.argv else '-render-ledger.json'))).write_text(json.dumps({'source':source.relative_to(R).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'resolution':[640,640],'fps':24,'images':ledger,'scope':'Actual evaluated saved frames, no synthetic interpolation; diagnostic excerpt only.'},indent=2));print('MATCHED_RENDER_COMPLETE',label,flush=True)
