"""Candidate B regional repair + editable deformation candidate. Blender 5.2.

No services, paid operations, or canonical edits. All coordinates are height units.
Run: blender -b -t 6 --python scripts/blender/build-shushu-geometry-v001.py
"""
import bpy, bmesh, math, json, sys, hashlib
from pathlib import Path
from collections import defaultdict
from mathutils import Vector, Matrix, Euler
from mathutils.bvhtree import BVHTree
import numpy as np

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/production/shushu/evidence/geometry-v001'
ASSET = ROOT/'assets/grimo/production/shushu/blender/shushu-geometry-v001.blend'
GLB = ROOT/'assets/grimo/production/shushu/runtime-probes/shushu-geometry-v001.glb'
OUT.mkdir(parents=True, exist_ok=True)
(OUT/'renders').mkdir(exist_ok=True)
sys.path.insert(0,str(Path(__file__).parent))
import importlib
donor = importlib.import_module('shushu-candidate-b-deform')

def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a))); return t*t*(3-2*t)

def mesh(name, verts, faces, material):
    m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update()
    o=bpy.data.objects.new(name,m);bpy.context.scene.collection.objects.link(o)
    m.materials.append(material)
    for p in m.polygons:p.use_smooth=True
    return o

def material(name,color,rough=.65):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=rough
    return m

def shape(o,name,fn):
    if not o.data.shape_keys:o.shape_key_add(name='Basis')
    basis=[p.co.copy() for p in o.data.shape_keys.key_blocks['Basis'].data]
    k=o.shape_key_add(name=name,from_mix=False)
    k.relative_key=o.data.shape_keys.key_blocks['Basis'];k.value=0
    for v,p in zip(k.data,basis):v.co=fn(p)
    return k

def remesh(o,voxel,ratio):
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bm=bmesh.new();bm.from_mesh(o.data)
    boundary=[e for e in bm.edges if e.is_boundary]
    if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
    mod=o.modifiers.new('Donor surface continuity','REMESH');mod.mode='VOXEL';mod.voxel_size=voxel
    bpy.ops.object.modifier_apply(modifier=mod.name)
    old=np.array([v.co[:] for v in o.data.vertices]);lo=old.min(0);hi=old.max(0)
    mod=o.modifiers.new('Relax donor sampling','SMOOTH');mod.factor=.55;mod.iterations=18
    bpy.ops.object.modifier_apply(modifier=mod.name)
    new=np.array([v.co[:] for v in o.data.vertices]);nlo=new.min(0);nhi=new.max(0)
    # Restore donor extent after removing high-frequency sampling ridges.
    for v in o.data.vertices:
        v.co=Vector(lo+(np.array(v.co)-nlo)*(hi-lo)/np.maximum(nhi-nlo,1e-9))
    mod=o.modifiers.new('Exterior density','DECIMATE');mod.ratio=ratio
    bpy.ops.object.modifier_apply(modifier=mod.name)
    for p in o.data.polygons:p.use_smooth=True

def face_y(x,z):
    # Fitted to undamaged forehead/cheek surface; retains donor silhouette.
    return -.249+2.55*x*x+.36*(z-.66)**2-.011*math.exp(-(x/.073)**2-((z-.615)/.035)**2)

def orbital_y(x,z,cx,cz,rx,rz):
    r2=((x-cx)/rx)**2+((z-cz)/rz)**2
    return face_y(x,z)-.014*max(0,1-r2)

