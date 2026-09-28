"""Composite unretouched, identically framed Blender evidence onto white."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/production/carol/evidence/skin-ear-correction-v001'
FONT = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 24)


def board(filename, views, cell):
    w,h=cell
    canvas=Image.new('RGB',(w*len(views),2*(h+48)+48),'white')
    draw=ImageDraw.Draw(canvas)
    draw.text((18,12),'CAROL / Skin ear correction / same camera, light and scale / Human review pending',font=FONT,fill='#333333')
    for row,label in enumerate(['old','new']):
        for col,view in enumerate(views):
            im=Image.open(OUT/label/(view+'.png')).convert('RGBA')
            im.thumbnail((w,h),Image.Resampling.LANCZOS)
            x=col*w+(w-im.width)//2
            y=48+row*(h+48)
            draw.text((col*w+18,y+10),label.upper()+' / '+view,font=FONT,fill='#333333')
            canvas.paste(im,(x,y+48),im)
    canvas.save(OUT/filename)


board('old-vs-new.png',['front','side','front-3q'],(650,570))
board('ear-focused.png',['ear-side','ear-top'],(750,670))
