"""Fixed-registration v011 evidence; no source fitting or generated references.

Run with Python + Pillow after rendering/finalization. An optional directory
argument composes a bounded attempt; default is the retained evidence folder.
"""
import importlib.util,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('evidence',ROOT/'scripts/blender/carol-v008-evidence.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
d=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'docs/production/carol/evidence/reconstruction-v011'
data=json.loads((d/'measurements.json').read_text())
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
current={v:e.background(Image.open(d/f'skin-{v}.png')).resize((640,640)) for v in ['front','side']}
locked={v:e.background(e.registered(data['reference_registration'][f'skin-{v}'],640)) for v in ['front','side']}
overlays={v:Image.blend(locked[v],current[v],.5) for v in ['front','side']}
for v in ['front','side']:
    overlays[v].save(d/f'skin-{v}-overlay.png')
    current[v].crop((160,210,480,455) if v=='front' else (20,210,345,455)).save(d/f'face-{v}.png')
sheet=Image.new('RGB',(1200,1420),'#f1f0f4');draw=ImageDraw.Draw(sheet)
status=data.get('executor_visual_precheck','NOT_RUN')
draw.text((16,14),f"{data['candidate']} | TECHNICAL {data['technical_static_gate']} | EXECUTOR VISUAL {status}",fill='#302f40',font=font)
draw.text((16,40),'One neutral model / frozen registration. 3Q and Top are diagnostics only. Human Gate not approved.',fill='#302f40',font=small)
for row,v in enumerate(['front','side']):
    for col,(label,im) in enumerate([('LOCKED Skin '+v,locked[v]),(data['candidate'],current[v]),('50% overlay',overlays[v])]):
        draw.text((col*400+10,80+row*425),label,fill='#302f40',font=font)
        panel=im.crop((20,190,620,570)).resize((390,247))
        sheet.paste(panel,(col*400+5,140+row*425))
for col,v in enumerate(['3q','top']):
    draw.text((col*600+16,960),'Derived '+v.upper(),fill='#302f40',font=font)
    im=e.background(Image.open(d/f'diagnostic-{v}.png'))
    im.thumbnail((560,420));sheet.paste(im,(col*600+20,990))
sheet.save(d/'diagnostic-sheet.png')
print(d/'diagnostic-sheet.png')
