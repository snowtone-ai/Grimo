"""Matching-camera author/saved evidence. Diagnostic excerpts, not Motion production."""
import bpy,sys,json,hashlib,importlib.util,subprocess
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging';sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);saved='--saved' in sys.argv;label='saved' if saved else 'author'
source=B/('shushu-v004-motion-gate-v003.glb' if saved else 'shushu-v004-motion-gate-v003-proof.blend');source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
if saved:g.GLB=source;g.imported()
else:bpy.ops.wm.open_mainfile(filepath=str(source))
video='--video' in sys.argv;scene,cam=g.r.b.setup_review(384 if video else 640,8);scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=8;cam.data.type='ORTHO'
folder=D/label;folder.mkdir(exist_ok=True);ledger=[]
def camera(view,mouth):
 cam.data.ortho_scale=.56 if mouth else 1.18
 cam.location={'front':(0,-3,.615 if mouth else .5),'side':(-3,0,.615 if mouth else .5),'3q':(-2,-2.5,.65),'3qR':(2,-2.5,.65)}[view]
 cam.rotation_euler=(Vector((0,-.02,.69) if mouth else (0,0,.5))-cam.location).to_track_quat('-Z','Y').to_euler()
def shot(path,f):
 scene.frame_set(f);scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);ledger.append({'file':str(path.relative_to(R)).replace('\\','/'),'frame':f,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
if video:
 for name,start,end,view,mouth in [('mouth',825,897,'front',True),('arm',477,557,'3q',False),('seat-return',1,169,'side',False),('composition',993,1149,'3qR',False)]:
  frames=R/'output/playwright/shushu-v003'/label/name;frames.mkdir(parents=True,exist_ok=True);camera(view,mouth)
  for f in range(start,end+1):shot(frames/f'{f:04}.png',f)
  subprocess.run(['ffmpeg','-y','-framerate','24','-start_number',str(start),'-i',str(frames/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','19',str(D/(label+'-'+name+'.mp4'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
else:
 rows=[('closed',825,True),('small',837,True),('medium',849,True),('large',861,True),('elbow-mid',1041,False),('offer',477,False),('offer-r',485,False),('self-mid',1065,False),('hold-mid',999,False),('wrist',493,False),('wrist-r',501,False),('self',509,False),('self-r',517,False),('hold',533,False),('seat-hold',549,False),('seat',103,False),('face-hold',1005,False),('interrupt',1029,False),('seat-face-hold',1101,False),('close-interrupt',1113,False),('return',1149,False)]
 for name,f,mouth in rows:
  for view in ['front','side','3q','3qR']:camera(view,mouth);shot(folder/(name+'-'+view+'.png'),f)
(D/(label+('-video' if video else '-render')+'-ledger.json')).write_text(json.dumps({'source':source.relative_to(R).as_posix(),'source_sha256':source_hash,'engine':scene.render.engine,'samples':8,'fps':24,'images':ledger,'scope':'actual contiguous evaluated frames; no generated interpolation'},indent=2));print('RENDER_COMPLETE',label,video,flush=True)
