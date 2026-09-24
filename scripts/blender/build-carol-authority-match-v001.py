"""Carol face/ear authority reconstruction; run using Blender background mode."""
import sys, json, math, hashlib, importlib.util, tempfile
from pathlib import Path
sys.dont_write_bytecode = True
import bpy, bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'assets/grimo/production/carol/blender/carol-face-ear-production-v003.blend'
OUTPUT = SOURCE.with_name('carol-face-ear-authority-match-v001.blend')
OUT = ROOT/'docs/production/carol/evidence/face-ear-authority-match-v001'
TMP = Path(tempfile.gettempdir())/'carol-authority-match-v001'
TMP.mkdir(exist_ok=True); OUT.mkdir(parents=True,exist_ok=True)
def load_module(name,file):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file))
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
util=load_module('ear_util','build-carol-ear-production-v002.py'); util.TMP=TMP
def table(rows,x):
    # Shape-preserving cubic Hermite interpolation of explicit sections.
    a=np.array(rows,float); xs=a[:,0]; ys=a[:,1:]
    dx=np.diff(xs); sec=np.diff(ys,axis=0)/dx[:,None]
    m=np.zeros_like(ys); m[0]=sec[0];m[-1]=sec[-1]
    for i in range(1,len(xs)-1):
        for j in range(ys.shape[1]):
            l,r=sec[i-1,j],sec[i,j]
            if l*r>0:
                w1=2*dx[i]+dx[i-1];w2=dx[i]+2*dx[i-1]
                m[i,j]=(w1+w2)/(w1/l+w2/r)
    i=max(0,min(len(xs)-2,int(np.searchsorted(xs,x))-1))
    t=max(0,min(1,(x-xs[i])/dx[i])); h=dx[i]
    return (2*t**3-3*t*t+1)*ys[i]+(t**3-2*t*t+t)*h*m[i]+(-2*t**3+3*t*t)*ys[i+1]+(t**3-t*t)*h*m[i+1]

# z, half-width, sagittal front, side-center X, rear X. Authority-derived
# controls: broad low cheeks, nearly flat chin, short muzzle, rounded cranium.
HEAD_SECTIONS=[
    (.225,.0,.205,.205,.205),(.233,.132,.135,.245,.365),
    (.25,.195,.090,.267,.428),(.28,.266,.046,.284,.485),
    (.32,.295,.010,.330,.529),(.36,.304,.004,.345,.556),
    (.38,.302,.012,.350,.568),(.412,.299,.033,.355,.580),
    (.46,.290,.034,.360,.585),(.51,.280,.048,.362,.580),
    (.56,.265,.077,.343,.566),(.61,.232,.126,.350,.541),
    (.66,.167,.209,.355,.496),(.69,.075,.300,.356,.410),
    (.700,.0,.356,.356,.356)]

def cube_directions():
    ids={}
    for axis in range(3):
        free=[a for a in range(3) if a!=axis]
        for fixed in [0,8]:
            for a in range(8):
                for b in range(8):
                    if axis==2 and fixed==0 and a>=4:continue
                    if axis==0 and fixed==8 and b<2:continue
                    for da,db in [(0,0),(1,0),(1,1),(0,1)]:
                        q=[0,0,0];q[axis]=fixed;q[free[0]]=a+da;q[free[1]]=b+db
                        ids.setdefault(tuple(q),Vector([c/4-1 for c in q]).normalized())
    return list(ids.values())

def rebuild_head():
    o=bpy.data.objects['CENTRAL_CHASSIS']; directions=cube_directions()
    assert len(directions)==351
    before=[v.co.copy() for v in o.data.vertices]
    for v,d in zip(o.data.vertices,directions):
        low=max(0,-d.z)
        z=.449+(.251*d.z if d.z>=0 else -.224*low**.65)
        if d.z<0:z+=.224*(low**.65-low**.95)*d.x*d.x
        w,f,cx,back=table(HEAD_SECTIONS,z)
        r=math.hypot(d.x,d.y); c=d.x/r if r>1e-8 else 0;s=d.y/r if r>1e-8 else 0
        # A broad oblique orbital surface gives actual Side eye width. The
        # nose/cheek center remains short; the rear is a rounded half ellipse.
        x=f+(cx-f)*(1-(-c)**1.4) if c<0 else cx+(back-cx)*c
        if c<0:
            y=w*s
            dy=abs(y)-.162;dz=z-.412
            weight=.96*math.exp(-(dy/.110)**6-(dz/.130)**6)*min(1,-d.x/.5)**2
            orbit=.148+.90*dy+.003*(dz/.0745)**2
            x=x*(1-weight)+orbit*weight
            x-=.033*math.exp(-(y/.075)**2-((z-.363)/.053)**2)*(-c)**4
        v.co=(x,w*s,z)
    # Carry only the short attachment strip halfway with its head boundary.
    for v in o.data.vertices[351:379]:
        neighbors=[]
        for e in o.data.edges:
            if v.index in e.vertices:
                other=e.vertices[0] if e.vertices[1]==v.index else e.vertices[1]
                if other<351:neighbors.append(other)
        if neighbors:v.co+=sum((o.data.vertices[j].co-before[j] for j in neighbors),Vector())/len(neighbors)*.55
    o.data.update()
    o['authority_match']='Explicit Front width / Side sagittal / oblique orbital cross-sections; one neutral 3D mesh'
    return before

