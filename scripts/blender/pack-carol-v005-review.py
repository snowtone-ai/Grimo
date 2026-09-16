"""Compose evidence only. Does not modify source images or saved geometry."""
import json,hashlib,ast
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/hero-geometry-v005'
board=Image.new('RGB',(1200,5*480),(235,239,246));d=ImageDraw.Draw(board)
for row,view in enumerate(['front','side','back','top','three-quarter']):
 for col,(label,folder) in enumerate([('A - frozen zero-based sculpt','parts-03'),('B - historical deformation 04','b-04')]):
  im=Image.open(OUT/'iterations'/folder/(view+'.png')).convert('RGBA')
  if view=='top' and col==1:im=im.rotate(180)
  im.thumbnail((590,450))
  x=col*600+(600-im.width)//2;y=row*480+28
  board.paste(im,(x,y),im);d.text((col*600+16,row*480+8),label+' / '+view,fill=(35,45,70))
board.save(OUT/'ab-five-view-comparison.jpg',quality=94)
protected=json.loads((OUT/'landmark-measurements.json').read_text())['protected_sha256']
checks={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in protected.items()}
assert all(checks.values())
reports={}
for k in ['a','b']:
 s=(ROOT/f'artifacts/carol-v005/{k}-glb-validation.txt').read_text(encoding='utf-8-sig')
 reports[k]=json.loads(s[s.index('{'):])
for p in (ROOT/'scripts/blender').glob('*carol-v005*.py'):ast.parse(p.read_text(encoding='utf-8'))
result={'protected_inputs_unchanged':checks,'preview_glb':reports,
 'scope':'Finite saved mesh and preview transport checks only. Both visual geometry gates FAIL; no claim of production topology readiness.'}
(OUT/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({'protected_unchanged':all(checks.values()),'glb':{k:v.get('validator') for k,v in reports.items()}},indent=2))
