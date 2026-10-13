"""Local continuation of the SAVED v003; never reconstructs/imports a replacement.

Run --measure, --trials, --apply, or --render. Baseline files are resolved once to
.git/shushu-v003-pre-gate; production keys, drivers, topology and timeline survive.
Diagnostic colours are temporary, approximate identity cues, not approved texture.
"""
import bpy,math,json,sys,hashlib,importlib.util,subprocess
from pathlib import Path
import numpy as np
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('v3',Path(__file__).with_name('build-shushu-geometry-v003.py'))
v3=importlib.util.module_from_spec(spec);spec.loader.exec_module(v3)
OUT=v3.OUT/'human-gate-revision';OUT.mkdir(exist_ok=True);(OUT/'renders').mkdir(exist_ok=True)
BACK=ROOT/'.git/shushu-v003-pre-gate';BACK.mkdir(exist_ok=True)
BASE='93869a8771045d7ed79ab036bd61d66ed97bd437'
VIEWS={'front':(0,-1,0),'side':(1,0,0),'3q':(1,-1,0)}
HEAD_POSES={'HeadTurn.L':((0,0,1),22),'HeadTurn.R':((0,0,1),-22),'HeadTilt.L':((0,1,0),12),'HeadTilt.R':((0,1,0),-12),'HeadRest':((1,0,0),10)}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def snapshot():
    for p in [v3.ASSET,v3.PROOF]:
        dest=BACK/p.name
        if not dest.exists():
            data=subprocess.run(['git','show',BASE+':'+p.relative_to(ROOT).as_posix()],cwd=ROOT,check=True,capture_output=True).stdout
            if data.startswith(b'version https://git-lfs.github.com/spec/v1'):
                data=subprocess.run(['git','lfs','smudge'],input=data,cwd=ROOT,check=True,capture_output=True).stdout
            assert data.startswith(b'BLENDER') or data[:4]==bytes([0x28,0xb5,0x2f,0xfd]),'Baseline must resolve to real Blender file, not LFS pointer'
            dest.write_bytes(data)
    if not (BACK/'preserved.json').exists():
        paths=list(ROOT.glob('*.png'))+list(ROOT.glob('*18-27*'))+list((v3.OUT.parent/'geometry-v002').glob('review-*.png'))
        paths+=list((ROOT/'assets/grimo/production/shushu/image-reference').rglob('*.png'))
        (BACK/'preserved.json').write_text(json.dumps({p.relative_to(ROOT).as_posix():sha(p) for p in paths if p.is_file()},indent=2),encoding='utf-8')
def load(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    v3.character=[o for o in bpy.data.objects if o.name.startswith('Shushu_')]
    v3.parts={n:bpy.data.objects['Shushu_'+n] for n in v3.NAMES}
    v3.raw=bpy.data.objects['Original_CandidateB_REFERENCE_ONLY'];v3.cam=bpy.data.objects['ReviewCamera']
    v3.clay=bpy.data.materials['Inspection clay - no texture']
    if path.name.endswith('proof.blend'):bpy.context.scene.frame_set(1)
    v3.reset()
def source_ids():
    groups=v3.components(v3.raw.data);polys=[list(p.vertices) for p in v3.raw.data.polygons]
    return groups,polys
def visible_eye(side,donor=False):
    """Front orthographic world-space pixel grid; nearest surface identifies eyes.
    Pink patterns and underlying rear eye volume are explicitly excluded.
    """
    if donor:
        groups,_=source_ids();polygons=set(groups[15 if side=='L' else 14]);v3.raw.data.calc_loop_triangles()
        faces={i for i,t in enumerate(v3.raw.data.loop_triangles) if t.polygon_index in polygons};trees=[(v3.tree(v3.raw),True)]
    else:trees=[(v3.tree(v3.parts['Head']),False),(v3.tree(bpy.data.objects['Shushu_Eye.'+side]),True)]
    sign=1 if side=='L' else -1;xs=np.linspace(.035,.225,301)*sign;zs=np.linspace(.55,.77,341);hits=[]
    for z in zs:
        for x in xs:
            rows=[]
            for tr,eye in trees:
                hit,n,idx,dist=tr.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))
                if hit is not None:rows.append((dist,idx,eye))
            if rows:
                dist,idx,eye=min(rows)
                if (idx in faces) if donor else eye:hits.append((float(x),float(z)))
    a=np.array(hits);return {'width':float(np.ptp(a[:,0])),'height':float(np.ptp(a[:,1])),'center':((a.min(0)+a.max(0))/2).tolist(),'projected_area':len(a)*(xs[1]-xs[0])*(zs[1]-zs[0])*sign,'grid_step':[abs(float(xs[1]-xs[0])),float(zs[1]-zs[0])],'bounds':[a.min(0).tolist(),a.max(0).tolist()]}
