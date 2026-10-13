"""Arrange unaltered Blender renders for the pending Human Geometry Gate."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v003/human-gate-revision'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
TITLE=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',25)
def board(name,title,rows,width=280):
    h=round(width*540/480);canvas=Image.new('RGB',(width*len(rows[0][1]),96+len(rows)*(h+35)),(244,243,241));draw=ImageDraw.Draw(canvas)
    draw.text((15,12),title,font=TITLE,fill=(25,25,25));draw.text((15,46),'Shushu v003 continuation / identical orthographic cameras / HUMAN PENDING',font=FONT,fill=(65,65,65));draw.text((15,69),'Colour = temporary diagnostic identity cues; no approved texture or final gaze claim',font=FONT,fill=(85,65,65))
    for r,(label,items) in enumerate(rows):
        for c,(file,caption) in enumerate(items):
            x=c*width;y=96+r*(h+35);draw.text((x+8,y+7),caption,font=FONT,fill=(25,25,25));im=Image.open(OUT/'renders'/f'{file}.png').convert('RGB');im.thumbnail((width,h),Image.Resampling.LANCZOS);canvas.paste(im,(x+(width-im.width)//2,y+35))
    canvas.save(OUT/name)
views=['front','side','3q']
if (OUT/'renders/donor-colour-3q.png').exists():
    for kind in ['clay','colour']:
        rows=[]
        for variant,label in [('donor','Original donor'),('before','Before'),('size-only','Size only'),('surround-only','Surround only'),('combined','Combined candidate')]:
            rows.append((label,[(f'donor-{kind}-{v}' if variant=='donor' else f'eye-{variant}-{kind}-{v}',f'{label} / {v}') for v in views]))
        board(f'01-eyes-{kind}.png',f'Eye alternatives / {kind}',rows)
if (OUT/'renders/blink-wink-colour-3q.png').exists():
    for kind in ['clay','colour']:
        board(f'02-mouth-{kind}.png',f'Neutral > small > donor-size opening > smile / {kind}',[(state,[(f'mouth-{state}-{kind}-{v}',f'{state} / {v}') for v in views]) for state in ['neutral','small','donor-open','smile']])
        board(f'03-seat-{kind}.png',f'Standing / intermediate / seat / {kind}',[(state,[(f'{state}-{kind}-{v}',f'{state} / {v}') for v in views]) for state in ['standing','seat25','seat50','seat75','seated']])
        board(f'04-blink-{kind}.png',f'Retained eyelid mechanism / {kind}',[(state,[(f'blink-{state}-{kind}-{v}',f'{state} / {v}') for v in views]) for state in ['half','closed','wink']])
        if kind=='clay':board('05-seat-before-after.png','Local proximal-thigh correction',[(variant,[(f'seat-{variant}-clay-{v}',f'{variant} / {v}') for v in views]) for variant in ['before','combined']])
    board('00-overview.png','Eye size / seated thigh / full opening - review overview',[
        ('eyes',[(f'donor-colour-front','Donor / eye'),('eye-before-colour-front','Before / eye'),('eye-size-only-colour-front','Size only / eye'),('eye-combined-colour-front','Selected / eye')]),
        ('seat',[('seat-before-clay-side','Before / seated side'),('seated-clay-side','Revised / seated side'),('seated-colour-front','Revised / seated front'),('seated-colour-3q','Revised / seated 3q')]),
        ('mouth',[(f'mouth-{state}-colour-front',state) for state in ['neutral','small','donor-open','smile']])],280)
paths=sorted(OUT.glob('*.png'))+sorted((OUT/'renders').glob('*.png'))
cameras=json.loads((OUT/'cameras.json').read_text())
assert len(cameras)==108 and len(list((OUT/'renders').glob('*.png')))==108
for view in views:
    baseline=cameras['eye-before-clay-'+view]
    for prefix in ['donor','eye-size-only','eye-surround-only','eye-combined']:
        row=cameras[prefix+'-clay-'+view];assert row==baseline,(prefix,view)
    for state in ['neutral','small','donor-open','smile']:
        assert cameras['mouth-'+state+'-clay-'+view]==baseline
manifest={'Human_Gate':'PENDING','renders':108,'boards':len(list(OUT.glob('*.png'))),'identical_clay_cameras_checked':True,'files':[{'path':p.relative_to(OUT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in paths]}
(OUT/'review-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('HUMAN_GATE_BOARDS_COMPLETE')
