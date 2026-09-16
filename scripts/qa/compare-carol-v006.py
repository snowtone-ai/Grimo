"""Uniform silhouette registration and honest multi-view reconstruction metrics.

No stretching, artwork synthesis, camera-specific geometry or metric masking.
White-background 3Q segmentation is explicitly uncertain; original files remain
untouched. All metrics are supporting evidence, never a Human PASS.
"""
from pathlib import Path
import argparse, json, math
import numpy as np
from PIL import Image, ImageDraw
from carol_reference_mask import reference_mask

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/reconstruction-v006'
SRC=ROOT/'assets/grimo/source/carol/approved-3d'
VIEWS={'front':'front-ortho-transparent','side':'side-ortho-transparent','back':'back-ortho-transparent','top':'top-plan-transparent','3q-left':'front-3q-left','3q-right':'front-3q-right'}
SIZE=768; HEIGHT=640
ALIASES={'eye_L_center':'eye_center_L','eye_R_center':'eye_center_R','ear_L_root':'ear_root_L','ear_R_root':'ear_root_R','ear_L_tip':'ear_tip_L','ear_R_tip':'ear_tip_R','nose_center':'nose_center','mouth_corner_L':'mouth_corner_L','mouth_corner_R':'mouth_corner_R','hoof_FL_center':'hoof_front_L','hoof_FR_center':'hoof_front_R','hoof_RL_center':'hoof_rear_L','hoof_RR_center':'hoof_rear_R'}

def foreground(im,white=False):
    im=im.convert('RGBA');a=np.asarray(im).copy()
    if white:
        a[:,:,3]=np.where(reference_mask(im),255,0)
    mask=a[:,:,3]>127
    # Ignore isolated alpha specks without discarding any major character part.
    ys,xs=np.where(mask)
    if not len(xs):raise ValueError('empty foreground')
    bbox=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)
    return Image.fromarray(a),bbox

def register(im,white=False):
    im,b=foreground(im,white);crop=im.crop(b);scale=HEIGHT/crop.height
    w=max(1,round(crop.width*scale));h=HEIGHT
    result=Image.new('RGBA',(SIZE,SIZE));x=(SIZE-w)//2;y=(SIZE-h)//2
    if w>SIZE-8:
        # One common per-view display scale must be chosen from both images.
        pass
    result.alpha_composite(crop.resize((w,h),Image.Resampling.LANCZOS),(x,y))
    return result,{'source_bbox':list(b),'scale':scale,'offset':[x-b[0]*scale,y-b[1]*scale],'registered_bbox':[x,y,x+w,y+h]}

def register_pair(ref,mod,white=False):
    a,ba=foreground(ref,white);b,bb=foreground(mod)
    # Same bbox height, identical isotropic scale rule, no width matching.
    ratios=[(r[2]-r[0])/(r[3]-r[1]) for r in [ba,bb]]
    old=Image.open(OUT/'old-look-native.png') if (OUT/'old-look-native.png').exists() else None
    if old is not None:ratios.append(old.width/old.height)
    height=min(HEIGHT,int((SIZE-64)/max(ratios)))
    def one(im,box):
        crop=im.crop(box);s=height/crop.height;w=round(crop.width*s);x=(SIZE-w)//2;y=(SIZE-height)//2
        out=Image.new('RGBA',(SIZE,SIZE));out.alpha_composite(crop.resize((w,height),Image.Resampling.LANCZOS),(x,y))
        return out,{'source_bbox':list(box),'scale':s,'offset':[x-box[0]*s,y-box[1]*s],'registered_bbox':[x,y,x+w,y+height]}
    aa,ra=one(a,ba);bb,rb=one(b,bb)
    return aa,bb,ra,rb

def silhouette(im):return np.asarray(im)[:,:,3]>127

def width(mask):
    yy,xx=np.where(mask);box=[xx.min(),yy.min(),xx.max()+1,yy.max()+1];out=[]
    for s in np.linspace(0,1,101):
        y=min(box[3]-1,round(box[1]+s*(box[3]-box[1]-1)));xs=np.where(mask[y])[0]
        out.append(float(xs[-1]-xs[0]+1) if len(xs) else 0)
    return np.array(out),box

def compose_background(im):
    out=Image.new('RGBA',im.size,(239,240,246,255));out.alpha_composite(im);return out.convert('RGB')

