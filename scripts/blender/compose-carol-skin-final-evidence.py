"""Compose honest, fixed-registration Skin and derived-view review sheets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / 'assets/grimo/source/carol/approved-3d'
OUT = ROOT / 'docs/production/carol/evidence/skin-final-v001'
RENDERS = OUT / 'renders'
WHITE = (255, 255, 255)
font_path = 'C:/Windows/Fonts/segoeui.ttf'
FONT = ImageFont.truetype(font_path, 23)
SMALL = ImageFont.truetype(font_path, 16)


def candidate(name):
    image = Image.open(RENDERS / (name + '.png')).convert('RGBA')
    canvas = Image.new('RGBA', image.size, (*WHITE, 255))
    canvas.alpha_composite(image)
    return canvas.convert('RGB')


def registered(name, size, scale, offset):
    source = Image.open(REF / name).convert('RGBA')
    background = Image.new('RGBA', source.size, (*WHITE, 255))
    background.alpha_composite(source)
    original = background.convert('RGB')
    transformed = original.resize((round(original.width * scale),
                                   round(original.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', size, WHITE)
    canvas.paste(transformed, offset)
    return canvas


def tile(image, size):
    image = image.copy()
    image.thumbnail(size, Image.Resampling.LANCZOS)
    cell = Image.new('RGB', size, WHITE)
    cell.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return cell


def label(draw, x, y, value):
    draw.text((x, y), value, fill=(44, 39, 36), font=FONT)


def skin_comparison():
    front = candidate('front')
    side = candidate('side')
    # Front follows the locked source registration. The refreshed Skin Side
    # canvas has no locked full-body registration: align its visible hoof
    # centers/support length and ground once, then hold that transform for both
    # source and candidate in the overlay. This is a visual diagnostic.
    front_px_per_h = 1200 / 1.23
    fscale = front_px_per_h / 994
    fref = registered('carol_skin_front.png', front.size, fscale,
                      (round(600 - 626.5 * fscale),
                       round(525 + .395 * front_px_per_h - 1075 * fscale)))
    side_px_per_h = 1300 / 1.34
    sscale = side_px_per_h / 1030
    sref = registered('carol_skin_side.png', side.size, sscale,
                      (round(650 - .53 * side_px_per_h - 80 * sscale),
                       round(525 + .395 * side_px_per_h - 946 * sscale)))
    cols = 3
    w, h = 610, 510
    sheet = Image.new('RGB', (cols * w + 60, 2 * (h + 44) + 78), WHITE)
    draw = ImageDraw.Draw(sheet)
    label(draw, 24, 13, 'CAROL / Skin geometry / fixed full-body registration')
    for row, (authority, render, view) in enumerate([(fref, front, 'FRONT'),
                                                       (sref, side, 'SIDE')]):
        images = [authority, render, Image.blend(authority, render, .5)]
        names = ['APPROVED SKIN', 'FINAL 3D CANDIDATE', '50% OVERLAY']
        for col, (im, title) in enumerate(zip(images, names)):
            x = 20 + col * w
            y = 57 + row * (h + 44)
            label(draw, x + 7, y, view + ' / ' + title)
            sheet.paste(tile(im, (w - 12, h - 35)), (x + 6, y + 32))
    draw.text((26, sheet.height - 25),
              'Front: locked 994 px/H. Side: support/ground registration ~1030 px/H; qualitative diagnostic.',
              fill=(92, 82, 78), font=SMALL)
    sheet.save(OUT / 'skin-authority-comparison.png')
    # Enlarged side face retains the same full-body transform and resolution.
    face_box = (70, 145, 760, 690)
    face_sheet = Image.new('RGB', (2070, 625), WHITE)
    d = ImageDraw.Draw(face_sheet)
    label(d, 20, 15, 'SIDE PROFILE / forehead, bridge, muzzle, jaw')
    for col, (im, title) in enumerate([(sref, 'APPROVED SKIN'), (side, 'FINAL 3D CANDIDATE'),
                                        (Image.blend(sref, side, .5), '50% OVERLAY')]):
        x = col * 690
        label(d, x + 15, 50, title)
        face_sheet.paste(im.crop(face_box), (x, 82))
    face_sheet.save(OUT / 'profile-closeup.png')


def spatial_review():
    names = [('front', 'FRONT'), ('three-quarter', 'DERIVED 3/4'),
             ('side', 'SIDE'), ('rear', 'DERIVED REAR'), ('top', 'DERIVED TOP')]
    w, h = 535, 500
    sheet = Image.new('RGB', (w * 3 + 44, h * 2 + 93), WHITE)
    draw = ImageDraw.Draw(sheet)
    label(draw, 24, 12, 'CAROL / one neutral 3D Skin model / spatial review')
    for i, (file, title) in enumerate(names):
        col, row = i % 3, i // 3
        x, y = 17 + col * w, 57 + row * h
        label(draw, x + 6, y, title)
        sheet.paste(tile(candidate(file), (w - 12, h - 41)), (x + 6, y + 32))
    draw.text((30, sheet.height - 23),
              'Rear and top are derived checks, not new approved image authorities. All views use the saved neutral mesh.',
              fill=(92, 82, 78), font=SMALL)
    sheet.save(OUT / 'spatial-review.png')


def normal_context():
    """Keep the fleece-covered Normal artwork visible for identity review."""
    pairs = [('carol_front.png', 'front', 'FRONT'),
             ('carol_side.png', 'side', 'SIDE')]
    w, h = 620, 595
    sheet = Image.new('RGB', (2 * w + 40, 2 * h + 105), WHITE)
    draw = ImageDraw.Draw(sheet)
    label(draw, 24, 13, 'CAROL / approved Normal identity context')
    for row, (source_name, render_name, view) in enumerate(pairs):
        rgba = Image.open(REF / source_name).convert('RGBA')
        backing = Image.new('RGBA', rgba.size, (*WHITE, 255))
        backing.alpha_composite(rgba)
        source = backing.convert('RGB')
        for col, (im, title) in enumerate([(source, 'APPROVED NORMAL'),
                                            (candidate(render_name), 'FINAL SKIN 3D')]):
            x, y = 18 + col * w, 55 + row * h
            label(draw, x + 6, y, view + ' / ' + title)
            sheet.paste(tile(im, (w - 12, h - 43)), (x + 6, y + 32))
    draw.text((27, sheet.height - 27),
              'Qualitative identity check only: Normal artwork has fleece; Skin model does not.',
              fill=(92, 82, 78), font=SMALL)
    sheet.save(OUT / 'normal-identity-context.png')


if __name__ == '__main__':
    skin_comparison()
    spatial_review()
    normal_context()
