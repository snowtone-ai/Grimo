"""Package a rejected local repair honestly, without replacing the source."""
from pathlib import Path
import json,hashlib,struct,subprocess
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/texture-return-v005/upper-w-local';R=E/'renders';A=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005'
def write(n,d):(E/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def board(name,rows,width=360):
    out=Image.new('RGB',(len(rows[0])*width,len(rows)*(width+28)),(237,239,230));draw=ImageDraw.Draw(out)
    for y,row in enumerate(rows):
        for x,(path,label) in enumerate(row):
            img=Image.open(path).convert('RGB');img.thumbnail((width,width),Image.Resampling.LANCZOS);out.paste(img,(x*width+(width-img.width)//2,y*(width+28)+(width-img.height)//2));draw.text((x*width+8,y*(width+28)+width+6),label,fill=(25,40,30))
    out.save(E/name,quality=94)
board('before-after-detail.jpg',[[(R/f'{label}-detail-{view}.png',f'{label} neutral {view}') for label in ['before','after']] for view in ['front','3q']],540)
board('before-after-states.jpg',[[(R/f'{label}-{state}-{view}.png',f'{label} {state} {view}') for view in ['front','side','3q'] for label in ['before','after']] for state in ['mouth-closed','mouth-small','mouth-large']],260)
board('saved-states.jpg',[[(R/f'after-{state}-{view}.png',f'after {state} {view}') for view in ['front','side','3q','left3q']] for state in ['neutral','mouth-closed','mouth-small','mouth-large','combined','recovery']],320)
recover={view:bool(np.array_equal(np.array(Image.open(R/f'after-neutral-{view}.png')),np.array(Image.open(R/f'after-recovery-{view}.png')))) for view in ['front','side','3q','left3q']};assert all(recover.values())
write('recovery.json',{'pixel_exact_by_view':recover,'pass':True})
source=np.array(Image.open(A/'jill-basecolor-v005.png').convert('RGBA'));dest=np.array(Image.open(A/'jill-basecolor-upper-w-local-v005.png').convert('RGBA'));assert np.array_equal(source[:,:,:3],dest[:,:,:3]);assert np.count_nonzero(dest[:,:,3]!=255)==2918
write('texture-delta.json',{'rgb_exact':True,'alpha_zero_texels':2918,'other_alpha':255,'all_uv_unchanged':True})
delta=json.loads((E/'geometry-delta.json').read_text());delta['method']='Only auxiliary upper collar/bowl/teeth and closed contact candidate edited. Original body coordinates unchanged; original internal texels masked separately, never recessed.'
if 'legacy_internal_ids' in delta:delta['legacy_excluded_from_exterior_probe_ids']=delta.pop('legacy_internal_ids')
write('geometry-delta.json',delta)
sources=[A/'jill-textured-rig-v005.blend',A/'jill-textured-rig-v005.glb',A/'jill-basecolor-v005.png',A/'source/tripo-return-original.glb',ROOT/'assets/grimo/production/jill/tripo/mouth-profile-v004/jill-rig-mouth-profile-v004.blend',ROOT/'assets/grimo/source/jill/jill-Identity-canonical.png']
protected=[]
for path in sources:
    rel=path.relative_to(ROOT).as_posix();blob=subprocess.check_output(['git','rev-parse','c404347:'+rel],cwd=ROOT,text=True).strip();now=subprocess.check_output(['git','hash-object',str(path)],cwd=ROOT,text=True).strip();assert blob==now,rel;protected.append({'path':rel,'sha256':sha(path),'git_blob_unchanged':True})
write('protected-sources.json',{'pass':True,'files':protected})
b=(A/'jill-upper-w-local-v005.glb').read_bytes();g=json.loads(b[20:20+struct.unpack_from('<I',b,12)[0]]);masks=[{'name':m['name'],'mode':m.get('alphaMode'),'cutoff':m.get('alphaCutoff',.5)} for m in g['materials'] if m.get('alphaMode')];assert masks==[{'name':'JILL_body_skin','mode':'MASK','cutoff':.5}]
write('Gate.json',{'result':'HOLD_REPAIR_FAILED','task_complete':False,'promote_candidate':False,'human_visual_go':False,'neutral_large_open_band':'Removed in the limited rendered views; upper contour follows W','closed_small':'FAIL: wrinkles/intersections at corners and auxiliary lower collar; visible in saved render and runtime','side':'HOLD: oral wall surface protrudes visibly','rig_counts':{'bones':130,'channels':39,'morphs':20,'anchors':16},'uv_topology_weights_drivers':'Preserved','original_body_all_21_keys':'Exact','fresh_glb':'PASS for data transport only; not appearance','runtime':'PASS bounded data integrity / FAIL visual closure','alpha_materials':masks,'recovery':recover,'scope_limitation':'Closed-contact trial affects auxiliary lower mouth collar; not accepted as a completed upper-mouth-only repair. Original source remains active.'})
assets=[A/n for n in ['jill-basecolor-upper-w-local-v005.png','jill-upper-w-local-v005.blend','jill-upper-w-local-v005.glb','jill-upper-w-review-bounded-v005.glb']]
scripts=[ROOT/p for p in ['scripts/blender/jill-upper-w-local-v005.py','scripts/blender/verify-jill-upper-w-local-v005.py','scripts/qa/jill-upper-w-mask-v005.py','scripts/qa/verify-jill-upper-w-runtime-v005.py','scripts/qa/package-jill-upper-w-v005.py','scripts/3d/jill-texture-v005/serve.mjs']]
files=assets+scripts+[ROOT/'docs/production/jill/HANDOFF.md',ROOT/'docs/production/jill/texture-return-v005/Evidence.md']+[p for p in E.rglob('*') if p.is_file() and p.name not in ['Manifest.json','RemoteReceipt.json']]
write('Manifest.json',{'branch':'codex/jill-texture-return-v005-20261017','start_head':'c4043471dbac3e58a39603802ecd18794a2bb9d6','verified_main':'336997db2b95244c17774258e2f5ff874a2adbc1','result':'HOLD_REPAIR_FAILED','hash_scope':'Workspace bytes, excluding manifest and later remote receipt. Text may be normalized by Git.','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(set(files))]})
print(json.dumps({'result':'HOLD_REPAIR_FAILED','recovery':recover,'files':len(files),'protected_sources':len(protected)},indent=2))
