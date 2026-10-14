"""Targeted independent byte/geometry checks and unretouched render boards."""
import json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/tripo-mouth-depth-v006'
sys.path.insert(0,str(ROOT/'scripts/3d'))
import importlib.util
spec=importlib.util.spec_from_file_location('mouth',ROOT/'scripts/3d/adjust-shushu-mouth-depth-v006.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
config=json.loads((OUT/'repair-config.json').read_text());record=json.loads((OUT/'geometry-validation.json').read_text())
raw,j,b,off=mod.read(ROOT/config['base']);other,j2,b2,off2=mod.read(ROOT/config['candidate']);assert raw[:off]==other[:off2];assert j==j2
assert sha(ROOT/config['candidate'])==record['candidate_sha256']
allowed=np.zeros(len(b),dtype=bool);stats={}
for node in j['nodes']:
 if 'mesh' not in node:continue
 pr=j['meshes'][node['mesh']]['primitives'][0];a=pr['attributes'];p=mod.accessor(j,b,a['POSITION']);q=mod.accessor(j2,b2,a['POSITION']);name=node['name']
 if name not in record['meshes']:
  for key,i in a.items():assert np.array_equal(mod.accessor(j,b,i),mod.accessor(j2,b2,i))
  continue
 ids=np.array(record['meshes'][name]['vertices']);normal_ids=np.array(record['meshes'][name]['normal_vertices']);assert np.array_equal(p[:,:2],q[:,:2])
 actual=np.flatnonzero(np.any(p!=q,axis=1));assert np.all(np.isin(actual,ids))
 for key,indices in [('POSITION',ids),('NORMAL',normal_ids)]:
  ac=j['accessors'][a[key]];v=j['bufferViews'][ac['bufferView']];start=v.get('byteOffset',0)+ac.get('byteOffset',0);stride=v.get('byteStride',12)
  for i in indices:allowed[start+i*stride:start+i*stride+12]=True
 faces=mod.accessor(j,b,pr['indices']).reshape(-1,3).astype(int);old=p[faces].astype(float);new=q[faces].astype(float)
 cross0=np.cross(old[:,1]-old[:,0],old[:,2]-old[:,0]);cross=np.cross(new[:,1]-new[:,0],new[:,2]-new[:,0]);touch=np.any(np.isin(faces,ids),axis=1)
 area0=np.linalg.norm(cross0,axis=1);area=np.linalg.norm(cross,axis=1);assert np.all(area[touch]>1e-12)
 assert np.array_equal(cross0[:,2],cross[:,2]) # unchanged signed front projection, no front folds
 normals=mod.accessor(j2,b2,a['NORMAL']);assert np.all(np.isfinite(normals));assert np.allclose(np.linalg.norm(normals[normal_ids],axis=1),1,atol=1e-5)
 stats[name]={'position_mask_vertices':len(ids),'actual_position_vertices':len(actual),'normal_vertices':len(normal_ids),'min_changed_triangle_area_ratio':float((area[touch]/area0[touch]).min()),'nondegenerate':True,'signed_front_projection_unchanged':True,'finite_unit_normals':True}
changed=np.frombuffer(b,dtype=np.uint8)!=np.frombuffer(b2,dtype=np.uint8)
assert not np.any(changed&~allowed)
textures=[]
for im in j['images']:
 v=j['bufferViews'][im['bufferView']];s=v.get('byteOffset',0);assert b[s:s+v['byteLength']]==b2[s:s+v['byteLength']];textures.append(hashlib.sha256(b[s:s+v['byteLength']]).hexdigest())
assert json.loads((OUT/'before-cameras.json').read_text())==json.loads((OUT/'candidate-cameras.json').read_text())
render_meta=json.loads((OUT/'candidate-render-source.json').read_text());assert render_meta['asset_sha256']==sha(ROOT/config['candidate'])
views=['front','left-three-quarter','right-three-quarter','left-side','right-side','left-oblique','right-oblique'];diffs={}
panel=Image.new('RGB',(1152,416*7),(245,242,239));draw=ImageDraw.Draw(panel)
for row,view in enumerate(views):
 old=np.array(Image.open(OUT/'renders'/f'before-{view}.png').convert('RGB'));new=np.array(Image.open(OUT/'renders'/f'candidate-{view}.png').convert('RGB'));delta=np.abs(old.astype(int)-new.astype(int));mask=np.any(delta!=0,axis=2);y,x=np.where(mask)
 diffs[view]={'changed_pixels':int(mask.sum()),'max_channel_delta':int(delta.max()),'bbox':[int(x.min()),int(y.min()),int(x.max()),int(y.max())] if len(x) else None}
 for col,(label,im) in enumerate([('v005',Image.fromarray(old)),('v006',Image.fromarray(new)),('difference x4',Image.fromarray(np.minimum(delta*4,255).astype('uint8')))]):
  draw.text((col*384+8,row*416+7),view+' / '+label,fill='#222222',font=font);panel.paste(im.resize((384,384)),(col*384,row*416+32))
panel.save(OUT/'01-seven-angle-before-v006-difference.png')
assert diffs['front']['max_channel_delta']<=3
front0=np.array(Image.open(OUT/'renders/before-front.png'));front1=np.array(Image.open(OUT/'renders/candidate-front.png'))
assert np.array_equal(front0[425:630,145:430],front1[425:630,145:430]);assert np.array_equal(front0[425:630,595:880],front1[425:630,595:880])
panel=Image.new('RGB',(1440,672),(245,242,239));draw=ImageDraw.Draw(panel)
refdir=ROOT/'assets/grimo/source/shushu/tripo-generation-pose';reference_records={}
for row,(side,refname,refbox,box) in enumerate([('left-side','right',(805,505,944,660),(827,590,952,740)),('right-side','left',(164,465,282,610),(72,590,197,740))]):
 refpath=refdir/f'shushu_bodyonly_{refname}.png';ref=Image.open(refpath);reference_records[side]={'path':refpath.relative_to(ROOT).as_posix(),'sha256':sha(refpath),'crop':refbox}
 cells=[('Approved Body-only',ref.crop(refbox)),('v005 / saved GLB',Image.open(OUT/'renders'/f'before-{side}.png').crop(box)),('v006 / saved GLB',Image.open(OUT/'renders'/f'candidate-{side}.png').crop(box))]
 for col,(label,im) in enumerate(cells):
  draw.text((col*480+8,row*336+5),side+' / '+label,fill='#222222',font=font);scale=min(450/im.width,300/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);panel.paste(im,(col*480+(480-im.width)//2,row*336+32))
panel.save(OUT/'02-reference-mouth-closeups.png')
shade0=json.loads((OUT/'before-shaded-render.json').read_text());shade1=json.loads((OUT/'candidate-shaded-render.json').read_text())
assert shade0['cameras']==shade1['cameras'] and shade1['asset_sha256']==sha(ROOT/config['candidate'])
assert all(shade0[k]==shade1[k] for k in ['resolution','samples','engine','color','lighting'])
panel=Image.new('RGB',(960,512*5),(245,242,239));draw=ImageDraw.Draw(panel)
for row,view in enumerate(views[:5]):
 for col,tag in enumerate(['before','candidate']):
  draw.text((col*480+8,row*512+5),view+' / '+('v005' if tag=='before' else 'v006')+' / original materials',fill='#222222',font=font);panel.paste(Image.open(OUT/'shaded'/f'{tag}-{view}.png').resize((480,480)),(col*480,row*512+32))
panel.save(OUT/'03-shaded-five-angle-before-v006.png')
protected=json.loads((OUT/'protected-inputs.json').read_text());changed_protected=[p for p,h in protected.items() if sha(ROOT/p)!=h];assert not changed_protected
result={'candidate_sha256':sha(ROOT/config['candidate']),'outside_allowed_byte_changes':0,'json_byte_identical':True,'textures_byte_identical':textures,'other_10_meshes_attributes_identical':True,'UV_indices_materials_nodes_accessors_metadata_identical':True,'front_eyes_pixel_identical':True,'front_render_difference':diffs['front'],'render_differences':diffs,'matched_cameras':True,'shaded_conditions_identical':True,'meshes':stats,'protected_inputs':len(protected),'changed_protected_inputs':changed_protected,'references':reference_records,'Human':'PENDING','boards':'crop/resize/layout only; no retouch of model renders or reference'}
(OUT/'targeted-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['textures_byte_identical','render_differences','references']},indent=2))
