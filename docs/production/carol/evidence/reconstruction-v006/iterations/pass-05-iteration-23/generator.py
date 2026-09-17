"""Carol reconstruction from the six approved plates; no historical mesh imports.

Blender +Z up, front -Y. The retained v005 asset is not opened. All geometry is
authored here. Measurement uncertainty and contradictory drawings stay visible.
"""
import argparse, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector, Quaternion
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/production/carol/evidence/reconstruction-v006'
SRC = ROOT / 'assets/grimo/source/carol/approved-3d'
P = argparse.ArgumentParser()
P.add_argument('--pass-number', type=int, default=1)
P.add_argument('--iteration', type=int, default=1)
P.add_argument('--resolution', type=int, default=768)
P.add_argument('--views', default='front,side,back,top,3q-left,3q-right')
P.add_argument('--camera-fit', default='')
P.add_argument('--profile-fit', default='')
ARGS = P.parse_args(sys.argv[sys.argv.index('--') + 1:])
assert (ROOT/'docs/production/carol/carol-reference-measurements.json').is_file(), 'Measure references before modeling'
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
SC = bpy.context.scene
COL = bpy.data.collections.new('CAROL_V006_AUTHORED'); SC.collection.children.link(COL)
ROOTOBJ = bpy.data.objects.new('Carol_Reconstruction_v006', None); COL.objects.link(ROOTOBJ)
ROOTOBJ['authority'] = 'Six approved individual plates. No B or historical geometry.'
LANDMARKS = {}

def mat(name, color, rough=.65):
    m = bpy.data.materials.new(name); m.diffuse_color = (*color, 1); m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value = (*color,1)
    bs.inputs['Roughness'].default_value = rough
    return m

CLAY=mat('Neutral clay',(.53,.53,.53),.82)
CREAM=mat('Face cream',(1,.83,.73)); BROWN=mat('Warm cocoa',(.19,.076,.047),.46)
PINK=mat('Ear coral',(.95,.31,.26)); DARK=mat('Eye deep brown',(.028,.009,.014),.13)
WHITE=mat('Cloud warm white',(.92,.9,1),.58); BLUE=mat('Cloud periwinkle',(.34,.43,.91),.62)
LILAC=mat('Cloud pale lilac',(.64,.65,.98),.62)
GOLD=mat('Motif warm gold',(1,.65,.12),.28); GLINT=mat('Eye glints',(1,.98,.94),.12)
RED=mat('Mouth interior',(.48,.025,.025),.58); TONGUE=mat('Tongue coral',(1,.20,.17),.55)

def mesh(name, vs, fs, material=CLAY):
    d=bpy.data.meshes.new(name); d.from_pydata(vs,[],fs); d.update()
    bm=bmesh.new(); bm.from_mesh(d); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(d); bm.free()
    ob=bpy.data.objects.new(name,d); COL.objects.link(ob); ob.parent=ROOTOBJ; d.materials.append(material)
    for f in d.polygons: f.use_smooth=True
    return ob

def param_surface(name, fn, nu=80, nv=48, material=CLAY):
    # Closed latitude surface with unique poles, avoiding degenerate pole quads.
    vs=[fn(0,0)]; fs=[]
    for j in range(1,nv):
        v=math.pi*j/nv
        for i in range(nu): vs.append(fn(math.tau*i/nu,v))
    vs.append(fn(0,math.pi)); end=len(vs)-1
    for i in range(nu): fs.append((0,1+(i+1)%nu,1+i))
    for j in range(nv-2):
        a=1+j*nu; b=a+nu
        for i in range(nu): fs.append((a+i,a+(i+1)%nu,b+(i+1)%nu,b+i))
    a=1+(nv-2)*nu
    for i in range(nu): fs.append((a+i,a+(i+1)%nu,end))
    return mesh(name,vs,fs,material)

def ellipsoid(name,c,r,material=CLAY, power=1):
    def signed(t): return math.copysign(abs(t)**power,t)
    return param_surface(name,lambda u,v:(c[0]+r[0]*signed(math.sin(v)*math.cos(u)),c[1]+r[1]*signed(math.sin(v)*math.sin(u)),c[2]+r[2]*signed(math.cos(v))),64,40,material)

def marker(name,p): LANDMARKS[name]=list(p)

# Per-depth sections: Y, half-width, floor, crown. Deliberate two-mass plan.
# These are primary design parameters, not copies of A's ellipsoid banks.
SECTIONS=np.array([
 [-1.93,.05,.88,1.65],[-1.74,.63,.48,2.10],[-1.44,1.01,.35,2.63],
 [-1.12,1.20,.32,2.80],[-.75,1.27,.31,2.79],[-.34,1.12,.31,2.66],
 [.00,.92,.32,2.54],[.35,.85,.31,2.44],[.65,.94,.31,2.36],
 [1.00,1.06,.32,2.27],[1.35,1.07,.35,2.13],[1.63,.83,.44,1.91],
 [1.83,.35,.70,1.58],[1.88,.01,1.11,1.14]])

