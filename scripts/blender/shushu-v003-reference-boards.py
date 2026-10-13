"""Review mosaics only; source PNG bytes are never edited."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v003'
OUT.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
def board(paths,name,cols=5,w=310,h=370):
    result=Image.new('RGB',(cols*w,((len(paths)+cols-1)//cols)*h),(246,246,246))
    d=ImageDraw.Draw(result)
    for i,p in enumerate(paths):
        im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im)
        im=ImageOps.contain(bg.convert('RGB'),(w-12,h-45))
        x=(i%cols)*w;y=(i//cols)*h
        result.paste(im,(x+(w-im.width)//2,y+30+(h-40-im.height)//2))
        d.text((x+8,y+6),p.stem[:34],font=font,fill=(30,30,30))
    result.save(OUT/name)
if __name__=='__main__':
    src=ROOT/'assets/grimo/source/shushu'
    board([src/'shushu-Identity-canonical.png',*[src/'tripo-generation-pose'/('shushu_bodyonly_'+s+'.png') for s in ['front','left','right','back']]],'authorities.png')
    pack=ROOT/'assets/grimo/production/shushu/image-reference/reference-pack-v001'
    paths=sorted(pack.rglob('*.png'),key=lambda p:p.name)
    paths=[p for p in paths if p.name[:2].isdigit()]
    board(paths[:17],'references-01-17.png')
    board(paths[17:],'references-18-26.png',3,390,470)
    manifest=json.loads((ROOT/'docs/production/shushu/evidence/candidate-b-8481/input-manifest.json').read_text())
    rows=[]
    for r in manifest['files'][:2]+manifest['references']:
        p=ROOT/r['path'];digest=hashlib.sha256(p.read_bytes()).hexdigest()
        assert digest==r['sha256'],p
        rows.append(dict(path=r['path'],sha256=digest,bytes=p.stat().st_size))
    (OUT/'source-integrity.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('Source FBX/GLB + five primary references hash verified; reference count',len(paths))