def measure():
    snapshot();load(BACK/v3.ASSET.name);groups,polys=source_ids();report={'baseline_commit':'93869a8771045d7ed79ab036bd61d66ed97bd437','baseline_blend_sha256':sha(BACK/v3.ASSET.name),'method':'Identical front orthographic rays; 0.000633 x 0.000647 world-unit grid. Visible nearest-hit eye surface, not pink pattern or hidden volume.','eyes':{}}
    for side in ['L','R']:
        ids=sorted({v for f in groups[15 if side=='L' else 14] for v in polys[f]});a=np.array([v3.raw.data.vertices[i].co for i in ids]);cap=np.array([v.co for v in bpy.data.objects['Shushu_Eye.'+side].data.vertices][:513])
        old=visible_eye(side);donor=visible_eye(side,True)
        report['eyes'][side]={'donor_component_bounds':[a.min(0).tolist(),a.max(0).tolist()],'donor_component_width_height':[float(np.ptp(a[:,0])),float(np.ptp(a[:,2]))],'v003_front_cap_width_height':[float(np.ptp(cap[:,0])),float(np.ptp(cap[:,2]))],'donor_visible':donor,'v003_visible':old,'visible_ratio_width_height':[old['width']/donor['width'],old['height']/donor['height']]}
    # The donor is untextured: pink extent is not an eye component measurement.
    report['pink_pattern']={'donor':'UNENCODED in original FBX/GLB; cannot measure as eyeball','diagnostic':'Temporary head vertex colour mask, separately labelled; no new visual authority'}
    bm=__import__('bmesh').new();bm.from_mesh(v3.raw.data)
    edges=[e for e in bm.edges if e.is_boundary and all(abs(v.co.x)<.08 and -.32<v.co.y<-.2 and .52<v.co.z<.64 for v in e.verts)]
    a=np.array([v.co for e in edges for v in e.verts]);report['donor_mouth_boundary']={'edges':len(edges),'bounds':[a.min(0).tolist(),a.max(0).tolist()],'width_height':[float(np.ptp(a[:,0])),float(np.ptp(a[:,2]))]} if len(a) else {'edges':0}
    bm.free()
    tr=v3.tree(v3.raw);cavity=[]
    for z in np.linspace(.557,.612,111):
        outside=[tr.ray_cast(Vector((x,-1,float(z))),Vector((0,1,0)))[0].y for x in [-.052,.052]]
        for x in np.linspace(-.046,.046,185):
            hit=tr.ray_cast(Vector((float(x),-1,float(z))),Vector((0,1,0)))[0]
            expected=sum(outside)/2-.012*(1-(x/.052)**2)
            if hit is not None and hit.y-expected>.010:cavity.append((float(x),float(z)))
    a=np.array(cavity);report['donor_mouth_deep_cavity_proxy']={'bounds':[a.min(0).tolist(),a.max(0).tolist()],'width_height':np.ptp(a,axis=0).tolist(),'definition':'Depth residual >0.010 from quadratic continuation of same-z muzzle samples x +/-0.052; search x +/-0.046, z 0.557..0.612. Approximate recessed cavity, not exact lip segmentation; includes upper central cleft.'}
    write('eye-measurements-before.json',report);print(json.dumps(report,indent=2),flush=True)
