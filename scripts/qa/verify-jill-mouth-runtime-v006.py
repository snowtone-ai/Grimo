"""Bounded real-runtime transport evidence, not full appearance certification."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'scripts/qa/verify-jill-runtime-v005.py').read_text(encoding='utf8')
source=source.replace('docs/production/jill/texture-return-v005','docs/production/jill/mouth-integration-v006').replace('assets/grimo/production/jill/tripo/texture-return-v005','assets/grimo/production/jill/tripo/mouth-integration-v006').replace('jill-textured-review-bounded-v005.glb','jill-review-bounded-v006.glb')
exec(compile(source,'<integrated mouth bounded runtime>','exec'),globals())
data=json.loads((E/'playcanvas-runtime.json').read_text())
direct=data.get('directMouth');assert direct and direct['instanceCount']==23,'Direct-control runtime proof missing'
expected=json.loads((E/'expression-sweep.json').read_text())['overlap_samples'];rows=[]
for sample in expected:
    matches=[s for s in direct['samples'] if s['controls']==sample['channels']];assert matches, sample['channels']
    row=matches[-1];assert len(row['instances'])==23
    delta=max(abs(weights[name]-sample['morphs'].get(name,0)) for weights in row['instances'] for name in weights)
    assert delta<1e-6,(sample['channels'],delta)
    rows.append({'controls':sample['channels'],'instances':23,'max_morph_delta':delta})
(E/'direct-mouth-runtime.json').write_text(json.dumps({'pass':True,'scope':'Live direct weights on all 23 morph instances, animation writer paused, 15 simultaneous-input cases compared against saved Blender driver results','model_sha256':data['model_sha256'],'states':rows},indent=2)+'\n',encoding='utf8')
print('Direct mouth controls: all 15 cases / 23 instances match saved Blender drivers')
static=json.loads((E/'static-mouth-runtime.json').read_text());blob=(A/'jill-textured-rig-v006.glb').read_bytes()
assert static['model_sha256']==hashlib.sha256(blob).hexdigest() and not static['errors']
assert static['meshInstances']==static['skinInstances']==23 and len(static['anchors'])==16
assert static['directMouth']['instanceCount']==23
static_rows=[]
for sample in expected:
    matches=[s for s in static['directMouth']['samples'] if s['controls']==sample['channels']];assert matches,sample['channels']
    delta=max(abs(weights[name]-sample['morphs'].get(name,0)) for weights in matches[-1]['instances'] for name in weights)
    assert delta<1e-6
    static_rows.append({'controls':sample['channels'],'max_morph_delta':delta})
baseline=static['samples'][0]
assert static['samples'][-1]['tag']=='neutral' and max(map(abs,static['samples'][-1]['weights']))<1e-6
bone_delta=max(math.dist(s['positions'][name],baseline['positions'][name]) for s in static['samples'] for name in baseline['positions'])
assert bone_delta<1e-7
(E/'static-mouth-runtime-proof.json').write_text(json.dumps({'pass':True,'scope':'Actual static GLB with no animation loaded; live simultaneous mouth controls, not baked poses','model_sha256':static['model_sha256'],'states':static_rows,'bones_max_position_delta_m':bone_delta,'neutral_recovery':True},indent=2)+'\n',encoding='utf8')
print('Static GLB: live direct mouth / 15 cases / neutral recovery passed')
