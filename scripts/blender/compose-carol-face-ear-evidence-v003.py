"""Compose bounded Human review evidence from real Blender PNGs; no shape warps.

Candidate/source use identical cameras and cell scales. Authority crops are
qualitative except explicitly labelled fixed-registration Normal Side overlays.
"""
import hashlib
import json
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/face-ear-production-v003'
TMP=Path(tempfile.gettempdir())/'carol-face-ear-v003'
REF=ROOT/'assets/grimo/source/carol/approved-3d'
BG=(248,247,244)
FONT='C:/Windows/Fonts/segoeui.ttf'

def text(im,xy,s,size=22,color=(45,41,39)):
    ImageDraw.Draw(im).text(xy,s,font=ImageFont.truetype(FONT,size),fill=color)

def canvas(size,title,subtitle):
    im=Image.new('RGB',size,BG);text(im,(24,15),title,30);text(im,(24,59),subtitle,19);return im

def read(name):return Image.open(TMP/(name+'.png')).convert('RGBA')

def opaque(im):
    bg=Image.new('RGBA',im.size,(*BG,255));bg.alpha_composite(im.convert('RGBA'));return bg.convert('RGB')

def place(im,pic,box):
    pic=pic.convert('RGBA');pic.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    im.paste(pic,(box[0]+(box[2]-box[0]-pic.width)//2,box[1]+(box[3]-box[1]-pic.height)//2),pic)

def panel(im,label,pic,x,y,w,h):
    text(im,(x+12,y),label,21);place(im,pic,(x+8,y+34,x+w-8,y+h))

def save(im,name):im.save(OUT/(name+'.png'))

def registered_reference(name):
    data=json.loads((TMP/'source.json').read_text())
    p=data['references']['REFERENCE '+name]['properties'];h=p['h'];x=p['origin'];g=p['ground']
    # Same world region as .66-H square face camera: x [-.05,.61], z [.14,.80].
    box=(x-.05*h,g-.80*h,x+.61*h,g-.14*h)
    return Image.open(REF/name).convert('RGBA').transform((720,720),Image.Transform.EXTENT,box,Image.Resampling.BICUBIC)

def face_sheets():
    im=canvas((1680,1080),'CAROL / Face Side decision','F2 selected for Human review. One local X-only correction; current eyes, jaw and cranium retained.')
    normal=Image.open(REF/'carol_side.png').crop((120,500,445,790))
    skin=Image.open(REF/'carol_skin_side.png').crop((65,340,460,700))
    for i,(label,pic) in enumerate([('AUTHORITY / Normal Side',normal),('AUTHORITY / Skin Side (qualitative)',skin),('SOURCE / exact v002 face',read('source-face-side')),('CANDIDATE / F2',read('F2-face-side'))]):
        panel(im,label,pic,i*420,100,420,410)
    reg=opaque(registered_reference('carol_side.png'))
    overlay_source=Image.blend(reg,opaque(read('source-face-side')),.45)
    overlay_candidate=Image.blend(reg,opaque(read('F2-face-side')),.45)
    for i,(label,pic) in enumerate([('Normal overlay / SOURCE',overlay_source),('Normal overlay / F2',overlay_candidate),('SOURCE / derived 3Q',read('source-face-3q')),('CANDIDATE / derived 3Q',read('F2-face-3q'))]):
        panel(im,label,pic,i*420,540,420,410)
    text(im,(24,973),'Overlays: inherited Normal Side h=916, ground=998, origin=144; fixed uniform projection, no candidate fitting.',20)
    text(im,(24,1004),'Nose moves forward 0.0124 H; control peak 0.020 H. Remaining depth deficit is visible. No Human identity/cuteness PASS.',20)
    text(im,(24,1035),'Skin Side is a qualitative source crop: its inherited registration is invalid for current face-landmark measurement.',19,(144,66,44))
    save(im,'face-side-review')
    im=canvas((1680,650),'CAROL / Front preservation','Purpose: detect collateral change. F2 does not change any control Y/Z, nose dimensions, eye or eyelid geometry.')
    front=Image.open(REF/'carol_front.png').crop((330,580,980,960))
    for i,(label,pic) in enumerate([('AUTHORITY / approved Front',front),('SOURCE',read('source-face-front')),('CANDIDATE / F2',read('F2-face-front')),('SOURCE / F2 50% overlay',Image.blend(opaque(read('source-face-front')),opaque(read('F2-face-front')),.5))]):
        panel(im,label,pic,i*420,105,420,450)
    text(im,(24,581),'Verified: EYE_L/R and EYELID_L/R geometry digests equal; nose/mouth/philtrum Y/Z delta = 0; 37 objects unchanged.',19)
    text(im,(24,612),'Same source/candidate framing and render settings. Reference crop is qualitative and uniformly displayed; no fitted overlap.',18)
    save(im,'face-front-preservation')
    im=canvas((1440,920),'CAROL / Skin Side registration diagnostic','PROBE_INVALID for authority matching: inherited Skin Side registration has a large face-landmark height mismatch.')
    reg=opaque(registered_reference('carol_skin_side.png'))
    for i,(prefix,label) in enumerate([('source','SOURCE / inherited registration'),('F2','CANDIDATE / same inherited registration')]):
        pic=Image.blend(reg,opaque(read(prefix+'-face-side')),.45)
        panel(im,label,pic,i*720,110,720,720)
    text(im,(24,859),'No registration, reference object or saved camera was changed. This mismatch is not evidence that the candidate failed.',20)
    save(im,'skin-registration-diagnostic')

def authority_ears():
    im=Image.open(REF/'modules/carol-ear-module-authority.png').convert('RGB');a=np.array(im).astype(float)
    gray=(a.max(2)-a.min(2)<12)&(a.mean(2)<235)&(a.mean(2)>170);w,h=im.size
    sx=int(w*.4)+int(np.argmax(gray.mean(0)[int(w*.4):int(w*.6)]));sy=int(h*.4)+int(np.argmax(gray.mean(1)[int(h*.4):int(h*.6)]))
    result=[]
    for j,box in enumerate([(0,0,sx,sy),(sx+1,0,w,sy),(0,sy+1,sx,h),(sx+1,sy+1,w,h)]):
        crop=im.crop(box).convert('RGBA');a=np.array(crop).astype(float)
        mask=(a[:,:,0]>a[:,:,1]*1.15)&(a[:,:,0]>a[:,:,2]*1.18)&(a[:,:,0]>70)
        b=Image.fromarray((mask*255).astype('uint8')).getbbox()
        crop=crop.crop((max(0,b[0]-12),max(0,b[1]-12),min(crop.width,b[2]+12),min(crop.height,b[3]+12)))
        result.append(ImageOps.mirror(crop) if j==3 else crop)
    return result

def ear_sheets():
    refs=authority_ears();views=['front','side','top','3q']
    im=canvas((1600,1000),'CAROL / Retained Ear v002 / Four views','Final candidate retains exact source ears. E1/E2 not promoted; Ear architecture review required.')
    for i,v in enumerate(views):
        panel(im,'AUTHORITY / '+v.upper(),refs[i],i*400,110,400,385)
        panel(im,'SOURCE = CANDIDATE / '+v.upper(),read('source-ear-'+v),i*400,525,400,385)
    text(im,(24,941),'Authority crops uniformly displayed; 3Q authority mirrored only for handedness. Candidate: one neutral EAR_L, fixed four cameras.',18)
    text(im,(24,969),'Remaining: Side wedge/plate read and weak cup containment. These known source limitations were not promoted as solved.',18)
    save(im,'ear-isolated-retained')
    im=canvas((1600,1490),'CAROL / Ear attempts / NOT PROMOTED','E1 then E2 only. Source ears retained in final blend. No E3 or cup-only third attempt.')
    for row,(prefix,title) in enumerate([('source','SOURCE v002'),('E1','E1 / REJECTED'),('E2','E2 / REJECTED')]):
        for i,v in enumerate(views):panel(im,title+' / '+v.upper(),read(prefix+'-ear-'+v),i*400,110+row*410,400,385)
    text(im,(24,1360),'E1: breadth shifts to middle, but excessive offset creates a wavy Top outline; Side remains heavy.',21)
    text(im,(24,1395),'E2: Side width reduces; Top develops a narrow distal transition instead of the authority\'s full, rounded tip.',21)
    text(im,(24,1430),'Unresolved tradeoff: Side flow vs broad-middle / rounded-tip Top and cup containment. STOP LOCAL REPAIR.',21,(144,66,44))
    save(im,'ear-attempts-not-promoted')
    im=canvas((1680,1030),'CAROL / Attached candidate / F2 + source ears','Saved candidate geometry. Existing non-final fleece below is a post-save occlusion diagnostic, not authority.')
    for i,v in enumerate(['front','side','3q']):panel(im,'CANDIDATE / '+v.upper(),read('candidate-attached-'+v),i*560,110,560,500)
    for i,v in enumerate(['front','side']):panel(im,'FLEECE DIAGNOSTIC / '+v.upper(),read('candidate-fleece-'+v),i*500,650,500,330)
    text(im,(1040,735),'Fleece remains outside candidate.',22)
    text(im,(1040,775),'Substantial ear occlusion persists.',22)
    text(im,(1040,815),'Root/clearance: future work unresolved.',22)
    text(im,(1040,855),'No fleece or ear redesign is claimed.',22)
    save(im,'candidate-attached')
    im=canvas((1600,650),'CAROL / Retained ear / Representative bend checks','Same camera / scale. Same closed shell and pink material region. Provisional controls only; no production rig.')
    for i,(v,title) in enumerate([('neutral','Neutral'),('lift','Lift +12 deg'),('droop','Droop -14 deg'),('attention','Attention +12 deg turn / +5 lift')]):
        panel(im,title,read('candidate-pose-'+v),i*400,115,400,440)
    text(im,(24,583),'Both ears: root-station motion 2.98e-8 H; no detected nonadjacent triangle intersections. Saved controls zero.',19)
    text(im,(24,614),'Volume ratios 0.9804 to 1.0153 relative to neutral. These checks do not constitute Human motion approval.',19)
    save(im,'ear-deformation-check')

def combined():
    im=canvas((1600,1370),'CAROL / Human review / F2 + source Ear v002','READY_FOR_HUMAN_FACE_EAR_REVIEW | Face executor: PASS (partial recovery) | Ear executor: FAIL / not promoted')
    for row,(p,title) in enumerate([('source','SOURCE'),('F2','CANDIDATE')]):
        for i,v in enumerate(['side','front','3q']):panel(im,title+' / '+v.upper(),read(p+'-face-'+v),i*533,105+row*390,533,375)
    for i,v in enumerate(['side','top','3q']):panel(im,'E2 REJECTED / '+v.upper(),read('E2-ear-'+v),i*380,915,380,270)
    text(im,(1170,935),'EAR V003 NOT PROMOTED',22,(144,66,44))
    for j,line in enumerate(['Final ears = exact source v002.','Side / Top tradeoff persists.','Cup read remains unresolved.','Next: Planner architecture review.']):text(im,(1170,982+j*32),line,19)
    text(im,(24,1224),'Human: 1 Side muzzle closer?  2 Front still Carol?  3 3Q still cute, non-canine?  4 Any facial regression?',21)
    text(im,(24,1260),'Ear review: 5 Side flow?  6 Broad middle / rounded taper?  7 Brown wraps pink?  E1/E2 did not resolve these together.',20)
    text(im,(24,1300),'Use face-side-review.png for authorities/overlays; ear-attempts-not-promoted.png for full four-view stop evidence.',19)
    text(im,(24,1334),'No Human Geometry, identity, cuteness or final-production approval. No authority promotion.',19,(144,66,44))
    save(im,'human-review')

def main():
    face_sheets();ear_sheets();combined()
    p=OUT/'validation.json';d=json.loads(p.read_text())
    evidence={}
    for file in sorted(OUT.glob('*.png')):
        with Image.open(file) as im:im.load();size=list(im.size)
        with Image.open(file) as im:im.verify()
        evidence[file.name]=dict(size=size,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),decoded=True)
    d['evidence']=evidence;p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print('EVIDENCE_DECODE_PASS',list(evidence))

if __name__=='__main__':main()