def compose(o):
    """Refresh only existing head rotations / composition keys after local edits."""
    keys=o.data.shape_keys.key_blocks;basis=keys['Basis'];pivot=Vector((0,.02,.52))
    for label,(axis,angle) in HEAD_POSES.items():
        if label not in keys:continue
        q=Quaternion(axis,math.radians(angle))
        for dst,b in zip(keys[label].data,basis.data):dst.co=pivot+q@(b.co-pivot)
        prefix='Corrective.Compose.'+label+'.'
        for k in keys:
            if k.name.startswith(prefix):
                face=keys[k.name[len(prefix):]]
                for dst,f,b in zip(k.data,face.data,basis.data):delta=f.co-b.co;dst.co=b.co+q@delta-delta
def revise_eyes(variant):
    report=json.loads((OUT/'eye-measurements-before.json').read_text());head=v3.parts['Head'];keys=head.data.shape_keys.key_blocks
    baseline={k.name:np.array([v.co for v in k.data]) for k in keys}
    for side,sign in [('L',1),('R',-1)]:
        # Independent x/z dimensions restore the measured visible donor envelope;
        # topology, wall, closed-eye volume and all blink/gaze logic remain.
        row=report['eyes'][side]
        sx=row['donor_visible']['width']/row['v003_visible']['width'] if variant in ['size-only','combined'] else 1.
        sz=row['donor_visible']['height']/row['v003_visible']['height'] if variant in ['size-only','combined'] else 1.
        g=head.vertex_groups['Local eyelid thickness.'+side]
        ws={v.index:math.sqrt(next((a.weight for a in v.groups if a.group==g.index),0)) for v in head.data.vertices}
        center=Vector((sign*.129,0,.660));eye=bpy.data.objects['Shushu_Eye.'+side]
        if sx!=1 or sz!=1:
            for k in eye.data.shape_keys.key_blocks:
                if k.name.startswith(('Seat','Head','Corrective.Compose.')):continue
                for v in k.data:v.co.x=center.x+(v.co.x-center.x)*sx;v.co.z=center.z+(v.co.z-center.z)*sz
            for k in keys:
                if k.name.startswith(('Seat','Head','Corrective.Compose.')):continue
                for i,t in ws.items():
                    if not t:continue
                    v=k.data[i];v.co.x+=t*(sx-1)*(v.co.x-center.x);v.co.z+=t*(sz-1)*(v.co.z-center.z)
        if variant in ['surround-only','combined']:
            # Recede the intermediate annulus smoothly, keeping the aperture,
            # outer boundary, lid wall, eye cap and closure seam exactly intact.
            # Use a smooth ring field. Per-vertex nearest angular neighbours can
            # introduce small ridges on the irregular saved donor boundary.
            for i,t in ws.items():
                if not (0<t<1):continue
                delta=.0025*math.sin(math.pi*t)**2
                for k in keys:
                    if k.name.startswith(('Seat','Head','Corrective.Compose.')):continue
                    k.data[i].co.y+=delta
        # Seating is a shared translation; preserve it relative to edited Basis.
        for o,old in [(head,baseline),(eye,None)]:
            if o==eye:continue
            for k in keys:
                if k.name.startswith('Seat'):
                    for i,t in ws.items():
                        if t:k.data[i].co=keys['Basis'].data[i].co+Vector(old[k.name][i]-old['Basis'][i])
        # Eye keys' seat deltas are independent translations, rebuilt from original amounts.
        for k in eye.data.shape_keys.key_blocks:
            if k.name.startswith('Seat'):
                t=int(k.name[4:])/100
                for dst,b in zip(k.data,eye.data.shape_keys.key_blocks['Basis'].data):dst.co=b.co+Vector((0,.04*t,-.129*t))
        compose(eye)
    compose(head)
