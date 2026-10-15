"""Compose existing Blender captures without altering their content."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json, sys

ROOT=Path(__file__).resolve().parents[7]
E=ROOT/'docs/production/jill/evidence/smartmesh25k-v001'
R=E/'renders'; B=E/'boards'; B.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
titlefont=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',25)
def sheet(name,title,rows,width=380):
    cols=len(rows[0]); h=width+44
    canvas=Image.new('RGB',(cols*width,len(rows)*h+92),'#eef0ea')
    draw=ImageDraw.Draw(canvas)
    draw.text((14,12),title,font=titlefont,fill='#17231f')
    draw.text((14,49),'JILL | Human Geometry Gate: HOLD / pending | Diagnostic evidence, not approval',font=small,fill='#862d1c')
    for ri,row in enumerate(rows):
        for ci,(path,label) in enumerate(row):
            x=ci*width;y=92+ri*h
            im=Image.open(path).convert('RGB');im=ImageOps.contain(im,(width,width))
            canvas.paste(im,(x+(width-im.width)//2,y+(width-im.height)//2))
            draw.text((x+8,y+width+9),label,font=small,fill='#17231f')
    canvas.save(B/(name+'.jpg'),quality=94)
def pair(views):return [[(R/f'before-fbx-{v}.png','BEFORE FBX | '+v),(R/f'after-fbx-{v}.png','AFTER | '+v)] for v in views]
sheet('01-orthographic','Identical cameras / shading / scale: before and after',pair(['front','left-facing-side','right-facing-side','back']),500)
sheet('02-three-quarter','Silhouette comparison / no global geometry change',pair(['front-three-quarter','opposite-front-three-quarter','rear-three-quarter']),500)
sheet('03-wings','Wing underside and both roots / retained source surfaces',pair(['wing-underside','wing-root-left','wing-root-right']),500)
sheet('03b-wing-undersides','Closer underside views / same cameras before and after',pair(['wing-underside-detail-left','wing-underside-detail-right']),500)
sheet('04-tail-feet-face','Tail root / soles / face: inspect remaining source defects',pair(['tail-root','soles','face-front','face-three-quarter']),500)
proof=json.loads((E/'deformation-validation.json').read_text())
for group in range(3):
    rows=[]
    for c in proof['cases'][group*4:group*4+4]:
        n=c['name']
        side='opposite-side' if n in ['WingR_Open','WingR_Close','ArmR_Offer','Combined_Right'] else 'side'
        rows.append([(R/'proof-neutral-front3q.png',n+' | neutral 3Q'),
                     (R/f'half-{n}-front3q.png','50% | front 3Q'),
                     (R/f'proof-{n}-front3q.png','100% | front 3Q'),
                     (R/f'proof-{n}-front.png','100% | front'),
                     (R/f'proof-{n}-{side}.png','100% | side ('+('-X' if side=='opposite-side' else '+X')+')')])
    sheet(f'0{5+group}-posed-appearance',f'Appearance lock: posed comparison {group+1}/3 | no approved pose reference',rows,320)
for group in range(2):
    names=[c['name'] for c in proof['cases'][group*4:group*4+4]]
    sheet(f'0{8+group}-contact-screen','Red: new crossing candidates / not a penetration-depth measurement',
          [[(R/f'contact-neutral-{n}.png',n+' | same faces at neutral'),(R/f'contact-screen-{n}.png',n+' | peak / HOLD')] for n in names],500)
src=ROOT/'assets/grimo/source/jill'
sheet('00-approved-authority','Approved 2D appearance authority / 3D identity still pending',
      [[(src/'jill-Identity-canonical.png','Canonical illustration'),(src/'tripo-generation-pose/jill_bodyonly_front.png','Approved body-only: front')],
       [(src/'tripo-generation-pose/jill_bodyonly_left.png','Approved body-only: left'),(src/'tripo-generation-pose/jill_bodyonly_right.png','Approved body-only: right')],
       [(src/'tripo-generation-pose/jill_bodyonly_back.png','Approved body-only: back'),(R/'after-fbx-front-three-quarter.png','Untextured 3D: Human identity pending')]],460)
if '--boards-only' in sys.argv:
    print('Review boards complete; existing GIFs retained')
    raise SystemExit(0)
for label,indices in [('wings',range(4)),('arms-tail',range(4,8)),('combined',range(8,12))]:
    frames=[]
    for ci in indices:
        n=proof['cases'][ci]['name']
        for state,prefix in [('Neutral',None),('50%','half'),('100%','proof'),('50%','half'),('Neutral',None)]:
            out=Image.new('RGB',(900,512),'#eef0ea');d=ImageDraw.Draw(out)
            d.text((12,8),f'{n} | {state} | HOLD / diagnostic only',font=font,fill='#17231f')
            d.text((12,36),'Front + rear 3Q | sampled sequence; not continuous motion certification',font=small,fill='#862d1c')
            for col,view in enumerate(['front','rear']):
                fn=(f'{prefix}-{n}-{view}.png' if prefix else ('proof-neutral-return-front.png' if view=='front' else 'proof-neutral-rear.png'))
                im=Image.open(R/fn).convert('RGB').resize((450,450),Image.Resampling.LANCZOS)
                out.paste(im,(450*col,62))
            frames.append(out)
    frames[0].save(B/f'diagnostic-{label}.gif',save_all=True,append_images=frames[1:],duration=650,loop=0)
print('Review boards and sampled GIFs complete')
