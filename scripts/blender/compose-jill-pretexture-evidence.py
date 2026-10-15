"""Compose labelled boards from actual renders; no image synthesis or retouch."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'docs/production/jill/rig-pretexture-v002'

def board(paths, output, columns, size):
    cell_h = size + 30
    result = Image.new('RGB', (size * columns, cell_h * ((len(paths) + columns - 1) // columns)), '#eef0e9')
    draw = ImageDraw.Draw(result)
    for i, path in enumerate(paths):
        im = Image.open(path).convert('RGB')
        im.thumbnail((size, size))
        x, y = (i % columns) * size, (i // columns) * cell_h
        result.paste(im, (x + (size-im.width)//2, y + (size-im.height)//2))
        draw.text((x+5, y+size+6), path.stem, fill='#17221a')
    result.save(E / output, quality=92)

board(sorted((E/'renders').glob('uv-*.png')), '05-uv-checker.jpg', 4, 360)
board([E/'renders'/f'{case}-{phase}-{view}.png'
       for case in ['wing-R', 'paw-R', 'tail-leaves', 'combined-R']
       for phase in ['half', 'peak', 'return'] for view in ['front', 'side', '3q']],
      '06-other-motion-review.jpg', 6, 280)
