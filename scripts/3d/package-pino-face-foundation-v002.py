"""Small contact sheets/GIFs; removes only this task's named temporary frames."""
import json, sys, hashlib, struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/pino/evidence/face-foundation-v002'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)

def row(paths,labels,size=360):
    board=Image.new('RGB',(size*len(paths),size+30),'#202735');d=ImageDraw.Draw(board)
    for i,(p,label) in enumerate(zip(paths,labels)):
        im=Image.open(p).convert('RGB');im.thumbnail((size,size))
        board.paste(im,(i*size,30));d.text((i*size+10,6),label,font=FONT,fill='white')
    return board

def preview():
    rows=[]
    for label in ['basis','closed','half','lids','wink-large']:
        paths=[OUT/f'_pass1-{label}-{v}.png' for v in ['front','side','3q']]
        if not all(p.exists() for p in paths):return
        rows.append(row(paths,[f'{label} / {v}' for v in ['front','side','3q']],320))
    board=Image.new('RGB',(960,350*len(rows)))
    for i,r in enumerate(rows):board.paste(r,(0,i*350))
    board.save(OUT/'_pass1-board.png')

def sections():
    a=np.load(OUT/'_audit.npz');v=a['vertices'];t=a['triangles']
    tri=v[t];board=Image.new('RGB',(1100,680),'white');d=ImageDraw.Draw(board)
    d.text((20,8),'Pino C mouth / actual source mesh sections (original scene units)',font=FONT,fill='black')
    for col,plane in enumerate([0,.025]):
        mask=(tri[:,:,0].min(1)<=plane)&(tri[:,:,0].max(1)>=plane)
        seg=[]
        for points in tri[mask]:
            hits=[]
            for p,q in zip(points,np.roll(points,-1,axis=0)):
                if (p[0]-plane)*(q[0]-plane)<0:
                    r=p+(q-p)*(plane-p[0])/(q[0]-p[0]);hits.append(r[1:])
            if len(hits)==2:seg.append(hits)
        d.text((col*550+30,50),f'X = {plane:.3f} / Y front < / Z up',font=FONT,fill='black')
        def pixel(p):return (col*550+60+(p[0]+.44)*4000,620-(p[1]-.50)*3400)
        for p,q in seg:
            if min(p[1],q[1])>.498 and max(p[1],q[1])<.652 and min(p[0],q[0])>-.442 and max(p[0],q[0])<-.338:
                d.line([pixel(p),pixel(q)],fill='#246392',width=2)
        for z in [.50,.55,.60,.65]:
            yy=pixel((-.44,z))[1];d.text((col*550+5,yy-10),f'{z:.2f}',font=FONT,fill='#444444')
        for y in [-.44,-.40,-.36]:d.text((pixel((y,.50))[0]-20,640),f'{y:.2f}',font=FONT,fill='#444444')
    board.save(OUT/'mouth-sections.png')

def save_rows(name,rows):
    board=Image.new('RGB',(rows[0].width,sum(r.height for r in rows)))
    y=0
    for r in rows:board.paste(r,(0,y));y+=r.height
    board.save(OUT/name)

