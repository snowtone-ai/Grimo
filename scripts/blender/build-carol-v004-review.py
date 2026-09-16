"""Compose reproducible evidence from actual renders/captures with Pillow.

No repainting or generated artwork. Crops, guides and a labeled 50% overlay
are diagnostics; presentation boards contain unretouched image pixels.
"""
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/blockout-v004'
HIST=Path(tempfile.gettempdir())/'carol-v004-historical-15bfa8e'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
DATA=json.loads((ROOT/'scripts/blender/carol-v004-reference-data.json').read_text())

def read(path):
    im=Image.open(path).convert('RGBA')
    bg=Image.new('RGBA',im.size,'#edf0f5');bg.alpha_composite(im)
    return bg.convert('RGB')

def board(items,name,title,cols=4,cell=(450,420),subtitle='Unretouched captures. Diagnostic materials are not production materials.'):
    cw,ch=cell; rows=(len(items)+cols-1)//cols
    canvas=Image.new('RGB',(cols*cw,90+rows*ch),'#edf0f5');d=ImageDraw.Draw(canvas)
    d.text((20,16),title,font=FONT,fill='#253147');d.text((20,52),subtitle,font=SMALL,fill='#4d5970')
    for i,(label,im) in enumerate(items):
        x=i%cols*cw;y=90+i//cols*ch
        d.text((x+16,y+12),label,font=FONT,fill='#253147')
        im=im.copy();im.thumbnail((cw-24,ch-55),Image.Resampling.LANCZOS)
        canvas.paste(im,(x+(cw-im.width)//2,y+46+(ch-55-im.height)//2))
    canvas.save(OUT/name)

sources=[('Canonical',read(OUT/'canonical-benchmark-front.png')),
         ('Historical / painted',read(OUT/'historical-benchmark-neutral-front.png')),
         ('v003 / diagnostic',read(OUT/'v003-benchmark-front.png')),
         ('v004 / diagnostic',read(OUT/'v004-benchmark-front.png'))]
faceboxes=[(510,416,866,672)]*2+[(372,466,728,722)]+[(510,416,866,672)]
faces=[(label,im.crop(box)) for (label,im),box in zip(sources,faceboxes)]
board(faces,'carol-v004-face-comparison.png','CAROL / face identity comparison',cell=(440,350),
      subtitle='Same pixel scale and crop size; v003 crop translated to its face center. Posed-to-neutral interpretation remains open.')
ears=[]
boxes={'left':[(387,514,567,644)]*2+[(207,491,387,621)]+[(387,514,567,644)],
       'right':[(785,406,965,536)]*2+[(713,491,893,621)]+[(785,406,965,536)]}
for side in ('left','right'):
    ears += [(label+' / '+side,im.crop(box)) for (label,im),box in zip(sources,boxes[side])]
board(ears,'carol-v004-ear-comparison.png','CAROL / independent left and right ear traces',cell=(440,260),
      subtitle='Same pixel scale. Compare root, pointed end, angle, inner-ear area and fleece occlusion.')
board([(label,im.crop((170,190,925,780))) for label,im in sources],
      'carol-v004-fleece-comparison.png','CAROL / fleece hierarchy comparison',cell=(450,440),
      subtitle='Historical fleece includes painted details. v003 and v004 contain no source-image texture.')
board([(label,im.crop((0,48,1100,948))) for label,im in sources],
      'carol-v004-review-board.png','CAROL v004 / source-registered orthographic comparison / HUMAN GATE PENDING',
      cell=(450,450),subtitle='One fixed diagnostic camera and source-space registration; no per-model framing adjustment.')
views=('front-perspective','front-orthographic','three-quarter','side','back','silhouette','clay')
board([(v,read(OUT/f'carol-v004-{v}.png')) for v in views]+
      [('v003 / side',read(OUT.parent/'blockout-v003/carol-v003-side.png')),
       ('v003 / back',read(OUT.parent/'blockout-v003/carol-v003-back.png'))],
      'carol-v004-geometry-board.png','CAROL v004 / geometry truth / unchanged v003 review cameras',cols=3,cell=(550,500),
      subtitle='Untextured diagnostic shading; all materials overridden for clay and silhouette. No Human pass implied.')
iterations=[]
for i in (1,2,3):
    for v in ('front-perspective','side','back'):
        p=ROOT/f'artifacts/carol-v004/loop{i}/carol-v004-{v}.png'
        iterations.append((f'Loop {i} / '+v,read(p)))
board(iterations,'carol-v004-iteration-board.png','CAROL v004 / three observed geometry iterations',cols=3,cell=(550,450))

# Historical close-ups preserve the pre-modeling page capture, not a recreation.
direct=read(OUT/'historical-page-front.png')
for label,box in {'face':(565,452,882,690),'left-ear':(427,543,573,669),
                  'right-ear':(843,435,974,545),'fleece':(268,212,890,558)}.items():
    direct.crop(box).save(OUT/f'historical-page-{label}-closeup.png')

def screen(x,y):return (83.44+1.44*x,202+1.4*y)
guides=[]
for label,im in (sources[0],sources[3]):
    im=im.copy();d=ImageDraw.Draw(im)
    for name,color in [('FACE','#ff3b57'),('EAR_L','#24b8db'),('EAR_R','#24b8db'),('BODY_OUTLINE','#cc64e6')]:
        points=[screen(*p) for p in DATA[name]];d.line(points+[points[0]],fill=color,width=2)
    for x,y in DATA['eye_centers']+DATA['features']['earRoots']:
        sx,sy=screen(x,y);d.ellipse((sx-5,sy-5,sx+5,sy+5),outline='#ed245e',width=2)
    guides.append((label+' / source guides',im.crop((170,190,950,790))))
overlay=Image.blend(sources[0][1],sources[3][1],.5).crop((170,190,950,790))
board(guides+[('50% canonical + v004 overlay',overlay)],'carol-v004-front-overlay.png',
      'CAROL / registered outline and landmark diagnostic',cols=3,cell=(550,490),
      subtitle='Magenta: BODY outline. Red: FACE and landmarks. Cyan: ears. Lines are targets, not claimed visible contour matches.')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=['scripts/grimo/build-carol-reference.py','scripts/grimo/build-carol-3d.py',
       'src/components/grimo/carol-3d-screen.tsx','src/components/grimo/carol-review-controls.tsx',
       'src/components/grimo/carol-3d-world.ts','public/grimo/carol-3d/carol.glb','assets/grimo/source/carol-transparent.png']
provenance={
 'label':'user-designated historical visual benchmark','repository':'snowtone-ai/grimoire',
 'branch':'codex/restore-carol-3d-check','commit':'15bfa8e4c3a8ba24c246fe806bd125b307d8f076',
 'exactFinalAcceptedBinaryProven':False,'sourceFiles':{p:sha(HIST/p) for p in paths},
 'builderUsedAsBlueprint':'scripts/grimo/build-carol-reference.py',
 'genericContrastOnly':'scripts/grimo/build-carol-3d.py',
 'historicalGLB':'public/grimo/carol-3d/carol.glb',
 'directCapture':{'url':'http://localhost:3000/plant/carol-3d','localCheckout':'task-plant-carol3d',
  'files':['historical-page-front.png','historical-page-original.png','historical-page-slight-three-quarter.png'],
  'capturedBeforeModeling':True,'closeups':'Crops of the original pre-modeling front screenshot.',
  'slightYawRadians':.12,'renderer':{'camera':'Orthographic','alpha':False,'exposure':1.15,'toneMapping':'ACESFilmic',
  'output':'sRGB','hemisphere':['#eff3ff','#afa6c2',1.5],'key':['#fff1db',2,[-3,6,5]],'rim':['#c2ceff',2,[3,3,-4]],
  'materialToneMapped':False,'scaleFormula':'No model scale normalization; source geometry uses .007 BU/pixel. halfHeight=max(2.32,2.12/aspect)*distance/8.8; aim=(0,1.38,0).'}},
 'reconstructedDiagnostic':{'files':['canonical-benchmark-front.png','historical-benchmark-neutral-front.png','v003-benchmark-front.png','v004-benchmark-front.png'],
  'renderer':'carol-v004-diagnostic.html; requested transparent ACES/sRGB exposure 1.65, warm key/cool rim/pink fill; not the renderer found at the verified HEAD.',
  'historicalMaterialHandling':'Original GLB materials/textures; toneMapped=false and opaque textured Basic materials as in actual world source. DoubleSide and maximum texture anisotropy for diagnostics. Morph influences zero for neutral comparison.',
  'camera':{'orthoWidth':5.5,'orthoHeight':4.5,'position':[0,1.55,9],'target':[0,1.55,0],'canvas':[1100,900]},
  'registration':'Historical glTF scaleX=.0072/.007, position=(.0936,.272,0); v003/v004 convert Blender (X,Y,Z) to (X,Z,-Y). Canonical uses the identical source rectangle. No per-model bbox fit.',
  'canonicalResolution':[768,493],'historicalSourceResolution':[624,400],
  'sourceResizeAspectDifferencePercent':abs((768/493)/(624/400)-1)*100},
 'limitations':['Not proven to be the exact 2026-09-10 accepted binary.',
  'Builder and checked-in binary can differ; no historical rebuild was used.',
  'Historical source paints eyes, mouth, inner ears and fleece detail. Extraction explicitly distinguishes source landmarks from new measured approximations.',
  'Historical obsolete lateral tail and atmosphere remain visible only in benchmark; not ported to v004.',
  'Source illustration is a posed three-quarter composition; its transfer into a neutral Full-3D front remains a Human judgment.',
  'Historical styling and production clay cannot certify the same material or geometry quality.']}
(OUT/'historical-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
metrics={}
for v in views:
    im=Image.open(OUT/f'carol-v004-{v}.png').convert('RGBA');bbox=im.getchannel('A').point(lambda a:255 if a>12 else 0).getbbox()
    metrics[v]={'size':im.size,'alphaBBox':bbox};assert bbox and bbox[0]>10 and bbox[1]>10 and bbox[2]<im.width-10 and bbox[3]<im.height-10
(OUT/'image-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
print('Review boards, guides, provenance and image metrics saved.')