def revise_mouth():
    head=v3.parts['Head'];mouth=bpy.data.objects['Shushu_MouthInterior']
    # Add a new full aperture without changing existing small-open / smile keys.
    # Recover the saved mouth rings from independent existing shape deltas,
    # avoiding re-cutting the head or depending on bmesh vertex ordering.
    def target(a):
        x=.034*math.cos(a);z=.588-.003*math.sin(math.pi*abs(x)/.034)+.026*math.sin(a)
        return Vector((x,-.266+2*x*x+.10*(z-.600),z))
    for o in [head,mouth]:
        keys=o.data.shape_keys.key_blocks;basis=keys['Basis'];small=keys['MouthOpen']
        if 'MouthDonorOpen' in keys:raise RuntimeError('Revision already applied')
        k=v3.shape(o,'MouthDonorOpen',lambda p:p);k.value=0
        for i,(dst,b,sm) in enumerate(zip(k.data,basis.data,small.data)):
            if o==mouth:
                if i==0:dst.co.z-=.012;continue
                w=1.;a=(i-1)/64*math.tau
            else:
                s=(sm.co.z-b.co.z)/.008;c=(keys['GentleSmile'].data[i].co.z-b.co.z)/.004
                w=.5*(c+math.sqrt(c*c+4*s*s))
                if w<.00001:continue
                t=round(math.sqrt(w)*8)/8;w=t*t
                sa=max(-1,min(1,s/w));ca=(1 if b.co.x>=0 else -1)*math.sqrt(max(0,1-sa*sa));a=math.atan2(sa,ca)
            dst.co=b.co+(target(a)-v3.mouth_point(a))*w
        # New shape rotates with all existing head pose controls.
        for label,(axis,angle) in HEAD_POSES.items():
            q=Quaternion(axis,math.radians(angle));c=v3.shape(o,'Corrective.Compose.'+label+'.MouthDonorOpen',lambda p:p);c.value=0
            for dest,f,b in zip(c.data,k.data,basis.data):delta=f.co-b.co;dest.co+=q@delta-delta
            driver=c.driver_add('value').driver
            for vn,kn in [('head',label),('face','MouthDonorOpen')]:
                var=driver.variables.new();var.name=vn;var.type='SINGLE_PROP';var.targets[0].id_type='KEY';var.targets[0].id=o.data.shape_keys;var.targets[0].data_path=f'key_blocks["{kn}"].value'
            driver.expression='head*face'
def revise_seat():
    for side in ['L','R']:
        o=v3.parts['Leg.'+side];keys=o.data.shape_keys.key_blocks
        for k in keys:
            if not k.name.startswith('Seat'):continue
            t=int(k.name[4:])/100
            for dst,b in zip(k.data,keys['Basis'].data):
                w=v3.smooth(.095,.205,b.co.z);center=Vector(((1 if side=='L' else -1)*(.14+.008*t),.065*t,b.co.z-.09*t))
                # Proximal thigh only: tuck the cap into pelvis, retain plantar frame.
                delta=dst.co-center;dst.co-=delta*(.18*t*w)
                dst.co.y+=.020*t*w;dst.co.z+=.020*t*w
