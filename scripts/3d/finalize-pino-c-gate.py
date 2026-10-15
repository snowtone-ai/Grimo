"""Assert evidence completeness and write the technical gate, never Human approval."""
import argparse,json,hashlib,re
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/geometry-c-v001';ASSET=ROOT/'assets/grimo/production/pino/candidate-c'
read=lambda n:json.loads((OUT/n).read_text(encoding='utf-8'))
def write(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
args=argparse.ArgumentParser();args.add_argument('--original-checkout',type=Path);a=args.parse_args()
expected={'fbx':'3531eddb0578be8e4885b942db629a97a949d2039eb496c88ed1dc041372a111','glb':'ee7339f8e4339037b87880b75d90fd944fe7dda84f696c2be42db7ea0f24da11'};sources=[]
for ext,h in expected.items():
    paths=[('immutable source',ASSET/'source'/f'cute blue creature 3d model.{ext}'),('retained archive',ASSET/'delivery'/f'pino-c-retained.{ext}')]
    if a.original_checkout:paths.append(('original user checkout',a.original_checkout/f'cute blue creature 3d model.{ext}'))
    for role,p in paths:
        actual=sha(p);assert actual==h,(role,ext,actual);sources.append(dict(role=role,format=ext,sha256=actual,unchanged=True))
write('source-verification.json',dict(originals=sources))
d=read('four-tests.json');s=read('four-tests-summary.json');r=read('saved-file-verification.json');ep=read('export-pixel-comparison.json');sn=read('saved-neutral-pixel-comparison.json');ex=read('master-export.json')
assert len(d['runs'])==14 and sum(len(x['frames']) for x in d['runs'])==182
assert all(x['neutral_return_exact'] for x in d['runs']) and all(d['neutral_restoration_exact'].values())
assert s['all_rendered_returns_pixel_exact'] and len(s['rendered_neutral_return'])==42
assert ep['all_nine_views_pixel_exact'] and sn['all_views_pixel_exact']
assert r['playback']['frames']==182 and all(r[n]['local_vertices'] and r[n]['corner_normals'] for n in ['pino-c-master-retained.blend','pino-c-master-derived-four-tests.blend'])
assert ex['active_binary_payload_byte_exact_to_reference'] and not ex['export_triangles_not_contained_in_fbx_faces']
for family in ['tail','eyes','forepaws','low-rest']:
    for name in [f'actual-{family}.gif',f'actual-{family}-extremes.png',f'cycles-{family}-extremes.png']:assert (OUT/name).is_file(),name
for doc in [OUT/'REVIEW.md',OUT/'REPRODUCE.md',ASSET/'README.md']:
    for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
        if '://' not in target:assert (doc.parent/unquote(target.split('#')[0])).exists(),(doc,target)
write('gate-status.json',dict(human_geometry_gate='PENDING',tripo_readiness='HOLD / BLOCKED',tripo_operations=False,adopted_repairs=False,
    master='FBX only',appearance_reference='immutable original GLB',neutral_appearance='PASS: exact active GLB binary/material data, reimport equality and nine pixel-exact views',
    neutral_return='PASS: 14 sequences / 42 rendered returns; saved Master/replay readback verified',
    actual_test_frames=182,actual_view_renders=546,
    tests={'tail':dict(status='FAIL / HOLD overall',bounded_volume='PASS',reason='Triple shell and unwelded overlapping root remain unresolved; production connection/collision suitability unknown'),
    'eyes':dict(status='UNKNOWN / HOLD',reason='Independent actual blink/wink/half/full-close attempts demonstrated; natural eyelid/eyeball closure and identity require Human review'),
    'forepaws':dict(status='FAIL',reason='Both-hand contact not reached; local distortion; endpoint-fitted fixtures do not establish general Food/Gift grasp'),
    'low-rest':dict(status='FAIL',reason='Attempted method loses natural face/body volume; 255 floor-penetrating vertices; belly/tail support absent; physical COM unknown')},
    feasibility_of_untried_rig_methods='UNKNOWN; failed diagnostic methods do not prove impossibility',
    runtime_smartphone_and_tripo_import='UNKNOWN; not exercised',authority_lock='2abea76fad578281f74b9fa628987a80b56ad6dc / integrated identical blob via main 8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b'))
print('Evidence complete. Human Geometry Gate PENDING; Tripo HOLD. Sources unchanged.')
