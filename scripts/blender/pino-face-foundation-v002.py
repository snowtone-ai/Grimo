"""Bounded Pino face diagnostic. Never writes rig-v001 or source assets."""
import bpy, json, sys, math, hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / 'assets/grimo/production/pino/candidate-c'
D = A / 'face-foundation-v002'
OUT = ROOT / 'docs/production/pino/evidence/face-foundation-v002'
BASE = A / 'rig-v001/pino-c-base-rig-v001.blend'
D.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

def dump(n, x):
    (OUT/n).write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def world(o): return np.array([o.matrix_world @ v.co for v in o.data.vertices])
def evaluated(o):
    bpy.context.view_layer.update()
    e=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return np.array([e.matrix_world @ v.co for v in e.data.vertices])

def load():
    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001']
    rig=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001']
    return o,rig,bpy.context.scene

def view(sc, name, target=(0,-.16,.64), scale=.55):
    dr=Vector({'front':(0,-1,0),'side':(1,0,0),'3q':(1,-1,0)}[name]).normalized()
    c=sc.camera;c.data.type='ORTHO'; c.location=Vector(target)+dr*3
    c.rotation_euler=(-dr).to_track_quat('-Z','Y').to_euler()
    c.data.ortho_scale=scale

def display(sc, size=480):
    sc.render.engine='BLENDER_WORKBENCH'
    sc.render.resolution_x=size;sc.render.resolution_y=size
    sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'
    sh=sc.display.shading
    sh.light='STUDIO';sh.color_type='MATERIAL'
    sh.show_shadows=True;sh.show_cavity=False
    sh.background_type='WORLD';sc.world.color=(.12,.14,.18)
    sc.view_settings.view_transform='Standard'

def render(sc, path):
    sc.render.filepath=str(path);bpy.ops.render.render(write_still=True)

def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)

def mouth_targets(V, labels):
    x,y,z=V.T
    wx=1-smooth(.047,.087,abs(x))
    wy=1-smooth(-.369,-.330,y)
    wz=smooth(.515,.551,z)*(1-smooth(.615,.638,z))
    w=wx*wy*wz*(labels==0)
    # Pass 2: the layered source bowl cannot tolerate a large vertical squash.
    # Close its recess toward a smooth local muzzle envelope, with only a tiny
    # lower-rim lift. This is a bounded prototype, not proven lip contact.
    envelope=-.402-.018*smooth(.540,.625,z)+1.8*x*x
    closed=V.copy();closed[:,2]+=.003*w*(1-smooth(.59,.62,z))
    closed[:,1]+=(envelope+.045*(y-envelope)-y)*w
    # A modest lower-rim opening, kept local to the existing mouth.
    lower=(1-smooth(.565,.617,z))*smooth(.485,.546,z)
    large=V.copy();large[:,2]-=.012*wx*wy*lower*(labels==0)
    large[:,1]-=.0015*wx*wy*lower*(labels==0)
    return closed,large,w