def mesh(name,verts,faces,mats,indices=None,subdiv=0):
    o=bpy.data.objects.get(name)
    if o is None:
        o=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(o)
    old=o.data; m=bpy.data.meshes.new(name+' authority match')
    m.from_pydata(verts,[],faces);m.update()
    for mat in mats:m.materials.append(mat)
    for p in m.polygons:p.use_smooth=True;p.material_index=indices[p.index] if indices else 0
    bm=bmesh.new();bm.from_mesh(m);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(m);bm.free()
    o.data=m;o.modifiers.clear();o.vertex_groups.clear()
    if subdiv:
        mod=o.modifiers.new('Smooth authority sections','SUBSURF');mod.levels=subdiv;mod.render_levels=subdiv
    if old and old.users==0:bpy.data.meshes.remove(old)
    return o

def mat(name,color,rough=.45):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Subsurface Weight'].default_value=.04
    return m

def face_material():
    original=bpy.data.objects['CENTRAL_CHASSIS'].data.materials[0]
    m=original.copy();m.name='Carol cream and soft cheek blush'
    n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    geo=n.new('ShaderNodeNewGeometry')
    masks=[]
    for s in [-1,1]:
        sub=n.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=(.17,s*.248,.326);l.new(geo.outputs['Position'],sub.inputs[0])
        div=n.new('ShaderNodeVectorMath');div.operation='DIVIDE';div.inputs[1].default_value=(.18,.064,.058);l.new(sub.outputs[0],div.inputs[0])
        dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(div.outputs[0],dot.inputs[0]);l.new(div.outputs[0],dot.inputs[1])
        neg=n.new('ShaderNodeMath');neg.operation='MULTIPLY';neg.inputs[1].default_value=-1.8;l.new(dot.outputs['Value'],neg.inputs[0])
        exp=n.new('ShaderNodeMath');exp.operation='EXPONENT';l.new(neg.outputs[0],exp.inputs[0]);masks.append(exp.outputs[0])
    add=n.new('ShaderNodeMath');add.operation='ADD';l.new(masks[0],add.inputs[0]);l.new(masks[1],add.inputs[1])
    mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.78,.67,.61,1);mix.inputs[2].default_value=(.85,.32,.25,1);l.new(add.outputs[0],mix.inputs[0])
    weight=n.new('ShaderNodeAttribute');weight.attribute_name='face_tone'
    blend=n.new('ShaderNodeMixRGB');blend.inputs[1].default_value=p.inputs['Base Color'].default_value[:];l.new(weight.outputs['Fac'],blend.inputs[0]);l.new(mix.outputs[0],blend.inputs[2]);l.new(blend.outputs[0],p.inputs['Base Color'])
    l.new(blend.outputs[0],p.inputs['Emission Color'])
    em=n.new('ShaderNodeMath');em.operation='MULTIPLY';em.inputs[1].default_value=.30;l.new(weight.outputs['Fac'],em.inputs[0]);l.new(em.outputs[0],p.inputs['Emission Strength'])
    return m

def surface_tree():
    bpy.context.view_layer.update();o=bpy.data.objects['CENTRAL_CHASSIS'];ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return BVHTree.FromPolygons([v.co for v in ev.data.vertices],[list(p.vertices) for p in ev.data.polygons])

