"""Arrange actual renders only: resize, place, label. No retouch or generated pixels."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json
ROOT=Path(__file__).resolve().parents[7];E=ROOT/'docs/production/jill/evidence/smartmesh25k-v002'
OLD=ROOT/'docs/production/jill/evidence/smartmesh25k-v001';R=E/'renders';B=E/'boards';B.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
titlefont=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
def resolve(p):return p if p.exists() else p.with_suffix('.jpg')
def sheet(name,title,rows,w=400):
    h=w+42;im=Image.new('RGB',(w*len(rows[0]),92+h*len(rows)),'#eef0ea');d=ImageDraw.Draw(im)
    d.text((12,12),title,font=titlefont,fill='#17231f')
    d.text((12,48),'JILL v002 | HOLD / Human PENDING | Temporary diagnostics, no Tripo approval',font=small,fill='#862d1c')
    for ri,row in enumerate(rows):
        for ci,(p,label) in enumerate(row):
            cell=ImageOps.contain(Image.open(resolve(p)).convert('RGB'),(w,w));x=ci*w;y=92+ri*h
            im.paste(cell,(x+(w-cell.width)//2,y+(w-cell.height)//2));d.text((x+7,y+w+9),label,font=small,fill='#17231f')
    im.save(B/(name+'.jpg'),quality=95)
def pairs(views):return [[(OLD/'renders'/f'after-fbx-{v}.png','v001 | '+v),(R/f'v002-neutral-{v}.png','v002 | '+v)] for v in views]
sheet('01-front-back','Identical cameras / studio / scale: v001 and v002',pairs(['front','back']),450)
sheet('02-sides','Both sides / existing proportions protected',pairs(['left-facing-side','right-facing-side']),450)
sheet('03-three-quarter','Both front 3Q and rear 3Q / same mesh',pairs(['front-three-quarter','opposite-front-three-quarter','rear-three-quarter']),450)
sheet('04-face-clay','Face: small local edits; eye/socket gap remains HOLD',pairs(['face-front','face-three-quarter']),500)
sheet('05-wing-roots','Wing roots / neutral / neck leaves unchanged',pairs(['wing-root-left','wing-root-right']),450)
sheet('06-wing-undersides','Both membrane undersides / no invented thickness',pairs(['wing-underside-detail-left','wing-underside-detail-right']),450)
sheet('07-tail-soles','Tail volume / soles / neutral',pairs(['tail-root','soles']),450)
sheet('08-face-material','Temporary material separation / not formal Texture',[
 [(R/f'face-material-v001-{v}.png','v001 TEMP | '+v),(R/f'face-material-v002-{v}.png','v002 TEMP | '+v)] for v in ['front','3q','left','right']],440)
sheet('09-neutral-extra','Both profile faces and shoulder roots',[
 [(R/'v002-neutral-face-left.png','v002 face +X'),(R/'v002-neutral-face-right.png','v002 face -X')],
 [(R/'v002-neutral-shoulder-left.png','v002 shoulder L'),(R/'v002-neutral-shoulder-right.png','v002 shoulder R')]],450)
proof=json.loads((E/'saved-gate-validation.json').read_text())
for ci,c in enumerate(proof['cases']):
    n=c['name'];oldside='opposite-side' if n in ['WingR_Open','WingR_Close','ArmR_Offer','Combined_Right'] else 'side'
    sheet(f'pose-{ci+1:02}-{n}',n+' / sampled transition and v001 comparison',[
      [(OLD/'renders'/f'half-{n}-front3q.png','v001 half 3Q'),(OLD/'renders'/f'proof-{n}-front3q.png','v001 peak 3Q'),(OLD/'renders'/f'proof-{n}-{oldside}.png','v001 peak side')],
      [(R/f'v002-half-{n}-front3q.png','v002 half 3Q'),(R/f'v002-peak-{n}-front3q.png','v002 peak 3Q'),(R/f'v002-peak-{n}-side.png','v002 peak side')],
      [(R/f'v002-half-{n}-front.png','v002 half front'),(R/f'v002-peak-{n}-front.png','v002 peak front'),(R/f'v002-return-{n}-front.png','v002 return front')]],330)
    sheet(f'roots-{ci+1:02}-{n}',n+' / roots, back and opposite 3Q',[
      [(R/f'v002-half-{n}-detail.png','v002 half detail'),(R/f'v002-peak-{n}-detail.png','v002 peak detail'),(R/f'v002-peak-{n}-rear.png','v002 peak rear 3Q')],
      [(R/f'v002-peak-{n}-opposite-side.png','v002 opposite side'),(R/f'v002-peak-{n}-opposite-front3q.png','v002 opposite front 3Q'),(R/f'v002-return-{n}-side.png','v002 return side')]],330)
# Approved illustrations remain 2D authority; same raster itself is never reinterpreted as a 3D render.
src=ROOT/'assets/grimo/source/jill'
sheet('00-authority-v002','Approved 2D references beside v002 / 3D Human PENDING',[
 [(src/'jill-Identity-canonical.png','Canonical'),(R/'v002-neutral-front-three-quarter.png','v002 front 3Q')],
 [(src/'tripo-generation-pose/jill_bodyonly_front.png','Approved body-only front'),(R/'v002-neutral-front.png','v002 front')],
 [(src/'tripo-generation-pose/jill_bodyonly_left.png','Approved body-only left'),(R/'v002-neutral-left-facing-side.png','v002 +X side')],
 [(src/'tripo-generation-pose/jill_bodyonly_right.png','Approved body-only right'),(R/'v002-neutral-right-facing-side.png','v002 -X side')],
 [(src/'tripo-generation-pose/jill_bodyonly_back.png','Approved body-only back'),(R/'v002-neutral-back.png','v002 back')]],380)
for group,names in [('wings',[c['name'] for c in proof['cases'][:4]]),('arms-tail',[c['name'] for c in proof['cases'][4:8]]),('combined',[c['name'] for c in proof['cases'][8:]])]:
    frames=[]
    for name in names:
        for stage,label in [('neutral','0%'),('half','50%'),('peak','100%'),('half','50% return'),('return','0% return')]:
            im=Image.new('RGB',(640,738),'#eef0ea');d=ImageDraw.Draw(im)
            d.text((10,10),name+' | '+label,font=titlefont,fill='#17231f')
            d.text((10,42),'HOLD / test shapes only / v001 left, v002 right',font=small,fill='#862d1c')
            for row,v in enumerate(['front','rear']):
                before=OLD/'renders'/((('proof-neutral-return-front.png' if v=='front' else 'proof-neutral-rear.png')) if stage in ['neutral','return'] else f'{"half" if stage=="half" else "proof"}-{name}-{v}.png')
                if stage=='neutral':after=R/('v002-neutral-front.png' if v=='front' else 'v002-neutral-gif-rear.png')
                elif stage=='return' and v=='rear':after=R/f'v002-return-{name}-gif-rear.png'
                else:after=R/f'v002-{stage}-{name}-{v}.png'
                for col,p in enumerate([before,after]):
                    tile=Image.open(resolve(p)).convert('RGB').resize((320,320),Image.Resampling.LANCZOS);im.paste(tile,(col*320,72+row*333))
            frames.append(im)
    frames[0].save(B/f'diagnostic-{group}-v001-v002.gif',save_all=True,append_images=frames[1:],duration=650,loop=0,optimize=False)
print('PACKAGED',len(list(B.iterdir())))