def main():
    p=argparse.ArgumentParser();p.add_argument('--folder',required=True);p.add_argument('--publish',action='store_true');args=p.parse_args()
    folder=Path(args.folder);folder=folder if folder.is_absolute() else ROOT/folder
    data=json.loads((folder/'geometry-data.json').read_text(encoding='utf8'))
    measured=json.loads((ROOT/'docs/production/carol/carol-reference-measurements.json').read_text(encoding='utf8'))
    dest=OUT if args.publish else folder/'comparison';dest.mkdir(parents=True,exist_ok=True)
    report={'schema_version':1,'status':'NOT_ACCEPTED','human_gate':'PENDING','render_stage':'CLAY_GEOMETRY','lookdev_status':'HELD_UNTIL_GEOMETRY_ACCEPTANCE','normalization':'Per view: center visible bbox and isotropically normalize equal bbox height. No anisotropic warp. Width differences retained.','views':{}}
    for v,stem in VIEWS.items():
        refpath=SRC/f'carol-{stem}.png';renderpath=folder/f'{v}-render.png';claypath=folder/f'{v}-clay.png'
        if not renderpath.exists():renderpath=claypath
        ref,mod,ra,rb=register_pair(Image.open(refpath),Image.open(renderpath),v.startswith('3q'))
        am=silhouette(ref);bm=silhouette(mod);inter=(am&bm).sum();union=(am|bm).sum();iou=float(inter/union)
        ref.save(dest/f'{v}-reference.png');mod.save(dest/f'{v}-render.png')
        oldpath=OUT/'old-look-native.png'
        if oldpath.exists():
            old=Image.open(oldpath).convert('RGBA');h=ra['registered_bbox'][3]-ra['registered_bbox'][1];w=round(old.width/old.height*h)
            framed=Image.new('RGBA',(SIZE,SIZE));framed.alpha_composite(old.resize((w,h),Image.Resampling.LANCZOS),((SIZE-w)//2,(SIZE-h)//2));framed.save(dest/f'{v}-old.png')
        # Clay and look must share exactly the render transform, not independent fit.
        clay=Image.open(claypath).convert('RGBA');box=rb['source_bbox'];out=Image.new('RGBA',(SIZE,SIZE));x,y,x1,y1=rb['registered_bbox'];out.alpha_composite(clay.crop(box).resize((x1-x,y1-y),Image.Resampling.LANCZOS),(x,y));out.save(dest/f'{v}-clay.png')
        Image.blend(compose_background(ref),compose_background(mod),.5).save(dest/f'{v}-overlay.png')
        diff=np.abs(np.asarray(compose_background(ref)).astype(int)-np.asarray(compose_background(mod)).astype(int)).astype('uint8');Image.fromarray(diff).save(dest/f'{v}-difference.png')
        sil=np.zeros((SIZE,SIZE,4),dtype=np.uint8);sil[am]=[71,157,234,160];sil[bm]=[245,137,95,190];sil[am&bm]=[91,194,156,255];Image.fromarray(sil).save(dest/f'{v}-silhouette.png')
        threshold=.92 if v.startswith('3q') else .95
        landmarks={k:[pt[0]*rb['scale']+rb['offset'][0],pt[1]*rb['scale']+rb['offset'][1]] for k,pt in data['cameras'][v]['landmarks_px'].items()}
        row={'silhouette_iou':round(iou,6),'target':threshold,'silhouette_status':'PASS' if iou>=threshold else 'FAIL','landmark_error':None,'face_depth':None,'top_width_error':None,'reference_file':str(refpath.relative_to(ROOT)),'render_file':str(renderpath.relative_to(ROOT)),'registration':{'reference':ra,'model':rb},'model_landmarks':landmarks,'landmark_status':'Not evaluated until explicit reference correspondence; null is not a pass','segmentation_uncertainty':'3Q white-background mask can include soft floor shadow / exclude white contour' if v.startswith('3q') else 'alpha threshold 127; boundary uncertainty ~1-2 source pixels'}
        source_view=measured['views'][v.replace('3q-','three_quarter_')]
        ref_landmarks=source_view['landmarks'];errors={};registered_refs={}
        dimensions=np.array([ra['registered_bbox'][2]-ra['registered_bbox'][0],ra['registered_bbox'][3]-ra['registered_bbox'][1]])
        for key,name in ALIASES.items():
            p=ref_landmarks.get(key)
            if p and isinstance(p.get('pixel'),list) and name in landmarks:
                rp=np.array(p['pixel'])*ra['scale']+ra['offset'];mp=np.array(landmarks[name]);delta=(mp-rp)/dimensions
                errors[key]={'normalized_error':float(np.linalg.norm(delta)),'delta_xy':delta.tolist(),'source_uncertainty_px':p.get('uncertainty_px'),'target':.01 if key.startswith(('eye','nose','mouth')) else .015}
                registered_refs[name]=rp.tolist()
        row['reference_landmarks']=registered_refs;row['landmark_errors']=errors
        if errors:
            row['landmark_error']=float(np.mean([e['normalized_error'] for e in errors.values()]));row['landmark_max_error']=max(e['normalized_error'] for e in errors.values());row['landmark_status']='PASS' if all(e['normalized_error']<=e['target'] for e in errors.values()) else 'FAIL'
        maskpath=folder/f'{v}-face-mask.png'
        if maskpath.exists():
            fa=np.array(Image.open(maskpath).convert('RGBA'));skin=(fa[:,:,:3].min(2)>127)&(fa[:,:,3]>127);ys,xs=np.where(skin)
            if len(xs):
                body_width=rb['source_bbox'][2]-rb['source_bbox'][0];ratio=float((xs.max()-xs.min()+1)/body_width)
                row['face_depth']={'visible_skin_width_body_ratio':ratio,'visible_skin_area_px':int(skin.sum()),'skin_bbox_px':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'method':'Visible surface ID mask; opaque fleece and all face parts occlude normally'}
                if v=='side':
                    row['face_depth']['reference_width_body_ratio']=source_view['measurements'].get('face_to_overall_width');row['face_depth']['status']='VISIBLE_NOT_ACCEPTED' if ratio>.08 else 'FAIL_FACE_DISAPPEARS'
        if v=='top':
            aw,ab=width(am);bw,bb=width(bm);norm=ab[2]-ab[0];error=float(np.abs(aw-bw).mean()/norm)
            row['top_width_error']=round(error,6);row['width_profile_reference_px']=aw.tolist();row['width_profile_model_px']=bw.tolist()
            row['top_width_status']='PASS' if error<=.02 else 'FAIL'
            def stats(w):
                j=35+int(np.argmin(w[35:70]));return {'mid_min_px':float(w[j]),'mid_location_s':j/100,'front_max_px':float(w[:45].max()),'rear_max_px':float(w[55:95].max()),'mid_max_ratio':float(w[j]/max(w[:45].max(),w[55:95].max()))}
            row['width_profile_stats']={'reference':stats(aw),'model':stats(bw)}
        report['views'][v]=row
    (dest/'metrics.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:{'iou':v['silhouette_iou'],'width_error':v['top_width_error']} for k,v in report['views'].items()},indent=2))

if __name__=='__main__':main()
