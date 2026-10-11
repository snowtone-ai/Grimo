"""Untextured Candidate B derivative and separate disposable deformation proof.

Blender 5.2; no service calls. Reuses v001 mesh/control utilities, NOT its face.
Run from repo root: blender -b -t 6 --python scripts/blender/build-shushu-geometry-v002.py
"""
import bpy,bmesh,sys,math,json,hashlib,importlib
from pathlib import Path
from collections import defaultdict
import numpy as np
from mathutils import Vector,Matrix,Euler
from mathutils.bvhtree import BVHTree

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
u=importlib.import_module('build-shushu-geometry-v001')
donor=u.donor
OUT=ROOT/'docs/production/shushu/evidence/geometry-v002'
ASSET=ROOT/'assets/grimo/production/shushu/blender/shushu-geometry-v002.blend'
PROOF=ASSET.with_name('shushu-geometry-v002-proof.blend')
STATIC=ROOT/'assets/grimo/production/shushu/tripo/geometry-v002/shushu-geometry-v002-tripo'
GLB=ROOT/'assets/grimo/production/shushu/runtime-probes/shushu-geometry-v002-proof.glb'
PART_NAMES=['Head','Torso','Leg.R','Leg.L','Ear.L','Ear.R','Paw.L','Paw.R']
character=[];parts={};eyes={};patches={};rig=None;proxy=None;cam=None
CONTACT_TARGETS=json.loads((OUT/'contact-targets.json').read_text()) if (OUT/'contact-targets.json').exists() else {}
smooth=u.smooth;shape=u.shape;evaluated=u.evaluated

def front_y(x,z):
    # Smooth field fitted to undamaged donor forehead/cheeks. Local patches only.
    return -.249+2.55*x*x+.36*(z-.66)**2-.002*math.exp(-(x/.060)**2-((z-.620)/.030)**2)

def eye_y(side,x,z):
    s=1 if side=='L' else -1;dx=x-s*.129;dz=z-.660;tilt=s*math.radians(22)
    xx=dx*math.cos(tilt)+dz*math.sin(tilt);zz=-dx*math.sin(tilt)+dz*math.cos(tilt)
    r2=(xx/.052)**2+(zz/.066)**2
    return front_y(x,z)-.006*max(0,1-r2)

def inner_point(cx,cz,rx,rz,a,tilt):
    xx=rx*math.cos(a);zz=rz*math.sin(a)
    return cx+xx*math.cos(tilt)-zz*math.sin(tilt),cz+xx*math.sin(tilt)+zz*math.cos(tilt)

def cut_patch(o,cx,cz,rx,rz,ix,iz,label,tilt=0):
    """Head-connected local annulus; outer vertices remain on the donor surface."""
    bm=face_bm;planes=[]
    id_layer=bm.verts.layers.int.get('v002_control_id') or bm.verts.layers.int.new('v002_control_id')
    next_id=max((v[id_layer] for v in bm.verts),default=0)+1
    for i in range(48):
        a=i/48*math.tau;n=Vector((math.cos(a)/rx,0,math.sin(a)/rz));planes.append(n)
        local=[f for f in bm.faces if not any(v[id_layer] for v in f.verts) and f.calc_center_median().y<-.065 and
               ((f.calc_center_median().x-cx)/rx)**2+((f.calc_center_median().z-cz)/rz)**2<2.2]
        geom=list({item for f in local for item in [f,*f.edges,*f.verts]})
        bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-7,
            plane_co=(cx+rx*math.cos(a),0,cz+rz*math.sin(a)),plane_no=n)
    doomed=[f for f in bm.faces if f.calc_center_median().y<-.065 and
            all(n.dot(f.calc_center_median()-Vector((cx,0,cz)))<1+1e-6 for n in planes)]
    bmesh.ops.delete(bm,geom=doomed,context='FACES')
    loose=[v for v in bm.verts if not v.link_faces]
    if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
    be=[e for e in bm.edges if e.is_boundary and all(v.co.y<-.065 and
        ((v.co.x-cx)/rx)**2+((v.co.z-cz)/rz)**2<1.16 for v in e.verts)]
    adj=defaultdict(list)
    for e in be:
        a,b=e.verts;adj[a].append(b);adj[b].append(a)
    assert adj and all(len(v)==2 for v in adj.values()),(label,'invalid boundary')
    start=min(adj,key=lambda v:v.co.x);bv=[start];prev=None;cur=start
    while True:
        nxt=next(v for v in adj[cur] if v!=prev)
        if nxt==start:break
        bv.append(nxt);prev,cur=cur,nxt
        assert len(bv)<=len(adj)
    assert len(bv)==len(adj),(label,'multiple boundaries')
    rows=[bv];data=[]
    for j in range(1,9):
        t=j/8;row=[]
        for v in bv:
            a=math.atan2((v.co.z-cz)/rz,(v.co.x-cx)/rx)
            tx,tz=inner_point(cx,cz,ix,iz,a,tilt)
            x=(1-t)*v.co.x+t*tx;z=(1-t)*v.co.z+t*tz
            target_y=front_y(x,z)
            w=smooth(.10,.94,t)
            # Only a shallow orbital lip: no broad artificial socket or flat face plane.
            y=target_y+(1-w)*(v.co.y-front_y(v.co.x,v.co.z))
            nv=bm.verts.new((x,y,z));nv[id_layer]=next_id;next_id+=1
            row.append(nv);data.append((nv,t,a))
        rows.append(row)
        for i in range(len(row)):
            k=(i+1)%len(row);bm.faces.new((rows[-2][i],rows[-2][k],row[k],row[i]))
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    return dict(cx=cx,cz=cz,rx=ix,rz=iz,control_verts=data,label=label,tilt=tilt)

