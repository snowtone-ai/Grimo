"""Arrange existing renders/references; never edits source references. Ordinary Python + Pillow."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import json, tempfile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v001'
R=OUT/'renders'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)

def board(name,items,columns=4,size=(320,360)):
    w,h=size;rows=(len(items)+columns-1)//columns
    im=Image.new('RGB',(columns*w,rows*(h+40)),(236,239,242));d=ImageDraw.Draw(im)
    for i,(label,path) in enumerate(items):
        x=(i%columns)*w;y=(i//columns)*(h+40)
        d.text((x+8,y+10),label,font=SMALL,fill=(30,35,43))
        src=Image.open(path).convert('RGB');src=ImageOps.contain(src,(w-8,h-8))
        im.paste(src,(x+(w-src.width)//2,y+40+(h-src.height)//2))
    im.save(OUT/name)

def main():
    board('face-review.png',[(label,R/file) for label,file in [
        ('Open / small closed smile','00-neutral.png'),('Half blink / arc corrective','04-half.png'),
        ('Closed / integrated skin','05-closed.png'),('Reopen = original geometry','00-neutral.png'),
        ('Left independent','06-left-closed.png'),('Right independent','07-right-closed.png'),
        ('Bounded gaze + left blink','08-gaze-blink.png'),('Small mouth / shallow interior','09-mouth-open.png')]])
    board('support-contact-review.png',[(label,R/file) for label,file in [
        ('Standing / fixed soles','00-neutral.png'),('Lower settle','10-settle.png'),
        ('Low rest / feet support','11-rest.png'),('Recovery = standing','00-neutral.png'),
        ('Low rest / side','12-rest.png'),('Low rest / low rear','13-rest.png'),
        ('One paw offer / no extension','14-offer.png'),('Bounded two-paw hold','15-hold.png'),
        ('Hold / side clearance','16-hold.png'),('Holding + cheek touch','17-hold-touch.png'),
        ('Head turn and tilt','18-head-turn.png'),('Local cheek + belly pressure','19-pressure.png')]])
    refs=ROOT/'assets/grimo/source/shushu'
    board('before-after-review.png',[
        ('Canonical identity',refs/'shushu-Identity-canonical.png'),
        ('Approved front',refs/'tripo-generation-pose/shushu_bodyonly_front.png'),
        ('B source / same studio',R/'source-front.png'),('Repaired candidate',R/'00-neutral.png'),
        ('Approved side',refs/'tripo-generation-pose/shushu_bodyonly_left.png'),
        ('B source / same studio',R/'source-side.png'),('Repaired candidate / side',R/'02-neutral.png'),
        ('Repaired threequarter',R/'01-neutral.png')])
    frames=json.loads((Path(tempfile.gettempdir())/'grimo-shushu-v001-review/frames.json').read_text())
    for family,paths in frames.items():
        ims=[]
        for p in paths:
            im=Image.open(p).convert('RGB');d=ImageDraw.Draw(im)
            d.rectangle((0,0,400,26),fill=(236,239,242));d.text((6,4),Path(p).stem,font=SMALL,fill=(30,35,43));ims.append(im)
        ims[0].save(OUT/(family+'-timeline.gif'),save_all=True,append_images=ims[1:],duration=180 if family=='face' else 280,loop=0,optimize=True)

if __name__=='__main__':main()