def add_lids(o,rig,V,labels):
    body=BVHTree.FromPolygons([Vector(p) for p in V],
        [list(p.vertices) for p in o.data.polygons if labels[p.vertices[0]]==0],all_triangles=True)
    lids=[]
    for side,comp in [('L',9),('R',8)]:
        p=V[labels==comp];c=(p.min(0)+p.max(0))/2
        ax=np.ptp(p[:,0])/2;az=np.ptp(p[:,2])/2
        eye=BVHTree.FromPolygons([Vector(pt) for pt in V],
            [list(f.vertices) for f in o.data.polygons if labels[f.vertices[0]]==comp],all_triangles=True)
        variants=[[],[],[]];faces=[];NX=32;NY=12
        for upper in [True,False]:
            offset=len(variants[0])
            for j in range(NY+1):
                t=j/NY
                for i in range(NX+1):
                    u=-.998+1.996*i/NX;x=c[0]+ax*1.025*u
                    r=math.sqrt(max(.0001,1-u*u));top=c[2]+az*1.035*r;bottom=c[2]-az*1.035*r
                    seam=c[2]+.005+.008*(1-u*u)
                    for state,close in enumerate([0,.5,1]):
                        if upper:
                            edge=top;end=top*(1-close)+(seam+.0006)*close
                        else:
                            edge=bottom;end=bottom*(1-close)+(seam-.0006)*close
                        z=edge*(1-t)+end*t
                        hit=eye.ray_cast(Vector((x,-.8,z)),Vector((0,1,0)))[0]
                        bh=body.ray_cast(Vector((x,-.8,z)),Vector((0,1,0)))[0]
                        # Closed lid rides over the unchanged convex eye. Its
                        # outer boundary recedes into head skin; Basis is buried.
                        ey=hit.y if hit else (bh.y if bh else c[1])
                        by=bh.y if bh else ey+.006
                        cover=ey-.0015
                        boundary=(1-smooth(0,.12,t))*1.0+smooth(.93,.999,abs(u))
                        yy=cover*(1-min(1,boundary))+(by+.001)*min(1,boundary)
                        if state==0:yy=by+.008
                        variants[state].append((x,yy,z))
            for j in range(NY):
                for i in range(NX):
                    a=offset+j*(NX+1)+i;b=a+1;cidx=b+NX+1;d=a+NX+1
                    faces.append((a,b,cidx,d) if upper else (d,cidx,b,a))
        me=bpy.data.meshes.new('Pino rolling upper and lower lids '+side)
        me.from_pydata(variants[0],[],faces);me.update()
        ob=bpy.data.objects.new('PinoSoftLids_'+side,me);bpy.context.scene.collection.objects.link(ob)
        me.materials.append(o.data.materials[0])
        for f in me.polygons:f.use_smooth=True
        ob.shape_key_add(name='Basis')
        for name,points in zip(['LidHalf','LidClosed'],variants[1:]):
            key=ob.shape_key_add(name=name)
            for dst,pt in zip(key.data,points):dst.co=pt
        g=ob.vertex_groups.new(name='mixamorig:Head');g.add(list(range(len(me.vertices))),1,'REPLACE')
        ob.parent=rig;mod=ob.modifiers.new('Head skin','ARMATURE');mod.object=rig
        ob['control_contract']='b in [0,1]: LidHalf=min(2*b,2-2*b), LidClosed=max(0,2*b-1). Eye cap unchanged.'
        lids.append(ob)
    return lids

def state(o,lids,closed=0,large=0,left=0,right=0):
    for k in list(o.data.shape_keys.key_blocks)[1:]:k.value=0
    o.data.shape_keys.key_blocks['PinoMouthClosed'].value=closed
    o.data.shape_keys.key_blocks['PinoMouthLarge'].value=large
    for ob,b in zip(lids,[left,right]):
        ob.data.shape_keys.key_blocks['LidHalf'].value=min(2*b,2-2*b)
        ob.data.shape_keys.key_blocks['LidClosed'].value=max(0,2*b-1)
    bpy.context.view_layer.update()

def build():
    o,rig,sc=load();V=world(o)
    labels=np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
    closed,large,w=mouth_targets(V,labels)
    for name,pts in [('PinoMouthClosed',closed),('PinoMouthLarge',large)]:
        key=o.shape_key_add(name=name)
        for v,p in zip(key.data,pts):v.co=p
    lids=add_lids(o,rig,V,labels)
    o['Human_Face_Gate']='PENDING';rig['Human_Face_Gate']='PENDING'
    o['Game_Neutral']='UNDECIDED by Human; existing open-smile Basis retained'
    sc['face_foundation_pass']=2
    state(o,lids);display(sc)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(D/'pino-face-foundation-v002.blend'),compress=True)
    for label,args in [('basis',(0,0,0,0)),('closed',(1,0,0,0)),('half',(.5,0,.5,.5)),
                       ('lids',(0,0,1,1)),('wink-large',(0,1,1,0))]:
        state(o,lids,*args)
        for name in ['front','side','3q']:
            view(sc,name);render(sc,OUT/('_pass2-'+label+'-'+name+'.png'))
    dump('pass2.json',{'mouth_affected_vertices':int(np.sum(w>0)),
        'mouth_max_displacement':float(np.linalg.norm(closed-V,axis=1).max()),
        'source_eye_vertices_unchanged':True,'new_lid_vertices':[len(l.data.vertices) for l in lids]})

