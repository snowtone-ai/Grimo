from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/rig-pretexture-technical-v003';R=E/'renders'
rows=[]
for src in sorted(R.glob('v002-*.png')):
    dst=R/src.name.replace('v002-','v003-',1);a=np.asarray(Image.open(src).convert('RGB')).astype(int);b=np.asarray(Image.open(dst).convert('RGB')).astype(int)
    rows.append({'source':src.name,'candidate':dst.name,'max_channel_delta':int(abs(a-b).max()),'different_pixels':int(np.any(a!=b,axis=2).sum())})
(E/'render-regression.json').write_text(json.dumps({'pixel_exact':all(r['max_channel_delta']==0 for r in rows),'max_channel_delta_observed':max(r['max_channel_delta'] for r in rows),'max_different_pixels_per_480x480':max(r['different_pixels'] for r in rows),'comparisons':rows,'boundary':'Material splitting changes a few raster edge samples. Report observed differences, do not claim pixel equality. Judge render boards alongside exact shape/weight/Morph preservation. Human pose approval remains pending.'},indent=2)+'\n')
def board(name,items,columns=3,width=400):
    height=width+30;im=Image.new('RGB',(columns*width,((len(items)+columns-1)//columns)*height),'#e9eee4');dr=ImageDraw.Draw(im)
    for i,(path,label) in enumerate(items):
        tile=Image.open(path).convert('RGB');tile.thumbnail((width,width));x=i%columns*width;y=i//columns*height;im.paste(tile,(x,y));dr.text((x+8,y+width+5),label,fill='#102521')
    im.save(E/name,quality=93)
face=[]
for state in ['neutral','close-mid','closed','open','blink-mid','blink']:
    for view in ['front','side','3q']:face.append((R/f'v003-{state}-{view}.png',f'v003 {state} {view}'))
board('face-review.jpg',face,width=320)
wing=[]
for state in ['fold','wing-open']:
    for source in ['v002','v003']:
        for view in ['front','side','back3q']:wing.append((R/f'{source}-{state}-{view}.png',f'{source} {state} {view}'))
board('wing-regression.jpg',wing,width=360)
board('diagnostic-review.jpg',[(p,p.stem.removeprefix('diagnostic-')) for p in sorted(R.glob('diagnostic-*.png'))],width=360)
print('PIXEL_EXACT',len(rows),all(r['max_channel_delta']==0 for r in rows))
