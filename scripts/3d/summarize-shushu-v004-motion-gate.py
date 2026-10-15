"""Build evidence boards from actual renders and aggregate measured results."""
from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready';F=D/'final-v002'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
def board(name,columns,rows,size=256,crop=None):
 height=round(size*(crop[3]-crop[1])/(crop[2]-crop[0])) if crop else size
 im=Image.new('RGB',(size*len(columns),(height+28)*len(rows)+32),'#f2f0ed');draw=ImageDraw.Draw(im)
 for i,(label,_) in enumerate(columns):draw.text((i*size+8,6),label,font=font,fill='#222222')
 for j,(label,stem) in enumerate(rows):
  for i,(_,folder) in enumerate(columns):
   p=folder/(stem+'.png');src=Image.open(p).convert('RGB')
   if crop:src=src.crop(crop)
   if crop:src=src.resize((size,height),Image.Resampling.LANCZOS)
   else:src.thumbnail((size,size))
   x=i*size+(size-src.width)//2;y=32+j*(height+28)
   im.paste(src,(x,y));draw.text((i*size+8,y+height+3),label,font=font,fill='#222222')
 im.save(F/name)
if __name__=='__main__':
 p=np.load(D/'muzzle-retopo.npz');t=p['patch_tri'];c=p['closed'];o=p['opened'];rows=[];last=None;maxstep=0.
 for a in np.linspace(0,1,101):
  q=c*(1-a)+o*a;n=np.cross(q[t[:,1]]-q[t[:,0]],q[t[:,2]]-q[t[:,0]])
  rows.append({'open':float(a),'xz_reversed_faces':int((n[:,1]>1e-12).sum()),'zero_area_faces':int((np.linalg.norm(n,axis=1)<1e-12).sum())})
  if last is not None:maxstep=max(maxstep,float(np.linalg.norm(q-last,axis=1).max()))
  last=q
 write(F/'aperture-sweep.json',{'samples':101,'finite':bool(np.isfinite(c).all() and np.isfinite(o).all()),'max_step_per_001_open':maxstep,'rows':rows,'scope':'Local patch orientation/finite continuity only. Not a collision/appearance PASS.'})
 assert not any(x['xz_reversed_faces'] or x['zero_area_faces'] for x in rows)
 columns=[('Blender authored',F/'author'),('Saved GLB / Blender',F/'saved'),('PlayCanvas / PC',F/'desktop'),('Xiaomi 14T Pro',F/'phone')]
 board('compare-mouth-front.png',columns,[(n,n+'-front') for n in ['closed','small','medium','large']])
 board('compare-mouth-views.png',[('Before / mouth B v001',D.parent/'production-rig-v004-mouth-b'/'author'),('Stem removed / gate v001',D/'phone'),('Final candidate / v002',F/'phone')],[(v,'closed-'+v) for v in ['front','side','3q']],320)
 board('compare-face-detail.png',[('Before / gate v001',D/'phone'),('Final candidate / v002',F/'phone')],[('Actual phone mouth crop','closed-front')],400,(175,325,465,510))
 board('compare-forelimb.png',[('Before normals / PC',D/'desktop-source-normals'),('Blender authored',D/'author'),('Saved GLB / Blender',D/'saved'),('Corrected / PC',F/'desktop'),('Corrected / Xiaomi',F/'phone')],[(n,n+'-side') for n in ['offer','self','hold','seat-hold']])
 board('compare-crown.png',[('Before / gate v001',D/'phone'),('Final candidate / v002',F/'phone')],[('Actual phone crown crop','closed-front')],400,(180,15,410,120))
 gpu=[]
 for platform in ['desktop','phone']:
  for file in sorted((F/platform).glob('gpu-*.json')):
   data=read(file)
   for row in data['captures']:gpu.append({'platform':platform,'frame':data['frame'],**row})
 perf={}
 for platform in ['desktop','phone']:
  x=read(F/platform/'performance.json');perf[platform]={k:v for k,v in x.items() if k not in ['intervals','normalCpuTimes','summary']}
 glb=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v002.glb'
 write(F/'measured-summary.json',{'candidate_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'candidate_bytes':glb.stat().st_size,'roundtrip':{k:v for k,v in read(F/'saved-roundtrip.json').items() if k!='rows'},'gpu':gpu,'performance':perf,'human':'PENDING','motion_production':'HOLD; local appearance confirmation and remaining defects must be resolved'})
