"""Compact evidence for the retained, BLOCKED v009 Phase A candidate.

No fitting, generated references, or changes to source images. All registered
rows use one fixed crop per view, scaled uniformly for display only.
"""
import importlib.util
import json
import shutil
from pathlib import Path
import sys
sys.dont_write_bytecode=True
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/reconstruction-v009'
OLD=OUT.with_name('reconstruction-v008')
spec=importlib.util.spec_from_file_location('registered_evidence',Path(__file__).with_name('carol-v008-evidence.py'))
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
data=json.loads((OUT/'measurements.json').read_text())
assert data['static_visual_status']=='FAIL'
for name in ['skin-front.png','skin-side.png','diagnostic-3q.png']:
    shutil.copyfile(OUT/'phase-a-attempt-2'/name,OUT/name)

for attempt in (1,2):
    folder=OUT/f'phase-a-attempt-{attempt}'
    for view,crop in [('front',(160,210,480,455)),('side',(20,210,345,455))]:
        im=e.background(Image.open(folder/f'skin-{view}.png')).resize((640,640))
        im.crop(crop).save(folder/f'face-{view}.png')

current={v:e.background(Image.open(OUT/f'skin-{v}.png')).resize((640,640)) for v in ['front','side']}
locked={v:e.background(e.registered(data['reference_registration'][f'skin-{v}'],640)) for v in ['front','side']}
prior={v:e.background(Image.open(OLD/f'skin-{v}.png')).resize((640,640)) for v in ['front','side']}
overlays={v:Image.blend(locked[v],current[v],.5) for v in ['front','side']}
for view in ['front','side']:
    overlays[view].save(OUT/f'skin-{view}-overlay.png')

rows=[('Skin Front','front',(25,200,610,550)),('Skin Side','side',(25,200,610,550)),
      ('Face Front','front',(160,210,480,455)),('Face Side','side',(20,210,345,455)),
      ('Hooves Front - TEMP V008','front',(155,465,485,545)),
      ('Hooves Side - TEMP V008','side',(125,465,495,545))]
w,h=380,240
sheet=Image.new('RGB',(4*w,(len(rows)+2)*h+42),'#f1f0f4');draw=ImageDraw.Draw(sheet)
draw.text((12,12),'V009-A2 | BLOCKED AT PHASE A | NOT AN ACCEPTED STATIC CANDIDATE',fill='#9a2424')
for r,(title,view,crop) in enumerate(rows):
    for c,(label,im) in enumerate([('LOCKED',locked[view]),('v008 revision 17',prior[view]),
                                  ('v009-A2 / FAIL',current[view]),('50% overlay',overlays[view])]):
        x,y=c*w,42+r*h
        draw.text((x+8,y+8),title+' | '+label,fill='#242137')
        panel=im.crop(crop);panel.thumbnail((w-16,h-35),Image.Resampling.LANCZOS)
        sheet.paste(panel,(x+(w-panel.width)//2,y+32+(h-35-panel.height)//2))
    if r>=2:
        name=('face' if r<4 else 'hoof')+'-'+view+'.png'
        current[view].crop(crop).save(OUT/name)
for r,view in enumerate(['3q','top'],len(rows)):
    x,y=0,42+r*h
    draw.text((12,y+12),'DERIVED '+view.upper()+' | NO LOCKED REFERENCE',fill='#242137')
    draw.text((12,y+40),'Ear / hoof modules are unchanged temporary v008.',fill='#9a2424')
    for c,(label,path) in enumerate([('v008 revision 17',OLD/f'diagnostic-revision-17-{view}.png'),
                                     ('v009-A2 / FAIL',OUT/f'diagnostic-{view}.png')],1):
        draw.text((c*w+8,y+8),label,fill='#242137')
        im=e.background(Image.open(path)).resize((640,640)).crop((70,65,580,590))
        im.thumbnail((w-16,h-35),Image.Resampling.LANCZOS)
        sheet.paste(im,(c*w+(w-im.width)//2,y+30))
sheet.save(OUT/'human-comparison.png')
print(OUT/'human-comparison.png')
