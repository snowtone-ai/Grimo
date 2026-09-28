"""Deterministic continuous-section Carol fleece. Blender 5.2, no add-ons.

build --attempt 1|2|3 (macro clay); render; audit; mark-failed.
The builder starts from accepted Skin and retains selected v002 eyes/hooves/charms.
No previous fleece mesh, historical geometry, camera-facing cards or remeshing.
"""
import bpy, bmesh, numpy as np, math, json, sys, hashlib, os, uuid
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v003'
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v003.blend'
BASE=ASSET.with_name('carol-skin-final-v002.blend')
PREVIOUS=ASSET.with_name('carol-normal-fleece-v002.blend')
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['build']
COMMAND=ARGS[0]
def arg(name,default):return ARGS[ARGS.index(name)+1] if name in ARGS else default
ATTEMPT=int(arg('--attempt','1'));PASS=int(arg('--pass-number','1'))
CONTRACT=json.loads((OUT/'authority-contract.json').read_text())
SKIN_SHA='321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def parent(ob,p):
    bpy.context.view_layer.update();m=ob.matrix_world.copy();ob.parent=p;ob.matrix_world=m
def empty(name,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(o);o.location=loc;return o
def mesh(name,verts,faces,mat=None):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o)
    for p in me.polygons:p.use_smooth=True
    if mat:me.materials.append(mat)
    return o
def material(name,col):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*col,1)
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*col,1)
    bs.inputs['Roughness'].default_value=.91;bs.inputs['Specular IOR Level'].default_value=.16
    return m
def save():
    staging=ASSET.with_name(ASSET.stem+'.'+uuid.uuid4().hex+'.blend')
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(staging),compress=True,relative_remap=False)
    bpy.ops.wm.read_factory_settings(use_empty=True);os.replace(staging,ASSET)
    bpy.ops.wm.open_mainfile(filepath=str(ASSET))
