"""Assemble unretouched renders and original authority images for Human review."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v003/appeal-revision'
RENDERS=OUT/'renders'
FONT='C:/Windows/Fonts/segoeui.ttf'
def font(n):return ImageFont.truetype(FONT,n)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def board(name,title,rows,subtitle='Same cameras and lighting / HUMAN PENDING / TRIPO HOLD'):
    w,h=420,473;canvas=Image.new('RGB',(w*3,100+(h+32)*len(rows)),(245,244,241));d=ImageDraw.Draw(canvas)
    d.text((18,12),title,fill='#222222',font=font(27));d.text((18,53),subtitle,fill='#555555',font=font(18))
    for j,(label,stem) in enumerate(rows):
        for i,view in enumerate(['front','side','3q']):
            y=100+j*(h+32);d.text((i*w+12,y+4),label+' / '+view,fill='#333333',font=font(20))
            im=Image.open(RENDERS/(stem+'-'+view+'.png')).convert('RGB');im=im.resize((w,h),Image.Resampling.LANCZOS);canvas.paste(im,(i*w,y+32))
    canvas.save(OUT/name)
def authorities():
    src=ROOT/'assets/grimo/source/shushu'
    rows=[('Canonical',src/'shushu-Identity-canonical.png')]
    rows +=[(s,src/'tripo-generation-pose'/('shushu_bodyonly_'+s+'.png')) for s in ['front','left','right','back']]
    for n in range(18,27):rows.append(('#'+str(n),next(ROOT.glob(str(n)+'-*.png'))))
    w,h=420,480;sheet=Image.new('RGB',(w*3,110+((len(rows)+2)//3)*h),(245,244,241));d=ImageDraw.Draw(sheet)
    d.text((18,12),'Canonical / approved views #18-26',font=font(28),fill='#222222')
    d.text((18,53),'Original 2D authority: resized only. Not a recaptured 3D camera match. #27 excluded.',font=font(18),fill='#555555')
    for j,(label,path) in enumerate(rows):
        x=(j%3)*w;y=110+(j//3)*h;d.text((x+14,y+5),label,font=font(20),fill='#333333')
        im=Image.open(path).convert('RGB');im.thumbnail((w,h-32),Image.Resampling.LANCZOS);sheet.paste(im,(x+(w-im.width)//2,y+32+(h-32-im.height)//2))
    sheet.save(OUT/'10-authorities.png')
    return {p.relative_to(ROOT).as_posix():digest(p) for _,p in rows}
def main():
    for kind in ['clay','colour']:
        board('01-mouth-'+kind+'.png','Closed > small > large > smile / '+kind,[(s,'mouth-'+s+'-'+kind) for s in ['neutral','small','full','smile']])
        board('02-seat-'+kind+'.png','Standing > transition > seated / '+kind,[(s,'body-'+s+'-'+kind) for s in ['standing','seat25','seat50','seat75','seat100']])
        board('03-lids-'+kind+'.png','Soft closure and independent blink / '+kind,[(s,'lids-'+s+'-'+kind) for s in ['half','closed','happy-closed','wink']])
        rows=[]
        for s,current in [('full','mouth-full'),('smile','mouth-smile'),('seat100','body-seat100'),('half','lids-half'),('closed','lids-closed')]:
            rows.extend([('2031076 '+s,'baseline-'+s+'-'+kind),('current '+s,current+'-'+kind)])
        board('04-before-after-'+kind+'.png','2031076 > saved revision / '+kind,rows)
        board('05-donor-'+kind+'.png','Original Donor > current large opening / '+kind,[('Donor','donor-'+kind),('current large','mouth-full-'+kind),('current smile','mouth-smile-'+kind)])
    board('06-companion.png','Seated companion: geometry and diagnostic colour',[('clay','companion-clay'),('colour','companion-colour')])
    sheet=Image.new('RGB',(1260,110+2*505),(245,244,241));d=ImageDraw.Draw(sheet)
    d.text((18,12),'Half-blink wall diagnosis / same camera',font=font(28),fill='#222222')
    d.text((18,55),'Normal wall folds over eye > disable to isolate cause > backward sleeve retains coverage',font=font(18),fill='#555555')
    for row,view in enumerate(['front','3q']):
        for col,(label,stem) in enumerate([('2031076 wall','baseline-half-clay'),('Wall disabled: diagnostic','probe-half-no-walls'),('Current backward sleeve','lids-half-clay')]):
            x=col*420;y=110+row*505;d.text((x+10,y+4),label+' / '+view,font=font(18),fill='#333333');sheet.paste(Image.open(RENDERS/(stem+'-'+view+'.png')).convert('RGB').resize((420,473),Image.Resampling.LANCZOS),(x,y+32))
    sheet.save(OUT/'07-lid-wall-diagnosis.png')
    auth=authorities()
    # An entry-point board showing actual pixels, not selectively retouched details.
    items=[('2031076 opening','baseline-full-colour-front'),('Current opening','mouth-full-colour-front'),('Current smile','mouth-smile-colour-front'),('2031076 seat','baseline-seat100-clay-3q'),('Current seat','body-seat100-clay-3q'),('Closed-eye smile','lids-happy-closed-colour-3q')]
    w,h=360,405;sheet=Image.new('RGB',(1080,90+2*(h+32)),(245,244,241));d=ImageDraw.Draw(sheet)
    d.text((18,12),'Shushu v003 / appeal revision',font=font(30),fill='#222222');d.text((18,52),'HUMAN PENDING / TRIPO HOLD / diagnostic colours, not final texture',font=font(18),fill='#555555')
    for j,(label,stem) in enumerate(items):
        x=j%3*w;y=90+j//3*(h+32);d.text((x+10,y+5),label,font=font(20),fill='#333333');sheet.paste(Image.open(RENDERS/(stem+'.png')).convert('RGB').resize((w,h),Image.Resampling.LANCZOS),(x,y+32))
    sheet.save(OUT/'00-overview.png')
    cameras=json.loads((OUT/'cameras.json').read_text());used={k:c for k,c in cameras.items() if not k.startswith('trial-')}
    expected=set()
    stems=['mouth-'+s for s in ['neutral','small','full','smile']]+['body-'+s for s in ['standing','seat25','seat50','seat75','seat100']]+['lids-'+s for s in ['half','closed','happy-closed','wink']]+['companion','donor']+['baseline-'+s for s in ['neutral','small','full','smile','seat100','half','closed']]
    for stem in stems:
        for kind in ['clay','colour']:
            for view in ['front','side','3q']:expected.add(stem+'-'+kind+'-'+view)
    expected.update('probe-half-no-walls-'+view for view in ['front','3q'])
    assert set(used)==expected,{'missing':list(expected-set(used)),'extra':list(set(used)-expected)}
    common={}
    for key,c in used.items():
        view=key.rsplit('-',1)[-1];bucket=(view,c['ortho_scale'],c['colour']);previous=common.setdefault(bucket,c)
        assert c==previous,(key,'Camera/lighting mismatch')
        assert (RENDERS/(key+'.png')).exists()
    report={'Human':'PENDING','Tripo':'HOLD','renderer':'Blender Cycles; no image editing beyond board resize/placement/labels','camera_groups_verified':len(common),'render_count':len(used),'renders':{key+'.png':digest(RENDERS/(key+'.png')) for key in used},'boards':{p.name:digest(p) for p in OUT.glob('*.png')},'authority_sources':auth,'authority_limit':'Original 2D images cannot be re-rendered under a Blender camera; their provenance and content are unchanged. Donor/current 3D comparisons use identical cameras.'}
    (OUT/'review-manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('APPEAL_BOARDS_COMPLETE',len(used))
if __name__=='__main__':main()
