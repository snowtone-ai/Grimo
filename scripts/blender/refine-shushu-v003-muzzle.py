"""Localized nose/subnasal continuation of the saved v003 appeal revision."""
import sys
sys.dont_write_bytecode = True
import bpy, json, hashlib, shutil, importlib.util, math, subprocess
from pathlib import Path
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('appeal', Path(__file__).with_name('refine-shushu-v003-appeal.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
v, r = a.v, a.r
OUT = v.OUT/'muzzle-revision'
BACK = ROOT/'.git/shushu-v003-muzzle-6f48223'
BASE = '6f4822362aaec9e795023f08349d4bb14c5188e0'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name, obj): (OUT/name).write_text(json.dumps(obj, indent=2)+'\n', encoding='utf-8')
def snapshot():
    OUT.mkdir(exist_ok=True); (OUT/'renders').mkdir(exist_ok=True); BACK.mkdir(exist_ok=True)
    manifest = BACK/'inputs.json'
    if manifest.exists(): return json.loads(manifest.read_text())
    inputs = {}
    for p in [v.ASSET, v.PROOF, v.STATIC.with_suffix('.fbx'), v.STATIC.with_suffix('.glb')]:
        rel=p.relative_to(ROOT).as_posix()
        data=subprocess.run(['git','show',f'{BASE}:{rel}'],cwd=ROOT,capture_output=True,check=True).stdout
        if data.startswith(b'version https://git-lfs'):
            data=subprocess.run(['git','lfs','smudge'],input=data,cwd=ROOT,capture_output=True,check=True).stdout
        (BACK/p.name).write_bytes(data);inputs[rel]=sha(BACK/p.name)
    for p in list(ROOT.glob('*.png'))+list(ROOT.glob('*18-27*'))+list((v.OUT.parent/'geometry-v002').glob('review-*.png'))+list((ROOT/'assets/grimo/source/shushu').rglob('*'))+list((ROOT/'assets/grimo/production/shushu/image-reference').rglob('*')):
        if p.is_file(): inputs[p.relative_to(ROOT).as_posix()] = sha(p)
    manifest.write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
    return inputs
def profile():
    tr = v.tree(v.parts['Head']); rows = []
    for z in np.arange(.590,.676,.002):
        row = {'z':float(z),'y':{}}
        for x in [0,.005,.010,.015,.020,.030,.040,.055,.070]:
            hit = tr.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))[0]
            row['y'][str(x)] = float(hit.y) if hit is not None else None
        rows.append(row)
    return rows
def inspect():
    a.load(BACK/v.ASSET.name)
    h = v.parts['Head']; b = h.data.shape_keys.key_blocks['Basis']
    pts = [(i,list(p.co)) for i,p in enumerate(b.data) if abs(p.co.x)<.022 and .612<p.co.z<.648 and p.co.y<-.255]
    pigment=[i for i,p in pts if abs(p[0])<.017 and .623<p[2]<.641 and p[1]<-.279]
    write('diagnosis.json',{'base':BASE,'profile':profile(),'nose_control_vertex_count':len(pts),'most_forward_control_examples':sorted(pts,key=lambda item:item[1][1])[:8],'diagnostic_nose_ids':pigment,'modifiers':[(m.name,m.type) for m in h.modifiers], 'shape_control_count':len(h.data.shape_keys.key_blocks)})
    print(json.dumps({'profile':profile()[12:29],'nose_vertices':pts[:40]},indent=2),flush=True)

def displacement(p):
    x,y,z = p
    # A compact C1 field replaces the inherited long tip and subnasal ridge.
    # X/Z and the mouth aperture stay fixed; only the local depth is edited.
    w = (1-v.smooth(.026,.046,abs(x)))*v.smooth(.602,.613,z)*(1-v.smooth(.650,.667,z))*v.smooth(-.235,-.258,y)
    if not w: return Vector((0,0,0))
    bed = -.268 + .20*(z-.625) + 7*x*x
    cap = .0135*math.exp(-((x/.015)**2+((z-.636)/.010)**2))
    return Vector((0,(bed-cap-y)*w,0))

def refine():
    h = v.parts['Head']; keys=h.data.shape_keys.key_blocks
    changes = {i:displacement(p.co) for i,p in enumerate(keys['Basis'].data)}
    changes = {i:d for i,d in changes.items() if d.length>1e-9}
    # Each expression, seat and corrective gets the identical Basis delta, so
    # their original relative deformations survive. Head compositions rotate it.
    for k in keys:
        if k.name.startswith(('Head','Corrective.Compose.')): continue
        for i,d in changes.items(): k.data[i].co += d
    r.compose(h); h.data.update(); h.update_tag(); v.reset()
    return {'vertices':len(changes),'max_delta':max(d.length for d in changes.values()),
            'basis_bounds': [np.array([keys['Basis'].data[i].co for i in changes]).min(0).tolist(), np.array([keys['Basis'].data[i].co for i in changes]).max(0).tolist()],
            'scope':'Head local Y only; expression/seat relative deltas retained; head rotations recomposed'}

def diagnostic_colour():
    # The diagnostic pigment belongs to the unchanged nose footprint, not to a
    # Y threshold that would remove pigment merely because the tip recedes.
    a.colour()
    h=v.parts['Head']; b=h.data.shape_keys.key_blocks['Basis']; attr=h.data.color_attributes['DiagnosticIdentity']
    ids=set(json.loads((OUT/'diagnosis.json').read_text())['diagnostic_nose_ids'])
    for loop in h.data.loops:
        p=b.data[loop.vertex_index].co
        if abs(p.x)<.017 and .623<p.z<.641:
            attr.data[loop.index].color=(.90,.86,.81,1)
        if loop.vertex_index in ids: attr.data[loop.index].color=(.055,.023,.043,1)