def rebuild_features(skin):
    tree=surface_tree()
    def x(y,z):
        h=tree.ray_cast(Vector((-2,y,z)),Vector((1,0,0)))[0]
        if h is None:raise RuntimeError(('off facial surface',y,z))
        return h.x
    pigment=mat('Carol approved eye pigment',(.04,.018,.012),.28)
    p=pigment.node_tree.nodes.get('Principled BSDF');p.inputs['Specular IOR Level'].default_value=.12;p.inputs['Coat Weight'].default_value=.12
    tex=pigment.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(TMP/'eye-authority-pigment.png'));tex.image.pack()
    pigment.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
    pigment.node_tree.links.new(tex.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.16
    brown=mat('Carol fine umber eyelid',(.095,.026,.017),.3)
    for side,sign in [('L',1),('R',-1)]:
        cy=sign*.162;cz=.412;verts=[(x(cy,cz)-.018,cy,cz)];uv=[(.5,.5)];N=96;R=16
        for k in range(1,R+1):
            r=k/R
            for j in range(N):
                a=2*math.pi*j/N
                # Slightly narrower crown, round fuller lower eye as authority.
                yy=.0685*r*math.cos(a)*(1-.045*math.sin(a))
                z=cz+.0745*r*math.sin(a);y=cy+sign*yy
                verts.append((x(y,z)-(.0015+.0165*(1-r*r)),y,z));uv.append(((1+r*math.cos(a))/2,(1+r*math.sin(a))/2))
        faces=[(0,1+j,1+(j+1)%N) for j in range(N)]
        for k in range(R-1):
            for j in range(N):
                a=1+k*N+j;b=1+k*N+(j+1)%N;faces.append((a,b,b+N,a+N))
        o=mesh('EYE_'+side,verts,faces,[pigment]);layer=o.data.uv_layers.new(name='Approved optical pigment')
        for poly in o.data.polygons:
            for i in poly.loop_indices:layer.data[i].uv=uv[o.data.loops[i].vertex_index]
        verts=[]
        for r,d in [(1,.002),(1.025,.003),(1.062,.0018),(1.11,-.001)]:
            for j in range(N):
                a=2*math.pi*j/N;y=cy+sign*.0685*r*math.cos(a)*(1-.045*math.sin(a));z=cz+.0745*r*math.sin(a)
                verts.append((x(y,z)-d,y,z))
        faces=[];mi=[]
        for k in range(3):
            for j in range(N):
                a=k*N+j;b=k*N+(j+1)%N;faces.append((a,b,b+N,a+N));mi.append(1 if k==0 else 0)
        lid=mesh('EYELID_'+side,verts,faces,[skin,brown],mi)
        att=lid.data.attributes.new('face_tone','FLOAT','POINT')
        for v in att.data:v.value=1
    # Tiny rounded triangular nose, surface-owned closed double-arc mouth.
    nose=bpy.data.objects['NOSE'];nose.location.x=x(0,.378)-.001
    for v in nose.data.vertices:v.co.x*=.76
    nose.data.materials.clear();nose.data.materials.append(mat('Carol chocolate nose',(.054,.020,.016),.31))
    mouthmat=mat('Carol closed smile umber',(.24,.034,.020),.54)
    for name in ['MOUTH_closed','PHILTRUM']:
        o=bpy.data.objects[name];o.data.materials.clear();o.data.materials.append(mouthmat);o.data.splines.clear()
        o.data.bevel_depth=.0019;o.data.bevel_resolution=4;o.data.resolution_u=12
        for sign in ([-1,1] if name=='MOUTH_closed' else [1]):
            sp=o.data.splines.new('POLY');sp.points.add(32)
            for i,pt in enumerate(sp.points):
                t=i/32
                if name=='MOUTH_closed':
                    y=sign*(3*(1-t)**2*t*.003+3*(1-t)*t*t*.039+t**3*.0455)
                    z=(1-t)**3*.362+3*(1-t)**2*t*.340+3*(1-t)*t*t*.339+t**3*.357
                else:y=0;z=.369*(1-t)+.362*t
                pt.co=(x(y,z)-.002,y,z,1)
    return {'eye_width_H':.137,'eye_height_H':.149,'eye_spacing_H':.324,'eye_center_Z_H':.412,
            'sagittal_samples':[[z,x(0,z)] for z in [.25,.28,.32,.35,.378,.412,.46,.51,.56]]}

def rebuild_ears():
    data=json.loads((OUT/'measurements.json').read_text());rows=data['ear_stations']
    # Closed root and rounded distal cap; Top breadth is independent of Front
    # drop, and pink/brown share one continuous sculpted containment surface.
    rows=[dict(u=-.012,top=.028,bottom=-.033,front=.031,back=.027,pink_top=None,pink_bottom=None)]+rows[2:]
    rows.append(dict(u=.401,top=-.154,bottom=-.158,front=.002,back=.006,pink_top=None,pink_bottom=None))
    brown=mat('Carol ear warm cocoa',(.205,.058,.026),.67)
    pink=mat('Carol ear recessed coral',(.98,.32,.24),.56)
    n=pink.node_tree.nodes;l=pink.node_tree.links;p=n.get('Principled BSDF')
    attr=n.new('ShaderNodeAttribute');attr.attribute_name='cup_blush'
    mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(1,.42,.34,1);mix.inputs[2].default_value=(.72,.075,.050,1);l.new(attr.outputs['Fac'],mix.inputs[0]);l.new(mix.outputs[0],p.inputs['Base Color'])
    stations=[[r[k] for k in ['u','top','bottom','front','back']] for r in rows]
    inner=[[.020,-.041,-.041],[.023,-.030,-.058],[.030,-.057,-.087],[.045,-.094,-.126],
        [.070,-.117,-.166],[.099,-.132,-.194],[.132,-.138,-.216],[.164,-.141,-.232],
        [.197,-.140,-.239],[.229,-.137,-.241],[.262,-.129,-.237],[.294,-.123,-.226],
        [.323,-.124,-.213],[.349,-.133,-.192],[.360,-.151,-.179],[.365,-.166,-.166]]
    # Resolve both rounded ends of the inner ear with extra longitudinal rings.
    us=sorted(set([r['u'] for r in rows]+list(np.linspace(.02,.39,70))+[.020,.022,.023,.360,.362,.364,.365]))
    verts=[];blush=[];NC=24
    for u in us:
        top,bottom,front,back=table(stations,u);h=top-bottom;mid=(top+bottom)/2
        phi,plo=table(inner,u)
        plo=max(bottom+h*.045,min(top-h*.10,plo));phi=max(plo+.0001,min(top-h*.05,phi))
        rim=plo-bottom
        section=[(back*math.sin(math.pi*j/8),mid+h/2*math.cos(math.pi*j/8)) for j in range(9)]
        zs=[bottom+rim*.15,bottom+rim*.5,plo]+[plo+(phi-plo)*v for v in [.1,.3,.5,.7,.9]]+[phi]+[phi+(top-phi)*v for v in [.08,.24,.44,.66,.85,.96]]
        for z in zs:
            xx=-front*math.sqrt(max(0,1-((z-mid)/(h/2))**2))
            t=(z-plo)/max(.0001,phi-plo)
            if 0<t<1:xx+=min(.010,(phi-plo)*.12)*math.sin(math.pi*t)**2
            section.append((xx,z))
        assert len(section)==NC
        verts.extend((x,u,z) for x,z in section)
        blush.extend([0]*12+[.05,.10,.18,.32,.58,.9]+[1]*6)
    faces=[];mi=[]
    for i in range(len(us)-1):
        for j in range(NC):
            a=i*NC+j;b=i*NC+(j+1)%NC;faces.append((a,b,b+NC,a+NC));mi.append(1 if 11<=j<=16 and .020<=us[i]<.365 else 0)
    faces.extend([tuple(reversed(range(NC))),tuple((len(us)-1)*NC+j for j in range(NC))]);mi.extend([0,0])
    sweep=math.radians(35);root=Vector((.386,.235,.579))
    for side,sign in [('L',1),('R',-1)]:
        points=[(root.x+x*math.cos(sweep)+u*math.sin(sweep),sign*(root.y-x*math.sin(sweep)+u*math.cos(sweep)),root.z+z) for x,u,z in verts]
        o=mesh('EAR_'+side,points,faces,[brown,pink],mi,2)
        att=o.data.attributes.new('cup_blush','FLOAT','POINT')
        for a,v in zip(att.data,blush):a.value=v
        o['authority_match']='Front/Top raster measured sections; closed shell with recessed material-continuous cup'
        o['root_H']=list(root);o['sweep_degrees']=35
    return {'root_H':list(root),'sweep_degrees':35,'section_count':len(us),'section_vertices':NC,'length_H':.413}

def setup():
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
    s.render.threads_mode='FIXED';s.render.threads=12;s.render.use_compositing=False;s.render.use_sequencer=False
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=-1.2;s.view_settings.gamma=1
    # Broad studio illumination reveals volume without the inherited near-black
    # under-jaw band. The same setup is applied to source and candidate evidence.
    s.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.30,.30,.30,1)
    for name,energy in [('key',310),('fill',260),('low fill',240),('rim',170)]:
        bpy.data.objects[name].data.energy=energy

