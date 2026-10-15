"""Unretouched fixed-camera evidence boards and source correspondence."""
import sys,json,hashlib,subprocess,importlib.util
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v003'
def write(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def board(name,cells,cols=4,crop=None,width=420):
    ims=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for label,path in cells:
        im=Image.open(path).convert('RGB')
        if crop:im=im.crop(crop)
        im=im.resize((width,round(im.height*width/im.width)))
        ims.append((label,im))
    h=max(im.height for _,im in ims)+32;canvas=Image.new('RGB',(cols*width,((len(ims)+cols-1)//cols)*h),(245,243,241));d=ImageDraw.Draw(canvas)
    for i,(label,im) in enumerate(ims):x=i%cols*width;y=i//cols*h;canvas.paste(im,(x,y));d.text((x+8,y+im.height+5),label,font=font,fill=(25,25,25))
    canvas.save(OUT/name)
def lineage():
    rows=[]
    source=np.load(OUT/'trace-v006.npz')['positions'];src=source[source[:,2]<.25]
    previous=None
    for tag in ['v006','lowpoly','autorig','v001','v002']:
        points=np.load(OUT/f'trace-{tag}.npz')['positions'];p=points[points[:,2]<.25];dist=cKDTree(src).query(p)[0]
        prevdist=cKDTree(previous).query(p)[0] if previous is not None else np.zeros(len(p))
        foot=p[(p[:,2]<.095)&(p[:,0]>.05)]
        rows.append({'stage':tag,'foot_bounds':[foot.min(0).tolist(),foot.max(0).tolist()],'foot_extent':np.ptp(foot,axis=0).tolist(),'lower_surface_to_static_max':float(dist.max()),'lower_surface_to_previous_max':float(prevdist.max()),'method':'One-sided nearest preserved surface positions below z=.25. Decimation changes sample density; not a bidirectional surface Hausdorff claim.'});previous=p
    write('lineage-comparison.json',rows)
    for view in ['front','left','3q-L','3q-R']:
        board(f'00-lineage-{view}.png',[(tag,OUT/'renders'/tag/f'neutral-{view}.png') for tag in ['v006','lowpoly','autorig','v001','v002']],5,width=400)
        board(f'00-feet-{view}.png',[(tag,OUT/'renders'/tag/f'neutral-{view}.png') for tag in ['v006','lowpoly','autorig','v001','v002']],5,crop=(150,395,490,620),width=400)
def iterations(tag):
    for view in ['front','left','3q-L','3q-R']:
        board(f'{tag}-support-{view}.png',[(label+' / '+name,folder/f'{name}-{view}.png') for name in ['seat-entry','seat-mid','seat'] for label,folder in [('v002',OUT.parent/'production-rig-v002/renders/candidate'),(tag,OUT/'renders'/tag)]],2,width=480)
    for view in ['front','3q-L','3q-R']:
        board(f'{tag}-eyes-{view}.png',[(label+' / '+name,folder/f'{name}-{view}.png') for name in ['seat-lowhead','seat-shift-L'] for label,folder in [('v002',OUT.parent/'production-rig-v002/renders/candidate'),(tag,OUT/'renders'/tag)]],2,crop=(125,155,525,425),width=600)
def textures():
    spec=importlib.util.spec_from_file_location('r',ROOT/'scripts/3d/report-shushu-production-rig-v001.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
    r.OUT=OUT;r.RIG=r.RIG.with_name('shushu-v006-production-rig-v003.glb')
    paths=[r.RIG,r.RIG.with_name(r.RIG.stem+'-proof.glb')]
    def numeric(path):
        j,raw=r.read(path);return hashlib.sha256(b''.join(r.accessor(j,raw,i).tobytes() for i in range(len(j['accessors'])))).hexdigest()
    before={str(path):numeric(path) for path in paths};r.restore_textures();after={str(path):numeric(path) for path in paths}
    assert before==after,'Numeric data changed during image-byte repack'
    # glTF omits an empty extensionsUsed property instead of emitting [].
    import struct
    for path in paths:
        j,raw=r.read(path)
        if j.get('extensionsUsed')==[]:
            del j['extensionsUsed'];meta=json.dumps(j,ensure_ascii=False,separators=(',',':')).encode();meta+=b' '*((-len(meta))%4)
            path.write_bytes(struct.pack('<III',0x46546c67,2,12+8+len(meta)+8+len(raw))+struct.pack('<II',len(meta),0x4e4f534a)+meta+struct.pack('<II',len(raw),0x004e4942)+raw)
    write('numeric-repack-invariance.json',{'before':before,'after':after});r.glb_audit()
def final_boards():
    states=['neutral','shift-L','shift-R','seat-entry','seat-mid','seat-three-quarter','seat','seat-rest','recovery-mid','standing-return']
    for view in ['front','left','3q-L','3q-R']:
        board(f'01-transition-{view}.png',[(state,OUT/'renders/candidate'/f'{state}-{view}.png') for state in states],5,width=400)
        board(f'02-v002-v003-{view}.png',[(label+' / '+name,folder/f'{name}-{view}.png') for name in ['seat-entry','seat-mid','seat-three-quarter','seat','seat-rest'] for label,folder in [('v002',OUT/'renders/v002'),('v003',OUT/'renders/candidate')]],2,width=480)
        board(f'03-reference-feet-{view}.png',[(label+' / '+state,folder/f'{state}-{view}.png') for label,folder,states0 in [('v006',OUT/'renders/v006',['neutral']),('v002',OUT/'renders/v002',['neutral','seat']),('v003',OUT/'renders/candidate',['neutral','seat'])] for state in states0],5,crop=(140,390,500,620),width=400)
    for state in states+['seat-lowhead','seat-shift-L']:
        board(f'view-{state}.png',[(state+' / '+view,OUT/'renders/candidate'/f'{state}-{view}.png') for view in ['front','left','3q-L','3q-R']],2,width=640)
    for view in ['front','3q-L','3q-R']:
        board(f'04-eye-detail-{view}.png',[(label+' / '+name,OUT/'detail'/folder/f'{name}-{view}.png') for name in ['seat-lowhead','seat-shift-L'] for label,folder in [('v002','v002'),('v003','candidate')]],2,width=650)
        board(f'05-face-regression-{view}.png',[(label+' / '+name,OUT/'detail'/folder/f'{name}-{view}.png') for name in ['neutral','half','closed','seat-rest','seat-joy'] for label,folder in [('v002','v002'),('v003','candidate')]],2,width=420)
    board('06-saved-glb.png',[(label+' / '+state,OUT/'renders'/folder/f'{state}-3q-L.png') for state in ['neutral','seat-mid','seat','seat-rest','seat-lowhead','seat-shift-L','standing-return'] for label,folder in [('editable','candidate'),('saved GLB','reimport')]],2,width=420)
def preserve():
    source=json.loads((OUT/'protected-inputs.json').read_text(encoding='utf-8'));changed=[];missing=[]
    for name,digest in source.items():
        path=ROOT/name
        if not path.exists():missing.append(name)
        elif hashlib.sha256(path.read_bytes()).hexdigest()!=digest:changed.append(name)
    write('protected-input-verification.json',{'inputs':len(source),'changed':changed,'missing':missing,'allowed':['docs/production/Handoff.md']})
    assert not missing and set(changed)<=set(['docs/production/Handoff.md']),'Protected input changed'
def manifest():
    files=sorted((ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging').glob('*production-rig-v003*'))
    write('delivery-manifest.json',{'date':'2026-10-15','assets':[{'path':str(path.relative_to(ROOT)).replace('\\','/'),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for path in files],'appearance_human':'PENDING; no Human approval is substituted','start_head':json.loads((OUT/'start-state.json').read_text())['head']})
if __name__=='__main__':
    if 'lineage' in sys.argv:lineage()
    if 'iterations' in sys.argv:iterations(sys.argv[-1])
    if 'textures' in sys.argv:textures()
    if 'boards' in sys.argv:final_boards()
    if 'preserve' in sys.argv:preserve()
    if 'manifest' in sys.argv:manifest()