def section(y):
    if ARGS.pass_number < 2:return [float(np.interp(y,SECTIONS[:,0],SECTIONS[:,i])) for i in (1,2,3)]
    j=int(np.clip(np.searchsorted(SECTIONS[:,0],y)-1,0,len(SECTIONS)-2));t=(y-SECTIONS[j,0])/(SECTIONS[j+1,0]-SECTIONS[j,0])
    values=[]
    for axis in (1,2,3):
        p0=SECTIONS[max(0,j-1),axis];p1=SECTIONS[j,axis];p2=SECTIONS[j+1,axis];p3=SECTIONS[min(len(SECTIONS)-1,j+2),axis]
        values.append(float(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)))
    return values

def chassis():
    def surf(u,v):
        y=-1.93+(1-math.cos(v))*.5*3.81
        w,lo,hi=section(y); mid=(lo+hi)/2; rz=(hi-lo)/2
        return (w*math.cos(u),y,mid+rz*math.sin(u))
    ob=param_surface('Fleece_Chassis_SectionLoft',surf,112,128,BLUE)
    ob['construction']='Continuous non-ellipsoidal longitudinal sections, two plan masses and midbody indentation'
    if ARGS.pass_number >= 2:
        cutter=ellipsoid('TEMP_head_insertion_channel',(0,-1.80,1.15),(1.10,.82,.63),CLAY,.80)
        mod=ob.modifiers.new('Volumetric head opening across front and side','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
        bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(cutter,do_unlink=True)
    return ob

def cheek_width(z):
    return .86*(1+.085*math.exp(-((z-.98)/.20)**2)-.065*math.exp(-((z-1.49)/.20)**2))

def face_y(x,z):
    # Broad cheek plane, tucked temples and a short muzzle; shared by the skin
    # and every attached feature, so relief is geometry rather than a decal.
    q=max(0,1-abs(x/cheek_width(z))**2-abs((z-1.15)/.57)**2.5)
    cheek=.070*math.exp(-((abs(x)-.48)/.27)**2-((z-.98)/.22)**2)
    muzzle=.095*math.exp(-((x/.28)**2+((z-1.08)/.16)**2))
    return -1.20-(1.00+cheek+muzzle)*q**.28

def face():
    def fn(u,v):
        z=1.15+.57*math.copysign(abs(math.cos(v))**.8,math.cos(v))
        x=cheek_width(z)*math.sin(v)*math.cos(u)
        q=max(0,1-abs(x/cheek_width(z))**2.0-abs((z-1.15)/.57)**2.5)
        front=math.sin(u)<0
        y=face_y(x,z) if front else -1.20+.28*math.sqrt(q)
        return x,y,z
    ob=param_surface('Head_Volumetric_Cheeks_Jaw',fn,128,80,CREAM)
    ob['full_depth']='See geometry-audit.json for measured final cheek/jaw sections'
    marker('face_left',(-cheek_width(1.15),-1.20,1.15)); marker('face_right',(cheek_width(1.15),-1.20,1.15))
    marker('face_top',(0,-1.20,1.72)); marker('face_bottom',(0,-1.20,.58))
    return ob

def curved_patch(name,c,rx,rz,bulge,material,tilt=0):
    n=96; rings=20; vs=[]; fs=[]
    for k in range(rings+1):
        r=k/rings
        for j in range(1 if k==0 else n):
            t=math.tau*j/n; a=rx*r*math.cos(t); b=rz*r*math.sin(t)
            x=c[0]+a*math.cos(tilt)+b*math.sin(tilt); z=c[1]-a*math.sin(tilt)+b*math.cos(tilt)
            vs.append((x,face_y(x,z)-.006-bulge*(1-r*r),z))
    for j in range(n):fs.append((0,1+j,1+(j+1)%n))
    for k in range(1,rings):
        a=1+(k-1)*n;b=a+n
        for j in range(n):fs.append((a+j,b+j,b+(j+1)%n,a+(j+1)%n))
    ob=mesh(name,vs,fs,material);m=ob.modifiers.new('Integral closed backing','SOLIDIFY');m.thickness=.015
    return ob

def tube(name,coords,r,material):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=4;d.resolution_u=24;d.use_fill_caps=True
    s=d.splines.new('BEZIER');s.bezier_points.add(len(coords)-1)
    for p,co in zip(s.bezier_points,coords):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
    ob=bpy.data.objects.new(name,d);COL.objects.link(ob);ob.parent=ROOTOBJ;d.materials.append(material)
    return ob

def facial_features():
    for label,x,tilt in [('L',-.443,-.07),('R',.514,.07)]:
        z=1.145;rx=.178;rz=.208
        ob=curved_patch('Eye_'+label,(x,z),rx,rz,.043,DARK,tilt)
        marker('eye_center_'+label,(x,face_y(x,z)-.049,z))
        for key,xx,zz in [('left',x-rx,z),('right',x+rx,z),('top',x,z+rz),('bottom',x,z-rz)]:marker('eye_'+label+'_'+key,(xx,face_y(xx,zz),zz))
        attr=ob.data.color_attributes.new(name='Amber_Iris',type='FLOAT_COLOR',domain='POINT')
        for i,v in enumerate(ob.data.vertices):
            xx=(v.co.x-x)/rx;zz=(v.co.z-z)/rz
            a=math.exp(-((xx/.76)**2+((zz+.46)/.43)**2)*1.2)
            b=math.exp(-((xx/.52)**2+((zz+.68)/.24)**2)*1.5)
            attr.data[i].color=(.028+.25*a+.58*b,.009+.085*a+.31*b,.014+.022*a+.045*b,1)
        m=DARK.copy();m.name='Amber_eye_'+label;ob.data.materials[0]=m
        nd=m.node_tree.nodes.new('ShaderNodeVertexColor');nd.layer_name='Amber_Iris';m.node_tree.links.new(nd.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
        # Glints belong to lookdev; no raised highlight geometry in clay.
    ellipsoid('Nose',(0.025,face_y(.025,1.128)-.019,1.128),(.049,.038,.025),BROWN)
    marker('nose_center',(.025,face_y(.025,1.128)-.03,1.128))
    # Rounded triangular smile opening, with an actual recessed backing.
    head=bpy.data.objects.get('Head_Volumetric_Cheeks_Jaw')
    def mouth_volume(u,v):
        x=.025+.15*math.sin(v)*math.cos(u)
        t=math.cos(v);z=1.035+(.025 if t>0 else .19)*t
        return x,face_y(x,z)+.055+.12*math.sin(v)*math.sin(u),z
    cutter=param_surface('TEMP_mouth_cavity',mouth_volume,80,48)
    mod=head.modifiers.new('Recessed smile opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
    bpy.context.view_layer.objects.active=head;bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
    # Interior is physically behind the skin, never a raised circular patch.
    ellipsoid('Mouth_interior',(.025,face_y(.025,.96)+.14,.962),(.149,.042,.122),RED)
    ellipsoid('Tongue',(.025,face_y(.025,.906)+.080,.906),(.087,.024,.057),TONGUE)
    smile=[(-.125,1.067),(-.113,1.032),(-.072,1.026),(.025,1.079),(.113,1.026),(.16,1.032),(.175,1.067)]
    tube('Smile_lip',[(x,face_y(x,z)-.009,z) for x,z in smile],.0065,RED)
    tube('Philtrum',[(.025,face_y(.025,z)-.010,z) for z in [1.112,1.095,1.079]],.0055,BROWN)
    for label,x in [('L',-.125),('R',.175)]:marker('mouth_corner_'+label,(x,face_y(x,1.067)-.01,1.067))


def ears():
    for sign,label in [(-1,'L'),(1,'R')]:
        # Broad drooping spoon, independently curved front bowl and thick convex rear.
        n=80;rings=24;vs=[];fs=[]
        for back in [False,True]:
            for k in range(rings+1):
                r=k/rings
                for j in range(1 if k==0 else n):
                    a=math.tau*j/n;along=r*math.cos(a);up=r*math.sin(a)
                    t=(along+1)/2
                    # High narrow root, descending broad bowl, rounded outer tip.
                    x=.82+.83*t
                    z=1.46-.32*t-.075*math.sin(math.pi*t)+.255*up*(.58+.60*t)
                    y=-1.72+.84*t-.075*math.sin(math.pi*t)+.20*up
                    y+= .105*math.sqrt(max(0,1-r*r))+.020 if back else -.040+.105*(1-r*r)-.070*math.exp(-((up-.40)/.32)**2)*(1-r*r)
                    vs.append((sign*x,y,z))
        count=1+rings*n
        for back in [0,1]:
            base=back*count
            for j in range(n):fs.append((base,base+1+j,base+1+(j+1)%n))
            for k in range(1,rings):
                a=base+1+(k-1)*n;b=a+n
                for j in range(n):fs.append((a+j,b+j,b+(j+1)%n,a+(j+1)%n))
        a=count-n
        for j in range(n):fs.append((a+j,a+(j+1)%n,count+a+(j+1)%n,count+a+j))
        ob=mesh('Ear_Bowl_'+label,vs,fs,BROWN);ob.data.materials.append(PINK)
        for f in ob.data.polygons:
            if all(i<count for i in f.vertices):
                p=f.center
                # Material assignment follows radial inset and lower bowl.
                ids=f.vertices; center=sum((Vector(vs[i]) for i in ids),Vector())/len(ids)
                xx=(abs(center.x)-1.235)/.415;t=(xx+1)/2
                zz=(center.z-1.46+.32*t+.075*math.sin(math.pi*t))/(.255*(.58+.60*t))
                if xx*xx+zz*zz < .75 and zz<.35:f.material_index=1
        marker('ear_root_'+label,(sign*.82,-1.72,1.46));marker('ear_tip_'+label,(sign*1.65,-.88,1.14))
        ellipsoid('Ear_root_'+label,(sign*.79,-1.60,1.42),(.07,.16,.085),BROWN)

def hooves():
    for y,region in [(-1.20,'front'),(1.24,'rear')]:
        for sign,label in [(-1,'L'),(1,'R')]:
            c=(sign*.53-.065,y,.235);vs=[];fs=[];n=80
            # Actual level sole and gently tapered wall, with paired toe relief.
            levels=[(.008,.68),(.020,.82),(.075,.96),(.16,1),(.27,.96),(.39,.85),(.46,.68)]
            for z,radius in levels:
                for i in range(n):
                    u=math.tau*i/n
                    x=.265*radius*math.cos(u)
                    yy=.318*radius*math.sin(u)
                    cleft=math.exp(-(x/.042)**2)*max(0,-math.sin(u))**6
                    yy+=.055*cleft*max(0,1-z/.34)
                    vs.append((c[0]+x,c[1]+yy,z))
            fs.append(tuple(reversed(range(n))))
            for j in range(len(levels)-1):
                for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
            fs.append(tuple((len(levels)-1)*n+i for i in range(n)))
            ob=mesh('Hoof_'+region+'_'+label,vs,fs,BROWN)
            for f in ob.data.polygons:
                if len(f.vertices)>4:f.use_smooth=False
            bevel=ob.modifiers.new('Rounded sole and wall transitions','BEVEL');bevel.width=.028;bevel.segments=3
            ellipsoid('Leg_'+region+'_'+label,(c[0],y,.46),(.19,.22,.25),CREAM,.72)
            marker('hoof_'+region+'_'+label,(c[0],c[1],.17))

# Each cluster is a closed cloud volume with asymmetric lobes on a shared core.
# Circular hierarchy lives in a local tangent frame, not an equal-sphere grid.
CLUSTERS=[]
def cloud(name,c,r,normal,seed,material=WHITE):
    n=Vector(normal).normalized(); e=Vector((0,0,1)).cross(n)
    if e.length<.1:e=Vector((1,0,0))
    e.normalize();f=n.cross(e).normalized()
    # Recess fillers are quiet domes. Only the major groups carry scallops;
    # repeating a miniature flower on every filler obscured the body hierarchy.
    secondary=name.startswith(('FL_BRIDGE_','FL_BLUE_','FL_BELLY_'))
    rng=np.random.default_rng(seed);count=4+seed%3
    angles=[math.tau*i/count+float(rng.uniform(-.2,.2)) for i in range(count)]
    lobes=[(np.array([.04,-.02,.14]),.79)]
    for a in angles:
        reach=float(rng.uniform(.43,.51));rad=float(rng.uniform(.47,.56))
        lobes.append((np.array([reach*math.cos(a),reach*math.sin(a),float(rng.uniform(-.04,.14))]),rad))
    if name=='FL_TAIL':
        # Rounded lobes in all three dimensions; a tangent-plane flower would
        # become a thin coin from Side and would not be a true rear organ.
        lobes=[(np.array([0,0,0]),.68),
               (np.array([-.42,.10,.04]),.56),(np.array([.40,-.05,.04]),.57),
               (np.array([.02,.41,.03]),.55),(np.array([-.06,-.40,.04]),.55),
               (np.array([.02,.04,.42]),.56),(np.array([0,-.06,-.35]),.52)]
    elif secondary:
        lobes=[(np.array([0,0,0]),.98)]
    # Author actual ellipsoidal lobe surfaces, then union their intersections.
    # A ray-envelope approximation made the former flowers stretch into scales.
    vs=[];fs=[];nu=32;nv=20
    for center,rad in lobes:
        base=len(vs)
        def point(u,v):
            d=np.array([math.sin(v)*math.cos(u),math.sin(v)*math.sin(u),math.cos(v)])
            q=center+rad*d
            return tuple(Vector(c)+e*(r[0]*q[0])+f*(r[1]*q[1])+n*(r[2]*q[2]*(1 if secondary else 1.12)))
        vs.append(point(0,0))
        for j in range(1,nv):
            for i in range(nu):vs.append(point(math.tau*i/nu,math.pi*j/nv))
        end=len(vs);vs.append(point(0,math.pi))
        for i in range(nu):fs.append((base,base+1+(i+1)%nu,base+1+i))
        for j in range(nv-2):
            a=base+1+j*nu;b=a+nu
            for i in range(nu):fs.append((a+i,a+(i+1)%nu,b+(i+1)%nu,b+i))
        a=base+1+(nv-2)*nu
        for i in range(nu):fs.append((a+i,a+(i+1)%nu,end))
    ob=mesh(name,vs,fs,material);ob['cluster_id']=name
    ob['scale_hierarchy']='chassis / unequal volumetric cloud lobes / recess domes'
    CLUSTERS.append({'id':name,'center':c,'radii':r,'normal':normal,'primitive_count':len(lobes),'seed':seed})
    return ob

def fleece():
    # Front-defined major clusters. Y placement follows curvature; face remains open.
    rows=[
      ('crown_L',(-.27,-.86,2.77),(.36,.29,.33)),('crown_R',(.33,-.68,2.70),(.34,.30,.35)),
      ('crown_center',(-.02,-1.08,2.52),(.45,.33,.30)),
      ('forehead_R',(.36,-1.93,2.06),(.42,.36,.30)),('forehead_L',(-.18,-1.98,1.96),(.35,.31,.30)),
      ('forehead_edge_R',(.79,-1.69,1.91),(.27,.29,.25)),('forehead_edge_L',(-.66,-1.75,1.79),(.26,.24,.25)),
      ('cheek_L_top',(-.86,-1.50,1.46),(.18,.22,.25)),('cheek_L',(-.88,-1.49,1.13),(.17,.24,.24)),
      ('cheek_L_low',(-.80,-1.51,.83),(.23,.22,.23)),
      ('cheek_R_top',(.94,-1.46,1.47),(.18,.24,.24)),('cheek_R',(.94,-1.46,1.13),(.18,.23,.24)),
      ('cheek_R_low',(.84,-1.51,.83),(.24,.23,.24)),
      ('chin_L',(-.48,-1.57,.57),(.29,.24,.27)),('chin_C',(.02,-1.58,.48),(.29,.21,.26)),('chin_R',(.53,-1.54,.58),(.30,.24,.25)),
      ('moon_lower',(-1.26,-.88,1.48),(.28,.34,.28)),('outer_R', (1.27,-.88,1.56),(.29,.35,.26)),
      ('outer_L_low',(-1.19,-.92,.70),(.28,.27,.28)),('outer_R_low',(1.19,-.92,.70),(.29,.28,.27))]
    for i,(name,c,r) in enumerate(rows):cloud('FL_FRONT_'+name,c,r,(0,-1,.12),100+i)
    # Curved blue recess banks, scale distinct from broad foreground whites.
    for sign in [-1,1]:
        for i,(y,z,x,r) in enumerate([(-.8,2.40,.83,.29),(-.41,2.33,.90,.28),(-.13,2.13,.92,.26),(.30,2.03,.77,.30),(.72,2.01,.77,.30),(1.13,1.91,.80,.30)]):
            cloud(f'FL_BLUE_{sign}_{i}',(sign*x,y,z),(r,r*.98,r*.75),(sign*.8,-.2,.6),200+i+10*(sign+1),BLUE if sign==-1 or i>1 else LILAC)
    # Side majors wrap the same waist and flank surface, not view-specific meshes.
    for sign in [-1,1]:
        for i,(y,z,x,a,b) in enumerate([(-.53,.96,1.13,.31,.36),(.02,.72,.89,.29,.28),(.32,1.44,.87,.29,.34),(.69,.64,.95,.34,.28),(1.13,1.19,1.02,.38,.41),(1.30,.64,.97,.32,.29)]):
            cloud(f'FL_FLANK_{sign}_{i}',(sign*x,y,z),(a,b,.26),(sign,0,.1),300+i+20*(sign+1))
    # Top ridge / rear anatomy. Narrow waist retained beneath major groups.
    for i,(c,r) in enumerate([
      ((.04,-.25,2.55),(.42,.39,.28)),((.03,.47,2.34),(.31,.33,.27)),
      ((-.27,1.07,2.10),(.38,.33,.31)),((.39,1.23,1.93),(.34,.34,.29)),
      ((-.47,1.60,1.49),(.36,.40,.29)),((.43,1.64,1.15),(.38,.42,.30)),
      ((-.41,1.57,.65),(.35,.27,.28)),((.23,1.61,.59),(.34,.24,.27))]):
        normal=(0,1,.15) if i>3 else (0,.25,1)
        cloud(f'FL_REAR_{i}',c,r,normal,400+i)
    # Separate root and terminal tuft; the rump shell is recessed beneath it.
    ellipsoid('Tail_root',(.02,1.81,1.65),(.13,.29,.13),WHITE)
    cloud('FL_TAIL',(.02,1.88,1.76),(.40,.42,.36),(0,1,.3),512)
    cloud('FL_RUMP_center',(.00,1.72,1.02),(.49,.43,.28),(0,1,.08),520)
    if ARGS.iteration >= 3:
        # Secondary bridge clouds follow the curved chassis and avoid front skin.
        # Unequal station spacing and staggered latitude avoid ring/band patterns.
        stations=[-1.75,-1.48,-1.12,-.80,-.45,-.11,.24,.59,.91,1.23,1.52,1.72]
        serial=0
        for station,y in enumerate(stations):
            w,lo,hi=section(y);mid=(lo+hi)/2;rz=(hi-lo)/2
            count=12 if station<6 else 11
            for j in range(count):
                angle=-.40+j*(math.pi+ .8)/(count-1)+(.09 if station%2 else -.04)
                x=w*math.cos(angle);z=mid+rz*math.sin(angle)
                normal=Vector((math.cos(angle)/max(w,.1),0,math.sin(angle)/max(rz,.1))).normalized()
                c=Vector((x,y,z))-normal*.065
                if y>1.50 and abs(x)<.49 and z>1.35:continue
                # Preserve the clear face/ear channel and the controlled waist.
                if y<-.85 and z<1.68:continue
                nearest=min((Vector(a['center'])-c).length for a in CLUSTERS)
                if nearest<.255:continue
                rr=.26+.065*((station*7+j*3)%5)/4
                cloud(f'FL_BRIDGE_{serial:03d}',tuple(c),(rr*1.13,rr*(1.10+.14*(j%3)),rr*.88),tuple(normal),600+serial,LILAC if (j+station)%3 else BLUE)
                serial+=1
        # Face-facing blue underclouds fill crown/temple layers behind the white canopy.
        for i,(c,r) in enumerate([
            ((-.62,-1.42,2.42),(.35,.34,.32)),((-.99,-1.17,2.10),(.34,.37,.32)),
            ((.78,-1.11,2.32),(.30,.34,.30)),((.02,-1.36,2.62),(.34,.26,.24)),
            ((-1.22,-.74,1.16),(.27,.33,.27)),((1.22,-.72,1.11),(.28,.34,.26)),
            ((-.99,-1.08,.52),(.28,.25,.30)),((.96,-1.03,.49),(.31,.24,.31)),
            ((-.12,-1.01,.37),(.34,.19,.29)),((.0,-1.55,2.39),(.39,.34,.34)),
            ((-.41,-1.61,2.11),(.36,.32,.29)),((.68,-1.42,2.32),(.36,.30,.32))]):cloud(f'FL_FRONT_BRIDGE_{i}',c,r,(0,-1,.05),800+i,BLUE if i<3 else WHITE)
    if ARGS.iteration>=7:
        for sign in [-1,1]:
            for i,y in enumerate([-.65,-.20,.28,.76]):
                w,lo,hi=section(y)
                cloud(f'FL_BELLY_{sign}_{i}',(sign*w*.64,y,.39),(.30,.27,.25),(sign*.25,0,-1),950+i+10*(sign+1))


def motifs():
    def star(name,c,size,normal):
        n=Vector(normal).normalized();x=Vector((1,0,0));x=(x-n*x.dot(n)).normalized();z=n.cross(x)
        vs=[tuple(Vector(c)+n*.065)];fs=[];N=80
        for i in range(N):
            a=math.tau*i/N;rr=size*(.79+.21*math.cos(5*a))
            vs.append(tuple(Vector(c)+x*(rr*math.sin(a))+z*(rr*math.cos(a))))
        for i in range(N):fs.append((0,1+i,1+(i+1)%N))
        ob=mesh(name,vs,fs,GOLD);m=ob.modifiers.new('Rounded motif thickness','SOLIDIFY');m.thickness=.055
        bevel=ob.modifiers.new('Soft edge','BEVEL');bevel.width=.025;bevel.segments=3
    for i,(c,s,n) in enumerate([((-.04,-1.42,2.51),.17,(0,-1,.3)),((.28,-1.94,1.99),.16,(0,-1,.1)),((-.99,-1.20,1.55),.135,(-.5,-1,.1)),((-.91,-1.43,.58),.14,(0,-1,0)),((.02,-1.86,.46),.14,(0,-1,0)),((1.27,1.12,1.28),.17,(1,0,.2)),((-.70,1.82,1.1),.15,(0,1,0))]):star('Star_'+str(i),c,s,n)
    # One curved crescent on the upper left flank; never duplicated per view.
    c=Vector((-.98,-.87,2.10));n=Vector((-.75,-.63,.18)).normalized();x=Vector((1,-1,0)).normalized();z=n.cross(x).normalized()
    points=[]
    for i in range(65):
        a=math.radians(55)+(math.radians(300)-math.radians(55))*i/64
        points.append((.33*math.cos(a),.36*math.sin(a)))
    start=points[-1];end=points[0]
    for i in range(1,65):
        t=i/64;xx=(1-t)*start[0]+t*end[0]-.25*math.sin(math.pi*t);zz=(1-t)*start[1]+t*end[1]
        points.append((xx,zz))
    vs=[tuple(c+x*a+z*b+n*(.025*(1-(a/.5)**2))) for a,b in points]
    ob=mesh('Moon_single_curved_crescent',vs,[tuple(range(len(vs)))],GOLD)
    m=ob.modifiers.new('Moon thickness','SOLIDIFY');m.thickness=.055
    m=ob.modifiers.new('Moon soft edge','BEVEL');m.width=.025;m.segments=3

def camera(name,az,el):
    t=Vector((0,0,1.5));a=math.radians(az);e=math.radians(el)
    pos=t+Vector((12*math.sin(a)*math.cos(e),-12*math.cos(a)*math.cos(e),12*math.sin(e)))
    d=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,d);SC.collection.objects.link(ob)
    ob.location=pos;ob.rotation_euler=(t-pos).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=5.6
    return ob

CAMERAS={k:camera('CAM_CAROL_'+label,a,e) for k,label,a,e in [('front','FRONT',0,0),('side','SIDE',90,0),('back','BACK',180,0),('top','TOP',180,90),('3q-left','3Q_LEFT',-38,18),('3q-right','3Q_RIGHT',38,18)]}
# Top front maps upward, matching the dedicated plan, not camera-dependent shape.
CAMERAS['top'].rotation_euler=(0,0,math.pi)
if ARGS.camera_fit:
    fit=json.loads((ROOT/ARGS.camera_fit).read_text(encoding='utf8'))
    for key,row in fit['views'].items():
        if 'azimuth' not in row:continue
        cam=CAMERAS[key];a=math.radians(row['azimuth']);e=math.radians(row['elevation']);dist=row.get('distance') or 12
        target=Vector((0,0,1.5));cam.location=target+Vector((dist*math.sin(a)*math.cos(e),-dist*math.cos(a)*math.cos(e),dist*math.sin(e)))
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=row['projection'];cam.data.lens=50
        cam.rotation_euler=(cam.rotation_euler.to_quaternion() @ Quaternion((0,0,1),math.radians(row.get('roll_degrees',0)))).to_euler()
        cam['camera_fit_rmse_px']=row['rmse_px']

def render(view,dest):
    SC.camera=CAMERAS[view];SC.render.filepath=str(dest);bpy.ops.render.render(write_still=True)

def setup():
    SC.render.engine='BLENDER_WORKBENCH';SC.render.resolution_x=ARGS.resolution;SC.render.resolution_y=ARGS.resolution;SC.render.resolution_percentage=100
    SC.render.image_settings.file_format='PNG';SC.render.image_settings.color_mode='RGBA';SC.render.film_transparent=True
    SC.display.shading.light='STUDIO';SC.display.shading.color_type='SINGLE';SC.display.shading.single_color=(.58,.58,.58)
    SC.display.shading.show_shadows=True;SC.display.shading.show_cavity=True;SC.display.shading.cavity_type='BOTH'
    SC.display.shading.curvature_ridge_factor=.5;SC.display.shading.curvature_valley_factor=.6
    SC.view_settings.view_transform='Standard'

def main():
    chassis();face()
    if ARGS.pass_number>=3:facial_features()
    if ARGS.pass_number>=4:ears();hooves()
    if ARGS.pass_number>=5:fleece()
    if ARGS.pass_number>=6:motifs()
    for ob in list(COL.objects):
        if ob.type=='CURVE':
            bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH')
            # Blender's converted curve caps can contain duplicate boundary
            # vertices. Weld then close the boundary in the generator itself.
            bm=bmesh.new();bm.from_mesh(ob.data)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
            bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
            bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    if ARGS.iteration>=5:
        def deform(p):
            x,y,z=p
            waist=1-.20*math.exp(-((y-.18)/.57)**2)
            # Shoulder breadth and raised rear underbody, fitted across orthos.
            breadth=1+.075*math.exp(-((z-1.8)/.63)**2)
            return (x*waist*breadth,y*.967,z)
        for ob in COL.objects:
            if ob.type=='MESH':
                for vertex in ob.data.vertices:
                    vertex.co=deform(vertex.co)
                    if ob.name.startswith('Hoof_') and ARGS.iteration>=7:vertex.co.z*=.85
        for key,p in list(LANDMARKS.items()):LANDMARKS[key]=list(deform(p))
    if ARGS.profile_fit:
        guide=json.loads((ROOT/ARGS.profile_fit).read_text());xs=np.array(guide['top_x_scale_by_world_y']);zs=np.array(guide['side_crown_z_offset_by_world_y'])
        def guide_value(y,table):
            j=int(np.clip(np.searchsorted(table[:,0],y)-1,0,len(table)-2));t=float(np.clip((y-table[j,0])/(table[j+1,0]-table[j,0]),0,1))
            p0=table[max(0,j-1),1];p1=table[j,1];p2=table[j+1,1];p3=table[min(len(table)-1,j+2),1]
            return float(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
        def profile_deform(p):
            x,y,z=p
            return x*guide_value(y,xs),y,z+guide_value(y,zs)*min(1,max(0,(z-1.35)/.7))
        for ob in COL.objects:
            if ob.type=='MESH':
                for vertex in ob.data.vertices:vertex.co=profile_deform(vertex.co)
        for key,p in list(LANDMARKS.items()):LANDMARKS[key]=list(profile_deform(p))
    # One shared spatial edit, after the saved calibration. The mantle above
    # the face becomes shallower; the long torso retains the dominant volume.
    # Do not move the face, ears, supports or camera with this fleece edit.
    for ob in COL.objects:
        if ob.type!='MESH' or not (ob.name.startswith('FL_') or ob.name.startswith('Fleece_')):continue
        for v in ob.data.vertices:
            x,y,z=v.co
            upper=max(0,min(1,(z-1.55)/.70))
            anterior=math.exp(-((y+1.38)/.62)**2)
            center=math.exp(-(x/.72)**4)
            v.co.y+=.10*anterior*upper*center
            v.co.z-=.025*anterior*upper
            if ob.name!='FL_TAIL':
                # A shallow saddle at the tuft root gives a real attachment.
                pocket=math.exp(-(x/.39)**4-((z-1.64)/.38)**4)
                v.co.y-=.13*pocket*max(0,min(1,(y-1.38)/.32))
                v.co.y-=.10*max(0,min(1,(y-1.35)/.30))*max(0,min(1,(z-1.50)/.30))
    # Weld cloud-to-shell intersections into real rounded valleys. The face,
    # ear bowls, tail and four supports stay independent anatomical meshes.
    fleece_objects=[ob for ob in COL.objects if ob.type=='MESH' and
                    (ob.name.startswith('FL_') or ob.name.startswith('Fleece_')) and ob.name!='FL_TAIL']
    bpy.ops.object.select_all(action='DESELECT')
    for ob in fleece_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['Fleece_Chassis_SectionLoft']
    bpy.ops.object.join();shell=bpy.context.object;shell.name='Fleece_Structural_Shell'
    mod=shell.modifiers.new('Continuous rounded cloud junctions','REMESH');mod.mode='VOXEL';mod.voxel_size=.018;mod.use_smooth_shade=True
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=shell.modifiers.new('Soften intersection creases','SMOOTH');mod.factor=1.0;mod.iterations=5
    bpy.ops.object.modifier_apply(modifier=mod.name)
    tail=bpy.data.objects.get('FL_TAIL')
    if tail:
        bpy.context.view_layer.objects.active=tail
        mod=tail.modifiers.new('Independent three-dimensional tuft','REMESH');mod.mode='VOXEL';mod.voxel_size=.012;mod.use_smooth_shade=True
        bpy.ops.object.modifier_apply(modifier=mod.name)
        mod=tail.modifiers.new('Soft tuft junctions','SMOOTH');mod.factor=1;mod.iterations=3
        bpy.ops.object.modifier_apply(modifier=mod.name)
    setup();bpy.context.view_layer.update()
    folder=OUT/'iterations'/f'pass-{ARGS.pass_number:02d}-iteration-{ARGS.iteration:02d}'
    folder.mkdir(parents=True,exist_ok=True)
    for v in ARGS.views.split(','):render(v,folder/f'{v}-clay.png')
    if ARGS.pass_number >= 2:
        SC.display.shading.light='FLAT';SC.display.shading.color_type='OBJECT'
        SC.display.shading.show_shadows=False;SC.display.shading.show_cavity=False
        for ob in COL.objects:ob.color=(1,1,1,1) if ob.name=='Head_Volumetric_Cheeks_Jaw' else (0,0,0,1)
        for v in ARGS.views.split(','):render(v,folder/f'{v}-face-mask.png')
        SC.display.shading.light='STUDIO';SC.display.shading.color_type='SINGLE'
        SC.display.shading.show_shadows=True;SC.display.shading.show_cavity=True
    # Lookdev is explicitly gated: pass 7 is opt-in, after geometry evidence review.
    if ARGS.pass_number>=7:
        SC.render.engine='CYCLES';SC.cycles.samples=32;SC.cycles.use_denoising=True
        SC.world=bpy.data.worlds.new('Soft studio');SC.world.use_nodes=True
        SC.world.node_tree.nodes['Background'].inputs[0].default_value=(.68,.73,.91,1);SC.world.node_tree.nodes['Background'].inputs[1].default_value=.45
        for name,pos,power,size in [('Key',(-4,-6,7),850,5),('Fill',(4,-4,4),450,5),('Rim',(1,4,6),700,4)]:
            d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);SC.collection.objects.link(o)
            o.location=pos;o.rotation_euler=(Vector((0,0,1.5))-o.location).to_track_quat('-Z','Y').to_euler()
        SC.view_settings.view_transform='AgX'
        for v in ARGS.views.split(','):render(v,folder/f'{v}-render.png')
    camera_data={}
    from bpy_extras.object_utils import world_to_camera_view
    for v,cam in CAMERAS.items():
        camera_data[v]={'projection':cam.data.type,'ortho_scale':cam.data.ortho_scale,'lens_mm':cam.data.lens if cam.data.type=='PERSP' else None,'position':list(cam.location),'rotation':list(cam.rotation_euler),'landmarks_px':{}}
        for k,p in LANDMARKS.items():
            q=world_to_camera_view(SC,cam,Vector(p));camera_data[v]['landmarks_px'][k]=[q.x*ARGS.resolution,(1-q.y)*ARGS.resolution]
    cross_sections={str(z):[[float(x),face_y(float(x),z),z] for x in np.linspace(-.85,.85,41) if abs(x/.86)**2.0+abs((z-1.15)/.57)**2.5<1] for z in [.65,.85,1.00,1.145,1.45,1.65]}
    (folder/'geometry-data.json').write_text(json.dumps({'pass':ARGS.pass_number,'iteration':ARGS.iteration,'landmarks_3d':LANDMARKS,'cameras':camera_data,'clusters':CLUSTERS,'sections':SECTIONS.tolist(),'face_cross_sections':cross_sections,'resolution':ARGS.resolution,'profile_fit':ARGS.profile_fit,'camera_fit':ARGS.camera_fit,'deformation':'iteration>=5: x waist gaussian 20%, shoulder gaussian +7.5%; y*0.967; shared across all views; sections/clusters remain authoring-space'},indent=2),encoding='utf8')
    SC.camera=CAMERAS['front']
    bpy.context.preferences.filepaths.save_version=0
    target=ROOT/'assets/grimo/production/carol/blender/carol-a-v006.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(target))

if __name__=='__main__':main()
