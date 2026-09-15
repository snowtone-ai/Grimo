"""Compose unretouched render evidence; Pillow only, no generated art."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/blockout-v003'
OLD=OUT.parent/'blockout-v002'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)


def board(entries,path,title):
    rows=(len(entries)+2)//3
    canvas=Image.new('RGB',(1800,100+rows*530),'#edf0f5')
    draw=ImageDraw.Draw(canvas)
    draw.text((24,20),title,font=FONT,fill='#253147')
    draw.text((24,56),'Renders keep identical camera framing. Canonical is independently fit; pose and shading differ.',font=SMALL,fill='#4d5970')
    for i,(label,source,is_reference) in enumerate(entries):
        x=(i%3)*600;y=100+(i//3)*530
        draw.rectangle((x+10,y+10,x+590,y+520),fill='white')
        draw.text((x+26,y+24),label,font=FONT,fill='#253147')
        im=Image.open(source).convert('RGBA')
        if is_reference: im=im.crop(im.getchannel('A').getbbox())
        im.thumbnail((560,450),Image.Resampling.LANCZOS)
        canvas.paste(im,(x+(600-im.width)//2,y+62+(450-im.height)//2),im)
    canvas.save(path)


views=('front-perspective','front-orthographic','three-quarter','side','back','silhouette','clay')
entries=[('Canonical / posed reference',ROOT/'assets/grimo/source/carol/carol-Identity-canonical.png',True),
         ('v002 / front',OLD/'carol-v002-front-perspective.png',False),
         ('v003 / front',OUT/'carol-v003-front-perspective.png',False)]
entries += [('v003 / '+v,OUT/f'carol-v003-{v}.png',False) for v in views if v!='front-perspective']
board(entries,OUT/'review-board.png','CAROL v003 / Full 3D continuous fleece study / HUMAN GATE PENDING')
iterations=[(f'Iteration {i} / '+label,ROOT/f'artifacts/carol-v003/pass{i}/carol-v003-front-perspective.png',False)
            for i,label in ((1,'rejected: bare supports'),(2,'rejected: cushion'),(3,'deep saddle'),
                            (5,'over-smoothed'),(7,'rejected: crown flap'),(8,'final geometry'))]
if all(path.is_file() for _,path,_ in iterations):
    board(iterations,OUT/'iteration-board.png','CAROL v003 / actual rendered corrective iterations')
else:
    print('Local iteration renders absent; keeping the versioned historical board.')
board([('v002 / clay',OLD/'carol-v002-clay.png',False),('v003 / clay',OUT/'carol-v003-clay.png',False),
       ('v003 / rear',OUT/'carol-v003-back.png',False)],OUT/'clay-comparison.png',
      'CAROL / identical diagnostic lighting / topology and volume comparison')
metrics={}
for view in views:
    im=Image.open(OUT/f'carol-v003-{view}.png').convert('RGBA')
    bbox=im.getchannel('A').point(lambda a:255 if a>12 else 0).getbbox()
    assert bbox and bbox[0]>10 and bbox[1]>10 and bbox[2]<im.width-10 and bbox[3]<im.height-10
    metrics[view]={'canvas':list(im.size),'alphaBBox':bbox}
(OUT/'image-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8')
im=Image.open(OUT/'carol-v003-front-perspective.png').convert('RGBA').resize((320,272),Image.Resampling.LANCZOS)
mobile=Image.new('RGBA',im.size,'#edf0f5');mobile.alpha_composite(im)
mobile.convert('RGB').save(OUT/'front-at-320.png')
