"""Write a local, file:// compatible diagnostic review from measured evidence."""
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/hero-modules-v003'
validation=json.loads((OUT/'validation.json').read_text(encoding='utf8'))
fit=json.loads((OUT/'fit-metrics.json').read_text(encoding='utf8'))
history=json.loads((OUT/'fit-history.json').read_text(encoding='utf8'))


def esc(x):return html.escape(str(x))
def picture(path,caption):
    return f'<figure><img src="{esc(path)}" alt="{esc(caption)}" loading="lazy"><figcaption>{esc(caption)}</figcaption></figure>'
def row(a,b):return f'<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>'


sections=[]
for module in ('ear','hoof'):
    views=[]
    for view in ('front','side','top','3q'):
        score=fit['modules'][module][view]['normalized_silhouette_iou']
        views.append(f'''<article class="view"><h3>{view.upper()} · IoU {score:.4f}</h3><div class="triptych">
        {picture(f'{module}-{view}-reference.png','Approved reference')}
        {picture(f'{module}-{view}-candidate.png','v003 candidate')}
        {picture(f'{module}-{view}-overlay.png','Reference coral · candidate teal · overlap charcoal')}
        </div></article>''')
    sections.append(f'<section id="{module}"><h2>{module.title()} · localized authority</h2>{"".join(views)}</section>')

integrated=''.join(picture(f'carol-{view}.png',view.replace('-',' ').title())
                   for view in ('front','side','3q-left','3q-right'))
eyes=''.join(picture(f'eye-{view}.png',view.replace('-',' ').title())
             for view in ('front','3q-left','3q-right','side'))

eye=validation['eye_metrics']
left=eye['raycast_visible_front']['L']
ear=fit['modules']['ear'];hoof=fit['modules']['hoof']
summary=[
    ('Disposition','STALLED_PARAMETERIZATION · executor precheck rejects Human handoff'),
    ('Ear Front / Side / Top / 3Q IoU',' / '.join(f"{ear[v]['normalized_silhouette_iou']:.4f}" for v in ('front','side','top','3q'))),
    ('Ear front centerline angle',f"{validation['ear_angle_degrees']:.2f}° · intended ~18°"),
    ('Hoof Front / Side / Top / 3Q IoU',' / '.join(f"{hoof[v]['normalized_silhouette_iou']:.4f}" for v in ('front','side','top','3q'))),
    ('Hoof width / visible crown',f"{validation['hoof_visible_width_H']:.4f} H / {validation['hoof_visible_crown_H']:.4f} H"),
    ('Visible Front eye aperture',f"{left['width_H']:.4f} × {left['height_H']:.4f} H · center Y {left['center_y_H']:.5f} H"),
    ('Eye relief / Side silhouette bulge',f"{eye['central_relief_H']:.4f} H / {eye['side_silhouette_bulge_H']:.4f} H"),
    ('Convergence',f"Ear {len(history['rounds']['ear'])} final-basis rounds, {history['stop']['ear']}; Hoof {len(history['rounds']['hoof'])} final-basis rounds, {history['stop']['hoof']}"),
    ('Frozen objects',f"{validation['frozen_objects']['count']} unchanged after save/reload"),
    ('Source / candidate SHA-256',f"{validation['source_blend_sha256']} / {validation['output_blend_sha256']}"),
    ('Parameter SHA-256',validation['parameter_file_sha256']),
]
table='<table>'+''.join(row(*r) for r in summary)+'</table>'

page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">
<title>Carol v003 · diagnostic geometry review</title>
<style>
:root{{--paper:#f8f6f1;--ink:#27242a;--muted:#68656b;--line:#ded9d1;--coral:#f57e66;--teal:#2caaa4}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.48 system-ui,sans-serif}}
main{{max-width:1450px;margin:auto;padding:24px clamp(16px,3vw,44px) 90px}}h1,h2{{font-family:Georgia,serif;line-height:1.08}}h1{{font-size:clamp(2rem,4vw,3.8rem);margin:.15em 0}}h2{{font-size:2rem}}
p{{max-width:900px}}.eyebrow{{font-size:.75rem;font-weight:800;letter-spacing:.14em;color:#895c45}}.flag{{display:inline-block;padding:6px 12px;border-radius:99px;background:#ffe9d7;color:#8c380f;font-weight:800;font-size:.8rem}}
nav{{display:flex;gap:18px;flex-wrap:wrap;margin:28px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:12px 0}}a{{color:#874b31}}
section{{margin-top:48px}}.view{{margin:18px 0;padding:18px;background:#fff;border:1px solid var(--line);border-radius:16px}}
.triptych{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}
figure{{margin:0;min-width:0}}img{{display:block;width:100%;aspect-ratio:1;object-fit:contain;background:#eee9e2;border-radius:9px}}.grid img{{aspect-ratio:4/3}}figcaption{{font-size:.82rem;color:var(--muted);padding:6px 2px}}
table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{padding:10px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;overflow-wrap:anywhere}}th{{width:27%;color:#5d5550}}
.note{{border-left:4px solid #d99749;background:#fff5e7;padding:14px 18px}}
@media(max-width:800px){{.triptych{{grid-template-columns:1fr 1fr}}.triptych figure:last-child{{grid-column:1/-1}}.grid{{grid-template-columns:1fr}}th,td{{display:block;width:100%}}}}
</style></head><body><main><div class="eyebrow">CAROL / LOCAL EXECUTOR DIAGNOSTIC</div><h1>Hero geometry v003</h1>
<span class="flag">STALLED_PARAMETERIZATION · NOT A HUMAN GEOMETRY PASS</span>
<p>The Front eye opening is preserved and the Side cap is shallow. The ear and hoof still differ visibly from their approved local sheets. This page exposes those differences; it is not a request to approve the current geometry.</p>
<nav><a href="#integrated">Integrated Carol</a><a href="#eye">Eye closeups</a><a href="#ear">Ear</a><a href="#hoof">Hoof</a><a href="#numbers">Numbers</a></nav>
<section id="integrated"><h2>Integrated Carol</h2><div class="grid">{integrated}</div></section>
<section id="eye"><h2>Eye and socket · closeups</h2><div class="grid">{eyes}</div></section>
{''.join(sections)}
<section id="numbers"><h2>Measurements and provenance</h2>{table}
<p class="note">Silhouette IoU centers each isolated contour and applies one uniform scale per view. It does not register the artwork to H space. The 3Q panels validate the shared 3D form. The pale hoof helper stub is excluded from the reference mask; Top candidate shows the hoof itself so the unchanged forelimb cannot hide its contour. The integrated images show the true limb attachment. A single stray shading pixel is removed from hoof masks before bounding-box normalization.</p>
<p><a href="validation.json">Post-reload validation</a> · <a href="fit-metrics.json">Per-view fit</a> · <a href="fit-history.json">Convergence history</a> · <a href="README.md">Diagnostic notes</a></p></section>
</main></body></html>'''
(OUT/'review.html').write_text(page,encoding='utf8')
print(OUT/'review.html')
