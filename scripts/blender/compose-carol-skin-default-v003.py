"""Label and crop saved, unretouched render evidence on white boards."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/skin-default-v003'
SRC=ROOT/'assets/grimo/source/carol'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
TITLE=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',31)


def tile(canvas,draw,col,row,label,path,crop,cell=(520,440),margin=52):
    w,h=cell
    x=col*w;y=margin+row*(h+46)
    draw.text((x+14,y+8),label,font=FONT,fill='#353038')
    im=Image.open(path).convert('RGBA')
    if crop: im=im.crop(crop)
    scale=min((w-20)/im.width,(h-50)/im.height)
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    white=Image.new('RGBA',im.size,'white');white.alpha_composite(im)
    canvas.paste(white.convert('RGB'),(x+(w-im.width)//2,y+43))


def board(name,title,rows,cell=(520,440)):
    cols=max(len(row) for row in rows);w,h=cell
    canvas=Image.new('RGB',(cols*w,52+len(rows)*(h+46)),'white')
    draw=ImageDraw.Draw(canvas)
    draw.text((15,10),title,font=TITLE,fill='#29242d')
    for row,items in enumerate(rows):
        for col,(label,path,crop) in enumerate(items):
            tile(canvas,draw,col,row,label,path,crop,cell)
    canvas.save(OUT/name)


def render(folder,view):return OUT/folder/(view+'.png')


board('ear-authority-comparison.png','CAROL / ear identity / references above, saved Skin below',[
    [('Identity / left ear',SRC/'carol-Identity-canonical.png',(272,246,399,374)),
     ('Approved Normal / Front ear',SRC/'approved-3d/carol_front.png',(0,585,365,880)),
     ('Approved Normal / Side ear',SRC/'approved-3d/carol_side.png',(470,490,795,740)),
     ('New Skin / ear close',render('new-skin','ear-side'),None)],
    [('New Skin / Front',render('new-skin','front'),(0,155,760,395)),
     ('New Skin / Side',render('new-skin','side'),(225,155,505,390)),
     ('New Skin / front 3Q',render('new-skin','front-3q'),(78,160,715,430)),
     ('New Skin / Top',render('new-skin','ear-top'),None)],
],(520,440))

board('skin-baseline-comparison.png','CAROL / matched camera, light and scale / old, v004, new',[
    [(label,render('old-skin',view),None) for label,view in [('v002 / Front','front'),('v002 / Side','side'),('v002 / front 3Q','front-3q')]],
    [(label,render('v004-internal-skin',view),None) for label,view in [('v004 Skin / Front','front'),('v004 Skin / Side','side'),('v004 Skin / front 3Q','front-3q')]],
    [(label,render('new-skin',view),None) for label,view in [('v003 default / Front','front'),('v003 default / Side','side'),('v003 default / front 3Q','front-3q')]],
],(600,490))

board('ear-v001-vs-v003.png','CAROL / ear v001 above, refined v003 below / matched view',[
    [(label,render('ear-v001',view),None) for label,view in [('v001 / Front','front'),('v001 / Side detail','ear-side'),('v001 / Top detail','ear-top')]],
    [(label,render('new-skin',view),None) for label,view in [('v003 / Front','front'),('v003 / Side detail','ear-side'),('v003 / Top detail','ear-top')]],
],(600,490))

board('fleece-occlusion.png','CAROL / refined Skin ears under unchanged v004 Fleece / diagnostic',[
    [(label,render('fleece-occlusion',view),None) for label,view in [('Front','front'),('front 3Q','front-3q'),('Side','side')]],
],(600,490))
