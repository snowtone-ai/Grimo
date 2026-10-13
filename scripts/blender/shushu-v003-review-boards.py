"""Pack unchanged render evidence into concise review boards and preview GIFs."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v003'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
TITLE=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',27)

def board(filename,title,items,cols=4,width=380):
    height=round(width*720/640);rows=(len(items)+cols-1)//cols
    canvas=Image.new('RGB',(cols*width,72+rows*(height+36)),(242,242,240));draw=ImageDraw.Draw(canvas)
    draw.text((18,15),title,font=TITLE,fill=(25,25,25))
    draw.text((18,47),'Shushu v003 / geometry review / Human acceptance pending',font=FONT,fill=(70,70,70))
    for i,(name,label) in enumerate(items):
        x=(i%cols)*width;y=72+(i//cols)*(height+36)
        draw.text((x+10,y+7),label,font=FONT,fill=(25,25,25))
        im=Image.open(OUT/'renders'/f'{name}.png').convert('RGB');im.thumbnail((width,height),Image.Resampling.LANCZOS)
        canvas.paste(im,(x+(width-im.width)//2,y+36))
    canvas.save(OUT/filename)

views=[('front','Front'),('left','Exact left'),('right','Exact right'),('three-quarter','Three-quarter'),('rear','Rear')]
board('review-01-identity.png','Original donor / v003 neutral - identical cameras',[(prefix+'-'+v,prefix+' / '+label) for prefix in ['donor','neutral'] for v,label in views],5,300)
board('review-02-face.png','Face - independent controls and native profile',[
    ('face-neutral','Neutral'),('face-half','Half blink'),('face-closed','Closed'),('face-reopen','Reopened'),
    ('face-wink','One eye only'),('face-gaze-left','Gaze geometry / left'),('face-gaze-right','Gaze geometry / right'),('face-neutral-side','Exact side / depth'),
    ('face-mouth-open','Small mouth opening'),('face-smile','Small smile'),('face-surprise','Small surprise'),('face-smile-three-quarter','Smile / three-quarter'),
    ('face-partial-three-quarter','70% blink / three-quarter'),('face-closed-three-quarter','Closed / three-quarter'),('turn-tilt','Head turn and tilt'),('self-contact-detail','Local cheek contact')],4,340)
board('review-03-support-contact.png','Rump support, folded legs and bounded contact',[
    ('seated-front','Seated / front'),('seated-left','Seated / exact side'),('seat100','Seated / three-quarter'),('seated-rear-three-quarter','Seated / rear three-quarter'),
    ('offer','Offer'),('hold-front','Hold / inspection prop'),('self-contact','Self contact / head participates'),('release','Released / neutral')],4,380)
board('review-04-transition.png','Standing to seated - inspect the whole transition',[
    ('neutral-three-quarter','Standing'),('seat25','25%'),('seat50','50%'),('seat75','75%'),('seat100','Seated'),('rest','Rest pose')],3,360)
for prefix,duration,label in [('seat',167,'Seating study - editable proof, not final timing'),('blink',83,'Blink study - untextured geometry')]:
    files=sorted((OUT/'preview-frames').glob(prefix+'-*.png'))
    if not files:continue
    frames=[]
    for file in files:
        im=Image.open(file).convert('RGB');c=Image.new('RGB',(im.width,im.height+34),(245,245,243));c.paste(im,(0,34))
        ImageDraw.Draw(c).text((8,8),label,font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13),fill=(25,25,25));frames.append(c)
    frames[0].save(OUT/(prefix+'-proof.gif'),save_all=True,append_images=frames[1:],duration=duration,loop=0,optimize=True)
print('REVIEW_BOARDS_COMPLETE')
