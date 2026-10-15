"""Build Human-review media from actual rendered duplicate-mesh frames."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/geometry-c-v001';M=OUT/'motion'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20);SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
VIEWS=['front','threequarter','side']
FAMILIES={'tail':['tail'],'eyes':['eyes-L-blink','eyes-R-blink','eyes-L-wink','eyes-R-wink','eyes-half','eyes-full-close'],
    'forepaws':['raise-L','raise-R','high-five-L','both-contact','food-hold','gift-present'],'low-rest':['low-rest']}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def frame(run,i):
    canvas=Image.new('RGB',(1080,420),'#eef0f3');d=ImageDraw.Draw(canvas)
    row=run['frames'][i];d.text((10,5),f"FBX duplicate / {run['name']} / {i+1:02d}/{len(run['frames']):02d} / strength {row['strength']:.2f}",font=FONT,fill='#182533')
    for k,v in enumerate(VIEWS):
        im=Image.open(M/f"{run['name']}-{i:03d}-{v}.png").convert('RGB').resize((350,350));canvas.paste(im,(k*360+5,36));d.text((k*360+10,390),v,font=SMALL,fill='#182533')
    return canvas
def board(items,path,cols=3,size=(350,350)):
    w,h=size[0]+20,size[1]+45;out=Image.new('RGB',(w*cols,h*((len(items)+cols-1)//cols)),'#eef0f3');d=ImageDraw.Draw(out)
    for i,(p,label) in enumerate(items):
        im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,'#eef0f3');bg.alpha_composite(im);im=bg.convert('RGB');im.thumbnail(size)
        x=(i%cols)*w;y=(i//cols)*h;out.paste(im,(x+(w-im.width)//2,y+32));d.text((x+10,y+5),label,font=SMALL,fill='#182533')
    out.save(path)
def main():
    data=read(OUT/('four-tests.json' if (OUT/'four-tests.json').exists() else 'four-tests-progress.json'));runs={r['name']:r for r in data['runs']};summary={};checks=[]
    for family,names in FAMILIES.items():
        if not all(n in runs for n in names):continue
        frames=[];items=[]
        for n in names:
            r=runs[n];frames.extend(frame(r,i) for i in range(len(r['frames'])))
            peak=max(range(len(r['frames'])),key=lambda i:abs(r['frames'][i]['strength']))
            for v in VIEWS:
                if (M/f'cycles-{n}-000-{v}.png').exists():items.append((M/f'cycles-{n}-000-{v}.png',f'{n} / {v} / endpoint'))
            for v in VIEWS:
                a=np.asarray(Image.open(M/f'{n}-000-{v}.png'));b=np.asarray(Image.open(M/f"{n}-{len(r['frames'])-1:03d}-{v}.png"));checks.append(dict(sequence=n,view=v,returned_pixels_exact=bool(np.array_equal(a,b))))
            rs=r['frames'];p=rs[peak]
            summary[n]=dict(neutral_return_exact=r['neutral_return_exact'],edge_ratio_min=min(x['edge_ratio_min'] for x in rs),edge_ratio_max=max(x['edge_ratio_max'] for x in rs),
                max_floor_penetration_vertices=max(x['floor_penetration_below_minus_1e_6'] for x in rs),lowest_z=min(x['lowest_z'] for x in rs),max_body_self_intersections=max(x['body_self_intersections'] for x in rs),
                tail_body_intersection_range=[min(x['tail_body_intersections'] for x in rs),max(x['tail_body_intersections'] for x in rs)],peak=p,fixture=r.get('fixture'))
        frames[0].save(OUT/f'actual-{family}.gif',save_all=True,append_images=frames[1:],loop=0,duration=130,optimize=False)
        # Actual transition extremes, including the last Neutral, in front/3Q/side.
        transition=[]
        for n in names:
            r=runs[n];peak=max(range(len(r['frames'])),key=lambda i:abs(r['frames'][i]['strength']))
            for i,label in [(0,'Neutral'),(peak,'extreme'),(len(r['frames'])-1,'returned')]:
                for v in VIEWS:transition.append((M/f'{n}-{i:03d}-{v}.png',f'{n} {label} / {v}'))
        board(transition,OUT/f'actual-{family}-extremes.png')
        if items:board(items,OUT/f'cycles-{family}-extremes.png')
    write(OUT/'four-tests-summary.json',dict(sequences=summary,rendered_neutral_return=checks,all_rendered_returns_pixel_exact=all(x['returned_pixels_exact'] for x in checks),gate='PENDING'))
    # Approved identity and pending pose references are explicitly distinguished.
    s=ROOT/'assets/grimo/source/pino';r=ROOT/'assets/grimo/production/pino/references'
    board([(s/'pino-Identity-canonical.png','Canonical identity'),(s/'tripo-generation-pose/pino_bodyonly_front.png','Approved body-only front'),(s/'tripo-generation-pose/pino_bodyonly_left.png','Approved body-only side'),
        (r/'pino-ref-05.png','Blink reference / Human PENDING'),(r/'pino-ref-22.png','High-five reference / PENDING'),(r/'pino-ref-28.png','Low-rest reference / PENDING'),
        (r/'pino-ref-25.png','Tail reference / PENDING'),(r/'pino-ref-30.png','Food reference / PENDING'),(r/'pino-ref-32.png','Gift reference / PENDING')],OUT/'appearance-authority-context.png')
    pairings=[('tail','pino-ref-25.png'),('eyes-full-close','pino-ref-05.png'),('high-five-L','pino-ref-22.png'),('gift-present','pino-ref-32.png'),('low-rest','pino-ref-28.png')]
    if all((M/f'cycles-{name}-000-side.png').exists() for name,_ in pairings):
        board([item for name,ref in pairings for item in [(r/ref,f'{name} reference / PENDING'),(M/f'cycles-{name}-000-threequarter.png','Actual diagnostic extreme / 3Q'),(M/f'cycles-{name}-000-side.png','Actual diagnostic extreme / side')]],OUT/'pose-reference-comparison.png')
    if all(n in runs for n in FAMILIES['eyes']):
        closeups=[]
        for name in FAMILIES['eyes']:
            for i in range(len(runs[name]['frames'])):
                im=Image.open(M/f'{name}-{i:03d}-front.png').convert('RGB').crop((65,75,335,220)).resize((756,406));canvas=Image.new('RGB',(756,443),'#eef0f3');canvas.paste(im,(0,35));ImageDraw.Draw(canvas).text((10,5),f'Actual eye trial / {name} / {i+1}',font=FONT,fill='#182533');closeups.append(canvas)
        closeups[0].save(OUT/'actual-eyes-detail.gif',save_all=True,append_images=closeups[1:],loop=0,duration=150,optimize=False)
if __name__=='__main__':main()
