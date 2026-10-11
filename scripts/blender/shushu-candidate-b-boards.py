"""Compact contact sheets from actual rendered evidence and unchanged references."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/candidate-b-8481'
R=OUT/'renders'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)

def board(name,items,cols=4,cell=(360,435)):
    rows=(len(items)+cols-1)//cols;w,h=cell
    out=Image.new('RGB',(cols*w,rows*h),(239,242,247));draw=ImageDraw.Draw(out)
    for i,(label,p) in enumerate(items):
        with Image.open(p) as im:
            im=im.convert('RGBA');im.thumbnail((w-16,h-42))
            x=i%cols*w+(w-im.width)//2;y=i//cols*h+30+(h-42-im.height)//2
            out.paste(im,(x,y),im)
        draw.text((i%cols*w+8,i//cols*h+8),label,font=FONT,fill=(30,37,50))
    out.save(OUT/name)

def main():
    refs=ROOT/'assets/grimo/source/shushu'
    board('canonical-comparison.png',[
        ('Canonical identity',refs/'shushu-Identity-canonical.png'),
        ('Approved generation front',refs/'tripo-generation-pose/shushu_bodyonly_front.png'),
        ('B raw neutral front',R/'neutral-front.png'),('B FBX wire',R/'wire-front.png'),
        ('Approved left-facing input',refs/'tripo-generation-pose/shushu_bodyonly_left.png'),('B left-facing profile',R/'neutral-left-facing.png'),
        ('Approved right-facing input',refs/'tripo-generation-pose/shushu_bodyonly_right.png'),('B right-facing profile',R/'neutral-right-facing.png'),
        ('Approved back input',refs/'tripo-generation-pose/shushu_bodyonly_back.png'),('B back',R/'neutral-back.png'),('B front 3/4',R/'neutral-front-threequarter.png'),('B rear 3/4',R/'neutral-rear-threequarter.png')])
    names=['neutral','head-yaw-left','head-down','head-roll','paw-left-offer','paw-right-offer','both-paws-hold','gift-low-offer','weight-shift','low-squat','toward-sitting','support-compression','cheek-pressure','belly-pressure','ear-left','occupied-paw-head-touch']
    board('deformation-contact-sheet.png',[(n,R/f'pose-{n}-threequarter.png') for n in names])
    board('support-and-seams.png',[(n,R/(n+'.png')) for n in ['neutral-left-facing','pose-low-squat-side','pose-toward-sitting-side','raw-pose-toward-sitting','neutral-front','pose-neutral-front','raw-pose-head-down','pose-head-down-threequarter']],4)
    board('raw-face-probes.png',[(n,R/('detail-'+n+'.png')) for n in ['raw-lid-left-half','raw-lid-left-closed','raw-lid-right-closed','mouth-open-raw']],4,(360,435))
    if (R/'repair-eyes-open-front.png').exists():
        board('local-face-repair-proof.png',[(n,R/('repair-'+n+'-front.png')) for n in ['eyes-open','left-half','left-closed','right-closed','both-closed','gaze-left','gaze-right','mouth-small-open']],4,(360,435))
    if (R/'contact-repaired-both-hold-front.png').exists():
        board('contact-and-handoff.png',[(label,R/(name+'.png')) for label,name in [
            ('Initial hold: body interference','pose-both-paws-hold-threequarter'),
            ('Bounded reachable hold','contact-repaired-both-hold-threequarter'),
            ('Hold plus head touch','contact-hold-plus-head-touch'),
            ('GLB reimport stressed sample','roundtrip-frame12')]])
    if '--compact' in sys.argv:
        # Remove only our reproducible intermediate renders after their comparison boards are saved.
        keep={'neutral-'+n+'.png' for n in ['front','left-facing','right-facing','back','front-threequarter','rear-threequarter','top','underside']}
        keep.update({'wire-front.png','wire-front-threequarter.png','repair-both-closed-threequarter.png',
                     'repair-sitting-local-smoothing.png','roundtrip-frame12.png',
                     'contact-repaired-both-hold-front.png','contact-repaired-both-hold-threequarter.png',
                     'contact-repaired-both-hold-side.png','contact-hold-plus-head-touch.png',
                     'pose-toward-sitting-side.png','raw-pose-toward-sitting.png','detail-raw-lid-left-closed.png'})
        allowed=('neutral-','wire-','pose-','raw-pose-','detail-','repair-','contact-','roundtrip-')
        for p in R.glob('*.png'):
            if p.name not in keep and p.name.startswith(allowed):p.unlink()
    print('Evidence boards saved')

if __name__=='__main__':main()