def geometry_record(prefix):
    bpy.context.view_layer.update();o=bpy.data.objects['CENTRAL_CHASSIS'];ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.data
    g=o.vertex_groups['HEAD'].index
    valid={v.index for v in m.vertices if any(a.group==g and a.weight>.75 for a in v.groups)}
    edges=[(e.vertices[0],e.vertices[1]) for e in m.edges if set(e.vertices)<=valid]
    samples=[]
    for z in np.linspace(.235,.690,183):
        pts=[]
        for a,b in edges:
            pa,pb=m.vertices[a].co,m.vertices[b].co
            if (pa.z-z)*(pb.z-z)<=0 and abs(pb.z-pa.z)>1e-9:
                t=(z-pa.z)/(pb.z-pa.z);pts.append(pa.lerp(pb,t))
        if pts:samples.append([float(z),min(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)])
    features={}
    for name in ['EYE_L','EYE_R','NOSE']:
        ob=bpy.data.objects[name];pts=[ob.matrix_world@v.co for v in ob.data.vertices]
        features[name]={'min':[min(p[i] for p in pts) for i in range(3)],'max':[max(p[i] for p in pts) for i in range(3)]}
    (TMP/(prefix+'-geometry.json')).write_text(json.dumps({'head_sections':samples,'features':features},indent=2))

