"""Compose current render evidence and hash the scoped deliverables."""
from pathlib import Path
import json,hashlib,datetime
import numpy as np
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/texture-return-v005';A=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005';R=E/'renders'
def board(name,rows,width=420):
    canvas=Image.new('RGB',(len(rows[0])*width,len(rows)*(width+32)),(237,239,230));draw=ImageDraw.Draw(canvas)
    for y,row in enumerate(rows):
        for x,(p,label) in enumerate(row):
            im=Image.open(p).convert('RGB');im.thumbnail((width,width),Image.Resampling.LANCZOS);canvas.paste(im,(x*width+(width-im.width)//2,y*(width+32)+(width-im.height)//2));draw.text((x*width+8,y*(width+32)+width+8),label,fill=(25,40,30))
    canvas.save(E/name,quality=94)
states=['neutral','blink-half','blink-full','mouth-closed','mouth-small','mouth-large']
board('candidate-face-review.jpg',[[(R/f'candidate-{s}-{v}.png',f'v005 {s} {v}') for v in ['front','side','3q']] for s in states])
board('raw-vs-repaired.jpg',[[(R/f'{prefix}-{s}-{v}.png',f'{prefix} {s} {v}') for v in ['front','3q'] for prefix in ['raw','candidate']] for s in ['neutral','blink-full','mouth-closed']])
board('body-motion-review.jpg',[[(R/f'candidate-{s}-{v}.png',f'v005 {s} {v}') for v in ['front','side','3q','back3q']] for s in ['wings-open','wings-fold','tail','combined']],360)
board('authority-comparison.jpg',[
    [(ROOT/'assets/grimo/source/jill/jill-Identity-canonical.png','Canonical / clover on visible thigh'),(ROOT/'assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png','Approved Body-only / front'),(ROOT/'assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png','Approved Body-only / right')],
    [(R/'candidate-body-3q.png','v005 / texture candidate / 3Q'),(R/'candidate-neutral-front.png','v005 / face / front'),(R/'candidate-tail-side.png','v005 / tail review / side')]
],500)
if (E/'reimport-proof.json').exists():
    board('saved-vs-reimport.jpg',[[(R/f'{prefix}-{s}-3q.png',f'{prefix} {s}') for prefix in ['candidate','reimport']] for s in ['neutral','blink-full','mouth-closed','mouth-large']],480)
for n,src in [('original-basecolor-preview.png',A/'source/original-basecolor-0.jpg'),('repaired-atlas-preview.png',A/'jill-basecolor-v005.png')]:
    im=Image.open(src);im.thumbnail((1024,1024));im.save(E/n)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
protected={
 'v004_rig':ROOT/'assets/grimo/production/jill/tripo/mouth-profile-v004/jill-rig-mouth-profile-v004.blend',
 'v004_neutral_glb':ROOT/'assets/grimo/production/jill/tripo/mouth-profile-v004/jill-texture-input-neutral-v004.glb',
 'canonical':ROOT/'assets/grimo/source/jill/jill-Identity-canonical.png'}
source_expected={'v004_rig':'df3891bbd11c522631202e0dd32945a788ff370477731568514261a5e4100cb7','v004_neutral_glb':'4646cffdff8248e6e74b1dcd5f1c6095e7ed7af2b7ad7771001c9b22aa662eb2','canonical':'a1812e4a450ae2d1b54c2bc78fc2ebedbf9a26be597438d4ace4a327bd309d15'}
protection={n:{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'unchanged':sha(p)==source_expected[n]} for n,p in protected.items()};assert all(x['unchanged'] for x in protection.values())
assert sha(A/'source/tripo-return-original.glb')=='e5a76605ca3e6a6f43bc6dc9875d88923cfe3e07b44f3439a9c05e987b1cc117'
correspondence=json.loads((E/'correspondence.json').read_text());preservation=json.loads((E/'preservation.json').read_text());reimport=json.loads((E/'reimport-proof.json').read_text());assert all(x['pass'] for x in [correspondence,preservation,reimport])
with np.load(E/'face-owner-correspondence.npz') as p:uv=p['source_uv'];ret=p['returned_uv_in_source_order']
area=lambda v:abs((v[:,1,0]-v[:,0,0])*(v[:,2,1]-v[:,0,1])-(v[:,1,1]-v[:,0,1])*(v[:,2,0]-v[:,0,0]))/2
bad=area(ret)<1e-14
gate={'correspondence':'PASS_BIDIRECTIONAL_TRIANGLE_BIJECTION','rig_preservation':'PASS_IMAGE_ONLY_DERIVATIVE','fresh_glb_face_roundtrip':'PASS_BOUNDED_SCOPE','human_v004_shape_go':'User explicitly reports GO in current task','human_texture_appearance':'HOLD','full_motion_production':'NOT_RUN','general_39_channel_runtime_solver':'NOT_PROVEN_BY_BAKED_REVIEW','normal_orm':'Not present / not adopted','texture_limitations':{'quantized_return_uv_step':1/4096,'quantized_return_uv_step_exact':bool(np.max(abs(ret*4096-np.rint(ret*4096)))==0),'collapsed_return_uv_faces':int(bad.sum()),'collapsed_source_area_4k_texel_squared':float(area(uv)[bad].sum()*4096**2),'largest_collapsed_source_face_4k_texel_squared':float(area(uv)[bad].max()*4096**2)},'hold_items':['Canonical visible-thigh clover is absent in return. Approved Body-only views omit it; new placement/mask requires Human resolution. No speculative duplication or new artwork.','Closed-lid raised rims / outer-corner gap remain in preserved v004 geometry. No printed open eyes; visual acceptance remains Human.','Peach/pink horn repair uses Canonical tongue hue on a bounded returned cream region. Horn/leaf boundary and colour need Human review.','Local cream/green skin continuity and PBR lighting must receive Human appearance judgment; sampled colours are not an approved RGB palette.']}
runtime=E/'playcanvas-runtime.json'
if runtime.exists():
    data=json.loads(runtime.read_text());gate['playcanvas']={'engine':data['engine'],'scope':data['scope'],'mesh_instances':data['meshInstances'],'skin_instances':data['skinInstances'],'morph_targets':sorted(set(data['morphTargets'])),'anchors':len(data['anchors']),'errors':data['errors'],'sample_tags':sorted(set(s['tag'] for s in data['samples']))}
(E/'Gate.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
files=list(A.rglob('*'))+list(E.rglob('*'))+[ROOT/'docs/production/jill/HANDOFF.md']+list((ROOT/'scripts/3d/jill-texture-v005').glob('*'))+[ROOT/p for p in ['scripts/blender/audit-jill-tripo-return-v005.py','scripts/blender/jill-texture-review-v005.py','scripts/blender/verify-jill-texture-glb-v005.py','scripts/qa/transfer-jill-basecolor-v005.py','scripts/qa/package-jill-texture-v005.py','scripts/qa/verify-jill-runtime-v005.py']]
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_head':'3e40a529cee78c521b1de703c2257953e7e4f6f1','authority_main_at_start':'8b5d13bc38061c0d574444416a039e70b9c61930','branch':'codex/jill-texture-return-v005-20261017','intake_actual_filename':'jill-texture-input-neutral-v004.glb.glb','intake_requested_filename':'jill-texture-input-neutral-v004.glb(1).glb','protected_sources':protection,'hash_scope':'Raw workspace bytes; excludes Manifest itself and later RemoteReceipt. Text normalization may differ in git.','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(set(files)) if p.is_file() and p.name not in ['Manifest.json','RemoteReceipt.json']]}
(E/'Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(gate,ensure_ascii=False,indent=2))
