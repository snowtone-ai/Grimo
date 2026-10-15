"""Summarize focused checks and verify protected inputs without modifying them."""
import json,hashlib,subprocess
from pathlib import Path
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-skin-compat'
def read(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
changed=[];missing=[];count=0
for r in read('protected-inputs.json'):
    p=ROOT/r['path']
    if not p.exists():missing.append(r['path']);continue
    h=sha(p);count+=1
    if h!=r['sha256']:changed.append({'path':r['path'],'before':r['sha256'],'after':h})
gpu=read('phone-local8-audit.json');captures=[c for r in gpu['gpu'] for c in r['captures']]
assert len(captures)==294 and all(c.get('glError')==0 and 'error' not in c for c in captures)
assert all(len(r['captures'])==3 for r in gpu['gpu'])
comparisons=[]
for a in OUT.glob('phone-local8-*.png'):
    if not any(a.name.startswith('phone-local8-'+s) for s in ['lit-','unlit-','normal-','arm-']):continue
    b=OUT/a.name.replace('local8','full8');
    if not b.exists():continue
    aa=np.array(Image.open(a).convert('RGB'),dtype=float);bb=np.array(Image.open(b).convert('RGB'),dtype=float);assert aa.shape==bb.shape==(640,640,3)
    d=np.abs(aa-bb);comparisons.append({'candidate':a.name,'reference':b.name,'meanAbsoluteRGB255':float(d.mean()),'maxChannel255':int(d.max()),'pixelsAnyChannelGt8':int((d.max(2)>8).sum())})
video=[]
for p in list(OUT.glob('*.webm'))+list(OUT.glob('*.mp4')):
    result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,nb_frames,codec_name','-of','json',str(p)],capture_output=True,text=True,check=True);video.append({'file':p.name,**json.loads(result.stdout)})
report={'protected':{'checked':count,'changed':changed,'missing':missing,'intentionalStateUpdate':['docs/production/Handoff.md']},'gpuSkin':{'frames':len(gpu['gpu']),'meshCaptures':len(captures),'maxPositionH':max(c['skinOnlyPosition'] for c in captures),'maxNormalDeg':max(c['skinOnlyNormalDeg'] for c in captures),'glErrors':0},'binding':{k:max(r[k] for r in gpu['binding']) for k in ['maxMatrix','maxAnchor','maxMorph']},'pixels':comparisons,'video':video,'handoffUnicodeCharacters':len((ROOT/'docs/production/Handoff.md').read_text(encoding='utf8')),'gate':'HOLD: Human local A and B; no original replacement or Motion production','gpuTime':'UNKNOWN'}
(OUT/'validation-summary.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps({'protected':report['protected'],'gpuSkin':report['gpuSkin'],'pixelPairs':len(comparisons),'video':len(video),'handoffCharacters':report['handoffUnicodeCharacters']},ensure_ascii=False))
assert not missing and all(r['path']=='docs/production/Handoff.md' for r in changed),'Protected input drift; inspect before commit'
assert report['handoffUnicodeCharacters']<=4000
