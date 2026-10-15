"""Unpainted rendered boards, exact image repack and protected input evidence."""
import sys,json,hashlib,subprocess,importlib.util,struct
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004'
STATES=['neutral','weight-transfer','legs-forward','rump-descending','rump-contact','seat','seat-rest','recover-load','recover-feet','standing-return']
COMPOSE=['seat-half','seat-closed','seat-joy','seat-lowhead','seat-shift-L','seat-shift-R','seat-offer-L','seat-hold-R','seat-both-hold']
VIEWS=['front','3q-L','3q-R','left','right','back','rear-L','rear-R']
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def board(name,cells,cols=4,width=512):
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19);tiles=[]
    for label,path in cells:
        im=Image.open(path).convert('RGB');im.thumbnail((width,width));tile=Image.new('RGB',(width,width+30),(243,241,239));tile.paste(im,((width-im.width)//2,0));ImageDraw.Draw(tile).text((8,width+5),label,fill=(25,25,25),font=font);tiles.append(tile)
    result=Image.new('RGB',(width*cols,(width+30)*((len(tiles)+cols-1)//cols)),(243,241,239))
    for i,t in enumerate(tiles):result.paste(t,(i%cols*width,i//cols*(width+30)))
    result.save(OUT/name)
def boards():
    for state in STATES+COMPOSE:
        paths=[(state+' / '+view,OUT/'renders/candidate'/f'{state}-{view}.png') for view in VIEWS]
        if all(p.exists() for _,p in paths):board('view-'+state+'.png',paths)
    for state in ['neutral','legs-forward','seat','seat-rest','standing-return']:
        paths=[(state+' / '+view,OUT/'renders/reimport'/f'{state}-{view}.png') for view in VIEWS]
        if all(p.exists() for _,p in paths):board('saved-view-'+state+'.png',paths)
    for view in VIEWS:
        paths=[(state,OUT/'renders/candidate'/f'{state}-{view}.png') for state in STATES]
        if all(p.exists() for _,p in paths):board('transition-'+view+'.png',paths,5,400)
    for view in ['front','left','3q-L','3q-R']:
        cells=[(tag+' / '+state,OUT/'renders'/tag/f'{state}-{view}.png') for state in ['neutral','legs-forward','seat'] for tag in ['before','candidate']]
        if all(p.exists() for _,p in cells):board('comparison-'+view+'.png',cells,2)
    for state in ['seat','seat-half','seat-closed','seat-joy','seat-lowhead','seat-shift-L','seat-shift-R','seat-offer-L','seat-hold-R','seat-both-hold']:
        cells=[(state+' / '+view,OUT/'detail/candidate'/f'{state}-{view}.png') for view in ['front','3q-L','3q-R','left','right']]
        if all(p.exists() for _,p in cells):board('face-'+state+'.png',cells,5)
    paths=sorted((OUT/'sequence').glob('*.png'))
    if paths:
        board('sequence-contact-sheet.png',[(f'frame {p.stem}',p) for p in paths],6,320)
        for k in range(0,len(paths),6):board(f'sequence-{k//6:02}.png',[(f'frame {p.stem}',p) for p in paths[k:k+6]],3,448)
    paths=sorted((OUT/'composition-sequence').glob('*.png'))
    for k in range(0,len(paths),6):board(f'composition-sequence-{k//6:02}.png',[(f'frame {p.stem}',p) for p in paths[k:k+6]],3,448)
    cells=[(tag+' / '+state,OUT/'renders'/tag/f'{state}-3q-L.png') for state in ['neutral','legs-forward','seat','seat-rest','standing-return'] for tag in ['candidate','reimport']]
    if all(p.exists() for _,p in cells):board('saved-glb-comparison.png',cells,2)
    cells=[('pose reference 23',OUT/'references/23-seated-left-profile.png'),('v003 crouch / left',OUT/'renders/before/seat-left.png'),('v004 seat / left',OUT/'renders/candidate/seat-left.png'),('pose reference 24',OUT/'references/24-seated-front-three-quarter.png'),('v003 crouch / 3q',OUT/'renders/before/seat-3q-L.png'),('v004 seat / 3q',OUT/'renders/candidate/seat-3q-L.png')]
    if all(p.exists() for _,p in cells):board('references-before-after.png',cells,3)
def references():
    import shutil
    names=['23-seated-left-profile.png','24-seated-front-three-quarter.png','25-seated-rear-three-quarter.png','26-standing-to-seated-transition-left-profile.png']
    folder=OUT/'references';folder.mkdir(exist_ok=True);rows=[]
    source=json.loads((ROOT/'manifest_18-27_revised_v003.json').read_text(encoding='utf-8'))
    for name in names:
        shutil.copyfile(ROOT/name,folder/name);rows.append({'source_path':name,'evidence_copy':'references/'+name,'sha256':sha(ROOT/name),'exact_copy':sha(ROOT/name)==sha(folder/name)})
    write('reference-provenance.json',{'actual_location':'Root-level supplied pack; no shushu_seated_refs directory was present','source_manifest':source,'images':rows,'scope':'Pose explanations only. Latest v003 manifest says #25 accepted by user, superseding older v002 README HOLD. No 3D geometry approval or unseen rear structure inferred.'})
def textures():
    sp=importlib.util.spec_from_file_location('report001',ROOT/'scripts/3d/report-shushu-production-rig-v001.py');r=importlib.util.module_from_spec(sp);sp.loader.exec_module(r)
    r.OUT=OUT;r.RIG=r.RIG.with_name('shushu-v006-production-rig-v004.glb')
    paths=[r.RIG,r.RIG.with_name(r.RIG.stem+'-proof.glb')]
    def numeric(p):
        j,raw=r.read(p);return hashlib.sha256(b''.join(r.accessor(j,raw,i).tobytes() for i in range(len(j['accessors'])))).hexdigest()
    before={p.name:numeric(p) for p in paths};r.restore_textures();after={p.name:numeric(p) for p in paths}
    for p in paths:
        j,raw=r.read(p)
        if j.get('extensionsUsed')==[]:
            del j['extensionsUsed'];meta=json.dumps(j,ensure_ascii=False,separators=(',',':')).encode();meta+=b' '*((-len(meta))%4)
            p.write_bytes(struct.pack('<III',0x46546c67,2,28+len(meta)+len(raw))+struct.pack('<II',len(meta),0x4e4f534a)+meta+struct.pack('<II',len(raw),0x004e4942)+raw)
    write('numeric-repack-invariance.json',{'before':before,'after':after});assert before==after;r.glb_audit()
def preserve():
    src=json.loads((OUT/'protected-inputs.json').read_text(encoding='utf-8'));changed=[];missing=[]
    for n,h in src.items():
        if not (ROOT/n).exists():missing.append(n)
        elif sha(ROOT/n)!=h:changed.append(n)
    allowed=['AGENTS.md','docs/production/Handoff.md']
    write('protected-input-verification.json',{'inputs':len(src),'changed':changed,'missing':missing,'allowed':allowed,'remote_agents_commit':'2abea76fad578281f74b9fa628987a80b56ad6dc'})
    assert not missing and set(changed)<=set(allowed)
def manifest():
    rig=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
    write('delivery-manifest.json',{'date':'2026-10-15','assets':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(rig.glob('*production-rig-v004*'))],'appearance':'HOLD / Human PENDING','start_head':json.loads((OUT/'start-state.json').read_text())['head'],'remote_authority_commit':'2abea76fad578281f74b9fa628987a80b56ad6dc'})
def videos():
    import subprocess
    for folder,step,name in [('sequence',6,'seat-return'),('composition-sequence',4,'seated-compositions')]:
        paths=sorted((OUT/folder).glob('*.png'));assert paths
        lines=[]
        for p in paths:lines += ["file '"+p.relative_to(OUT).as_posix()+"'",f'duration {step/24:.9f}']
        lines += ["file '"+paths[-1].relative_to(OUT).as_posix()+"'"]
        listing=OUT/(name+'-frames.txt');listing.write_text('\n'.join(lines)+'\n',encoding='utf-8')
        subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(listing),'-vf','fps=24','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(OUT/(name+'.mp4'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    write('video-provenance.json',{'source':'Actual saved proof renders; no interpolation or image repair. Repeated sampled frames at their 24fps source time spacing. Inspect the linked full-resolution frame boards.','clips':[{'name':n+'.mp4','sha256':sha(OUT/(n+'.mp4'))} for n in ['seat-return','seated-compositions']]})
if __name__=='__main__':
    for arg,fn in [('references',references),('boards',boards),('textures',textures),('videos',videos),('preserve',preserve),('manifest',manifest)]:
        if arg in sys.argv:fn()
