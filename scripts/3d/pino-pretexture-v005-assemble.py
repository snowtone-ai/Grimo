"""Assemble only the reviewable v005 evidence; no retouch or production imagery."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageChops
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'artifacts/pino-pretexture-v005'
OUT=ROOT/'docs/production/pino/evidence/pretexture-reliability-v005'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/pretexture-reliability-v005'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
TITLE=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
def dump(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8', newline='\n')
def board(name,title,rows,cell=(400,440)):
 w,h=cell;columns=max(len(r) for r in rows);canvas=Image.new('RGB',(w*columns,60+h*len(rows)),(24,30,39));draw=ImageDraw.Draw(canvas);draw.text((15,15),title,font=TITLE,fill='white')
 for y,row in enumerate(rows):
  for x,(label,path) in enumerate(row):
   draw.text((x*w+12,65+y*h),label,font=FONT,fill='white')
   im=Image.open(path).convert('RGB');im.thumbnail((w-12,h-40),Image.Resampling.LANCZOS);canvas.paste(im,(x*w+(w-im.width)//2,95+y*h))
 canvas.save(OUT/name,optimize=True)
def frame(name):return TMP/(name+'.png')
def main():
 source=ROOT/'assets/grimo/source/pino'
 board('01-identity-and-neutral.png','PINO v005 / reference above; temporary diagnostic colors below / Human PENDING',[
 [('Canonical',source/'pino-Identity-canonical.png'),('Approved body-only front',source/'tripo-generation-pose/pino_bodyonly_front.png'),('Approved body-only left',source/'tripo-generation-pose/pino_bodyonly_left.png')],
 [('Neutral / front',frame('color-neutral-front')),('Neutral / side',frame('color-neutral-side')),('Neutral / 3Q',frame('color-neutral-3q'))]],(500,470))
 labels=[('neutral-face','Neutral'),('blink-half','Half'),('closed','Squint + closed mouth'),('wink','Wink'),('mouth-closed','Mouth closed'),('mouth-small','Small mouth'),('mouth-open','Open mouth')]
 face_rows=[[(label+' / '+view,frame('color-'+state+'-'+view)) for state,label in labels] for view in ['front','side']]
 face_rows.append([(label,frame('checker-'+state+'-'+view)) for label,state,view in [('Checker Neutral front','neutral-face','front'),('Checker Neutral side','neutral-face','side'),('Checker half front','blink-half','front'),('Checker closed front','closed','front'),('Checker closed side','closed','side'),('Checker open front','mouth-open','front'),('Checker open side','mouth-open','side')]])
 board('02-face.png','Temporary BaseColor + checker / eye, cheek and mouth boundaries / Human PENDING',face_rows,(360,410))
 body=['contact-mid','contact','rest-mid','rest','tail-L','tail-R']
 board('03-body-checker.png','Temporary colors and 64px UV checker / bounded v004 poses / Human PENDING',[
 [(s+' / color 3Q',frame('color-'+s+'-3q')) for s in body],
 [(s+' / color side',frame('color-'+s+'-side')) for s in body],
 [(s+' / checker',frame('checker-'+s+'-3q')) for s in body[:-1]]],(380,420))
 board('04-return.png','Changed-UV synthetic donor returned as image only / actual Tripo UNVERIFIED',[
 [(s+' / diagnostic before',frame('color-'+s+'-3q')) for s in ['neutral','contact','rest','tail-L']],
 [(s+' / returned image',frame('returned-'+s+'-3q')) for s in ['neutral','contact','rest','tail-L']]],(440,470))
 # Same-camera, measured pose samples replayed in both directions, not continuous Motion.
 frames=[]
 for step in [0,1,2,1,0]:
  a=['neutral-face','blink-half','closed'][step];b=['neutral','contact-mid','contact'][step];c=['neutral','rest-mid','rest'][step]
  canvas=Image.new('RGB',(1200,450),(24,30,39));d=ImageDraw.Draw(canvas)
  for col,(label,name) in enumerate([('Face',a),('Contact',b),('Low rest',c)]):
   im=Image.open(frame('color-'+name+('-front' if col==0 else '-3q'))).convert('RGB').resize((400,400))
   canvas.paste(im,(col*400,45));d.text((col*400+10,10),label+' / diagnostic samples',font=FONT,fill='white')
  frames.append(canvas)
 frames[0].save(OUT/'diagnostic-cycles.gif',save_all=True,append_images=frames[1:],duration=[700,450,900,450,700],loop=0,optimize=False)
 pixels={}
 for view in ['front','side','3q']:
  a=np.asarray(Image.open(frame('protected-v004-'+view))).astype(int);b=np.asarray(Image.open(frame('protected-v005-'+view))).astype(int);delta=np.abs(a-b)
  pixels[view]=dict(changed_pixels=int((delta>0).any(2).sum()),max_channel=int(delta.max()))
 dump('neutral-pixels.json',pixels)
 assert all(v['changed_pixels']==0 for v in pixels.values())
 protected=[]
 old='assets/grimo/production/pino/candidate-c/texture-handoff-v004'
 paths=[f'{old}/{name}' for name in ['pino-c-texture-handoff-v004.blend','pino-c-v004-tripo-input.glb','pino-c-v004-rigged-review.glb','pino-c-v004-return-map.npz']]
 paths += [str(p.relative_to(ROOT)).replace('\\','/') for p in source.rglob('*.png')]
 for path in paths:
  blob=subprocess.check_output(['git','show','fe39c6d:'+path],cwd=ROOT);actual=(ROOT/path).read_bytes()
  if blob.startswith(b'version https://git-lfs.github.com/spec/v1'):
   expected=next(x.split(':',1)[1] for x in blob.decode().splitlines() if x.startswith('oid sha256:'))
  else:expected=hashlib.sha256(blob).hexdigest()
  sha=hashlib.sha256(actual).hexdigest();assert sha==expected
  protected.append(dict(path=path,sha256=sha,equals_v004_commit=True))
 dump('source-protection.json',dict(files=protected,tracked_existing_pino_asset_diff=subprocess.check_output(['git','diff','--name-only','--','assets/grimo/source/pino','assets/grimo/production/pino/candidate-c/texture-handoff-v004','assets/grimo/production/pino/candidate-c/texture-ready-v003','assets/grimo/production/pino/candidate-c/face-foundation-v002','assets/grimo/production/pino/candidate-c/rig-v001'],cwd=ROOT,text=True)))
 files=[]
 for folder in [DEST,OUT]:
  for p in sorted(folder.rglob('*')):
   if p.is_file() and p.name!='file-manifest.json':files.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 dump('file-manifest.json',dict(source_commit='fe39c6d8aab1e550ee31823ca29e85b9b2658632',authority_main='28c1505b7aadf63db25f1be97eba8b99cd332cee',Human_Pre_Texture_Gate='PENDING',files=files))
 print(json.dumps(dict(neutral=pixels,protected_files=len(protected),manifest_files=len(files))))
if __name__=='__main__':main()