def resolve_patches(head):
    # Keep actual BMesh references across all cuts; never infer ownership from coordinates.
    face_bm.verts.index_update()
    for p in patches.values():
        assert all(v.is_valid for v,t,a in p['control_verts'])
        p['transitions']=[(v.index,t,a) for v,t,a in p['control_verts']]
        assert len({i for i,t,a in p['transitions']})==len(p['transitions'])
    face_bm.verts.layers.int.remove(face_bm.verts.layers.int['v002_control_id'])
    face_bm.to_mesh(head.data);face_bm.free()

def blink(head,p,side):
    k=shape(head,'Blink.'+side,lambda p:p)
    for idx,t,a in p['transitions']:
        v=k.data[idx].co;w=t*t
        ux=(v.x-p['cx'])/.066
        seam=p['cz']-.036+.007*ux*ux
        v.z+=(seam-v.z)*w
        cover=front_y(v.x,v.z)-.0008
        v.y+=(cover-v.y)*smooth(.0,.40,t)
    arc=shape(head,'BlinkArc.'+side,lambda p:p)
    basis=head.data.shape_keys.key_blocks['Basis']
    for idx,t,a in p['transitions']:
        half=(basis.data[idx].co+k.data[idx].co)*.5
        desired=front_y(half.x,half.z)-.0005
        arc.data[idx].co.y+=(desired-half.y)*smooth(.08,.68,t)
    drv=arc.driver_add('value').driver;drv.expression='4*b*(1-b)'
    var=drv.variables.new();var.name='b';var.type='SINGLE_PROP';var.targets[0].id_type='KEY'
    var.targets[0].id=head.data.shape_keys;var.targets[0].data_path='key_blocks["Blink.'+side+'"].value'

def smile_line(x):
    a=abs(x)/.025
    return .604+.006*(2*a-1)**2

def mouth_keys(head,p):
    # Two tiny lobes; surrounding head owns the moving aperture.
    basis=head.shape_key_add(name='Basis') if not head.data.shape_keys else head.data.shape_keys.key_blocks['Basis']
    for idx,t,a in p['transitions']:
        co=head.data.vertices[idx].co.copy();target=smile_line(.025*math.cos(a))+.00065*math.sin(a)
        co.z+=t*t*(target-(p['cz']+p['rz']*math.sin(a)))
        co.y=front_y(co.x,co.z)
        head.data.vertices[idx].co=co
        for key in head.data.shape_keys.key_blocks:key.data[idx].co=co
    for name,half_height,width in [('MouthOpen',.0075,.025),('Surprise',.009,.012),('GentleSmile',.0012,.027)]:
        key=shape(head,name,lambda p:p)
        for idx,t,a in p['transitions']:
            co=key.data[idx].co
            tz=(.606+half_height*math.sin(a) if name=='Surprise' else smile_line(.025*math.cos(a))+half_height*math.sin(a))
            co.z+=t*t*(tz-(smile_line(.025*math.cos(a))+.00065*math.sin(a)))
            co.x+=t*t*(width-.025)*math.cos(a)
            co.y+=(front_y(co.x,co.z)-co.y)*t*t

