"""Compose the fixed-registration v012 rejection packet with Pillow."""
import importlib.util
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('evidence', ROOT/'scripts/blender/carol-v008-evidence.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)
directory = ROOT/'docs/production/carol/evidence/reconstruction-v012'
data = json.loads((directory/'measurements.json').read_text())
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)
current = {view:e.background(Image.open(directory/f'skin-{view}.png')).resize((640,640))
           for view in ('front','side')}
locked = {view:e.background(e.registered(data['reference_registration'][f'skin-{view}'],640))
          for view in ('front','side')}
overlays = {view:Image.blend(locked[view],current[view],.5) for view in ('front','side')}
for view in ('front','side'):
    overlays[view].save(directory/f'skin-{view}-overlay.png')
    current[view].crop((160,210,480,455) if view=='front' else (20,210,345,455)).save(directory/f'face-{view}.png')
sheet = Image.new('RGB',(1200,1420),'#f1f0f4')
draw = ImageDraw.Draw(sheet)
draw.text((16,14),f"{data['candidate']} | TECHNICAL PASS | EXECUTOR VISUAL FAIL",fill='#302f40',font=font)
draw.text((16,40),'One neutral model / frozen registration. 3Q and Top are derived. Human Gate not review ready.',fill='#302f40',font=small)
for row,view in enumerate(('front','side')):
    for col,(label,im) in enumerate(((f'LOCKED Skin {view}',locked[view]),
                                     (data['candidate'],current[view]),('50% overlay',overlays[view]))):
        draw.text((col*400+10,80+row*425),label,fill='#302f40',font=font)
        sheet.paste(im.crop((20,190,620,570)).resize((390,247)),(col*400+5,140+row*425))
for col,view in enumerate(('3q','top')):
    draw.text((col*600+16,960),'Derived '+view.upper(),fill='#302f40',font=font)
    im=e.background(Image.open(directory/f'diagnostic-{view}.png'))
    im.thumbnail((560,420))
    sheet.paste(im,(col*600+20,990))
sheet.save(directory/'diagnostic-sheet.png')
print(directory/'diagnostic-sheet.png')
