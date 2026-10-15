"""Package only bounded Pino-generated review images; never touch source assets."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import argparse,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/rig-v001'
p=argparse.ArgumentParser();p.add_argument('--family');p.add_argument('--preview',action='store_true');p.add_argument('--finalize',action='store_true');p.add_argument('--manifest',action='store_true');args=p.parse_args()
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
def write_manifest():
 asset=ROOT/'assets/grimo/production/pino/candidate-c/rig-v001'
 for path in asset.glob('*.blend1'):path.unlink()
 protected=[ROOT/'assets/grimo/production/pino/candidate-c/source/cute blue creature 3d model.fbx',ROOT/'assets/grimo/production/pino/candidate-c/source/cute blue creature 3d model.glb',*list((ROOT/'assets/grimo/source/pino').rglob('*.png'))]
 scripts=[ROOT/'scripts/3d/package-pino-base-rig-v001.py',*list((ROOT/'scripts/blender').glob('*pino*rig-v001.py')),ROOT/'scripts/blender/repair-pino-proof-support-v001.py']
 paths=sorted(set([p for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json']+[p for p in asset.rglob('*') if p.is_file()]+protected+scripts))
 manifest={'start_revision':'81432f9cf17836ed15eb4464baf710e5bbc44222','branch':'codex/pino-base-rig-v001-20261015','human_rig_geometry_gate':'PENDING','artifacts':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def row(paths,label):
 images=[Image.open(p).convert('RGB') for p in paths];w,h=images[0].size
 result=Image.new('RGB',(w*3,h+35),(235,239,245));draw=ImageDraw.Draw(result)
 for j,(im,view) in enumerate(zip(images,['FRONT','SIDE','3/4'])):
  result.paste(im,(j*w,35));draw.text((j*w+8,8),label+' / '+view,fill=(25,35,50),font=font)
 return result
if args.finalize:
 comparisons=[];rows=[]
 for label in ['reference','candidate']:
  rows.append(row([OUT/f'neutral-{label}-{v}.png' for v in ['front','side','threequarter']],label+' / Cycles 16spp'))
 sheet=Image.new('RGB',(rows[0].width,sum(r.height for r in rows)))
 for j,r in enumerate(rows):sheet.paste(r,(0,j*r.height))
 sheet.save(OUT/'neutral-comparison.png')
 for view in ['front','side','threequarter']:
  a=np.array(Image.open(OUT/f'neutral-reference-{view}.png').convert('RGB'),dtype=int);b=np.array(Image.open(OUT/f'neutral-candidate-{view}.png').convert('RGB'),dtype=int);d=abs(a-b)
  comparisons.append({'view':view,'changed_pixels':int(np.any(d!=0,axis=2).sum()),'max_channel_difference_8bit':int(d.max()),'mean_channel_difference_8bit':float(d.mean())})
 (OUT/'neutral-pixels.json').write_text(json.dumps(comparisons,indent=2)+'\n')
 records=json.loads((OUT/'deformation-metrics.json').read_text());summary={}
 for family in ['tail','eyes','paws','rest']:
  rows=[r for r in records if r['family']==family]
  summary[family]={'samples':len(rows),'below_floor_vertices_max':max(r['below_floor_vertices'] for r in rows),'min_z':min(r['z_min'] for r in rows),'edge_ratio_max':max(r['edge_ratio_max'] for r in rows),'edge_ratio_p99_max':max(r['edge_ratio_p99'] for r in rows),'tail_volume_ratio_range':[min(r['tail_volume_ratio'] for r in rows),max(r['tail_volume_ratio'] for r in rows)],'neutral_pixels':json.loads((OUT/f'{family}-return-pixels.json').read_text())}
 summary['high_five_endpoint_errors']={side:next(r for r in records if r['family']=='paws' and r['index']==idx)['paw_contact_error'][side] for side,idx in [('L',2),('R',6)]}
 summary['both_paw_min_gap_at_extreme']=next(r for r in records if r['family']=='paws' and r['index']==10)['distal_paw_gap']
 summary['rest_foot_contact_counts']=[r['floor_contacts']['hindfeet'] for r in records if r['family']=='rest']
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 rejected=Image.open(OUT/'rejected-deep-rest-context.png');rejected.crop((0,rejected.height-435,rejected.width,rejected.height)).save(OUT/'rejected-deep-rest.png')
 # Only our known, reproducible scratch/preview images are removed.
 for pattern in ['preview-*.png','neutral-reference-*.png','neutral-candidate-*.png','rejected-deep-rest-context.png']:
  for path in OUT.glob(pattern):
   assert path.parent.resolve()==OUT.resolve();path.unlink()
 write_manifest()
 print(json.dumps({'neutral_pixels':comparisons,'summary':summary}))
elif args.manifest:write_manifest()
elif args.preview:
 labels=['neutral','tail','blink','highfive','contact','rest'];rows=[row([OUT/f'preview-{label}-{v}.png' for v in ['front','side','threequarter']],label) for label in labels]
 sheet=Image.new('RGB',(rows[0].width,sum(r.height for r in rows)))
 for j,r in enumerate(rows):sheet.paste(r,(0,j*r.height))
 sheet.save(OUT/'preview-board.png')
elif args.family:
 scratch=OUT/'_scratch';paths=sorted(scratch.glob('*-front.png'));family=args.family
 frames=[row([scratch/f'{path.stem[:2]}-{v}.png' for v in ['front','side','threequarter']],f'{family} {j+1}/{len(paths)}') for j,path in enumerate(paths)]
 frames[0].save(OUT/f'{family}.gif',save_all=True,append_images=frames[1:],duration=180,loop=0,optimize=True)
 selected=({'tail':[0,2,6],'eyes':[0,2,4,7],'paws':[0,2,6,10],'rest':[0,2,4,6,8]})[family]
 sheet=Image.new('RGB',(frames[0].width,frames[0].height*len(selected)))
 for j,i in enumerate(selected):sheet.paste(frames[i],(0,j*frames[0].height))
 sheet.save(OUT/f'{family}-representatives.png')
 # Body pixels only: labels intentionally differ by sample number.
 first=[Image.open(scratch/f'00-{v}.png').convert('RGB') for v in ['front','side','threequarter']]
 last=[Image.open(scratch/f'{len(paths)-1:02d}-{v}.png').convert('RGB') for v in ['front','side','threequarter']]
 (OUT/f'{family}-return-pixels.json').write_text(json.dumps({'neutral_return_pixel_equal':all(ImageChops.difference(a,b).getbbox() is None for a,b in zip(first,last))},indent=2)+'\n')
 for path in scratch.glob('*.png'):
  assert path.parent.resolve()==(OUT/'_scratch').resolve();path.unlink()
