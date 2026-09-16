"""Register approved plates once; compose evidence without synthesizing artwork."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/hero-geometry-v005'
SRC=ROOT/'assets/grimo/source/carol'
OUT.mkdir(parents=True,exist_ok=True)
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
def board(items,path,cols=3,cell=(500,460)):
    w,h=cell; result=Image.new('RGB',(cols*w,((len(items)+cols-1)//cols)*h),(235,238,244))
    draw=ImageDraw.Draw(result)
    for i,(label,p) in enumerate(items):
        im=Image.open(p).convert('RGBA') if not isinstance(p,Image.Image) else p.convert('RGBA')
        im.thumbnail((w-24,h-58),Image.Resampling.LANCZOS)
        x,y=(i%cols)*w,(i//cols)*h
        result.paste(im,(x+(w-im.width)//2,y+46+(h-58-im.height)//2),im)
        draw.text((x+12,y+12),label,font=FONT,fill=(35,45,65))
    result.save(path)
def main():
    sheet=SRC/'approved-3d/carol-3d-production-canonical-sheet.png'
    im=Image.open(sheet)
    old=OUT.parent/'blockout-v004'
    items=[('A Identity veto',SRC/'carol-Identity-canonical.png')]
    items += [(label,SRC/f'approved-3d/carol-{view}-transparent.png') for label,view in [('B Front','front-ortho'),('C Side','side-ortho'),('D Back','back-ortho'),('E Top / front at top','top-plan')]]
    items += [('F Approved 3/4',im.crop((380,60,1040,540))),('G Part closeups',im.crop((0,800,785,1060))),('H Historical / paint, not shape',old/'historical-benchmark-neutral-front.png'),('I v004 rejected side',old/'carol-v004-side.png')]
    board(items,OUT/'01-reference-board.png')
    data={'version':5,'units':'Blender units; proposed height 3.0, not physical meters','axis':{'front':'-Y','up':'+Z','image_right_front':'+X'},'registration_locked':True,'registration_note':'Uniform scale per source; no anisotropic warping, no per-iteration refit. Illustrated plates are not mutually exact orthographic projections. Residuals must remain visible.',
      'plates':{
       'front':{'file':'carol-front-ortho-transparent.png','pixels_per_unit':325,'origin_px':[645,1110],'mapping':'X=(u-645)/325; Z=(1110-v)/325','width_px':1280,'height_px':1280},
       'side':{'file':'carol-side-ortho-transparent.png','pixels_per_unit':295,'origin_px':[700,995],'mapping':'Y=(u-700)/295; Z=(995-v)/295','width_px':1456,'height_px':1088},
       'back':{'file':'carol-back-ortho-transparent.png','pixels_per_unit':325,'origin_px':[635,1110],'mapping':'X=-(u-635)/325; Z=(1110-v)/325','width_px':1280,'height_px':1280},
       'top':{'file':'carol-top-plan-transparent.png','pixels_per_unit':280,'origin_px':[630,630],'mapping':'X=(u-630)/280; Y=(v-630)/280','width_px':1280,'height_px':1280}},
      'front_landmarks_px':{'crown':[630,140],'face_center':[654,746],'face_left':[407,739],'face_right':[926,743],'chin':[651,899],'eye_L':[503,737],'eye_R':[814,737],'eye_tilt_degrees':[-8,8],'nose':[653,745],'mouth':[655,797],'ear_root_L':[362,679],'ear_root_R':[966,682],'ear_tip_L':[126,751],'ear_tip_R':[1175,751],'inner_ear_L':[242,767],'inner_ear_R':[1068,767],'hoof_L':[454,1106],'hoof_R':[789,1106],'moon':[356,458],'stars':[[624,296],[706,477],[194,621],[312,922],[646,963]]},
      'proposed_landmarks_3d':{'crown':[0,-.75,3.0],'body_center':[0,.15,1.4],'face_center':[.025,-1.90,1.12],'face_dimensions':[1.66,.46,1.12],'eye_L':[-.437,-2.025,1.148],'eye_R':[.520,-2.025,1.148],'nose':[.025,-2.12,1.12],'mouth':[.03,-2.1,.965],'ear_root_L':[-.87,-1.02,1.36],'ear_root_R':[.98,-1.0,1.35],'ear_tip_L':[-1.60,-1.03,1.10],'ear_tip_R':[1.63,-.99,1.11],'hoof_FL':[-.59,-1.12,0],'hoof_FR':[.59,-1.12,0],'hoof_RL':[-.59,1.12,0],'hoof_RR':[.59,1.12,0],'tuft':[0,1.94,1.49]},
      'uncertainties':['Top plan scale reconciles depth but ear width differs from front.','Moon is one physical left-flank ornament; all three face-on depictions cannot be matched by one planar crescent.','Star correspondence between plates is not uniquely specified; placement proposal requires Human review.','Hidden dimensions and camera orthogonality are inferred, not measured ground truth.']}
    for v,p in data['plates'].items():
        actual=Image.open(SRC/'approved-3d'/p['file']); p['width_px'],p['height_px']=actual.size
    data['protected_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*SRC.rglob('*.png'),ROOT/'assets/grimo/production/carol/blender/carol-blockout-v004.blend']}
    (OUT/'landmark-measurements.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
if __name__=='__main__': main()