def cut_patch(o,cx,cz,rx,rz,inner_x,inner_z,label):
    """Connected head-skin annulus with 8 controllable radial transition rows."""
    bm=bmesh.new();bm.from_mesh(o.data)
    # Exact polygonal cut: centroid-only deletion made a zigzag border and stray islands.
    planes=[]
    for i in range(40):
        a=i/40*math.tau;n=Vector((math.cos(a)/rx,0,math.sin(a)/rz))
        planes.append(n)
        local=[f for f in bm.faces if f.calc_center_median().y<-.06 and
               ((f.calc_center_median().x-cx)/rx)**2+((f.calc_center_median().z-cz)/rz)**2<2.2]
        geom=list({item for f in local for item in [f,*f.edges,*f.verts]})
        bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-7,plane_co=Vector((cx+rx*math.cos(a),0,cz+rz*math.sin(a))),plane_no=n)
    doomed=[f for f in bm.faces if f.calc_center_median().y<-.075 and
            all(n.dot(f.calc_center_median()-Vector((cx,0,cz)))<1+1e-6 for n in planes)]
    bmesh.ops.delete(bm,geom=doomed,context='FACES')
    loose=[v for v in bm.verts if not v.link_faces]
    if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
    boundary=[e for e in bm.edges if e.is_boundary]
    be=[e for e in boundary if all(v.co.y<-.07 and
             ((v.co.x-cx)/rx)**2+((v.co.z-cz)/rz)**2<1.15 for v in e.verts)]
    adj=defaultdict(list)
    for e in be:
        a,b=e.verts;adj[a].append(b);adj[b].append(a)
    assert all(len(v)==2 for v in adj.values()),(label,'branched boundary')
    start=min(adj,key=lambda v:v.co.x);bv=[start];prev=None;cur=start
    while True:
        nxt=next(v for v in adj[cur] if v!=prev)
        if nxt==start:break
        bv.append(nxt);prev,cur=cur,nxt
        assert len(bv)<=len(adj)
    assert len(bv)==len(adj),(label,'multiple boundary cycles',len(bv),len(adj))
    assert len(bv)>12,(label,len(bv))
    rows=[bv]; transitions=[]
    for j in range(1,9):
        t=j/8;row=[]
        for v in bv:
            a=math.atan2((v.co.z-cz)/rz,(v.co.x-cx)/rx)
            x=(1-t)*v.co.x+t*(cx+inner_x*math.cos(a))
            z=(1-t)*v.co.z+t*(cz+inner_z*math.sin(a))
            y=(1-smooth(0,.38,t))*v.co.y+smooth(0,.38,t)*face_y(x,z)
            nv=bm.verts.new((x,y,z));row.append(nv)
            transitions.append((nv,t,a))
        rows.append(row)
        for i in range(len(row)):
            k=(i+1)%len(row);bm.faces.new((rows[-2][i],rows[-2][k],row[k],row[i]))
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    if bm.calc_volume(signed=True)<0:
        for f in bm.faces:f.normal_flip()
    bm.verts.index_update()
    data=[(v.index,t,a,tuple(v.co)) for v,t,a in transitions]
    inner=[v.index for v in rows[-1]]
    bm.to_mesh(o.data);bm.free()
    return {'cx':cx,'cz':cz,'rx':inner_x,'rz':inner_z,'transitions':data,'inner':inner,'label':label}

def eye_point(cx,cz,rx,rz,u,v,offset=0):
    x=cx+rx*u;z=cz+rz*v
    return Vector((x,orbital_y(x,z,cx,cz,rx,rz)-offset,z))

def disc(name,cx,cz,rx,rz,radius,mat,offset):
    verts=[eye_point(cx,cz,rx,rz,0,0,offset)];faces=[];n=64
    for ring in range(1,9):
        r=radius*ring/8
        for i in range(n):
            a=i/n*math.tau;verts.append(eye_point(cx,cz,rx,rz,r*math.cos(a),r*math.sin(a),offset))
    for i in range(n):faces.append((0,1+i,1+(i+1)%n))
    for ring in range(7):
        for i in range(n):
            a=1+ring*n+i;b=1+ring*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    o=mesh(name,verts,faces,mat)
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
    return o

def ellipsoid(name,center,radii,mat,segments=32,rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,radius=1,location=center)
    o=bpy.context.object;o.name=name;o.scale=radii
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for v in o.data.vertices:v.co=o.matrix_world@v.co
    o.matrix_world=Matrix.Identity(4);o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def tube(name,points,radius,mat):
    verts=[];faces=[];n=8
    for i,p in enumerate(points):
        p=Vector(p);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        t.normalize();a=t.cross(Vector((0,-1,0))).normalized();b=t.cross(a).normalized()
        for j in range(n):verts.append(p+radius*(a*math.cos(j/n*math.tau)+b*math.sin(j/n*math.tau)))
    for i in range(len(points)-1):
        for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
    faces.extend([tuple(reversed(range(n))),tuple(range(len(verts)-n,len(verts)))])
    return mesh(name,verts,faces,mat)

