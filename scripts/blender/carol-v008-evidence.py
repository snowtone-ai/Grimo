"""Skin gate comparisons; uses frozen registration exported by the build.

python scripts/blender/carol-v008-evidence.py --revision 9
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


def comparison_sheet(rows, path):
    # Same fixed image-space crop for every diagnostic/before-after panel.
    # This removes empty framing only; no geometry registration or scaling fit.
    width,height = 480,316
    result = Image.new('RGB',(3*width,len(rows)*height),'#f1f0f4')
    draw = ImageDraw.Draw(result)
    for r,row in enumerate(rows):
        for c,(label,im) in enumerate(row):
            draw.text((c*width+8,r*height+8),label,fill='#242137')
            if isinstance(im,Path):
                im = Image.open(im)
            assert im.size == (640,640), 'Diagnostic crop is defined for 640 px renders'
            panel = background(im).crop((25,200,600,550))
            panel = panel.resize((width,292))
            result.paste(panel,(c*width,r*height+24))
    result.save(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision',type=int,choices=[9],default=9)
    parser.add_argument('--publish-blocked',action='store_true',
                        help='Copy selected Skin evidence only; never implies a Human submission.')
    parser.add_argument('--baseline-directory',type=Path,
                        help='Prior pushed evidence for an explicitly labelled before/after sheet.')
    parser.add_argument('--include-clearance',action='store_true')
    args = parser.parse_args()
    directory = ROOT/'tmp-carol-v008'/('revision-'+str(args.revision))
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
        for col,(label,image) in enumerate([('LOCKED reference',reference),
                                           ('revision '+str(args.revision)+' | same neutral',model),
                                           ('50% overlay',overlay)]):
            x,y = col*size,row*(size+32)
            draw.text((x+10,y+9),key+' | '+label,fill='#242137')
            sheet.paste(background(image).resize((size,size)),(x,y+32))
    sheet.save(directory/'skin-review-sheet.png')
    extra = []
    if args.baseline_directory:
        prior = json.loads((args.baseline_directory/'measurements.json').read_text())
        assert prior['reference_registration'] == data['reference_registration']
        assert prior['reference_hashes'] == data['reference_hashes']
        rows = []
        for view in ['front','side']:
            key = 'skin-'+view
            rows.append([
                (view+' | LOCKED',registered(data['reference_registration'][key],640)),
                (view+' | prior selected '+str(prior['selected_geometry_revision']),args.baseline_directory/(key+'.png')),
                (view+' | selected '+str(data['selected_geometry_revision']),directory/(key+'.png'))])
        comparison_sheet(rows,directory/'skin-before-after.png')
        extra.append('skin-before-after.png')
    if args.include_clearance:
        probes = ROOT/'tmp-carol-v008/clearance-selected'
        report = json.loads((probes/'motion-clearance.json').read_text())
        assert report['neutral_geometry_digest'] == data['geometry_digest']
        for kind,degrees in [('head-yaw',8),('head-pitch',6),('head-roll',5),('ear-sweep',8)]:
            rows = []
            for view in ['front','side']:
                rows.append([
                    (view+' | neutral',directory/('skin-'+view+'.png')),
                    (view+' | '+kind+' -'+str(degrees)+' deg',probes/(kind+'-minus-'+view+'.png')),
                    (view+' | '+kind+' +'+str(degrees)+' deg',probes/(kind+'-plus-'+view+'.png'))])
            filename = 'clearance-'+kind+'.png'
            comparison_sheet(rows,directory/filename)
            extra.append(filename)
        shutil.copy2(probes/'motion-clearance.json',directory/'motion-clearance.json')
        extra.append('motion-clearance.json')
    if args.publish_blocked:
        if data.get('executor_disposition') not in {'BLOCKED_AT_V008_SKIN_REVISION_GATE',
                                                    'BLOCKED_AT_V008_SKIN_FINAL_FIT'}:
            raise RuntimeError('Only an explicitly blocked Skin packet may be published here')
        final = ROOT/'docs/production/carol/evidence/reconstruction-v008'
        final.mkdir(parents=True,exist_ok=True)
        for name in ['skin-front.png','skin-side.png','skin-front-overlay.png',
                     'skin-side-overlay.png','skin-review-sheet.png','measurements.json']+extra:
            shutil.copy2(directory/name,final/name)
    print(directory/'skin-review-sheet.png')


if __name__=='__main__':
    main()