def preview():
    a.load(BACK/v.ASSET.name); report=refine(); write('candidate-local-edit.json',report)
    old=r.OUT; r.OUT=BACK; (BACK/'renders').mkdir(exist_ok=True)
    for view in ['side','3q']: r.render('candidate-neutral-clay',view)
    a.pose('smile'); r.render('candidate-smile-clay','3q')
    a.pose('neutral'); diagnostic_colour(); r.render('candidate-neutral-colour','3q',colour=True)
    r.OUT=old; write('candidate-profile.json',profile())
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(BACK/'candidate.blend'))
    print('MUZZLE_PREVIEW_COMPLETE',flush=True)

def apply():
    inputs=snapshot(); former=json.loads((OUT/'continuity.json').read_text()) if (OUT/'continuity.json').exists() else {}
    for p in [v.ASSET,v.PROOF]:
        allowed={inputs[p.relative_to(ROOT).as_posix()]}
        if p.name in former: allowed.add(former[p.name]['after_sha256'])
        assert sha(p) in allowed,('Concurrent asset edit',str(p))
    report={}; bpy.context.preferences.filepaths.save_version=0
    for p in [v.ASSET,v.PROOF]:
        a.load(BACK/p.name); edit=refine()
        bpy.context.scene['Human Geometry Gate']='PENDING'
        bpy.context.scene['v003_muzzle_revision']='6f48223 continuation: compact rounded nose and relaxed subnasal depth'
        bpy.data.texts['READ_ME_v003'].write('\nMuzzle continuation from 6f48223: local Head depth only; original expression deltas, mouth rim, lid walls, seated skin and proof retained. Human PENDING / Tripo HOLD. Evidence: docs/production/shushu/evidence/geometry-v003/muzzle-revision/REVIEW.md\n')
        bpy.ops.wm.save_as_mainfile(filepath=str(p))
        report[p.name]={'baseline_sha256':sha(BACK/p.name),'after_sha256':sha(p),'local_edit':edit}
    write('continuity.json',report)
    a.load(v.ASSET); original=v.character; v.character=[o for o in original if not o.hide_render]
    v.export_static(); v.character=original
    shutil.copy2(v.OUT/'static-roundtrip.json',OUT/'static-roundtrip.json')
    print('MUZZLE_APPLY_COMPLETE',flush=True)

def final_renders():
    # Fourteen new views, matched against already saved appeal renders.
    chosen=[('neutral','clay',list(r.VIEWS),True),('neutral','colour',list(r.VIEWS),True),
        ('smile','clay',list(r.VIEWS),True),('companion','colour',list(r.VIEWS),False),
        ('small','colour',['3q'],True),('full','colour',['3q'],True)]
    previous_cameras=json.loads((a.OUT/'cameras.json').read_text()); old=r.OUT; r.OUT=OUT
    for state,kind,views,face in chosen:
        a.load(v.ASSET)
        if kind=='colour':diagnostic_colour()
        a.pose(state); body=a.coloured_body() if state=='companion' and kind=='colour' else None
        for view in views:
            stem=state+'-'+kind; r.render('after-'+stem,view,face,kind=='colour')
            prior=('companion' if state=='companion' else 'mouth-'+state)+'-'+kind+'-'+view
            shutil.copy2(a.OUT/'renders'/(prior+'.png'),OUT/'renders'/('before-'+stem+'-'+view+'.png'))
            cameras=json.loads((OUT/'cameras.json').read_text()); cameras['before-'+stem+'-'+view]=previous_cameras[prior]
            assert cameras['after-'+stem+'-'+view]==cameras['before-'+stem+'-'+view]
            write('cameras.json',cameras)
        if body:bpy.data.objects.remove(body,do_unlink=True)
    r.OUT=old; print('MUZZLE_RENDERS_COMPLETE',flush=True)

def side_margin():
    # The previous close-up clipped the former tip at its left edge. Re-capture
    # both versions with an identical small camera translation, preserving scale.
    for state,kind in [('neutral','clay'),('neutral','colour'),('smile','clay')]:
        for version in ['before','after']:
            a.load(BACK/v.ASSET.name if version=='before' else v.ASSET)
            if kind=='colour':diagnostic_colour()
            a.pose(state);sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=12;sc.cycles.use_denoising=True
            sc.render.resolution_x=480;sc.render.resolution_y=540;sc.render.resolution_percentage=100
            direction=Vector((1,0,0));target=Vector((0,-.058,.65));cam=v.cam
            cam.location=target+3*direction;cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.54
            name=f'{version}-{state}-{kind}-side';sc.render.filepath=str(OUT/'renders'/(name+'.png'));bpy.ops.render.render(write_still=True)
            cameras=json.loads((OUT/'cameras.json').read_text());cameras[name]={'direction':[1,0,0],'target':list(target),'ortho_scale':.54,'resolution':[480,540],'engine':'CYCLES','samples':12,'colour':'diagnostic' if kind=='colour' else 'clay'};write('cameras.json',cameras)
    print('MUZZLE_SIDE_MARGIN_COMPLETE',flush=True)

if __name__ == '__main__':
    snapshot()
    if '--inspect' in sys.argv: inspect()
    if '--preview' in sys.argv: preview()
    if '--apply' in sys.argv: apply()
    if '--render' in sys.argv: final_renders()
    if '--side-margin' in sys.argv: side_margin()
