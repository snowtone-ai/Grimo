"""Verify captured real PlayCanvas states against the saved authoring reference."""
from pathlib import Path
import json, struct, hashlib, math

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'docs/production/jill/texture-return-v005'
A = ROOT / 'assets/grimo/production/jill/tripo/texture-return-v005'
r = json.loads((E / 'playcanvas-runtime.json').read_text())
states = json.loads((E / 'review-states.json').read_text())
schedule = json.loads((E / 'runtime-schedule.json').read_text())
b = (A / 'jill-textured-review-bounded-v005.glb').read_bytes()
g = json.loads(b[20:20 + struct.unpack_from('<I', b, 12)[0]])
names = g['meshes'][0]['extras']['targetNames']
assert r['model_sha256'] == hashlib.sha256(b).hexdigest()
assert r['engine'] == '2.22.2' and not r['errors']
assert r['meshInstances'] == r['skinInstances'] == r['morphInstances'] == 23
assert set(r['morphTargets']) == {20} and len(set(r['anchors'])) == 16
assert all(m['diffuseMapUv'] == 0 and m['diffuseTexture'] == {'width':4096,'height':4096} for m in r['materials'])
rows = []
for case in [{'name':'neutral','peak_seconds':0}, *schedule['cases']]:
    row = next(s for s in r['samples'] if s['tag'] == case['name'] and abs(s['time'] - case['peak_seconds']) < 1e-5)
    expected = states[case['name']]['morphs']
    delta = max(abs(row['weights'][i] - expected[n]) for i,n in enumerate(names))
    assert delta < 1e-5, (case['name'], delta)
    assert len(row['anchorPositions']) == 16 and all(math.isfinite(x) for p in row['anchorPositions'] for x in p)
    rows.append({'state':case['name'],'morph_max_delta':delta,'anchor_positions_finite':True})
base = r['samples'][0]
movements = {}
for tag,bone in [('wings-open','DEF_wing_outer.L'),('wings-fold','DEF_wing_outer.R'),('tail','DEF_tail_02'),('combined','DEF_head')]:
    row = next(s for s in r['samples'] if s['tag'] == tag)
    dist = math.dist(base['positions'][bone], row['positions'][bone])
    assert dist > 1e-5
    movements[tag] = {'bone':bone,'world_displacement_m':dist}
assert len(r['samples']) > 50, 'Continuous playback evidence missing'
assert r['samples'][-1]['tag'] == 'neutral' and max(map(abs,r['samples'][-1]['weights'])) < 1e-5
out = {'pass':True,'scope':'Real Desktop WebGL2 2.22.2; bounded baked clip only, no general channel solver/full motion/mobile claim','model_sha256':r['model_sha256'],'states':rows,'representative_bone_motion':movements,'captured_samples':len(r['samples']),'neutral_recovery':True,'human_visual_go':False}
(E / 'runtime-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(out,indent=2))
