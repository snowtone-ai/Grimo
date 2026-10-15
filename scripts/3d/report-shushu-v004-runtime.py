"""Label actual captures and measure image differences. No image retouching."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-runtime'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
def board(name,poses,view):
    im=Image.new('RGB',(4*400,len(poses)*435),(245,242,244));d=ImageDraw.Draw(im)
    for row,pose in enumerate(poses):
        for col,mode in enumerate(['approved','stock','four','full8']):
            if mode=='approved':
                mapped={'return':'standing-return','half-hold':'seat-hold-R'}.get(pose,pose)
                folder='candidate' if pose=='half-hold' else 'reimport'
                v={'3q':'3q-L','side':'left','front':'front'}[view]
                p=ROOT/f'docs/production/shushu/evidence/production-rig-v004/renders/{folder}/{mapped}-{v}.png'
            else:p=OUT/f'{mode}-{pose}-{view}.png'
            d.text((col*400+8,row*435+6),f'{mode} / {pose} / {view}',fill=(30,30,30),font=font)
            if p.exists():
                tile=Image.open(p).convert('RGB');tile.thumbnail((400,400));im.paste(tile,(col*400,row*435+30))
            else:d.text((col*400+8,row*435+100),'No matching source view',fill='black',font=font)
    im.save(OUT/name)
board('comparison-front.png',['neutral','seat','return'],'front')
board('comparison-side.png',['neutral','seat','half-hold'],'side')
board('comparison-3q.png',['legs-forward','seat','seat-rest','recover-load','return'],'3q')
rows=[]
for p in sorted(OUT.glob('stock-*.png')):
    for mode in ['four','full8']:
        q=OUT/p.name.replace('stock-',mode+'-');a=np.array(Image.open(p).convert('RGB')).astype(float);b=np.array(Image.open(q).convert('RGB')).astype(float)
        if a.shape!=b.shape:raise ValueError(f'Mismatched capture dimensions {p.name} {a.shape} {b.shape}')
        diff=np.abs(a-b);rows.append({'capture':p.name,'against':mode,'mae':float(diff.mean()),'maxChannel':float(diff.max()),'pixelsChangedGt3':int((diff.max(2)>3).sum()),'totalPixels':int(a.shape[0]*a.shape[1])})
(OUT/'image-differences.json').write_text(json.dumps(rows,indent=2)+'\n')
