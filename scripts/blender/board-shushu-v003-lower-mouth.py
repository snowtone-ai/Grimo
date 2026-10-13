"""Arrange actual saved renders; no image edits to geometry or reference."""
import sys
sys.dont_write_bytecode=True
import json,hashlib,importlib.util
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('boards',Path(__file__).with_name('board-shushu-v003-reference-nose.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
b.OUT=ROOT/'docs/production/shushu/evidence/geometry-v003/lower-mouth-revision';OUT=b.OUT
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 b.comparison('01-colour-before-after.png','smile','colour','Opened lower lip: before / saved after')
 im,draw=b.sheet(2,3,'Lower lip / chin: reference, before and saved after','Only lower opening depth changed / HUMAN PENDING / TRIPO HOLD')
 for col,view in enumerate(['front','side']):
  source=OUT.parent/'nose-reference-revision/reference-crops'/f'approved-{view}.png'
  b.cell(im,draw,source,0,col,'approved reference / '+view)
  for row,version in enumerate(['before','after'],1):b.cell(im,draw,OUT/'renders'/f'{version}-smile-colour-{view}.png',row,col,version+' / '+view)
 im.save(OUT/'00-reference-before-after.png')
 im,draw=b.sheet(2,3,'Side: clay, small opening, large opening','Identical before / after cameras; unretouched saved renders')
 for row,(state,kind) in enumerate([('smile','clay'),('small','colour'),('full','colour')]):
  for col,version in enumerate(['before','after']):b.cell(im,draw,OUT/'renders'/f'{version}-{state}-{kind}-side.png',row,col,version+' / '+state+' / '+kind)
 im.save(OUT/'02-clay-openings-side.png')
 cameras=json.loads((OUT/'cameras.json').read_text());records={};pairs={}
 for name,cam in cameras.items():
  path=OUT/'renders'/(name+'.png')
  with Image.open(path) as image:image.load();assert image.size==(640,640)
  records[name]={'size':[640,640],'sha256':sha(path)}
  if name.startswith('after-'):
   old='before-'+name[6:];assert cameras[old]==cam;pairs[name]={'before':old,'cameras_equal':True}
 assert len(pairs)==6
 (OUT/'review-manifest.json').write_text(json.dumps({'Human':'PENDING','Tripo':'HOLD','pairs':pairs,'renders':records,'operations':'Crop existing approved reference, resize and arrange only; no retouch or warp.','reference_note':'An illustrated reference has no calibrated physical scale or 3D camera. No exact millimetre/pixel match is asserted.'},indent=2)+'\n')
 print('LOWER_MOUTH_BOARDS_COMPLETE',flush=True)
if __name__=='__main__':main()
