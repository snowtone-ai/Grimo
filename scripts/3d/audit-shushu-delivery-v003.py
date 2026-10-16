"""Bind deliverables to their actual hashes; fail on stale final captures."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=['shushu-v004-motion-gate-v002.blend','shushu-v004-motion-gate-v002-proof.blend','shushu-v004-motion-gate-v002.glb','shushu-v006-production-rig-v004.blend','shushu-v006-production-rig-v004-proof.blend','shushu-v006-production-rig-v004.glb'];protected=[]
for name in sources:
 p=B/name;rel=p.relative_to(R).as_posix();pointer=subprocess.check_output(['git','show','HEAD:'+rel],cwd=R,text=True);expected=pointer.split('oid sha256:')[1].splitlines()[0];actual=sha(p);is_pointer=p.stat().st_size<1024 and p.read_bytes().startswith(b'version https://git-lfs.github.com/spec/v1');assert (p.read_text()==pointer if is_pointer else actual==expected),(rel,expected,actual);protected.append({'path':rel,'expected_lfs_object_sha256':expected,'worktree_file_sha256':actual,'state':'unchanged LFS pointer' if is_pointer else 'materialized object matches LFS SHA256'})
(D/'protected-source-hashes.json').write_text(json.dumps(protected,indent=2))
asset=B/'shushu-v004-motion-gate-v003.glb';digest=sha(asset);ledgers=[]
for label in ['desktop','phone']:
 rows=json.loads((D/label/'capture-ledger.json').read_text());assert len(rows)==135,(label,len(rows))
 for row in rows:
  assert row['artifactSha256']==digest and row['sha256']==sha(D/label/(row['name']+'-'+row['view']+'.png'))
  assert abs(row['actual']['time']-row['frame']/24)<1e-4 and row['actual']['visibility']=='visible'
  if 'android' in row:assert row['android']['sha256']==sha(D/label/(row['name']+'-'+row['view']+'-android.png')) and row['android']['after']['rendered']>row['actual']['rendered']
 for p in sorted((D/label).glob('*-video-ledger.json')):
  data=json.loads(p.read_text());assert data['artifactSha256']==digest and data['sha256']==sha(p.with_name(p.name.replace('-video-ledger.json','.webm')))
  assert [r['f'] for r in data['frames']]==list(range(data['start'],data['end']+1))
  assert all(b['rendered']>a['rendered'] for a,b in zip(data['frames'],data['frames'][1:]))
 ledgers.append({'surface':label,'stills':len(rows),'videos':len(list((D/label).glob('*-video-ledger.json')))})
perf=json.loads((D/'phone/performance-environment.json').read_text());assert perf['artifact']['sha256']==digest
assert perf['summary']['productionRoute'] and perf['summary']['activeModels']==14
assert all(x['sha256']==sha(R/x['path']) for x in perf['runtimeModules'])
runtime=json.loads((D/'phone/production-loader.json').read_text());assert len(runtime['rows'])==7 and all(x['pixelPngExact'] for x in runtime['rows'])
life=json.loads((D/'phone/production-loader-lifecycle.json').read_text());assert life['before']==life['after'] and all(x['candidateExact'] and x['originalRestoredExact'] for x in life['rows'])
control=json.loads((D/'phone-purpose-controls/purpose-controls.json').read_text());assert control['artifactSha256']==digest and len(control['rows'])==26 and any(x['carrierFrame']!=x['frame'] for x in control['rows']);assert all(x['position']<1e-5 and x['normal']<1e-4 and x['anchor']<1e-4 for x in control['rows'])
probes=json.loads((D/'paw-space-probes.json').read_text())['rows'];assert len(probes)==264 and all(not x['confirmed_inside_vertices'] and not x['head_confirmed_inside'] and x['proximal_inside_torso_count']>0 and not x['invalid_drivers'] for x in probes);assert min(x['volume_proxy'] for x in probes)>.98
assert all(x['tip_surface_clearance_H']['Head']<.004 for x in probes if x['state'].get('SelfContact.'+x['side'])==1 and len(x['state'])==2)
for label,source in [('author',B/'shushu-v004-motion-gate-v003-proof.blend'),('saved',asset)]:
 for kind,count in [('render',84),('video',480)]:
  ledger=json.loads((D/(label+'-'+kind+'-ledger.json')).read_text());assert ledger['source_sha256']==sha(source) and len(ledger['images'])==count
  if kind=='render':assert all(sha(R/x['file'])==x['sha256'] for x in ledger['images'])
contact=json.loads((D/'contact-surface-audit.json').read_text());assert len(contact['rows'])==102 and all(not t['distal_triangle_crossings'] for x in contact['rows'] for t in x['distal_nearest_signed_probes'])
video=json.loads((D/'encoded-video-audit.json').read_text());assert video['artifact_sha256']==digest and len(video['videos'])==40 and all(x['unique_decoded_frame_hashes']>1 for x in video['videos'])
assert all(x['sha256']==sha(R/x['file']) for x in video['videos'])
boards=json.loads((D/'comparison-ledger.json').read_text());assert boards['artifact_sha256']==digest
assert all(x['sha256']==sha(R/x['path']) for board in boards['boards'] for x in board['sources'])
p=json.loads((D/'phone/performance.json').read_text());assert p['seconds']==300 and p['contextLoss']==0 and p['controllerSamples']>10000
paths=[B/'shushu-v004-motion-gate-v003.blend',B/'shushu-v004-motion-gate-v003-proof.blend',asset,*sorted((R/'assets/grimo/production/shushu/runtime').glob('*.mjs'))]
selection=D/'delivery-files.json'
evidence=[]
if selection.exists():
 for rel in json.loads(selection.read_text(encoding='utf-8'))['paths']:
  p=R/rel
  if p==D/'delivery-manifest.json' or p in paths:continue
  assert p.is_file(),rel
  data=p.read_bytes();mode='raw'
  try:
   data.decode('utf-8');data=data.replace(b'\r\n',b'\n');mode='UTF-8 normalized LF'
  except UnicodeDecodeError:pass
  evidence.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'hash_bytes':mode,'bytes':p.stat().st_size})
report={'artifact_sha256':digest,'artifacts':[{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in paths],'evidence':evidence,'protected_source_files':len(protected),'capture_ledgers':ledgers,'scope':'Hash/frame/freshness correspondence; art, contact and performance gates remain separate.'};(D/'delivery-manifest.json').write_text(json.dumps(report,indent=2));print({'artifact_sha256':digest,'artifacts':len(paths),'evidence':len(evidence),'protected_source_files':len(protected),'capture_ledgers':ledgers})