def build_face(clay):
    global face_bm
    head=parts['Head']
    face_bm=bmesh.new();face_bm.from_mesh(head.data)
    for side,s in [('L',1),('R',-1)]:
        patches[side]=cut_patch(head,s*.129,.660,.084,.100,.052,.066,'Orbit.'+side,s*math.radians(22))
    patches['Mouth']=cut_patch(head,0,.606,.048,.037,.025,.010,'Mouth')
    resolve_patches(head)
    for side in ['L','R']:blink(head,patches[side],side)
    mouth_keys(head,patches['Mouth'])
    happy=shape(head,'HappyLids',lambda p:p)
    for side in ['L','R']:
        p=patches[side];closed=head.data.shape_keys.key_blocks['Blink.'+side]
        for idx,t,a in p['transitions']:
            q=closed.data[idx].co.copy();old=q.copy();ux=(q.x-p['cx'])/.066
            q.z+=.014*max(0,1-ux*ux)*t*t
            q.y+=(front_y(q.x,q.z)-.0008-q.y)*t*t
            happy.data[idx].co+=q-old
    for side,s in [('L',1),('R',-1)]:
        p=patches[side];verts=[(p['cx'],eye_y(side,p['cx'],p['cz']),p['cz'])];faces=[];n=64
        for row in range(1,9):
            radius=row/8
            for i in range(n):
                x,z=inner_point(p['cx'],p['cz'],p['rx']*radius,p['rz']*radius,i/n*math.tau,p['tilt'])
                verts.append((x,eye_y(side,x,z),z))
        for i in range(n):faces.append((0,1+i,1+(i+1)%n))
        for row in range(7):
            for i in range(n):
                a=1+row*n+i;b=1+row*n+(i+1)%n;faces.append((a,a+n,b+n,b))
        eye=u.mesh('Shushu_Eye.'+side,verts,faces,clay);eyes[side]=eye;character.append(eye)
        # The ocular cap recesses under the closing skin; the skin remains smooth
        # rather than inflating a protruding lid bowl to clear the original cap.
        shape(eye,'Blink.'+side,lambda q:q+Vector((0,.010,0)))
        e_arc=shape(eye,'BlinkArc.'+side,lambda q:q+Vector((0,-.002,0)))
        drv=e_arc.driver_add('value').driver;drv.expression='4*b*(1-b)'
        var=drv.variables.new();var.name='b';var.type='SINGLE_PROP';var.targets[0].id_type='KEY'
        var.targets[0].id=eye.data.shape_keys;var.targets[0].data_path='key_blocks["Blink.'+side+'"].value'
        # Surface-attached tiny lid crease, with the head skin doing the actual closure.
        pts=[]
        for i in range(33):
            x,z=inner_point(p['cx'],p['cz'],p['rx'],p['rz'],i/32*math.pi,p['tilt'])
            pts.append(Vector((x,front_y(x,z)-.001,z)))
        margin=u.tube('Shushu_LidMargin.'+side,pts,.00085,clay)
        close=shape(margin,'Blink.'+side,lambda p:p)
        arc=shape(margin,'BlinkArc.'+side,lambda p:p)
        joy=shape(margin,'HappyLids',lambda p:p)
        for idx,q in enumerate(close.data):
            center=pts[idx//8];offset=q.co-center;ux=(center.x-p['cx'])/.066
            z=p['cz']-.036+.007*ux*ux
            target=Vector((center.x,front_y(center.x,z)-.0015,z));q.co=target+offset
            mid=(center+target)*.5
            arc.data[idx].co.y+=front_y(mid.x,mid.z)-.0015-mid.y
            dest=target.copy();dest.z+=.014*max(0,1-ux*ux);dest.y=front_y(dest.x,dest.z)-.0015
            joy.data[idx].co+=dest-target
        drv=arc.driver_add('value').driver;drv.expression='4*b*(1-b)'
        var=drv.variables.new();var.name='b';var.type='SINGLE_PROP';var.targets[0].id_type='KEY'
        var.targets[0].id=margin.data.shape_keys;var.targets[0].data_path='key_blocks["Blink.'+side+'"].value'
        character.append(margin)
        # Independent shallow gaze alters actual cap surface; no authored pupil/color.
        for label,dx,dz in [('GazeLeft',-.004,0),('GazeRight',.004,0),('GazeUp',0,.003),('GazeDown',0,-.003)]:
            def gaze(q,dx=dx,dz=dz,side=side,p=p):
                rr=((q.x-p['cx'])/.067)**2+((q.z-p['cz'])/.075)**2
                w=max(0,1-rr)**2;q.x+=dx*w;q.z+=dz*w;q.y=eye_y(side,q.x,q.z);return q
            shape(eye,label,gaze)
    nose=u.ellipsoid('Shushu_Nose',(0,front_y(0,.638)-.006,.638),(.014,.007,.006),clay)
    character.append(nose)
    v=[(0,front_y(0,.606)+.009,.606)];f=[];n=64
    for i in range(n):
        a=i/n*math.tau;x=.025*math.cos(a);z=smile_line(x)+.00065*math.sin(a)
        v.append((x,front_y(x,z)+.001,z))
    for i in range(n):f.append((0,1+i,1+(i+1)%n))
    interior=u.mesh('Shushu_MouthInterior',v,f,clay)
    for name,hh,width in [('MouthOpen',.0075,.025),('Surprise',.009,.012),('GentleSmile',.0012,.027)]:
        k=shape(interior,name,lambda p:p)
        for i,q in enumerate(list(k.data)[1:]):
            a=i/n*math.tau;q.co.x=width*math.cos(a)
            q.co.z=.606+hh*math.sin(a) if name=='Surprise' else smile_line(.025*math.cos(a))+hh*math.sin(a)
            q.co.y=front_y(q.co.x,q.co.z)+.001
    character.append(interior)

def seated_key(o,part):
    def seat(p):
        if part.startswith('Leg'):
            # Entire short limb turns forward/outward around a plush hip, not a human knee.
            s=1 if part.endswith('L') else -1;pivot=Vector((s*.136,.014,.193))
            rotation=Euler((math.radians(-67),s*math.radians(-9),0),'XYZ').to_matrix()
            drop=.03397910 if s>0 else .03398983
            q=rotation@(p-pivot)+pivot+Vector((s*.016,-.020,-drop))
            return q
        q=p.copy();q.z-=.120
        if part=='Torso':
            # Broad rump contact, local lower-body redistribution only.
            w=1-smooth(.145,.29,p.z);q.z-=.010*w
            q.x*=1+.05*w;q.y=.02+(q.y-.02)*(1+.06*w)
            if q.z<.014:q.z=.001+max(0,q.z+.001)*.12
        return q
    seated=shape(o,'Seated',seat)
    if part.startswith('Leg'):
        s=1 if part.endswith('L') else -1;pivot=Vector((s*.136,.014,.193))
        rotation=Euler((math.radians(-33.5),s*math.radians(-4.5),0),'XYZ').to_matrix()
        drop=.03397910 if s>0 else .03398983
        offset=Vector((s*.016,-.020,-drop))*.5
        arc=shape(o,'SeatArc',lambda p:p)
        basis=o.data.shape_keys.key_blocks['Basis']
        for idx,q in enumerate(arc.data):
            p=basis.data[idx].co;target=rotation@(p-pivot)+pivot+offset
            q.co+=target-(p+seated.data[idx].co)*.5
        drv=arc.driver_add('value').driver;drv.expression='4*s*(1-s)'
        var=drv.variables.new();var.name='s';var.type='SINGLE_PROP';var.targets[0].id_type='KEY'
        var.targets[0].id=o.data.shape_keys;var.targets[0].data_path='key_blocks["Seated"].value'
        # The short leg sweeps forward while its lowest sole stays on the floor.
        # Its Z coordinate is quadratic in s; only a few vertices form the lower envelope.
        base=np.array([q.co[:] for q in basis.data]);end=np.array([q.co[:] for q in seated.data]);delta=np.array([q.co[:] for q in arc.data])-base
        active=set()
        for s0 in np.linspace(0,1,401):active.add(int(np.argmin(base[:,2]+s0*(end[:,2]-base[:,2])+4*s0*(1-s0)*delta[:,2])))
        ground=shape(o,'SeatGround',lambda p:p+Vector((0,0,.05)))
        expressions=[f'{(.001-base[i,2])/.05:.6g}{-(end[i,2]-base[i,2]+4*delta[i,2])/.05:+.6g}*s{4*delta[i,2]/.05:+.6g}*s*s' for i in sorted(active)]
        expression='max('+','.join(expressions)+')'
        assert len(expression)<256,(len(expression),len(active))
        drv=ground.driver_add('value').driver;drv.expression=expression
        var=drv.variables.new();var.name='s';var.type='SINGLE_PROP';var.targets[0].id_type='KEY'
        var.targets[0].id=o.data.shape_keys;var.targets[0].data_path='key_blocks["Seated"].value'

def init_rig():
    global rig
    rig=u.rig_create()
    for part,o in parts.items():
        if part=='Head':u.bind(o,rig,'Head',lambda p:{'Head':smooth(.475,.54,p.z),'Root':1-smooth(.475,.54,p.z)})
        elif part.startswith(('Paw','Ear')):u.bind(o,rig,part)
        elif part.startswith('Leg'):u.bind(o,rig,'Root',lambda p,part=part:{'Root':smooth(.055,.095,p.z),'Foot.'+part[-1]:1-smooth(.055,.095,p.z)})
        else:u.bind(o,rig,'Root')
    for o in character:
        part=o.get('part','Head')
        if 'part' not in o:u.bind(o,rig,'Head')
        u.support_keys(o,part);seated_key(o,part)
        o['production_id']=o.name;o.data.name=o.name
    for side,s in [('L',1),('R',-1)]:
        def cheek(p,s=s):
            q=((p.x-s*.23)/.070)**2+((p.y+.13)/.085)**2+((p.z-.571)/.060)**2
            guard=smooth(.177,.205,abs(p.x))*(1-smooth(.592,.620,p.z))
            p.y+=.017*math.exp(-q*2)*guard;return p
        shape(parts['Head'],'CheekPressure.'+side,cheek)
    def belly(p):
        q=(p.x/.12)**2+((p.y+.239)/.065)**2+((p.z-.325)/.11)**2
        p.y+=.025*math.exp(-q*2);return p
    shape(parts['Torso'],'BellyPressure',belly)

def reset():
    for o in character:
        if o.data.shape_keys:
            for k in o.data.shape_keys.key_blocks:k.value=0
    for b in rig.pose.bones:b.matrix_basis=Matrix.Identity(4)
    if proxy:proxy.hide_render=True;proxy.hide_viewport=True
    bpy.context.view_layer.update()

def key(name,value,objects=None):
    for o in objects or character:
        if o.data.shape_keys and name in o.data.shape_keys.key_blocks:o.data.shape_keys.key_blocks[name].value=value
        if name.startswith('Blink.') and o.data.shape_keys and 'BlinkArc.'+name[-1] in o.data.shape_keys.key_blocks:
            o.data.shape_keys.key_blocks['BlinkArc.'+name[-1]].value=4*value*(1-value)
        if name=='Seated' and o.data.shape_keys and 'SeatArc' in o.data.shape_keys.key_blocks:
            o.data.shape_keys.key_blocks['SeatArc'].value=4*value*(1-value)
    bpy.context.view_layer.update()

def head_pose(pitch=0,yaw=0,roll=0):
    rest=rig.data.bones['Head'].matrix_local
    depth=.065*parts['Head'].data.shape_keys.key_blocks['SupportedRest'].value+.120*parts['Head'].data.shape_keys.key_blocks['Seated'].value
    pivot=rest.translation-Vector((0,0,depth))
    rot=Euler(tuple(math.radians(a) for a in (pitch,roll,yaw)),'XYZ').to_matrix().to_4x4()
    rig.pose.bones['Head'].matrix=Matrix.Translation(pivot)@rot@Matrix.Translation(-pivot)@rest
    bpy.context.view_layer.update()

def paw_pose(side,target):
    rest=rig.data.bones['Paw.'+side].matrix_local;pivot=rest.translation
    rot=(rig.data.bones['Paw.'+side].tail_local-pivot).rotation_difference(Vector(target)-pivot).to_matrix().to_4x4()
    rig.pose.bones['Paw.'+side].matrix=Matrix.Translation(pivot)@rot@Matrix.Translation(-pivot)@rest
    bpy.context.view_layer.update()

def state(name):
    reset()
    if name in ['half','closed','smile']:
        for s in ['L','R']:key('Blink.'+s,.5 if name=='half' else 1)
        if name=='smile':key('GentleSmile',1);key('HappyLids',1)
    elif name=='left-closed':key('Blink.L',1)
    elif name=='right-closed':key('Blink.R',1)
    elif name=='mouth-open':key('MouthOpen',1)
    elif name=='surprise':key('Surprise',1)
    elif name=='gaze-blink':key('Blink.L',.55);key('GazeRight',1)
    elif name=='rest':key('SupportedRest',1)
    elif name.startswith('seat'):key('Seated',float(name.split('-')[1]) if '-' in name else 1)
    elif name=='offer':paw_pose('L',(.42,-.30,.34))
    elif name in ['hold','hold-touch']:
        for s,sg in [('L',1),('R',-1)]:paw_pose(s,(sg*.42,-.40,.38))
        proxy.hide_render=False
        proxy.hide_viewport=False
        if name=='hold-touch':head_pose(-6,0,0);key('CheekPressure.L',.7)
    elif name=='head-turn':head_pose(8,18,7)
    elif name=='pressure':key('CheekPressure.L',1);key('BellyPressure',1)
    elif name=='combined':key('Blink.L',.6);key('MouthOpen',.6);key('CheekPressure.L',.8);head_pose(4,8,3)
    elif name=='groom':
        head_pose(16,0,8);paw_pose('L',CONTACT_TARGETS.get(name,{}).get('target',(.25,-.16,.49)));key('CheekPressure.L',.45)
    elif name=='chest-groom':paw_pose('L',CONTACT_TARGETS.get(name,{}).get('target',(.11,-.20,.40)))

def make_proxy(clay):
    global proxy
    mounts=[]
    for side,s in [('R',-1),('L',1)]:
        paw_pose(side,(s*.42,-.40,.38));v,t=evaluated(parts['Paw.'+side])
        tree=BVHTree.FromPolygons([Vector(p) for p in v],t.tolist(),all_triangles=True)
        p,n,_,_=tree.find_nearest(Vector((0,-.35,.40)));mounts.append(p+n*.006)
    pts=[mounts[0].lerp(mounts[1],i/16)+Vector((0,-.060*math.sin(math.pi*i/16),0)) for i in range(17)]
    stem=u.tube('Reachable_Holding_Proxy',pts,.006,clay)
    caps=[u.ellipsoid('ProxyEnd',p,(.006,.006,.006),clay,24,12) for p in mounts]
    verts=[];faces=[]
    for o in [stem,*caps]:
        offset=len(verts);verts.extend(v.co.copy() for v in o.data.vertices)
        faces.extend([offset+i for i in p.vertices] for p in o.data.polygons)
        bpy.data.objects.remove(o,do_unlink=True)
    proxy=u.mesh('Reachable_Holding_Proxy',verts,faces,clay);proxy['role']='Independent disposable contact fixture, no final accessory'
    reset()

def render(name,direction=(0,-1,.08),detail=False):
    target=Vector((0,-.08,.73) if detail else (0,0,.49));d=Vector(direction).normalized()
    cam.location=target+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
    cam.data.ortho_scale=.87 if detail else 1.16
    bpy.context.scene.render.filepath=str(OUT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)

def static_export():
    reset();copies=[]
    for o in character:
        ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=bpy.data.meshes.new_from_object(ev)
        m.materials.clear();copy=bpy.data.objects.new(o.name,m);bpy.context.scene.collection.objects.link(copy)
        copy.matrix_world=ev.matrix_world;copy['production_id']=o.name;copies.append(copy)
        for a in list(m.color_attributes):m.color_attributes.remove(a)
        for a in list(m.uv_layers):m.uv_layers.remove(a)
    bpy.ops.object.select_all(action='DESELECT')
    for o in copies:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(STATIC.with_suffix('.glb')),export_format='GLB',use_selection=True,
        export_animations=False,export_skins=False,export_morph=False,export_materials='NONE',export_texcoords=False,export_attributes=False,export_yup=True)
    bpy.ops.export_scene.fbx(filepath=str(STATIC.with_suffix('.fbx')),use_selection=True,object_types={'MESH'},
        apply_unit_scale=True,axis_forward='-Z',axis_up='Y',bake_anim=False,use_mesh_modifiers=False,path_mode='AUTO',use_custom_props=True)
    for o in copies:bpy.data.objects.remove(o,do_unlink=True)

