"""Measure approved raster references and compose unwarped Blender evidence.

Python with Pillow/NumPy/SciPy. --measure writes reconstruction measurements
and an eye pigment atlas sampled from the approved Normal Front.
"""
import sys, json, hashlib, tempfile, math, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT=Path(__file__).resolve().parents[2]
REF=ROOT/'assets/grimo/source/carol/approved-3d'
OUT=ROOT/'docs/production/carol/evidence/face-ear-authority-match-v001'
TMP=Path(tempfile.gettempdir())/'carol-authority-match-v001'
OUT.mkdir(parents=True,exist_ok=True); TMP.mkdir(exist_ok=True)
def measure():
    a=np.array(Image.open(REF/'modules/carol-ear-module-authority.png').convert('RGB')).astype(float)
    mask=(a[:,:,0]>a[:,:,1]*1.2)&(a[:,:,0]>a[:,:,2]*1.25)&(a[:,:,0]>75)
    pink=(a[:,:,0]>155)&(a[:,:,2]>a[:,:,1]*.71)&(a[:,:,0]-a[:,:,2]>50)&mask
    # Shared horizontal axis of the authority's Front and Top panels.
    # Root -> distal. Pixel extents are directly measured, not prior geometry.
    stations=[]
    for x in [604,598,586,570,545,510,470,425,380,335,290,245,200,160,125,95,75,62,56]:
        f=np.where(mask[:560,x])[0]; t=np.where(mask[620:1100,x])[0]+620
        p=np.where(pink[:560,x])[0]
        runs=np.split(p,np.where(np.diff(p)>1)[0]+1)
        p=max(runs,key=len) if len(p) else p
        if len(p)<8:p=np.array([])
        if not len(f) or not len(t):continue
        stations.append(dict(pixel_x=x,u=(607-x)*.400/553,
            top=(157-f.min())*.400/553,bottom=(157-f.max())*.400/553,
            front=(t.max()-850)*.400/553,back=(850-t.min())*.400/553,
            pink_top=(157-p.min())*.400/553 if len(p) else None,
            pink_bottom=(157-p.max())*.400/553 if len(p) else None))
    data={'units':'H = total Normal height; module scale derived from attached ear span',
       'source_commit':'656d6510b6ca81205cca1fced46d176f10d7aca7',
       'registration':{
           'normal_front':{'ppH':1011,'origin':646,'ground':1162,'note':'face-local center; global body center stays 626.5'},
           'normal_side':{'ppH':916,'origin':144,'ground':998},
           'skin_front':{'ppH':994,'origin':626.5,'ground':1075},
           'skin_side':{'ppH':1160,'origin':82,'ground':945,'note':'face-local similarity; nose/eye/chin registration, not whole-body fit'}},
       'landmarks_px':{
           'normal_front':{'eye_left':[488,750],'eye_right':[814,750],'nose':[645,777],'mouth':[645,803],'chin':[642,933],'eye_box':[419,674,558,825]},
           'normal_side':{'nose':[154,646],'eye':[281,615],'chin':[266,773],'forehead_break':[174,610],'eye_box':[221,535,342,693]},
           'skin_front':{'eye_left':[464,660],'eye_right':[784,660],'nose':[624,686],'chin':[624,848],'crown':[626,381],'cheek_left':[328,731]},
           'skin_side':{'nose':[92,506],'eye':[244,476],'chin':[299,678],'crown':[438,183],'forehead_break':[118,467],'eye_box':[169,378,320,571]}},
       'ear_stations':stations,
       'ear_registration':{'length_H':.400,'root_px_front':[607,157],'root_px_top':[607,850],'pixels_per_H':1382.5},
       'limitations':['Illustrated views are not calibrated orthographic photographs.',
           'Normal Front face is about 20 px right of the global centerline; symmetrized face reconstruction.',
           'Skin Side cranium and eye scale cannot both exactly agree with Skin Front under one similarity transform. Normal visible face and locked eye size have priority.'],
       'authority_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in list(REF.glob('*.png'))+[REF/'modules/carol-ear-module-authority.png',REF.parent/'carol-Identity-canonical.png']}}
    (OUT/'measurements.json').write_text(json.dumps(data,indent=2)+'\n')
    # Optical pigment only: source right eye inside its boundary. UV texture is
    # carried by a curved orbital surface; evidence renders are never retouched.
    src=Image.open(REF/'carol_front.png').convert('RGB')
    tex=src.transform((768,768),Image.Transform.EXTENT,(748,686,878,824),Image.Resampling.BICUBIC)
    tex.save(TMP/'eye-authority-pigment.png')
    print(json.dumps(stations,indent=2))
BG=(248,247,244)
def text(im,xy,s,size=22,color=(47,44,43)):
    ImageDraw.Draw(im).text(xy,s,font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',size),fill=color)
def canvas(size,title,subtitle):
    im=Image.new('RGB',size,BG);text(im,(24,16),title,31);text(im,(24,62),subtitle,19);return im
def opaque(im):
    bg=Image.new('RGBA',im.size,(*BG,255));bg.alpha_composite(im.convert('RGBA'));return bg.convert('RGB')
def panel(im,label,pic,x,y,w,h):
    text(im,(x+14,y),label,21)
    pic=pic.convert('RGBA');pic.thumbnail((w-24,h-40),Image.Resampling.LANCZOS)
    im.paste(pic,(x+(w-pic.width)//2,y+36+(h-40-pic.height)//2),pic)
def read(name):return Image.open(TMP/(name+'.png')).convert('RGBA')
def tight(im):
    box=im.getchannel('A').getbbox();im=im.crop(box)
    pad=max(8,int(max(im.size)*.045));return ImageOps.expand(im,border=pad,fill=(0,0,0,0))
def save(im,name):im.save(OUT/(name+'.png'))
def registered(key):
    data=json.loads((OUT/'measurements.json').read_text());r=data['registration'][key];h=r['ppH'];g=r['ground'];o=r['origin']
    filename={'normal_front':'carol_front.png','normal_side':'carol_side.png','skin_front':'carol_skin_front.png','skin_side':'carol_skin_side.png'}[key]
    box=(o-.32*h,g-.777*h,o+.32*h,g-.137*h) if 'front' in key else (o-.035*h,g-.777*h,o+.605*h,g-.137*h)
    return Image.open(REF/filename).convert('RGBA').transform((900,900),Image.Transform.EXTENT,box,Image.Resampling.BICUBIC)
def face_sheets():
    for view in ['front','side']:
        im=canvas((1800,1170),'CAROL / '+view.upper()+' / Face authority matching','Reference registration is fixed. Source and candidate use identical orthographic cameras, scale and lighting.')
        for i,(label,pic) in enumerate([('Normal authority',registered('normal_'+view)),('Skin authority',registered('skin_'+view)),('Source / 656d651',read('source-face-'+view)),('Candidate / authority-match-v001',read('candidate-face-'+view))]):
            panel(im,label,pic,i*450,110,450,475)
        for i,(key,prefix) in enumerate([('normal_'+view,'source'),('normal_'+view,'candidate'),('skin_'+view,'source'),('skin_'+view,'candidate')]):
            a=opaque(registered(key));b=opaque(read(prefix+'-face-'+view));ov=Image.blend(a,b,.45)
            panel(im,key.replace('_',' ')+' / '+prefix+' overlay',ov,i*450,620,450,470)
        text(im,(24,1104),'Normal includes occluding fleece; the candidate shows the same complete head without fleece. Skin registration is face-local.',19)
        text(im,(24,1135),'No per-view deformation, image warping of renders, authority regeneration, or Human acceptance is implied.',19)
        save(im,'face-'+view+'-comparison')
    im=canvas((1800,1170),'CAROL / Spatial consistency','One neutral head and one pair of ears. Derived views test volume; they are not new image authorities.')
    for row,prefix in enumerate(['source','candidate']):
        for i,v in enumerate(['front','3q','side','top']):panel(im,prefix.upper()+' / '+v,read(prefix+'-face-'+v),i*450,110+row*505,450,475)
    text(im,(24,1140),'The original torso is visible below the jaw for attachment context; torso, limbs, hooves and tail have not been redesigned.',18)
    save(im,'face-spatial-review')
def ear_sheets():
    ref=Image.open(REF/'modules/carol-ear-module-authority.png').convert('RGBA')
    boxes=[(30,70,630,545),(865,35,1145,555),(30,685,630,1005),(715,640,1250,1110)]
    views=['front','side','top','3q'];refs=[ref.crop(b) for b in boxes];refs[3]=ImageOps.mirror(refs[3])
    im=canvas((1800,1530),'CAROL / Ear / Front, Side, Top, 3Q','Measured Front + Top sections; rounded shell and contained inner ear. Uniform display fit only; no silhouette stretching.')
    for i,v in enumerate(views):
        panel(im,'AUTHORITY / '+v,refs[i],i*450,110,450,440)
        for row,prefix in enumerate(['source','candidate']):panel(im,prefix.upper()+' / '+v,tight(read(prefix+'-ear-'+v)),i*450,580+row*430,450,405)
    text(im,(24,1464),'Side above is a strict local orthographic diagnostic. The illustrated module has an unspecified elevated camera.',19)
    text(im,(24,1495),'3Q authority mirrored for handedness only. Attached Front / Side below use common absolute world cameras.',19)
    save(im,'ear-four-view-comparison')
    im=canvas((1500,770),'CAROL / Ear Side / Camera interpretation','Same neutral mesh: distal-side camera, elevation 14.7 deg, roll 11 deg; mirrored for reference handedness.')
    panel(im,'AUTHORITY / Side',refs[1],0,115,500,570)
    for i,prefix in enumerate(['source','candidate']):
        p=TMP/(prefix+'-ear-side-elevated.png')
        if p.exists():panel(im,prefix.upper()+' / elevated Side',tight(ImageOps.mirror(read(prefix+'-ear-side-elevated'))),500+i*500,115,500,570)
    text(im,(24,720),'This camera interpretation is qualitative. Strict orthographic Side remains visible in ear-four-view-comparison.png.',19)
    save(im,'ear-side-camera-diagnostic')
def attached():
    im=canvas((1800,1250),'CAROL / Attached face and ears','Source and candidate use the same body and the same absolute cameras. Fleece is not part of this candidate.')
    for row,prefix in enumerate(['source','candidate']):
        for i,v in enumerate(['front','side','3q']):panel(im,prefix.upper()+' / '+v,read(prefix+'-attached-'+v),i*600,110+row*535,600,505)
    text(im,(24,1200),'Only face, eyes, nose, mouth, head transition and ears changed. Identity / naturalness acceptance remains with Human.',20)
    save(im,'attached-three-view')
def metrics():
    data=json.loads((OUT/'measurements.json').read_text());result={}
    # Traced visible skin boundary samples. Coordinates are image pixels,
    # These fitting diagnostics are not an independent or held-out benchmark.
    front=[(440,428,819),(480,390,860),(530,365,891),(600,346,907),(660,334,916),(720,328,921),(760,337,911),(800,370,878),(825,434,816)]
    side=[(132,410),(122,444),(118,467),(102,480),(87,526),(94,560),(109,589),(133,616),(161,638),(201,659),(251,675)]
    normal=[(185,546),(179,576),(174,610),(157,627),(149,661),(154,690),(170,718),(196,745),(226,764)]
    data['traced_contours_px']={'skin_front':[list(x) for x in front],'skin_side':[list(x) for x in side],'normal_side':[list(x) for x in normal]}
    data['contour_measurement_note']='Selected visible fitting contours; manual annotation uncertainty approximately +/- 3 px. Not whole-image similarity, held-out validation, or Human perceptual acceptance.'
    (OUT/'measurements.json').write_text(json.dumps(data,indent=2)+'\n')
    for prefix in ['source','candidate']:
        p=TMP/(prefix+'-geometry.json')
        if not p.exists():continue
        geo=json.loads(p.read_text());s=np.array(geo['head_sections']);res={}
        for key,pts in [('skin_front',front),('skin_side',side),('normal_side',normal)]:
            r=data['registration'][key];h=r['ppH'];g=r['ground'];o=r['origin'];errors=[]
            for pt in pts:
                if key=='skin_front':
                    py,l,rr=pt;z=(g-py)/h
                    pred_l=o+np.interp(z,s[:,0],s[:,2])*h;pred_r=o+np.interp(z,s[:,0],s[:,3])*h
                    errors.extend([pred_l-l,pred_r-rr])
                else:
                    px,py=pt;z=(g-py)/h;pred=o+np.interp(z,s[:,0],s[:,1])*h;errors.append(pred-px)
            res[key]={'contour_mean_absolute_error_px':float(np.mean(np.abs(errors))),'contour_rmse_px':float(np.sqrt(np.mean(np.array(errors)**2))),'sample_count':len(errors)}
        res['features']=geo['features'];result[prefix]=res
    from scipy import ndimage as ndi
    a=np.array(Image.open(REF/'modules/carol-ear-module-authority.png').convert('RGB')).astype(float)
    mask=(a[:,:,0]>a[:,:,1]*1.2)&(a[:,:,0]>a[:,:,2]*1.25)&(a[:,:,0]>75)
    earboard=canvas((1600,1030),'CAROL / Ear contours / fixed registration','Cyan: authority contour. Magenta: 3D contour. No per-candidate translation, scale fitting, or deformation.')
    for row,view in enumerate(['front','top']):
        mm=mask.copy();mm[:,654:]=False
        if view=='front':mm[581:]=False
        else:mm[:581]=False
        scale=.48/850*1382.5
        affine=(scale,0,607-.2*1382.5-425*scale,0,scale,(157+.104*1382.5 if view=='front' else 850)-425*scale)
        auth=np.array(Image.fromarray((mm*255).astype('uint8')).transform((850,850),Image.Transform.AFFINE,affine,Image.Resampling.NEAREST))>127
        arim=auth^ndi.binary_erosion(auth)
        for col,prefix in enumerate(['source','candidate']):
            pred=np.array(read(prefix+'-ear-'+view))[:,:,3]>127;rim=pred^ndi.binary_erosion(pred)
            iou=float((auth&pred).sum()/(auth|pred).sum())
            error=float((ndi.distance_transform_edt(~arim)[rim].mean()+ndi.distance_transform_edt(~rim)[arim].mean())/2)
            result.setdefault(prefix,{})['ear_'+view]={'silhouette_IoU':iou,'symmetric_contour_distance_H':error*.48/850,'fixed_registration':True}
            pic=np.full((850,850,3),248,np.uint8);pic[auth]=(230,238,238);pic[pred]=(237,228,234)
            pic[ndi.binary_dilation(arim,iterations=2)]=(0,160,180);pic[ndi.binary_dilation(rim,iterations=2)]=(215,45,120)
            panel(earboard,prefix.upper()+' / '+view+' / IoU '+format(iou,'.3f'),Image.fromarray(pic),col*800,105+row*440,800,420)
    text(earboard,(24,993),'Intrinsic module frames aligned at the authored roots; attached absolute-world evidence separately tests size and placement.',18)
    save(earboard,'ear-contour-overlay')
    (OUT/'fit-metrics.json').write_text(json.dumps(result,indent=2)+'\n');return result
def review():
    im=canvas((1800,1160),'CAROL / Face + Ear / Human review','Authority-match-v001 | Actual Blender renders | Face and ear candidate only | Perceptual approval pending')
    for i,v in enumerate(['front','3q','side']):panel(im,'CANDIDATE / '+v,read('candidate-face-'+v),i*600,110,600,545)
    for i,v in enumerate(['front','side','top','3q']):panel(im,'EAR / '+v,read('candidate-ear-'+v),i*450,700,450,365)
    text(im,(24,1090),'Review face-front-comparison.png and face-side-comparison.png for fixed reference overlays and before / after.',19)
    text(im,(24,1122),'Ear four-view / attached three-view evidence exposes the remaining projection, root and shading differences.',19)
    save(im,'human-review')

def measurement_sheet():
    data=json.loads((OUT/'measurements.json').read_text())
    im=canvas((1800,850),'CAROL / Authority measurements','Fixed face-local similarity registrations. Dots: feature centers. Cyan: traced visible contour samples.')
    for col,key in enumerate(['normal_front','normal_side','skin_front','skin_side']):
        pic=registered(key);draw=ImageDraw.Draw(pic);r=data['registration'][key];h=r['ppH'];o=r['origin'];g=r['ground']
        left=o-.32*h if 'front' in key else o-.035*h;top=g-.777*h
        def point(px,py,color,radius=8):
            xx=(px-left)/(.64*h)*900;yy=(py-top)/(.64*h)*900
            draw.ellipse((xx-radius,yy-radius,xx+radius,yy+radius),fill=color,outline='white',width=2)
        for name,coords in data['landmarks_px'][key].items():
            if len(coords)==2:point(*coords,(215,50,130),9)
        for p in data.get('traced_contours_px',{}).get(key,[]):
            if key=='skin_front':point(p[1],p[0],(0,165,180));point(p[2],p[0],(0,165,180))
            else:point(*p,(0,165,180))
        panel(im,key.replace('_',' ').upper(),pic,col*450,110,450,475)
        text(im,(col*450+24,600),'px/H: '+str(h)+' | origin: '+str(o),18)
        text(im,(col*450+24,631),'ground row: '+str(g),18)
    text(im,(24,695),'Locked eye aperture: 0.137 H x 0.149 H | spacing: 0.324 H | reconstructed center Z: 0.412 H',23)
    text(im,(24,734),'Nose width: 0.039 H | center Z: 0.378 H | mouth centerline width: 0.091 H | ear local extent: 0.413 H',23)
    text(im,(24,790),'Measurements and all ear stations: measurements.json. Selected contours are fitting diagnostics; manual uncertainty about +/- 3 px.',19)
    save(im,'authority-measurements')
def compose():
    face_sheets();ear_sheets();attached();review();m=metrics()
    measurement_sheet()
    raw=OUT/'renders';raw.mkdir(exist_ok=True)
    for p in TMP.glob('candidate-*.png'):shutil.copy2(p,raw/p.name)
    validation=json.loads((OUT/'validation.json').read_text());validation['fit_metrics']=m
    validation['evidence']={}
    for p in sorted(OUT.rglob('*.png')):
        with Image.open(p) as im:im.load();size=list(im.size)
        validation['evidence'][str(p.relative_to(OUT)).replace('\\','/')]={'size':size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'decoded':True}
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps(m,indent=2))
if __name__=='__main__':
    if '--compose' in sys.argv:compose()
    else:measure()
