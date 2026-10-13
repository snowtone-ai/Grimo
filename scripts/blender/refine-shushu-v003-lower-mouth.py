"""Continue saved v003: retract only the opened lower lip into a round profile."""
import sys
sys.dont_write_bytecode=True
import bpy,json,importlib.util,shutil,hashlib,subprocess,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('nose',Path(__file__).with_name('refine-shushu-v003-reference-nose.py'))
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
a,r,v=n.a,n.r,n.v
BASE='b92aa7683beb2c1ca7d0c7a4e0173c5ee32773d9'
OUT=v.OUT/'lower-mouth-revision'
BACK=ROOT/'.git/shushu-v003-lower-mouth-b92aa76'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def snapshot():
 BACK.mkdir(parents=True,exist_ok=True)
 if (BACK/'inputs.json').exists():return
 inputs=json.loads((n.OUT/'protected-inputs.json').read_text(encoding='utf-8'))
 for p in [v.ASSET,v.PROOF,v.STATIC.with_suffix('.fbx'),v.STATIC.with_suffix('.glb')]:
  rel=p.relative_to(ROOT).as_posix();data=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True,check=True).stdout
  if data.startswith(b'version https://git-lfs.github.com/spec/v1'):data=subprocess.run(['git','lfs','smudge'],input=data,cwd=ROOT,capture_output=True,check=True).stdout
  assert hashlib.sha256(data).hexdigest()==sha(p),('Concurrent change',rel)
  (BACK/p.name).write_bytes(data);inputs[rel]=sha(p)
 (BACK/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
 write('authority.json',{'base':BASE,'Human':'PENDING','Tripo':'HOLD','request':'Opened lower jaw must form the reference smooth curve; change this region alone, preserve Front cuteness.','reference':str(n.REFERENCE.relative_to(ROOT)),'reference_sha256':sha(n.REFERENCE),'unapproved_27_used':False})
def lower_delta(b,p,interior=False):
 # The existing opening moves the lower half down. Keep neutral, upper lip,
 # smile corners and every other expression exactly unchanged.
 opening=v.smooth(0,.006,b.z-p.z)
 locality=(1-v.smooth(.046,.074,abs(b.x)))*v.smooth(.525,.542,b.z)*(1-v.smooth(.600,.601,b.z))*v.smooth(-.180,-.245,b.y)
 if interior:locality=1.
 d=max(0.,.602-p.z)
 # Rounded recession from the fixed upper mouth to the lower rim, rather
 # than the old near-constant-depth plane. Blend through the existing skin.
 target=-.267+.34*d+2.7*d*d+2*p.x*p.x
 reference=-.266+2*p.x*p.x+.10*(p.z-.600)
 return max(0.,target-(reference if interior else p.y))*opening*locality
def refine():
 report={}
 for o in [v.parts['Head'],bpy.data.objects['Shushu_MouthInterior']]:
  keys=o.data.shape_keys.key_blocks;basis=keys['Basis'];rows={}
  for name in ['MouthOpen','MouthDonorOpen']:
   count=0;maximum=0.
   for i,p in enumerate(keys[name].data):
    delta=lower_delta(basis.data[i].co,p.co,o.name=='Shushu_MouthInterior')
    if delta>1e-10:p.co.y+=delta;count+=1;maximum=max(maximum,delta)
   rows[name]={'changed_vertices':count,'maximum_depth_recession':maximum}
  r.compose(o);report[o.name]=rows
 v.reset();return report
def render(version,state,kind,view,path=None):
 old=n.OUT;n.OUT=OUT
 info=n.render(f'{version}-{state}-{kind}',view,kind,state);n.OUT=old
 return info
def preview():
 for view in ['side','front','3q']:
  a.load(BACK/v.ASSET.name);info=refine();render('candidate','smile','colour',view)
 write('candidate.json',info);print('LOWER_MOUTH_PREVIEW_COMPLETE',flush=True)
def apply():
 inputs=json.loads((BACK/'inputs.json').read_text());old=json.loads((OUT/'continuity.json').read_text()) if (OUT/'continuity.json').exists() else {};saved={}
 for p in [v.ASSET,v.PROOF]:
  rel=p.relative_to(ROOT).as_posix();assert sha(p) in {inputs[rel],old.get('saved',{}).get(rel,{}).get('after')},('Concurrent saved asset change',rel)
 for p in [v.ASSET,v.PROOF]:
  a.load(BACK/p.name);info=refine();bpy.context.scene['LowerMouthRevision']='Opened lower lip rounded toward Human reference; other regions held; Human PENDING / Tripo HOLD'
  bpy.ops.wm.save_as_mainfile(filepath=str(p));rel=p.relative_to(ROOT).as_posix();saved[rel]={'before':inputs[rel],'after':sha(p),'local_edit':info}
 write('continuity.json',{'base':BASE,'Human':'PENDING','Tripo':'HOLD','saved':saved})
 a.load(v.ASSET);v.character=[o for o in v.character if not o.hide_render];v.export_static();shutil.copy2(v.OUT/'static-roundtrip.json',OUT/'static-roundtrip.json');print('LOWER_MOUTH_SAVED_COMPLETE',flush=True)
def final_renders():
 cameras={};old=json.loads((n.OUT/'cameras.json').read_text());tasks=[('smile','colour',q) for q in r.VIEWS]+[('smile','clay','side'),('small','colour','side'),('full','colour','side')]
 for version in ['before','after']:
  for state,kind,view in tasks:
   name=f'{version}-{state}-{kind}-{view}';previous=n.OUT/'renders'/f'after-{state}-{kind}-{view}.png'
   if version=='before' and previous.exists():
    (OUT/'renders').mkdir(exist_ok=True);shutil.copy2(previous,OUT/'renders'/(name+'.png'));cameras[name]=old['after-'+name[7:]];continue
   a.load(BACK/v.ASSET.name if version=='before' else v.ASSET);cameras[name]=render(version,state,kind,view)
 write('cameras.json',cameras);print('LOWER_MOUTH_RENDERS_COMPLETE',flush=True)
if __name__=='__main__':
 snapshot()
 if '--preview' in sys.argv:preview()
 if '--apply' in sys.argv:apply()
 if '--render' in sys.argv:final_renders()
