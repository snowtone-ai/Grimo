"""Carol v002: fine cloud hierarchy, shared pigment wash, and tapered hooves with distal cuts.
Uses v001's construction utilities, not its saved geometry or material assignment.
Run Blender --python this_file -- [render] [quick] views front side ...
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'scripts/blender/build-carol-normal-fleece-v001.py').read_text(encoding='utf-8')
source=source.replace('h,_,_,_=tree.ray_cast(pos+n*.6,-n,1.2)','h=None')
source=source.replace('ev=ob.evaluated_get(deps); me=ev.to_mesh()','me=ob.data')
source=source.replace('ev.to_mesh_clear()','pass')
source=source.replace("k=o.shape_key_add(name='Local_contact_compress')","k=o.shape_key_add(name='Local_contact_compress',from_mix=False); k.value=0")
source=source.replace('world=o.matrix_world.copy(); o.parent=p;', 'bpy.context.view_layer.update(); world=o.matrix_world.copy(); o.parent=p;')
exec(source[:source.index("if 'render' not in MODE")].replace('normal-fleece-v001','normal-fleece-v002'))

def pigment():
    m=bpy.data.materials.new('Fleece — continuous pearl lavender azure wash');m.use_nodes=True
    n=m.node_tree.nodes;l=m.node_tree.links;b=n.get('Principled BSDF')
    b.inputs['Roughness'].default_value=.86;b.inputs['Specular IOR Level'].default_value=.22
    b.inputs['Subsurface Weight'].default_value=.08;b.inputs['Subsurface Radius'].default_value=(.07,.045,.09)
    a=n.new('ShaderNodeAttribute');a.attribute_name='pigment'
    coord=n.new('ShaderNodeTexCoord');coord.object=bpy.data.objects['PIGMENT_SPACE']
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=28;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.7
    l.new(coord.outputs['Object'],noise.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.23;ramp.color_ramp.elements[0].color=(.40,.50,1,1)
    ramp.color_ramp.elements[1].position=.77;ramp.color_ramp.elements[1].color=(1,.96,.91,1)
    l.new(noise.outputs['Fac'],ramp.inputs[0])
    mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.28
    l.new(a.outputs['Color'],mix.inputs[1]);l.new(ramp.outputs[0],mix.inputs[2])
    geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Normal'],sep.inputs[0])
    top=n.new('ShaderNodeMapRange');top.inputs['From Min'].default_value=0;top.inputs['From Max'].default_value=1;top.inputs['To Min'].default_value=0;top.inputs['To Max'].default_value=.35
    l.new(sep.outputs['Z'],top.inputs['Value'])
    glaze=n.new('ShaderNodeMixRGB');l.new(top.outputs[0],glaze.inputs[0]);l.new(mix.outputs[0],glaze.inputs[1]);glaze.inputs[2].default_value=(1,.96,.94,1)
    facing=n.new('ShaderNodeLayerWeight');facing.inputs['Blend'].default_value=.3
    edge=n.new('ShaderNodeValToRGB');edge.color_ramp.elements[0].position=.12;edge.color_ramp.elements[0].color=(0,0,0,1)
    edge.color_ramp.elements[1].position=.95;edge.color_ramp.elements[1].color=(.72,.72,.72,1)
    l.new(facing.outputs['Fresnel'],edge.inputs[0])
    rim=n.new('ShaderNodeMixRGB');l.new(edge.outputs[0],rim.inputs[0]);l.new(glaze.outputs[0],rim.inputs[1]);rim.inputs[2].default_value=(.28,.24,.88,1)
    ao=n.new('ShaderNodeAmbientOcclusion');ao.inputs['Distance'].default_value=.035;ao.samples=16;ao.only_local=True
    shade=n.new('ShaderNodeMixRGB');shade.inputs[1].default_value=(.55,.56,1,1);shade.inputs[2].default_value=(1,1,1,1);l.new(ao.outputs['AO'],shade.inputs[0])
    depth=n.new('ShaderNodeMixRGB');depth.blend_type='MULTIPLY';depth.inputs[0].default_value=.5;l.new(rim.outputs[0],depth.inputs[1]);l.new(shade.outputs[0],depth.inputs[2])
    l.new(depth.outputs[0],b.inputs['Base Color'])
    em=n.new('ShaderNodeEmission');em.inputs['Strength'].default_value=1.65;l.new(depth.outputs[0],em.inputs['Color'])
    sh=n.new('ShaderNodeMixShader');sh.inputs[0].default_value=.55;l.new(b.outputs[0],sh.inputs[1]);l.new(em.outputs[0],sh.inputs[2]);l.new(sh.outputs[0],n.get('Material Output').inputs['Surface'])
    return m

def wash(o):
    attr=o.data.color_attributes.new(name='pigment',type='FLOAT_COLOR',domain='POINT')
    # One coordinate field spans every region; no random object colors.
    from mathutils.noise import noise_vector
    for v,d in zip(o.data.vertices,attr.data):
        x,y,z=v.co;ay=abs(y)
        white=max(math.exp(-((x-.10)/.25)**2-((z-.665)/.19)**2-((y)/.23)**4),
                  math.exp(-((y)/.18)**2-((z-.87)/.22)**2-((x-.33)/.37)**2),
                  math.exp(-((x-.14)/.28)**2-((z-.18)/.19)**2),
                  math.exp(-((x-.24)/.14)**2-((ay-.29)/.10)**2-((z-.44)/.24)**4),
                  math.exp(-((x-.94)/.28)**4-((z-.34)/.25)**4))
        white=max(white,math.exp(-((x-.12)/.25)**4-((z-.72)/.26)**4))
        moon_blue=math.exp(-((x-.43)/.53)**4-((y-.30)/.20)**4-((z-.755)/.205)**4)
        white*=1-.96*moon_blue
        blue=max(moon_blue,math.exp(-((x-.43)/.35)**2-((ay-.35)/.25)**2-((z-.70)/.28)**2))
        base=[.43-.40*blue,.50-.29*blue,1.15+.05*blue]
        white=min(1,white*1.09)
        col=[base[i]*(1-white)+[1,.98,.94][i]*white for i in range(3)]
        d.color=(*col,1)
    o.data.materials.clear();o.data.materials.append(fleece)

# Spheres and a few joined unequal lobes replace the repeated radial flower recipe.
old_cloud=cloud
def cloud(name,c,r,normal,region,mat,seed,quiet=False):
    n=Vector(normal).normalized();e=Vector((0,0,1)).cross(n)
    if e.length<.1:e=Vector((0,1,0))
    e.normalize();f=n.cross(e).normalized()
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=24)
    o=bpy.context.object;o.name=name
    for v in o.data.vertices:
        q=v.co.copy();v.co=Vector(c)+e*q.x*r[0]+f*q.y*r[1]+n*q.z*r[2]
    o.data.update()
    o['motion_owner']='head' if region in ['crown','face_frame'] else 'torso'
    link_parent(o,owners[o['motion_owner']]);clouds.append(o);return o

def blend_owned_surfaces():
    """Soft connected head and torso surfaces; local controls independent of lobes."""
    for owner in ['head','torso']:
        obs=[o for o in clouds if o['motion_owner']==owner]
        bpy.ops.object.select_all(action='DESELECT')
        for o in obs:
            o.modifiers.clear();o.select_set(True)
        bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=obs[0]
        # Apply ownership transform before masks/pigment use character coordinates.
        world=o.matrix_world.copy();o.parent=None;o.matrix_world=world
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
        o.name='FLEECE_'+owner.upper()+'_SURFACE'
        rem=o.modifiers.new('Connected cloud volumes','REMESH');rem.mode='VOXEL';rem.voxel_size=.0045;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
        sm=o.modifiers.new('Soft cloud junctions','SMOOTH');sm.factor=.85;sm.iterations=5;bpy.ops.object.modifier_apply(modifier=sm.name)
        for p in o.data.polygons:p.use_smooth=True
        for a in list(o.data.color_attributes):o.data.color_attributes.remove(a)
        wash(o);o.vertex_groups.clear();o['semantic_region']=owner+'_regional_surface';o['motion_owner']=owner
        for side,sign in [('L',1),('R',-1)]:
            g=o.vertex_groups.new(name='touch_'+side)
            for v in o.data.vertices:
                w=max(0,min(1,.5+sign*v.co.y/.12))
                if w:g.add([v.index],w,'REPLACE')
        for region,center,radius in [('crown',(.42,0,.80),.3),('face_frame',(.20,0,.48),.32),('chest_front',(.28,0,.2),.24),('central_back',(.72,0,.68),.3),('rump',(1,0,.4),.27),('lower_belly',(.65,0,.23),.3)]:
            g=o.vertex_groups.new(name=region)
            for v in o.data.vertices:
                w=math.exp(-((v.co-Vector(center)).length/radius)**2*2)
                if w>.01:g.add([v.index],w,'REPLACE')
        o.shape_key_add(name='Basis',from_mix=False)
        for side,sign in [('L',1),('R',-1)]:
            k=o.shape_key_add(name='Local_contact_'+side,from_mix=False);k.value=0
            c=Vector((.30,sign*.3,.43)) if owner=='head' else Vector((.65,sign*.43,.4))
            for v,p in zip(o.data.vertices,k.data):p.co=v.co+Vector((.009,-sign*.018,0))*math.exp(-((v.co-c).length/.18)**2*2)
        k=o.shape_key_add(name='Face_opening_corrective',from_mix=False);k.value=0
        for v,p in zip(o.data.vertices,k.data):
            w=math.exp(-((v.co.x-.22)/.25)**4-((v.co.z-.40)/.28)**4)
            p.co=v.co+Vector((.018,math.copysign(.018,v.co.y),.015 if v.co.z>.5 else -.015))*w
        link_parent(o,owners[owner]);clouds[:]=[q for q in clouds if q not in obs]+[o]

def hoof(name,cx,cy):
    # One continuous tapered solid. Only its distal 24% carries two incisions.
    old=bpy.data.objects[name];parent=old.parent;mat=old.data.materials[0]
    bpy.data.objects.remove(old,do_unlink=True)
    verts=[];faces=[];N=96;R=40
    for j in range(R+1):
        t=j/R;theta=math.pi*t
        z=.081+.081*math.cos(theta)
        width=.098*math.sin(theta)**.55
        depth=.105*math.sin(theta)**.65
        for i in range(N):
            a=math.tau*i/N;y=width*math.cos(a);x=depth*math.sin(a)
            distal=max(0,1-z/.075)**.8
            grooves=sum(math.exp(-((y-g)/.007)**2) for g in [-.033,.033])
            # Cuts indent both the forward face and the rounded terminal edge.
            x+=.037*grooves*distal*max(0,-math.sin(a))
            zz=z+.029*grooves*max(0,1-z/.028)**2
            verts.append((cx+x+.035*(z/.162),cy+y,zz))
    for j in range(R):
        for i in range(N):
            a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o)
    import bmesh
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    for p in me.polygons:p.use_smooth=True
    me.materials.append(mat)
    from mathutils import Matrix
    rot=Matrix.Rotation(-math.copysign(math.radians(32),cy),3,'Z');center=Vector((cx,cy,0))
    for v in me.vertices:v.co=center+rot@(v.co-center)
    if parent:link_parent(o,parent)

old_motif=motif
def motif(name,c,size,normal,moon=False,owner='torso'):
    o=old_motif(name,c,size,normal,moon,owner)
    if moon:return o
    # Actual imported CC0 mesh, rounded and reshaped to Carol's soft ornament.
    bpy.context.view_layer.update()
    c=bpy.data.objects[name+'_anchor'].matrix_world.translation.copy()
    bpy.data.objects.remove(o,do_unlink=True)
    lines=(ROOT/'assets/grimo/source/carol/third-party/savino-star/star.obj').read_text().splitlines()
    vv=[tuple(map(float,q.split()[1:4])) for q in lines if q.startswith('v ')]
    ff=[tuple(int(v)-1 for v in q.split()[1:]) for q in lines if q.startswith('f ')]
    outline=[Vector(((z-2.42857)/2.5435,(y+3.03791)/2.5435)) for i,(x,y,z) in enumerate(vv[:10])]
    boundary=[]
    for i,p in enumerate(outline):
        rounding=.20 if i%2==0 else .14
        a=p.lerp(outline[(i-1)%10],rounding);b=p.lerp(outline[(i+1)%10],rounding)
        for j in range(8):
            t=j/8;boundary.append((1-t)**2*a+2*(1-t)*t*p+t*t*b)
    extent=max(q.length for q in boundary);boundary=[q/extent for q in boundary]
    n=Vector(normal).normalized();e=Vector((0,0,1)).cross(n).normalized();f=n.cross(e).normalized()
    # Use the donor outline, with rounded corners and a continuous convex cap.
    verts=[];faces=[];N=len(boundary);R=8
    for back in [False,True]:
        start=len(verts);verts.append(c+n*(-.012 if back else .041))
        for j in range(1,R+1):
            t=j/R
            for q in boundary:verts.append(c+e*q.x*size*t+f*q.y*size*t+n*(.010-.022*(1-t*t)**.6 if back else .010+.031*(1-t*t)**.6))
        for i in range(N):faces.append((start,start+1+i,start+1+(i+1)%N))
        for j in range(R-1):
            a=start+1+j*N;b=a+N
            for i in range(N):faces.append((a+i,b+i,b+(i+1)%N,a+(i+1)%N))
    layer=1+R*N;a=1+(R-1)*N;b=layer+a
    for i in range(N):faces.append((a+i,a+(i+1)%N,b+(i+1)%N,b+i))
    me=bpy.data.meshes.new(name+'_Savino_CC0');me.from_pydata(verts,[],faces);me.update()
    import bmesh
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o)
    for p in o.data.polygons:p.use_smooth=True
    o.data.materials.append(gold);link_parent(o,owners[owner])
    o['source']='Savino, Star, OpenGameArt, CC0; rounded and rescaled'
    # Small physical ivory inlay, not a view-dependent billboard.
    sparkle=bpy.data.materials.get('Motif ivory glint')
    if not sparkle:
        sparkle=bpy.data.materials.new('Motif ivory glint');sparkle.use_nodes=True
        bs=sparkle.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(1,.96,.77,1);bs.inputs['Emission Color'].default_value=(1,.94,.74,1);bs.inputs['Emission Strength'].default_value=1.4
    cc=c+n*.0415
    points=[cc+e*u*size+f*v*size for u,v in [(0,.18),(.15,0),(0,-.18),(-.15,0)]]
    mesh=bpy.data.meshes.new(name+'_glint');mesh.from_pydata(points,[],[(0,1,2,3)]);mesh.materials.append(sparkle)
    ob=bpy.data.objects.new(name+'_glint',mesh);bpy.context.scene.collection.objects.link(ob);link_parent(ob,owners[owner])
    return o

if 'render' not in MODE:
    bpy.ops.wm.open_mainfile(filepath=str(BASE));sc=bpy.context.scene
    owners={'head':empty('FLEECE_HEAD_OWNER',(.38,0,.49)),'torso':empty('FLEECE_TORSO_OWNER',(.65,0,.38)),'tail':bpy.data.objects['TAIL_PIVOT']}
    empty('PIGMENT_SPACE',(0,0,0));fleece=pigment();clouds=[]
    for v in bpy.data.objects['CENTRAL_CHASSIS'].data.vertices:
        if v.co.x>.46 and v.co.z<.23:v.co.z+=.065*math.exp(-((v.co.x-.73)/.28)**4)*max(0,min(1,(.23-v.co.z)/.14))
    for ob in list(sc.objects):
        if ob.name.startswith('HOOF_'):
            cy=sum(v.co.y for v in ob.data.vertices)/len(ob.data.vertices)
            if 'FORE' in ob.name:cy=math.copysign(.20,cy)
            hoof(ob.name,.38 if 'FORE' in ob.name else .91,cy)
    for name in ['FORE_L','FORE_R']:
        for v in bpy.data.objects[name].data.vertices:
            v.co.y+=math.copysign(.055,v.co.y)*max(0,min(1,(.24-v.co.z)/.12))
    for side in ['L','R']:
        for name in ['EYE_'+side,'EYELID_'+side]:
            ob=bpy.data.objects[name]
            for v in ob.data.vertices:
                v.co.z=.43672+(v.co.z-.43672)*.897-.022
                v.co.y=math.copysign(.162,v.co.y)+(v.co.y-math.copysign(.162,v.co.y))*1.040
    specs=[]
    def add(name,c,r,reg,n=(0,0,1)):specs.append((name,c,r,n,reg))
    # Compact high crown, cascading uneven scallops at the face aperture.
    for name,c,r in [
        ('Crown_apex',(.49,0,.875),(.18,.14,.145)),
        ('Crown_front',(.28,0,.815),(.15,.12,.13)),
        ('Brow_center',(.105,0,.665),(.115,.125,.112)),
        ('Brow_left',(.14,.145,.715),(.12,.137,.126)),
        ('Brow_right',(.15,-.16,.735),(.128,.145,.128)),
        ('Brow_low_left',(.075,.105,.612),(.088,.07,.073)),
        ('Brow_low_right',(.07,-.115,.621),(.095,.072,.071)),
        ('Brow_low_middle',(.065,-.005,.614),(.09,.069,.076))]:
        add(name,c,r,'crown' if name.startswith('Crown') else 'face_frame',(-1,0,0))
    for s in [-1,1]:
        tag='L' if s==1 else 'R'
        for name,x,y,z,rx,ry,rz,reg in [
            ('Crown_peak',.50,.18,.86,.16,.13,.129,'crown'),
            ('Crown_bank',.52,.30,.79,.16,.13,.14,'crown'),
            ('Crown_mid',.34,.255,.805,.13,.125,.125,'crown'),
            ('Temple',.32,.345,.675,.135,.12,.13,'face_frame'),
            ('Outer_brow',.20,.285,.633,.13,.093,.095,'face_frame'),
            ('Cheek_top',.25,.295,.53,.08,.069,.066,'face_frame'),
            ('Cheek_middle',.24,.311,.410,.081,.072,.071,'face_frame'),
            ('Cheek_low',.27,.292,.306,.087,.083,.08,'face_frame'),
            ('Chest_inner',.27,.13,.204,.123,.09,.088,'chest_front'),
            ('Chest_outer',.32,.263,.205,.115,.11,.103,'chest_front'),
            ('Lower_front',.45,.39,.25,.13,.125,.12,'lower_belly'),
            ('Lower_mid',.65,.40,.235,.135,.12,.12,'lower_belly'),
            ('Side_upper',.75,.335,.745,.165,.166,.158,'central_back'),
            ('Side_middle',.67,.419,.57,.14,.13,.15,'central_back'),
            ('Side_back',.91,.335,.62,.17,.16,.16,'rump'),
            ('Rump_high',1.035,.23,.48,.12,.16,.14,'rump'),
            ('Rump_low',1.045,.23,.27,.12,.16,.12,'rump'),
            ('White_rump_top',.95,.421,.43,.13,.13,.133,'rump'),
            ('White_rump_bottom',.85,.43,.26,.13,.13,.113,'rump'),
            ('White_rump_front',.77,.442,.37,.125,.105,.13,'rump'),
            ('White_rump_back',1.03,.40,.31,.12,.115,.105,'rump'),
            ('Ear_under',.60,.435,.30,.105,.095,.091,'central_back'),
            ('Outer_low',.57,.465,.34,.105,.09,.10,'lower_belly'),
            ('Crown_small',.34,.28,.865,.09,.075,.08,'crown'),
            ('Brow_sidelet',.11,.232,.645,.080,.085,.068,'face_frame'),
            ('Crown_frontlet',.22,.16,.83,.075,.08,.082,'crown'),
            ('Moon_cloudlet',.30,.39,.735,.10,.087,.096,'crown'),
            ('Lower_frontlet',.34,.365,.175,.092,.082,.07,'lower_belly'),
            ('Lower_outerlet',.46,.46,.237,.09,.078,.087,'lower_belly'),
            ('Back_cloudlet',.87,.40,.72,.095,.08,.09,'central_back'),
        ]:add(name+'_'+tag,(x,s*y,z),(rx,ry,rz),reg,(0,s,0))
    for name,c,r,reg in [
        ('Chest_center',(.28,0,.155),(.13,.12,.078),'chest_front'),
        ('Dorsal',(.73,0,.79),(.21,.24,.17),'central_back'),
        ('Dorsal_rear',(.93,0,.64),(.20,.24,.20),'central_back'),
        ('Rump_center',(1.045,0,.40),(.13,.22,.20),'rump'),
        ('Rump_round_top',(1.05,.03,.52),(.12,.15,.13),'rump'),
        ('Rump_round_low',(1.07,-.04,.27),(.12,.14,.13),'rump'),
        ('Belly',(.68,0,.23),(.30,.28,.13),'lower_belly'),
        ('Inner_crown',(.46,0,.70),(.20,.24,.14),'crown'),
        ('Inner_torso',(.74,0,.43),(.26,.29,.20),'central_back')]:add(name,c,r,reg)
    # Individually placed Front-authority lobes. Pixel measurements are converted
    # to spatial ellipsoids; depth remains real and continuous with the side crown.
    specs=[q for q in specs if q[0] in ['Belly','Inner_torso','Rump_center']]
    add('Inner_crown',(.46,0,.70),(.20,.23,.14),'crown')
    front_lobes=[
        (405,265,80,80,.51),(525,229,76,70,.50),(630,238,89,89,.50),(730,234,72,72,.51),(835,264,88,83,.53),
        (317,321,85,85,.48),(413,305,56,57,.33),(473,282,40,52,.29),(543,278,73,73,.32),(702,281,80,78,.32),(850,310,55,58,.36),(940,328,78,86,.49),
        (252,409,70,74,.46),(1010,409,76,75,.46),(202,487,73,61,.55),(1053,487,73,67,.54),
        (521,359,70,62,.20),(635,350,80,65,.20),(737,357,69,66,.22),
        (854,408,105,89,.26),(727,430,90,80,.11),(617,444,92,82,.10),
        (507,515,70,65,.04),(581,536,88,84,.015),(672,542,55,80,.02),(725,536,74,82,.035),(828,513,67,74,.08),(918,483,67,66,.22),
        (895,591,70,65,.13),(957,627,66,53,.25),
        (382,406,83,80,.29),(440,454,55,59,.17),(433,524,40,45,.14),(385,580,58,52,.20),(338,624,53,56,.24),
        (348,705,30,35,.22),(335,774,56,55,.17),(345,859,55,55,.21),
        (965,712,30,35,.23),(969,780,53,54,.17),(957,860,55,53,.23),
        (432,948,70,63,.23),(504,972,63,54,.22),(588,991,51,51,.21),(673,995,49,54,.22),(733,983,62,59,.23),(808,951,76,61,.26),
        (140,580,60,60,.60),(173,480,50,54,.58),(128,646,66,57,.65),
        (1110,585,58,62,.60),(1090,666,67,61,.61),
        (191,836,57,60,.46),(240,855,55,55,.40),(247,761,42,48,.50),(275,701,43,40,.43),
        (213,932,57,67,.36),(241,988,51,60,.35),(303,1038,58,46,.34),(367,1018,52,45,.27),
        (530,1050,45,45,.31),(570,1065,40,37,.38),(659,1070,45,38,.39),(726,1050,52,39,.35),
        (889,1040,54,40,.34),(954,1011,58,52,.39),(1019,957,53,71,.37),
        (1060,872,64,65,.46),(1024,813,45,45,.45),(1098,800,60,58,.60),
        (212,568,63,58,.48),(1085,575,65,62,.51),(164,649,66,65,.64),(1101,654,67,64,.65),
        (245,922,64,67,.47),(996,928,74,74,.49),(300,996,64,58,.47),(908,1002,70,57,.49)
    ]
    for i,(px,py,rx,rz,x) in enumerate(front_lobes):
        y=(627-px)/1012;z=(1161-py)/1012
        reg='chest_front' if py>900 else ('crown' if py<410 else 'face_frame')
        if 410<=py<=600 and x<.1:x+=.045
        if py>900 and 380<px<850:x=.19+max(0,py-948)/102*.10
        depth=max(.068,min(.13,rx/1012*1.2))
        if 600<py<900 and 290<px<1000:x=.285;depth=.065
        elif py>900:depth=max(depth,.095)
        add('Authority_front_%02d'%i,(x,y,z),(depth,rx/1012,rz/1012),reg,(-1,0,0))
    # Side-authority dorsal/flank/rump hierarchy, on both sides of a full body.
    for side in [-1,1]:
        for i,(px,py,rx,rz,y) in enumerate([
            (660,215,135,134,.07),(826,267,123,118,.21),
            (753,322,100,111,.33),(979,391,108,116,.23),
            (923,507,102,102,.36),(1059,515,100,110,.24),
            (713,433,98,92,.39),(809,537,81,83,.42),
            (1026,604,139,110,.36),(1113,699,100,99,.31),
            (1080,792,95,89,.31),(940,797,110,101,.41),
            (899,682,91,90,.43),(763,824,85,89,.38),
            (667,834,70,76,.37),(585,842,70,76,.34),
            (536,785,99,108,.37),(454,846,75,63,.35),
            (1138,577,66,72,.23),(1211,657,40,43,.10),
        ]):
            x=(px-150)/920;z=(1000-py)/920
            # Narrow the high crown in Front without changing Side height/length.
            y*=1-.35*max(0,(z-.55)/.45)
            ry=.12 if py>500 else .13
            add('Side_%s_%02d'%(side,i),(x,side*y,z),(rx/920,ry,rz/920),'central_back' if px<850 else 'rump',(0,side,0))
        for i,(x,y,z,rx,ry,rz) in enumerate([
            (.34,.32,.67,.12,.10,.12),(.45,.32,.72,.13,.12,.13),
            (.29,.36,.56,.095,.085,.095),(.43,.34,.59,.105,.095,.09),
        ]):add('Head_bridge_%s_%d'%(side,i),(x,side*y,z),(rx,ry,rz),'face_frame',(0,side,0))
    # Small linking volumes close the mantle around ear roots and lower flank.
    for side in [-1,1]:
        for i,(x,y,z,rx,ry,rz) in enumerate([
            (.52,.39,.40,.10,.10,.085),(.64,.40,.43,.10,.10,.09),(.73,.44,.36,.085,.09,.085),
            (.72,.40,.52,.095,.095,.09),(.61,.42,.32,.09,.09,.09),
            (.80,.27,.65,.14,.15,.13),(.92,.25,.57,.12,.14,.12),
            (.44,.34,.27,.10,.11,.09),(.82,.36,.33,.09,.10,.10),
            (.72,.42,.28,.08,.09,.07),
        ]):add('Mantle_link_%s_%d'%(side,i),(x,side*y,z),(rx,ry,rz),'central_back',(0,side,0))
    add('Chest_continuity',(.34,0,.20),(.115,.27,.070),'chest_front',(-1,0,0))
    add('Dorsal_continuity',(.80,0,.80),(.17,.20,.15),'central_back')
    for i,(x,y,z,rx,ry,rz) in enumerate([
        (1.06,0,.58,.14,.16,.13),(1.11,-.18,.48,.105,.12,.115),
        (1.10,.18,.49,.105,.12,.12),(1.15,0,.40,.095,.125,.115),
        (1.10,-.22,.29,.105,.105,.10),(1.10,.22,.28,.10,.11,.10),
        (1.10,-.075,.225,.10,.10,.09),(1.10,.09,.23,.105,.105,.095),
        (.99,-.13,.69,.12,.13,.12),(.98,.13,.69,.12,.13,.12)
    ]):add('Rear_mantle_%02d'%i,(x,y,z),(rx,ry,rz),'rump',(1,0,0))
    for i,(name,c,r,n,reg) in enumerate(specs):
        # Utility basis maps e/f/n; convert desired world ellipsoid radii.
        nn=Vector(n).normalized();ee=Vector((0,0,1)).cross(nn)
        if ee.length<.1:ee=Vector((0,1,0))
        ee.normalize();ff=nn.cross(ee).normalized()
        rr=tuple(sum(abs(a[j])*r[j] for j in range(3)) for a in [ee,ff,nn])
        cloud('FL_'+name,c,rr,n,reg,fleece,100+i)
    blend_owned_surfaces()
    # Candidate-only diffuse lift removes the heavy cast shadow across the face.
    for mat in list(bpy.data.materials):
        if mat==fleece or not mat.use_nodes:continue
        if not any(mat==m for m in bpy.data.objects['CENTRAL_CHASSIS'].data.materials):continue
        nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');out=nt.nodes.get('Material Output')
        if bs and out:
            em=nt.nodes.new('ShaderNodeEmission');em.inputs['Strength'].default_value=1.9
            if bs.inputs['Base Color'].is_linked:nt.links.new(bs.inputs['Base Color'].links[0].from_socket,em.inputs['Color'])
            else:em.inputs['Color'].default_value=bs.inputs['Base Color'].default_value
            mix=nt.nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.35;nt.links.new(bs.outputs[0],mix.inputs[1]);nt.links.new(em.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs['Surface'])
    old_cloud('TAIL_FLEECE_SHELL',(1.235,0,.36),(.046,.045,.055),(1,0,.2),'tail',fleece,77)
    wash(clouds[-1])
    sub=clouds[-1].modifiers.new('Tail soft finish','SUBSURF');sub.levels=2;sub.render_levels=2
    gold=material('Motif honey light',(1,.58,.09),(1,.35,.01))
    bs=gold.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.36;bs.inputs['Emission Color'].default_value=(1,.5,.04,1);bs.inputs['Emission Strength'].default_value=.12
    nodes=gold.node_tree.nodes;links=gold.node_tree.links
    fres=nodes.new('ShaderNodeLayerWeight');ramp=nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color=(1,.76,.22,1);ramp.color_ramp.elements[1].position=.7;ramp.color_ramp.elements[1].color=(1,.38,.025,1)
    links.new(fres.outputs['Fresnel'],ramp.inputs[0]);links.new(ramp.outputs[0],bs.inputs['Base Color'])
    for name,c,size,n,owner in [
        ('STAR_crown',(.14,0,.856),.071,(-1,0,.15),'head'),
        ('STAR_brow',(-.02,-.04,.696),.070,(-1,0,0),'head'),
        ('STAR_chest',(.1,0,.173),.059,(-1,0,0),'torso'),
        ('STAR_upper_left',(.28,.43,.57),.055,(-1,0,0),'head'),
        ('STAR_lower_left',(.30,.39,.235),.058,(-.8,.6,0),'torso'),
        ('STAR_rump',(.91,-.55,.36),.063,(0,-1,0),'torso'),
        ('STAR_rump_L',(.91,.55,.36),.063,(0,1,0),'torso')]:motif(name,c,size,n,owner=owner)
    # A solid crescent charm: rounded elliptical cross sections taper into tips.
    # No surface-fitting plate or view-dependent displacement.
    moon=old_motif('MOON',(.32,.30,.72),.14,(-.72,.69,.02),True,owner='head')
    bpy.context.view_layer.update()
    c=bpy.data.objects['MOON_anchor'].matrix_world.translation.copy()
    bpy.data.objects.remove(moon,do_unlink=True)
    n=Vector((-.72,.69,.02)).normalized();e=Vector((0,0,1)).cross(n).normalized();f=n.cross(e).normalized()
    verts=[];faces=[];N=96;K=32
    for j in range(N+1):
        t=j/N;a=math.radians(55+250*t)
        radial=e*math.cos(a)+f*math.sin(a)
        thick=.045*math.sin(math.pi*t)**.68+.0005
        center=c+radial*.105+n*.016
        for k in range(K):
            q=math.tau*k/K
            verts.append(center+radial*thick*math.cos(q)+n*thick*.85*math.sin(q))
    for j in range(N):
        for k in range(K):
            a=j*K+k;b=j*K+(k+1)%K;faces.append((a,b,b+K,a+K))
    faces.extend([tuple(reversed(range(K))),tuple(N*K+k for k in range(K))])
    me=bpy.data.meshes.new('Solid crescent charm');me.from_pydata(verts,[],faces);me.update()
    import bmesh
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    moon=bpy.data.objects.new('MOON',me);sc.collection.objects.link(moon)
    for p in me.polygons:p.use_smooth=True
    me.materials.append(gold);link_parent(moon,owners['head'])
    moon['surface_attachment']='Solid tapered crescent charm seated on head fleece; independent head ownership'

    for name,c in [('fleece_front',(.14,0,.225)),('pocket_front_L',(.14,.2,.265)),('pocket_front_R',(.14,-.2,.265)),('gift_reveal',(.14,0,.245))]:link_parent(empty(name,c),owners['torso'])
    for o in list(sc.objects):
        if o.type in ['CAMERA','LIGHT']:bpy.data.objects.remove(o,do_unlink=True)
    for name,pos,target,scale in [
        ('front',(-4,0,.51),(.5,0,.51),1.30),('side',(.63,4,.51),(.63,0,.51),1.42),
        ('opposite_side',(.63,-4,.51),(.63,0,.51),1.42),('3q',(-2.8,-3,1.6),(.57,0,.47),1.5),
        ('rear',(4,0,.51),(.6,0,.51),1.4),('top',(.6,0,4),(.6,0,0),1.5)]:camera('REVIEW_'+name,pos,target,scale)
    for name,pos,power,size in [('Key',(-3,-2,4),260,4),('Fill',(-4,3,1.2),340,4),('Rim',(3,1,3),180,3),('Low fill',(-3,0,-.4),35,3)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
        o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((.5,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
    sc.world.use_nodes=True;sc.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.8,.8,.85,1)
    sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.7
    sc.render.engine='CYCLES';sc.cycles.samples=48;sc.cycles.use_denoising=True
    sc.render.resolution_x=1000;sc.render.resolution_y=1000;sc.render.resolution_percentage=100
    sc.render.film_transparent=True;sc.view_settings.view_transform='Standard';sc.view_settings.exposure=-.85
    sc.render.use_compositing=False;sc.render.use_sequencer=False
    sc.camera=bpy.data.objects['REVIEW_front'];sc['phase1_state']='NORMAL_FLEECE_V002_CONVERGENCE_IN_PROGRESS'
    # Blender on Windows can fail replacing an existing Unicode-path file.
    # Save a new sibling first; Python's Unicode-aware replace publishes it only
    # after Blender completed the save. Keep external asset paths unchanged.
    import os,uuid
    staging=ASSET.with_name(ASSET.stem+'.'+uuid.uuid4().hex+'.blend')
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(staging),compress=True,relative_remap=False)
    os.replace(staging,ASSET)
else:
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));sc=bpy.context.scene
if 'finalize' in MODE:
    assert 'render' in MODE, 'Finalize must reopen the reviewed saved candidate'
    import os,uuid
    sc['phase1_state']='NORMAL_FLEECE_V002_AWAITING_HUMAN_REVIEW'
    staging=ASSET.with_name(ASSET.stem+'.'+uuid.uuid4().hex+'.blend')
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(staging),compress=True,relative_remap=False)
    # Release Windows memory-mapped data from the opened destination first.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    os.replace(staging,ASSET)
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));sc=bpy.context.scene
if 'quick' in MODE:sc.render.resolution_percentage=60;sc.cycles.samples=16
views=MODE[MODE.index('views')+1:] if 'views' in MODE else ['front','side']
import hashlib,json
asset_sha=hashlib.sha256(ASSET.read_bytes()).hexdigest()
manifest_path=OUT/'render-manifest.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
if manifest.get('asset_sha256')!=asset_sha:manifest={'asset_sha256':asset_sha,'views':{}}
for view in views:
    sc.camera=bpy.data.objects['REVIEW_'+view];sc.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
    manifest['views'][view]={'file':view+'.png','sha256':hashlib.sha256((OUT/(view+'.png')).read_bytes()).hexdigest(),
        'resolution':[round(sc.render.resolution_x*sc.render.resolution_percentage/100),round(sc.render.resolution_y*sc.render.resolution_percentage/100)],
        'samples':sc.cycles.samples,'camera':sc.camera.name,'camera_matrix':[list(row) for row in sc.camera.matrix_world],
        'orthographic_scale':sc.camera.data.ortho_scale,'view_transform':sc.view_settings.view_transform,'exposure':sc.view_settings.exposure}
    manifest_path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
