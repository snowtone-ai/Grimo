"""Assemble focused before/after evidence and verify protected source hashes."""
from pathlib import Path
import json,hashlib,importlib.util,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/tripo-gem-cleanup-v002';PREV=OUT.with_name('tripo-gem-cleanup-v001')
DEST=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v002';TMP=ROOT/'artifacts/pino-gem-cleanup-v002'
def write(n,d):(OUT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
def board(path,cols,rows,w,h):
 im=Image.new('RGB',(cols*w,rows*(h+42)),(244,244,242));return im,ImageDraw.Draw(im)
def place(board,draw,path,x,y,w,h,label):
 board.paste(Image.open(path).convert('RGB').resize((w,h),Image.Resampling.LANCZOS),(x,y+42));draw.text((x+14,y+8),label,font=font,fill='black')
im,draw=board(OUT,2,1,800,800)
place(im,draw,PREV/'before-face-close.png',0,0,800,800,'Before / original donor')
place(im,draw,OUT/'after-face-close.png',800,0,800,800,'After / saved repaired donor')
im.save(OUT/'01-face-before-after.png')
im,draw=board(OUT,3,2,500,500)
for col,view in enumerate(['front','left-3q','right-3q']):
 place(im,draw,PREV/f'before-{view}.png',col*500,0,500,500,'Before / '+view)
 place(im,draw,OUT/f'after-{view}.png',col*500,542,500,500,'After / '+view)
im.save(OUT/'02-three-view-before-after.png')
im,draw=board(OUT,3,1,550,550)
for col,(path,label) in enumerate([(PREV/'before-face-close.png','Original'),(OUT/'texture-only-face-close.png','Texture only / contact remains'),(OUT/'after-face-close.png','Texture + local depth repair')]):place(im,draw,path,col*550,0,550,550,label)
im.save(OUT/'03-cause-and-repair.png')
rows=[];boxes={'front':(385,510,515,600),'face-close':(275,395,625,625),'left-3q':(645,510,765,600),'right-3q':(135,510,255,600)}
for view,box in boxes.items():
 a=np.array(Image.open(PREV/f'before-{view}.png'));b=np.array(Image.open(OUT/f'after-{view}.png'));diff=np.any(a!=b,2);y,x=np.where(diff)
 mask=np.zeros(diff.shape,bool);x0,y0,x1,y1=box;mask[y0:y1,x0:x1]=True
 outside=int((diff&~mask).sum());assert outside==0
 rows.append({'view':view,'changed_pixels':int(diff.sum()),'changed_bounds_xyxy':[int(x.min()),int(y.min()),int(x.max()),int(y.max())],'allowed_mouth_rectangle_xyxy':box,'changed_pixels_outside_mouth':outside})
write('render-difference.json',rows)
frames=[Image.open(TMP/'orbit'/f'{i:02d}-final.png').convert('RGB') for i in range(15)];loop=frames+frames[-2:0:-1]
loop[0].save(OUT/'04-mouth-orbit.gif',save_all=True,append_images=loop[1:],duration=120,loop=0)
sheet=Image.new('RGB',(5*256,3*286),'#f4f4f2');d=ImageDraw.Draw(sheet)
for i,frame in enumerate(frames):
 x=(i%5)*256;y=(i//5)*286;sheet.paste(frame.resize((256,256)),(x,y+30));d.text((x+10,y+3),f'{-35+i*5:+d} degrees',font=font,fill='black')
sheet.save(OUT/'05-orbit-contact-sheet.png')
# Source files must still match the committed protection record from diagnosis.
existing=Path('C:/Users/chidj/.codex/worktrees/pino-pretexture-v005/Grimo');prior=json.loads((PREV/'protection.json').read_text());protected=[]
for row in prior['protected']:
 p=existing/row['path'];actual=sha(p);expected=row['expected_committed_sha256'];protected.append({'path':str(p),'sha256':actual,'matches_committed':actual==expected})
donor=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v001/pino-c-v005-tripo-donor-original.glb'
original=Path('C:/Users/chidj/project/プロダクト/Grimo/pino-c-v005-tripo-output.glb.glb')
assert all(r['matches_committed'] for r in protected)
assert sha(donor)==sha(original)==prior['archive_sha256']
write('protection.json',{'files':protected,'all_match':True,'original_donor_sha256':sha(original),'archived_donor_sha256':sha(donor),'original_and_archive_unchanged':True,'master_applied':False})
# Saved payload and material checks; no export round-trip or donor Master transplant.
spec=importlib.util.spec_from_file_location('gl',ROOT/'scripts/3d/package-pino-texture-ready-v003.py');gl=importlib.util.module_from_spec(spec);spec.loader.exec_module(gl)
g,b=gl.read(DEST/'pino-c-v005-tripo-gem-cleaned-v002.glb');sg,sb=gl.read(donor)
assert g['materials']==sg['materials'] and g['nodes']==sg['nodes'] and g['meshes']==sg['meshes']
assert all(np.isfinite(gl.accessor(g,b,i)).all() for i in range(len(g['accessors'])))
write('saved-glb-check.json',{'materials_nodes_mesh_definitions_exact':True,'all_accessors_finite':True,'mesh_count':len(g['meshes']),'all_regular_meshes_retained':True,'candidate_sha256':sha(DEST/'pino-c-v005-tripo-gem-cleaned-v002.glb'),'image_return_not_applied':True})
# Remove only obsolete raw frames from this task's earlier evidence location.
old_orbit=OUT/'orbit'
if old_orbit.is_dir():
 for i in range(15):
  for tag in ['final','control']:
   p=old_orbit/f'{i:02d}-{tag}.png'
   if p.is_file():p.unlink()
 if not any(old_orbit.iterdir()):old_orbit.rmdir()
paths=[p for p in OUT.iterdir() if p.is_file() and p.name!='file-manifest.json']+[p for p in DEST.iterdir() if p.is_file()]
write('file-manifest.json',{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in paths})
print('EVIDENCE_AND_PROTECTION_VERIFIED')
