"""Normalized-height authority comparisons and same-asset diagnostic sheets."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v002'
REF=ROOT/'assets/grimo/source/carol/approved-3d'
FONT=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
SMALL=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
def cut(path):
    im=Image.open(path).convert('RGBA')
    if im.getchannel('A').getextrema()[0]<250:box=im.getchannel('A').point(lambda x:255 if x>128 else 0).getbbox()
    else:
        rgb=im.convert('RGB');mask=Image.new('L',im.size)
        mask.putdata([255 if min(p)<220 and max(p)-min(p)>22 else 0 for p in rgb.getdata()]);box=mask.getbbox()
    return im.crop(box)
def tile(path,mirror=False):
    im=cut(path)
    if mirror:im=ImageOps.mirror(im)
    factor=540/im.height;im=im.resize((round(im.width*factor),540),Image.Resampling.LANCZOS)
    assert im.width<=730, 'Comparison needs a wider tile; never silently change the height normalization'
    bg=Image.new('RGBA',(750,570),'white');bg.alpha_composite(im,((750-im.width)//2,560-im.height));return bg.convert('RGB')
def board(name,rows,footer):
    im=Image.new('RGB',(1500,len(rows)*625+55),'white');d=ImageDraw.Draw(im)
    for y,row in enumerate(rows):
        for x,(label,path,mirror) in enumerate(row):
            d.text((x*750+18,y*625+12),label,font=FONT,fill='#302d40');im.paste(tile(path,mirror),(x*750,y*625+45))
    d.text((18,im.height-38),footer,font=SMALL,fill='#494357');im.save(OUT/name,quality=95)
board('01-authority-comparison.jpg',[
    [('Approved Normal Front',REF/'carol_front.png',False),('v002 — saved candidate Front',OUT/'front.png',False)],
    [('Approved Normal Side',REF/'carol_side.png',False),('v002 — moon side, display mirrored',OUT/'side.png',True)]
], 'Equal 540px character height, aspect ratio retained, ground aligned. Side display mirrored. One saved asset for every view.')
board('02-spatial-review.jpg',[
    [('Same asset — 3Q',OUT/'3q.png',False),('Same asset — opposite side',OUT/'opposite_side.png',False)],
    [('Same asset — rear',OUT/'rear.png',False),('Same asset — top',OUT/'top.png',False)]
], 'Derived diagnostic views, not fitting authorities. Same neutral asset, lighting and materials.')
im=Image.new('RGB',(1300,1080),'white');d=ImageDraw.Draw(im)
for x,view in enumerate(['front','side']):
    src=cut(OUT/(view+'.png'))
    if view=='side':src=ImageOps.mirror(src)
    for y,(label,box) in enumerate([('Fleece / pigment',(.08,.04,.92,.64)),('Hoof / lower fleece',(.10,.72,.90,1))]):
        crop=src.crop(tuple(int(v*(src.width if i%2==0 else src.height)) for i,v in enumerate(box)))
        crop.thumbnail((620,455),Image.Resampling.LANCZOS)
        d.text((x*650+18,y*520+10),view.title()+' — '+label,font=FONT,fill='#302d40')
        im.paste(crop,(x*650+(650-crop.width)//2,y*520+50),crop.getchannel('A'))
d.text((18,1046),'Unretouched crops of the saved-asset native renders. No bloom, depth of field or compositing.',font=SMALL,fill='#494357')
im.save(OUT/'03-surface-review.jpg',quality=95)
im=Image.new('RGB',(1000,330),'#faf9fc');d=ImageDraw.Draw(im)
d.text((22,14),'160px character-height readability — static appearance only',font=FONT,fill='#302d40')
for i,(label,path,mirror) in enumerate([
    ('Approved Front',REF/'carol_front.png',False),
    ('v002 Front',OUT/'front.png',False),
    ('v002 Side',OUT/'side.png',True),
    ('v002 3Q',OUT/'3q.png',False)]):
    src=cut(path)
    if mirror:src=ImageOps.mirror(src)
    src=src.resize((round(src.width*160/src.height),160),Image.Resampling.LANCZOS)
    im.paste(src,(i*250+(250-src.width)//2,80),src.getchannel('A'))
    d.text((i*250+30,260),label,font=SMALL,fill='#302d40')
d.text((22,302),'No device, interaction, animation or runtime validation is implied.',font=SMALL,fill='#494357')
im.save(OUT/'04-small-scale-review.jpg',quality=95)
