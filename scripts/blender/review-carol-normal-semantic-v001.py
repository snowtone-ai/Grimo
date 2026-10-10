"""Compose unretouched Blender captures and verify same-asset evidence."""
from pathlib import Path
import hashlib,json,sys
from PIL import Image,ImageDraw,ImageFont
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-normal-semantic-v001.blend'
FOLDER=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'artifacts/carol-semantic/draft')
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def board(folder,name='spatial.jpg'):
    manifest=json.loads((folder/'render-manifest.json').read_text())
    assert manifest['asset_sha256']==sha(ASSET),'Stale asset'
    views=list(manifest['views']);w=420;h=460
    im=Image.new('RGB',(w*min(4,len(views)),h*((len(views)+3)//4)),(248,248,253));d=ImageDraw.Draw(im)
    for i,v in enumerate(views):
        p=folder/(v+'.png');assert sha(p)==manifest['views'][v]['sha256'],'Stale view '+v
        pic=Image.open(p).convert('RGBA');pic.thumbnail((w,h-40));x=i%4*w;y=i//4*h
        im.paste(pic,(x+(w-pic.width)//2,y+38),pic);d.text((x+16,y+10),v+' / '+manifest['mode'],font=FONT,fill=(55,55,70))
    im.save(folder/name,quality=95)

board(FOLDER)
print('Verified and composed',FOLDER)

if '--final' in sys.argv:
    out=ROOT/'docs/production/carol/evidence/normal-semantic-v001'
    for mode in ['clay','silhouette']:board(out/mode)
    def normalized(path,height=460):
        a=Image.open(path).convert('RGBA');rgb=np.array(a)[:,:,:3]
        mask=np.array(a)[:,:,3]>100
        if np.all(mask):mask=np.sum(255-rgb.astype(float),axis=2)>55
        yy,xx=np.where(mask);a=a.crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1))
        a=a.resize((round(a.width*height/a.height),height),Image.Resampling.LANCZOS)
        return a
    ref=ROOT/'assets/grimo/source/carol/approved-3d'
    compare=Image.new('RGB',(1440,1100),'white');draw=ImageDraw.Draw(compare);sources=[]
    for row,v in enumerate(['front','side']):
        for col,(label,p) in enumerate([('APPROVED AUTHORITY',ref/('carol_'+v+'.png')),('SEMANTIC CANDIDATE',out/'beauty'/(v+'.png'))]):
            a=normalized(p)
            if v=='side' and col==1:a=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            compare.paste(a,(col*720+(720-a.width)//2,row*550+55),a)
            draw.text((col*720+25,row*550+15),label+' / '+v+(' / mirrored display' if v=='side' and col else ''),font=FONT,fill=(45,45,60))
            sources.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'display_mirrored':v=='side' and col==1})
    compare.save(out/'authority-comparison.jpg',quality=95)
    diagnostic=Image.new('RGB',(1440,1550),(248,248,253));draw=ImageDraw.Draw(diagnostic)
    for row,mode in enumerate(['beauty','clay','silhouette']):
        for col,v in enumerate(['front','yaw+45','side']):
            a=Image.open(out/mode/(v+'.png')).convert('RGBA');a.thumbnail((480,470))
            diagnostic.paste(a,(col*480+(480-a.width)//2,row*515+40),a)
            draw.text((col*480+20,row*515+10),mode+' / '+v,font=FONT,fill=(45,45,60))
    diagnostic.save(out/'form-and-look.jpg',quality=95)
    (out/'board-sources.json').write_text(json.dumps({'asset_sha256':sha(ASSET),'authority_comparison':'Equal visible height; side candidate mirrored only for comparison. Spatial board uses unchanged camera scale. No shape retouching.','sources':sources},indent=2))
    print('Final evidence integrity PASS')
