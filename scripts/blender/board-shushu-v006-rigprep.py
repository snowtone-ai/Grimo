"""Unretouched comparison boards and quantitative image differences."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/tripo-rigprep-v006-lowpoly'
metrics={}
def board(filename,names,size):
 canvas=Image.new('RGB',(size*3,(size+28)*len(names)),(245,245,245));d=ImageDraw.Draw(canvas)
 for row,name in enumerate(names):
  a=Image.open(OUT/'renders'/f'source-{name}.png').convert('RGB');b=Image.open(OUT/'renders'/f'candidate-{name}.png').convert('RGB')
  x=np.asarray(a).astype(float);y=np.asarray(b).astype(float);delta=abs(y-x)
  # Full frame metrics include background; foreground metrics exclude it.
  bg=x[0,0];mask=np.max(abs(x-bg),axis=2)>4
  ma=mask;mb=np.max(abs(y-bg),axis=2)>4
  metrics[name]={'resolution':list(a.size),'mean_absolute_rgb_255':float(delta.mean()),'foreground_mean_absolute_rgb_255':float(delta[mask].mean()),'rgb_rmse_255':float(np.sqrt(np.mean(delta**2))),'pixels_max_channel_gt3_percent':float(np.mean(delta.max(2)>3)*100),'silhouette_mask_xor_pixels':int(np.sum(ma!=mb)),'foreground_pixels':int(mask.sum())}
  if name=='face-front':
   for label,box in [('eye_right',(210,450,450,695)),('eye_left',(575,450,815,695)),('mouth',(410,630,615,845))]:
    l,t,r,bottom=box;v=delta[t:bottom,l:r];metrics[name][label]={'box':box,'mean_absolute_rgb_255':float(v.mean()),'max_rgb':float(v.max()),'changed_pixels':int(np.sum(v.max(2)>0))}
  diff=Image.fromarray(np.clip(delta*8,0,255).astype('uint8'))
  for col,(im,label) in enumerate([(a,'v006 Human PASS'),(b,'lowpoly v001'),(diff,'absolute difference x8')]):
   canvas.paste(im.resize((size,size)),(col*size,row*(size+28)+28));d.text((col*size+7,row*(size+28)+6),name+' / '+label,fill=(20,20,20))
 canvas.save(OUT/filename)
views=['front','left-three-quarter','right-three-quarter','left-side','right-side']
board('01-body-five-view-comparison.png',['body-'+v for v in views],384)
board('02-face-five-view-comparison.png',['face-'+v for v in views],480)
board('03-eyes-mouth-closeup-comparison.png',['eyes-front','mouth-front','mouth-left-side','mouth-right-side'],480)
overview=Image.new('RGB',(960,506),(245,245,245));d=ImageDraw.Draw(overview)
for i,tag in enumerate(['source','candidate']):
 overview.paste(Image.open(OUT/'renders'/f'{tag}-body-front.png').convert('RGB').resize((480,480)),(i*480,26))
 d.text((i*480+8,7),'v006 / 523,683 triangles' if i==0 else 'lowpoly v001 / 99,565 triangles',fill=(20,20,20))
overview.save(OUT/'00-front-overview.png')
source=json.loads((OUT/'source-render.json').read_text());candidate=json.loads((OUT/'candidate-render.json').read_text())
assert source['cameras']==candidate['cameras']
reduction=json.loads((OUT/'reduction.json').read_text())
assert source['asset_sha256']==reduction['source_sha256']
assert candidate['asset_sha256']==reduction['output_sha256']
(OUT/'image-differences.json').write_text(json.dumps({'same_cameras_lighting_resolution_samples_seed':True,'source_sha256':source['asset_sha256'],'candidate_sha256':candidate['asset_sha256'],'metrics':metrics,'limitations':'lit differences include path-traced sampling/indirect lighting; silhouette mask excludes background by RGB threshold, not geometric proof; image metrics do not grant Human approval'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(metrics,indent=2))
