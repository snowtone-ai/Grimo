from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root=Path.cwd()
out=root/'docs/production/carol/evidence/blockout-v002'
entries=[('Identity canonical (posed)',root/'assets/grimo/source/carol/carol-Identity-canonical.png'),
('v001 / front perspective',root/'docs/production/carol/evidence/blockout-v001/carol-front-perspective-16x9.png'),
('v002 / front perspective',out/'carol-v002-front-perspective.png'),
('v002 / three-quarter',out/'carol-v002-three-quarter.png'),
('v002 / side',out/'carol-v002-side.png'),
('v002 / back',out/'carol-v002-back.png')]
board=Image.new('RGB',(1800,1280),'#edf0f5')
d=ImageDraw.Draw(board)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
d.text((32,22),'CAROL / Structural blockout v002 / Human Gate pending',font=font,fill='#273047')
d.text((32,60),'Images independently fit to panels. Compare form; this is not a common-scale measurement plate.',font=small,fill='#536078')
for i,(label,path) in enumerate(entries):
    x=(i%3)*600;y=110+(i//3)*575
    d.rounded_rectangle((x+14,y+8,x+586,y+555),radius=16,fill='white')
    d.text((x+32,y+25),label,font=font,fill='#273047')
    im=Image.open(path).convert('RGBA')
    bbox=im.getchannel('A').getbbox()
    if bbox: im=im.crop(bbox)
    im.thumbnail((530,465),Image.Resampling.LANCZOS)
    board.paste(im,(x+(600-im.width)//2,y+76+(465-im.height)//2),im)
board.save(out/'carol-v002-comparison.png')
