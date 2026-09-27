"""Phase 1: current-authority fleece on the accepted Skin. Blender background CLI.

No historical geometry, view-conditioned geometry, production rig or animation.
Re-run from accepted Skin; render mode reopens the saved candidate.
"""
import bpy, math, random, json, sys, hashlib
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
ASSET = ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v001.blend'
BASE = ROOT/'assets/grimo/production/carol/blender/carol-skin-final-v002.blend'
OUT = ROOT/'docs/production/carol/evidence/normal-fleece-v001'
OUT.mkdir(parents=True, exist_ok=True)
MODE = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []

def link_parent(o,p):
    world=o.matrix_world.copy(); o.parent=p; o.matrix_world=world

def empty(name, loc):
    o=bpy.data.objects.new(name,None); bpy.context.scene.collection.objects.link(o)
    o.location=loc; o.empty_display_size=.025; return o

def material(name, base, blue):
    m=bpy.data.materials.new(name); m.diffuse_color=(*base,1); m.use_nodes=True
    n=m.node_tree.nodes; l=m.node_tree.links; bs=n.get('Principled BSDF')
    bs.inputs['Roughness'].default_value=.77
    bs.inputs['Subsurface Weight'].default_value=.065
    bs.inputs['Subsurface Radius'].default_value=(.04,.025,.018)
    bs.inputs['Sheen Weight'].default_value=.22
    tex=n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=35
    tex.inputs['Detail'].default_value=2.0; tex.inputs['Roughness'].default_value=.65
    coord=n.new('ShaderNodeTexCoord'); l.new(coord.outputs['Object'],tex.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.18
    ramp.color_ramp.elements[0].color=(*(base[k]*.80+blue[k]*.20 for k in range(3)),1)
    ramp.color_ramp.elements[1].position=.8; ramp.color_ramp.elements[1].color=(*base,1)
    l.new(tex.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],bs.inputs['Base Color'])
    fine=n.new('ShaderNodeTexNoise'); fine.inputs['Scale'].default_value=420
    l.new(coord.outputs['Object'],fine.inputs['Vector'])
    bump=n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.085
    bump.inputs['Distance'].default_value=.00035
    l.new(fine.outputs['Fac'],bump.inputs['Height']); l.new(bump.outputs['Normal'],bs.inputs['Normal'])
    return m

