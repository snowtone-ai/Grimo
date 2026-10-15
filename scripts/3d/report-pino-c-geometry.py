"""Assemble Pino C measurements/figures without modifying model assets."""
import json,hashlib,sys
from pathlib import Path
from collections import defaultdict,Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/geometry-c-v001';ASSET=ROOT/'assets/grimo/production/pino/candidate-c';RENDERS=OUT/'renders'
D=np.load(OUT/'glb-diagnostic-arrays.npz');V,T,L=[D[k] for k in ['vertices','triangles','components']]
def js(name,d):(OUT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
COLORS={'body':'#8a949d','tail-A':'#007ea8','tail-B':'#e47a14','tail-inner':'#ad388a'}

def tail_shells():
    ids=np.where(L[T[:,0]]==2)[0];fs=T[ids];edges=defaultdict(list)
    for i,t in enumerate(fs):
        for a,b in zip(t,np.roll(t,-1)):edges[tuple(sorted((int(a),int(b))))].append(i)
    parent=list(range(len(fs)))
    def find(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    for adj in edges.values():
        if len(adj)==2:parent[find(adj[0])]=find(adj[1])
    group=defaultdict(list)
    for i in range(len(fs)):group[find(i)].append(i)
    sets=[fs[g] for g in sorted(group.values(),key=lambda g:V[fs[g]].max(axis=(0,1))[0],reverse=True)]
    records=[]
    for k,f in enumerate(sets):
        verts=np.unique(f);p=V[verts];e=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);e.sort(axis=1);_,c=np.unique(e,axis=0,return_counts=True)
        records.append(dict(label=f'tail-{chr(65+k)}',triangles=len(f),vertices=len(verts),boundary_edges=int(sum(c==1)),nonmanifold_edges=int(sum(c!=2)),bounds=[p.min(axis=0).tolist(),p.max(axis=0).tolist()]))
    js('tail-shells.json',dict(shells=records,inner_component=5,inner_triangles=1476,shared_vertex_count_between_A_B=len(set(np.unique(sets[0]))&set(np.unique(sets[1])))))
    return {'body':T[L[T[:,0]]==0],'tail-A':sets[0],'tail-B':sets[1],'tail-inner':T[L[T[:,0]]==5]}

def section(tris,axis,value):
    result=[]
    for t in V[tris]:
        d=t[:,axis]-value
        if min(d)>=0 or max(d)<=0:continue
        pts=[]
        for a,b in [(0,1),(1,2),(2,0)]:
            if d[a]*d[b]<0:pts.append(t[a]+(t[b]-t[a])*(-d[a])/(d[b]-d[a]))
        if len(pts)==2:result.append(np.array(pts)[:,[i for i in range(3) if i!=axis]])
    return result

def figures():
    sets=tail_shells();fig,axs=plt.subplots(2,2,figsize=(12,10),layout='constrained')
    for ax,(axis,val,title) in zip(axs.flat,[(0,0.00001,'Sagittal: x=0 (body and 3 tail shells)'),(1,.015,'Rear root section: y=0.015'),(1,.20,'Mid-tail section: y=0.20'),(1,.395,'Distal section: y=0.395')]):
        for name,f in sets.items():
            segs=section(f,axis,val)
            ax.add_collection(LineCollection(segs,colors=COLORS[name],linewidths=1.3,label=name))
        ax.autoscale();ax.set_aspect('equal');ax.set_title(title);ax.grid(alpha=.2);ax.set_xlabel('Y rear' if axis==0 else 'X left');ax.set_ylabel('Z up')
        if axis==0:ax.set_ylim(0,.62);ax.set_xlim(-.44,.46)
        else:ax.set_ylim(.025,.60);ax.set_xlim(-.24,.24)
    axs[0,0].legend(loc='upper left',fontsize=9);fig.suptitle('Pino C / unchanged source / sections are diagnostics, not cuts to the model')
    fig.savefig(OUT/'tail-sections.png',dpi=150);plt.close(fig)
    # Eye patches and body are measured in the same coordinates.
    eyes=[]
    for comp,side in [(8,'R'),(9,'L')]:
        p=V[L==comp];eyes.append(dict(anatomical_side=side,component=comp,vertices=len(p),bounds=[p.min(axis=0).tolist(),p.max(axis=0).tolist()],width=float(np.ptp(p[:,0])),height=float(np.ptp(p[:,2])),depth=float(np.ptp(p[:,1])),boundary_edges=34,eyelid_gaze_control='UNKNOWN; absent rig/morph'))
    js('eyes.json',dict(eyes=eyes,open_surfaces_both_present=True,complete_closed_eyeball_volumes=False,blink_and_gaze='UNKNOWN'))
    fig,axs=plt.subplots(1,3,figsize=(15,6),layout='constrained')
    for ax,side in zip(axs[:2],[-1,1]):
        for comp,color in [(0,'#a6adb4'),(8,'#007ea8'),(9,'#e47a14')]:
            f=T[L[T[:,0]]==comp];segs=section(f,0,side*.1445);ax.add_collection(LineCollection(segs,colors=color,linewidths=1.1))
        ax.autoscale();ax.set_aspect('equal');ax.set_xlim(-.405,-.26);ax.set_ylim(.56,.75);ax.set_title(f'Eye sagittal x={side*.1445:.4f}');ax.set_xlabel('Y rear');ax.set_ylabel('Z up');ax.grid(alpha=.2)
    for z,col in [(.30,'#007ea8'),(.38,'#e47a14'),(.44,'#ad388a')]:axs[2].add_collection(LineCollection(section(T[L[T[:,0]]==0],2,z),colors=col,linewidths=1,label=f'z={z}'))
    axs[2].autoscale();axs[2].set_aspect('equal');axs[2].set_title('Forepaw / belly horizontal sections');axs[2].set_xlabel('X left');axs[2].set_ylabel('Y rear');axs[2].legend();axs[2].grid(alpha=.2)
    fig.suptitle('No eyeball or eyelid reconstruction performed; arm/belly belong to component 0');fig.savefig(OUT/'eyes-paws-sections.png',dpi=150);plt.close(fig)
    s=read('support.json');fig,ax=plt.subplots(figsize=(8,6),layout='constrained');p=V[(L==0)&(V[:,2]<.045)];ax.scatter(p[:,0],p[:,1],s=3,c=p[:,2],cmap='Blues');h=np.array(s['contact_hull_xy']);h=np.concatenate([h,h[:1]]);ax.plot(h[:,0],h[:,1],color='#e47a14',label='convex hull of 19 vertices at z <= 0.001');ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('X left');ax.set_ylabel('Y rear');ax.legend(fontsize=9);ax.set_title('Footprint only / COM and dynamic stability UNKNOWN\nTail minimum z=0.050293; tail is not a support');fig.savefig(OUT/'support-footprint.png',dpi=150);plt.close(fig)

FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
def tile(path,size=(340,340)):
    im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,'#eef0f3');bg.alpha_composite(im);return bg.convert('RGB').resize(size)
