"""Continue saved 2031076 geometry; local expression and seated silhouette refinement."""
import bpy, math, json, sys, shutil, importlib.util, hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('revision',Path(__file__).with_name('revise-shushu-geometry-v003.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
v=r.v3
OUT=v.OUT/'appeal-revision';OUT.mkdir(exist_ok=True);(OUT/'renders').mkdir(exist_ok=True)
BACK=ROOT/'.git/shushu-v003-2031076';BACK.mkdir(exist_ok=True)
BASE='2031076828185dd714cf9aca8438c289942986fd'
def write(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def backup():
    for p in [v.ASSET,v.PROOF]:
        dest=BACK/p.name
        if not dest.exists():
            import subprocess
            data=subprocess.run(['git','show',BASE+':'+p.relative_to(ROOT).as_posix()],cwd=ROOT,check=True,capture_output=True).stdout
            if data.startswith(b'version https://git-lfs.github.com/spec/v1'):
                data=subprocess.run(['git','lfs','smudge'],input=data,cwd=ROOT,check=True,capture_output=True).stdout
            assert data.startswith(b'BLENDER') or data[:4]==bytes([0x28,0xb5,0x2f,0xfd])
            dest.write_bytes(data)
    if not (OUT/'protected-inputs.json').exists():
        paths=list(ROOT.glob('*.png'))+list(ROOT.glob('*18-27*'))+list((v.OUT.parent/'geometry-v002').glob('review-*.png'))
        paths+=list((ROOT/'assets/grimo/production/shushu/image-reference').rglob('*.png'))
        paths+=list((ROOT/'assets/grimo/source/shushu').rglob('*.png'))
        write('protected-inputs.json',{p.relative_to(ROOT).as_posix():r.sha(p) for p in paths})
def patch_parameters(head):
    keys=head.data.shape_keys.key_blocks;out={}
    for i,b in enumerate(keys['Basis'].data):
        s=(keys['MouthOpen'].data[i].co.z-b.co.z)/.008
        c=(keys['GentleSmile'].data[i].co.z-b.co.z)/.004
        w=.5*(c+math.sqrt(c*c+4*s*s))
        if w<.00001:continue
        t=round(math.sqrt(w)*8)/8;w=t*t
        sa=max(-1,min(1,s/w));ca=(1 if b.co.x>=0 else -1)*math.sqrt(max(0,1-sa*sa))
        out[i]=(w,math.atan2(sa,ca))
    return out
def full_point(a):
    c=math.cos(a);s=math.sin(a);x=.0375*c
    z=.606-.007*math.sin(math.pi*abs(c))+.008*s if s>=0 else .606-.050*(-s)**.85
    return Vector((x,-.266+2*x*x+.10*(z-.600),z))
def mouth_refine():
    head=v.parts['Head'];mouth=bpy.data.objects['Shushu_MouthInterior'];params=patch_parameters(head)
    for o in [head,mouth]:
        keys=o.data.shape_keys.key_blocks;basis=keys['Basis']
        for i,(w,a) in (params.items() if o==head else ((i,(1.,(i-1)/64*math.tau)) for i in range(1,65))):
            keys['MouthDonorOpen'].data[i].co=basis.data[i].co+(full_point(a)-v.mouth_point(a))*w
            c=math.cos(a);s=math.sin(a);x=.028*c
            z=.602-.003*math.sin(math.pi*abs(c))+.001*s if s>=0 else .602-.014*(-s)**.85
            small=Vector((x,-.266+2*x*x+.10*(z-.600),z))
            keys['MouthOpen'].data[i].co=basis.data[i].co+(small-v.mouth_point(a))*w
            # Wider, raised corners give a readable smile; use full=.8 + smile=1.
            delta=Vector((.004*math.cos(a),0,.009*math.cos(a)**2))
            delta.y=4*basis.data[i].co.x*delta.x+.10*delta.z
            keys['GentleSmile'].data[i].co=basis.data[i].co+delta*w
        if o==mouth:
            # Shallow curved chamber instead of the former deep cone.
            for k in keys:
                if k.name.startswith(('Head','Corrective.Compose.')):continue
                k.data[0].co.y-=.020
            keys['MouthDonorOpen'].data[0].co.z=.580
        r.compose(o)
    # Cheek lift ties the smile to the muzzle rather than only changing the hole.
    keys=head.data.shape_keys.key_blocks
    for i,b in enumerate(keys['Basis'].data):
        p=b.co;w=math.exp(-2*(((abs(p.x)-.065)/.045)**2+((p.z-.604)/.033)**2))*max(0,min(1,(-p.y-.17)/.06))
        if i in params:w*=1-math.sqrt(params[i][0])
        keys['GentleSmile'].data[i].co+=Vector((0,-.003*w,.003*w))
    r.compose(head)
    rebuild_chamber(mouth)
def rebuild_chamber(o):
    """Curved cavity and an attached lower tongue surface, all under same controls.

    Shape key names, action and scripted composition drivers are transferred.
    Parametric evaluation is only for the local mouth interior, never the head.
    """
    old=o.data.shape_keys;arrays={k.name:np.array([p.co for p in k.data]) for k in old.key_blocks}
    action=old.animation_data.action if old.animation_data else None
    slot=old.animation_data.action_slot if action else None
    driver_specs=[]
    if old.animation_data:
        for f in old.animation_data.drivers:
            driver_specs.append((f.data_path,f.driver.expression,[(x.name,x.targets[0].data_path) for x in f.driver.variables]))
    faces=[];n=64
    for i in range(n):faces.append((0,1+(i+1)%n,1+i))
    for ring in range(3):
        start=1+ring*n
        for i in range(n):faces.append((start+i,start+(i+1)%n,start+n+(i+1)%n,start+n+i))
    tongue_start=257;first_tongue_face=len(faces)
    for i in range(n):faces.append((tongue_start,tongue_start+1+(i+1)%n,tongue_start+1+i))
    for ring in range(2):
        start=tongue_start+1+ring*n
        for i in range(n):faces.append((start+i,start+(i+1)%n,start+n+(i+1)%n,start+n+i))
    def generate(a):
        center=a[0].copy();rim=a[1:];verts=[center.copy()]
        for rad in [.25,.5,.75,1.]:
            for p in rim:
                co=center+(p-center)*rad
                g=math.sqrt(max(0,1-rad*rad));co[1]=p[1]*(1-g)+center[1]*g
                verts.append(co)
        lo=rim.min(0);hi=rim.max(0);width=hi[0]-lo[0];height=hi[2]-lo[2]
        tc=np.array([(lo[0]+hi[0])*.5,center[1]-.009,lo[2]+height*.25])
        verts.append(tc.copy())
        for rad in [1/3,2/3,1.]:
            for i in range(n):
                angle=i/n*math.tau
                verts.append(tc+np.array([width*.29*math.cos(angle)*rad,.003*rad*rad,height*.205*math.sin(angle)*rad]))
        return np.array(verts)
    generated={name:generate(a) for name,a in arrays.items() if not name.startswith(('Head','Corrective.Compose.'))}
    new=bpy.data.meshes.new('Shushu_MouthInterior_curved_chamber');new.from_pydata(generated['Basis'].tolist(),[],faces);new.update()
    new.materials.append(v.clay);o.data=new
    for poly in new.polygons:poly.use_smooth=True
    for name in arrays:
        k=o.shape_key_add(name=name,from_mix=False);k.value=0
        a=generated.get(name,generated['Basis'])
        for dst,co in zip(k.data,a):dst.co=co
    if action:
        ad=new.shape_keys.animation_data_create();ad.action=action
        if slot:ad.action_slot=slot
    for path,expr,variables in driver_specs:
        d=new.shape_keys.driver_add(path).driver;d.expression=expr
        for name,path in variables:
            x=d.variables.new();x.name=name;x.type='SINGLE_PROP';x.targets[0].id_type='KEY';x.targets[0].id=new.shape_keys;x.targets[0].data_path=path
    o['tongue_first_polygon']=first_tongue_face;o['mouth_rim_vertex_start']=193;o['mouth_rim_vertex_count']=64
    r.compose(o)
def seat_refine():
    # Smooth the leg's existing bent volume with a local, boundary-constrained
    # Laplacian. The foot, standing pose and original contact frame stay intact.
    for side in ['L','R']:
        o=v.parts['Leg.'+side];keys=o.data.shape_keys.key_blocks
        b=np.array([p.co for p in keys['Basis'].data]);adj=[[] for _ in b]
        for e in o.data.edges:
            a,c=e.vertices;adj[a].append(c);adj[c].append(a)
        full=np.array([p.co for p in keys['Seat100'].data]);sign=1 if side=='L' else -1
        for k in keys:
            if not k.name.startswith('Seat'):continue
            t=int(k.name[4:])/100;a=np.array([p.co for p in k.data]);original=a.copy()
            weights=np.array([v.smooth(.075,.125,z)*(1-v.smooth(.225,.28,z)) for z in b[:,2]])
            for _ in range(8):
                avg=np.array([a[ids].mean(0) if ids else a[i] for i,ids in enumerate(adj)])
                a+=(avg-a)*(.42*t*weights[:,None])
            # Fill the narrow ankle-to-thigh waist, then bury the proximal cap
            # inside the rump with a smooth support-preserving field.
            for i,p in enumerate(a):
                z=b[i,2];w=v.smooth(.080,.15,z)
                target=np.array([sign*.16+(b[i,0]-sign*.14)*1.1,-.105+(z-.08)*1.1,.14-b[i,1]])
                p+=(target-full[i])*t*w
                for j in range(3):k.data[i].co[j]=float(p[j])
    continuous_body()
def continuous_body():
    """An evaluated union follows the retained torso/leg deformation sources.

    This is a geometry-review skin, with changing evaluated topology. It is not
    claimed to be a final skinned game mesh or a morph-target export.
    """
    torso=v.parts['Torso']
    ng=bpy.data.node_groups.new('Shushu continuous body from editable controls','GeometryNodeTree')
    ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry')
    ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    nodes=ng.nodes;links=ng.links;inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');join=nodes.new('GeometryNodeJoinGeometry')
    links.new(inp.outputs['Geometry'],join.inputs['Geometry'])
    for side in ['L','R']:
        leg=v.parts['Leg.'+side];info=nodes.new('GeometryNodeObjectInfo');info.transform_space='RELATIVE';info.inputs['Object'].default_value=leg;info.inputs['As Instance'].default_value=False
        links.new(info.outputs['Geometry'],join.inputs['Geometry']);leg.hide_render=True;leg.hide_set(True)
    links.new(join.outputs['Geometry'],out.inputs['Geometry'])
    mod=torso.modifiers.new('Continuous body source union','NODES');mod.node_group=ng
    mod=torso.modifiers.new('Continuous soft body surface','REMESH');mod.mode='VOXEL';mod.voxel_size=.0025;mod.use_smooth_shade=True;mod.adaptivity=0
    mod=torso.modifiers.new('Soft junction relaxation','SMOOTH');mod.factor=.8;mod.iterations=60
    torso['surface_representation']='Evaluated voxel union of retained deforming torso and legs; geometry proof, not final morph topology'
def lids_refine():
    head=v.parts['Head'];keys=head.data.shape_keys.key_blocks
    for side,sign in [('L',1),('R',-1)]:
        g=head.vertex_groups['Local eyelid thickness.'+side]
        eye=bpy.data.objects['Shushu_Eye.'+side]
        cap=np.array([p.co for p in eye.data.shape_keys.key_blocks['Basis'].data][:513]);x=cap[:,0];z=cap[:,2]
        coeff=np.linalg.lstsq(np.array([np.ones(len(x)),x,z,x*x,x*z,z*z]).T,cap[:,1],rcond=None)[0]
        for p in head.data.vertices:
            t=math.sqrt(next((a.weight for a in p.groups if a.group==g.index),0))
            if not t:continue
            i=p.index;closed=keys['Blink.'+side].data[i];basis=keys['Basis'].data[i]
            old=closed.co.copy();u=(old.x-sign*.129)/.051
            # A gently arched seam, with the centre lifted, gives a soft closure.
            dz=.010*max(0,1-u*u)*t
            closed.co.z+=dz
            x,z=closed.co.x,closed.co.z
            y=float(coeff@np.array([1,x,z,x*x,x*z,z*z]))-.004
            closed.co.y+=(y-closed.co.y)*v.smooth(.2,.9,t)*.50
            # Half-blink keeps its original aperture, only follows half the new
            # closure delta; no change to the restored open-eye dimensions.
            # Existing HalfBlink key is a delta corrective and stays intact.
    r.compose(head)
    rebuild_lid_walls()
def rebuild_lid_walls():
    """Replace normal extrusion, which folded across the right half-open eye,
    with a thin, backward-facing aperture sleeve following all head keys.
    """
    head=v.parts['Head'];source=head.data.shape_keys
    for side in ['L','R']:
        old=head.modifiers['Inner eyelid wall.'+side];old.show_viewport=False;old.show_render=False
        group=head.vertex_groups['Local eyelid thickness.'+side]
        ids={p.index for p in head.data.vertices if any(x.group==group.index and x.weight>.99 for x in p.groups)}
        adjacent={i:[] for i in ids}
        for e in head.data.edges:
            i,j=e.vertices
            if i in ids and j in ids:adjacent[i].append(j);adjacent[j].append(i)
        assert all(len(neighbors)==2 for neighbors in adjacent.values())
        first=min(ids);order=[first];previous=None;current=first
        while True:
            nxt=next(i for i in adjacent[current] if i!=previous)
            if nxt==first:break
            order.append(nxt);previous,current=current,nxt
        assert len(order)==len(ids)
        n=len(order);faces=[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
        basis=[source.key_blocks['Basis'].data[i].co.copy() for i in order]
        o=v.mesh('Shushu_LidWall.'+side,basis+[p+Vector((0,.024,0)) for p in basis],faces);o['part']='LidWall.'+side
        for col in list(o.users_collection):col.objects.unlink(o)
        bpy.data.collections['CHARACTER_EDITABLE'].objects.link(o);v.character.append(o)
        for original in source.key_blocks:
            k=o.shape_key_add(name=original.name,from_mix=False);k.value=0
            for j,i in enumerate(order):
                p=original.data[i].co;k.data[j].co=p;k.data[n+j].co=p+Vector((0,.024,0))
        ad=o.data.shape_keys.animation_data_create()
        if source.animation_data.action:
            ad.action=source.animation_data.action;ad.action_slot=source.animation_data.action_slot
        for f in source.animation_data.drivers:
            d=o.data.shape_keys.driver_add(f.data_path).driver;d.expression=f.driver.expression
            for original in f.driver.variables:
                x=d.variables.new();x.name=original.name;x.type='SINGLE_PROP';x.targets[0].id_type='KEY';x.targets[0].id=o.data.shape_keys;x.targets[0].data_path=original.targets[0].data_path
        r.compose(o)
        mod=o.modifiers.new('Match subdivided aperture','SUBSURF');mod.levels=1;mod.render_levels=1
        o['construction']='Backward aperture sleeve, not normal-based solidify; all head expression/pose keys and action copied'
def refine(): mouth_refine();seat_refine();lids_refine();v.reset()
def load(path): r.load(path)
def render(name,view,face=True,colour=False):
    old=r.OUT;r.OUT=OUT
    r.render(name,view,face,colour);r.OUT=old
def colour():
    r.diagnose_colour()
    for o in v.character:
        if o.get('part','').startswith('LidWall.'):
            o.data.materials.clear();o.data.materials.append(bpy.data.materials['Diagnostic pink pattern / not eye'])
    torso=v.parts['Torso']
    if 'Continuous soft body surface' in torso.modifiers:
        ng=bpy.data.node_groups.new('Diagnostic ivory after union','GeometryNodeTree')
        ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
        inp=ng.nodes.new('NodeGroupInput');out=ng.nodes.new('NodeGroupOutput');mat=ng.nodes.new('GeometryNodeSetMaterial');mat.inputs['Material'].default_value=torso.data.materials[0]
        ng.links.new(inp.outputs['Geometry'],mat.inputs['Geometry']);ng.links.new(mat.outputs['Geometry'],out.inputs['Geometry'])
        mod=torso.modifiers.new('Diagnostic colour override','NODES');mod.node_group=ng
    mouth=bpy.data.objects['Shushu_MouthInterior']
    if 'tongue_first_polygon' in mouth:
        m=bpy.data.materials.new('Diagnostic tongue - geometry attached to mouth');m.diffuse_color=(.94,.32,.34,1);m.use_nodes=True
        m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.94,.32,.34,1)
        m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.55
        mouth.data.materials.append(m)
        for p in list(mouth.data.polygons)[mouth['tongue_first_polygon']:]:p.material_index=1
    # A labelled upper-lid edge cue separates lid skin from eyeball and pink mask.
    h=v.parts['Head'];basis=h.data.shape_keys.key_blocks['Basis'];attr=h.data.color_attributes['DiagnosticIdentity']
    weights={}
    for side,sign in [('L',1),('R',-1)]:
        g=h.vertex_groups['Local eyelid thickness.'+side]
        for p in h.data.vertices:
            t=math.sqrt(next((a.weight for a in p.groups if a.group==g.index),0));co=basis.data[p.index].co
            above=co.z-.660-sign*.20*(co.x-sign*.129)
            if t>.86 and above>0:weights[p.index]=v.smooth(.86,.99,t)
    for loop in h.data.loops:
        if loop.vertex_index in weights:
            old=Vector(attr.data[loop.index].color[:3]);c=old.lerp(Vector((.085,.025,.040)),weights[loop.vertex_index]);attr.data[loop.index].color=(*c,1)
def coloured_body():
    """Temporary evaluated colour mesh, using distance to the current source parts.
    No rendered pixels or saved editable materials are modified.
    """
    torso=v.parts['Torso']
    if 'Continuous soft body surface' not in torso.modifiers:return None
    vv,tt=v.evaluated(torso)
    mods=list(torso.modifiers)
    for m in mods:m.show_viewport=False
    tb=v.tree(torso)
    for m in mods:m.show_viewport=True
    lb=[v.tree(v.parts['Leg.'+s]) for s in ['L','R']]
    o=v.mesh('Diagnostic continuous body',vv.tolist(),tt.tolist())
    m=bpy.data.materials.new('Diagnostic source distance colour');m.use_nodes=True
    bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Roughness'].default_value=.6
    attr=o.data.color_attributes.new(name='BodyDiagnostic',type='FLOAT_COLOR',domain='POINT')
    for i,p in enumerate(vv):
        p=Vector(p);dt=tb.find_nearest(p)[3];dl=min(tr.find_nearest(p)[3] for tr in lb)
        w=v.smooth(-.009,.009,dt-dl);c=Vector((.90,.86,.81)).lerp(Vector((.83,.26,.40)),w);attr.data[i].color=(*c,1)
    node=m.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name=attr.name;m.node_tree.links.new(node.outputs['Color'],bs.inputs['Base Color'])
    o.data.materials.clear();o.data.materials.append(m);torso.hide_render=True
    return o
def pose(state):
    v.reset()
    if state=='small':v.key('MouthOpen')
    if state=='full':v.key('MouthDonorOpen')
    if state in ['smile','happy-closed','companion']:
        v.key('GentleSmile');v.key('HappyLids',.45)
        if state!='happy-closed':v.key('MouthDonorOpen',.8)
    if state=='companion':v.sit(1);v.key('HeadTilt.L',.2);v.key('Blink.L',.15);v.key('Blink.R',.15)
    if state.startswith('seat'):v.sit(float(state[4:])/100)
    if state in ['closed','happy-closed','half','wink']:
        v.key('Blink.L',.5 if state=='half' else 1);v.key('Blink.R',.5 if state=='half' else 0 if state=='wink' else 1)
def final_renders():
    groups={'mouth':['neutral','small','full','smile'],'body':['standing','seat25','seat50','seat75','seat100'],'lids':['half','closed','happy-closed','wink']}
    chosen=sys.argv[sys.argv.index('--group')+1] if '--group' in sys.argv else 'all'
    kinds=[True] if '--colour-only' in sys.argv else [False,True]
    for col in kinds:
        load(v.ASSET)
        if col:colour()
        kind='colour' if col else 'clay'
        for group,states in groups.items():
            if chosen not in ['all',group]:continue
            for state in states:
                pose(state);body=coloured_body() if col and group=='body' else None
                for view in r.VIEWS:render(group+'-'+state+'-'+kind,view,group!='body',col)
                if body:bpy.data.objects.remove(body,do_unlink=True);v.parts['Torso'].hide_render=False
        if chosen in ['all','companion']:
            pose('companion');body=coloured_body() if col else None
            for view in r.VIEWS:render('companion-'+kind,view,False,col)
            if body:bpy.data.objects.remove(body,do_unlink=True);v.parts['Torso'].hide_render=False
    print('APPEAL_RENDERS_COMPLETE',flush=True)
def reference_renders():
    states=sys.argv[sys.argv.index('--states')+1].split(',') if '--states' in sys.argv else ['neutral','small','full','smile','seat100','half','closed']
    for col in [False,True]:
        load(BACK/v.ASSET.name)
        if col:colour()
        kind='colour' if col else 'clay'
        for state in states:
            pose(state)
            # Baseline smile uses its documented .65 opening, no added HappyLids.
            if state=='smile':v.key('MouthDonorOpen',.65);v.key('HappyLids',0)
            for view in r.VIEWS:render('baseline-'+state+'-'+kind,view,state!='seat100',col)
        if '--states' not in sys.argv:
            v.reset();r.show_donor(True)
            for view in r.VIEWS:render('donor-'+kind,view,True,col)
    print('APPEAL_REFERENCE_RENDERS_COMPLETE',flush=True)
def lid_probe():
    load(v.ASSET);pose('half');head=v.parts['Head'];report={}
    for side in ['L','R']:
        group=head.vertex_groups['Local eyelid thickness.'+side]
        ids={p.index for p in head.data.vertices if any(x.group==group.index and x.weight>.99 for x in p.groups)}
        report[side]={'inner_ring_vertices':len(ids),'base_y_normals':[list(p.normal) for p in head.data.polygons if all(i in ids for i in p.vertices)][:10]}
    for m in head.modifiers:
        if m.type=='SOLIDIFY':m.show_render=False;m.show_viewport=False
    for view in ['front','3q']:render('probe-half-no-walls',view)
    write('lid-probe.json',report)
def preview():
    load(BACK/v.ASSET.name);refine()
    states=sys.argv[sys.argv.index('--states')+1].split(',') if '--states' in sys.argv else ['full','smile','closed','half','seat']
    for state in states:
        v.reset()
        if state=='full':v.key('MouthDonorOpen')
        if state=='smile':v.key('MouthDonorOpen',.8);v.key('GentleSmile');v.key('HappyLids',.45)
        if state in ['closed','half']:v.key('Blink.L',1 if state=='closed' else .5);v.key('Blink.R',1 if state=='closed' else .5)
        if state=='seat':v.sit(1)
        body=state in ['seat','standing']
        for view in (['side','3q'] if body else ['front','3q']):render('trial-'+state,view,not body)
    bpy.ops.wm.save_as_mainfile(filepath=str(BACK/'candidate.blend'))
def apply():
    for p in [v.ASSET,v.PROOF]:
        allowed={r.sha(BACK/p.name)}
        if (OUT/'continuity.json').exists():allowed.add(json.loads((OUT/'continuity.json').read_text())[p.name]['after_sha256'])
        assert r.sha(p) in allowed,('Concurrent model edit',p)
    report={}
    for p in [v.ASSET,v.PROOF]:
        load(BACK/p.name);refine();bpy.context.scene['Human Geometry Gate']='PENDING';bpy.context.scene['v003_appeal_revision']='2031076 continuation: smile chamber / seated continuity / soft lids'
        note=bpy.data.texts.get('READ_ME_v003')
        note.write('\n2031076 appeal continuation: Human PENDING, Tripo HOLD.\nTorso uses the retained, hidden Leg.L/R controls through an evaluated continuous skin. Edit source shape keys normally; do not render/export the legs twice. The evaluated skin topology varies with pose; this is not the final runtime rig.\nMouthOpen is the small opening; crossfade to MouthDonorOpen for full opening. Smile: MouthDonorOpen=.8, GentleSmile=1, HappyLids=.45.\nLidWall.L/R replace folding normal-extruded walls with backward sleeves, following all head controls and the proof action. Old head Solidify modifiers remain disabled for provenance.\nEvidence: docs/production/shushu/evidence/geometry-v003/appeal-revision/REVIEW.md\n')
        bpy.ops.wm.save_as_mainfile(filepath=str(p));report[p.name]={'baseline_sha256':r.sha(BACK/p.name),'after_sha256':r.sha(p)}
    write('continuity.json',report)
    load(v.ASSET);v.validate_geometry()
    # Hidden leg meshes are deformation sources, already included in torso skin.
    source_character=v.character;v.character=[o for o in source_character if not o.hide_render]
    v.export_static();v.character=source_character
if __name__=='__main__':
    backup()
    if '--preview' in sys.argv:preview()
    if '--apply' in sys.argv:apply()
    if '--render' in sys.argv:final_renders()
    if '--references' in sys.argv:reference_renders()
    if '--lid-probe' in sys.argv:lid_probe()
