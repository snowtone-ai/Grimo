"""Compact boards, sampled transition GIFs, preservation and final file manifest."""
from pathlib import Path
import sys,json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];TMP=ROOT/'artifacts/pino-texture-v004';OUT=ROOT/'docs/production/pino/evidence/texture-handoff-v004';DEST=ROOT/'assets/grimo/production/pino/candidate-c/texture-handoff-v004'
FONT=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',19);SMALL=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',15)
def dump(n,x):(OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def tile(path,label,size=300):
 im=Image.new('RGB',(size,size+30),(25,30,37));src=Image.open(path).convert('RGB');src.thumbnail((size,size));im.paste(src,((size-src.width)//2,30+(size-src.height)//2));ImageDraw.Draw(im).text((8,4),label,font=SMALL,fill='white');return im

def board(name,rows,size=300):
 b=Image.new('RGB',(len(rows[0])*size,len(rows)*(size+30)),(25,30,37))
 for y,row in enumerate(rows):
  for x,(path,label) in enumerate(row):b.paste(tile(path,label,size),(x*size,y*(size+30)))
 b.save(OUT/name,optimize=True)
def scratch(prefix,view):return TMP/f'{prefix}-{view}.png'
def triptych(prefix,label,size=300):
 b=Image.new('RGB',(size*3,size+30),(25,30,37))
 for i,view in enumerate(['front','side','3q']):b.paste(tile(scratch(prefix,view),label+' / '+view,size),(i*size,0))
 return b

def main():
 board('identity-comparison.png',[
 [(ROOT/'assets/grimo/source/pino/pino-Identity-canonical.png','Canonical / authority'),(ROOT/'assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png','Approved body-only front'),(ROOT/'assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png','Approved body-only left')],
 [(scratch('source-neutral',v),'v003 saved Basis / '+v) for v in ['front','side','3q']],
 [(scratch('final-neutral',v),'v004 saved Basis / '+v) for v in ['front','side','3q']]],400)
 board('face-stages.png',[[(scratch('final-eye-'+str(b),view),f'blink {b} / {view}') for b in [0,.5,.75,.9,.97,1]] for view in ['front','side','3q']],240)
 board('body-probes.png',[[(scratch('final-'+state,view),state+' / '+view) for view in ['front','side','3q']] for state in ['contact-mid','contact','rest-mid','rest','tail-L','tail-R']],300)
 board('expressions.png',[[(scratch('final-mouth-'+str(c),view),'mouth closed='+str(c)+' / '+view) for c in [0,.35,.7,1]] for view in ['front','side','3q']],240)
 board('wink-combined.png',[[(scratch('final-face-'+state,view),state+' / '+view) for view in ['front','side','3q']] for state in ['wink','combined']],300)
 for name,frames in [
 ('blink-cycle.gif',[(f'final-eye-{b}',f'blink {b}') for b in [0,.25,.5,.75,.9,.97,1,.97,.9,.75,.5,.25,0]]),
 ('body-cycle.gif',[(f'final-{s}',s) for s in ['neutral','contact-mid','contact','contact-mid','neutral','rest-mid','rest','rest-mid','neutral','tail-L','neutral','tail-R','neutral']]),
 ('mouth-cycle.gif',[(f'final-mouth-{c}',f'closed {c}') for c in [0,.35,.7,1,.7,.35,0]])]:
  ims=[triptych(p,label).quantize(colors=128) for p,label in frames];ims[0].save(OUT/name,save_all=True,append_images=ims[1:],duration=[450 if i in [0,len(ims)-1] else 180 for i in range(len(ims))],loop=0,optimize=False)
 differences={}
 for view in ['front','side','3q']:
  a=np.array(Image.open(scratch('source-neutral',view)).convert('RGB')).astype(int);b=np.array(Image.open(scratch('final-neutral',view)).convert('RGB')).astype(int);d=abs(a-b);differences[view]=dict(changed_pixels=int(np.any(d,axis=2).sum()),max_channel_delta=int(d.max()),mean_channel_delta=float(d.mean()))
 dump('neutral-render-difference.json',differences)
 # Compare physical files with the committed source content/LFS object IDs.
 old=json.loads((ROOT/'docs/production/pino/evidence/texture-ready-v003/source-protection.json').read_text());paths=[x['path'] for x in old]+['assets/grimo/production/pino/candidate-c/texture-ready-v003/pino-c-texture-ready-v003-HOLD.'+x for x in ['blend','glb']]+['assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_'+x+'.png' for x in ['front','back','left','right']]
 protection=[]
 for path in paths:
  raw=subprocess.check_output(['git','show','1dd7980:'+path],cwd=ROOT)
  expected=raw.decode().split('oid sha256:')[1].splitlines()[0] if raw.startswith(b'version https://git-lfs.github.com/spec/v1') else hashlib.sha256(raw).hexdigest()
  actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest();protection.append(dict(path=path,expected_sha256=expected,actual_sha256=actual,matches=expected==actual))
 assert all(x['matches'] for x in protection);dump('source-protection.json',protection)
 finalize()

def finalize():
 # Reuse captured runtime output; no browser session or asset mutation required.
 raw=TMP/'runtime-raw.txt'
 if raw.exists():
  body=raw.read_text(encoding='utf8').split('### Result\n',1)[1].lstrip();r=json.JSONDecoder().raw_decode(body)[0]
  probes={s['name']:s for s in json.loads((OUT/'probe-controls.json').read_text())};C=np.array([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1.]])
  for row in r['records']:
   errors=[]
   for name,mat in zip(r['summary']['bone_names'],row.pop('skin_matrices')):
    actual=np.array(mat).reshape(4,4).T;expected=C@np.array(probes[row['name']]['skin_delta'][name])@C.T;errors.append(float(abs(actual-expected).max()))
   row['max_skin_matrix_error']=max(errors);row['changed_skin_matrices']=sum(not np.allclose(np.array(probes[row['name']]['skin_delta'][n]),np.eye(4),atol=1e-5) for n in r['summary']['bone_names'])
  assert max(x['max_skin_matrix_error'] for x in r['records'])<1e-5 and not r['summary']['errors']
  r['glb_sha256']=hashlib.sha256((DEST/'pino-c-v004-rigged-review.glb').read_bytes()).hexdigest()
  r['note']='Desktop Chromium / PlayCanvas 2.22.2; captured live skin matrices versus Blender world deformation deltas. Same local GLB URI and unchanged delivered file. No mobile/performance/full-Motion assertion.'
  dump('runtime-probe.json',r)
 if all((TMP/f'runtime-{n}.png').exists() for n in ['contact','rest','closed','wink']):
  board('runtime-comparison.png',[[(TMP/f'runtime-{n}.png','PlayCanvas / '+n) for n in row] for row in [['contact','rest'],['closed','wink']]],400)
 manifest=[]
 for p in sorted([*DEST.glob('*'),*OUT.glob('*')]):
  if p.is_file() and p.name!='file-manifest.json':manifest.append(dict(path=str(p.relative_to(ROOT)).replace('\\','/'),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 dump('file-manifest.json',manifest)

if __name__=='__main__':
 if '--finalize' in sys.argv:finalize()
 else:main()
