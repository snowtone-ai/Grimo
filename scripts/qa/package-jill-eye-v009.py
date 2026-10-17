"""Verify completed captures, package comparisons, write the manifest last."""
from pathlib import Path
import json,hashlib,struct,subprocess,ast
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/eye-join-v009';A=ROOT/'assets/grimo/production/jill/tripo/eye-join-v009'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(E/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def read_glb(p):
    raw=p.read_bytes();n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);k=20+n;nb=struct.unpack_from('<I',raw,k)[0];return g,raw[k+8:k+8+nb]
for n in ['preservation.json','reimport-proof.json']:assert json.loads((E/n).read_text())['pass']
g,blob=read_glb(A/'jill-textured-rig-v009.glb')
assert sha(A/'jill-basecolor-v009.png')==sha(ROOT/'assets/grimo/production/jill/tripo/eye-boundary-v008/jill-basecolor-v008.png')
names=g['meshes'][0]['extras']['targetNames'];expected=json.loads((E/'review-states.json').read_text());runtime=[]
for file,model in [('static-runtime.json','jill-textured-rig-v009.glb'),('bounded-runtime.json','jill-review-bounded-v009.glb')]:
    d=json.loads((E/file).read_text());assert not d['errors'] and d['model_sha256']==sha(A/model)
    assert d['skinInstances']==d['morphInstances']==23 and len(d['anchors'])==16 and set(d['morphTargets'])=={20}
    assert d['samples'][-1]['tag']=='neutral' and max(map(abs,d['samples'][-1]['weights']))<1e-6
    if file.startswith('bounded'):
        checks=[]
        for state in ['mouth-closed','mouth-small','mouth-large','blink-half','blink-full','wings-open','wings-fold','tail','combined']:
            sample=next(x for x in d['samples'] if x['tag']==state);delta=max(abs(w-expected[state]['morphs'][n]) for n,w in zip(names,sample['weights']));assert delta<2e-6;checks.append({'state':state,'max_weight_delta':delta})
        assert len(d['samples'])>30;runtime.append({'file':file,'cases':checks,'rendered_samples':len(d['samples'])})
    else:
        assert d['directEye']['instanceCount']==d['directMouth']['instanceCount']==23
        eye=d['directEye']['samples'];assert len(eye)>=30
        for row in eye:
            assert len(row['instances'])==23
            assert max(abs(v-row['controls'][n]) for inst in row['instances'] for n,v in inst.items())<1e-6
        for row in d['directMouth']['samples']:
            c=row['controls'];want={'FACE_MouthClose':c['mouth_close'],'FACE_MouthOpen':c['mouth_open']*(1-c['mouth_close']),'FACE_Smile.L':c['smile.L']*(1-c['mouth_close']),'FACE_Smile.R':c['smile.R']*(1-c['mouth_close'])}
            assert max(abs(v-want[n]) for inst in row['instances'] for n,v in inst.items())<1e-6
        runtime.append({'file':file,'eye_samples_all_23_instances':len(eye),'mouth_samples':len(d['directMouth']['samples'])})
recovery=np.array_equal(np.array(Image.open(E/'runtime-neutral-canvas.png')),np.array(Image.open(E/'runtime-recovery-canvas.png')));assert recovery
mouth={}
for s in ['neutral','mouth-closed','mouth-small','mouth-large','recovery']:
    a=np.array(Image.open(E/f'renders/{s}-front.png'));b=np.array(Image.open(ROOT/f'docs/production/jill/clover-v007/renders/face-{s}-front.png'));mouth[s]=bool(np.array_equal(a[365:520,225:415],b[365:520,225:415]))
assert all(mouth.values());write('mouth-pixel-regression.json',{'pass':True,'roi_xyxy':[225,365,415,520],'same_camera_front_exact':mouth})
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',25)
for detail,width,height in [(False,1560,1328),(True,1040,416)]:
    canvas=Image.new('RGB',(width,height),'#eef0e8');draw=ImageDraw.Draw(canvas)
    for row,(name,label) in enumerate([('runtime-before-face.png','v008 BEFORE'),('runtime-face.png','v009 AFTER')]):
        im=Image.open(E/name).convert('RGB')
        if detail:
            canvas.paste(im.crop((0,325,520,505)),(0,row*208+28));canvas.paste(im.crop((1040,325,1560,505)),(520,row*208+28));draw.text((12,row*208),label,fill='#183324',font=font)
        else:canvas.paste(im.crop((0,75,1560,715)),(0,row*664+24));draw.text((12,row*664),label,fill='#183324',font=font)
    canvas.save(E/('eye-detail-before-after.png' if detail else 'eye-before-after.png'))
frames=[Image.open(E/f'runtime-sweep-{i:02}.png').convert('RGB').resize((1170,480)) for i in range(21)];frames[0].save(E/'blink-runtime.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
protected=[]
for folder,names0 in [('clover-v007',['jill-textured-rig-v007.blend','jill-textured-rig-v007.glb','jill-basecolor-v007.png']),('mouth-integration-v006',['jill-textured-rig-v006.blend','jill-textured-rig-v006.glb']),('texture-return-v005',['jill-textured-rig-v005.blend','jill-textured-rig-v005.glb','jill-basecolor-v005.png'])]:
    for name in names0:
        p=ROOT/'assets/grimo/production/jill/tripo'/folder/name;rel=p.relative_to(ROOT).as_posix();prior=subprocess.check_output(['git','rev-parse','cc080bc:'+rel],cwd=ROOT,text=True).strip();now=subprocess.check_output(['git','hash-object',str(p)],cwd=ROOT,text=True).strip();assert prior==now;protected.append({'path':rel,'git_blob_exact':True,'sha256':sha(p)})
write('verification.json',{'pass':True,'runtime':runtime,'neutral_canvas_recovery_exact':bool(recovery),'mouth_pixels_exact':mouth,'protected_sources':protected,'full_model_complete':False,'remaining':'Eye appearance Human GO. Full model acceptance is not inferred from the scoped feature approvals.'})
write('Gate.json',{'mouth':'Human GO','clover':'Human OK','horns':'unchanged / no change needed','eye_join_technical':True,'eye_appearance':'Human GO: 2026-10-18','full_model_complete':False,'remaining':'Physical floating outer lid bands corrected bilaterally; Human eye appearance GO received. Full model acceptance is not inferred.'})
scripts=['scripts/blender/jill-eye-join-v009.py','scripts/blender/verify-jill-eye-join-v009.py','scripts/qa/capture-jill-eye-v009.js','scripts/qa/capture-jill-eye-v009-bounded.js','scripts/qa/package-jill-eye-v009.py','scripts/3d/jill-eye-v008/review-controls.mjs','scripts/3d/jill-texture-v005/serve.mjs','scripts/3d/jill-texture-v005/viewer.mjs','docs/production/jill/HANDOFF.md']
for p in scripts:
    if p.endswith('.py'):ast.parse((ROOT/p).read_text(encoding='utf8'))
files=[p for p in E.rglob('*') if p.is_file() and p.name not in ['Manifest.json','RemoteReceipt.json']]+list(A.glob('*'))+[ROOT/p for p in scripts]
write('Manifest.json',{'branch':'codex/jill-texture-return-v005-20261017','base':'cc080bc','scope':'Bilateral local lid/skin join and Blink correction; original eye Basis/approved mouth/clover/horns preserved; Human eye appearance GO','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(set(files)) if p.is_file()]})
print('v009 focused proofs passed; comparisons finalized; manifest written last',flush=True)