def proof_animation():
    scene=bpy.context.scene;scene.render.fps=24;scene.frame_start=1
    states=['neutral','half','closed','smile','left-closed','right-closed','mouth-open','surprise','combined',
            'chest-groom','rest','head-turn','seat-0.25','seat-0.5','seat-0.75','seat','gaze-blink','offer','hold','hold-touch','groom','pressure','neutral']
    samples={}
    for i,name in enumerate(states):
        frame=1+i*8;scene.frame_set(frame);state(name)
        proxy.keyframe_insert('hide_render',frame=frame);proxy.keyframe_insert('hide_viewport',frame=frame)
        for o in character:
            if o.data.shape_keys:
                for k in list(o.data.shape_keys.key_blocks)[1:]:k.keyframe_insert('value',frame=frame)
        for b in rig.pose.bones:
            b.rotation_mode='QUATERNION';b.keyframe_insert('location',frame=frame);b.keyframe_insert('rotation_quaternion',frame=frame);b.keyframe_insert('scale',frame=frame)
        samples[str(frame)]=name
    scene.frame_end=1+(len(states)-1)*8;scene.frame_set(1)
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
    for o in character:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,export_animations=True,
        export_animation_mode='SCENE',export_force_sampling=True,export_skins=True,export_morph=True,
        export_morph_animation=True,export_anim_scene_split_object=False,export_materials='NONE',export_texcoords=False,export_attributes=False,export_extras=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(PROOF))
    return samples