def renders(prefix):
    setup();geometry_record(prefix);face={'CENTRAL_CHASSIS','EYE_L','EYE_R','EYELID_L','EYELID_R','NOSE','MOUTH_closed','PHILTRUM'}
    for view,d in [('front',(-4,0,0)),('side',(0,-4,0)),('3q',(-3,-3,.3)),('top',(0,0,4))]:
        util.render(prefix+'-face-'+view,d,(.285,0,.457),.64,face,size=(900,900))
    attached={o.name for o in bpy.data.objects if o.type in {'MESH','CURVE'}}
    for view,d in [('front',(-4,0,0)),('side',(0,-4,0)),('3q',(-3,-3,1.2))]:
        util.render(prefix+'-attached-'+view,d,(.51,0,.38),1.34,attached,size=(1100,1100))
    sw=math.radians(35);front=Vector((-math.cos(sw),math.sin(sw),0));side=Vector((math.sin(sw),math.cos(sw),0))
    root=Vector((.386,.235,.579)) if prefix=='candidate' else util.ROOT_POS
    center=root+side*.2+Vector((0,0,-.104))
    for v,d in [('front',front*4),('side',-side*4),('top',Vector((0,0,4))),('3q',front*3-side*2+Vector((0,0,.65)))]:
        util.render(prefix+'-ear-'+v,d,center,.48,{'EAR_L'},size=(850,850),roll=-math.pi/2-sw if v=='top' else 0)
    util.render(prefix+'-ear-side-elevated',side*4+Vector((0,0,1.05)),center,.54,{'EAR_L'},size=(850,850),roll=math.radians(11))

def build():
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));bpy.context.scene.frame_set(1)
    frozen={o.name:util.snapshot(o) for o in bpy.data.objects}
    before=rebuild_head();skin=face_material();head=bpy.data.objects['CENTRAL_CHASSIS'];head.data.materials.append(skin)
    att=head.data.attributes.new('face_tone','FLOAT','POINT')
    for v,a in zip(head.data.vertices,att.data):
        t=max(0,min(1,(.40-v.co.z)/.15))*max(0,min(1,(v.co.x-.22)/.24))
        a.value=(1-t*t*(3-2*t)) if v.index<351 else 0
    for p in head.data.polygons:
        if all(i<379 for i in p.vertices):p.material_index=1
    features=rebuild_features(skin);ears=rebuild_ears();setup();provenance()
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    changed=[n for n in frozen if util.snapshot(bpy.data.objects[n])!=frozen[n]]
    checks={n:util.mesh_check(bpy.data.objects[n]) for n in ['CENTRAL_CHASSIS','EAR_L','EAR_R']}
    validation={'source_commit':'656d6510b6ca81205cca1fced46d176f10d7aca7','changed_objects':changed,'features':features,'ears':ears,'mesh_checks':checks,
        'non_head_chassis_vertices_unchanged':all(tuple(v.co)==tuple(before[v.index]) for v in head.data.vertices if v.index>=379),
        'head_sections':HEAD_SECTIONS,'human_status':'PENDING'}
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print('VALIDATION',json.dumps(validation));reload_validate();renders('candidate')

