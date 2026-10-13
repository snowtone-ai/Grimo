"""Arrange unretouched matched muzzle renders and verify their camera pairs."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v003/muzzle-revision'
PREVIOUS=OUT.parent/'appeal-revision'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def font(n):return ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
def board(name,title,state,kind):
    w,h=420,473; sheet=Image.new('RGB',(1260,110+2*(h+32)),(245,244,241));d=ImageDraw.Draw(sheet)
    d.text((18,12),title,fill='#222222',font=font(27))
    d.text((18,55),'Same saved cameras / unretouched renders / HUMAN PENDING / TRIPO HOLD',fill='#555555',font=font(18))
    for row,version in enumerate(['before','after']):
        for col,view in enumerate(['front','side','3q']):
            x=col*w;y=110+row*(h+32)
            d.text((x+12,y+4),version+' / '+view,fill='#333333',font=font(21))
            pic=Image.open(OUT/'renders'/f'{version}-{state}-{kind}-{view}.png').convert('RGB')
            sheet.paste(pic.resize((w,h),Image.Resampling.LANCZOS),(x,y+32))
    sheet.save(OUT/name)
def small_full():
    sheet=Image.new('RGB',(840,1120),(245,244,241));d=ImageDraw.Draw(sheet)
    d.text((18,12),'Small / large mouth regression - 3Q',fill='#222222',font=font(27))
    d.text((18,55),'Same camera / diagnostic colour / HUMAN PENDING',fill='#555555',font=font(18))
    for row,state in enumerate(['small','full']):
        for col,version in enumerate(['before','after']):
            x=col*420;y=110+row*505;d.text((x+12,y+4),version+' / '+state,fill='#333333',font=font(21))
            pic=Image.open(OUT/'renders'/f'{version}-{state}-colour-3q.png').convert('RGB')
            sheet.paste(pic.resize((420,473),Image.Resampling.LANCZOS),(x,y+32))
    sheet.save(OUT/'04-open-mouth-check.png')
def main():
    board('00-nose-clay.png','Nose / subnasal geometry: before > after','neutral','clay')
    board('01-nose-colour.png','Nose / subnasal depth: diagnostic colour','neutral','colour')
    board('02-smile-clay.png','Smile: preserved aperture / softened muzzle','smile','clay')
    board('03-companion-colour.png','Seated companion: before > after','companion','colour')
    small_full()
    cameras=json.loads((OUT/'cameras.json').read_text());pairs={};images={}
    for name,camera in cameras.items():
        p=OUT/'renders'/(name+'.png')
        with Image.open(p) as im:im.load();size=list(im.size)
        assert size==[480,540];images[name]={'sha256':sha(p),'size':size}
        if name.startswith('after-'):
            before='before-'+name[len('after-'):];assert camera==cameras[before]
            parts=name.split('-');state=parts[1];prior=('companion' if state=='companion' else 'mouth-'+state)+'-'+'-'.join(parts[2:])
            recaptured=parts[-1]=='side' and state!='companion'
            if not recaptured:assert sha(OUT/'renders'/(before+'.png'))==sha(PREVIOUS/'renders'/(prior+'.png'))
            pairs[name]={'before':before,'cameras_identical':True,'predecessor_source':('Saved 6f48223 model, same translated side camera' if recaptured else prior)}
    assert len(pairs)==14 and len(images)==28
    result={'Human':'PENDING','Tripo':'HOLD','candidate_views':14,'recaptured_predecessor_views':3,'reused_predecessor_renders':11,'pairs':pairs,'images':images,'board_operations':'Resize, arrangement and labels only; no pixel retouch or render warping'}
    (OUT/'review-manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('MUZZLE_BOARDS_COMPLETE',len(pairs))
if __name__=='__main__':main()
