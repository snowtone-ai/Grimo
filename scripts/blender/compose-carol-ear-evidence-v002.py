"""Assemble the four review PNGs from actual Blender renders (Pillow/NumPy).

No synthesized pixels or shape warps. Isolated views are uniformly fitted to
cells; deformation panels retain identical camera framing and scale.
"""
import hashlib
import json
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/ear-production-v002'
TMP=Path(tempfile.gettempdir())/'carol-ear-v002'
AUTH=ROOT/'assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.png'
BG=(248,247,244)
FONT=Path('C:/Windows/Fonts/segoeui.ttf')


def label(canvas,xy,text,size=22,color=(49,45,42)):
    font=ImageFont.truetype(str(FONT),size) if FONT.exists() else ImageFont.load_default()
    ImageDraw.Draw(canvas).text(xy,text,font=font,fill=color)


def place(canvas,im,box,crop=False,reference=False):
    im=im.convert('RGBA')
    if crop:
        if reference:
            a=np.asarray(im).astype(float)
            mask=(a[:,:,0]>a[:,:,1]*1.15)&(a[:,:,0]>a[:,:,2]*1.18)&(a[:,:,0]>70)
            bbox=Image.fromarray((mask*255).astype('uint8')).getbbox()
        else:bbox=im.getchannel('A').getbbox()
        if bbox:im=im.crop((max(0,bbox[0]-12),max(0,bbox[1]-12),min(im.width,bbox[2]+12),min(im.height,bbox[3]+12)))
    im.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    canvas.paste(im,(box[0]+(box[2]-box[0]-im.width)//2,box[1]+(box[3]-box[1]-im.height)//2),im)


def donor_summary():
    data=json.loads((TMP/'audit.json').read_text())
    canvas=Image.new('RGB',(1600,1060),BG)
    label(canvas,(24,14),'CAROL / Face-side donor audit / Ear quality excluded',28)
    label(canvas,(24,53),'Chosen: ear-production-v001 (same face as hero-modules-v003). HUMAN REVIEW REQUIRED.',21)
    refs=ROOT/'assets/grimo/source/carol/approved-3d'
    place(canvas,Image.open(refs/'carol_side.png').crop((120,390,540,800)),(20,110,305,355))
    place(canvas,Image.open(refs/'carol_front.png').crop((340,590,980,950)),(330,110,700,355))
    label(canvas,(20,85),'Approved Normal Side / face crop',17)
    label(canvas,(330,85),'Approved Normal Front / face crop',17)
    for j,t in enumerate([
        'Selection: smooth forehead-to-cheek / under-jaw transition;',
        'short nose, closed mouth and less protruding, seated eyes.',
        'No older donor clearly improved the combined side-face read.',
        'Limits: muzzle remains simplified; no donor is authority-matched.',
        'Ears / fleece hidden to expose head geometry. Current assets:',
        'identical orthographic cameras. Legacy a-v006: head-fit camera',
        'and added neutral light (source has no world / render lights).',
        'Exact short filenames probe-v001 / a-v006 absent; carol-prefixed',
        'counterparts were present and inspected. No source files edited.'
    ]):label(canvas,(750,100+j*27),t,18)
    notes=[
        ('Selected: rounded head, seated eyes.','Face geometry identical to modules-v003.'),
        ('Same face / nose / jaw as selected donor.','No distinct side-face advantage.'),
        ('Same muzzle / jaw; eyes protrude more.','Weaker eye-to-side-face integration.'),
        ('Same muzzle / jaw as modules-v002.','No recovered nose / muzzle advantage.'),
        ('More exposed eye bulge in Side.','No useful muzzle improvement.'),
        ('Nose forward; forehead / jaw boxier.','Larger eye does not offset planar head.'),
        ('v011 face family, same short muzzle.','Fleece omitted; eye remains bulbous.'),
        ('Sloping wedge forehead; open mouth.','Different eye proportions / identity.')
    ]
    for i,(name,note) in enumerate(zip(data,notes)):
        x=(i%4)*400;y=385+(i//4)*320
        label(canvas,(x+10,y),name.replace('carol-',''),19)
        for j,view in enumerate(['side','front']):
            place(canvas,Image.open(TMP/f'audit-{name}-{view}.png'),(x+j*200,y+30,x+j*200+200,y+235))
        for k,t in enumerate(note):label(canvas,(x+10,y+245+k*23),t,16)
    label(canvas,(24,1031),'Current-axis assets shown at shared scale; legacy only uniformly fit. Geometry choice is provisional, not perceptual approval.',17)
    canvas.save(OUT/'donor-audit-summary.png')


def main():
    donor_summary()
    authority=Image.open(AUTH).convert('RGB');a=np.asarray(authority).astype(float)
    gray=(a.max(2)-a.min(2)<12)&(a.mean(2)<235)&(a.mean(2)>170)
    w,h=authority.size
    sx=int(w*.4)+int(np.argmax(gray.mean(0)[int(w*.4):int(w*.6)]))
    sy=int(h*.4)+int(np.argmax(gray.mean(1)[int(h*.4):int(h*.6)]))
    crops=[(0,0,sx,sy),(sx+1,0,w,sy),(0,sy+1,sx,h),(sx+1,sy+1,w,h)]
    canvas=Image.new('RGB',(1520,940),BG)
    label(canvas,(28,18),'CAROL EAR / Current authority and one neutral 3D mesh',30)
    label(canvas,(28,60),'Same EAR_L in all four renders. Local orthographic axes; uniform panel fit only. HUMAN REVIEW REQUIRED.',19)
    for i,(view,crop) in enumerate(zip(['Front','Side','Top','3Q'],crops)):
        x=i*380
        label(canvas,(x+20,108),view,26)
        ref=authority.crop(crop)
        if view=='3Q':ref=ImageOps.mirror(ref)
        place(canvas,ref,(x+12,170,x+368,492),crop=True,reference=True)
        place(canvas,Image.open(TMP/('ear-'+view.lower()+'.png')),(x+12,554,x+368,890),crop=True)
        ImageDraw.Draw(canvas).line((x+6,518,x+374,518),fill=(212,208,201),width=1)
        label(canvas,(x+20,144),'AUTHORITY'+(' / mirrored presentation' if view=='3Q' else ''),17)
        label(canvas,(x+20,530),'CANDIDATE / neutral',17)
    label(canvas,(28,906),'3Q reference is mirrored only to align handedness; authority file is unchanged. No camera-dependent geometry.',17)
    canvas.save(OUT/'ear-isolated-comparison.png')
    for view in ['front','side']:
        canvas=Image.new('RGB',(1400,960),BG)
        label(canvas,(28,20),'CAROL / Attached ears / '+view.title(),30)
        label(canvas,(28,65),'Main image: saved candidate, unchanged audited v001 donor. Ear geometry only. HUMAN REVIEW REQUIRED.',19)
        place(canvas,Image.open(TMP/('attached-'+view+'.png')),(0,105,1050,950))
        label(canvas,(1040,170),'FLEECE DIAGNOSTIC',19)
        label(canvas,(1040,202),'Existing non-final donor',16)
        place(canvas,Image.open(TMP/('fleece-'+view+'.png')),(1030,240,1390,620))
        for j,t in enumerate(['Substantial occlusion remains.','Fleece is not in the output blend.','Head and fleece were not edited.']):
            label(canvas,(1040,662+j*28),t,16)
        canvas.save(OUT/('carol-ear-attached-'+view+'.png'))
    canvas=Image.new('RGB',(1600,570),BG)
    label(canvas,(24,18),'CAROL EAR / Independent provisional deformation controls',29)
    label(canvas,(24,60),'Fixed camera and scale; first three root stations remain fixed. The pink seat and outer shell deform together.',19)
    for i,(pose,text) in enumerate([('neutral','Neutral'),('lift','Lift / +12 deg'),('droop','Droop / -14 deg'),('attention','Attention / +12 deg turn')]):
        label(canvas,(i*400+20,110),text,22)
        place(canvas,Image.open(TMP/('pose-'+pose+'.png')),(i*400,148,i*400+400,540))
    label(canvas,(24,539),'Test shape keys are zero in the saved asset. These are bend checks, not an approved animation or a production rig.',17)
    canvas.save(OUT/'ear-deformation-check.png')
    path=OUT/'validation.json';data=json.loads(path.read_text())
    data['evidence']={'authority_panel_dividers_px':[sx,sy],'reference_3q_mirrored_for_handedness':True,
                     'images':{p.name:{'size':list(Image.open(p).size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.glob('*.png'))}}
    for p in OUT.glob('*.png'):
        with Image.open(p) as im:im.verify()
    path.write_text(json.dumps(data,indent=2)+'\n')
    print('Evidence decoded:',list(data['evidence']['images']))


if __name__=='__main__':main()
