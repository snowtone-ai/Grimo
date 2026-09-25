"""Compose review boards from untouched renders; no retouch or shape warping."""
import importlib.util
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('boards', Path(__file__).with_name('compose-carol-skin-final-evidence.py'))
B = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(B)
B.OUT = ROOT / 'docs/production/carol/evidence/skin-final-v002'
B.RENDERS = B.OUT / 'renders'
BEFORE = ROOT / 'docs/production/carol/evidence/skin-final-v001/renders'


def verify_render_set():
    asset = ROOT / 'assets/grimo/production/carol/blender/carol-skin-final-v002.blend'
    report = json.loads((B.OUT / 'validation.json').read_text())
    assert hashlib.sha256(asset.read_bytes()).hexdigest() == report['saved_asset_sha256']
    for name in ['front', 'side', 'three-quarter', 'rear', 'top', 'head-front', 'head-side', 'head-three-quarter']:
        path = B.RENDERS / (name + '.png')
        assert path.stat().st_mtime >= asset.stat().st_mtime, 'Stale render: ' + name
        with Image.open(path) as im:
            im.verify()
    return report['saved_asset_sha256']


def rgb(path):
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, 'white')
    bg.alpha_composite(im)
    return bg.convert('RGB')


def before_after():
    w, h = 600, 550
    sheet = Image.new('RGB', (w * 2 + 40, h * 3 + 105), 'white')
    draw = ImageDraw.Draw(sheet)
    B.label(draw, 24, 12, 'CAROL / v001 to v002 / identical cameras and image scale')
    for row, name in enumerate(['front', 'side', 'three-quarter']):
        for col, (path, label) in enumerate([(BEFORE / (name + '.png'), 'BEFORE v001'),
                                            (B.RENDERS / (name + '.png'), 'HEAD-REFINED v002')]):
            x, y = 20 + col * w, 55 + row * h
            B.label(draw, x + 8, y, name.upper() + ' / ' + label)
            sheet.paste(B.tile(rgb(path), (w - 16, h - 42)), (x + 8, y + 35))
    draw.text((25, sheet.height - 30), 'Material and environment fill also refined. Geometry-only comparison is provided separately.',
              fill=(92, 82, 78), font=B.SMALL)
    sheet.save(B.OUT / 'before-after.png')


def head_detail():
    w, h = 750, 755
    sheet = Image.new('RGB', (w * 3 + 40, h + 100), 'white')
    draw = ImageDraw.Draw(sheet)
    B.label(draw, 24, 12, 'CAROL / head refinement / one saved neutral 3D candidate')
    for col, name in enumerate(['front', 'side', 'three-quarter']):
        x, y = 20 + col * w, 56
        B.label(draw, x + 8, y, name.upper())
        sheet.paste(B.tile(B.candidate('head-' + name), (w - 16, h - 40)), (x + 8, y + 35))
    draw.text((25, sheet.height - 28), 'Close cameras include surrounding geometry. Cropped ear tips here: inspect full-body / spatial boards for complete ears.',
              fill=(92, 82, 78), font=B.SMALL)
    sheet.save(B.OUT / 'head-detail.png')


def matched_geometry():
    w, h = 680, 575
    sheet = Image.new('RGB', (w * 2 + 40, h * 2 + 105), 'white')
    draw = ImageDraw.Draw(sheet)
    B.label(draw, 24, 12, 'CAROL / geometry comparison / matching v002 materials, lighting and cameras')
    for row, name in enumerate(['front', 'side']):
        for col, (path, label) in enumerate([(B.OUT / 'matched-source-renders' / (name + '.png'), 'v001 GEOMETRY'),
                                            (B.RENDERS / (name + '.png'), 'v002 GEOMETRY')]):
            x, y = 20 + col * w, 55 + row * h
            B.label(draw, x + 8, y, name.upper() + ' / ' + label)
            sheet.paste(B.tile(rgb(path), (w - 16, h - 42)), (x + 8, y + 35))
    draw.text((25, sheet.height - 30), 'Source geometry is unchanged. Source blush remains at its original facial position. No image warping.',
              fill=(92, 82, 78), font=B.SMALL)
    sheet.save(B.OUT / 'matched-geometry-comparison.png')


if __name__ == '__main__':
    asset_hash = verify_render_set()
    B.skin_comparison()
    B.spatial_review()
    B.normal_context()
    before_after()
    head_detail()
    matched_geometry()
    files = {str(p.relative_to(B.OUT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(B.OUT.rglob('*.png'))}
    (B.OUT / 'evidence-manifest.json').write_text(json.dumps({'saved_asset_sha256': asset_hash,
        'all_final_renders_newer_than_saved_asset': True, 'png_sha256': files}, indent=2) + '\n')