def board(items,name,columns=3):
    w,h=360,385;out=Image.new('RGB',(w*columns,h*((len(items)+columns-1)//columns)),'white');draw=ImageDraw.Draw(out)
    for i,(p,label) in enumerate(items):
        x=(i%columns)*w;y=(i//columns)*h;out.paste(tile(p),(x+10,y+30));draw.text((x+10,y+5),label,font=FONT,fill='#151e28')
    out.save(OUT/name)

def compare():
    views=['front','front-left','front-right','left','right','back','rear-left','top','underside'];results={}
    for kind in ['retained','trial']:
        rows=[]
        for v in views:
            a=np.asarray(Image.open(RENDERS/f'source-{v}.png').convert('RGBA')).astype(int);b=np.asarray(Image.open(RENDERS/f'{kind}-{v}.png').convert('RGBA')).astype(int);d=np.abs(a-b);mask=np.any(d>0,axis=-1)
            rows.append(dict(view=v,changed_pixels=int(mask.sum()),max_channel_delta=int(d.max()),mean_abs_delta=float(d.mean()),alpha_changed_pixels=int(np.any(d[:,:,3:]!=0,axis=-1).sum())))
            # Diagnostic difference image amplifies RGB difference eightfold; alpha is fixed opaque.
            Image.fromarray(np.clip(d[:,:,:3]*8,0,255).astype('uint8')).save(RENDERS/f'diff-{kind}-{v}.png')
        results[kind]=dict(all_views_pixel_exact=all(r['changed_pixels']==0 for r in rows),views=rows)
    js('pixel-comparison.json',results)
    board([(RENDERS/f'source-{v}.png',v) for v in views],'00-source-nine-views.png')
    for n,group in enumerate([views[:3],views[3:6],views[6:]],1):
        board([(RENDERS/f'{tag}-{v}.png',f'{v} / {tag}') for v in group for tag in ['source','retained','diff-retained']],f'comparison-{n:02d}-source-retained.png')
    board([(RENDERS/f'{tag}-{v}.png',f'{v} / {tag}') for v in ['back','left','rear-left'] for tag in ['source','trial','diff-trial']],'trial-comparison.png')
    board([(RENDERS/f'probe-{k}-{end}-{view}.png',f'{k} / {view}') for k,end in [('tail','end'),('tail','opposite'),('paw-L','end'),('paw-R','end'),('paws-both','end'),('low-rest','end')] for view in ['front','side']],'deformation-probes.png',4)
    trial=read('trial.json');trial.update(pixel_exact=results['trial']['all_views_pixel_exact'],adoption='REJECTED / NOT IN DELIVERY' if not results['trial']['all_views_pixel_exact'] else 'NOT ADOPTED: bounded pixel checks do not resolve triple shell/root and global defects');js('trial.json',trial)

def manifest():
    refs=[ROOT/'assets/grimo/source/pino/pino-Identity-canonical.png',*sorted((ROOT/'assets/grimo/source/pino/tripo-generation-pose').glob('*.png')),*sorted((ROOT/'assets/grimo/production/pino/references').glob('*.png'))]
    files=[*sorted(ASSET.rglob('*')),*sorted(OUT.rglob('*')),*sorted((ROOT/'scripts/blender').glob('*pino-c-*.py')),*sorted((ROOT/'scripts/3d').glob('*pino-c-*.py'))]
    def rec(p):
        raw=p.read_bytes();text=p.suffix in ['.py','.json','.md']
        return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw.replace(b'\r\n',b'\n') if text else raw).hexdigest(),hash_policy='UTF-8 file bytes with LF newlines' if text else 'raw binary file bytes')
    js('manifest.json',dict(initial_base_main_sha='940fc5ee3d9c2d155031a0c3030034d4999dea16',integrated_main_sha='8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b',appearance_lock_commit='2abea76fad578281f74b9fa628987a80b56ad6dc',appearance_lock_blob='7d9fd5fd071aceaa71716e4fa5b817661fb7bb12',branch='codex/pino-c-geometry-gate-20261015',sources_fixed=True,geometry_master='FBX / Human selected',appearance_reference='original GLB / Human specified',delivery='FBX-derived Neutral candidate with preserved original GLB appearance; geometry readiness HOLD',human_geometry_gate='PENDING',tripo_operations=False,adopted_repairs=False,files=[rec(p) for p in files if p.is_file() and p.name!='manifest.json' and not p.name.endswith('.log') and p.name!='four-tests-progress.json'],authority_images=[rec(p) for p in refs]))

def originals():
    views=['front','front-left','left','back','right','front-right','rear-left','top','underside'];rows=[]
    for v in views:
        a=np.asarray(Image.open(RENDERS/f'original-fbx-{v}.png').convert('RGBA')).astype(int)
        b=np.asarray(Image.open(RENDERS/f'original-glb-{v}.png').convert('RGBA')).astype(int)
        d=np.abs(a-b)
        rows.append(dict(view=v,changed_pixels=int(np.any(d>0,axis=-1).sum()),max_channel_delta=int(d.max()),mean_abs_delta=float(d.mean()),alpha_changed_pixels=int((d[:,:,3]>0).sum())))
        Image.fromarray(np.clip(d[:,:,:3]*8,0,255).astype('uint8')).save(RENDERS/f'original-diff-{v}.png')
    js('originals-pixel-comparison.json',dict(exact=False,method='Identical Cycles camera/light/material import settings; RGB absolute difference x8; includes importer material and triangulation differences',views=rows))
    for n,group in enumerate([views[:3],views[3:6],views[6:]],1):
        board([(RENDERS/f'original-{tag}-{v}.png',f'{v} / {tag}') for v in group for tag in ['fbx','glb','diff']],f'originals-comparison-{n:02d}.png')

def exported():
    views=['front','front-left','left','back','right','front-right','rear-left','top','underside'];rows=[]
    for v in views:
        a=np.asarray(Image.open(RENDERS/f'original-glb-{v}.png').convert('RGBA')).astype(int);b=np.asarray(Image.open(RENDERS/f'master-derived-{v}.png').convert('RGBA')).astype(int);d=np.abs(a-b)
        rows.append(dict(view=v,changed_pixels=int(np.any(d>0,axis=-1).sum()),max_channel_delta=int(d.max()),mean_abs_delta=float(d.mean())))
        Image.fromarray(np.clip(d[:,:,:3]*8,0,255).astype('uint8')).save(RENDERS/f'export-diff-{v}.png')
    js('export-pixel-comparison.json',dict(all_nine_views_pixel_exact=all(r['changed_pixels']==0 for r in rows),views=rows,limit='Deterministic sampled views supplement exact active binary payload, material JSON and reimported surface/normal equality; no Motion or Tripo PASS implied.'))
    for n,group in enumerate([views[:3],views[3:6],views[6:]],1):
        board([(RENDERS/(f'original-glb-{v}.png' if tag=='reference' else f'master-derived-{v}.png' if tag=='derived' else f'export-diff-{v}.png'),f'{v} / {tag}') for v in group for tag in ['reference','derived','diff']],f'export-comparison-{n:02d}.png')
    if (OUT/'saved-file-verification.json').exists():
        restored=[]
        for v in ['front','front-left','left']:
            a=np.asarray(Image.open(RENDERS/f'original-fbx-{v}.png'));b=np.asarray(Image.open(RENDERS/f'replay-neutral-{v}.png'));restored.append(dict(view=v,pixel_exact=bool(np.array_equal(a,b)),changed_pixels=int(np.any(a!=b,axis=-1).sum())))
        js('saved-neutral-pixel-comparison.json',dict(reference='original FBX import (diagnostic Master); final GLB appearance checked separately',views=restored,all_views_pixel_exact=all(r['pixel_exact'] for r in restored)))

if __name__=='__main__':
    figures()
    if (OUT/'run.json').exists():compare();manifest()
    if (OUT/'originals-comparison.json').exists():originals()
    if (OUT/'export-reimport.json').exists():exported()
    manifest()
