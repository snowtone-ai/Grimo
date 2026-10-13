"""Arrange saved, unretouched nose renders and approved reference crops."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v003/nose-reference-revision'
SOURCE=ROOT/'assets/grimo/source/shushu/tripo-generation-pose'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def font(n):return ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
def sheet(columns,rows,title,subtitle):
 im=Image.new('RGB',(420*columns,110+452*rows),(245,244,241));draw=ImageDraw.Draw(im)
 draw.text((16,12),title,fill='#222222',font=font(25));draw.text((16,54),subtitle,fill='#555555',font=font(17))
 return im,draw
def cell(im,draw,path,row,col,label):
 x=420*col;y=110+452*row;draw.text((x+12,y+5),label,fill='#333333',font=font(19))
 pic=Image.open(path).convert('RGB');im.paste(pic.resize((420,420),Image.Resampling.LANCZOS),(x,y+32))
def comparison(name,state,kind,title):
 im,draw=sheet(3,2,title,'Same cameras / unretouched renders / HUMAN PENDING / TRIPO HOLD')
 for row,version in enumerate(['before','after']):
  for col,view in enumerate(['front','side','3q']):cell(im,draw,OUT/'renders'/f'{version}-{state}-{kind}-{view}.png',row,col,version+' / '+view)
 im.save(OUT/name)
def reference():
 crops={'front':(263,264,815,816),'side':(148,225,703,780)};records={};(OUT/'reference-crops').mkdir(exist_ok=True)
 im,draw=sheet(2,2,'Human nose target / saved v003 candidate','2D reference crops above; 3D diagnostic renders below')
 for col,view in enumerate(['front','side']):
  source=SOURCE/('shushu_bodyonly_front.png' if view=='front' else 'shushu_bodyonly_left.png');target=OUT/'reference-crops'/f'approved-{view}.png'
  Image.open(source).crop(crops[view]).save(target);records[view]={'source':source.relative_to(ROOT).as_posix(),'source_sha256':sha(source),'crop_bbox':crops[view],'crop_sha256':sha(target)}
  cell(im,draw,target,0,col,'approved reference / '+view);cell(im,draw,OUT/'renders'/f'after-smile-colour-{view}.png',1,col,'saved v003 / '+view)
 im.save(OUT/'00-reference-match.png');return records
def mouth():
 im,draw=sheet(2,2,'Small / large opening: nose follows expression','Same cameras / diagnostic colour / HUMAN PENDING')
 for row,state in enumerate(['small','full']):
  for col,version in enumerate(['before','after']):cell(im,draw,OUT/'renders'/f'{version}-{state}-colour-3q.png',row,col,version+' / '+state)
 im.save(OUT/'03-open-regression.png')
def main():
 comparison('01-clay-before-after.png','neutral','clay','Nose geometry: saved before / after')
 comparison('02-colour-before-after.png','smile','colour','Rounded nose / short philtrum: open smile')
 crops=reference();mouth();cameras=json.loads((OUT/'cameras.json').read_text());images={};pairs={}
 for name,camera in cameras.items():
  path=OUT/'renders'/(name+'.png')
  with Image.open(path) as im:im.load();size=list(im.size)
  assert size==[640,640];images[name]={'sha256':sha(path),'size':size}
  if name.startswith('after-'):
   old='before-'+name[6:];assert camera==cameras[old];pairs[name]={'before':old,'cameras_identical':True}
 assert len(pairs)==8 and len(images)==16
 result={'Human':'PENDING','Tripo':'HOLD','saved_candidate_views':8,'before_views':8,'pairs':pairs,'images':images,'reference_crops':crops,
  'image_operations':'Reference crop; resize, arrangement and labels only. No retouch/warp of reference or 3D renders.',
  'projection_note':'2D approved illustrations do not supply a calibrated 3D camera. Before/after Blender pairs use identical recorded cameras; reference crops are visual authorities, not a pixel-exact projection proof.'}
 (OUT/'review-manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('REFERENCE_NOSE_BOARDS_COMPLETE',len(pairs))
if __name__=='__main__':main()