def add_blink(head,patch,side):
    k=shape(head,'Blink.'+side,lambda p:p)
    cx,cz,rx,rz=[patch[x] for x in ['cx','cz','rx','rz']]
    for idx,t,a in patch['transitions']:
        p=k.data[idx].co;u=math.cos(a);v=math.sin(a)
        edge=cz-.020+.010*u*u
        dz=edge-(cz+rz*v)
        # Finite transition maintains ownership of cheek/forehead, with a curved seam.
        w=t*t
        p.z+=w*dz
        p.y=face_y(p.x,p.z)-.0175*max(0,1-((p.x-cx)/rx)**2)*smooth(.18,.75,t)
    half=shape(head,'BlinkArc.'+side,lambda p:p)
    basis=head.data.shape_keys.key_blocks['Basis']
    for idx,t,a in patch['transitions']:
        p=(basis.data[idx].co+k.data[idx].co)*.5
        r2=((p.x-cx)/rx)**2+((p.z-cz)/rz)**2
        cover=.014*max(0,1-r2)+.0015*(1-smooth(.98,1.08,r2))
        desired=(1-smooth(.05,.38,t))*p.y+smooth(.05,.38,t)*(face_y(p.x,p.z)-cover)
        half.data[idx].co.y+=desired-p.y
    driver=half.driver_add('value').driver;driver.expression='4*b*(1-b)'
    var=driver.variables.new();var.name='b';var.type='SINGLE_PROP'
    var.targets[0].id_type='KEY';var.targets[0].id=head.data.shape_keys
    var.targets[0].data_path='key_blocks["Blink.'+side+'"].value'
    return k

def add_mouth(head,patch):
    # Neutral is tiny closed mouth; open key is the actual expanded skin opening.
    k=shape(head,'MouthOpen',lambda p:p)
    for idx,t,a in patch['transitions']:
        p=head.data.vertices[idx].co.copy();p.z+=t*t*((.0012-.020)*math.sin(a)+.005*math.cos(a)**2)
        head.data.vertices[idx].co=p
        for old in head.data.shape_keys.key_blocks:
            if old!=k:old.data[idx].co=p
    # Shape was created with open coordinates; preserve those as the open state.
    return k

def bind(o,rig,bone,weight_fn=None):
    for b in rig.data.bones:o.vertex_groups.new(name=b.name)
    for v in o.data.vertices:
        weights=weight_fn(v.co) if weight_fn else {bone:1}
        for n,w in weights.items():
            if w>1e-6:o.vertex_groups[n].add([v.index],w,'REPLACE')
    o.parent=rig;mod=o.modifiers.new('Portable linear skin','ARMATURE');mod.object=rig
    mod.use_deform_preserve_volume=False

def rig_create():
    ad=bpy.data.armatures.new('Shushu_ProbeSkeleton');o=bpy.data.objects.new('Shushu_DeformationRig',ad)
    bpy.context.scene.collection.objects.link(o);bpy.context.view_layer.objects.active=o;o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    def bone(n,h,t,p=None):
        b=ad.edit_bones.new(n);b.head=h;b.tail=t
        if p:b.parent=ad.edit_bones[p]
    bone('Root',(0,0,0),(0,0,.20))
    bone('Head',(0,0,.495),(0,0,.76),'Root')
    for side,s in [('L',1),('R',-1)]:
        bone('Paw.'+side,(s*.168,.015,.462),(s*.32,-.01,.335),'Root')
        bone('Foot.'+side,(s*.14,0,.04),(s*.14,-.09,.04),'Root')
        bone('Ear.'+side,(s*.19,.065,.835),(s*.28,.085,.95),'Head')
    bpy.ops.object.mode_set(mode='OBJECT');o.show_in_front=True
    o['role']='Editable standard-LBS development rig; not final production Rig'
    return o

def support_keys(o,part):
    def rest(p):
        x,y,z=p
        if part.startswith('Leg'):
            w=smooth(.055,.24,z);p.z-=.065*w
            # Compress a broad plush shank instead of folding a thin human knee.
            center=.136 if x>0 else -.136
            bulge=math.sin(math.pi*w)*.14
            p.x=center+(x-center)*(1+bulge)+(1 if x>0 else -1)*.009*w
            p.y=y*(1+.10*math.sin(math.pi*w))+.010*w
        else:
            p.z-=.065
        return p
    shape(o,'SupportedRest',rest)
    def shift(p):
        w=smooth(.035,.24,p.z) if part.startswith('Leg') else 1
        p.x+=.008*w
        return p
    shape(o,'WeightShift',shift)

def evaluated(o):
    bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh()
    v=np.array([ev.matrix_world@p.co for p in m.vertices]);m.calc_loop_triangles()
    t=np.array([p.vertices[:] for p in m.loop_triangles]);ev.to_mesh_clear();return v,t

def reset():
    for o in character:
        if o.data.shape_keys:
            for k in o.data.shape_keys.key_blocks:k.value=0
    for b in rig.pose.bones:b.matrix_basis=Matrix.Identity(4)
    proxy.hide_render=True

