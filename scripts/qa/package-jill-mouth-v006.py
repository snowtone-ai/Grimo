"""Readable comparisons and reproducible local-mouth evidence packaging."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/mouth-integration-v006';R=E/'renders';A=ROOT/'assets/grimo/production/jill/tripo/mouth-integration-v006'
def write(name,data):(E/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def board(name,rows,width=320,crop=None):
    content=int(width*(crop[3]-crop[1])/(crop[2]-crop[0])) if crop else width
    height=content+28;out=Image.new('RGB',(len(rows[0])*width,len(rows)*height),(236,239,231));draw=ImageDraw.Draw(out)
    for y,row in enumerate(rows):
        for x,(p,label) in enumerate(row):
            im=Image.open(p).convert('RGB')
            if crop:im=im.crop(crop)
            if crop:im=im.resize((width,content),Image.Resampling.LANCZOS)
            else:im.thumbnail((width,content),Image.Resampling.LANCZOS)
            out.paste(im,(x*width+(width-im.width)//2,y*height+(content-im.height)//2));draw.text((x*width+7,y*height+content+5),label,fill=(24,40,28))
    out.save(E/name,quality=94)
board('before-after.jpg',[[(R/f'{label}-{state}-{view}.png',f'{label} {state} {view}') for label in ['before','after']] for state,view in [('neutral','front'),('neutral','3q'),('mouth-closed','3q'),('mouth-small','3q')]],400)
board('mouth-detail.jpg',[[(R/f'{label}-neutral-{view}.png',f'{label} {view}') for label in ['before','after']] for view in ['front','3q']],500,(155,300,475,540))
board('saved-states.jpg',[[(R/f'after-{state}-{view}.png',f'{state} {view}') for view in ['front','side','3q','left3q']] for state in ['neutral','mouth-closed','mouth-small','mouth-large','combined','recovery']],280)
board('overlap-sweep.jpg',[[(R/f'sweep-c{c}-o{o}-3q.png',f'close={c} open={o}; smile 1/.5') for o in [0,.5,1]] for c in [0,.25,.5,.75,1]],300)
board('interaction.jpg',[[(R/f'interaction-{s}-{view}.png',f'{s} {view}') for view in ['front','side','3q']] for s in ['touch-L','touch-R','touch-both-closed','head-left-open','head-right-closed','breath-closed']],280)
channels=json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())['authoring_properties']
if (R/'whole-neutral-back.png').exists():
    for offset in range(0,len(channels),8):
        rows=[]
        for channel in list(channels)[offset:offset+8]:
            values=sorted(set(channels[channel]['range'])-{0})
            if len(values)==1:values=[0]+values
            rows.append([((R/f'channel-{channel}-{value}-{view}.png') if value else R/f'whole-neutral-{view}.png',f'{channel} {value} {view}') for value in values for view in ['front','side','3q']])
        board(f'motion-envelope-{offset//8+1}.jpg',rows,200)
if (E/'direct-c1-o1.png').exists():
    board('runtime-direct-sweep.jpg',[[(E/f'direct-c{c}-o{o}.png',f'Live close={c} open={o}; smile 1/.5') for o in [0,.5,1]] for c in [0,.25,.5,.75,1]],500)
if (E/'static-direct-c1-o1.png').exists():
    board('static-runtime-mouth.jpg',[[(E/f'static-direct-c{c}-o{o}.png',f'Static GLB live: close={c}, open={o}') for c,o in row] for row in [[(0,0),(0,1)],[(.5,0),(.5,1)],[(1,0),(1,1)]]],650)
captures=sorted((ROOT/'output/playwright').glob('jill-v006-static-transition-*.png'))
if len(captures)==21:
    frames=[]
    for p in captures+list(reversed(captures[1:-1])):
        im=Image.open(p).convert('RGB');im.thumbnail((1000,500),Image.Resampling.LANCZOS);frames.append(im)
    frames[0].save(E/'runtime-mouth-transition.gif',save_all=True,append_images=frames[1:],duration=90,loop=0)
recovery={view:bool(np.array_equal(np.array(Image.open(R/f'after-neutral-{view}.png')),np.array(Image.open(R/f'after-recovery-{view}.png')))) for view in ['front','side','3q','left3q']};assert all(recovery.values());write('recovery.json',{'pass':True,'saved_render_pixel_exact':recovery})
protected=[]
for rel in ['assets/grimo/production/jill/tripo/texture-return-v005/jill-textured-rig-v005.blend','assets/grimo/production/jill/tripo/texture-return-v005/jill-textured-rig-v005.glb','assets/grimo/production/jill/tripo/texture-return-v005/jill-basecolor-v005.png','assets/grimo/production/jill/tripo/mouth-profile-v004/jill-rig-mouth-profile-v004.blend','assets/grimo/source/jill/jill-Identity-canonical.png']:
    p=ROOT/rel;old=subprocess.check_output(['git','rev-parse','74596c9:'+rel],cwd=ROOT,text=True).strip();now=subprocess.check_output(['git','hash-object',str(p)],cwd=ROOT,text=True).strip();assert old==now,rel;protected.append({'path':rel,'sha256':sha(p),'git_blob_unchanged':True})
write('protected-sources.json',{'pass':True,'files':protected})
write('Gate.json',{'result':'MOUTH_HUMAN_GO / FULL_MODEL_HOLD','full_goal_complete':False,'human_visual_go':True,'source_replaced':False,'mouth_band_w':'Removed in inspected Front/Side/left/right3Q and runtime states; Human mouth appearance GO received 2026-10-18','closure_small_large_recovery':'No recurrence of preceding trial defects in inspected cases','saved_blend':json.loads((E/'saved-blend-proof.json').read_text())['pass'],'local_preservation':json.loads((E/'local-preservation.json').read_text())['pass'],'fresh_glb':json.loads((E/'reimport-proof.json').read_text())['pass'],'bounded_runtime':json.loads((E/'runtime-validation.json').read_text())['pass'],'direct_runtime':json.loads((E/'direct-mouth-runtime.json').read_text())['pass'],'static_glb_live_controls':json.loads((E/'static-mouth-runtime-proof.json').read_text())['pass'],'invariants':{'bones':130,'authoring_channels':39,'morphs':20,'anchors':16},'human_decision':{'date':'2026-10-18','mouth':'GO','clover':'Add according to Canonical'},'remaining':['Existing eyelid/outer-corner appearance HOLD','Horn provisional boundary/colour','Canonical thigh clover addition authorized, not yet implemented','Full model Human appearance GO'],'certification_scope':'Focused authoring envelope and bounded desktop runtime; full motion production and real mobile are outside this repair certification'})
files=[p for p in E.rglob('*') if p.is_file() and p.name not in ['Manifest.json','RemoteReceipt.json']]+[p for p in A.glob('*') if p.is_file() and 'integrated-' not in p.name]
files += [ROOT/p for p in ['scripts/blender/jill-mouth-integration-v006.py','scripts/blender/jill-mouth-validate-v006.py','scripts/blender/audit-jill-mouth-v006.py','scripts/blender/verify-jill-mouth-glb-v006.py','scripts/qa/package-jill-mouth-v006.py','scripts/qa/verify-jill-mouth-runtime-v006.py','scripts/qa/capture-jill-mouth-v006.js','scripts/3d/jill-texture-v005/serve.mjs','scripts/3d/jill-texture-v005/viewer.mjs','scripts/3d/jill-mouth-v006/mouth-controller.mjs','scripts/3d/jill-mouth-v006/review-controls.mjs','docs/production/jill/HANDOFF.md','docs/production/jill/texture-return-v005/Evidence.md']]
write('Manifest.json',{'branch':'codex/jill-texture-return-v005-20261017','start_head':'74596c9673434f4120b300ec0c96fb9c663fc4d0','verified_main':'8b9d736abca118de5bd1e2e1f64b961e25f0ba42','status':'MOUTH_HUMAN_GO / FULL_MODEL_NOT_COMPLETE','hash_scope':'Workspace bytes excluding manifest/remote receipt; Git may normalize text endings','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(set(files))]})
print(json.dumps({'recovery':recovery,'protected_sources':len(protected),'files':len(files)},indent=2))
