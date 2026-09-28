"""Carol v004 regional full-3D fleece studies, driven by current authority.

Donor: snowtone-ai/grimoire@15bfa8e4c3a8ba24c246fe806bd125b307d8f076
scripts/grimo/build-carol-reference.py: surface, ring_point, locks_depth,
body_front, head_front, volume_paint. Current pixels and locks replace all old
coordinates. The original radial port is retained as a diagnostic. Active
--spatial --solid-locks studies use an inset shared guide and regional locks,
following the Human's subsequent method-flexibility instruction.
"""
import bpy
import bmesh
import numpy as np
import math
import json
import hashlib
import sys
import os
import time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/production/carol/evidence/normal-fleece-v004'
WORK = ROOT/'artifacts/carol-fleece-v004'
ASSET = ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v004.blend'
SKIN = ASSET.with_name('carol-skin-final-v002.blend')
SKIN_SHA = '321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a'
REF = ROOT/'assets/grimo/source/carol/approved-3d'
ARGS = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['build']
INVENTORY = json.loads((OUT/'tuft-inventory.json').read_text())
SCALE = 1/1012
SEGMENTS = 384
RINGS = 96
CACHE = {}
SURFACES = {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arg(key, default):
    return ARGS[ARGS.index(key)+1] if key in ARGS else default


def smooth(x):
    t = np.clip(x, 0, 1)
    return t*t*(3-2*t)


def pixels(path):
    key = str(path)
    if key not in CACHE:
        im = bpy.data.images.load(key,check_existing=True)
        data = np.empty(im.size[0]*im.size[1]*4,np.float32)
        im.pixels.foreach_get(data)
        CACHE[key] = data.reshape(im.size[1],im.size[0],4)[::-1].copy()
    return CACHE[key]


def sample(pic,x,y):
    h,w = pic.shape[:2]
    x=np.clip(x,0,w-1.001);y=np.clip(y,0,h-1.001)
    ix=x.astype(int);iy=y.astype(int)
    fx=(x-ix)[...,None];fy=(y-iy)[...,None]
    return (pic[iy,ix]*(1-fx)+pic[iy,ix+1]*fx)*(1-fy)+(pic[iy+1,ix]*(1-fx)+pic[iy+1,ix+1]*fx)*fy


def linear(rgb):
    rgb=np.asarray(rgb)
    return np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)


def parent_keep(ob,parent):
    bpy.context.view_layer.update()
    matrix=ob.matrix_world.copy();ob.parent=parent;ob.matrix_world=matrix


def empty(name,location):
    ob=bpy.data.objects.new(name,None)
    bpy.context.scene.collection.objects.link(ob);ob.location=location
    return ob


def make_mesh(name,verts,faces):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:p.use_smooth=True
    return ob


def skin_tree(legs=False):
    vertices=[];faces=[]
    for ob in bpy.context.scene.objects:
        if ob.name!='CENTRAL_CHASSIS' and not (legs and ob.name.startswith(('FORE_','HIND_'))):continue
        ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
        offset=len(vertices)
        vertices.extend(ob.matrix_world@v.co for v in me.vertices)
        faces.extend([offset+i for i in p.vertices] for p in me.polygons)
        ev.to_mesh_clear()
    return BVHTree.FromPolygons(vertices,faces)


def boundary_radii(mask,center):
    """Donor surface(): last authority-mask hit along each radial sample."""
    h,w=mask.shape;cx,cy=center
    radii=[]
    samples=np.arange(.5,max(h,w),.5)
    for i in range(SEGMENTS):
        a=i*math.tau/SEGMENTS
        sx=(cx+math.cos(a)*samples).astype(int)
        sy=(cy+math.sin(a)*samples).astype(int)
        valid=(sx>=0)&(sx<w)&(sy>=0)&(sy<h)
        hits=samples[valid][mask[sy[valid],sx[valid]]]
        radii.append(float(hits[-1]) if len(hits) else 1.)
    radii=np.array(radii)
    return .14*np.roll(radii,1)+.72*radii+.14*np.roll(radii,-1)