def set_key(name,value,objects=None):
    for o in objects or character:
        if o.data.shape_keys and name in o.data.shape_keys.key_blocks:o.data.shape_keys.key_blocks[name].value=value
        if name.startswith('Blink.') and o.data.shape_keys and ('BlinkArc.'+name[-1]) in o.data.shape_keys.key_blocks:
            o.data.shape_keys.key_blocks['BlinkArc.'+name[-1]].value=4*value*(1-value)

def head_pose(x=0,z=0,y=0):
    rot=Euler(tuple(math.radians(a) for a in (x,y,z)),'XYZ').to_matrix().to_4x4()
    rest=rig.data.bones['Head'].matrix_local
    depth=head.data.shape_keys.key_blocks['SupportedRest'].value*.065
    pivot=rest.translation-Vector((0,0,depth))
    rig.pose.bones['Head'].matrix=Matrix.Translation(pivot)@rot@Matrix.Translation(-pivot)@rest
    bpy.context.view_layer.update()

def paw_pose(side,target):
    bone=rig.data.bones['Paw.'+side]
    depth=head.data.shape_keys.key_blocks['SupportedRest'].value*.065
    pivot=bone.head_local-Vector((0,0,depth))
    rotation=(bone.tail_local-bone.head_local).rotation_difference(Vector(target)-pivot).to_matrix().to_4x4()
    rig.pose.bones[bone.name].matrix=Matrix.Translation(pivot)@rotation@Matrix.Translation(-pivot)@bone.matrix_local
    bpy.context.view_layer.update()

def apply_state(name):
    reset()
    if name=='half':set_key('Blink.L',.5);set_key('Blink.R',.5)
    elif name=='closed':set_key('Blink.L',1);set_key('Blink.R',1)
    elif name=='left-closed':set_key('Blink.L',1)
    elif name=='right-closed':set_key('Blink.R',1)
    elif name=='gaze-blink':set_key('Blink.L',.55);set_key('GazeRight',1)
    elif name=='mouth-open':set_key('MouthOpen',1)
    elif name=='settle':set_key('SupportedRest',.38)
    elif name=='rest':set_key('SupportedRest',1)
    elif name=='shift':set_key('WeightShift',1)
    elif name=='offer':paw_pose('L',(.27,-.20,.34));set_key('WeightShift',-.6)
    elif name in ['hold','hold-touch']:
        for side,s in [('L',1),('R',-1)]:paw_pose(side,(s*.080,-.22,.445))
        proxy.hide_render=False
        if name=='hold-touch':head_pose(5,7);set_key('CheekPressure.L',.7)
    elif name=='head-turn':head_pose(8,18,7)
    elif name=='pressure':set_key('CheekPressure.L',1);set_key('BellyPressure',1)

def setup_render():
    s=bpy.context.scene;s.render.engine='CYCLES' if '--cycles' in sys.argv else 'BLENDER_EEVEE'
    if s.render.engine=='CYCLES':s.cycles.samples=24
    s.render.resolution_x=640;s.render.resolution_y=720;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.film_transparent=False
    s.world=bpy.data.worlds.new('Neutral studio');s.world.use_nodes=True
    s.world.node_tree.nodes['Background'].inputs[0].default_value=(.75,.78,.82,1)
    s.world.node_tree.nodes['Background'].inputs[1].default_value=.65
    s.view_settings.view_transform='AgX'
    def light(n,loc,power,size):
        d=bpy.data.lights.new(n,'AREA');d.energy=power;d.shape='DISK';d.size=size
        o=bpy.data.objects.new(n,d);s.collection.objects.link(o);o.location=loc
        o.rotation_euler=(Vector((0,0,.45))-o.location).to_track_quat('-Z','Y').to_euler()
    light('Soft key',(-2,-3,4),320,4);light('Soft fill',(3,-1,2),160,3)
    cam=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));s.collection.objects.link(cam)
    s.camera=cam;cam.data.type='ORTHO';cam.data.lens=55
    return cam

def render(name,direction=(0,-1,0),detail=False):
    target=Vector((0,-.1,.655) if detail else (0,0,.49))
    d=Vector(direction)
    # A slightly elevated orthographic view keeps the support plane visible;
    # an upward-looking orthographic camera lets the floor occlude the feet.
    if not detail and d.z<.08:d.z=.08
    d.normalize();cam.location=target+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
    cam.data.ortho_scale=.56 if detail else 1.17
    bpy.context.scene.render.filepath=str(OUT/'renders'/f'{name}.png')
    bpy.ops.render.render(write_still=True)