def diagnose_colour():
    def mat(name,c):
        m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Roughness'].default_value=.6;return m
    white=mat('Diagnostic ivory',(.90,.86,.81));pink=mat('Diagnostic pink pattern / not eye',(.83,.26,.40));dark=mat('Diagnostic eyeball',(.055,.023,.043));inner=mat('Diagnostic mouth cavity',(.18,.028,.045))
    for o in v3.character:
        o.data.materials.clear();o.data.materials.append(dark if o.get('part','').startswith('Eye.') else inner if o.get('part')=='MouthInterior' else pink if o.get('part','').startswith(('Ear.','Paw.','Leg.')) else white)
    # Separate coloured head mask follows Basis, not world pose. No pixel image edits.
    h=v3.parts['Head'];m=mat('Diagnostic head mask',(.90,.86,.81));h.data.materials.clear();h.data.materials.append(m)
    attr=h.data.color_attributes.new(name='DiagnosticIdentity',type='FLOAT_COLOR',domain='CORNER')
    basis=h.data.shape_keys.key_blocks['Basis']
    for loop in h.data.loops:
        p=basis.data[loop.vertex_index].co;x=abs(p.x);r=((x-.134)/.071)**2+((p.z-.648)/.084)**2
        w=(1-v3.smooth(.88,1.08,r))*(1-v3.smooth(-.135,-.095,p.y))
        c=Vector((.90,.86,.81)).lerp(Vector((.83,.26,.40)),w)
        nose=abs(p.x)<.017 and .623<p.z<.641 and p.y<-.279
        attr.data[loop.index].color=(*(Vector((.055,.023,.043)) if nose else c),1)
    node=m.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name=attr.name;m.node_tree.links.new(node.outputs['Color'],m.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    groups,_=source_ids();v3.raw.data.materials.clear()
    head_material=h.data.materials[0]
    for m in [head_material,pink,dark,inner]:v3.raw.data.materials.append(m)
    raw_attr=v3.raw.data.color_attributes.new(name='DiagnosticIdentity',type='FLOAT_COLOR',domain='CORNER')
    for loop in v3.raw.data.loops:
        p=v3.raw.data.vertices[loop.vertex_index].co;x=abs(p.x);rr=((x-.134)/.071)**2+((p.z-.648)/.084)**2
        w=(1-v3.smooth(.88,1.08,rr))*(1-v3.smooth(-.135,-.095,p.y));c=Vector((.90,.86,.81)).lerp(Vector((.83,.26,.40)),w)
        if abs(p.x)<.017 and .623<p.z<.641 and p.y<-.279:c=Vector((.055,.023,.043))
        if abs(p.x)<.041 and .558<p.z<.616 and -.240<p.y<-.17:c=Vector((.18,.028,.045))
        raw_attr.data[loop.index].color=(*c,1)
    for i,faces in enumerate(groups):
        for idx in faces:v3.raw.data.polygons[idx].material_index=2 if i in [14,15] else 1 if i in [2,3,4,5,6,7] else 0
def render(name,view,face=True,colour=False):
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=12;sc.cycles.use_denoising=True;sc.render.resolution_x=480;sc.render.resolution_y=540;sc.render.resolution_percentage=100
    d=Vector(VIEWS[view]).normalized();target=Vector((0,-.04,.65) if face else (0,0,.49));scale=.54 if face else 1.15
    cam=v3.cam;cam.location=target+3*d;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    sc.render.filepath=str(OUT/'renders'/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
    records=json.loads((OUT/'cameras.json').read_text()) if (OUT/'cameras.json').exists() else {}
    records[name+'-'+view]={'direction':list(VIEWS[view]),'target':list(target),'ortho_scale':scale,'resolution':[480,540],'engine':'CYCLES','samples':12,'colour':'diagnostic' if colour else 'clay'};write('cameras.json',records)
def show_donor(on):
    v3.raw.hide_render=not on;v3.raw.hide_set(not on);bpy.data.collections['SOURCE_REFERENCE_ONLY'].hide_render=not on
    for o in v3.character:o.hide_render=on
def trials():
    variants=sys.argv[sys.argv.index('--variants')+1].split(',') if '--variants' in sys.argv else ['before','size-only','surround-only','combined']
    for variant in variants:
        if variant=='donor':continue
        load(BACK/v3.ASSET.name)
        if variant!='before':revise_eyes(variant)
        if variant=='combined':revise_mouth();revise_seat()
        v3.reset()
        write('trial-'+variant+'.json',{side:visible_eye(side) for side in ['L','R']})
        for view in VIEWS:render('eye-'+variant+'-clay',view)
        if variant in ['before','combined']:
            v3.sit(1)
            for view in VIEWS:render('seat-'+variant+'-clay',view,False)
            v3.reset()
        diagnose_colour()
        for view in VIEWS:render('eye-'+variant+'-colour',view,colour=True)
    if '--variants' not in sys.argv or 'donor' in variants:
        load(BACK/v3.ASSET.name);show_donor(True)
        for view in VIEWS:render('donor-clay',view)
        diagnose_colour()
        for view in VIEWS:render('donor-colour',view,colour=True)
def apply():
    # Refuse to overwrite model edits made concurrently since snapshot/application.
    for path in [v3.ASSET,v3.PROOF]:
        manifest=OUT/('continuity-'+path.stem+'.json')
        allowed={sha(BACK/path.name)}
        if manifest.exists():allowed.add(json.loads(manifest.read_text())['after_sha256'])
        assert sha(path) in allowed,('Concurrent model change: preserve and inspect',str(path))
    for path in [v3.ASSET,v3.PROOF]:
        load(BACK/path.name);before={o.name:{'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'keys':[k.name for k in o.data.shape_keys.key_blocks],'drivers':len(o.data.shape_keys.animation_data.drivers) if o.data.shape_keys.animation_data else 0} for o in v3.character}
        revise_eyes('combined');revise_mouth();revise_seat();v3.reset()
        for o in v3.character:
            row=before[o.name];assert len(o.data.vertices)==row['vertices'] and len(o.data.polygons)==row['polygons'];assert all(k in o.data.shape_keys.key_blocks for k in row['keys'])
        bpy.context.scene['Human Geometry Gate']='PENDING';bpy.context.scene['v003_local_revision']='donor-visible eye size / softened annulus / proximal seat / full mouth'
        bpy.ops.wm.save_as_mainfile(filepath=str(path));write('continuity-'+path.stem+'.json',{'before':before,'after_sha256':sha(path),'baseline_sha256':sha(BACK/path.name),'Human_Gate':'PENDING'})
    load(v3.ASSET);v3.validate_geometry();v3.export_static()
    prop=bpy.data.objects['Inspection_HeldProp'];v3.pose('hold');c=Vector(prop['hold_center']);r=prop['radius'];ds=[v3.tree(v3.parts['Paw.'+s]).find_nearest(c)[3] for s in ['L','R']];clearance=v3.tree(v3.parts['Torso']).find_nearest(c)[3]-r
    assert all(abs(d-r)<.0001 for d in ds) and clearance>.002
    v3.write('hold-contact.json',{'center':list(c),'radius':r,'paw_surface_distance':ds,'paw_gap':[d-r for d in ds],'torso_clearance':clearance,'meaning':'Existing hold prop/control retained and rechecked.'})
    v3.reset();write('eye-measurements-after.json',{s:visible_eye(s) for s in ['L','R']})
    preserved=json.loads((BACK/'preserved.json').read_text());assert all(sha(ROOT/p)==h for p,h in preserved.items());write('preserved-inputs.json',preserved)
def final_renders():
    for colour in [False,True]:
        load(v3.ASSET)
        if colour:diagnose_colour()
        kind='colour' if colour else 'clay'
        for state in ['neutral','small','donor-open','smile']:
            v3.reset()
            if state=='small':v3.key('MouthOpen')
            if state=='donor-open':v3.key('MouthDonorOpen')
            if state=='smile':v3.key('GentleSmile');v3.key('MouthDonorOpen',.65)
            for view in VIEWS:render('mouth-'+state+'-'+kind,view,colour=colour)
        for state,t in [('standing',0),('seat25',.25),('seat50',.5),('seat75',.75),('seated',1)]:
            v3.reset();v3.sit(t)
            for view in VIEWS:render(state+'-'+kind,view,False,colour)
        for state,t in [('half',.5),('closed',1),('wink',.7)]:
            v3.reset();v3.key('Blink.L',t);v3.key('Blink.R',t if state!='wink' else 0)
            for view in VIEWS:render('blink-'+state+'-'+kind,view,colour=colour)
    print('V003_REVISION_RENDERS_COMPLETE',flush=True)
if __name__=='__main__':
    snapshot()
    if '--measure' in sys.argv:measure()
    elif '--trials' in sys.argv:trials()
    elif '--apply' in sys.argv:apply()
    elif '--render' in sys.argv:final_renders()
    else:raise RuntimeError('Choose --measure / --trials / --apply / --render')
