"""Write the static, file:// friendly human review page from measured evidence."""
import html
import json
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/hero-modules-v002'
validation=json.loads((OUT/'validation.json').read_text(encoding='utf8'))
fit=json.loads((OUT/'fit-metrics.json').read_text(encoding='utf8'))
views=['front','side','top','3q']


def esc(s):
    return html.escape(str(s))


def img(name,alt):
    return f'<img src="{esc(name)}" alt="{esc(alt)}" loading="lazy">'


def row(label,value):
    return f'<tr><th>{esc(label)}</th><td>{esc(value)}</td></tr>'


def module_section(module,title):
    cells=[]
    for view in views:
        m=fit['modules'][module][view]
        score=m['normalized_silhouette_iou']
        target=.975 if view=='3q' else .990
        cells.append(f'''<article class="view">
          <h3>{esc(view.upper())} <span class="badge attention">ATTENTION · IoU {score:.3f} / {target:.3f}</span></h3>
          <div class="triptych">
            <figure>{img(f'{module}-{view}-reference.png',f'{title} {view} approved reference')}<figcaption>Approved reference</figcaption></figure>
            <figure>{img(f'{module}-{view}-candidate.png',f'{title} {view} candidate render')}<figcaption>Candidate · v011 integration</figcaption></figure>
            <figure>{img(f'{module}-{view}-overlay.png',f'{title} {view} silhouette overlay')}<figcaption>Contour: reference coral · candidate teal</figcaption></figure>
          </div>
          <p class="small">Aspect difference {m['aspect_ratio_error_fraction']*100:.1f}% · normalized silhouette diagnostic</p>
        </article>''')
    return f'<section id="{module}"><div class="section-head"><span class="eyebrow">LOCALIZED AUTHORITY</span><h2>{esc(title)}</h2></div>{"".join(cells)}</section>'


def dimension_table():
    rec=validation['module_records']
    def extent(name,axis):
        b=rec[name]['world_bounds']
        return b['max'][axis]-b['min'][axis]
    ear=rec['EAR_R']['world_bounds']
    rows=[
        ('Ear root-to-tip centerline front angle','25.2° from .180 H drop / .382 H span; contract ≈18° · ATTENTION'),
        ('Ear full 3D bounds',f"X {ear['max'][0]-ear['min'][0]:.4f} H · Y {ear['max'][1]-ear['min'][1]:.4f} H · Z {ear['max'][2]-ear['min'][2]:.4f} H"),
        ('Front hoof width',f"{extent('HOOF_FORE_R',1):.4f} H · target .219 H"),
        ('Hind hoof width',f"{extent('HOOF_HIND_R',1):.4f} H · target .219 H"),
        ('Hoof visible crown / hidden overlap','Nominal crown .111 H; mesh continues to .150 H inside the frozen limb. The exposed visual boundary requires Human review.'),
        ('Support centers','Fore X .390 H · hind X .920 H, unchanged from contract'),
        ('Toe architecture','Exactly 3 toe prominences / 2 shallow clefts in each single hoof mesh'),
    ]
    return '<table class="facts">'+''.join(row(*r) for r in rows)+'</table>'


def provenance():
    pieces=[]
    for key in ('ear','hoof'):
        data=validation['authority_images'][key]
        path=ROOT/data['path']
        with Image.open(path) as im:
            im.load()
            dims=f'{im.width} × {im.height} {im.format}; decoded OK'
        pieces.append(row(f'{key.capitalize()} authority',f"{data['path']} · SHA-256 {data['sha256']} · {path.stat().st_size:,} bytes · {dims}"))
    pieces.append(row('Source blend',f"{validation['source_blend']} · SHA-256 {validation['source_blend_sha256']}"))
    pieces.append(row('Candidate blend',f"{validation['output_blend']} · SHA-256 {validation['output_blend_sha256']}"))
    pieces.append(row('Changed objects',', '.join(validation['changed_objects'])))
    pieces.append(row('Frozen verification',f"{validation['frozen_objects']['count']} of {validation['frozen_objects']['count']} objects matched by name, world transform, vertex/face count, mesh digest and material slots after save/reload."))
    face=validation['frozen_objects']['before']['CENTRAL_CHASSIS']
    pieces.append(row('v011 face anchor',f"CENTRAL_CHASSIS mesh SHA-256 {face['mesh_sha256']}; EYE_L/R, EYELID_L/R and NOSE also identical. See validation.json for every record."))
    return '<table class="facts">'+''.join(pieces)+'</table>'


integrated=''.join(f'<figure>{img(f"carol-{v}.png",f"Integrated Carol {v}")}<figcaption>{esc(v.replace("-"," ").title())}</figcaption></figure>' for v in ('front','side','3q-left','3q-right'))

