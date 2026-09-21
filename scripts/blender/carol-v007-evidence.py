"""Deterministic reference registration/contact sheets. No authority edits.

python scripts/blender/carol-v007-evidence.py skin|skin-stress|normal|final
Registration uses ground, eye spacing and support separation; never canvas size.
"""
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'tmp-carol-v007'
FINAL=ROOT/'docs/production/carol/evidence/reconstruction-v007'
REF=ROOT/'assets/grimo/source/carol/approved-3d'
MODE=sys.argv[1]
# Pixel observations are recorded explicitly, not treated as locked numbers.
# Front H/centerline are locked; skin H is inferred from 0.324 eye spacing;
# side H is crown-to-ground, skin-side H from 0.530 support separation.
REG={
    'normal-front':dict(h=1011,ground=1162,origin=626.5,view='front',basis='contract H=1011; centerline=626.5'),
    'normal-side':dict(h=916,ground=998,origin=144,view='side',basis='crown apex 82; ground 998; nose x144'),
    'skin-front':dict(h=994,ground=1075,origin=626.5,view='front',basis='eye-center separation ~322 / 0.324; ground 1075'),
    'skin-side':dict(h=1019,ground=1037,origin=64,view='side',basis='near-hoof footprint centers x461 and x1001 at row1030; 540 / 0.530; origin=461-0.390*1019'),
}
def bg(im):
    im=im.convert('RGBA')
    base=Image.new('RGBA',im.size,'#f1f0f4'); base.alpha_composite(im)
    return base.convert('RGB')
def registered(key,size):
    r=REG[key]
    im=Image.open(REF/('carol_'+('skin_' if key.startswith('skin') else '')+r['view']+'.png')).convert('RGBA')
    # Screen span=1.52H; center world height=.5; side center X=.65.
    scale=size/1.52/r['h']
    ox=size/2-r['origin']*scale
    if r['view']=='side': ox-=.65*size/1.52
    oy=size/2+.5*size/1.52-r['ground']*scale
    return im.transform((size,size),Image.Transform.AFFINE,(1/scale,0,-ox/scale,0,1/scale,-oy/scale),resample=Image.Resampling.BICUBIC)
def tile(im,label,size=430):
    out=Image.new('RGB',(size,size+36),'#ececf2')
    out.paste(bg(im).resize((size,size)),(0,36))
    ImageDraw.Draw(out).text((12,10),label,fill='#242137')
    return out
def sheet(items,path,cols=2,size=430):
    rows=(len(items)+cols-1)//cols
    out=Image.new('RGB',(cols*size,rows*(size+36)),'white')
    for i,(label,im) in enumerate(items):out.paste(tile(im,label,size),((i%cols)*size,(i//cols)*(size+36)))
    out.save(path)
if MODE in ['skin','normal']:
    items=[]
    for view in ['front','side']:
        key=MODE+'-'+view
        im=Image.open(TMP/(key+'.png'))
        items += [(key+' LOCKED reference',registered(key,im.width)),(key+' same model',im)]
    sheet(items,TMP/(MODE+'-sheet.png'))
elif MODE=='skin-stress':
    names=['neutral','yaw','yaw-R','pitch','lean-L','lean-R','ears','COM','forehoof','tail']
    sheet([(name,Image.open(TMP/('skin-test-'+name+'.png'))) for name in names],TMP/'skin-stress-sheet.png',5,320)
elif MODE=='final':
    items=[]
    for key in REG:
        im=Image.open(FINAL/(key+'.png'))
        reference=registered(key,im.width)
        overlay=Image.blend(bg(reference),bg(im),.5)
        overlay.save(FINAL/(key+'-overlay.png'))
        pair=Image.new('RGB',(im.width*2,im.height),'white')
        pair.paste(bg(reference));pair.paste(bg(im),(im.width,0))
        items.append((key+' : reference | model',pair))
    # Four authority pairs in a 2x2 sheet, preserving each square projection.
    out=Image.new('RGB',(1600,2*436),'white')
    d=ImageDraw.Draw(out)
    for i,(label,im) in enumerate(items):
        x=(i%2)*800; y=(i//2)*436
        d.text((x+12,y+8),label,fill='black')
        out.paste(im.resize((800,400)),(x,y+36))
    out.save(FINAL/'final-four-view-sheet.png')
    names=['neutral','yaw','lean-L','lean-R','ears','COM','forehoof','compress','peek','tail']
    sheet([(name,Image.open(TMP/('motion-'+name+'.png'))) for name in names],FINAL/'motion-readiness-sheet.png',5,384)
    sheet([(name,Image.open(FINAL/('derived-'+name+'.png'))) for name in ['3q-left','3q-right','back','top']],TMP/'derived-sheet.png',2,430)
    data=json.loads((FINAL/'measurements.json').read_text())
    data['reference_registration']=REG
    (FINAL/'measurements.json').write_text(json.dumps(data,indent=2)+'\n')
