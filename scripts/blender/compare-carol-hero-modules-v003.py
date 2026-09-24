"""Generate honest, normalized silhouette comparisons for the two module sheets.

Run with system Python + Pillow after the Blender builder. The sheets provide
view-specific artwork without pixel/world registration, so this reports a
shape-only diagnostic, never a production geometry PASS by itself.
"""
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageOps, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/production/carol/evidence/hero-modules-v003'
REFS = {
    'ear': ROOT / 'assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.png',
    'hoof': ROOT / 'assets/grimo/source/carol/approved-3d/modules/carol-hoof-module-authority.png',
}
VIEWS = {'front': (0,0), 'side': (1,0), 'top': (0,1), '3q': (1,1)}
SIZE = 512
SPAN = 440


def reference_mask(image, module):
    # Saturated brown / pink geometry only. White ground, grey shadow and
    # pale helper stubs are excluded from the comparison.
    rgb = image.convert('RGB')
    mask = Image.new('L', rgb.size, 0)
    a = mask.load()
    p = rgb.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r,g,b = p[x,y]
            hi,lo = max(r,g,b),min(r,g,b)
            sat = (hi-lo)/max(1,hi)
            if sat > .17 and lo < 220 and r > g*1.28 and (module!='hoof' or r<220):
                a[x,y] = 255
    return mask


def normalize(mask):
    box = mask.getbbox()
    if not box:
        raise ValueError('empty silhouette')
    crop = mask.crop(box)
    scale = SPAN/max(crop.size)
    shape = crop.resize((round(crop.width*scale),round(crop.height*scale)), Image.Resampling.BILINEAR)
    square = Image.new('L',(SIZE,SIZE))
    square.paste(shape, ((SIZE-shape.width)//2,(SIZE-shape.height)//2))
    return square, {'bbox_pixels':list(box),'aspect_width_over_height':round(crop.width/crop.height,4)}


def candidate_hoof_mask(image):
    mask=Image.new('L',image.size)
    out=mask.load(); pixels=image.load()
    for y in range(image.height):
        for x in range(image.width):
            r,g,b,a=pixels[x,y]
            if a>128 and r<190 and r>g*1.15 and g>b*1.02:
                out[x,y]=255
    # Isolated shading/antialias pixels above the hoof must not stretch the
    # normalization box (one such pixel distorted the v002 Side score).
    return mask.filter(ImageFilter.MedianFilter(size=3))


def iou(a,b):
    x = a.point(lambda v:255 if v>=128 else 0)
    y = b.point(lambda v:255 if v>=128 else 0)
    intersection = ImageChops.multiply(x,y)
    union = ImageChops.lighter(x,y)
    ia = sum(intersection.histogram()[128:])
    ua = sum(union.histogram()[128:])
    return round(ia/ua,4)


def overlay(a,b):
    a=a.point(lambda v:255 if v>=128 else 0)
    b=b.point(lambda v:255 if v>=128 else 0)
    out = Image.new('RGB',(SIZE,SIZE),'white')
    pixels=out.load(); ap=a.load();bp=b.load()
    for y in range(SIZE):
        for x in range(SIZE):
            if ap[x,y] and bp[x,y]: pixels[x,y]=(69,81,86)
            elif ap[x,y]: pixels[x,y]=(245,126,102)
            elif bp[x,y]: pixels[x,y]=(44,170,164)
    return out


def main():
    metrics={'method':'Saturated approved module pixels versus ear candidate alpha or exposed brown hoof pixels with the frozen forelimb in Front/Side/3Q. Each silhouette is uniformly scaled to the same 440px longest axis and centered. Top candidates are rotated into each sheet presentation axis. This is shape-only: source sheets have no world-space registration. Pale helper stubs and shadows are excluded. Reference coral; candidate teal; overlap charcoal.',
             'target_iou_primary':.90,'target_iou_mean':.93,'target_iou_3q':.90,'modules':{}}
    for module, path in REFS.items():
        original=Image.open(path)
        original.load()
        assert original.size==(1254,1254)
        module_data={}
        for view,(col,row) in VIEWS.items():
            box=(col*627,row*627,(col+1)*627,(row+1)*627)
            panel=original.crop(box)
            panel.save(OUT/f'{module}-{view}-reference.png')
            ref,ref_info=normalize(reference_mask(panel,module))
            candidate=Image.open(OUT/f'{module}-{view}-candidate.png').convert('RGBA')
            if module=='ear' and view=='top':
                # The authority sheet lays the lateral axis horizontally;
                # Blender's top camera has it vertically. This is only a
                # presentation-axis registration, not a per-view mesh change.
                candidate=ImageOps.flip(candidate.rotate(90))
            if module=='hoof' and view=='top':
                # v002 compared a left-facing toe to a down-facing reference.
                candidate=candidate.rotate(90)
            cand_mask = (candidate_hoof_mask(candidate) if module=='hoof'
                         else candidate.getchannel('A'))
            cand,cand_info=normalize(cand_mask)
            overlay(ref,cand).save(OUT/f'{module}-{view}-overlay.png')
            module_data[view]={'normalized_silhouette_iou':iou(ref,cand),
                               'reference':ref_info,'candidate':cand_info,
                               'aspect_ratio_error_fraction':round(abs(cand_info['aspect_width_over_height']/ref_info['aspect_width_over_height']-1),4)}
        metrics['modules'][module]=module_data
    (OUT/'fit-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf8')
    print(json.dumps(metrics['modules'],indent=2))


if __name__=='__main__':
    main()
