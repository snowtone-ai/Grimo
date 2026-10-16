"""Assemble review boards from unchanged captures; audit actual encoded videos."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,re,sys
R=Path(__file__).resolve().parents[2];BASE=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready';D=BASE/'final-v003'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
asset=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v003.glb';digest=sha(asset)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
def board(name,rows,columns):
 w=256;h=285;out=Image.new('RGB',(len(columns)*w,len(rows)*h+40),'#eee9ed');draw=ImageDraw.Draw(out);sources=[]
 for col,(title,folder) in enumerate(columns):draw.text((col*w+8,10),title,font=font,fill='#242024')
 for row,(title,file) in enumerate(rows):
  for col,(_,folder) in enumerate(columns):
   p=folder/file
   if not p.exists():raise FileNotFoundError(p)
   im=Image.open(p).convert('RGB');im.thumbnail((w,w));out.paste(im,(col*w+(w-im.width)//2,40+row*h));draw.text((col*w+5,40+row*h+w+4),title,font=font,fill='#242024');sources.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p)})
 p=D/name;out.save(p);return {'file':name,'sha256':sha(p),'sources':sources,'scope':'Unchanged source renders; thumbnails only. Engine lighting differs. Open originals for 640px inspection.'}
columns=[('v002 phone',BASE/'final-v002/phone'),('v003 Blender',D/'author'),('v003 GLB reimport',D/'saved'),('v003 PlayCanvas PC',D/'desktop'),('v003 Xiaomi',D/'phone')]
boards=[board('compare-face.png',[(n,n+'.png') for n in ['closed-front','closed-3q','large-front','large-3q']],columns)]
armrows=[('SelfContact middle / f514','f514-3q.png'),('Hold -> Self / f538','f538-side.png'),('Both Hold / f533','hold-side.png'),('Seat + interrupt / f549','seat-hold-3q.png')]
# Author/reimport renders use the named key states; detailed f514/f538 witnesses
# are runtime-only. Keep these before/after rows in the same engine/camera.
boards.append(board('compare-arms.png',armrows,[columns[0],columns[-1]]))
boards.append(board('compare-selfcontact-iteration.png',[(n,n+'.png') for n in ['self-front','self-3q','seat-hold-3q']],[('Rejected first v003',D/'rejected-selfcontact'),('Final v003 Xiaomi',D/'phone')]))
crop=Image.new('RGB',(640,190),'#eee9ed');dr=ImageDraw.Draw(crop);sources=[]
for col,(title,folder) in enumerate([columns[0],columns[-1]]):
 p=folder/'closed-3q.png';im=Image.open(p).crop((140,20,250,100));im=im.resize((220,160),Image.Resampling.NEAREST);crop.paste(im,(col*320,25));dr.text((col*320+5,2),title,font=font,fill='black');sources.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p),'crop_xyxy':[140,20,250,100],'nearest_scale':2})
crop.save(D/'compare-crown.png');boards.append({'file':'compare-crown.png','sources':sources,'scope':'Inspection crop enlarged 2x; original 640px files remain unchanged. Pixel region contains the former ear-root spike.'})
boards.append(board('compare-pipeline.png',[(n,n+'.png') for n in ['hold-side','seat-hold-3q','elbow-mid-3q','seat-face-hold-3qR']],columns[1:]))
body=Image.new('RGB',(512,6*285+40),'#eee9ed');dr=ImageDraw.Draw(body);dr.text((8,10),'Human-approved v004',font=font,fill='black');dr.text((264,10),'v003 Blender candidate',font=font,fill='black');body_sources=[]
for row,(pose,oldview,newview) in enumerate([(p,o,n) for p in ['neutral','seat'] for o,n in [('front','front'),('left','side'),('3q-L','3q')]]):
 for col,p in enumerate([BASE.parent/'production-rig-v004/renders/candidate'/(pose+'-'+oldview+'.png'),D/'author'/((pose if pose=='seat' else 'return')+'-'+newview+'.png')]):
  im=Image.open(p).convert('RGB');im.thumbnail((256,256));body.paste(im,(col*256+(256-im.width)//2,40+row*285));dr.text((col*256+5,40+row*285+260),pose+' / '+newview,font=font,fill='black');body_sources.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p)})
body.save(D/'compare-approved-body.png');boards.append({'file':'compare-approved-body.png','sources':body_sources,'scope':'Approved identity/body reference. Different render lighting/camera framing; no pixel identity claim. Mouth localized changes require Human review.'})
(D/'comparison-ledger.json').write_text(json.dumps({'artifact_sha256':digest,'boards':boards},indent=2))
if '--boards-only' in sys.argv:print('BOARDS',len(boards));raise SystemExit(0)
videos=[]
for p in [*sorted((D/'desktop').glob('*.webm')),*sorted((D/'phone').glob('*.webm')),*sorted(D.glob('author-*.mp4')),*sorted(D.glob('saved-*.mp4'))]:
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,nb_read_frames,duration:format=duration','-of','json',str(p)],text=True))
 hashes=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','framemd5','-'],text=True);rows=[x for x in hashes.splitlines() if x and not x.startswith('#')];unique=len({x.rsplit(',',1)[1].strip() for x in rows});assert unique>1,('Stale encoded video',p)
 videos.append({'file':p.relative_to(R).as_posix(),'sha256':sha(p),'decoded_frames':len(rows),'unique_decoded_frame_hashes':unique,'media':info})
(D/'encoded-video-audit.json').write_text(json.dumps({'artifact_sha256':digest,'videos':videos,'scope':'Actual decoded frame hashes prove update, not fixed-rate playback or GPU timing. See per-video timeline/render-counter ledgers.'},indent=2))
def perf(label):
 folder=D/label;env=json.loads((folder/'performance-environment.json').read_text());p=json.loads((folder/'performance.json').read_text());assert p['seconds']==300 and p['contextLoss']==0
 progress=json.loads((folder/'performance-progress.json').read_text());assert len(progress)==30 and all(x['visibility']=='visible' for x in progress)
 temperature=lambda name:int(re.search(r'temperature:\s*(\d+)',json.loads((folder/(name+'.json')).read_text())['battery']).group(1))/10
 return {'artifact':env['artifact'],'captureRun':env['captureRun'],**{k:p[k] for k in ['seconds','samples','rafP50','rafP95','rafP99','rafMax','jankGt25','normalCpuP50','normalCpuP95','normalCpuMax','contextLoss','gpuTime']},**{k:p[k] for k in ['controllerCpuP50','controllerCpuP95','controllerCpuMax','controllerSamples'] if k in p},'battery_celsius_start':temperature('device-start'),'battery_celsius_end':temperature('device-end'),'loadedMs':env['summary']['loadedMs'],'firstFrameMs':env['summary']['firstFrameMs']}
old,new=perf('phone-baseline-v002'),perf('phone');assert new['artifact']['sha256']==digest
(D/'performance-comparison.json').write_text(json.dumps({'v002':old,'v003':new,'scope':'Same phone/Chrome/USB/visible view/993-frame common loop/300s. Sequential single runs, recorded initial thermal state; not a causal thermal or GPU benchmark. v003 destroys the diagnostic model and runs only the production loader/controller/deformer. rAF is not GPU time.'},indent=2))
gpu=[]
for label in ['desktop','phone']:
 data=[json.loads((D/label/('gpu-'+str(f)+'.json')).read_text()) for f in [1,477,493,509,514,517,533,538,549,1041,1089,1095,1113,1149]];rows=[x for d in data for x in d['captures']];assert len(rows)==42 and all(x['glError']==0 for x in rows)
 gpu.append({'surface':label,'frames':len(data),'mesh_captures':len(rows),'max_raw_position_H':max(x['maxPosition'] for x in rows),'max_skin_only_position_H':max(x['skinOnlyPosition'] for x in rows),'max_normal_degrees':max(x['maxNormalDeg'] for x in rows),'gl_error':0})
(D/'gpu-comparison.json').write_text(json.dumps({'artifact_sha256':digest,'results':gpu,'scope':'Actual material shader transform feedback. Raw position includes GPU Morph precision; skin-only receives captured GPU Morph values. These are position/normal correspondence checks, not GPU timing.'},indent=2))
print('ASSEMBLED',len(boards),'boards',len(videos),'decoded videos',digest)
