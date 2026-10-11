"""Lay out existing authority PNGs and neutral-clay evidence. No image generation."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v002'
PACK=ROOT/'assets/grimo/production/shushu/image-reference/reference-pack-v001'
items=json.loads((PACK/'manifest.json').read_text(encoding='utf-8'))['items']
refs={int(x['name'][:2]):PACK/x['group']/(x['name']+'.png') for x in items}
primary=ROOT/'assets/grimo/source/shushu'
def render(name):return OUT/'renders'/(name+'.png')
def board(name,title,subtitle,cells):
    cols=4;cw=288;ch=346;pad=12;header=80
    rows=math.ceil(len(cells)/cols)
    canvas=Image.new('RGB',(cols*cw+(cols+1)*pad,header+rows*(ch+pad)+pad),(246,246,246))
    draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    big=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',25)
    draw.text((pad,12),title,fill=(30,30,30),font=big)
    draw.text((pad,47),subtitle,fill=(65,65,65),font=font)
    for i,(label,path) in enumerate(cells):
        x=pad+(i%cols)*(cw+pad);y=header+(i//cols)*(ch+pad)
        tile=Image.new('RGB',(cw,ch-29),(235,235,235))
        source=Image.open(path).convert('RGBA');source.thumbnail(tile.size,Image.Resampling.LANCZOS)
        tile.paste(source,((cw-source.width)//2,(tile.height-source.height)//2),source.getchannel('A'))
        canvas.paste(tile,(x,y));draw.text((x,y+ch-24),label,fill=(35,35,35),font=font)
    canvas.save(OUT/(name+'.png'))

board('review-01-identity','SHUSHU v002 | identity / source comparison',
      'Authorities are unchanged. All 3D renders use the same uncolored clay and inspection light.',[
('Canonical identity',primary/'shushu-Identity-canonical.png'),('Original B / front',render('donor-front')),
('Previous v001 / front',render('v001-front')),('v002 / front',render('neutral-front')),
('Approved body-only side',primary/'tripo-generation-pose/shushu_bodyonly_left.png'),('Original B / side',render('donor-side')),
('v002 / side',render('neutral-side')),('v002 / three-quarter',render('neutral-three-quarter')),
('Approved body-only back',primary/'tripo-generation-pose/shushu_bodyonly_back.png'),('Original B / rear',render('donor-rear')),
('v002 / rear',render('neutral-rear')),('Approved 03 / three-quarter',refs[3])])
board('review-02-face','SHUSHU v002 | face / independent controls',
      'Human appearance gate PENDING. No pupils, color, highlights, textures or UVs are authored.',[
('Approved 02 / neutral',refs[2]),('v002 / neutral',render('face-neutral')),
('Original B / face',render('donor-face')),('Previous v001 / face',render('v001-face')),
('Approved 04 / half blink',refs[4]),('v002 / half blink',render('face-half')),
('Approved 05 / closed',refs[5]),('v002 / closed',render('face-closed')),
('Approved 06 / small opening',refs[6]),('v002 / small opening',render('face-mouth-open')),
('Approved 07 / smile',refs[7]),('v002 / closed-eye smile',render('face-smile')),
('Approved 08 / surprise',refs[8]),('v002 / tiny surprise',render('face-surprise')),
('v002 / left lid only',render('face-left-closed')),('v002 / combined controls',render('face-combined'))])
board('review-03-support-contact','SHUSHU v002 | support / bounded contact',
      '09/10 = feet-supported rest; 17 = rump-supported seat. Temporary fixture is a separate object.',[
('Approved 09 / shallow rest',refs[9]),('v002 / shallow rest front',render('rest-front')),
('Approved 17 / true seat',refs[17]),('v002 / rump-supported front',render('seat-front')),
('Approved 10 / shallow side',refs[10]),('v002 / shallow rest side',render('rest-side')),
('v002 / seated side',render('seat-side')),('v002 / seated three-quarter',render('seat')),
('Approved 11 / one-paw offer',refs[11]),('v002 / one-paw offer',render('offer')),
('Approved 12 / two-paw hold',refs[12]),('v002 / bounded fixture hold',render('hold')),
('Approved 13 / head tilt',refs[13]),('v002 / head turn + tilt',render('head-turn')),
('Approved 14 / cheek pressure',refs[14]),('v002 / cheek + belly pressure',render('pressure')),
('Approved 15 / self-groom',refs[15]),('v002 / lower-cheek contact',render('groom')),
('v002 / chest contact',render('chest-groom')),('Approved 16 / food anticipation',refs[16])])
print('THREE_REVIEW_BOARDS_COMPLETE')
