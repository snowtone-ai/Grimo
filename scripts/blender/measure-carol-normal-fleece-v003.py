"""Small current-authority contract and equal-height raster diagnostics. No general CV."""
from pathlib import Path
import json, hashlib, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy.ndimage import binary_fill_holes, binary_closing, distance_transform_edt

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v003'
REF=ROOT/'assets/grimo/source/carol/approved-3d'
OUT.mkdir(parents=True,exist_ok=True)

def load(path,side=False):
    im=Image.open(path).convert('RGBA'); a=np.array(im)
    if a[:,:,3].min()<128: mask=a[:,:,3]>128
    else:
        rgb=a[:,:,:3].astype(float)
        ink=(rgb.min(2)<224)&((rgb.max(2)-rgb.min(2))>23)
        mask=binary_fill_holes(binary_closing(ink,iterations=3))
    ys,xs=np.where(mask); box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
    return im,mask,box

def normalized(path,mirror=False,height=600):
    im,mask,box=load(path); im=im.crop(box); mm=Image.fromarray((mask*255).astype('uint8')).crop(box)
    if mirror: im=ImageOps.mirror(im);mm=ImageOps.mirror(mm)
    size=(round(im.width*height/im.height),height)
    im=im.resize(size,Image.Resampling.LANCZOS);mm=mm.resize(size,Image.Resampling.NEAREST)
    canvas=Image.new('RGBA',(900,height),(255,255,255,0)); canvas.alpha_composite(im,((900-im.width)//2,0))
    m=np.zeros((height,900),bool);x=(900-mm.width)//2;m[:,x:x+mm.width]=np.array(mm)>128
    return canvas,m,box

def contract():
    result={'schema':'carol.v003.current-authority-contract','coordinate_system':'X rearward, Y character left, Z up; canonical height 1.0; ground 0',
      'method':'Current-image manual semantic landmarks plus alpha/closed-color-outline silhouette. No historical measurements. Gold ornaments excluded from pigment and fleece constraints.',
      'front_mapping':{'center_u':630,'ground_v':1161,'pixels_per_unit':1012},
      'side_mapping':{'face_tip_u':145,'ground_v':999,'pixels_per_unit':918},
      'landmarks_px':{
        'front':{'face_opening':[[477,600],[554,640],[646,635],[721,638],[816,610],[909,667],[936,789],[900,878],[813,922],[644,937],[490,921],[404,876],[379,789],[409,685]],
          'ear_left':[58,638,350,838],'ear_right':[963,638,1222,837],
          'hoof_left':[340,1052,555,1161],'hoof_right':[704,1050,915,1161],
          'chest_lower':[[181,969],[310,1080],[479,1070],[625,1110],[777,1075],[1011,1052],[1102,963]],
          'face_bright_roi':[580,826,718,868],'chin_roi':[560,882,726,916]},
        'side':{'crown_back':[[113,464],[157,351],[284,263],[411,183],[538,143],[650,80],[793,174],[949,276],[1075,405],[1170,509]],
          'face_exposure':[[188,506],[173,610],[143,643],[176,720],[265,773],[382,750]],
          'cheek':[[452,489],[521,573],[513,679],[463,755]],
          'ear':[513,509,770,722],'chest':[231,746,507,913],
          'belly':[[300,874],[461,916],[642,925],[756,917],[855,889],[1068,902],[1168,844]],
          'rump':[1100,490,1215,823],'tail':[1193,607,1289,727],
          'hooves':[[359,867,605,1000],[841,867,1074,1000]]}},
      'fleece_sections_z_halfwidth_xfront_xback':[
        [.075,.01,.42,.82],[.10,.30,.25,.99],[.14,.43,.15,1.09],
        [.20,.48,.105,1.13],[.28,.51,.12,1.145],[.38,.515,.14,1.14],
        [.48,.535,.085,1.11],[.58,.535,-.018,1.065],[.68,.48,.015,.98],
        [.78,.407,.11,.905],[.86,.335,.19,.82],[.93,.235,.32,.74],
        [.975,.115,.435,.645],[1.0,0,.55,.55]],
      'manual_landmark_uncertainty_px':5,'human_acceptance':'PENDING'}
    for view in ['front','side']:
        path=REF/f'carol_{view}.png';im,mask,box=load(path)
        h=box[3]-box[1]; w=box[2]-box[0]
        rows=[]
        for y in np.linspace(box[1],box[3]-1,65).astype(int):
            xs=np.where(mask[y])[0]
            if len(xs):rows.append([int(y),int(xs.min()),int(xs.max())])
        result[view]={'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                      'bbox_px':box,'width_over_height':w/h,'row_envelope_px':rows}
    (OUT/'authority-contract.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    # Pigment preparation is explicitly deferred until macro geometry is credible.
    if '--prepare-pigment' not in sys.argv:return result
    # Preclean projected pigment: nearby valid wool colors fill face/ear/gold areas.
    for view in ['front','side']:
        im,mask,box=load(REF/f'carol_{view}.png');a=np.array(im);rgb=a[:,:,:3].astype(float)
        reliable=mask&(rgb[:,:,2]>rgb[:,:,0]*.91)&(rgb[:,:,2]>rgb[:,:,1]*.98)&(rgb.mean(2)>135)
        for key in (['face_opening'] if view=='front' else ['face_exposure','cheek']):
            p=Image.new('L',im.size);ImageDraw.Draw(p).polygon([tuple(q) for q in result['landmarks_px'][view][key]],fill=255)
            reliable &= np.array(p)==0
        if view=='front': reliable[595:938,370:940]=False
        else: reliable[500:782,120:550]=False
        indices=distance_transform_edt(~reliable,return_distances=False,return_indices=True)
        out=rgb[indices[0],indices[1]].astype('uint8')
        Image.fromarray(out).save(OUT/f'pigment-{view}.png')
    return result

def diagnostics():
    report={'method':'600px equal outline height, aspect preserved, ground aligned and horizontally centered; Side mirrored for common orientation. Whole silhouette includes ears/hooves/tail and any protruding charms; ornament geometry is excluded from the macro-fitting contract. Distances normalized by character height. Diagnostics are not acceptance gates.','versions':{}}
    for version in ['v002','v003']:
        folder=OUT.with_name('normal-fleece-'+version); measurements={}
        for view in ['front','side']:
            path=folder/(view+'.png')
            if not path.exists():continue
            ai,a,_=normalized(REF/f'carol_{view}.png');ci,c,box=normalized(path,view=='side')
            edgea=a & ~binary_closing(~a,iterations=1)
            from scipy.ndimage import binary_erosion
            ea=a^binary_erosion(a);ec=c^binary_erosion(c)
            d=(distance_transform_edt(~ea)[ec].mean()+distance_transform_edt(~ec)[ea].mean())/1200
            measurements[view]={'silhouette_iou':float((a&c).sum()/(a|c).sum()),'symmetric_contour_distance_over_height':float(d),'width_over_height':(box[2]-box[0])/(box[3]-box[1])}
            if version=='v003':
                ov=np.full((*a.shape,3),255,np.uint8);ov[a]=[228,169,191];ov[c]=[145,197,232];ov[a&c]=[179,185,204]
                Image.fromarray(ov).save(OUT/f'overlay-{view}.png')
        report['versions'][version]=measurements
    (OUT/'geometry-measurements.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    semantic={'method':'600px equal-height Front. Fixed ear/hoof ROIs and brown-color threshold; brightness from fixed image-aligned cheek-free lower-face/chin rectangles. Shading proxies, not material-independent geometry or Human acceptance.','samples':{}}
    for label,path in [('authority',REF/'carol_front.png'),('v002',OUT.with_name('normal-fleece-v002')/'front.png'),('v003',OUT/'front.png')]:
        if not path.exists():continue
        im,mask,_=normalized(path);rgb=np.asarray(im)[:,:,:3].astype(float)
        luma=rgb@np.array([.2126,.7152,.0722])
        sample={}
        for name,box in [('ear_left',[95,275,287,430]),('hoof_left',[235,522,425,600])]:
            x0,y0,x1,y1=box;c=rgb[y0:y1,x0:x1];brown=(c[:,:,0]>c[:,:,1]*1.13)&(c[:,:,1]>c[:,:,2]*1.07)&(c[:,:,0]<227)&(c[:,:,1]<172)
            yy,xx=np.where(brown)
            if len(xx):sample[name]={'width_px':int(xx.max()-xx.min()+1),'height_px':int(yy.max()-yy.min()+1),'height_over_width':float((yy.max()-yy.min()+1)/(xx.max()-xx.min()+1))}
        sample['lower_face_luma']=float(luma[402:425,425:492].mean())
        sample['chin_luma']=float(luma[435:454,414:498].mean())
        sample['chin_minus_lower_face_luma']=sample['chin_luma']-sample['lower_face_luma']
        semantic['samples'][label]=sample
    (OUT/'semantic-measurements.json').write_text(json.dumps(semantic,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    contract();diagnostics()