def dump(name,x):
    (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def pixels(a,b):
    a=np.asarray(Image.open(a).convert('RGB')).astype(int)
    b=np.asarray(Image.open(b).convert('RGB')).astype(int)
    d=abs(a-b)
    return {'changed_pixels':int(np.any(d,axis=2).sum()),'pixels':int(d.shape[0]*d.shape[1]),'max_channel_delta':int(d.max())}

def finalize():
    views=['front','side','3q']
    save_rows('basis-comparison.png',[row([OUT/f'_{name}-basis-{v}.png' for v in views],
        [f'{name} / {v}' for v in views],300) for name in ['original','candidate','reimport']])
    save_rows('face-representatives.png',[row([OUT/'_frames'/f'{frame:03d}-{v}.png' for v in views],
        [f'{label} / {v}' for v in views],300) for frame,label in [(7,'Closed (HOLD)'),(25,'Large'),(85,'Both half'),(109,'Closed eyes + large')]])
    row([OUT/f'_source-{v}.png' for v in views]+[OUT/'_source-cutaway.png'],
        ['Source front','Source side','Source 3q','Source cutaway'],300).save(OUT/'source-audit.png')
    row([OUT/f'_pass1-closed-{v}.png' for v in views],['Rejected pass 1 / '+v for v in views],300).save(OUT/'rejected-pass1.png')
    timeline=json.loads((OUT/'timeline.json').read_text(encoding='utf-8'))
    frames=[]
    for f in timeline['gif_samples']:
        label=next(label for ff,label,args in reversed(timeline['states']) if ff<=f)
        im=row([OUT/'_frames'/f'{f:03d}-{v}.png' for v in views],views,300)
        board=Image.new('RGB',(900,365),'#202735');board.paste(im,(0,35))
        ImageDraw.Draw(board).text((10,7),f'{f:03d}  {label} | eye ownership tint only / NO TEXTURE',font=FONT,fill='white')
        frames.append(board.quantize(colors=128))
    frames[0].save(OUT/'face-proof.gif',save_all=True,append_images=frames[1:],duration=160,loop=0,disposal=2,optimize=False)
    diff={'original_vs_v002':{},'v001_vs_v002':{},'v002_vs_glb_reimport':{},'gif_basis_returns':{}}
    for v in views:
        diff['original_vs_v002'][v]=pixels(OUT/f'_original-basis-{v}.png',OUT/f'_candidate-basis-{v}.png')
        diff['v001_vs_v002'][v]=pixels(OUT/f'_source-{v}.png',OUT/f'_candidate-basis-{v}.png')
        diff['v002_vs_glb_reimport'][v]=pixels(OUT/f'_candidate-basis-{v}.png',OUT/f'_reimport-basis-{v}.png')
        diff['gif_basis_returns'][v]={str(f):pixels(OUT/'_frames'/f'001-{v}.png',OUT/'_frames'/f'{f:03d}-{v}.png') for f in [37,43,61,79,97,121]}
    dump('pixels.json',diff)
    saved=json.loads((OUT/'saved-checks.json').read_text(encoding='utf-8'))
    if 'snapshots' in saved:
        saved['snapshot_hashes']={k:hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest() for k,v in saved.pop('snapshots').items()}
    if 'frame_checks' in saved:
        records=saved.pop('frame_checks')
        saved['frame_summary']={'frames':len(records),'all_finite':all(r['finite'] for r in records),
            'frozen_body_tail_max_delta':max(r['frozen_body_tail_max_delta'] for r in records),
            'eye_cap_max_delta':max(r['eye_cap_max_delta'] for r in records)}
    saved['export_options']['filepath']='assets/grimo/production/pino/candidate-c/face-foundation-v002/pino-face-foundation-v002-diagnostic.glb'
    dump('saved-checks.json',saved)
    arr=np.load(OUT/'_audit.npz');v=arr['vertices'];t=arr['triangles']
    edges=np.sort(np.concatenate([t[:,[0,1]],t[:,[1,2]],t[:,[2,0]]]),axis=1)
    ue,count=np.unique(edges,axis=0,return_counts=True)
    roi=(arr['components']==0)&(abs(v[:,0])<.09)&(v[:,1]<-.33)&(v[:,2]>.50)&(v[:,2]<.64)
    within=roi[ue].all(1)
    dump('mouth-topology.json',{'mouth_roi':{'component':0,'abs_x_lt':.09,'y_lt':-.33,'z':[.50,.64]},
        'original_boundary_edges_wholly_inside_roi':int(np.sum(within&(count==1))),
        'original_overconnected_edges_wholly_inside_roi':int(np.sum(within&(count>2))),
        'candidate_original_mesh_topology_unchanged':saved['lock_checks']['triangles'],
        'self_intersection_and_lip_contact':'UNKNOWN; not established by unchanged topology'})
    for name in ['cute blue creature 3d model.glb']:
        path=ROOT/'assets/grimo/production/pino/candidate-c/source'/name
        b=path.read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n])
        dump('native-glb.json',{'sha256':hashlib.sha256(b).hexdigest(),'images':len(j.get('images',[])),
            'textures':len(j.get('textures',[])),'morph_targets':sum(len(p.get('targets',[])) for m in j['meshes'] for p in m['primitives']),
            'texcoord_attributes':sorted({k for m in j['meshes'] for p in m['primitives'] for k in p['attributes'] if k.startswith('TEXCOORD')})})
    print(json.dumps({'pixels':diff,'saved_summary':saved['frame_summary']},indent=2))

def clean():
    # All targets are direct children of this fixed task evidence directory.
    # No source asset, external directory, or arbitrary user path is accepted.
    for p in OUT.glob('_*'):
        if p.is_file():p.unlink()
    frames=OUT/'_frames'
    if frames.is_dir():
        for p in frames.glob('*.png'):p.unlink()
        frames.rmdir()

def manifest():
    asset=ROOT/'assets/grimo/production/pino/candidate-c/face-foundation-v002'
    paths=[p for folder in [asset,OUT] for p in folder.iterdir() if p.is_file() and not p.name.startswith('_') and p.name!='manifest.json']
    paths += [Path(__file__),ROOT/'scripts/blender/pino-face-foundation-v002.py']
    records={p.relative_to(ROOT).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in paths}
    protected={}
    for rel,expected in [('assets/grimo/production/pino/candidate-c/rig-v001/pino-c-base-rig-v001.blend','b7f36853bdb0a221d62d18c29bb667849fd33d6edba815a4e3bd13599f44f978'),
        ('assets/grimo/production/pino/candidate-c/source/cute blue creature 3d model.glb','ee7339f8e4339037b87880b75d90fd944fe7dda84f696c2be42db7ea0f24da11')]:
        actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest();assert actual==expected
        protected[rel]={'sha256':actual,'unchanged':True}
    dump('manifest.json',{'start_head':'80ed1a9c1335b520e50190059410f23126c61762',
        'branch':'codex/pino-face-foundation-v002-20261015','Human_Face_Gate':'PENDING','Production':'HOLD',
        'geometry_passes':2,'protected_inputs':protected,'files':records})

if __name__=='__main__':
    if '--manifest' in sys.argv:manifest()
    elif '--clean' in sys.argv:clean()
    elif '--finalize' in sys.argv:sections();finalize()
    else:preview();sections()
