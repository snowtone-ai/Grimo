"""Skin gate comparisons; uses frozen registration exported by the build.

python scripts/blender/carol-v008-evidence.py --cycle 2
Final/Normal packets are intentionally unavailable before the Skin gate.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT/'assets/grimo/source/carol/approved-3d'


def background(image):
    result = Image.new('RGBA',image.size,'#f1f0f4')
    result.alpha_composite(image.convert('RGBA'))
    return result.convert('RGB')


def registered(reg,size):
    image = Image.open(REF/reg['file']).convert('RGBA')
    scale = size/1.52/reg['h']
    ox = size/2-reg['origin']*scale
    if reg['view']=='side':
        ox -= .65*size/1.52
    oy = size/2+.5*size/1.52-reg['ground']*scale
    return image.transform((size,size),Image.Transform.AFFINE,
        (1/scale,0,-ox/scale,0,1/scale,-oy/scale),resample=Image.Resampling.BICUBIC)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cycle',type=int,choices=[1,2,3],default=2)
    parser.add_argument('--publish-blocked',action='store_true',
                        help='Copy selected Skin evidence only; never implies a Human submission.')
    args = parser.parse_args()
    directory = ROOT/'tmp-carol-v008'/('cycle-'+str(args.cycle))
    data = json.loads((directory/'measurements.json').read_text())
    for name,digest in data['reference_hashes'].items():
        assert hashlib.sha256((REF/name).read_bytes()).hexdigest()==digest, name
    size = 480
    sheet = Image.new('RGB',(size*3,(size+32)*2),'#f1f0f4')
    draw = ImageDraw.Draw(sheet)
    for row,view in enumerate(['front','side']):
        key = 'skin-'+view
        model = Image.open(directory/(key+'.png')).convert('RGBA')
        reference = registered(data['reference_registration'][key],model.width)
        overlay = Image.blend(background(reference),background(model),.5)
        overlay.save(directory/(key+'-overlay.png'))
        for col,(label,image) in enumerate([('LOCKED reference',reference),('same neutral model',model),('50% overlay',overlay)]):
            x,y = col*size,row*(size+32)
            draw.text((x+10,y+9),key+' | '+label,fill='#242137')
            sheet.paste(background(image).resize((size,size)),(x,y+32))
    sheet.save(directory/'skin-review-sheet.png')
    if args.publish_blocked:
        if data.get('executor_disposition') != 'BLOCKED_AT_V008_SKIN_INTERNAL_GATE':
            raise RuntimeError('Only an explicitly blocked Skin packet may be published here')
        final = ROOT/'docs/production/carol/evidence/reconstruction-v008'
        final.mkdir(parents=True,exist_ok=True)
        for name in ['skin-front.png','skin-side.png','skin-front-overlay.png',
                     'skin-side-overlay.png','skin-review-sheet.png','measurements.json']:
            shutil.copy2(directory/name,final/name)
    print(directory/'skin-review-sheet.png')


if __name__=='__main__':
    main()
