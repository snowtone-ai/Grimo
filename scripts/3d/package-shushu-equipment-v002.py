"""Package only current-ledger evidence; never sweep unrelated/stale work into Git."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/standard-appearance-v002';A=R/'assets/grimo/production/shushu/equipment/standard-v002'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
authorDoc=read(D/'author-ledger.json');savedDoc=read(D/'saved-ledger.json')
assert authorDoc['captureSettings']==savedDoc['captureSettings'],'Author/saved capture conditions differ'
author=authorDoc['images'];saved=savedDoc['images'];pc=read(D/'pc/capture-ledger.json')['images']
assert len(author)==len(saved)==28 and len(pc)==40
rows=[]
for a,b in zip(author,saved):
 assert (a['frame'],a['view'])==(b['frame'],b['view'])
 for record in [a,b]:assert sha(R/record['file'])==record['sha256']
 x=np.asarray(Image.open(R/a['file']).convert('RGB')).astype(float);y=np.asarray(Image.open(R/b['file']).convert('RGB')).astype(float);diff=np.abs(x-y)
 rows.append({'frame':a['frame'],'view':a['view'],'rgbMeanAbsolute8bit':float(diff.mean()),'rgbMaximum8bit':float(diff.max()),'pixelsAnyDifference':int(np.any(diff>0,axis=-1).sum())})
for p in pc:assert sha(D/'pc'/p['file'])==p['sha256']
write(D/'roundtrip-comparison.json',{'scope':'28 matched 640px author/saved images; same fixed EEVEE conditions; pixel differences include glTF export/import normals/material implementation. Does not compare PC pixels or infer Human PASS.','rows':rows})
validation=read(R/'output/shushu-flower-v002-glb-validation.json');validation['file']='assets/grimo/production/shushu/equipment/standard-v002/shushu-head-flower-v002.glb';write(D/'flower-glb-validation.json',validation)
sheet=Image.new('RGB',(1280,1340),'#f6f1f2');draw=ImageDraw.Draw(sheet)
for row,view in enumerate(['front','3qR']):
 for col,prefix,label in [(0,'before-','Before v001'),(1,'','Rounded satin v002')]:
  x=col*640;y=row*670;im=Image.open(D/'pc'/f'{prefix}close-{view}.png').convert('RGB').resize((640,640));sheet.paste(im,(x,y));draw.text((x+16,y+646),label+' / '+view,fill='#352d33')
sheet.save(D/'before-after.jpg',quality=94)
paths=[D/f for f in ['REVIEW.md','STRUCTURE.md','index.html','runtime.html','preservation.json','approved-pads.json','visible-clearance.json','author-texture-pack.json','author-ledger.json','saved-ledger.json','blockout-ledger.json','roundtrip-comparison.json','flower-glb-validation.json','before-after.jpg']]
paths += [R/p['file'] for p in author+saved]
paths += [R/p['file'] for p in read(D/'blockout-ledger.json')]
paths += [D/'pc'/p['file'] for p in pc]
paths += [D/'pc'/f for f in ['environment.json','attachment-and-toggle.json','capture-ledger.json','video-ledger.json','lifecycle.json','errors.json','head-ear-3qR.webm']]
paths += [A/f for f in ['shushu-head-flower-v002.glb','shushu-head-flower-v002.blend','shushu-standard-appearance-v002-proof.blend']]
paths += [R/'assets/grimo/production/shushu/runtime'/f for f in ['shushu-v004-loader-v004.mjs','shushu-standard-appearance-v002.mjs']]
paths += [R/'scripts/blender'/f for f in ['build-shushu-equipment-v002.py','finalize-shushu-flower-blend-v002.py','verify-shushu-equipment-v002.py','audit-shushu-equipment-v002.py']]
paths += [R/'scripts/3d'/f for f in ['capture-shushu-equipment-v002.mjs','package-shushu-equipment-v002.py']]
paths += [R/'.gitattributes',R/'docs/production/Handoff.md',R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004/REVIEW.md',R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004/index.html']
paths += [R/'docs/production/shushu/evidence/standard-appearance-v001'/f for f in ['REVIEW.md','index.html','runtime.html']]
paths=sorted(set(paths))
audit=read(D/'pc/attachment-and-toggle.json');assert len(audit['rows'])==192 and all(r['matrixError']==r['localError']==r['glError']==0 for r in audit['rows'])
assert read(D/'pc/errors.json')==[]
assert read(D/'preservation.json')['all14MeshesExact']
assert read(D/'author-texture-pack.json')['exact']
assert read(D/'approved-pads.json')['unchanged']
assert validation['validator']['errors']==validation['validator']['warnings']==0
# Windows Blender/Python reports may have CRLF. Hash the same LF byte stream
# required by scoped .gitattributes, so a later checkout retains evidence hashes.
for p in paths:
 if p.suffix in {'.md','.json','.html','.mjs','.py'} or p.name=='.gitattributes':p.write_text(p.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
inputs=[R/'assets/grimo/production/shushu/equipment/standard-v001/shushu-hind-sole-pads-v001.png',R/'assets/grimo/production/shushu/equipment/standard-v001/shushu-head-flower-v001.glb',R/'assets/grimo/source/shushu/shushu-Identity-canonical.png',R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v004.glb',R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v004-proof.blend']
entry=lambda p:{'file':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
manifest={'date':'2026-10-17','branch':'codex/shushu-abc-motion-repair-v004-20261017','approvedComparisonHead':'8d3235f0b176088f2434ee482aa5d14d7b94ef58','rulesMainHead':'336997db2b95244c17774258e2f5ff874a2adbc1','gates':{'existingV004ComparisonHumanAppearance':'PASS: explicit Human instruction, original scope only','hindSolePadsHuman':'PASS: latest Human 足裏はOK','v001FlowerHuman':'FAIL: thin and cheap appearance','v002FlowerHuman':'PENDING','phone':'UNKNOWN; no USB','originalReplacementAndMotionProduction':'HOLD until Human GO'},'inputsReadOnly':[entry(p) for p in inputs],'artifacts':[entry(p) for p in paths],'exclusions':'Original assets, .blend1 backups, stale non-ledger captures, output scratch, pre-existing user changes; manifest itself excluded from recursive hashing.'}
write(D/'delivery-manifest.json',manifest)
stage=[str(p.relative_to(R).as_posix()) for p in paths]+['docs/production/shushu/evidence/standard-appearance-v002/delivery-manifest.json','docs/production/Handoff.md','docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004/REVIEW.md','docs/production/shushu/evidence/standard-appearance-v001/runtime.html']
# Explicit reviewed path list for scoped staging; script itself never stages/commits.
(R/'output/shushu-equipment-v002-stage-paths.txt').write_text('\n'.join(stage)+'\n',encoding='utf-8')
print(json.dumps({'artifacts':len(paths),'bytes':sum(p.stat().st_size for p in paths),'maxRoundtripMeanRGB8bit':max(r['rgbMeanAbsolute8bit'] for r in rows)},indent=2))