def main():
    global head_surface,eye_fits,cam
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'renders').mkdir(exist_ok=True);STATIC.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.preferences.filepaths.save_version=0
    source=ROOT/'assets/grimo/production/shushu/tripo/candidate-b-8481/cute panda 3d model 8481.fbx'
    bpy.ops.import_scene.fbx(filepath=str(source))
    raw=next(o for o in bpy.context.scene.objects if o.type=='MESH')
    # Actual source FBX world coordinates already map to normalized Blender Z up / -Y front.
    coords=np.array([raw.matrix_world@v.co for v in raw.data.vertices])
    print('IMPORTED_SOURCE_BOUNDS',coords.min(0),coords.max(0))
    assert np.max(coords[:,2])>.99 and np.min(coords[:,2])>-1e-5
    raw.matrix_world=Matrix.Identity(4)
    for v,co in zip(raw.data.vertices,coords):v.co=co
    raw.name='SourceB_UntouchedTopology';raw.data.materials.clear()
    archive=bpy.data.collections.new('SOURCE_B_REFERENCE_ONLY');bpy.context.scene.collection.children.link(archive)
    for c in list(raw.users_collection):c.objects.unlink(raw)
    archive.objects.link(raw);archive.hide_render=True;archive.hide_viewport=True
    clay=u.material('Diagnostic neutral clay',(.55,.55,.55),.72)
    groups=donor.components(raw.data);polys=[list(p.vertices) for p in raw.data.polygons]
    eye_fits={}
    for index,side in [(14,'R'),(15,'L')]:
        ids=sorted({v for f in groups[index] for v in polys[f]});a=coords[ids];x=a[:,0];z=a[:,2]
        eye_fits[side]=np.linalg.lstsq(np.array([np.ones(len(a)),x,z,x*x,x*z,z*z]).T,a[:,1],rcond=None)[0]
    for n,name in enumerate(PART_NAMES):
        g=groups[n];ids=sorted({v for f in g for v in polys[f]});mp={v:i for i,v in enumerate(ids)}
        o=u.mesh('Shushu_'+name,coords[ids],[[mp[v] for v in polys[f]] for f in g],clay)
        parts[name]=o;o['part']=name;o['provenance']='Actual original Candidate B FBX, first eight semantic components'
        if name=='Head':
            for v in o.data.vertices:
                x,y,z=v.co
                # Remove donor socket and open-mouth relief only in motion-critical patches.
                orbit=max(1-smooth(1.10,1.65,math.sqrt(((x-s*.129)/.100)**2+((z-.660)/.120)**2)) for s in [-1,1])
                mouth=(1-smooth(.070,.115,abs(x)))*smooth(.52,.55,z)*(1-smooth(.658,.685,z))
                w=max(orbit,mouth)*(1-smooth(-.090,-.040,y))
                v.co.y=(1-w)*y+w*front_y(x,z)
        # Per-module continuity repair; no whole-character remesh. Keep donor face relief.
        u.remesh(o,.007 if n==0 else .008,.55 if n==0 else .6)
        if n in [0,1]:
            bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
            old=np.array([v.co[:] for v in o.data.vertices]);lo=old.min(0);hi=old.max(0)
            mod=o.modifiers.new('Remove source sampling bands','SMOOTH');mod.factor=.75;mod.iterations=65 if n==0 else 40
            bpy.ops.object.modifier_apply(modifier=mod.name)
            arr=np.array([v.co[:] for v in o.data.vertices]);nlo=arr.min(0);nhi=arr.max(0)
            for v in o.data.vertices:v.co=Vector(lo+(np.array(v.co)-nlo)*(hi-lo)/np.maximum(nhi-nlo,1e-9))
        if name.startswith('Leg'):
            for v in o.data.vertices:
                if v.co.z<.012:v.co.z=.001
        if name=='Head':
            for v in o.data.vertices:
                # Reapply local smooth front after donor-band smoothing, so that
                # inherited sockets do not reappear around the attached annuli.
                x,y,z=v.co
                orbit=max(1-smooth(1.10,1.65,math.sqrt(((x-s*.129)/.100)**2+((z-.660)/.120)**2)) for s in [-1,1])
                mouth=(1-smooth(.070,.115,abs(x)))*smooth(.52,.55,z)*(1-smooth(.658,.685,z))
                w=max(orbit,mouth)*(1-smooth(-.090,-.040,y))
                v.co.y=(1-w)*y+w*front_y(x,z)
                # Rounded infant jaw floor replaces the donor's squared lower corners only.
                floor=.482+.090*(abs(v.co.x)/.305)**3
                if v.co.z<floor:v.co.z+=(floor-v.co.z)*.90
        character.append(o)
    v,t=evaluated(parts['Head']);head_surface=BVHTree.FromPolygons([Vector(p) for p in v],t.tolist(),all_triangles=True)
    build_face(clay);init_rig();make_proxy(clay)
    # Everything editable has one diagnostic clay; no UV/color/maps exist on the candidate.
    for o in character:
        for a in list(o.data.uv_layers):o.data.uv_layers.remove(a)
        for a in list(o.data.color_attributes):o.data.color_attributes.remove(a)
        for p in o.data.polygons:p.use_smooth=True
    cam=u.setup_render();scene=bpy.context.scene
    scene.render.resolution_x=480;scene.render.resolution_y=540
    scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.75,.75,.75,1)
    ground=u.mesh('Diagnostic_Ground',[(-3,-3,0),(3,-3,0),(3,3,0),(-3,3,0)],[(0,1,2,3)],clay)
    for label,objects in [('SHUSHU_GEOMETRY',character),('DEVELOPMENT_ONLY',[rig,proxy]),
                          ('INSPECTION_ONLY',[ground,cam,*[o for o in scene.objects if o.type=='LIGHT']])]:
        collection=bpy.data.collections.new(label);scene.collection.children.link(collection)
        for o in objects:
            for existing in list(o.users_collection):existing.objects.unlink(o)
            collection.objects.link(o)
    for mat in list(bpy.data.materials):
        if mat!=clay and mat.users==0:bpy.data.materials.remove(mat)
    for image in list(bpy.data.images):
        if image.users==0:bpy.data.images.remove(image)
    scene['boundary']='UNCOLORED editable geometry, disposable rig only. Human geometry acceptance pending.'
    scene['pose_contract']='Generation/rest: donor A stance. Standing vs seated Game Neutral UNDECIDED.'
    scene['attachment_ownership']='Crown=Head; Wear=ear exterior/chest; Bouquet/Gift=paws; Food=mouth. No accessory geometry.'
    reset();static_export();bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    if '--no-render' not in sys.argv:
        for name,d in [('front',(0,-1,.08)),('side',(1,0,.08)),('rear',(0,1,.08)),('three-quarter',(1,-2,.10))]:
            state('neutral');render('neutral-'+name,d)
        for name in ['neutral','half','closed','left-closed','mouth-open','smile','surprise','combined']:
            state(name);render('face-'+name,(0,-1,.02),True)
        for name in ['rest','seat','offer','hold','hold-touch','head-turn','groom','pressure']:
            state(name);render(name,(1,-2,.12))
        for name in ['rest','seat']:
            state(name);render(name+'-front');render(name+'-side',(1,0,.08))
    samples=proof_animation()
    (OUT/'build-manifest.json').write_text(json.dumps({'blender':bpy.app.version_string,'source_fbx_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'eye_fits':{k:v.tolist() for k,v in eye_fits.items()},'animation_samples':samples,
        'candidate_meshes':{o.name:{'vertices':len(o.data.vertices),'polygons':len(o.data.polygons)} for o in character},
        'neutral_source':'Original Candidate B; no v001 visible face used','appearance':'single neutral diagnostic clay; static export no authored material/UV/color/texture'},indent=2)+'\n')
    print('V002_BUILD_COMPLETE')

if __name__=='__main__':main()
