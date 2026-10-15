"""Final focused evidence and protected-input audit; never modifies production assets."""
from pathlib import Path
import ast,json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def main():
    initial=read('protected-inputs.json');changed=[];missing=[]
    for name,old in initial.items():
        p=ROOT/name
        if not p.is_file():missing.append(name)
        elif sha(p)!=old:changed.append(name)
    assert not missing and set(changed)<={'docs/production/Handoff.md'},(changed,missing)
    base=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
    source=base/'shushu-v006-production-rig-v004.glb'
    assert sha(source)=='5fb05e5b7a9cbdb07a64beb5a511d6347c656d85d111ed16eccc533ecfc44cb5'
    validator=read('glb-validation.json')['validator'];assert validator['errors']==0
    rt=read('saved-roundtrip.json');assert rt['max_position_error']<1e-5 and rt['anchor_max_matrix_error']<1e-5
    runtime=read('runtime-checks.json');assert not runtime['errors']
    assert all(a['maxMorph']<1e-5 and a['maxAnchor']<1e-5 for a in runtime['audits'])
    tex=read('texture-authoring.json');assert tex['outside_local_changes']==0 and tex['uv_changes']==0
    assert read('texture-stage-geometry-invariance.json')['equal']
    assert read('texture-material-restoration.json')['numeric_accessor_bytes_unchanged']
    gpu=read('gpu-mouth-readback.json');mouth=[c for f in gpu['frames'] for c in f['captures'] if c.get('mesh') in ['ShushuStatic_Head','ShushuStatic_MouthInterior','ShushuStatic_OralBowl','ShushuStatic_Tongue']]
    assert len(mouth)==32 and all(not c.get('error') and c['glError']==0 for c in mouth)
    expected=[OUT/k/f'{s}-{v}.png' for k in ['author','saved','runtime','geometry-clay','before'] for s in ['closed','small','medium','large'] for v in ['front','side','3q']]
    assert all(p.is_file() and Image.open(p).size==(640,640) for p in expected)
    image_diff=[]
    for s in ['closed','small','medium','large']:
        for v in ['front','side','3q']:
            a=np.array(Image.open(OUT/'author'/f'{s}-{v}.png')).astype(float);b=np.array(Image.open(OUT/'saved'/f'{s}-{v}.png')).astype(float)
            image_diff.append({'state':s,'view':v,'rms_8bit':float(np.sqrt(((a-b)**2).mean())),'max_8bit':float(abs(a-b).max()),'note':'Separate Cycles render / saved import; this is not an Engine pixel-equality claim.'})
    scripts=[p for parent in ['scripts/3d','scripts/blender'] for p in (ROOT/parent).glob('*shushu-v004-mouth-b.py')]
    for p in scripts:ast.parse(p.read_text(encoding='utf8'))
    assets=[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(base.glob('shushu-v004-mouth-b-v001*'))]
    result={'source_HEAD':'d5e9882dd644ca35c6944ed9e1c7b4163944890a','branch':'codex/shushu-v004-mouth-b-20261015','protected_input_count':len(initial),'protected_unchanged':len(initial)-len(changed),'authorized_state_document_changes':changed,'missing':missing,'source_v004_sha256':sha(source),'assets':assets,'required_native_renders':len(expected),'validator':{k:validator[k] for k in ['errors','warnings','infos']},'saved_max_position_error':rt['max_position_error'],'saved_anchor_matrix_error':rt['anchor_max_matrix_error'],'runtime_max_morph_error':max(a['maxMorph'] for a in runtime['audits']),'runtime_max_anchor_matrix_error':max(a['maxAnchor'] for a in runtime['audits']),'gpu_mouth_max_position_error':max(c['maxPosition'] for c in mouth),'gpu_mouth_max_normal_angle_degrees':max(c['maxNormalDeg'] for c in mouth),'changed_head_texels':tex['changed_texels'],'head_texels':tex['head_texels'],'changed_head_percent':tex['changed_texels']/tex['head_texels']*100,'blender_saved_image_comparison':image_diff,'syntax_checked_python_scripts':len(scripts),'technical_scope':'Focused mouth candidate PC diagnostic. Geometry return and digital correspondence are separate from Human visual approval.','GO_HOLD':'Technical evidence ready / Human mouth approval PENDING / Original replacement and Motion production HOLD / A unchanged HOLD / Phone excluded by Human'}
    (OUT/'validation-summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps({k:v for k,v in result.items() if k not in ['blender_saved_image_comparison','assets']},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