def main():
    global character,rig,proxy,cam,head,parts
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/grimo/production/shushu/blender/shushu-candidate-b-feasibility.blend'))
    raw=bpy.data.objects['CandidateB_RawFBX_Copy']
    groups=donor.components(raw.data)
    verts=[v.co.copy() for v in raw.data.vertices];polys=[list(p.vertices) for p in raw.data.polygons]
    # Save original source as a hidden, editable donor collection in the derivative.
    archive=bpy.data.collections.new('SOURCE_B_REFERENCE_ONLY');bpy.context.scene.collection.children.link(archive)
    rawcopy=raw.copy();rawcopy.data=raw.data.copy();archive.objects.link(rawcopy);rawcopy.name='SourceB_UntouchedTopology'
    for o in list(bpy.data.objects):
        if o!=rawcopy:bpy.data.objects.remove(o,do_unlink=True)
    archive.hide_render=True;archive.hide_viewport=True
    white=material('Provisional warm ivory',(.92,.865,.79));pink=material('Provisional sakura',(.85,.36,.46))
    dark=material('Eye plum',(.038,.017,.030),.26);iris_mat=material('Iris warm plum',(.085,.038,.067),.30)
    shine=material('Eye highlights',(.98,.95,.94),.18);nosemat=material('Nose and lip',(.18,.062,.082))
    inside=material('Minimal mouth interior',(.19,.040,.052));tonguemat=material('Mouth floor',(.88,.24,.25))
    parts={};classification=[]
    names=['Head','Torso','Leg.R','Leg.L','Ear.L','Ear.R','Paw.L','Paw.R']
    for n,g in enumerate(groups):
        classification.append({'component':n,'source_faces':len(g),'role':names[n]+' donor exterior' if n<8 else
            ('generated eye caps replaced by controllable eyes' if n in [14,15] else 'thin generated overlapping strip/detail; preserved in hidden source, excluded from repaired exterior')})
        if n>=8:continue
        ids=sorted({i for f in g for i in polys[f]});mapping={old:new for new,old in enumerate(ids)}
        o=mesh('Shushu_'+names[n],[verts[i] for i in ids],[[mapping[i] for i in polys[f]] for f in g],white if n<2 else pink)
        parts[names[n]]=o
        if n==0:
            for v in o.data.vertices:
                x,y,z=v.co
                # Replace damaged orbital/mouth relief only, preserve side/back and lower cheeks.
                region=(1-smooth(.225,.270,abs(x)))*smooth(.505,.545,z)*(1-smooth(.765,.81,z))*(1-smooth(-.09,-.025,y))
                v.co.y=(1-region)*y+region*face_y(x,z)
        remesh(o,.0065 if n==0 else .0070,.28 if n==0 else .32)
        if n in [2,3]:
            for v in o.data.vertices:
                # Donor sole reconstructed as a support surface, not a single rounded point.
                if v.co.z<.012:v.co.z=.001
        o['provenance']='Regional derivative of original Tripo P2.0 Candidate B'
        o['part']=names[n]
    head=parts['Head']
    patches={}
    for side,s in [('L',1),('R',-1)]:
        patches[side]=cut_patch(head,s*.139,.669,.080,.091,.047,.061,'Orbit.'+side)
    mouthpatch=cut_patch(head,0,.582,.050,.041,.026,.020,'Mouth')
    # Preserve the aperture rows. Welding near-coincident corner vertices here
    # changes their morph ownership and introduces a visible eyelid crease.
    from mathutils.kdtree import KDTree
    tree=KDTree(len(head.data.vertices))
    for v in head.data.vertices:tree.insert(v.co,v.index)
    tree.balance()
    for patch in [*patches.values(),mouthpatch]:
        patch['transitions']=[(tree.find(Vector(co))[1],t,a) for idx,t,a,co in patch['transitions']]
    for p in head.data.polygons:p.use_smooth=True
    for side in ['L','R']:add_blink(head,patches[side],side)
    add_mouth(head,mouthpatch)
    # Provisional color fields make volume/identity legible without textures.
    attr=head.data.color_attributes.new(name='IdentityPreview',type='FLOAT_COLOR',domain='POINT')
    for v in head.data.vertices:
        x,y,z=v.co;orb=max(math.exp(-(((x-s*.139)/.071)**2+((z-.684)/.082)**2)*2) for s in [-1,1])
        blush=max(math.exp(-(((x-s*.186)/.068)**2+((z-.592)/.037)**2)*2) for s in [-1,1])
        a=max(.85*orb,.45*blush)*(1-smooth(-.08,-.02,y))
        attr.data[v.index].color=tuple((1-a)*white.diffuse_color[k]+a*pink.diffuse_color[k] for k in range(3))+(1,)
    hm=white.copy();hm.name='Provisional facial color field';head.data.materials[0]=hm
    node=hm.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='IdentityPreview'
    hm.node_tree.links.new(node.outputs['Color'],hm.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    character=list(parts.values());facial=[]
    for side,s in [('L',1),('R',-1)]:
        cx=s*.139;cz=.669;rx=.047;rz=.061
        eye=disc('Shushu_Eye.'+side,cx,cz,rx,rz,.999,dark,0)
        iris=disc('Shushu_Iris.'+side,cx,cz,rx,rz,.78,iris_mat,.00025)
        for label,dx,dz in [('GazeLeft',-.006,0),('GazeRight',.006,0),('GazeUp',0,.004),('GazeDown',0,-.004)]:
            def gaze(p,dx=dx,dz=dz):
                p.x+=dx;p.z+=dz;p.y=orbital_y(p.x,p.z,cx,cz,rx,rz)-.00030;return p
            shape(iris,label,gaze)
        highlights=[]
        for hn,u,v,r in [('Main',-.29,.38,.007),('Small',.34,-.32,.0025)]:
            p=eye_point(cx,cz,rx,rz,u,v,.001)
            h=ellipsoid('Shushu_Highlight'+hn+'.'+side,p,(r,.0001,r),shine,24,12)
            for v in h.data.vertices:v.co.y=orbital_y(v.co.x,v.co.z,cx,cz,rx,rz)-.0005
            for label,dx,dz in [('GazeLeft',-.006,0),('GazeRight',.006,0),('GazeUp',0,.004),('GazeDown',0,-.004)]:
                shape(h,label,lambda p,dx=dx,dz=dz:Vector((p.x+dx,orbital_y(p.x+dx,p.z+dz,cx,cz,rx,rz)-.0005,p.z+dz)))
            highlights.append(h)
        # Soft dark upper margin follows the opening; no independent floating lid shell.
        pts=[]
        for i in range(33):
            a=i/32*math.pi;x=cx+rx*math.cos(a);z=cz+rz*math.sin(a)
            pts.append((x,face_y(x,z)-.001,z))
        lash=tube('Shushu_LidMargin.'+side,pts,.0013,nosemat)
        closekey=shape(lash,'Blink.'+side,lambda p:p)
        for idx,p in enumerate(closekey.data):
            center=Vector(pts[idx//8]);offset=p.co-center
            u=max(-1,min(1,(center.x-cx)/rx));z=cz-.020+.010*u*u
            y=face_y(center.x,z)-.0175*max(0,1-u*u)-.0018
            p.co=Vector((center.x,y,z))+offset
        facial.extend([eye,iris,*highlights,lash])
    nose=ellipsoid('Shushu_Nose',(0,face_y(0,.623)-.008,.624),(.013,.009,.0075),nosemat)
    facial.append(nose)
    # Minimal recessed mouth bowl with moving perimeter and a shallow pink floor.
    v=[(0,face_y(0,.582)+.013,.582)];f=[];n=48
    for i in range(n):
        a=i/n*math.tau;x=.026*math.cos(a);z=.582+.005*math.cos(a)**2+.0012*math.sin(a)
        v.append((x,face_y(x,z)+.0005,z))
    for i in range(n):f.append((0,i+1,(i+1)%n+1))
    mouth=mesh('Shushu_MouthInterior',v,f,inside)
    openkey=shape(mouth,'MouthOpen',lambda p:p)
    for i,p in enumerate(list(openkey.data)[1:]):
        a=i/n*math.tau;p.co.z=.582+.020*math.sin(a);p.co.y=face_y(p.co.x,p.co.z)+.0005
    facial.append(mouth)
    tongue=ellipsoid('Shushu_MouthFloor',(0,face_y(0,.572)+.005,.572),(.016,.002,.002),tonguemat)
    # Closed floor remains inside head; opening brings it into the minimal cavity.
    for v in tongue.data.vertices:v.co.z=.582+(v.co.z-.572)*.08;v.co.y+=.006
    shape(tongue,'MouthOpen',lambda p:Vector((p.x,p.y-.006,.568+(p.z-.582)/.08)))
    facial.append(tongue)
    pts=[(0,face_y(0,z)-.001,z) for z in [.618,.612,.606]]
    facial.append(tube('Shushu_Philtrum',pts,.001,nosemat))
    character.extend(facial)
    rig=rig_create()
    for name,o in parts.items():
        if name=='Head':
            def weights(p):
                h=smooth(.475,.54,p.z);return {'Head':h,'Root':1-h}
            bind(o,rig,'Head',weights)
        elif name.startswith('Ear'):bind(o,rig,name)
        elif name.startswith('Paw'):bind(o,rig,name)
        elif name.startswith('Leg'):
            def foot_weights(p,name=name):
                r=smooth(.055,.095,p.z);return {'Root':r,'Foot.'+name[-1]:1-r}
            bind(o,rig,'Root',foot_weights)
        else:bind(o,rig,'Root')
    for o in facial:bind(o,rig,'Head')
    for name,o in parts.items():support_keys(o,name)
    for o in facial:support_keys(o,'Head')
    for o in character:
        o.data.name=o.name
        o['production_id']=o.name
    def cheek(p):
        x,y,z=p;q=((x-.212)/.073)**2+((y+.155)/.09)**2+((z-.577)/.050)**2
        guard=(1-smooth(.595,.619,z))*smooth(.155,.19,x)
        p.y+=.018*math.exp(-q*2)*guard;return p
    shape(head,'CheekPressure.L',cheek)
    def belly(p):
        q=(p.x/.12)**2+((p.y+.239)/.065)**2+((p.z-.325)/.11)**2
        p.y+=.025*math.exp(-q*2);return p
    shape(parts['Torso'],'BellyPressure',belly)
    # A large sphere exceeded the rigid short-paw reach. Fit a thin actual handle
    # to the existing paw surfaces; never expand the arms or pass a prop through belly.
    mounts=[]
    for side,s in [('R',-1),('L',1)]:
        paw_pose(side,(s*.080,-.22,.445))
        pv,pt=evaluated(parts['Paw.'+side])
        tree=BVHTree.FromPolygons([Vector(p) for p in pv],pt.tolist(),all_triangles=True)
        point,normal,idx,dist=tree.find_nearest(Vector((0,-.290,.445)))
        mounts.append(point+normal*.006)
    mat=material('Holding proxy',(.32,.48,.38))
    points=[mounts[0].lerp(mounts[1],i/16)+Vector((0,-.008*math.sin(math.pi*i/16),0)) for i in range(17)]
    stem=tube('HoldingStem',points,.006,mat)
    caps=[ellipsoid('HoldingEnd',p,(.006,.006,.006),mat,24,12) for p in mounts]
    vs=[];fs=[]
    for o in [stem,*caps]:
        start=len(vs);vs.extend([v.co.copy() for v in o.data.vertices]);fs.extend([[start+i for i in f.vertices] for f in o.data.polygons])
        bpy.data.objects.remove(o,do_unlink=True)
    proxy=mesh('Reachable_Holding_Proxy',vs,fs,mat)
    proxy['role']='Reachable tangent-contact test handle; not approved bouquet/food/Gift'
    proxy['contact_mounts']=json.dumps([list(p) for p in mounts])
    for bone in rig.pose.bones:bone.matrix_basis=Matrix.Identity(4)
    cam=setup_render()
    ground=mesh('ReviewGround',[(-3,-3,0),(3,-3,0),(3,3,0),(-3,3,0)],[(0,1,2,3)],material('Review ground',(.76,.79,.83)))
    gm=ground.data.materials[0];nodes=gm.node_tree.nodes
    checker=nodes.new('ShaderNodeTexChecker');checker.inputs['Scale'].default_value=40
    checker.inputs['Color1'].default_value=(.70,.73,.77,1)
    checker.inputs['Color2'].default_value=(.77,.80,.84,1)
    gm.node_tree.links.new(checker.outputs['Color'],nodes['Principled BSDF'].inputs['Base Color'])
    bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
    bpy.context.scene['units']='One height normalization unit; physical character size not approved'
    bpy.context.scene['status']='Geometry candidate; Human identity/naturalness Gate pending; Game Neutral unresolved'
    states=[('neutral',(0,-1,0),False),('neutral',(1,-1,.10),False),('neutral',(1,0,.0),False),
            ('neutral',(0,1,.04),False),('half',(0,-1,0),True),('closed',(0,-1,0),True),
            ('left-closed',(0,-1,0),True),('right-closed',(0,-1,0),True),('gaze-blink',(1,-3,0),True),
            ('mouth-open',(0,-1,0),True),('settle',(0,-1,0),False),('rest',(0,-1,0),False),
            ('rest',(1,0,0),False),('rest',(1,1,-.08),False),('offer',(1,-2,.08),False),
            ('hold',(0,-1,0),False),('hold',(1,0,0),False),('hold-touch',(1,-2,.08),False),
            ('head-turn',(1,-2,0),False),('pressure',(0,-1,0),False)]
    report={'input_production_head':'749675cac5ebdb07587e715eb2cb59bfcae2768f','blender':bpy.app.version_string,
            'source_classification':classification,'states':{},'geometry':{},'final_rig':False,'human_gate':'PENDING'}
    reset()
    base={o.name:evaluated(o)[0] for o in character}
    for name,o in parts.items():
        v,t=evaluated(o);report['geometry'][name]={'vertices':len(v),'triangles':len(t),'bounds':[v.min(0).tolist(),v.max(0).tolist()]}
    for index,(state,direction,detail) in enumerate(states):
        apply_state(state)
        if '--no-render' not in sys.argv:render(f'{index:02d}-{state}',direction,detail)
        if state not in report['states']:
            row={}
            for part in ['Torso','Leg.L','Leg.R','Paw.L','Paw.R','Head']:
                o=parts[part];v,t=evaluated(o);vb=base[o.name]
                es=np.array([e.vertices[:] for e in o.data.edges]);before=np.linalg.norm(vb[es[:,0]]-vb[es[:,1]],axis=1)
                meaningful=before>1e-5
                ratio=np.linalg.norm(v[es[meaningful,0]]-v[es[meaningful,1]],axis=1)/before[meaningful]
                row[part]={'minimum_z':float(v[:,2].min()),'edge_ratio_min_max':[float(ratio.min()),float(ratio.max())],
                           'max_displacement':float(np.linalg.norm(v-vb,axis=1).max())}
                if part.startswith('Leg'):
                    sole=vb[:,2]<.012;row[part]['sole_max_displacement']=float(np.linalg.norm(v[sole]-vb[sole],axis=1).max())
                    row[part]['sole_samples']=int(sole.sum())
            report['states'][state]=row
    reset()
    report['recovery_max_error']=max(float(np.linalg.norm(evaluated(o)[0]-base[o.name],axis=1).max()) for o in character)
    report['plush_feature_displacement']={}
    apply_state('pressure')
    for o in facial:report['plush_feature_displacement'][o.name]=float(np.linalg.norm(evaluated(o)[0]-base[o.name],axis=1).max())
    reset()
    # Focused combined portable proof, not a finished Motion library.
    scene=bpy.context.scene;scene.render.fps=24;scene.frame_start=1;scene.frame_end=120
    timeline=[(1,'neutral'),(9,'half'),(13,'closed'),(19,'neutral'),(25,'left-closed'),(31,'right-closed'),
              (37,'gaze-blink'),(43,'mouth-open'),(49,'neutral'),(61,'settle'),(73,'rest'),(85,'neutral'),
              (91,'offer'),(99,'hold'),(105,'hold-touch'),(111,'pressure'),(120,'neutral')]
    for frame,state in timeline:
        apply_state(state)
        for b in rig.pose.bones:
            b.keyframe_insert('location',frame=frame);b.keyframe_insert('rotation_quaternion' if b.rotation_mode=='QUATERNION' else 'rotation_euler',frame=frame)
            b.keyframe_insert('scale',frame=frame)
        for o in character:
            if o.data.shape_keys:
                for k in list(o.data.shape_keys.key_blocks)[1:]:k.keyframe_insert('value',frame=frame)
    # Shared scene timeline contains bones plus every mesh's morphs simultaneously.
    scene.frame_set(1)
    for o in [rig,*character]:o.select_set(True)
    for o in bpy.context.selected_objects:
        if o not in [rig,*character]:o.select_set(False)
    GLB.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,
        export_animations=True,export_animation_mode='SCENE',export_frame_range=True,
        export_force_sampling=True,export_skins=True,export_morph=True,export_yup=True,
        export_all_influences=False,export_extras=True,export_anim_scene_split_object=False)
    scene.frame_set(1);proxy.hide_render=True
    bpy.ops.object.select_all(action='DESELECT');head.select_set(True);bpy.context.view_layer.objects.active=head
    ASSET.parent.mkdir(parents=True,exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    (OUT/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
    print('SHUSHU_GEOMETRY_SAVED',str(ASSET))

if __name__=='__main__':main()