def provenance():
    s=bpy.context.scene
    for key in ['selected_candidate','human_geometry_gate','static_visual_status','motion_preflight','executor_visual_precheck','motion_clearance','candidate_role']:
        if key in s:del s[key]
    s['stage']='READY_FOR_HUMAN_FACE_EAR_AUTHORITY_MATCH_REVIEW'
    s['selected_candidate']='carol-face-ear-authority-match-v001'
    s['human_geometry_gate']='PENDING_HUMAN_PERCEPTUAL_REVIEW'
    s['candidate_role']='Face / ear reconstruction candidate; not an approved authority'
    s['source_commit']='656d6510b6ca81205cca1fced46d176f10d7aca7'
    for side in ['L','R']:
        ear=bpy.data.objects['EAR_'+side]
        for key in ['ear_controls','root_position_H']:
            if key in ear:del ear[key]
        ear['controls_status']='Neutral reconstructed shell; legacy provisional shape keys removed; rig outside scope'
        eye=bpy.data.objects['EYE_'+side]
        for key in ['surface_frame','normal_relief_H']:
            if key in eye:del eye[key]
        eye['surface_model']='Raycast-conformal orbital patch; 0.018 H center relief, 0.0015 H edge relief'
    bpy.data.objects['CENTRAL_CHASSIS']['architecture']='Authority-derived cranial sections and oblique orbital field; short attachment strip; original torso controls'
    for im in bpy.data.images:
        if im.name.startswith('eye-authority-pigment'):
            im.filepath='//carol-approved-eye-pigment.png'

def reload_validate():
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    source={o.name:util.snapshot(o) for o in bpy.data.objects}
    body=[tuple(v.co) for v in bpy.data.objects['CENTRAL_CHASSIS'].data.vertices][379:]
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))
    actual={o.name:util.snapshot(o) for o in bpy.data.objects}
    changed=sorted(n for n in source if actual[n]!=source[n])
    allowed=sorted(['CENTRAL_CHASSIS','EAR_L','EAR_R','EYE_L','EYE_R','EYELID_L','EYELID_R','NOSE','MOUTH_closed','PHILTRUM'])
    assert set(source)==set(actual) and changed==allowed
    assert body==[tuple(v.co) for v in bpy.data.objects['CENTRAL_CHASSIS'].data.vertices][379:]
    checks={n:util.mesh_check(bpy.data.objects[n]) for n in ['CENTRAL_CHASSIS','EAR_L','EAR_R']}
    for c in checks.values():
        assert c['finite'] and c['outward_normals'] and c['nonmanifold_edges']==0 and c['nonadjacent_triangle_intersections']==0
    pigment=[im for im in bpy.data.images if im.name.startswith('eye-authority-pigment')]
    assert len(pigment)==1 and pigment[0].packed_file
    manifest=json.loads((ROOT/'assets/grimo/source/carol/approved-3d/authority.json').read_text())
    authority_checks={}
    for entry in manifest['authorityOrder']:
        p=ROOT/entry['path'];raw=p.read_bytes()
        if p.suffix=='.md':raw=raw.replace(b'\r\n',b'\n')
        authority_checks[entry['path']]=hashlib.sha256(raw).hexdigest()==entry['sha256'].lower()
    assert all(authority_checks.values())
    v=json.loads((OUT/'validation.json').read_text())
    v['mesh_checks']=checks
    v['save_reload']={'passed':True,'changed_geometry_objects':changed,'preserved_object_snapshot_count':len(source)-len(changed),'torso_controls_379_onward_unchanged':True,'eye_pigment_packed':True,'authority_manifest_hashes':authority_checks,'blend_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}
    v['presentation_changes']={'studio_lights':'key 310 W, fill 260 W, low fill 240 W, rim 170 W','world_gray':.30,'exposure':-1.2,'comparison':'Identical source and candidate settings; not included in geometry snapshot equality.'}
    (OUT/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
    print('SAVE_RELOAD_PASS',json.dumps(v['save_reload']))

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    if 'source' in args:
        bpy.ops.wm.open_mainfile(filepath=str(SOURCE));renders('source')
    else:build()
