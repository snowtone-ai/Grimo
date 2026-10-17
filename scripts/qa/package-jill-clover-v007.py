"""Finalize evidence only after Blender and real browser captures have finished."""
from pathlib import Path
import ast,hashlib,json,subprocess
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/clover-v007';A=ROOT/'assets/grimo/production/jill/tripo/clover-v007';OLD=ROOT/'docs/production/jill/mouth-integration-v006/renders'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,d):(E/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
rows={s:bool(np.array_equal(np.array(Image.open(E/f'renders/face-{s}-front.png')),np.array(Image.open(OLD/f'after-{s}-front.png')))) for s in ['neutral','mouth-closed','mouth-small','mouth-large','recovery']};assert all(rows.values())
d=json.loads((E/'static-runtime.json').read_text());assert d['model_sha256']==sha(A/'jill-textured-rig-v007.glb') and not d['errors'];assert d['skinInstances']==d['morphInstances']==23 and len(d['anchors'])==16 and set(d['morphTargets'])=={20}
checks=[]
for controls in [{'mouth_close':1,'mouth_open':1,'smile.L':1,'smile.R':1},{'mouth_close':.5,'mouth_open':0,'smile.L':0,'smile.R':0},{'mouth_close':0,'mouth_open':1,'smile.L':0,'smile.R':0},{'mouth_close':0,'mouth_open':.5,'smile.L':1,'smile.R':.5}]:
    matches=[x for x in d['directMouth']['samples'] if x['controls']==controls];assert matches
    expected={'FACE_MouthClose':controls['mouth_close'],'FACE_MouthOpen':controls['mouth_open']*(1-controls['mouth_close']),'FACE_Smile.L':controls['smile.L']*(1-controls['mouth_close']),'FACE_Smile.R':controls['smile.R']*(1-controls['mouth_close'])}
    delta=max(abs(weights[k]-v) for weights in matches[-1]['instances'] for k,v in expected.items());assert delta<1e-6;checks.append({'controls':controls,'max_delta':delta})
assert d['samples'][-1]['tag']=='neutral' and max(map(abs,d['samples'][-1]['weights']))<1e-6
for name in ['preservation.json','reimport-proof.json','texture-diff.json']:assert json.loads((E/name).read_text())['pass']
protected=[]
for version,files in [('mouth-integration-v006',['jill-textured-rig-v006.blend','jill-textured-rig-v006.glb']),('texture-return-v005',['jill-textured-rig-v005.blend','jill-textured-rig-v005.glb','jill-basecolor-v005.png'])]:
    for name in files:
        p=ROOT/'assets/grimo/production/jill/tripo'/version/name;rel=p.relative_to(ROOT).as_posix();old=subprocess.check_output(['git','rev-parse','d4e73c1:'+rel],cwd=ROOT,text=True).strip();now=subprocess.check_output(['git','hash-object',str(p)],cwd=ROOT,text=True).strip();assert old==now;protected.append({'path':rel,'sha256':sha(p),'git_blob_unchanged':True})
write('verification.json',{'pass':True,'approved_v006_face_pixels_exact':rows,'static_runtime':{'engine':d['engine'],'skin':23,'morphs':20,'anchors':16,'model_sha256':d['model_sha256'],'simultaneous_inputs':checks,'neutral_recovery':True},'protected_sources':protected,'full_model_complete':False})
write('Gate.json',{'mouth':'Human GO 2026-10-18','clover':'Human OK 2026-10-18','horns':'Human: no change needed; retain inherited v005 appearance. No horn edits made.','technical':True,'full_model_complete':False,'remaining':'Human-reported eye/skin boundary line with eyeball exposed outside it; now explicitly authorized for diagnosis and local repair, separate derivative.'})
scripts=['scripts/blender/jill-clover-v007.py','scripts/blender/verify-jill-clover-v007.py','scripts/qa/project-jill-clover-v007.py','scripts/qa/capture-jill-clover-v007.js','scripts/qa/package-jill-clover-v007.py','scripts/3d/jill-texture-v005/serve.mjs','scripts/3d/jill-texture-v005/viewer.mjs','docs/production/jill/HANDOFF.md']
for p in scripts:
    if p.endswith('.py'):ast.parse((ROOT/p).read_text(encoding='utf8'))
files=[p for p in E.rglob('*') if p.is_file() and p.name not in ['Manifest.json','RemoteReceipt.json']]+list(A.glob('*'))+[ROOT/p for p in scripts]
write('Manifest.json',{'branch':'codex/jill-texture-return-v005-20261017','mouth_base_commit':'d4e73c1','human_decisions':'2026-10-18 mouth GO, clover OK, horns unchanged','scope':'Image-only clover derivative; full-model eye issue remains','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(set(files)) if p.is_file()]})
print('v007 proofs passed; immutable mouth and original assets preserved; manifest written last')
