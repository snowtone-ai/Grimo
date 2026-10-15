"""Assemble unretouched render contact sheets for visual review (Pillow)."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
E=Path(__file__).resolve().parents[2]/'docs/production/jill/rig-other-v001'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
sets=[('01-wings',['neutral','wing-L-open-peak','wing-L-fold-peak','wing-R-open-peak','wing-R-fold-peak','both-wings-open-peak','both-wings-fold-peak']),
 ('02-body',['paw-L-offer-peak','paw-R-offer-peak','tail-left-peak','tail-right-peak','head-gaze-peak','low-support-peak','paw-IK-contact-peak']),
 ('03-face-composite',['blink-half','blink-peak','mouth-close-peak','mouth-open-peak','combined-left-half','combined-left-peak','combined-right-peak']),
 ('04-return',['both-wings-fold-return','blink-return','combined-left-return','low-support-return']),
 ('06-glb-roundtrip',['glb-neutral','glb-blink','glb-combined-left'])]
for board,names in sets:
    b=Image.new('RGB',(1440,len(names)*504),(239,239,235));d=ImageDraw.Draw(b)
    for i,name in enumerate(names):
        for j,view in enumerate(['front','side','3q']):
            im=Image.open(E/'renders'/f'{name}-{view}.png').convert('RGB');im.thumbnail((480,480));b.paste(im,(j*480,i*504+24))
            d.text((j*480+8,i*504+4),f'{name} / {view}',font=font,fill=(20,30,25))
    b.save(E/(board+'.jpg'),quality=94)
names=['detail-neutral-back','detail-fold-back','detail-offer-shoulder','detail-combined-back','detail-tail-root','blink-face-3q','mouth-close-face-3q','head-gaze-face-3q']
b=Image.new('RGB',(1440,4*744),(239,239,235));d=ImageDraw.Draw(b)
for i,name in enumerate(names):
    x=i%2*720;y=i//2*744;im=Image.open(E/'renders'/f'{name}.png').convert('RGB');b.paste(im,(x,y+24));d.text((x+8,y+4),name,font=font,fill=(20,30,25))
b.save(E/'05-details.jpg',quality=94)
names=['neutral','combined-left-peak','glb-combined-left']
b=Image.new('RGB',(1440,504),(239,239,235));d=ImageDraw.Draw(b)
for j,name in enumerate(names):
    im=Image.open(E/'renders'/f'{name}-3q.png').convert('RGB');im.thumbnail((480,480));b.paste(im,(480*j,24));d.text((480*j+8,4),name+' / Human PENDING',font=font,fill=(20,30,25))
b.save(E/'00-overview.jpg',quality=94)
print('EVIDENCE_BOARDS_READY')