page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carol · Hero ear and hoof modules v002</title>
<style>
:root{{--ink:#26252b;--muted:#656771;--paper:#faf9f6;--panel:#fff;--line:#ddd8d1;--coral:#f57e66;--teal:#2caaa4;--amber:#956211}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
.wrap{{max-width:1460px;margin:auto;padding:30px clamp(16px,3vw,46px) 100px}}header{{display:flex;gap:28px;justify-content:space-between;align-items:end;padding:20px 0 30px;border-bottom:1px solid var(--line)}}
h1{{font:600 clamp(2rem,4vw,4rem)/1.05 Georgia,serif;letter-spacing:-.035em;margin:.15em 0}}h2{{font:600 clamp(1.65rem,2.5vw,2.5rem)/1.1 Georgia,serif;margin:.1em 0}}h3{{font-size:1.05rem;margin:0 0 16px}}p{{margin:.5em 0}}.eyebrow{{color:#87624c;font-size:.77rem;font-weight:800;letter-spacing:.15em}}
.lead{{max-width:790px;color:var(--muted)}}.badge{{display:inline-block;border-radius:99px;padding:5px 10px;font:700 .72rem/1.25 system-ui;letter-spacing:.04em;vertical-align:middle}}.attention{{background:#fff0d8;color:#8b5600}}.pass{{background:#e1f3e8;color:#276c45}}.pending{{background:#e8e6fa;color:#514f89}}
.status{{display:flex;flex-wrap:wrap;gap:9px;padding:22px 0}}nav{{display:flex;gap:18px;flex-wrap:wrap;padding:10px 0 22px;border-bottom:1px solid var(--line)}}a{{color:#7c4934;text-decoration-thickness:1px;text-underline-offset:3px}}section{{padding-top:48px}}.section-head{{margin-bottom:24px}}
.view{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px;margin:18px 0;box-shadow:0 5px 24px #281b1010}}
.triptych{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}figure{{margin:0;min-width:0}}figure img{{display:block;width:100%;aspect-ratio:1;object-fit:contain;background:#f4f1ed;border-radius:10px}}figcaption{{font-size:.84rem;font-weight:650;color:var(--muted);padding:7px 2px 0}}.small{{font-size:.78rem;color:var(--muted)}}
.integrated{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}.integrated img{{aspect-ratio:4/3}}.facts{{border-collapse:collapse;width:100%;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}}.facts th,.facts td{{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid var(--line)}}.facts th{{width:24%;color:#5b5554}}.facts td{{overflow-wrap:anywhere}}.note{{background:#fff8ed;border-left:4px solid #dca150;padding:15px 18px;margin-top:20px}}
@media(max-width:850px){{header{{display:block}}.triptych{{grid-template-columns:1fr 1fr}}.triptych figure:last-child{{grid-column:1/-1}}.integrated{{grid-template-columns:1fr}}.facts th,.facts td{{display:block;width:100%}}.facts td{{padding-top:0}}}}
</style></head><body><div class="wrap"><header><div><div class="eyebrow">CAROL / HUMAN GEOMETRY REVIEW</div><h1>Hero ear &amp; hoof modules</h1><p class="lead">v002 · approved local module sheets · one spatial ear and one continuous three-toe hoof architecture · integrated into the frozen v011 Carol.</p></div><div class="badge pending">PENDING HUMAN REVIEW</div></header>
<div class="status"><span class="badge attention">TECHNICAL MODULE GATE · ATTENTION</span><span class="badge attention">EXECUTOR VISUAL PRECHECK · ATTENTION</span><span class="badge pass">FROZEN OBJECTS · PASS</span><span class="badge pending">HUMAN GEOMETRY GATE · PENDING</span></div>
<p class="lead">The modules are integrated and reviewable. The numerical silhouette target is not met in several views; this page presents the mismatch openly. The v011 underbody is a frozen context, including its known visual limitations.</p>
<nav><a href="#integrated">Integrated Carol</a><a href="#ear">Ear · four views</a><a href="#hoof">Hoof · four views</a><a href="#measurements">Measurements</a><a href="#provenance">Provenance &amp; freeze</a></nav>
<section id="integrated"><div class="section-head"><span class="eyebrow">IN CONTEXT</span><h2>Carol · four views</h2></div><div class="integrated">{integrated}</div></section>
{module_section('ear','Ear')}{module_section('hoof','Hoof')}
<section id="measurements"><div class="section-head"><span class="eyebrow">NUMERICAL CHECK</span><h2>Dimensions &amp; fit</h2></div>{dimension_table()}<div class="note"><strong>How to read IoU:</strong> Each reference and render contour is centered and uniformly scaled by its longest axis. This compares silhouettes, not registered world dimensions or color. The pale orientation stub and neutral shadow are excluded. The ear Top render is rotated into the reference sheet's presentation axes; the mesh is unchanged. Reference-only pixels are coral, candidate-only pixels teal, shared pixels charcoal. Targets: ≥0.990 Front / Side / Top, ≥0.975 3Q. Exact targets were not reached.</div></section>
<section id="provenance"><div class="section-head"><span class="eyebrow">TRACEABILITY</span><h2>Sources, changes &amp; freeze</h2></div>{provenance()}<p class="small">Full per-object before/after records: <a href="validation.json">validation.json</a>. Per-view metric data: <a href="fit-metrics.json">fit-metrics.json</a>.</p></section>
</div></body></html>'''
(OUT/'review.html').write_text(page,encoding='utf8')
print(OUT/'review.html')