def owner_colors(o):
    labels=np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
    m=bpy.data.materials.new('DIAGNOSTIC eye ownership (no texture)');m.diffuse_color=(.025,.10,.20,1)
    o.data.materials.append(m);idx=len(o.data.materials)-1
    for p in o.data.polygons:
        if labels[p.vertices[0]] in [8,9]:p.material_index=idx

def colored():
    bpy.ops.wm.open_mainfile(filepath=str(D/'pino-face-foundation-v002.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];sc=bpy.context.scene
    lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']]
    owner_colors(o);display(sc)
    for label,args in [('open',(0,0,0,0)),('half',(0,0,.5,.5)),('closed',(0,0,1,1)),('wink',(0,0,1,0))]:
        state(o,lids,*args)
        for name in ['front','side','3q']:
            view(sc,name);render(sc,OUT/('_owners-'+label+'-'+name+'.png'))

def geometry_snapshot(o,rig):
    def digest(values,dtype=np.float64):
        return hashlib.sha256(np.array(values,dtype=dtype).tobytes()).hexdigest()
    return {'basis':digest([v.co[:] for v in o.data.vertices]),
        'triangles':digest([p.vertices[:] for p in o.data.polygons],np.int64),
        'corner_normals':digest([n.vector[:] for n in o.data.corner_normals]),
        'skin':digest([(v.index,g.group,g.weight) for v in o.data.vertices for g in v.groups]),
        'groups':[g.name for g in o.vertex_groups],
        'legacy_keys':{k.name:digest([v.co[:] for v in k.data]) for k in list(o.data.shape_keys.key_blocks)[:3]},
        'bone_rest':{b.name:{'parent':b.parent.name if b.parent else None,'matrix':[list(r) for r in b.matrix_local]} for b in rig.data.bones},
        'material_base_color':[list(m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value) for m in o.data.materials],
        'uv':len(o.data.uv_layers)}

POSES=[(1,'Basis',(0,0,0,0)),(7,'Closed',(1,0,0,0)),
    (13,'Small',(.68,0,0,0)),(19,'Medium / original Basis',(0,0,0,0)),
    (25,'Large',(0,1,0,0)),(31,'Closed return',(1,0,0,0)),(37,'Basis return',(0,0,0,0)),
    (43,'Eyes open',(0,0,0,0)),(49,'Left half',(0,0,.5,0)),(55,'Left wink',(0,0,1,0)),
    (61,'Open return',(0,0,0,0)),(67,'Right half',(0,0,0,.5)),(73,'Right wink',(0,0,0,1)),
    (79,'Open return',(0,0,0,0)),(85,'Both half',(0,0,.5,.5)),(91,'Both closed',(0,0,1,1)),
    (97,'Open return',(0,0,0,0)),(103,'Combined small / half',(.68,0,.5,.5)),
    (109,'Combined large / closed',(0,1,1,1)),(115,'Combined recover',(.34,0,.5,.5)),
    (121,'Basis return',(0,0,0,0))]

def channel_key(ob,frame):
    for k in list(ob.data.shape_keys.key_blocks)[1:]:
        k.keyframe_insert(data_path='value',frame=frame,group='Face diagnostic only')

def all_curves(action):
    for layer in action.layers:
        for strip in layer.strips:
            if strip.type=='KEYFRAME':
                for bag in strip.channelbags:
                    yield from bag.fcurves

def proof():
    bpy.context.preferences.filepaths.save_version=0
    source,source_rig,_=load();baseline=geometry_snapshot(source,source_rig)
    bpy.ops.wm.open_mainfile(filepath=str(D/'pino-face-foundation-v002.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];rig=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];sc=bpy.context.scene
    lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']]
    current=geometry_snapshot(o,rig)
    locked={k:current[k]==baseline[k] for k in baseline}
    assert all(locked.values()),locked
    o['Face_Status']='HOLD: two prototype passes; lip contact and lid fringe unresolved'
    rig['Face_Status']=o['Face_Status']
    sc['Human_Face_Gate']='PENDING';sc['Production_Status']='HOLD'
    sc['Final_Game_Neutral']='Human decision pending; no change to open-smile Basis'
    state(o,lids);display(sc,360)
    bpy.ops.wm.save_as_mainfile(filepath=str(D/'pino-face-foundation-v002.blend'),compress=True)
    # Build curves only after all state values have been collected. No source or
    # body animation is authored; old blink keys stay zero in this proof.
    for frame,label,args in POSES:
        state(o,lids,*args)
        for ob in [o]+lids:channel_key(ob,frame)
        sc.timeline_markers.new(label,frame=frame)
    for ob in [o]+lids:
        for fc in all_curves(ob.data.shape_keys.animation_data.action):
            for kp in fc.keyframe_points:kp.interpolation='LINEAR'
    sc.frame_start=1;sc.frame_end=121;sc.render.fps=24;sc.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(D/'pino-face-foundation-v002-proof.blend'),compress=True)
    # A single full asset with diagnostic tracks, no texture images. Importers
    # may stash its morph tracks; activate them together for this proof.
    bpy.ops.object.select_all(action='DESELECT')
    for ob in [o,rig]+lids:ob.select_set(True)
    options={'filepath':str(D/'pino-face-foundation-v002-diagnostic.glb'),'export_format':'GLB',
        'use_selection':True,'export_skins':True,'export_morph':True,'export_morph_normal':True,
        'export_animations':True,'export_frame_range':True,'export_frame_step':1,
        'export_animation_mode':'SCENE','export_force_sampling':True,'export_all_influences':True,
        'export_extras':True,'export_apply':False,'export_yup':True}
    supported={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    options={k:v for k,v in options.items() if k in supported}
    bpy.ops.export_scene.gltf(**options)
    checks=[]
    labels=np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
    V=world(o)
    mouth_roi=(labels==0)&(abs(V[:,0])<.09)&(V[:,1]<-.33)&(V[:,2]>.48)&(V[:,2]<.65)
    body=~mouth_roi
    for frame in range(1,122):
        sc.frame_set(frame);p=evaluated(o)
        checks.append({'frame':frame,'finite':bool(np.isfinite(p).all()),
            'frozen_body_tail_max_delta':float(np.linalg.norm(p[body]-V[body],axis=1).max()),
            'eye_cap_max_delta':float(np.linalg.norm(p[np.isin(labels,[8,9])]-V[np.isin(labels,[8,9])],axis=1).max())})
    # Independent controls sampled from saved animated state.
    independence=[]
    for f,opposite in [(49,1),(55,1),(67,0),(73,0)]:
        sc.frame_set(f);ob=lids[opposite]
        independence.append({'frame':f,'opposite_lid_max_delta':float(np.linalg.norm(evaluated(ob)-world(ob),axis=1).max())})
    dump('saved-checks.json',{'lock_checks':locked,'snapshots':{'source':baseline,'candidate':current},
        'frame_checks':checks,'independence':independence,'export_options':options,
        'glb_bytes':(D/'pino-face-foundation-v002-diagnostic.glb').stat().st_size})
    # Render serialized poses. Temporary solid eye ownership tint is never saved
    # to authoring/proof/GLB; geometry and evaluated states are unchanged.
    bpy.ops.wm.open_mainfile(filepath=str(D/'pino-face-foundation-v002-proof.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];sc=bpy.context.scene
    owner_colors(o);display(sc,300);frames=OUT/'_frames';frames.mkdir(exist_ok=True)
    for frame in range(1,122,3):
        sc.frame_set(frame)
        for name in ['front','side','3q']:
            view(sc,name);render(sc,frames/f'{frame:03d}-{name}.png')
    dump('timeline.json',{'fps':24,'frame_range':[1,121],'states':POSES,
        'gif_samples':list(range(1,122,3)),'note':'Temporary solid eye ownership tint only; no Texture. Frozen tail/paws/rest.'})

def reimport():
    # Reopen the uncolored proof and compare world-space evaluated surfaces to
    # the GLB reimport, including a small temporary Head pose for skin checking.
    from mathutils.kdtree import KDTree
    from mathutils import Quaternion
    bpy.ops.wm.open_mainfile(filepath=str(D/'pino-face-foundation-v002-proof.blend'))
    srcobs=[bpy.data.objects[n] for n in ['PINO_C_BASE_RIG_V001','PinoSoftLids_L','PinoSoftLids_R']]
    srcrig=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];sc=bpy.context.scene
    names=[ob.name for ob in srcobs];samples={};base={};features={};head_owned={}
    sc.frame_set(1)
    for ob in srcobs:
        base[ob.name]=world(ob)
        features[ob.name]=(np.array([ob.matrix_world@v.co for v in ob.data.shape_keys.key_blocks['LidClosed'].data])
            if ob.name.startswith('PinoSoftLids') else base[ob.name])
        head_owned[ob.name]=np.array([len(v.groups)==1 and ob.vertex_groups[v.groups[0].group].name=='mixamorig:Head' and v.groups[0].weight>.99999 for v in ob.data.vertices])
    for f in [1,10,25,31,49,55,73,91,103,109,121]:
        sc.frame_set(f);samples[f]={ob.name:evaluated(ob) for ob in srcobs}
    p=srcrig.pose.bones['mixamorig:Head'];p.rotation_mode='QUATERNION'
    q=(srcrig.matrix_world@p.bone.matrix_local).to_quaternion()
    p.rotation_quaternion=q.inverted()@Quaternion((0,0,1),math.radians(4))@q
    samples['head4']={ob.name:evaluated(ob) for ob in srcobs}
    p.rotation_quaternion=Quaternion()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(D/'pino-face-foundation-v002-diagnostic.glb'))
    sc=bpy.context.scene;obs=[o for o in sc.objects if o.type=='MESH'];rig=next(o for o in sc.objects if o.type=='ARMATURE')
    report={'meshes':{},'frames':[],'bone_count':len(rig.data.bones),'imported_names':[o.name for o in obs]}
    report['animation_binding']={}
    for owner in [rig]+[o.data.shape_keys for o in obs if o.data.shape_keys]:
        ad=owner.animation_data
        if not ad:continue
        report['animation_binding'][owner.name]={'active':ad.action.name if ad.action else None,
            'nla':[{'name':t.name,'muted':t.mute,'strips':[{'action':s.action.name,'slot':s.action_slot.identifier if s.action_slot else None} for s in t.strips]} for t in ad.nla_tracks]}
        if ad.action is None:
            strips=[s for t in ad.nla_tracks for s in t.strips]
            if strips:
                ad.action=strips[0].action;ad.action_slot=strips[0].action_slot
                for t in ad.nla_tracks:t.mute=True
    first=min(k.co.x for action in bpy.data.actions for fc in all_curves(action) for k in fc.keyframe_points)
    report['imported_first_frame']=first
    mapping={}
    for name in names:
        if name.startswith('PINO_'):
            ob=next(o for o in obs if 'PinoMouthClosed' in o.data.shape_keys.key_blocks)
        else:
            sign=1 if name.endswith('_L') else -1
            ob=next(o for o in obs if 'LidClosed' in o.data.shape_keys.key_blocks and np.mean(world(o)[:,0])*sign>0)
        v=world(ob);src=base[name]
        feature=(np.array([ob.matrix_world@v.co for v in ob.data.shape_keys.key_blocks['LidClosed'].data])
            if name.startswith('PinoSoftLids') else v)
        kd=KDTree(len(src))
        for i,q in enumerate(features[name]):kd.insert(Vector(q),i)
        kd.balance();pairs=[kd.find(Vector(q)) for q in feature]
        mapping[name]=(ob,np.array([i for q,i,d in pairs]))
        report['meshes'][name]={'vertices':len(v),'source_vertices':len(src),
            'base_nearest_max_delta':float(np.linalg.norm(v-base[name][mapping[name][1]],axis=1).max()),
            'correspondence_feature_max_delta':max(d for q,i,d in pairs),
            'morphs':[k.name for k in ob.data.shape_keys.key_blocks],
            'armature_modifier':any(m.type=='ARMATURE' and m.object==rig for m in ob.modifiers),
            'unassigned':sum(not v.groups for v in ob.data.vertices)}
    for f,bank in samples.items():
        sc.frame_set(round((121 if f=='head4' else f)-1+first))
        if f=='head4':
            p=rig.pose.bones['mixamorig:Head'];p.rotation_mode='QUATERNION'
            q=(rig.matrix_world@p.bone.matrix_local).to_quaternion()
            p.rotation_quaternion=q.inverted()@Quaternion((0,0,1),math.radians(4))@q
        errors={};head_errors={}
        for name,(ob,idx) in mapping.items():
            dist=np.linalg.norm(evaluated(ob)-bank[name][idx],axis=1)
            errors[name]=float(dist.max());head_errors[name]=float(dist[head_owned[name][idx]].max())
        report['frames'].append({'frame':f,'max_world_delta':errors,'head_owned_max_delta':head_errors})
    dump('glb-reimport.json',report)
    # One small persisted reimport snapshot at Basis; not a new production asset.
    rig.pose.bones['mixamorig:Head'].rotation_quaternion=Quaternion();sc.frame_set(round(first))
    cd=bpy.data.cameras.new('Reimport review');c=bpy.data.objects.new(cd.name,cd);sc.collection.objects.link(c);sc.camera=c
    sc.world=bpy.data.worlds.new('Reimport world');display(sc,480)
    for name in ['front','side','3q']:
        view(sc,name);render(sc,OUT/('_reimport-basis-'+name+'.png'))
    print('PINO_FACE_REIMPORT',json.dumps(report))

def source_compare():
    bpy.ops.wm.open_mainfile(filepath=str(D/'pino-face-foundation-v002.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];sc=bpy.context.scene
    lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']]
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(A/'source/cute blue creature 3d model.glb'))
    ref=next(ob for ob in set(bpy.data.objects)-before if ob.type=='MESH')
    checks={'basis_positions_exact':np.array_equal(world(o),world(ref)),
        'triangles_exact':[p.vertices[:] for p in o.data.polygons]==[p.vertices[:] for p in ref.data.polygons],
        'corner_normals_exact':np.array_equal(np.array([n.vector[:] for n in o.data.corner_normals]),np.array([n.vector[:] for n in ref.data.corner_normals])),
        'original_uv_layers':len(ref.data.uv_layers),'original_has_morph':bool(ref.data.shape_keys),
        'original_images':len(bpy.data.images)}
    dump('original-glb-checks.json',checks);state(o,lids);display(sc,480)
    for label in ['original','candidate']:
        ref.hide_render=label!='original';o.hide_render=label=='original'
        for lid in lids:lid.hide_render=label=='original'
        for name in ['front','side','3q']:
            view(sc,name);render(sc,OUT/('_'+label+'-basis-'+name+'.png'))
    print('PINO_FACE_SOURCE',json.dumps(checks))

def check_frozen():
    bpy.ops.wm.open_mainfile(filepath=str(D/'pino-face-foundation-v002-proof.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];sc=bpy.context.scene;V=world(o)
    labels=np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
    mouth_roi=(labels==0)&(abs(V[:,0])<.09)&(V[:,1]<-.33)&(V[:,2]>.48)&(V[:,2]<.65)
    masks={'outside_mouth':~mouth_roi,'tail':np.isin(labels,[2,5]),
        'paws_and_legs':(labels==0)&(V[:,2]<.45), 'eye_caps':np.isin(labels,[8,9])}
    maxima={k:0 for k in masks};returns={};finite=True
    for f in range(1,122):
        sc.frame_set(f);v=evaluated(o);dist=np.linalg.norm(v-V,axis=1);finite=finite and bool(np.isfinite(v).all())
        for k,m in masks.items():maxima[k]=max(maxima[k],float(dist[m].max()))
        if f in [1,37,43,61,79,97,121]:returns[str(f)]=float(dist.max())
    saved=json.loads((OUT/'saved-checks.json').read_text(encoding='utf-8'))
    saved['frame_summary']={'frames':121,'all_finite':finite,'frozen_regions_max_delta':maxima,
        'basis_returns_max_delta':returns,'mouth_roi':'original component 0; abs(X)<.09, Y<-.33, .48<Z<.65',
        'metric_correction':'Earlier Z<.49 body mask included the lower chin; replaced by all vertices outside the explicit face ROI.'}
    dump('saved-checks.json',saved)

def diagnose():
    bpy.ops.wm.open_mainfile(filepath=str(D/'pino-face-foundation-v002.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];sc=bpy.context.scene
    lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']]
    display(sc);state(o,lids,1,0,1,1)
    e=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me=bpy.data.meshes.new_from_object(e)
    tmp=bpy.data.objects.new('DIAGNOSTIC recalculated normals',me);sc.collection.objects.link(tmp)
    if me.has_custom_normals:me.normals_split_custom_set([(0,0,0)]*len(me.loops))
    o.hide_render=True
    for name in ['front','3q']:
        view(sc,name);render(sc,OUT/('_diagnostic-recalc-'+name+'.png'))
    np.savez_compressed(OUT/'_closed.npz',vertices=world(tmp),triangles=np.array([p.vertices[:] for p in me.polygons]))

def audit():
    o,rig,sc=load();V=world(o)
    labels=np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
    comps=[]
    for i in np.unique(labels):
        pts=V[labels==i]
        comps.append({'id':int(i),'vertices':len(pts),'min':pts.min(0).tolist(),'max':pts.max(0).tolist()})
    dump('source-audit.json',{'base_sha256':sha(BASE),'original_glb_sha256':sha(A/'source/cute blue creature 3d model.glb'),
         'components':comps,'uv_layers':len(o.data.uv_layers),'images':len(bpy.data.images),
         'keys':[k.name for k in o.data.shape_keys.key_blocks],
         'materials':[{'name':m.name,'diffuse':list(m.diffuse_color)} for m in o.data.materials],
         'rig_bones':len(rig.data.bones),'shape':list(V.shape),'matrix':[list(r) for r in o.matrix_world]})
    np.savez_compressed(OUT/'_audit.npz',vertices=V,components=labels,triangles=np.array([p.vertices[:] for p in o.data.polygons]))
    display(sc)
    for name in ['front','side','3q']:
        view(sc,name);render(sc,OUT/('_source-'+name+'.png'))
    # Destructive cutaway applies only to a disposable in-memory mesh copy.
    import bmesh
    cut=o.copy();cut.data=o.data.copy();sc.collection.objects.link(cut)
    cut.shape_key_clear();cut.modifiers.clear();o.hide_render=True
    bm=bmesh.new();bm.from_mesh(cut.data)
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if (cut.matrix_world@v.co).x > .001],context='VERTS')
    bm.to_mesh(cut.data);bm.free()
    view(sc,'side');render(sc,OUT/'_source-cutaway.png')
    print('PINO_FACE_AUDIT',json.dumps(comps))

if __name__=='__main__':
    if '--check-frozen' in sys.argv:check_frozen()
    elif '--source-compare' in sys.argv:source_compare()
    elif '--reimport' in sys.argv:reimport()
    elif '--proof' in sys.argv:proof()
    elif '--owners' in sys.argv:colored()
    elif '--diagnose' in sys.argv:diagnose()
    elif '--build' in sys.argv:build()
    else:audit()