def cloud(name,c,r,normal,region,mat,seed,quiet=False):
    """Unequal volumetric lobes, voxel-welded into one continuous editable unit."""
    rng=random.Random(seed); n=Vector(normal).normalized()
    e=Vector((0,0,1)).cross(n)
    if e.length<.1:e=Vector((0,1,0))
    e.normalize(); f=n.cross(e).normalized(); pieces=[]
    lobes=[((0,0,-.05),(.78,.73,.79))]
    if not quiet:
        count=4+seed%2
        for i in range(count):
            a=2*math.pi*i/count+rng.uniform(-.20,.20)
            reach=rng.uniform(.45,.56); rad=rng.uniform(.45,.60)
            lobes.append(((reach*math.cos(a),reach*math.sin(a),rng.uniform(-.01,.17)),(rad,rad*rng.uniform(.85,1.12),rad*.92)))
    else:lobes=[((0,0,0),(1,1,1))]
    for pos,scale in lobes:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20)
        o=bpy.context.object
        for v in o.data.vertices:
            q=Vector(tuple(pos[k]+v.co[k]*scale[k] for k in range(3)))
            v.co=Vector(c)+e*q.x*r[0]+f*q.y*r[1]+n*q.z*r[2]
        pieces.append(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in pieces:o.select_set(True)
    bpy.context.view_layer.objects.active=pieces[0]; bpy.ops.object.join(); o=pieces[0]; o.name=name
    rem=o.modifiers.new('Welded cloud junctions','REMESH'); rem.mode='VOXEL'; rem.voxel_size=.0045 if min(r)>.06 else .0025; rem.use_smooth_shade=True
    bpy.ops.object.modifier_apply(modifier=rem.name)
    sm=o.modifiers.new('Soft junction recovery','SMOOTH'); sm.factor=1.3; sm.iterations=5
    bpy.ops.object.modifier_apply(modifier=sm.name)
    dec=o.modifiers.new('Practical control surface','DECIMATE'); dec.ratio=.16
    bpy.ops.object.modifier_apply(modifier=dec.name)
    for p in o.data.polygons:p.use_smooth=True
    o.data.materials.append(mat); o['semantic_region']=region; o['motion_owner']='head' if region in ['crown','face_frame'] else 'tail' if region=='tail' else 'torso'
    o['construction']='Unequal welded volumetric lobes, broad core, no per-lobe transform animation'
    link_parent(o,owners[o['motion_owner']]); clouds.append(o)
    vg=o.vertex_groups.new(name=region); vg.add(list(range(len(o.data.vertices))),1,'REPLACE')
    # Continuous local masks, independent of object boundaries.
    for side,sign in [('L',1),('R',-1)]:
        g=o.vertex_groups.new(name='touch_'+side)
        for v in o.data.vertices:
            w=max(0,min(1,.5+sign*v.co.y/.12))
            if w:g.add([v.index],w,'REPLACE')
    o.shape_key_add(name='Basis')
    k=o.shape_key_add(name='Local_contact_compress')
    for v,p in zip(o.data.vertices,k.data):
        d=v.co-Vector(c); weight=math.exp(-((d.dot(e)/max(r[0],.01))**2+(d.dot(f)/max(r[1],.01))**2)*2)
        p.co=v.co-n*(.018*weight)
    if region in ['face_frame','chest_front']:
        k=o.shape_key_add(name='Face_opening_corrective')
        for v,p in zip(o.data.vertices,k.data):
            d=v.co-Vector(c); w=math.exp(-sum((d[j]/max(r))**2 for j in range(3))*1.8)
            p.co=v.co+Vector((.018,math.copysign(.018,c[1]) if abs(c[1])>.1 else 0,-.012 if c[2]<.35 else .010))*w
    print('CLOUD_DONE',name,flush=True)
    return o

def motif(name,c,size,normal,moon=False,owner='torso'):
    n=Vector(normal).normalized(); e=Vector((0,0,1)).cross(n).normalized(); f=n.cross(e).normalized()
    # Ray attach to actual evaluated fleece, excluding Skin and other motifs.
    from mathutils.bvhtree import BVHTree
    deps=bpy.context.evaluated_depsgraph_get(); origin=Vector(c)+n*.8; hits=[]
    allverts=[]; allfaces=[]
    for ob in clouds:
        ev=ob.evaluated_get(deps); me=ev.to_mesh()
        offset=len(allverts); allverts.extend(ob.matrix_world@v.co for v in me.vertices)
        allfaces.extend(tuple(offset+i for i in p.vertices) for p in me.polygons)
        tree=BVHTree.FromPolygons([ob.matrix_world@v.co for v in me.vertices],[p.vertices[:] for p in me.polygons])
        hit,norm,idx,dist=tree.ray_cast(origin,-n,1.5)
        if hit is not None:hits.append((dist,hit))
        ev.to_mesh_clear()
    if hits:c=min(hits,key=lambda x:x[0])[1]+n*.007
    if not moon:
        tree=BVHTree.FromPolygons(allverts,allfaces)
        verts=[]; faces=[]; N=80; rings=8; c=Vector(c)
        def point(a,rad,back=False):
            rr=size*(.78+.22*math.cos(5*a))*rad
            pos=c+e*(rr*math.sin(a))+f*(rr*math.cos(a))
            h,_,_,_=tree.ray_cast(pos+n*.6,-n,1.2)
            if h is not None:pos=h
            return pos+n*((.004 if back else .012+.014*(1-rad*rad)))
        for back in [False,True]:
            start=len(verts);verts.append(point(0,0,back))
            for j in range(1,rings+1):
                for i in range(N):verts.append(point(math.tau*i/N,j/rings,back))
            for i in range(N):faces.append((start,start+1+i,start+1+(i+1)%N))
            for j in range(rings-1):
                a=start+1+j*N;b=a+N
                for i in range(N):faces.append((a+i,b+i,b+(i+1)%N,a+(i+1)%N))
        layer=1+rings*N;a=1+(rings-1)*N;b=layer+a
        for i in range(N):faces.append((a+i,a+(i+1)%N,b+(i+1)%N,b+i))
        me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
        import bmesh
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
        o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o);me.materials.append(gold)
        for p in me.polygons:p.use_smooth=True
        link_parent(o,owners[owner]);a=empty(name+'_anchor',c);link_parent(a,owners[owner]);return o
    curve=bpy.data.curves.new(name,'CURVE'); curve.dimensions='2D'; curve.resolution_u=16
    curve.fill_mode='BOTH'; curve.extrude=.006; curve.bevel_depth=.004; curve.bevel_resolution=3
    coords=[]
    if moon:
        for i in range(65):
            a=math.radians(55+250*i/64); coords.append((math.cos(a)*size,math.sin(a)*size))
        start,end=coords[-1],coords[0]
        for i in range(1,49):
            t=i/48; coords.append(((1-t)*start[0]+t*end[0]-.87*size*math.sin(math.pi*t),(1-t)*start[1]+t*end[1]))
    else:
        for i in range(100):
            a=2*math.pi*i/100; rad=size*(.78+.22*math.cos(5*a)); coords.append((rad*math.sin(a),rad*math.cos(a)))
    sp=curve.splines.new('POLY'); sp.points.add(len(coords)-1)
    for p,(x,y) in zip(sp.points,coords):p.co=(x,y,0,1)
    sp.use_cyclic_u=True; o=bpy.data.objects.new(name,curve); bpy.context.scene.collection.objects.link(o)
    from mathutils import Matrix
    o.matrix_world=Matrix(((e.x,f.x,n.x,c[0]),(e.y,f.y,n.y,c[1]),(e.z,f.z,n.z,c[2]),(0,0,0,1)))
    curve.materials.append(gold); link_parent(o,owners[owner]); o['surface_attachment']=name+'_anchor'
    a=empty(name+'_anchor',c); link_parent(a,owners[owner]); return o

