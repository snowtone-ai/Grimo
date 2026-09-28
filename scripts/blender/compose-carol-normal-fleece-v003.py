"""Unretouched equal-height comparisons, overlays and semantic crops."""
from pathlib import Path
import importlib.util,sys,json
sys.dont_write_bytecode=True
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v003'
REF=ROOT/'assets/grimo/source/carol/approved-3d'
spec=importlib.util.spec_from_file_location('measure',Path(__file__).with_name('measure-carol-normal-fleece-v003.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
DEST=OUT/(sys.argv[1] if len(sys.argv)>1 else '.')
FONT=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22);SMALL=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
def tile(path,mirror=False,height=490):
    im,mask,box=m.load(path);im=im.crop(box)
    if mirror:im=ImageOps.mirror(im)
    im=im.resize((round(im.width*height/im.height),height),Image.Resampling.LANCZOS)
    bg=Image.new('RGB',(730,height+20),'white');bg.paste(im,((730-im.width)//2,10),im.getchannel('A'));return bg
def board(name,rows,footer):
    im=Image.new('RGB',(1460,len(rows)*555+45),'white');d=ImageDraw.Draw(im)
    for j,row in enumerate(rows):
        for i,(label,path,mirror) in enumerate(row):
            d.text((i*730+18,j*555+12),label,font=FONT,fill='#33303e');im.paste(tile(path,mirror),(i*730,j*555+43))
    d.text((18,im.height-29),footer,font=SMALL,fill='#50495e');im.save(DEST/name,quality=93)
board('01-authority-comparison.jpg',[[('Approved Front',REF/'carol_front.png',False),('v003 '+DEST.name+' Front',DEST/'front.png',False)],
 [('Approved Side',REF/'carol_side.png',False),('v003 '+DEST.name+' Side (display mirrored)',DEST/'side.png',True)]],
 'Equal 490px character height; original aspect; ground aligned. Native renders are unretouched.')
im=Image.new('RGB',(1460,1110),'white');d=ImageDraw.Draw(im)
for j,view in enumerate(['front','side']):
    ai,a,_=m.normalized(REF/f'carol_{view}.png');ci,c,_=m.normalized(DEST/f'{view}.png',view=='side')
    ov=np.full((*a.shape,3),255,np.uint8);ov[a]=[230,165,188];ov[c]=[127,192,237];ov[a&c]=[177,180,201]
    panel=Image.fromarray(ov);panel.thumbnail((700,490));im.paste(panel,(15,j*550+42))
    d.text((18,j*550+12),view+' overlay: pink authority / blue candidate',font=FONT,fill='#33303e')
    if view=='front':
        for k,(label,box) in enumerate([('Front ear',(65,280,285,420)),('Front face / chin',(245,290,650,485))]):
            aic=ai.crop(box);cic=ci.crop(box)
            for ix,(pic,tag) in enumerate([(aic,'Approved'),(cic,'v003')]):
                pic.thumbnail((345,215));im.paste(pic,(740+ix*355,k*260+70),pic.getchannel('A'))
                d.text((740+ix*355,k*260+35),tag+' '+label,font=SMALL,fill='#33303e')
    else:
        pic=tile(DEST/'3q.png',height=430);im.paste(pic,(730,610));d.text((750,566),'Same asset 3Q diagnostic',font=FONT,fill='#33303e')
im.save(DEST/'02-geometry-overlay.jpg',quality=93)
if all((DEST/f'{v}.png').exists() for v in ['rear','top','opposite_side']):
    board('03-spatial-review.jpg',[[('3Q',DEST/'3q.png',False),('Opposite side',DEST/'opposite_side.png',False)],[('Rear',DEST/'rear.png',False),('Top',DEST/'top.png',False)]], 'One saved full-spatial asset. Diagnostic views are not new authorities.')
    im=Image.new('RGB',(1460,1090),'white');d=ImageDraw.Draw(im)
    for j,(view,label,box) in enumerate([
        ('front','Fleece / pigment',(160,0,740,300)),('front','Face opening / lower face',(260,280,640,482)),
        ('front','Chest / hooves',(220,460,680,600)),('side','Ear integration',(200,230,535,425))]):
        pic,_,_=m.normalized(DEST/f'{view}.png',view=='side');pic=pic.crop(box);pic.thumbnail((690,455))
        x=(j%2)*730;y=(j//2)*530;im.paste(pic,(x+(730-pic.width)//2,y+55),pic.getchannel('A'));d.text((x+18,y+15),label,font=FONT,fill='#33303e')
    im.save(DEST/'04-surface-review.jpg',quality=93)
    im=Image.new('RGB',(1100,290),'#faf9fc');d=ImageDraw.Draw(im)
    for i,(label,path,mirror) in enumerate([('Approved Front',REF/'carol_front.png',False),('v003 Front',DEST/'front.png',False),('v003 Side',DEST/'side.png',True),('v003 3Q',DEST/'3q.png',False)]):
        pic,_,box=m.load(path);pic=pic.crop(box)
        if mirror:pic=ImageOps.mirror(pic)
        pic=pic.resize((round(pic.width*160/pic.height),160),Image.Resampling.LANCZOS);im.paste(pic,(i*275+(275-pic.width)//2,60),pic.getchannel('A'))
        d.text((i*275+40,235),label,font=SMALL,fill='#33303e')
    d.text((20,15),'160px character-height review; static appearance only',font=FONT,fill='#33303e');im.save(DEST/'05-small-scale-review.jpg',quality=93)
print('COMPOSED',DEST)
