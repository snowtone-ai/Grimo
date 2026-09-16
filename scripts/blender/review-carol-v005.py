"""Fixed-registration comparison, not an image-generation or reference-editing tool."""
import runpy, json, sys
from PIL import Image
from pathlib import Path
M=runpy.run_path(str(Path(__file__).with_name('prepare-carol-v005.py')))
OUT=M['OUT']; ROOT=M['ROOT']; board=M['board']
data=json.loads((OUT/'landmark-measurements.json').read_text())
folder=Path(sys.argv[1]) if len(sys.argv)>1 else OUT/'iterations/primary-02'
items=[]
for v in ['front','side','back','top']:
    p=data['plates'][v]; im=Image.open(M['SRC']/'approved-3d'/p['file']).convert('RGBA')
    # All rendered review cameras have 5.8 BU span and the same 1000px resolution.
    scale=1000/(5.8*p['pixels_per_unit']); size=(round(im.width*scale),round(im.height*scale))
    im=im.resize(size,Image.Resampling.LANCZOS)
    ref=Image.new('RGBA',(1000,1000)); u,v0=p['origin_px']
    oy=500 if v=='top' else 500+1.5*1000/5.8
    # Back reference's image-right is world -X. All origins already recorded in image space.
    ref.alpha_composite(im,(round(500-u*scale),round(oy-v0*scale)))
    render=Image.open(folder/f'{v}.png').convert('RGBA')
    white=Image.new('RGBA',(1000,1000),(235,238,244,255))
    a=Image.alpha_composite(white,ref); b=Image.alpha_composite(white,render)
    overlay=Image.blend(a,b,.5); overlay.save(folder/f'{v}-overlay.png')
    items += [(v+' / locked reference',ref),(v+' / geometry',render),(v+' / 50% overlay',overlay)]
board(items,folder/'registered-board.png',cols=3,cell=(480,460))
board([(v,folder/f'{v}.png') for v in ['front','side','back','top','three-quarter']],folder/'board.png')