def camera(name,pos,target,scale):
    d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale
    o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);o.location=pos
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
def presentation():
    sc=bpy.context.scene
    for o in list(sc.objects):
        if o.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(o,do_unlink=True)
    for name,pos,target,scale in [
        ('front',(-4,0,.51),(.5,0,.51),1.30),('side',(.63,4,.51),(.63,0,.51),1.42),
        ('opposite_side',(.63,-4,.51),(.63,0,.51),1.42),('3q',(-2.8,-3,1.6),(.57,0,.47),1.5),
        ('rear',(4,0,.51),(.6,0,.51),1.4),('top',(.6,0,4),(.6,0,0),1.5)]:camera('REVIEW_'+name,pos,target,scale)
    for name,pos,power,size in [('Key',(-3,-2,4),180,5),('Fill',(-4,3,1.0),220,5),('Rear fill',(3,1,2),120,5),('Low fill',(-3,0,-1),100,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
        o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=pos
        o.rotation_euler=(Vector((.5,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
    sc.world.use_nodes=True;bg=sc.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(1,1,1,1);bg.inputs['Strength'].default_value=.8
    sc.render.engine='CYCLES';sc.cycles.samples=48;sc.cycles.use_denoising=True
    sc.render.resolution_x=sc.render.resolution_y=1000;sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
    sc.view_settings.view_transform='Standard';sc.view_settings.exposure=-.85
    sc.render.use_compositing=False;sc.render.use_sequencer=False;sc.camera=bpy.data.objects['REVIEW_front']

def sections(z):
    table=CONTRACT['fleece_sections_z_halfwidth_xfront_xback']
    i=max(0,min(len(table)-2,int(np.searchsorted([r[0] for r in table],z)-1)))
    t=(z-table[i][0])/(table[i+1][0]-table[i][0]);t=max(0,min(1,t))
    result=[]
    for k in [1,2,3]:
        a=table[max(0,i-1)][k];b=table[i][k];c=table[i+1][k];d=table[min(len(table)-1,i+2)][k]
        result.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
    return result

def shellpoint(z,t,detail=False):
    w,xf,xb=sections(z);co=math.cos(t);si=math.sin(t)
    if ATTEMPT>1 and z>.95:
        w=.72*math.sqrt(max(0,1-z));half=.62*math.sqrt(max(0,1-z));xf=.55-half;xb=.55+half
    x=(xf+xb)/2-(xb-xf)/2*co;y=w*si
    front=max(0,co)
    # A true three-dimensional face recess; Skin occludes the recessed surface.
    aperture=(1-smooth(.525,.588,z))*smooth(.207,.256,z)
    opening=.257+.012*math.exp(-((z-.42)/.13)**2)
    x+=(.36 if ATTEMPT==1 else .065)*math.exp(-(y/opening)**8)*aperture*front**5
    # Recess the actual shoulder surface behind the accepted ear geometry.
    socket=math.exp(-((abs(y)-.426)/.151)**(6 if ATTEMPT==1 else 4)-((z-.451)/(.107 if ATTEMPT==1 else .074))**(6 if ATTEMPT==1 else 4))*front**2
    x+=(.43 if ATTEMPT==1 else .31)*socket
    if ATTEMPT==3:
        # Explicit rounded-rectangular aperture in the same spatial surface.
        # Use the accepted face's measured convex Y profile, with a shallow lip.
        q=(y/.289)**4+((z-.391)/.174)**4
        inside=1-smooth(.78,1.25,q)
        facial=.023+3.3*y*y+.062*math.exp(-((z-.235)/.048)**2)
        desired=facial-.056+.135*inside
        blend=(1-smooth(.32,.39,abs(y)))*smooth(.16,.21,z)*(1-smooth(.60,.66,z))*front**.4
        x=x*(1-blend)+desired*blend
        # The full accepted ear module sits above a broad, smoothly recessed bed.
        ear=math.exp(-((abs(y)-.447)/.160)**6-((z-.442)/.100)**6)*front**.6
        x=x*(1-ear)+max(x,.83)*ear
    if detail:
        # Shallow anisotropic locks, sampled in current-authority projection space.
        # The field is displaced on ONE pre-existing shell, never sphere union.
        relief=0.0
        for u,v,ru,rv,amp in FRONT_LOCKS:
            yy=(630-u)/1012;zz=(1161-v)/1012
            r=((y-yy)/(ru/1012))**2+((z-zz)/(rv/1012))**2
            relief+=amp*math.exp(-r*1.8)
        x-=relief*front**3*(2.7 if ATTEMPT==3 else 1)
        sidefield=0.0
        for u,v,ru,rv,amp in SIDE_LOCKS:
            xx=(u-145)/918;zz=(999-v)/918
            r=((x-xx)/(ru/918))**2+((z-zz)/(rv/918))**2
            sidefield+=amp*math.exp(-r*1.9)
        y+=math.copysign(sidefield*abs(si)**4*(2.7 if ATTEMPT==3 else 1),y)
        # Unequal selective outline scallops have a short inward falloff.
        if ATTEMPT==2:
            q=(.012*math.sin(z*70+.4)+.006*math.sin(z*117+1.1))
            y+=math.copysign(q*abs(si)**18,y)
            x+=.009*math.sin(z*66+.2)*max(0,-co)**18
        else:
            # Spatially localized outline scallops, fading over .11 units into
            # the surface; no radial or circumferential propagation.
            for xx,zz,rr,amp in [(.24,.73,.10,.017),(.46,.86,.11,.023),(.66,.91,.13,.020),(.86,.73,.12,.016),(.99,.53,.12,.018),(1.05,.32,.10,.018),(.90,.19,.10,.016),(.55,.15,.11,.019),(.28,.20,.09,.019)]:
                bump=amp*math.exp(-((x-xx)/rr)**2-((z-zz)/rr)**2)
                y+=math.copysign(bump*abs(si)**8,y)
            y+=math.copysign(relief*abs(si)**14*.8,y)
        z+=(.012+.014*math.sin(5*t+.7)+.009*math.cos(9*t+.2))*math.exp(-((z-.10)/.052)**2)
    return (x,y,z)

# Current approved-image lock centers/radii only, not historical landmark data.
FRONT_LOCKS=[(630,216,93,79,.021),(527,233,81,65,.016),(722,232,81,65,.016),
 (423,254,91,75,.018),(838,253,89,73,.019),(321,315,84,88,.017),(938,315,83,82,.018),
 (494,294,65,74,.014),(574,296,87,88,.018),(697,294,88,85,.020),
 (400,308,62,51,.010),(864,306,60,54,.012),(338,399,103,80,.015),(855,421,105,95,.020),
 (581,412,88,85,.017),(737,417,92,89,.020),(646,356,121,69,.016),
 (479,504,75,80,.016),(570,541,88,93,.021),(707,542,92,94,.021),(796,506,72,72,.016),
 (914,537,81,88,.018),(371,483,80,73,.014),(256,483,77,76,.012),
 (169,523,63,73,.009),(1084,527,62,70,.010),(136,594,66,63,.010),(1121,597,67,70,.011),
 (377,660,63,62,.016),(353,785,54,55,.014),(359,854,56,59,.014),
 (973,656,73,66,.016),(965,785,54,55,.014),(964,854,56,59,.014),
 (433,944,65,59,.018),(508,984,64,54,.014),(607,1011,62,61,.016),(709,1000,65,59,.018),(810,981,66,61,.016),(874,945,69,62,.016),
 (204,902,68,91,.014),(1041,900,69,91,.015),(293,1011,68,63,.012),(994,1013,75,63,.013)]
SIDE_LOCKS=[(649,169,132,105,.018),(493,229,104,105,.020),(359,299,94,102,.018),
 (244,377,92,96,.018),(169,454,64,80,.018),(298,442,83,85,.019),(467,428,124,108,.024),
 (548,322,105,94,.017),(749,315,109,98,.019),(861,267,91,100,.017),
 (731,433,86,90,.014),(969,369,107,92,.018),(1068,482,93,81,.018),
 (963,625,115,94,.023),(1090,595,101,99,.018),(1100,747,90,99,.018),
 (932,784,123,104,.022),(775,848,95,76,.020),(608,799,102,99,.017),
 (468,565,83,76,.019),(465,681,74,73,.018),(358,834,95,81,.019),
 (626,637,89,97,.014),(827,536,96,93,.016)]

def create_shell(detail):
    verts=[];faces=[];N=320;R=256
    for j in range(R+1):
        z=.075+.925*j/R
        for i in range(N):verts.append(shellpoint(z,math.tau*i/N,detail))
    for j in range(R):
        for i in range(N):
            a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
    faces+=[tuple(reversed(range(N))),tuple(R*N+i for i in range(N))]
    clay=material('V003 neutral pearl clay',(.73,.73,.73))
    # Shared edge coordinates preserve a continuous exterior. Semantic seam is
    # only authoring ownership, not separate lobe geometry or overlapping balls.
    for owner in ['head','torso']:
        fs=[f for f in faces if (sum(verts[k][0] for k in f)/len(f)<.54)==(owner=='head')]
        ids=sorted({k for f in fs for k in f});remap={k:i for i,k in enumerate(ids)}
        ob=mesh('FLEECE_'+owner.upper()+'_SURFACE',[verts[k] for k in ids],[tuple(remap[k] for k in f) for f in fs],clay)
        ob['construction']='Continuous dual-envelope section shell; shallow smooth relief; no union/remesh'
        ob['motion_owner']=owner;ob['semantic_region']=owner+'_regional_surface'
        for name in ['touch_L','touch_R','crown','face_frame','chest_front','central_back','rump','lower_belly','ear_socket']:
            g=ob.vertex_groups.new(name=name)
            for v in ob.data.vertices:
                x,y,z=v.co
                if name.startswith('touch'):weight=smooth(-.08,.08,y if name=='touch_L' else -y)
                else:
                    cx,cz,rr={'crown':(.40,.82,.31),'face_frame':(.19,.46,.25),'chest_front':(.17,.19,.19),'central_back':(.72,.68,.3),'rump':(1,.4,.26),'lower_belly':(.64,.15,.27),'ear_socket':(.48,.45,.16)}[name]
                    weight=math.exp(-((x-cx)**2+(z-cz)**2)/(rr*rr))
                if weight>.008:g.add([v.index],weight,'REPLACE')
        parent(ob,bpy.data.objects['FLEECE_'+owner.upper()+'_OWNER'])
    # Independent genuinely volumetric tuft, generated as one displaced surface.
    vv=[];ff=[];n=64;r=40
    for j in range(r+1):
        a=math.pi*j/r
        for i in range(n):
            t=math.tau*i/n;rr=1+.12*math.sin(3*t)*math.sin(a)**2+.07*math.cos(5*a)
            vv.append((1.196+.060*math.cos(a)*rr,.060*math.sin(a)*math.cos(t)*rr,.366+.062*math.sin(a)*math.sin(t)*rr))
    for j in range(r):
        for i in range(n):a=j*n+i;b=j*n+(i+1)%n;ff.append((a,b,b+n,a+n))
    ob=mesh('TAIL_FLEECE_SHELL',vv,ff,clay);parent(ob,bpy.data.objects['TAIL_PIVOT']);ob['motion_owner']='tail'

def retain_modules():
    # v002 is only a donor for near-correct facial features and small solid charms.
    with bpy.data.libraries.load(str(PREVIOUS),link=False) as (src,dst):
        names=[n for n in src.objects if n.startswith(('EYE_','EYELID_','HOOF_','STAR_')) or n=='MOON']
    for n in names:
        if bpy.data.objects.get(n):bpy.data.objects.remove(bpy.data.objects[n],do_unlink=True)
    with bpy.data.libraries.load(str(PREVIOUS),link=False) as (src,dst):dst.objects=names
    for ob in dst.objects:bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.update()
    for ob in dst.objects:
        m=ob.matrix_world.copy();ob.parent=None;ob.matrix_world=m
        if ob.type=='MESH':
            ob.data.transform(ob.matrix_world);ob.matrix_world.identity()
        if ob.name.startswith('HOOF_'):
            center=np.mean([v.co[:] for v in ob.data.vertices],axis=0)
            for v in ob.data.vertices:
                v.co.y=center[1]+(v.co.y-center[1])*1.10;v.co.z*=.76
        if ob.name.startswith('STAR_') or ob.name=='MOON':
            if ob.type=='EMPTY':bpy.data.objects.remove(ob,do_unlink=True);continue
            parent(ob,bpy.data.objects['FLEECE_HEAD_OWNER' if any(s in ob.name for s in ['crown','brow','upper','MOON']) else 'FLEECE_TORSO_OWNER'])

def face_ears():
    ob=bpy.data.objects['CENTRAL_CHASSIS']
    # Candidate-only lower-front flattening removes the downward facing shelf;
    # head width, eye line and the accepted source file remain intact.
    for v in ob.data.vertices:
        x,y,z=v.co
        if x<.29 and .19<z<(.40 if ATTEMPT==1 else .335):
            target=.023+2.85*y*y
            w=(1-smooth(.32 if ATTEMPT==1 else .29,.40 if ATTEMPT==1 else .335,z))*smooth(.19,.245,z)*(1-smooth(.20,.29,x))
            if ATTEMPT==3:w*=.22
            v.co.x=x*(1-w)+target*w
        if x>.46 and z<.23:v.co.z+=.065*math.exp(-((x-.73)/.28)**4)*max(0,min(1,(.23-z)/.14))
    # Correct lower-face normal flow, only on the visible front lower region.
    ob.data.update()
    normals=[]
    for v in ob.data.vertices:
        n=v.normal.copy();x,y,z=v.co
        weight=(1-smooth(.32 if ATTEMPT==1 else .29,.39 if ATTEMPT==1 else .335,z))*smooth(.20,.26,z)*(1-smooth(.16,.28,x))
        target=Vector((-1,5.7*y,.035)).normalized();normals.append(tuple(n.lerp(target,weight*.9).normalized()))
    ob.data.normals_split_custom_set_from_vertices(normals)
    for name in ['EAR_L','EAR_R']:
        o=bpy.data.objects[name]
        for v in o.data.vertices:
            v.co.z=.440+(v.co.z-.470)*.72
            v.co.x=.35+(v.co.x-.35)*1.18
            v.co.y+=math.copysign(.008,v.co.y)
        o['v003_front_correction']='72% vertical span; root socket exposure; 118% depth sweep'
    # Direct diffuse face shader, no new emission or mixed unlit shader.
    for m in ob.data.materials:
        if not m.use_nodes:continue
        bs=m.node_tree.nodes.get('Principled BSDF')
        if bs:
            bs.inputs['Roughness'].default_value=.9;bs.inputs['Specular IOR Level'].default_value=.16
            bs.inputs['Emission Strength'].default_value=0

def build():
    assert sha(BASE)==SKIN_SHA
    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    empty('FLEECE_HEAD_OWNER',(.38,0,.49));empty('FLEECE_TORSO_OWNER',(.65,0,.38))
    retain_modules();face_ears();create_shell(ATTEMPT>1)
    if ATTEMPT>1:attach_charms()
    for name,loc in [('fleece_front',(.12,0,.20)),('pocket_front_L',(.15,.20,.24)),('pocket_front_R',(.15,-.20,.24)),('gift_reveal',(.14,0,.23))]:parent(empty(name,loc),bpy.data.objects['FLEECE_TORSO_OWNER'])
    presentation();sc=bpy.context.scene
    sc['phase1_state']='NORMAL_FLEECE_V003_GEOMETRY_REVIEW';sc['geometry_attempt']=ATTEMPT
    sc['authority_contract_sha256']=sha(OUT/'authority-contract.json')
    sc['accepted_skin_sha256']=SKIN_SHA
    save()

def attach_charms():
    from mathutils.bvhtree import BVHTree
    vs=[];fs=[]
    for name in ['FLEECE_HEAD_SURFACE','FLEECE_TORSO_SURFACE']:
        o=bpy.data.objects[name];offset=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices);fs.extend(tuple(offset+i for i in p.vertices) for p in o.data.polygons)
    tree=BVHTree.FromPolygons(vs,fs)
    for o in list(bpy.context.scene.objects):
        if o.type!='MESH' or not(o.name.startswith('STAR_') or o.name=='MOON') or o.name.endswith('_glint'):continue
        pts=[o.matrix_world@v.co for v in o.data.vertices];c=sum(pts,Vector())/len(pts)
        n=Vector((0,math.copysign(1,c.y),0)) if 'rump' in o.name else Vector((-.80,.60,.03)).normalized() if o.name=='MOON' else Vector((-1,0,0))
        hit,normal,idx,dist=tree.ray_cast(c+n*2,-n,4)
        if hit is None:continue
        delta=hit+n*.023-c;o.location+=delta
        glint=bpy.data.objects.get(o.name+'_glint')
        if glint:glint.location+=delta

def render():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));sc=bpy.context.scene
    folder=OUT/arg('--folder','.')
    folder.mkdir(parents=True,exist_ok=True)
    quick='--quick' in ARGS
    if quick:sc.render.resolution_percentage=60;sc.cycles.samples=16
    views=arg('--views','front,side,3q').split(',');digest=sha(ASSET)
    mp=folder/'render-manifest.json';manifest=json.loads(mp.read_text()) if mp.exists() else {}
    if manifest.get('asset_sha256')!=digest:manifest={'asset_sha256':digest,'asset':ASSET.relative_to(ROOT).as_posix(),'views':{}}
    for view in views:
        sc.camera=bpy.data.objects['REVIEW_'+view];path=folder/(view+'.png');sc.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        manifest['views'][view]={'file':path.name,'sha256':sha(path),'resolution':[round(sc.render.resolution_x*sc.render.resolution_percentage/100)]*2,
            'samples':sc.cycles.samples,'camera':sc.camera.name,'camera_matrix':[list(r) for r in sc.camera.matrix_world],
            'orthographic_scale':sc.camera.data.ortho_scale,'geometry_attempt':sc.get('geometry_attempt'),'appearance_pass':sc.get('appearance_pass',0),
            'view_transform':sc.view_settings.view_transform,'exposure':sc.view_settings.exposure}
        mp.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
def audit():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));sc=bpy.context.scene
    report={'asset':ASSET.relative_to(ROOT).as_posix(),'sha256':sha(ASSET),'accepted_skin_sha256':sha(BASE),'accepted_skin_unchanged':sha(BASE)==SKIN_SHA,
       'starting_pushed_commit':'ab8ce236055df5ab6d8c81039aed73bd961cf843','v002_human_review':'FAIL','v003_human_review':'PENDING','phase1_state':sc.get('phase1_state'),
       'geometry_attempt':sc.get('geometry_attempt'),'appearance_pass':sc.get('appearance_pass',0),'non_finite_vertices':0,'owners':{},'meshes':{},'authorities':[],
       'no_camera_conditioned_geometry':True,'compositing':sc.render.use_compositing,'motion':'NOT_PERFORMED','deformation':'NOT_PERFORMED','runtime':'NOT_PERFORMED','device':'NOT_PERFORMED'}
    for o in sc.objects:
        if o.type=='MESH':
            report['non_finite_vertices']+=sum(not all(math.isfinite(a) for a in v.co) for v in o.data.vertices)
            report['meshes'][o.name]={'vertices':len(o.data.vertices),'groups':[g.name for g in o.vertex_groups]}
    for name in ['FLEECE_HEAD_OWNER','FLEECE_TORSO_OWNER','TAIL_PIVOT']:
        report['owners'][name]=[o.name for o in sc.objects if o.parent and o.parent.name==name];assert report['owners'][name]
    for name in ['FLEECE_HEAD_SURFACE','FLEECE_TORSO_SURFACE']:
        assert {'touch_L','touch_R','face_frame','chest_front','lower_belly'}<=set(report['meshes'][name]['groups'])
    report['anchors']={}
    for name in ['fleece_front','pocket_front_L','pocket_front_R','gift_reveal']:
        ob=bpy.data.objects[name];assert ob.parent.name=='FLEECE_TORSO_OWNER'
        report['anchors'][name]={'parent':ob.parent.name,'position':list(ob.matrix_world.translation)}
    report['neutral_shape_values']={o.name:{k.name:k.value for k in o.data.shape_keys.key_blocks if k.name!='Basis'} for o in sc.objects if o.type=='MESH' and o.data.shape_keys}
    assert all(abs(v)<1e-8 for values in report['neutral_shape_values'].values() for v in values.values())
    for a in json.loads((ROOT/'assets/grimo/source/carol/approved-3d/authority.json').read_text())['authorityOrder']:
        p=ROOT/a['path'];report['authorities'].append({'path':a['path'],'sha256':sha(p),'matches_manifest':sha(p).lower()==a['sha256'].lower()})
    report['images']=[{'name':i.name,'packed':bool(i.packed_file),'path':i.filepath} for i in bpy.data.images if i.source=='FILE']
    for i in bpy.data.images:
        if i.source=='FILE' and not i.packed_file:assert Path(bpy.path.abspath(i.filepath)).is_file(),i.filepath
    assert report['accepted_skin_unchanged'] and report['non_finite_vertices']==0
    assert all(a['matches_manifest'] for a in report['authorities'])
    assert len([n for n in report['meshes'] if n.startswith('HOOF_')])==4
    (OUT/'asset-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('AUDIT_OK',report['sha256'])
if COMMAND=='build':build()
elif COMMAND=='look':raise RuntimeError('Appearance withheld: geometry has not converged.')
elif COMMAND=='render':render()
elif COMMAND=='audit':audit()
elif COMMAND=='finalize':
    raise RuntimeError('Geometry failed the bounded internal review; this asset cannot be finalized as review-ready.')
elif COMMAND=='mark-failed':
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));sc=bpy.context.scene
    sc['phase1_state']='NORMAL_FLEECE_V003_GEOMETRY_FAILED'
    sc['failure_reason']='Three geometry attempts exhausted. Broad crown/chest shelves and deep ear/face recesses remain; fleece hierarchy and Front likeness are not credible. Appearance work withheld.'
    save()
else:raise ValueError(COMMAND)