def ring_point(center,radii,angle,r):
    """Exact donor r**12 silhouette-to-ellipse interpolation."""
    rx=(radii[0]+radii[len(radii)//2])/2
    ry=(radii[len(radii)//4]+radii[3*len(radii)//4])/2
    ca=np.cos(angle);sa=np.sin(angle)
    radius=np.interp(angle/math.tau*len(radii),np.arange(len(radii)+1),np.r_[radii,radii[0]])
    ellipse=1/np.sqrt((ca/rx)**2+(sa/ry)**2)
    sample_angles=np.arange(len(radii))*math.tau/len(radii)
    base=1/np.sqrt((np.cos(sample_angles)/rx)**2+(np.sin(sample_angles)/ry)**2)
    # Full-depth extension requires a monotonic radial map. An interior ellipse
    # inside every boundary radius preserves the donor fade without foldovers.
    ellipse*=min(1,float(np.min(radii/base))*.985)
    radius=ellipse+(radius-ellipse)*r**12
    return center[0]+ca*radius*r,center[1]+sa*radius*r


def locks_depth(x,y,locks):
    """Donor fifth-power smooth maximum; current locks add measured orientation."""
    total=np.zeros(np.broadcast_shapes(np.shape(x),np.shape(y)))
    for lock in locks:
        cx,cy=lock['center_px'];rx=lock['width_px']/2;ry=lock['height_px']/2
        a=math.radians(lock['orientation_deg']);dx=x-cx;dy=y-cy
        u=math.cos(a)*dx+math.sin(a)*dy;v=-math.sin(a)*dx+math.cos(a)*dy
        value=lock['relief_H']*np.exp(-2*((u/rx)**2+(v/ry)**2))
        total+=value**5
    return total**.2


def body_front(x,y,r):
    # The torso sits behind the accepted full head, with genuine rear volume.
    setback=.22*np.exp(-((y-710)/280)**4)
    return .61+setback-.50*np.sqrt(np.maximum(0,1-r*r))-locks_depth(x,y,BODY_LOCKS)


def head_front(x,y,r):
    # Same rounded donor base plus measured locks; the face is excluded in the
    # parameter-domain mask, never excavated from a completed exterior shell.
    return .38-.32*np.sqrt(np.maximum(0,1-r*r))-locks_depth(x,y,HEAD_LOCKS)


def depth_field(name,x,y,r,front=True):
    if front:
        return head_front(x,y,r) if name=='HeadFleece' else body_front(x,y,r)
    center,radii=SURFACES[name]
    angle=np.mod(np.arctan2(y-center[1],x-center[0]),math.tau)
    rimx,rimy=ring_point(center,radii,angle,np.ones_like(r))
    fn=head_front if name=='HeadFleece' else body_front
    base=fn(center[0],center[1],1)
    seam=fn(rimx,rimy,np.ones_like(r))
    depth=.26 if name=='HeadFleece' else .53-.22*np.exp(-((y-710)/280)**4)
    nz=np.sqrt(np.maximum(0,1-r*r))
    if name=='BodyFleece':
        if 'rear-depth-profile' not in CACHE:
            rows=np.arange(1254,dtype=float)
            va=np.where(rows>=center[1],math.pi/2,3*math.pi/2)
            lo=np.zeros_like(rows);hi=np.ones_like(rows)
            for _ in range(22):
                mid=(lo+hi)/2
                _,py=ring_point(center,radii,va,mid)
                below=abs(py-center[1])<abs(rows-center[1])
                lo=np.where(below,mid,lo);hi=np.where(~below,mid,hi)
            rv=(lo+hi)/2
            profile=np.array(json.loads((WORK/'side-profile.json').read_text()))
            z=(1161-rows)/1012
            target=np.interp(z,profile[:,0],profile[:,2])
            _,rimy=ring_point(center,radii,va,np.ones_like(rows))
            rim=body_front(np.full_like(rows,center[0]),rimy,np.ones_like(rows))
            origin=base+(rim-base)*rv**12
            bottom=smooth((z-.052)/.055)
            CACHE['rear-depth-profile']=(target-origin)*bottom/np.maximum(.045,np.sqrt(np.maximum(0,1-rv*rv)))
        depth=np.interp(y,np.arange(1254),CACHE['rear-depth-profile'])
    sx=base+(seam-base)*r**12+depth*nz
    # Side locks drive one attached spatial relief field on the reverse/lateral
    # hemisphere. They are not duplicated view-specific meshes.
    relief=locks_depth(145+sx*918,999-(1161-y)*918/1012,INVENTORY['side'])
    return sx+relief*nz*.55


def shader(name,im=None,attribute=None,lit=.22,color=None):
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    ns=mat.node_tree.nodes;lk=mat.node_tree.links;ns.clear()
    out=ns.new('ShaderNodeOutputMaterial')
    diffuse=ns.new('ShaderNodeBsdfDiffuse');diffuse.inputs['Roughness'].default_value=.65
    emit=ns.new('ShaderNodeEmission')
    mix=ns.new('ShaderNodeMixShader');mix.inputs[0].default_value=lit
    if im:
        tex=ns.new('ShaderNodeTexImage');tex.image=im
        lk.new(tex.outputs['Color'],diffuse.inputs['Color']);lk.new(tex.outputs['Color'],emit.inputs['Color'])
    elif attribute:
        tex=ns.new('ShaderNodeVertexColor');tex.layer_name=attribute
        lk.new(tex.outputs['Color'],diffuse.inputs['Color']);lk.new(tex.outputs['Color'],emit.inputs['Color'])
    else:
        diffuse.inputs['Color'].default_value=(*linear(color),1)
        emit.inputs['Color'].default_value=(*linear(color),1)
    lk.new(emit.outputs[0],mix.inputs[1]);lk.new(diffuse.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],out.inputs['Surface'])
    return mat


def volume_paint(name,center,radii):
    """Donor opaque spherical atlas, extended with actual lateral authority."""
    size=768 if '--draft' in ARGS else 1536
    ty,tx=np.mgrid[0:size,0:size]
    angle=(tx+.5)/size*math.tau
    theta=(1-(ty+.5)/size)*math.pi
    r=np.sin(theta)
    x,y=ring_point(center,radii,angle,r)
    d=np.where(theta<math.pi/2,depth_field(name,x,y,r),depth_field(name,x,y,r,False))
    if name=='BodyFleece':x=lateral_projection(x,y,d,r)
    front=sample(pixels(WORK/'pigment-front.png'),x,y)[:,:,:3]
    side=sample(pixels(WORK/'pigment-side.png'),145+d*918,999-(1161-y)*918/1012)[:,:,:3]
    confidence=smooth((np.cos(theta)+.02)/.28)
    # Unseen rear uses the lateral watercolor, kept pale at the polar cap.
    result=side*(1-confidence[...,None])+front*confidence[...,None]
    rgba=np.ones((size,size,4),np.float32);rgba[:,:,:3]=linear(result)
    im=bpy.data.images.new(name+' opaque spatial watercolor',width=size,height=size,alpha=False,float_buffer=True)
    im.colorspace_settings.name='Linear Rec.709'
    im.pixels.foreach_set(rgba.ravel());im.pack()
    return shader(name+' donor opaque watercolor',im=im,lit=.16)


def lateral_projection(u,v,depth,r):
    mask=pixels(WORK/'body-mask.png')[:,:,0]>.5
    widths=[]
    for row in mask:
        hits=np.where(row)[0]
        widths.append([hits[0],hits[-1]] if len(hits) else [630,630])
    widths=np.array(widths)
    side=locks_depth(145+depth*918,999-(1161-v)*918/1012,INVENTORY['side'])
    world_y=(630-u)/1012
    weight=smooth((abs(world_y)-.20)/.22)*(1-smooth((np.sqrt(np.maximum(0,1-r*r))-.68)/.22))
    edge=np.where(world_y>0,np.interp(v,np.arange(len(widths)),widths[:,0]),np.interp(v,np.arange(len(widths)),widths[:,1]))
    room=abs(u-edge)/1012
    delta=room*(1-np.exp(-side*1.8*weight/np.maximum(.001,room)))
    return u-np.sign(world_y)*delta*1012


def lateral_field(verts,radial,tree):
    """Local Side locks on the donor surface, without longitudinal extrusion."""
    if 'side-radii' not in CACHE:
        mask=pixels(WORK/'silhouette-side.png')[:,:,0]>.5
        CACHE['side-radii']=boundary_radii(mask,(705,525))
    radii=CACHE['side-radii'];center=(705,525)
    x=145+verts[:,0]*918;y=999-verts[:,2]*918
    angle=np.mod(np.arctan2(y-center[1],x-center[0]),math.tau)
    distance=np.hypot(x-center[0],y-center[1])
    lo=np.zeros(len(verts));hi=np.ones(len(verts))
    for _ in range(22):
        mid=(lo+hi)/2
        px,py=ring_point(center,radii,angle,mid)
        inside=np.hypot(px-center[0],py-center[1])<distance
        lo=np.where(inside,mid,lo);hi=np.where(inside,hi,mid)
    r=(lo+hi)/2
    target=.53*np.sqrt(np.maximum(0,1-r*r))+locks_depth(x,y,INVENTORY['side'])*1.1
    weight=smooth((verts[:,0]-.36)/.25)*smooth((abs(verts[:,1])-.08)/.20)*(1-smooth((radial-.90)/.095))
    verts[:,1]=np.sign(verts[:,1])*(abs(verts[:,1])*(1-weight)+target*weight)
    for i,(px,py,pz) in enumerate(verts):
        if abs(py)<.10:continue
        sign=1 if py>0 else -1
        hit,_,_,_=tree.ray_cast(Vector((px,sign*2,pz)),Vector((0,-sign,0)),4)
        if hit and abs(hit.y)>abs(py):verts[i,1]=sign*(abs(hit.y)+.018)
    return verts


def attached_side_pigment(ob):
    """Blend the spherical donor atlas with Side pigment on lateral normals.

    Both coordinates and weights are baked in the object's rest mesh, not tied
    to the render camera. The front/rear atlas remains the primary paint domain.
    """
    me=ob.data;me.update()
    uv=me.uv_layers.new(name='AuthoritySide')
    color=me.color_attributes.new(name='SidePigmentWeight',type='FLOAT_COLOR',domain='POINT')
    for ve in me.vertices:
        nx,ny,_=ve.normal
        w=abs(ny)**6/(abs(nx)**6+abs(ny)**6+1e-10)
        if nx>0:w=1
        color.data[ve.index].color=(w,w,w,1)
    for loop in me.loops:
        co=me.vertices[loop.vertex_index].co
        uv.data[loop.index].uv=((145+co.x*918)/1448,1-(999-co.z*918)/1086)
    im=bpy.data.images.load(str(WORK/'pigment-side.png'),check_existing=True);im.pack()
    mat=me.materials[0];nodes=mat.node_tree.nodes;links=mat.node_tree.links
    base=next(n for n in nodes if n.type=='TEX_IMAGE')
    primary=nodes.new('ShaderNodeUVMap');primary.uv_map='VolumePaint';links.new(primary.outputs['UV'],base.inputs['Vector'])
    tex=nodes.new('ShaderNodeTexImage');tex.image=im
    coords=nodes.new('ShaderNodeUVMap');coords.uv_map=uv.name;links.new(coords.outputs['UV'],tex.inputs['Vector'])
    weight=nodes.new('ShaderNodeVertexColor');weight.layer_name=color.name
    mix=nodes.new('ShaderNodeMixRGB');links.new(weight.outputs['Color'],mix.inputs[0])
    links.new(base.outputs['Color'],mix.inputs[1]);links.new(tex.outputs['Color'],mix.inputs[2])
    for node in nodes:
        if node.type in ['BSDF_DIFFUSE','EMISSION']:links.new(mix.outputs['Color'],node.inputs['Color'])


def surface(name,mask,center,parent,front,tree,exclusion=None):
    """Port of donor surface(): front/rear radial hemispheres and shared seam.

    Face exclusion is applied to the input domain. Its boundary rolls a short
    distance into the accepted Skin, so the volume has a closed inner return.
    """
    radii=boundary_radii(mask,center)
    SURFACES[name]=(center,radii)
    angles=np.arange(SEGMENTS)*math.tau/SEGMENTS
    inner=np.zeros(SEGMENTS)
    if exclusion is not None:
        # Invert ring_point on the current face-mask contour before tessellation.
        face_radius=boundary_radii(exclusion,center)
        low=np.zeros(SEGMENTS);high=np.ones(SEGMENTS)
        for _ in range(24):
            middle=(low+high)/2
            px,py=ring_point(center,radii,angles,middle)
            dist=np.hypot(px-center[0],py-center[1])
            low=np.where(dist<face_radius,middle,low)
            high=np.where(dist>=face_radius,middle,high)
        inner=(low+high)/2
    rr=[];aa=[];isfront=[]
    for hemisphere in [True,False]:
        for j in range(RINGS+1):
            r=np.sin((j/RINGS)*math.pi/2)
            radial=inner+(1-inner)*r if exclusion is not None else np.full(SEGMENTS,r)
            rr.extend(radial);aa.extend(angles);isfront.extend([hemisphere]*SEGMENTS)
    rr=np.array(rr);aa=np.array(aa);isfront=np.array(isfront)
    u,v=ring_point(center,radii,aa,rr)
    depth=np.where(isfront,front(u,v,rr),depth_field(name,u,v,rr,False))
    verts=np.stack((depth,(630-u)*SCALE,(1161-v)*SCALE),axis=1)
    if name=='BodyFleece':
        # Same closed donor volume, displaced along the lateral normal. This
        # supplies actual Side lock relief rather than stretching Front ridges.
        verts[:,1]=(630-lateral_projection(u,v,depth,rr))/1012
        verts=lateral_field(verts,rr,skin_tree(legs=True))
        lower=skin_tree(legs=True)
        for i,(px,py,pz) in enumerate(verts[:(RINGS+1)*SEGMENTS]):
            if pz>=.37:continue
            hy=math.copysign(min(.19,max(.08,abs(py))),py)
            hit,_,_,_=lower.ray_cast(Vector((-1,hy,max(.09,pz))),Vector((1,0,0)),3)
            if hit:
                target=hit.x-.025+.30*(abs(py)/.6)**2
                w=(1-float(smooth((pz-.19)/.18)))*float(smooth((pz-.055)/.045))
                delta=min(0,(target-px)*w)
                verts[i,0]+=delta
                verts[i+(RINGS+1)*SEGMENTS,0]+=delta*rr[i]**12
    if exclusion is not None:
        relief=locks_depth(u,v,HEAD_LOCKS)
        for i in range((RINGS+1)*SEGMENTS):
            px,py,pz=verts[i]
            hit,_,_,_=tree.ray_cast(Vector((-1,py,pz)),Vector((1,0,0)),3)
            if hit:
                delta=min(0,hit.x-.012-relief[i]*.95-px)
                verts[i,0]+=delta
                verts[i+(RINGS+1)*SEGMENTS,0]+=delta
        # The real Skin supplies contact depth at every point of the mask edge.
        ix,iy=ring_point(center,radii,angles,inner)
        contact=[]
        for px,py in zip(ix,iy):
            hit,_,_,_=tree.ray_cast(Vector((-1,(630-px)*SCALE,(1161-py)*SCALE)),Vector((1,0,0)),3)
            contact.append(hit.x if hit else .21)
        contact=np.array(contact)
        for hemisphere in [0,1]:
            for j in range(RINGS+1):
                sl=slice((hemisphere*(RINGS+1)+j)*SEGMENTS,(hemisphere*(RINGS+1)+j+1)*SEGMENTS)
                r=np.sin(j/RINGS*math.pi/2)
                weight=1-smooth(r/.12)
                target=contact+(.018 if hemisphere else -.004)
                verts[sl,0]=verts[sl,0]*(1-weight)+target*weight
    else:
        # Clamp the unseen front body behind the face only where Skin occupies
        # its projection; it remains a separate torso mass, as in the donor.
        for i in range((RINGS+1)*SEGMENTS):
            px,py,pz=verts[i]
            fu=int(np.clip(630-py*1012,0,1253));fv=int(np.clip(1161-pz*1012,0,1253))
            if pixels(WORK/'face-mask.png')[fv,fu,0]>.5:
                hit,_,_,_=tree.ray_cast(Vector((-1,py,pz)),Vector((1,0,0)),3)
                if hit:verts[i,0]=max(px,hit.x+.095)
    faces=[];stride=(RINGS+1)*SEGMENTS
    for hemi in [0,1]:
        for j in range(RINGS):
            for i in range(SEGMENTS):
                a=hemi*stride+j*SEGMENTS+i;b=hemi*stride+j*SEGMENTS+(i+1)%SEGMENTS
                f=(a,b,b+SEGMENTS,a+SEGMENTS)
                faces.append(tuple(reversed(f)) if hemi else f)
    for i in range(SEGMENTS):
        a=RINGS*SEGMENTS+i;b=RINGS*SEGMENTS+(i+1)%SEGMENTS
        faces.append((a,b,b+stride,a+stride))
        faces.append((i,i+stride,(i+1)%SEGMENTS+stride,(i+1)%SEGMENTS))
    ob=make_mesh(name,verts,faces)
    ob.data.materials.append(volume_paint(name,center,radii))
    uv=ob.data.uv_layers.new(name='VolumePaint')
    for poly in ob.data.polygons:
        us=[aa[k]/math.tau for k in poly.vertices]
        crosses=max(us)-min(us)>.5
        for li in poly.loop_indices:
            k=ob.data.loops[li].vertex_index
            a=aa[k]/math.tau
            if crosses and a<.5:a+=1
            theta=math.asin(min(1,rr[k]));theta=theta if isfront[k] else math.pi-theta
            uv.data[li].uv=(a,1-theta/math.pi)
    # Weld coincident poles and the silhouette seam after UV assignment.
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    attached_side_pigment(ob)
    ob['construction']='Pinned donor radial mask/r**12/locks_depth closed volume; Skin-constrained extension'
    ob['reference_center']=center;ob['motion_owner']='head' if exclusion is not None else 'torso'
    for label,sign in [('touch_L',1),('touch_R',-1)]:
        group=ob.vertex_groups.new(name=label)
        for ve in ob.data.vertices:
            weight=float(smooth((ve.co.y*sign+.05)/.1))
            if weight>0:group.add([ve.index],weight,'REPLACE')
    parent_keep(ob,parent)
    return ob


def vertex_paint(ob,front_weight=True,lit=1):
    pic=pixels(REF/'carol_front.png')
    sidepic=pixels(REF/'carol_side.png')
    pts=np.array([tuple(ob.matrix_world@v.co) for v in ob.data.vertices])
    front=sample(pic,630-pts[:,1]*1012,1161-pts[:,2]*1012)[:,:3]
    side=sample(sidepic,145+pts[:,0]*918,999-pts[:,2]*918)[:,:3]
    w=1-smooth((abs(pts[:,1])-.17)/.16)
    colors=linear(front*w[:,None]+side*(1-w[:,None]))
    attr=ob.data.color_attributes.new(name='CurrentAuthorityPaint',type='FLOAT_COLOR',domain='POINT')
    attr.data.foreach_set('color',np.column_stack((colors,np.ones(len(colors)))).ravel())
    ob.data.materials.clear();ob.data.materials.append(shader(ob.name+' current authority',attribute=attr.name,lit=lit))
    for poly in ob.data.polygons:poly.material_index=0


def ornaments(tree):
    mat=shader('Soft gold',color=(1,.84,.38),lit=.32)
    items=[('CrownStar',627,273,65),('BrowStar',678,469,58),('LeftStar',151,628,50),('BellyStar',276,962,49),('ChinStar',629,1006,46)]
    for name,x,y,radius in items:
        cy=(630-x)*SCALE;cz=(1161-y)*SCALE
        hit,_,_,_=tree.ray_cast(Vector((-1,cy,cz)),Vector((1,0,0)),3)
        if hit is None:continue
        verts=[]
        for d in [hit.x-.012,hit.x+.014]:
            for i in range(10):
                a=i*math.pi/5;r=radius*SCALE*(1 if i%2==0 else .50)
                verts.append((d,cy+math.sin(a)*r,cz+math.cos(a)*r))
        faces=[tuple(range(9,-1,-1)),tuple(range(10,20))]
        faces.extend((i,(i+1)%10,(i+1)%10+10,i+10) for i in range(10))
        ob=make_mesh(name,verts,faces);ob.data.materials.append(mat)
        bevel=ob.modifiers.new('Soft rounded gold edge','BEVEL');bevel.width=.008;bevel.segments=4
    # Crescent is a closed strip; its inner concavity is real geometry.
    cy=(630-318)*SCALE;cz=(1161-442)*SCALE
    hit,_,_,_=tree.ray_cast(Vector((-1,cy,cz)),Vector((1,0,0)),3)
    if hit:
        verts=[];n=64
        for depth in [hit.x-.025,hit.x+.008]:
            for j in range(n+1):
                t=j/n;ao=math.radians(54+252*t);ai=math.radians(78+204*t)
                outer=(cy+.117*math.sin(ao),cz+.127*math.cos(ao))
                inner=(cy+.044+.104*math.sin(ai),cz+.024+.107*math.cos(ai))
                if j in [0,n]:inner=outer
                verts.extend([(depth,*outer),(depth,*inner)])
        faces=[];off=(n+1)*2
        for j in range(n):
            a=j*2
            faces.extend([(a,a+2,a+3,a+1),(a+off+1,a+off+3,a+off+2,a+off),(a,a+off,a+off+2,a+2),(a+1,a+3,a+off+3,a+off+1)])
        ob=make_mesh('Moon',verts,faces);ob.data.materials.append(mat)
        bevel=ob.modifiers.new('Soft gold edge','BEVEL');bevel.width=.004;bevel.segments=3


def retained_ornaments(tree):
    source=ASSET.with_name('carol-normal-fleece-v002.blend')
    with bpy.data.libraries.load(str(source),link=False) as (src,dst):
        dst.objects=[n for n in src.objects if n.startswith('STAR_') or n=='MOON']
    objects={}
    for ob in dst.objects:
        bpy.context.scene.collection.objects.link(ob)
        matrix=ob.matrix_world.copy();ob.parent=None;ob.matrix_world=matrix
        if ob.type!='MESH':
            bpy.data.objects.remove(ob,do_unlink=True);continue
        ob.data.transform(ob.matrix_world);ob.matrix_world.identity();objects[ob.name]=ob
    specs={'STAR_crown':(627,273),'STAR_brow':(678,469),'STAR_upper_left':(151,628),
           'STAR_lower_left':(276,962),'STAR_chest':(629,1006),'MOON':(322,445)}
    for name,ob in list(objects.items()):
        if name.endswith('_glint'):continue
        center=sum((v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices)
        if name in specs:
            x,y=specs[name];cy=(630-x)/1012;cz=(1161-y)/1012
            hit,_,_,_=tree.ray_cast(Vector((-1,cy,cz)),Vector((1,0,0)),3)
            if hit is None:continue
            target=Vector((hit.x-.019,cy,cz))
        else:
            sign=1 if name.endswith('_L') else -1
            hit,_,_,_=tree.ray_cast(Vector((.98,sign*2,.33)),Vector((0,-sign,0)),4)
            if hit is None:continue
            target=hit+Vector((0,sign*.02,0))
        delta=target-center
        ob.location+=delta
        if name+'_glint' in objects:objects[name+'_glint'].location+=delta
        if name in specs:
            samples=[]
            for index in range(0,len(ob.data.vertices),max(1,len(ob.data.vertices)//100)):
                vertex=ob.data.vertices[index]
                p=vertex.co+ob.location
                hit,_,_,_=tree.ray_cast(Vector((-1,p.y,p.z)),Vector((1,0,0)),3)
                if hit:samples.append((p.y-target.y,p.z-target.z,hit.x))
            sample_array=np.asarray(samples)
            basis=np.column_stack((sample_array[:,:2],np.ones(len(sample_array))))
            plane=np.linalg.lstsq(basis,sample_array[:,2],rcond=None)[0]
            plane[:2]=np.clip(plane[:2],-.35,.35)
            plane[2]=np.quantile(sample_array[:,2]-sample_array[:,:2]@plane[:2],.08)-.020
            original=np.array([v.co+ob.location for v in ob.data.vertices])
            old_basis=np.column_stack((original[:,1]-target.y,original[:,2]-target.z,np.ones(len(original))))
            old_plane=np.linalg.lstsq(old_basis,original[:,0],rcond=None)[0]
            for piece in [ob]+([objects[name+'_glint']] if name+'_glint' in objects else []):
                for vertex in piece.data.vertices:
                    p=vertex.co+piece.location
                    original_base=old_plane[0]*(p.y-target.y)+old_plane[1]*(p.z-target.z)+old_plane[2]
                    new_base=plane[0]*(p.y-target.y)+plane[1]*(p.z-target.z)+plane[2]
                    vertex.co.x+=new_base-original_base
        owner=bpy.data.objects['FLEECE_HEAD_OWNER' if name in ['STAR_brow','STAR_crown','MOON'] else 'FLEECE_TORSO_OWNER']
        parent_keep(ob,owner)
        if name+'_glint' in objects:parent_keep(objects[name+'_glint'],owner)


def align_face(tree):
    for name in ['EYE_L','EYE_R','EYELID_L','EYELID_R','NOSE','MOUTH_closed','PHILTRUM']:
        ob=bpy.data.objects[name];inv=ob.matrix_world.inverted()
        dy=-.020 if name.startswith('EYE') else -.014
        dz=-.029 if name.startswith('EYE') else -.016
        def moved(co):
            p=ob.matrix_world@Vector(co[:3])
            old,_,_,_=tree.ray_cast(Vector((-1,p.y,p.z)),Vector((1,0,0)),3)
            p.y+=dy;p.z+=dz
            new,_,_,_=tree.ray_cast(Vector((-1,p.y,p.z)),Vector((1,0,0)),3)
            if old and new:p.x+=new.x-old.x
            return inv@p
        if ob.type=='MESH':
            for vertex in ob.data.vertices:vertex.co=moved(vertex.co)
        else:
            for spline in ob.data.splines:
                for point in spline.points:point.co=(*moved(point.co),point.co.w)


def presentation():
    sc=bpy.context.scene
    for ob in list(sc.objects):
        if ob.type in ['CAMERA','LIGHT']:bpy.data.objects.remove(ob,do_unlink=True)
    for yaw in [-45,-30,-15,0,15,30,45,90,-90,135,180]:
        name='front' if yaw==0 else 'side' if yaw==-90 else 'rear' if yaw==180 else f'yaw{yaw:+03d}'
        a=math.radians(yaw)
        target=Vector((.58,0,.50));pos=target+Vector((-4*math.cos(a),4*math.sin(a),0))
        d=bpy.data.cameras.new('VIEW_'+name);d.type='ORTHO';d.ortho_scale=1.32 if yaw==0 else 1.50
        ob=bpy.data.objects.new(d.name,d);sc.collection.objects.link(ob);ob.location=pos
        ob.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler()
    d=bpy.data.cameras.new('VIEW_top');d.type='ORTHO';d.ortho_scale=1.5
    ob=bpy.data.objects.new(d.name,d);sc.collection.objects.link(ob);ob.location=(.58,0,4)
    ob.rotation_euler=(Vector((.58,0,0))-ob.location).to_track_quat('-Z','Y').to_euler()
    for name,position,power,size in [('Key',(-3,-2,4),30,5),('Fill',(-4,3,1.5),30,5),('Rear',(3,1,2),25,5),('Low',(-3,0,-2),22,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
        ob=bpy.data.objects.new(name,d);sc.collection.objects.link(ob);ob.location=position
        ob.rotation_euler=(Vector((.5,0,.4))-ob.location).to_track_quat('-Z','Y').to_euler()
    sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1)
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
    sc.render.engine='CYCLES';sc.cycles.samples=32;sc.cycles.use_denoising=True
    sc.render.resolution_x=sc.render.resolution_y=1254;sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
    sc.view_settings.view_transform='Standard';sc.view_settings.exposure=0
    sc.render.use_compositing=False;sc.render.use_sequencer=False;sc.camera=bpy.data.objects['VIEW_front']


def save():
    bpy.context.preferences.filepaths.save_version=0
    scene=bpy.context.scene
    scene['generator_flags']=' '.join(ARGS)
    scene['generator_hashes']=json.dumps({name:sha(Path(__file__).parent/name) for name in ['build-carol-normal-fleece-v004.py','carol-fleece-v004-authority.py','carol_fleece_spatial.py']},sort_keys=True)
    bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=False,do_recursive=True)
    bpy.ops.file.pack_all()
    staging=ASSET.with_name(ASSET.stem+'.staging.blend')
    bpy.ops.wm.save_as_mainfile(filepath=str(staging),compress=True)
    for attempt in range(5):
        try:
            os.replace(staging,ASSET)
            break
        except PermissionError:
            if attempt==4:raise
            time.sleep(.5*(attempt+1))


def build():
    assert sha(SKIN)==SKIN_SHA
    bpy.ops.wm.open_mainfile(filepath=str(SKIN))
    bpy.context.scene.frame_set(1)
    # Keep the accepted attached facial modules while the fleece converges.
    for name in ['EAR_L','EAR_R']:
        ob=bpy.data.objects[name]
        for ve in ob.data.vertices:ve.co.z=.449+(ve.co.z-.505)*.80
    tree=skin_tree()
    align_face(tree)
    head_owner=empty('FLEECE_HEAD_OWNER',(.30,0,.50))
    body_owner=empty('FLEECE_TORSO_OWNER',(.66,0,.38))
    if '--spatial' in ARGS:
        sys.path.insert(0,str(Path(__file__).parent))
        from carol_fleece_spatial import build_surface
        fleece=build_surface(globals(),tree,head_owner,body_owner)
    else:
        body=surface('BodyFleece',pixels(WORK/'body-mask.png')[:,:,0]>.5,(630,621),body_owner,body_front,tree)
        head=surface('HeadFleece',pixels(WORK/'head-mask.png')[:,:,0]>.5,(646,767),head_owner,head_front,tree,pixels(WORK/'face-mask.png')[:,:,0]>.5)
        fleece=[body,head]
    # Existing continuous three-terminal hooves were already built for Normal.
    previous=ASSET.with_name('carol-normal-fleece-v002.blend')
    with bpy.data.libraries.load(str(previous),link=False) as (src,dst):
        dst.objects=[n for n in src.objects if n.startswith('HOOF_')]
    for ob in dst.objects:
        old=bpy.data.objects.get(ob.name.removesuffix('.001'))
        if old and old!=ob:bpy.data.objects.remove(old,do_unlink=True)
        bpy.context.scene.collection.objects.link(ob)
        ob.data.transform(ob.matrix_world);ob.parent=None;ob.matrix_world.identity()
        center=np.mean([v.co[:] for v in ob.data.vertices],axis=0)
        for ve in ob.data.vertices:
            ve.co.y=center[1]+(ve.co.y-center[1])*1.10;ve.co.z*=.76
    allverts=[];allfaces=[]
    if '--spatial' in ARGS:
        from carol_fleece_spatial import regional_skin_paint
        regional_skin_paint(globals())
    for ob in fleece:
        offset=len(allverts)
        allverts.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        allfaces.extend([offset+k for k in p.vertices] for p in ob.data.polygons)
    retained_ornaments(BVHTree.FromPolygons(allverts,allfaces))
    for name,loc in [('fleece_front',(.12,0,.18)),('pocket_front_L',(.14,.20,.24)),('pocket_front_R',(.14,-.20,.24)),('gift_reveal',(.14,0,.23))]:
        parent_keep(empty(name,loc),body_owner)
    presentation()
    if '--solid-locks' in ARGS:
        for name,energy in [('Key',95),('Fill',40),('Rear',65),('Low',16)]:
            bpy.data.objects[name].data.energy=energy
        bpy.context.scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.50
    bpy.context.scene['phase1_state']='NORMAL_FLEECE_V004_IN_PROGRESS'
    bpy.context.scene['accepted_skin_sha256']=SKIN_SHA
    bpy.context.scene['method_donor_commit']='15bfa8e4c3a8ba24c246fe806bd125b307d8f076'
    save()


def render():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));sc=bpy.context.scene
    folder=OUT/arg('--folder','renders');folder.mkdir(parents=True,exist_ok=True)
    if '--quick' in ARGS:sc.render.resolution_percentage=55;sc.cycles.samples=12
    if '--clay' in ARGS:
        mat=shader('Diagnostic diffuse clay',lit=1,color=(.78,.78,.78))
        for name in ['BodyFleece','HeadFleece','TailFleece']:
            ob=bpy.data.objects.get(name)
            if ob:ob.data.materials.clear();ob.data.materials.append(mat)
        sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
        bpy.data.objects['Key'].data.energy=180
    manifest={'asset_sha256':sha(ASSET),'generator_hashes':json.loads(sc.get('generator_hashes','{}')),'diagnostic_clay':'--clay' in ARGS,'views':{}}
    for view in arg('--views','front,yaw+30,side').split(','):
        sc.camera=bpy.data.objects['VIEW_'+view]
        path=folder/(view+'.png');sc.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        manifest['views'][view]={'sha256':sha(path),'camera_matrix':[list(row) for row in sc.camera.matrix_world],'ortho_scale':sc.camera.data.ortho_scale,'size':[int(sc.render.resolution_x*sc.render.resolution_percentage/100)]*2,'samples':sc.cycles.samples}
        (folder/'render-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')


BODY_LOCKS=[x for x in INVENTORY['front'] if x['region']!='head']
HEAD_LOCKS=[x for x in INVENTORY['front'] if x['region'] in ['head','blue_flank']]
if ARGS[0]=='build':
    build()
    if '--render' in ARGS:render()
elif ARGS[0]=='render':render()
else:raise ValueError(ARGS[0])
