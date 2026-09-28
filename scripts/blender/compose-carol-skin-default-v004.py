"""Compose the minimal, unretouched v004 ear review boards."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'docs/production/carol/evidence/skin-default-v004'
SOURCE = ROOT / 'assets/grimo/source/carol'
V003 = ROOT / 'docs/production/carol/evidence/skin-default-v003/new-skin'
V004 = EVIDENCE / 'renders/skin-v004'
FLEECE = EVIDENCE / 'renders/fleece-occlusion'
FONT_PATH = 'C:/Windows/Fonts/arial.ttf'
FONT = ImageFont.truetype(FONT_PATH, 23)
TITLE = ImageFont.truetype(FONT_PATH, 30)


def tile(canvas, draw, col, row, label, path, crop=None, cell=(560, 420),
         margin=58, row_gap=50):
    width, height = cell
    x, y = col * width, margin + row * (height + row_gap)
    draw.text((x + 15, y + 8), label, font=FONT, fill='#353038')
    im = Image.open(path).convert('RGBA')
    if crop:
        im = im.crop(crop)
    scale = min((width - 24) / im.width, (height - 55) / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)),
                   Image.Resampling.LANCZOS)
    white = Image.new('RGBA', im.size, 'white')
    white.alpha_composite(im)
    canvas.paste(white.convert('RGB'),
                 (x + (width - im.width) // 2, y + 43))


def board(name, title, rows, cell=(560, 420)):
    columns = max(len(row) for row in rows)
    width, height = cell
    canvas = Image.new('RGB', (columns * width,
                               58 + len(rows) * (height + 50)), 'white')
    draw = ImageDraw.Draw(canvas)
    draw.text((16, 12), title, font=TITLE, fill='#29242d')
    for row_index, row in enumerate(rows):
        for col_index, (label, path, crop) in enumerate(row):
            tile(canvas, draw, col_index, row_index, label, path, crop, cell)
    canvas.save(EVIDENCE / name, optimize=True)


def view(folder, name):
    return folder / f'{name}.png'


def main():
    board('ear-authority-comparison.png',
          'CAROL / ear authority above, saved v004 Skin below', [
        [
            ('Identity / left ear', SOURCE / 'carol-Identity-canonical.png',
             (272, 246, 399, 374)),
            ('Approved Normal / Front ear',
             SOURCE / 'approved-3d/carol_front.png', (0, 585, 365, 880)),
            ('Approved Normal / Side ear',
             SOURCE / 'approved-3d/carol_side.png', (470, 490, 795, 740)),
        ],
        [
            ('v004 Skin / Front', view(V004, 'front'), (165, 100, 600, 455)),
            ('v004 Skin / Side', view(V004, 'side'), (185, 95, 585, 490)),
            ('v004 Skin / front 3Q', view(V004, 'front-3q'),
             (115, 100, 680, 500)),
            ('v004 ear / Top diagnostic', view(V004, 'ear-top'), None),
        ],
    ], (500, 380))

    board('ear-v003-vs-v004.png',
          'CAROL / matched camera and light / v003 above, v004 below', [
        [
            ('v003 / Front', view(V003, 'front'), (165, 100, 600, 455)),
            ('v003 / Side detail', view(V003, 'ear-side'), None),
            ('v003 / Top detail', view(V003, 'ear-top'), None),
        ],
        [
            ('v004 / Front', view(V004, 'front'), (165, 100, 600, 455)),
            ('v004 / Side detail', view(V004, 'ear-side'), None),
            ('v004 / Top detail', view(V004, 'ear-top'), None),
        ],
    ], (560, 430))

    board('fleece-occlusion.png',
          'CAROL / refined v004 Skin ears under unchanged v004 Fleece', [[
        ('Front', view(FLEECE, 'front'), None),
        ('front 3Q', view(FLEECE, 'front-3q'), None),
        ('Side', view(FLEECE, 'side'), None),
    ]], (600, 480))

    board('skin-v003-vs-v004.png',
          'CAROL / full standalone Skin / v003 above, v004 below', [
        [
            ('v003 / Front', view(V003, 'front'), None),
            ('v003 / front 3Q', view(V003, 'front-3q'), None),
            ('v003 / Side', view(V003, 'side'), None),
        ],
        [
            ('v004 / Front', view(V004, 'front'), None),
            ('v004 / front 3Q', view(V004, 'front-3q'), None),
            ('v004 / Side', view(V004, 'side'), None),
        ],
    ], (600, 500))


if __name__ == '__main__':
    main()
