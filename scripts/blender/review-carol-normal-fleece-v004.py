"""Unretouched, equal-scale evidence and image-space diagnostics."""
from pathlib import Path
import json
import sys
import hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import binary_erosion, distance_transform_edt

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v004'
WORK=ROOT/'artifacts/carol-fleece-v004'
REF=ROOT/'assets/grimo/source/carol/approved-3d'
FOLDER=OUT/(sys.argv[1] if len(sys.argv)>1 else 'renders')
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)


def verify_manifest():
    manifest=json.loads((FOLDER/'render-manifest.json').read_text())
    asset=ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v004.blend'
    digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest(asset)==manifest['asset_sha256'],'Evidence is not from the current saved asset'
    for name,value in manifest['generator_hashes'].items():
        assert digest(ROOT/'scripts/blender'/name)==value,f'Generator changed: {name}'
    assert manifest['views'],'No rendered views'
    for view,record in manifest['views'].items():
        path=FOLDER/f'{view}.png'
        assert digest(path)==record['sha256'],f'Render changed: {view}'
        with Image.open(path) as im:
            assert list(im.size)==record['size'],f'Incorrect size: {view}'
            alpha=np.asarray(im.convert('RGBA'))[:,:,3]
            assert np.count_nonzero(alpha>128)>1000,f'Blank render: {view}'
    print(json.dumps({'evidence_integrity':'PASS','asset_sha256':manifest['asset_sha256'],'views':len(manifest['views'])}))


def normalized(path,height=720,maskpath=None):
    im=Image.open(path).convert('RGBA')
    mask=np.array(Image.open(maskpath))>128 if maskpath else np.array(im)[:,:,3]>128
    y,x=np.where(mask)
    box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))
    im=im.crop(box);mask=Image.fromarray((mask*255).astype('uint8')).crop(box)
    size=(round(im.width*height/im.height),height)
    im=im.resize(size,Image.Resampling.LANCZOS)
    m=np.array(mask.resize(size,Image.Resampling.NEAREST))>128
    canvas=Image.new('RGB',(1100,height+80),'white')
    canvas.paste(im,((1100-size[0])//2,40),im)
    padded=np.zeros((height,1100),bool);padded[:,(1100-size[0])//2:(1100+size[0])//2]=m
    return canvas,padded,box


def main():
    verify_manifest()
    if '--verify-only' in sys.argv:return
    measurements={}
    for view in ['front','side']:
        if not (FOLDER/f'{view}.png').exists():continue
        a,am,_=normalized(REF/f'carol_{view}.png',maskpath=WORK/f'silhouette-{view}.png')
        b,bm,_=normalized(FOLDER/f'{view}.png')
        board=Image.new('RGB',(2200,870),'white');board.paste(a,(0,50));board.paste(b,(1100,50))
        d=ImageDraw.Draw(board);d.text((28,20),'CURRENT APPROVED '+view.upper(),font=FONT,fill='#303036')
        d.text((1128,20),'V004 / SAME SAVED MODEL',font=FONT,fill='#303036')
        board.save(FOLDER/f'comparison-{view}.jpg',quality=94)
        ea=am^binary_erosion(am);eb=bm^binary_erosion(bm)
        measurements[view]={'silhouette_iou':float((am&bm).sum()/(am|bm).sum()),'symmetric_contour_distance_H':float((distance_transform_edt(~ea)[eb].mean()+distance_transform_edt(~eb)[ea].mean())/(2*720))}
        ov=np.full((*am.shape,3),255,np.uint8);ov[am]=[235,157,185];ov[bm]=[130,190,235];ov[am&bm]=[183,182,208]
        Image.fromarray(ov).save(FOLDER/f'overlay-{view}.png')
    views=['yaw-45','yaw-30','yaw-15','front','yaw+15','yaw+30','yaw+45','side','yaw+90','yaw+135','rear','top']
    available=[v for v in views if (FOLDER/f'{v}.png').exists()]
    board=Image.new('RGB',(500*min(4,len(available)),550*((len(available)+3)//4)),'white')
    for i,view in enumerate(available):
        im=Image.open(FOLDER/f'{view}.png').convert('RGBA');im.thumbnail((500,500))
        x=(i%4)*500;y=(i//4)*550
        board.paste(im,(x+(500-im.width)//2,y+35),im)
        ImageDraw.Draw(board).text((x+15,y+5),view,font=FONT,fill='#303036')
    board.save(FOLDER/'spatial.jpg',quality=94)
    product=Image.new('RGB',(640,280),'white')
    for i,(path,maskpath,label) in enumerate([
        (REF/'carol_front.png',WORK/'silhouette-front.png','APPROVED / 160 PX'),
        (FOLDER/'front.png',None,'IN PROGRESS / 160 PX'),
    ]):
        small,_,_=normalized(path,height=160,maskpath=maskpath)
        product.paste(small.crop((390,0,710,240)),(i*320,35))
        ImageDraw.Draw(product).text((i*320+15,12),label,font=FONT,fill='#303036')
    product.save(FOLDER/'product-scale.png')
    if '--anatomy-comparison' in sys.argv:
        anatomy_comparison()
    (FOLDER/'geometry-measurements.json').write_text(json.dumps(measurements,indent=2),encoding='utf-8')
    print(json.dumps(measurements))


def anatomy_comparison():
    """Historical images are labeled; only the last column is the current asset."""
    board=Image.new('RGB',(2000,1060),'white')
    draw=ImageDraw.Draw(board)
    columns=[('APPROVED AUTHORITY',REF),
             ('V002 / HISTORICAL',OUT.parent/'normal-fleece-v002'),
             ('V004-33 / REJECTED SHAPE',OUT/'iterations/33'),
             ('V004 / ANATOMICAL REVISION',FOLDER)]
    sources=[]
    for row,view in enumerate(['front','side']):
        for col,(label,folder) in enumerate(columns):
            filename=f'carol_{view}.png' if col==0 else f'{view}.png'
            if view=='side' and col>=2:filename='yaw+90.png'
            path=folder/filename
            mask=WORK/f'silhouette-{view}.png' if col==0 else None
            panel,_,_=normalized(path,height=390,maskpath=mask)
            panel=panel.crop((300,0,800,470))
            mirrored=col>0 and view=='side'
            if mirrored:panel=panel.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            board.paste(panel,(col*500,row*530+45))
            draw.text((col*500+12,row*530+10),label,font=FONT,fill='#303036')
            sources.append({'label':label,'view':view,'path':path.relative_to(ROOT).as_posix(),
                            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                            'display_mirrored':mirrored})
    board.save(FOLDER/'anatomy-comparison.jpg',quality=94)
    (FOLDER/'anatomy-comparison-sources.json').write_text(json.dumps({
        'normalization':'Equal character height; no shape retouching; historical lighting differs',
        'sources':sources},indent=2),encoding='utf-8')


if __name__=='__main__':main()