def camera(name,pos,target,scale):
    d=bpy.data.cameras.new(name); o=bpy.data.objects.new(name,d); bpy.context.scene.collection.objects.link(o)
    o.location=pos; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler(); d.type='ORTHO'; d.ortho_scale=scale
    return o

if 'render' not in MODE and 'polish' not in MODE:
    bpy.ops.wm.open_mainfile(filepath=str(BASE)); sc=bpy.context.scene
    # Concrete Normal integration issue: the accepted hidden abdomen protrudes
    # below the fleece. Tuck only its underside; head and support are unaffected.
    for v in bpy.data.objects['CENTRAL_CHASSIS'].data.vertices:
        if v.co.x>.46 and v.co.z<.23:
            w=math.exp(-((v.co.x-.73)/.28)**4)*max(0,min(1,(.23-v.co.z)/.14))
            v.co.z+=.065*w
    # Normal's explicit visible hoof authority supersedes Skin distal styling.
    # Preserve the existing three-toe topology and planted support centers.
    for ob in sc.objects:
        if ob.name.startswith('HOOF_'):
            cy=sum(v.co.y for v in ob.data.vertices)/len(ob.data.vertices)
            cx=.38 if 'FORE' in ob.name else .91
            for v in ob.data.vertices:
                v.co.x=cx+(v.co.x-cx)*1.45
                v.co.y=cy+(v.co.y-cy)*1.83
                v.co.z*=1.47
    owners={'head':empty('FLEECE_HEAD_OWNER',(.38,0,.49)), 'torso':empty('FLEECE_TORSO_OWNER',(.65,0,.38)), 'tail':bpy.data.objects['TAIL_PIVOT']}
    clouds=[]
    white=material('Fleece pearl warm cloud',(1,.93,.88),(.76,.75,.96))
    lilac=material('Fleece soft periwinkle',(.46,.55,1),(.34,.40,.82))
    blue=material('Fleece moon recess blue',(.16,.28,.92),(.15,.23,.70))
    gold=material('Motif warm gold',(1,.69,.13),(1,.42,.035)); gold.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.32
    # Crown rises behind the brow, reconciling Front stack and Side apex.
    specs=[
      ('Crown_apex',(.56,0,.855),(.235,.145,.20),(0,0,1),'crown',white),
      ('Crown_front',(.31,0,.805),(.22,.14,.15),(-1,0,.3),'crown',white),
      ('Crown_depth_bridge',(.235,0,.747),(.255,.145,.12),(0,0,1),'crown',white),
      ('Brow_center',(.075,0,.645),(.16,.12,.12),(-1,0,.2),'face_frame',white),
      ('Brow_L',(.10,.19,.67),(.14,.14,.12),(-1,.2,.1),'face_frame',white),
      ('Brow_R',(.11,-.19,.685),(.15,.15,.12),(-1,-.2,.1),'face_frame',white),
      ('Chest_center',(.27,0,.185),(.17,.10,.13),(-1,0,-.1),'chest_front',white),
      ('Back_dorsal',(.80,0,.76),(.31,.18,.24),(0,0,1),'central_back',lilac),
      ('Rump_center',(1.07,0,.40),(.30,.25,.19),(1,0,.2),'rump',white),
      ('Belly_center',(.65,0,.22),(.26,.26,.085),(0,0,-1),'lower_belly',lilac),
    ]
    for s in [-1,1]:
        label='L' if s==1 else 'R'
        specs += [
          ('Crown_bank_'+label,(.52,s*.27,.80),(.21,.15,.19),(-.25,s,.4),'crown',lilac),
          ('Upper_flank_'+label,(.70,s*.36,.65),(.24,.22,.17),(.1,s,.3),'central_back',blue if s==1 else lilac),
          ('Temple_bank_'+label,(.40,s*.36,.735),(.17,.16,.17),(-.5,s,.2),'face_frame',blue if s==1 else lilac),
          ('Outer_brow_'+label,(.23,s*.32,.60),(.11,.11,.12),(-1,s*.3,.1),'face_frame',white),
          ('Cheek_upper_'+label,(.29,s*.29,.44),(.063,.075,.07),(-1,s*.2,0),'face_frame',white),
          ('Cheek_lower_'+label,(.29,s*.29,.315),(.08,.085,.08),(-1,s*.2,0),'face_frame',white),
          ('Chest_wing_'+label,(.33,s*.20,.205),(.16,.11,.15),(-1,s*.2,0),'chest_front',white),
          ('Lower_flank_'+label,(.55,s*.37,.24),(.20,.12,.16),(0,s,-.1),'lower_belly',lilac),
          ('Belly_wrap_'+label,(.66,s*.26,.19),(.19,.063,.105),(0,s,-.3),'lower_belly',lilac),
          ('Side_major_'+label,(.88,s*.38,.35),(.23,.21,.18),(.15,s,.1),'rump',white),
          ('Side_bridge_'+label,(.68,s*.43,.46),(.16,.15,.12),(0,s,0),'central_back',lilac),
          ('Rump_upper_'+label,(.99,s*.25,.61),(.19,.16,.17),(.6,s,.2),'rump',lilac),
          ('Rump_lower_'+label,(1.0,s*.23,.20),(.17,.10,.14),(.4,s,-.1),'rump',white),
        ]
    for i,(name,c,r,n,reg,mat) in enumerate(specs):cloud('FL_'+name,c,r,n,reg,mat,103+i)
    cloud('FL_Crown_inner_transition',(.48,0,.675),(.305,.30,.14),(0,0,1),'crown',lilac,211,True)
    cloud('FL_Torso_inner_transition',(.78,0,.42),(.30,.29,.23),(0,0,1),'central_back',lilac,212,True)
    cloud('TAIL_FLEECE_SHELL',(1.232,0,.372),(.047,.045,.056),(1,0,.25),'tail',white,77)
    # Quiet transition volume around the tail core is tail-owned, never rump-fused.
    cloud('TAIL_FLEECE_ATTACHMENT',(1.15,0,.356),(.043,.040,.086),(1,0,.2),'tail',lilac,78,True)
    motif('STAR_crown',(.155,0,.852),.055,(-1,0,.2),owner='head')
    motif('STAR_brow',(-.035,-.045,.704),.052,(-1,0,.1),owner='head')
    motif('STAR_chest',(-.01,0,.177),.045,(-1,0,0))
    motif('STAR_lower_left',(.185,.385,.225),.045,(-.8,.6,.1))
    motif('STAR_rump',(.90,-.548,.37),.061,(0,-1,.1))
    motif('STAR_rump_L',(.90,.548,.37),.061,(0,1,.1))
    motif('MOON',(.42,.29,.735),.125,(-.70,.71,.12),True,owner='head')
    for name,c in [('fleece_front',(-.002,0,.225)),('pocket_front_L',(.09,.20,.265)),('pocket_front_R',(.09,-.20,.265)),('gift_reveal',(.14,0,.245))]:
        from mathutils.bvhtree import BVHTree
        hits=[]; origin=Vector((-1,c[1],c[2])); deps=bpy.context.evaluated_depsgraph_get()
        for ob in clouds:
            if ob.get('semantic_region')!='chest_front':continue
            ev=ob.evaluated_get(deps); me=ev.to_mesh()
            tree=BVHTree.FromPolygons([ob.matrix_world@v.co for v in me.vertices],[p.vertices[:] for p in me.polygons])
            h,_,_,dist=tree.ray_cast(origin,Vector((1,0,0)))
            if h is not None:hits.append((dist,h))
            ev.to_mesh_clear()
        if hits:c=min(hits,key=lambda p:p[0])[1]+Vector((-.004,0,0))
        o=empty(name,c); link_parent(o,owners['torso']); o['attachment_contract']='Body-owned stable frame; do not attach to residual deformation'
    # Stable material presentation and orthographic same-asset review cameras.
    for o in list(sc.objects):
        if o.type in ['CAMERA','LIGHT']:bpy.data.objects.remove(o,do_unlink=True)
    camera('REVIEW_front',(-4,0,.50),(.5,0,.50),1.40)
    camera('REVIEW_side',(.63,4,.50),(.63,0,.50),1.50)
    camera('REVIEW_opposite_side',(.63,-4,.50),(.63,0,.50),1.50)
    camera('REVIEW_3q',(-2.8,-3,.1+1.5),(.57,0,.46),1.50)
    camera('REVIEW_rear',(4,-1.5,1.2),(.6,0,.47),1.50)
    camera('REVIEW_top',(.6,0,4),(.6,0,0),1.50)
    for name,pos,power,size in [('Key',(-2,-3,4),350,3),('Fill',(-2,3,2),250,3),('Rim',(3,1,3),300,2.5)]:
        d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.shape='DISK'; d.size=size
        o=bpy.data.objects.new(name,d); sc.collection.objects.link(o); o.location=pos; o.rotation_euler=(Vector((.5,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
    sc.world.color=(.35,.35,.35)
    sc.render.engine='CYCLES'; sc.cycles.samples=32; sc.cycles.use_denoising=True
    sc.render.resolution_x=800; sc.render.resolution_y=800; sc.render.resolution_percentage=100
    sc.render.film_transparent=True; sc.view_settings.view_transform='AgX'; sc.view_settings.exposure=.7
    sc.camera=bpy.data.objects['REVIEW_front']; sc['phase1_state']='CANDIDATE_INTERNAL_REVIEW'
else:
    bpy.ops.wm.open_mainfile(filepath=str(ASSET)); sc=bpy.context.scene
if 'render' not in MODE:
    sc.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.45,.45,.50,1)
    sc.view_settings.view_transform='Standard'; sc.view_settings.exposure=-1.4
    sc.render.use_compositing=False; sc.render.use_sequencer=False
    bpy.data.objects['Fill'].data.energy=170
    bpy.data.objects['Key'].data.energy=420
    sc['phase1_state']='NORMAL_FLEECE_AWAITING_HUMAN_PHASE1_REVIEW'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET),compress=True)
if 'quick' in MODE:
    sc.render.resolution_percentage=60; sc.cycles.samples=12
views=MODE[MODE.index('views')+1:] if 'views' in MODE else ['front','side']
for view in views:
    sc.camera=bpy.data.objects['REVIEW_'+view]; sc.render.filepath=str(OUT/(view+'.png')); bpy.ops.render.render(write_still=True)
