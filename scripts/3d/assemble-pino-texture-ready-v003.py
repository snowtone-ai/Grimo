"""Compact review evidence: representative GIFs, UV wire layout, checksums."""
from pathlib import Path
import json,hashlib,subprocess,importlib.util,shutil,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];TMP=ROOT/'artifacts/pino-texture-v003';OUT=ROOT/'docs/production/pino/evidence/texture-ready-v003';DEST=ROOT/'assets/grimo/production/pino/candidate-c/texture-ready-v003'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',14)
def dump(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def picture(path,size):return ImageOps.contain(Image.open(path).convert('RGB'),size)
def main():
    frames=[(f['label'],f['controls']) for f in json.loads((TMP/'proof-frames.json').read_text(encoding='utf8'))]
    dump('proof-controls.json',[{'label':name,'closed':a[0],'large':a[1],'blink_L':a[2],'blink_R':a[3]} for name,a in frames])
    visibility=[]
    for i,(name,args) in enumerate(frames):
        for view in ['front','side','3q']:
            rgb=np.asarray(Image.open(TMP/f'proof-{i:02d}-{view}.png').convert('RGB'),dtype=int);r,g,b=rgb.transpose(2,0,1)
            eye=(g>r+8)&(b>g+8)&(b>r+15);oral=(r>g+3)&(abs(g-b)<=3)
            visibility.append({'frame':i,'state':name,'view':view,'eye_blue_pixels':int(eye.sum()),'image_left_eye_pixels':int(eye[:,:180].sum()) if view=='front' else None,'image_right_eye_pixels':int(eye[:,180:].sum()) if view=='front' else None,'oral_color_pixels_in_front_mouth_roi':int(oral[185:255,120:240].sum()) if view=='front' else None})
    hidden={}
    for view in ['front','side','3q']:
        a=np.asarray(Image.open(TMP/f'proof-00-{view}.png').convert('RGB'),dtype=int);b=np.asarray(Image.open(TMP/f'closed-liner-hidden-{view}.png').convert('RGB'),dtype=int);delta=abs(a-b)
        hidden[view]={'changed_pixels_when_hiding_closed_liner':int((delta.max(2)>0).sum()),'max_channel_delta':int(delta.max())}
    dump('visibility-probes.json',{'scope':'360px diagnostic swatches; occlusion probe only, not visual approval. Anatomical L is image right in front view. Oral ROI front x120:240 y185:255 avoids warm studio highlights elsewhere.','closed_liner_hidden_comparison':hidden,'samples':visibility})
    neutral={};board=Image.new('RGB',(1200,870),(28,32,39));draw=ImageDraw.Draw(board)
    for i,view in enumerate(['front','side','3q']):
        a=Image.open(TMP/f'authority-{view}.png').convert('RGB');b=Image.open(TMP/f'candidate-neutral-{view}.png').convert('RGB');delta=np.abs(np.asarray(a,dtype=int)-np.asarray(b,dtype=int));neutral[view]={'changed_pixels':int((delta.max(2)>0).sum()),'max_channel':int(delta.max())}
        board.paste(a,(400*i,35));board.paste(b,(400*i,465));draw.text((400*i+10,8),'v002 source '+view,font=font,fill='white');draw.text((400*i+10,440),'v003 Basis | '+str(neutral[view]),font=small,fill='white')
    board.save(OUT/'neutral-comparison.png');dump('neutral-render-difference.json',neutral)
    # Representative body failures and bounded checks; existing rig proof poses.
    body=Image.new('RGB',(1080,1170),(28,32,39));d=ImageDraw.Draw(body)
    rows=[('Bounded checks: tail L / tail R / low forepaw',['tail-left-LBS4-3q','tail-right-LBS4-3q','forepaw-LBS4-3q']),('Both paws: existing stress pose FAIL (front / side / 3Q)',['both-paws-LBS4-front','both-paws-LBS4-side','both-paws-LBS4-3q']),('Rest: shallow is not low rest; deep test penetrates floor',['shallow-rest-LBS4-3q','deep-rest-LBS4-front','deep-rest-LBS4-side'])]
    for row,(title,items) in enumerate(rows):
        d.text((10,row*390+5),title,font=font,fill='white')
        for col,item in enumerate(items):body.paste(picture(TMP/(item+'.png'),(360,350)),(col*360,row*390+35))
    body.save(OUT/'body-boundaries.png')
    identity=Image.new('RGB',(1350,980),(28,32,39));d=ImageDraw.Draw(identity)
    refs=[('Canonical',ROOT/'assets/grimo/source/pino/pino-Identity-canonical.png'),('Approved Body-only front',ROOT/'assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png'),('Approved Body-only left',ROOT/'assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png')]
    for col,(label,path) in enumerate(refs):
        im=picture(path,(450,450));identity.paste(im,(450*col+(450-im.width)//2,35));d.text((450*col+10,8),label,font=font,fill='white')
    for col,view in enumerate(['front','side','3q']):
        identity.paste(picture(TMP/f'identity-{view}.png',(450,450)),(450*col,525));d.text((450*col+10,497),'v003 Basis / '+view+' / untextured',font=font,fill='white')
    identity.save(OUT/'identity-comparison.png')
    cause=Image.new('RGB',(1080,400),(28,32,39));d=ImageDraw.Draw(cause)
    for i,(label,name) in enumerate([('Saved Master / local pose normals','roundtrip-master-closed-front'),('Native import / missing normal binding','roundtrip-native-closed'),('GLB normals rebound / same closed pose','reimport-closed-front')]):
        cause.paste(picture(TMP/(name+'.png'),(360,360)),(360*i,35));d.text((360*i+8,8),label,font=small,fill='white')
    cause.save(OUT/'normal-cause.png')
    stages=Image.new('RGB',(1080,1950),(28,32,39));d=ImageDraw.Draw(stages)
    labels=['half both','three quarter both','settling both','near closed both','closed both']
    for row,label in enumerate(labels):
        idx=next(i for i,(name,args) in enumerate(frames) if name==label)
        for col,view in enumerate(['front','side','3q']):
            stages.paste(picture(TMP/f'proof-{idx:02d}-{view}.png',(360,360)),(360*col,390*row+28))
            d.text((360*col+8,390*row+5),label+' / '+view,font=small,fill='white')
    stages.save(OUT/'eye-closure-stages.png')
    bank=np.load(TMP/'uv-layout.npz');audit=json.loads((OUT/'saved-master-audit.json').read_text());uv=Image.new('RGB',(2100,2170),'white');d=ImageDraw.Draw(uv);colors=['#286f9c','#b36b16','#509447','#a45691'];triangles=[];owners=[]
    for idx,record in enumerate(audit['objects']):
        points=bank[f'{idx}_uv'];starts=bank[f'{idx}_starts'];counts=bank[f'{idx}_counts']
        for face,(start,count) in enumerate(zip(starts,counts)):
            p=points[start:start+count];d.line([(25+float(x)*2048,60+(1-float(y))*2048) for x,y in np.vstack([p,p[:1]])],fill=colors[idx],width=1)
            for i in range(1,count-1):triangles.append(p[[0,i,i+1]]);owners.append((idx,face))
        d.text((25+idx*515,2120),record['name'].replace('PINO_C_BASE_RIG_V001','Original body'),font=small,fill=colors[idx])
    d.text((25,15),'PinoUV_v003 candidate atlas — UV wire layout, NOT a texture — Human Gate PENDING',font=font,fill='black');uv.save(DEST/'pino-c-v003-uv-layout.png')
    sp=importlib.util.spec_from_file_location('uvcheck',ROOT/'scripts/3d/pino-uv-overlap.py');check=importlib.util.module_from_spec(sp);sp.loader.exec_module(check);pairs,zero=check.overlaps(triangles);uvpoints=np.concatenate([bank[f'{i}_uv'] for i in range(len(audit['objects']))]);dump('uv-audit.json',{'triangles':len(triangles),'positive_area_overlap_pairs':len(pairs),'zero_area_uv_triangles':len(zero),'tolerance_uv':1e-8,'bounds_min':uvpoints.min(0).tolist(),'bounds_max':uvpoints.max(0).tolist(),'method':'grid broad phase + strict separating-axis test across every object; shared borders excluded'})
    # Compare local protected files against the exact HEAD Git/LFS content.
    paths=subprocess.check_output(['git','ls-files','assets/grimo/production/pino/candidate-c/source','assets/grimo/production/pino/candidate-c/rig-v001','assets/grimo/production/pino/candidate-c/face-foundation-v002','assets/grimo/source/pino/pino-Identity-canonical.png'],cwd=ROOT,text=True,encoding='utf8').splitlines();protected=[]
    for path in paths:
        if Path(path).suffix.lower() not in {'.blend','.glb','.fbx','.png'}:continue
        original=subprocess.check_output(['git','show','HEAD:'+path],cwd=ROOT);actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        if original.startswith(b'version https://git-lfs'):expected=original.decode().split('oid sha256:')[1].splitlines()[0]
        else:expected=hashlib.sha256(original).hexdigest()
        protected.append({'path':path,'sha256':actual,'matches_authority_HEAD':actual==expected})
    dump('source-protection.json',protected)
    if (TMP/'validator.json').exists():
        validator=json.loads((TMP/'validator.json').read_text(encoding='utf-8-sig'))
        dump('glb-validator.json',{'file':Path(validator['file']).name,'validator':validator['validator'],'structure_report':'gltf-structure.json; legacy metrics counters are not used'})
    spec=importlib.util.spec_from_file_location('glb',ROOT/'scripts/3d/package-pino-texture-ready-v003.py');glb=importlib.util.module_from_spec(spec);spec.loader.exec_module(glb)
    document,blob=glb.read(DEST/'pino-c-texture-ready-v003-HOLD.glb');structure=[]
    for mesh in document['meshes']:
        primitives=[]
        for p in mesh['primitives']:
            joints=glb.accessor(document,blob,p['attributes']['JOINTS_0']);weights=glb.accessor(document,blob,p['attributes']['WEIGHTS_0'])
            primitives.append({'vertices':document['accessors'][p['attributes']['POSITION']]['count'],'triangles':document['accessors'][p['indices']]['count']//3,'joint_index_max':int(joints.max()),'weight_sum_max_error':float(abs(weights.sum(1)-1).max()),'all_targets_have_position_normal':all('POSITION' in t and 'NORMAL' in t for t in p['targets']),'provenance_attributes':[x for x in p['attributes'] if x.startswith('_PINO_')]})
        structure.append({'mesh':mesh['name'],'morph_names':mesh['extras']['targetNames'],'primitives':primitives})
    dump('gltf-structure.json',{'meshes':structure,'skin_joint_counts':[len(s['joints']) for s in document['skins']],'materials':[m['name'] for m in document['materials']],'textures':len(document.get('textures',[])),'images':len(document.get('images',[])),'animations':len(document.get('animations',[]))})
    if (TMP/'runtime-probe.log').exists():
        raw=(TMP/'runtime-probe.log').read_text(encoding='utf-8-sig');dump('runtime-probe.json',json.loads(raw.split('### Result\n',1)[1].split('\n### Ran',1)[0]))
    for name in ['runtime-three-quarter','runtime-wink','runtime-combined','runtime-head-probe']:
        if (TMP/(name+'.png')).exists():shutil.copyfile(TMP/(name+'.png'),OUT/(name+'.png'))
    dump('file-manifest.json',[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(DEST.iterdir()) if p.is_file()])
if __name__=='__main__':main()
