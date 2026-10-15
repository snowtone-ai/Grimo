"""Pino C local pre-texture engineering. Source assets are read only."""
import bpy, sys, json, math, hashlib, importlib.util
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
AS=ROOT/'assets/grimo/production/pino/candidate-c'
DEST=AS/'texture-ready-v003'
OUT=ROOT/'docs/production/pino/evidence/texture-ready-v003'
TMP=ROOT/'artifacts/pino-texture-v003'
for p in [DEST,OUT,TMP]:p.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('face2',ROOT/'scripts/blender/pino-face-foundation-v002.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
_source_view=f.view
def precise_view(sc,*args,**kwargs):
    _source_view(sc,*args,**kwargs)
    sc.camera.data.clip_start=.01;sc.camera.data.clip_end=10
f.view=precise_view
def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def coords(o):return np.array([v.co[:] for v in o.data.vertices])
def load():
    bpy.ops.wm.open_mainfile(filepath=str(AS/'face-foundation-v002/pino-face-foundation-v002.blend'))
    return bpy.data.objects['PINO_C_BASE_RIG_V001'],bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'],bpy.context.scene
def inspect():
    o,r,s=load();v=coords(o);labels=np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
    t=np.array([p.vertices[:] for p in o.data.polygons]);n=np.array([p.normal[:] for p in o.data.polygons])
    np.savez_compressed(TMP/'source.npz',v=v,t=t,n=n,labels=labels,corner=np.array([n.vector[:] for n in o.data.corner_normals]))
    dump('initial-inspection.json',{'modifiers':[{p:getattr(m,p,None) for p in ['name','type','use_deform_preserve_volume','use_vertex_groups']} for m in o.modifiers], 'matrix':list(map(list,o.matrix_world)), 'custom_normals':o.data.has_custom_normals, 'materials':[m.name for m in o.data.materials]})
def mouth(v,labels,tri):
    x,y,z=v.T
    w=(1-f.smooth(.060,.085,abs(x)))*(1-f.smooth(-.350,-.325,y))*(labels==0)
    lower=np.minimum(.615,.552+16.5*x*x)
    body=BVHTree.FromPolygons([Vector(p) for p in v],[list(t) for t in tri if labels[t[0]]==0],all_triangles=True)
    close=v.copy()
    # Pose-only unfolding of the source recess; distinct sheet depths survive.
    fitroi=(labels==0)&(abs(x)<.11)&(y<-.33)&(z>.485)&(z<.637)
    for i in np.where(fitroi)[0]:
        hit=body.ray_cast(Vector((x[i],-.8,z[i])),Vector((0,1,0)))[0]
        if not hit:continue
        envelope=-.413+3.8*(z[i]-.608)**2+1.5*x[i]*x[i]
        mask=(1-f.smooth(.045,.085,abs(x[i])))*f.smooth(.49,.54,z[i])*(1-f.smooth(.610,.625,z[i]))
        close[i,1]+=min(0,envelope-hit.y)*mask
    large=v.copy();large[:,2]-=.012*w*f.smooth(.49,lower,z)*(1-f.smooth(.575,.617,z))
    return close,large
def lids(o,rig,v,labels):
    body=BVHTree.FromPolygons([Vector(p) for p in v],[list(p.vertices) for p in o.data.polygons if labels[p.vertices[0]]==0],all_triangles=True)
    result=[]
    for side,comp in [('L',9),('R',8)]:
        ep=v[labels==comp];c=ep.mean(0);c[2]=(ep[:,2].min()+ep[:,2].max())/2
        outward=Vector((.46 if side=='L' else -.46,-.888,0));outward.normalize()
        tangent=Vector((-outward.y,outward.x,0))
        retract=o.shape_key_add(name='PinoEyeRetract_'+side,from_mix=False)
        for dst,p in zip(retract.data,v):dst.co=p
        for idx in np.where(labels==comp)[0]:retract.data[int(idx)].co-=outward*.060
        eye=BVHTree.FromPolygons([Vector(p) for p in v],[list(p.vertices) for p in o.data.polygons if labels[p.vertices[0]]==comp],all_triangles=True)
        eu=np.array([(Vector(p)-Vector(c)).dot(tangent) for p in ep]);ax=max(abs(eu.min()),abs(eu.max()));az=np.ptp(ep[:,2])/2
        ez=ep[:,2]-c[2];ed=np.array([(Vector(p)-Vector(c)).dot(outward) for p in ep])
        design=np.stack([eu*0+1,eu,ez,eu*eu,eu*ez,ez*ez],axis=1)
        fit=np.linalg.lstsq(design,ed,rcond=None)[0];fit[0]+=float(np.max(ed-design@fit))+.001
        bp=v[labels==0];rel=bp-c;bu=rel@np.array(tangent);bz=rel[:,2];bdp=rel@np.array(outward)
        br=np.sqrt((bu/ax)**2+(bz/az)**2)
        sel=(br>1.02)&(br<1.65)&(bdp>-.060)&(bdp<.050)
        designbody=np.stack([bu*0+1,bu,bz,bu*bu,bu*bz,bz*bz],axis=1)
        samples=[];depths=[]
        for radius in [1.15,1.35,1.55]:
            for theta in np.linspace(0,2*math.pi,64,endpoint=False):
                uu=ax*radius*math.cos(theta);zz=az*radius*math.sin(theta)
                q=Vector(c)+tangent*uu;q.z+=zz
                hit=body.ray_cast(q+outward*.6,-outward)[0]
                if hit:
                    samples.append([1,uu,zz,uu*uu,uu*zz,zz*zz]);depths.append((hit-q).dot(outward))
        bodyfit=np.linalg.lstsq(samples,depths,rcond=None)[0];bodyfit[0]+=.0010
        rad=float(np.sqrt((eu/ax)**2+(ez/az)**2).max());ax*=rad*1.20;az*=rad*1.18
        vv=[[],[],[],[],[]];faces=[];NX=64;NY=24
        for upper in [True,False]:
            off=len(vv[0])
            for j in range(NY+1):
                s=j/NY
                for i in range(NX+1):
                    u=-.999+1.998*i/NX;root=math.sqrt(max(.0001,1-u*u));edge=c[2]+(1 if upper else -1)*az*root
                    seam=c[2]+.008*(1-u*u)
                    for k,b in enumerate([0,.65,.83,.95,1]):
                        end=(edge+(-.003 if upper else .003))*(1-b)+seam*b
                        z=edge*(1-s)+end*s
                        q=Vector(c)+tangent*(u*ax);q.z=z
                        origin=q+outward*.6
                        eh=eye.ray_cast(origin,-outward)[0];bh=body.ray_cast(origin,-outward)[0]
                        uu=u*ax;zz=z-c[2]
                        e=float(np.array([1,uu,zz,uu*uu,uu*zz,zz*zz])@fit)
                        actualbody=(bh-q).dot(outward) if bh else e-.01
                        bd=float(np.array([1,uu,zz,uu*uu,uu*zz,zz*zz])@bodyfit)
                        radial=math.sqrt((uu/(ax/1.20))**2+(zz/(az/1.18))**2)
                        boundary=f.smooth(.94,1.18,radial)
                        depth=(e+.002)*(1-boundary)+(actualbody-.002)*boundary
                        if k==4:
                            # One fair closed surface extending under the surrounding
                            # head, with a shallow seam. No ray-hit ridges in the cap.
                            depth=bd+.0012-.0012*np.exp(-((z-seam)/.0025)**2)
                            depth-=.010*f.smooth(1.02,1.18,radial)
                        if k==0:depth=actualbody-.008
                        vv[k].append(tuple(q+outward*depth))
            for j in range(NY):
                for i in range(NX):
                    a=off+j*(NX+1)+i;quad=(a,a+1,a+NX+2,a+NX+1)
                    faces.append(quad[::-1] if upper else quad)
        me=bpy.data.meshes.new('Texture-ready rolling lid '+side);me.from_pydata(vv[0],[],faces);me.update()
        ob=bpy.data.objects.new('PinoSoftLids_'+side,me);bpy.context.scene.collection.objects.link(ob);me.materials.append(o.data.materials[0])
        for p in me.polygons:p.use_smooth=True
        ob.shape_key_add(name='Basis')
        for name,points in zip(['LidHalf','LidThreeQuarter','LidAlmostClosed','LidClosed'],vv[1:]):
            k=ob.shape_key_add(name=name,from_mix=False)
            for d,p in zip(k.data,points):d.co=p
        k=ob.shape_key_add(name='LidRetreat',from_mix=False)
        for d,p in zip(k.data,vv[0]):d.co=Vector(p)-outward*.060
        g=ob.vertex_groups.new(name='mixamorig:Head');g.add(list(range(len(me.vertices))),1,'REPLACE')
        ob.parent=rig;m=ob.modifiers.new('Head skin','ARMATURE');m.object=rig
        result.append(ob)
    return result
def fair_closed_skin(o,v,labels):
    body=BVHTree.FromPolygons([Vector(p) for p in v],[list(p.vertices) for p in o.data.polygons if labels[p.vertices[0]]==0],all_triangles=True)
    for side,comp in [('L',9),('R',8)]:
        ep=v[labels==comp];c=ep.mean(0);c[2]=(ep[:,2].min()+ep[:,2].max())/2
        out=np.array((.46 if side=='L' else -.46,-.888,0));out/=np.linalg.norm(out);tan=np.array((-out[1],out[0],0))
        eu=(ep-c)@tan;ax=max(abs(eu));az=np.ptp(ep[:,2])/2
        samples=[];depth=[]
        for un in np.linspace(-1.7,1.7,27):
            for zn in np.linspace(-1.7,1.7,27):
                if un*un+zn*zn>1.7**2:continue
                q=c+tan*(un*ax)+np.array((0,0,zn*az));hit=body.ray_cast(Vector(q+out*.6),Vector(-out))[0]
                if hit:samples.append((un,zn));depth.append((np.array(hit)-q)@out)
        samples=np.array(samples);depth=np.array(depth);rad=np.linalg.norm(samples,axis=1)
        powers=[(a,b) for a in range(3) for b in range(3-a)]
        def design(uv):return np.stack([uv[:,0]**a*uv[:,1]**b for a,b in powers],axis=1)
        basis=design(samples);ring=rad>1.18
        quad=[powers.index(p) for p in [(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]]
        coeff=np.linalg.lstsq(basis[ring][:,quad],depth[ring],rcond=None)[0]
        target=basis[:,quad]@coeff+.001+.007*np.exp(-(rad/.95)**4)
        window=1-f.smooth(.85,1.65,rad)
        # Smooth spatial field shared by every internal layer. Thin-plate RBF
        # follows the actual socket depression without pulling sheets apart.
        def kernel(a,b):
            dd=np.linalg.norm(a[:,None,:]-b[None,:,:],axis=2);return dd*dd*np.log(np.maximum(dd,1e-10))
        poly=np.c_[np.ones(len(samples)),samples]
        mat=np.block([[kernel(samples,samples)+np.eye(len(samples))*.00001,poly],[poly.T,np.zeros((3,3))]])
        fit=np.linalg.solve(mat,np.r_[(target-depth)*window,np.zeros(3)])
        rel=v-c;uv=np.stack([rel@tan/ax,rel[:,2]/az],axis=1);rr=np.linalg.norm(uv,axis=1)
        shift=np.zeros(len(v));inside=rr<1.65
        shift[inside]=kernel(uv[inside],samples)@fit[:-3]+np.c_[np.ones(inside.sum()),uv[inside]]@fit[-3:]
        region=(labels==0)&(rr<1.65)&(v[:,1]<-.23)
        pts=v.copy();seam=.008*(1-(uv[:,0]/1.2)**2)
        shift-=.0015*np.exp(-((rel[:,2]-seam)/.003)**2)*(1-f.smooth(.65,1.0,abs(uv[:,0])))
        pts[region]+=shift[region,None]*out
        key=o.shape_key_add(name='PinoSkinClose_'+side,from_mix=False)
        for dst,p in zip(key.data,pts):dst.co=p
def mouth_lift(pts):
    x,y,z=pts.T
    mask=(1-f.smooth(.045,.085,abs(x)))*(1-f.smooth(-.34,-.31,y))*f.smooth(.525,.565,z)*(1-f.smooth(.607,.62,z))
    delta=np.zeros_like(pts);delta[:,2]=(.614-z)*mask
    return delta

def dynamic_normals(o):
    me=o.data;keys=me.shape_keys.key_blocks;faces=[p.vertices[:] for p in me.polygons]
    def normals(pts):
        if o.name=='PinoOralLiner':
            # Clipped source polygons deliberately keep their own vertices to
            # preserve Basis corner normals. Smooth coincident positions only
            # for posed normals; changing this topology would alter provenance.
            a=np.asarray(pts);ff=np.asarray(faces,dtype=int)
            _,inv=np.unique(np.round(a,7),axis=0,return_inverse=True)
            face=np.cross(a[ff[:,1]]-a[ff[:,0]],a[ff[:,2]]-a[ff[:,0]])
            sums=np.zeros((int(inv.max())+1,3));np.add.at(sums,inv[ff.ravel()],np.repeat(face,3,axis=0))
            length=np.linalg.norm(sums,axis=1);sums/=np.maximum(length,1e-20)[:,None]
            return sums[inv[np.array([l.vertex_index for l in me.loops])]]
        tmp=bpy.data.meshes.new('Normal evaluation scratch');tmp.from_pydata(pts,[],faces);tmp.update()
        for p in tmp.polygons:p.use_smooth=True
        nn=np.array([p.vector[:] for p in tmp.corner_normals]);bpy.data.meshes.remove(tmp);return nn
    v=coords(o);base=np.array([n.vector[:] for n in me.corner_normals])
    bank={}
    for key in list(keys)[1:]:
        if key.name=='LidRetreat':
            bank[key.name]=np.zeros_like(base);continue
        pts=np.array([p.co[:] for p in key.data]);changed=np.linalg.norm(pts-v,axis=1)>1e-7
        active=np.array([any(changed[i] for i in p.vertices) for p in me.polygons])
        mask=np.repeat(active,[p.loop_total for p in me.polygons])
        bank[key.name]=(normals(pts.tolist())-base)*mask[:,None]
    # A transient lift aligns the actual aperture and its lining. Evaluate the
    # combined small-opening pose rather than adding two unrelated normal fields.
    lift='PinoMouthLift' if 'PinoMouthLift' in keys else 'OralLift' if 'OralLift' in keys else None
    if lift:
        close='PinoMouthClosed' if lift.startswith('Pino') else 'OralClosed'
        dc=np.array([p.co[:] for p in keys[close].data])-v;dl=np.array([p.co[:] for p in keys[lift].data])-v
        changed=(np.linalg.norm(dc,axis=1)+np.linalg.norm(dl,axis=1))>1e-7
        mask=np.repeat([any(changed[i] for i in p.vertices) for p in me.polygons],[p.loop_total for p in me.polygons])
        bank[lift]=((normals((v+.75*dc+.45*dl).tolist())-base)*mask[:,None]-.75*bank[close])/.45
    normal_controller(o,base,bank)

def normal_controller(o,base,bank):
    me=o.data;keys=me.shape_keys.key_blocks
    attr=me.attributes.new('PinoCanonicalCornerNormal','FLOAT_VECTOR','CORNER');attr.data.foreach_set('vector',base.ravel())
    group=bpy.data.node_groups.new('Pino canonical + morph normal deltas','GeometryNodeTree')
    group.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    nodes=group.nodes;links=group.links;inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');setn=nodes.new('GeometryNodeSetMeshNormal');setn.mode='FREE';setn.domain='CORNER'
    links.new(inp.outputs['Geometry'],setn.inputs['Mesh']);links.new(setn.outputs['Mesh'],out.inputs['Geometry'])
    get=nodes.new('GeometryNodeInputNamedAttribute');get.data_type='FLOAT_VECTOR';get.inputs['Name'].default_value=attr.name;last=get.outputs['Attribute']
    for key in list(keys)[1:]:
        dn=bank[key.name]
        a=me.attributes.new('PinoDN_'+key.name,'FLOAT_VECTOR','CORNER');a.data.foreach_set('vector',dn.ravel())
        get=nodes.new('GeometryNodeInputNamedAttribute');get.data_type='FLOAT_VECTOR';get.inputs['Name'].default_value=a.name
        val=nodes.new('ShaderNodeValue');val.name='Value_'+key.name;driver=val.outputs[0].driver_add('default_value').driver
        variable=driver.variables.new();variable.name='weight';variable.targets[0].id_type='KEY';variable.targets[0].id=me.shape_keys;variable.targets[0].data_path=key.path_from_id('value');driver.expression='weight'
        scale=nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';links.new(get.outputs['Attribute'],scale.inputs[0]);links.new(val.outputs[0],scale.inputs['Scale'])
        add=nodes.new('ShaderNodeVectorMath');add.operation='ADD';links.new(last,add.inputs[0]);links.new(scale.outputs[0],add.inputs[1]);last=add.outputs[0]
    norm=nodes.new('ShaderNodeVectorMath');norm.operation='NORMALIZE';links.new(last,norm.inputs[0]);links.new(norm.outputs[0],setn.inputs['Custom Normal'])
    mod=o.modifiers.new('Pino portable morph normals','NODES');mod.node_group=group
    while list(o.modifiers).index(mod)>0:bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_move_up(modifier=mod.name)


def source_oral_liner(o,r,v,labels):
    basis=[];closed=[];large=[];normals=[];faces=[]
    target=o.data.shape_keys.key_blocks['PinoMouthLarge']
    # Clip the actual source triangles, preserving their planes and corner
    # normals. A re-sampled grid caused z-fighting and changed Basis shading.
    for p in o.data.polygons:
        pp=v[list(p.vertices)];c=pp.mean(0)
        if labels[p.vertices[0]]!=0 or abs(c[0])>.075 or not(.54<c[2]<.63 and -.43<c[1]<-.34):continue
        poly=[(pp[i].copy(),np.array(target.data[vi].co),np.array(o.data.corner_normals[li].vector)) for i,(vi,li) in enumerate(zip(p.vertices,p.loop_indices))]
        for theta in np.linspace(0,2*math.pi,64,endpoint=False):
            nx,nz=math.cos(theta),math.sin(theta)
            def distance(a):return 1-(a[0][0]/.0455*nx+(a[0][2]-.5865)/.0285*nz)
            out=[]
            for a,b in zip(poly,poly[1:]+poly[:1]):
                da,db=distance(a),distance(b)
                if da>=0:out.append(a)
                if (da>=0)!=(db>=0):
                    t=da/(da-db);out.append(tuple(x+(y-x)*t for x,y in zip(a,b)))
            poly=out
            if not poly:break
        if len(poly)<3:continue
        start=len(basis)
        for pos,lg,n in poly:
            q=pos.copy();q[1]-=.000005;basis.append(q);closed.append(np.array((pos[0],-.413,pos[2])));lg[1]-=.000005;large.append(lg);normals.append(n/np.linalg.norm(n) if np.linalg.norm(n)>0 else n)
        for i in range(1,len(poly)-1):faces.append((start,start+i,start+i+1))
    me=bpy.data.meshes.new('Source-aligned retracting oral liner');me.from_pydata(basis,[],faces);me.update()
    ob=bpy.data.objects.new('PinoOralLiner',me);bpy.context.scene.collection.objects.link(ob);me.materials.append(o.data.materials[0])
    for p in me.polygons:p.use_smooth=True
    me.normals_split_custom_set_from_vertices(normals)
    ob.shape_key_add(name='Basis')
    for name,pts in [('OralClosed',closed),('OralLarge',large)]:
        key=ob.shape_key_add(name=name,from_mix=False)
        for d,co in zip(key.data,pts):d.co=co
    key=ob.shape_key_add(name='OralLift',from_mix=False)
    for d,co in zip(key.data,np.array(basis)+mouth_lift(np.array(basis))):d.co=co
    key=ob.shape_key_add(name='OralOcclude',from_mix=False)
    for d,co in zip(key.data,basis):d.co=co+np.array((0,.035,0))
    g=ob.vertex_groups.new(name='mixamorig:Head');g.add(list(range(len(me.vertices))),1,'REPLACE');ob.parent=r;m=ob.modifiers.new('Head skin','ARMATURE');m.object=r
    return ob

def build():
    o,r,s=load();labels=np.load(TMP/'source.npz')['labels']
    f.display(s,400)
    for view in ['front','side','3q']:
        f.view(s,view);f.render(s,TMP/('authority-'+view+'.png'))
    for side in ['L','R']:bpy.data.objects.remove(bpy.data.objects['PinoSoftLids_'+side],do_unlink=True)
    v=coords(o);tri=np.array([p.vertices[:] for p in o.data.polygons])
    for name,pts in zip(['PinoMouthClosed','PinoMouthLarge'],mouth(v,labels,tri)):
        for d,p in zip(o.data.shape_keys.key_blocks[name].data,pts):d.co=p
    lift=o.shape_key_add(name='PinoMouthLift',from_mix=False)
    for d,p in zip(lift.data,v+mouth_lift(v)*(labels==0)[:,None]):d.co=p
    ll=lids(o,r,v,labels);fair_closed_skin(o,v,labels)
    for ob,side,comp in zip(ll,['L','R'],[9,8]):
        pts=np.array([p.co[:] for p in o.data.shape_keys.key_blocks['PinoSkinClose_'+side].data])
        skin=BVHTree.FromPolygons([Vector(p) for p in pts],[list(p.vertices) for p in o.data.polygons if labels[p.vertices[0]]==0],all_triangles=True)
        ep=v[labels==comp];c=ep.mean(0);c[2]=(ep[:,2].min()+ep[:,2].max())/2
        outward=Vector((.46 if side=='L' else -.46,-.888,0));outward.normalize();tan=Vector((-outward.y,outward.x,0))
        ax=max(abs((ep-c)@np.array(tan)));az=np.ptp(ep[:,2])/2
        eu=(ep-c)@np.array(tan);rad=float(np.sqrt((eu/ax)**2+((ep[:,2]-c[2])/az)**2).max());ax*=rad*1.20
        for vi,dst in enumerate(ob.data.shape_keys.key_blocks['LidClosed'].data):
            half=vi//1625;idx=vi%1625;u=-.999+1.998*(idx%65)/64;row_t=(idx//65)/24
            seam=c[2]+.008*(1-(u/1.2)**2);d=(1 if half==0 else -1)*.003*(1-row_t)
            q=Vector(c)+tan*(u*ax);q.z=seam+d
            hit=skin.ray_cast(q+outward*.6,-outward)[0]
            if hit:
                # Collapse the whole wrapping surface to one narrow crease,
                # including its outer edge. Keeping the outer edge fixed made
                # a detached round patch during the final settlement.
                depth=-.0015+.0022*(1-(d/.003)**2)-.004*f.smooth(.75,1,abs(u))
                dst.co=hit+outward*depth
    liner=source_oral_liner(o,r,v,labels)
    dynamic_normals(o)
    for ob in [*ll,liner]:dynamic_normals(ob)
    state(o,ll);f.display(s,400)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(TMP/'candidate.blend'),compress=True)
    for view in ['front','side','3q']:
        f.view(s,view);f.render(s,TMP/('candidate-neutral-'+view+'.png'))
    diag=bpy.data.materials.new('DIAGNOSTIC eye ownership');diag.diffuse_color=(.025,.10,.20,1);o.data.materials.append(diag)
    for p in o.data.polygons:
        if labels[p.vertices[0]] in [8,9]:p.material_index=len(o.data.materials)-1
    for label,args in [('basis',(0,0,0,0)),('closed',(1,0,0,0)),('half',(0,0,.5,.5)),('combined',(0,1,1,1))]:
        state(o,ll,*args)
        for view in ['front','side','3q']:
            f.view(s,view);f.render(s,TMP/(label+'-'+view+'.png'))
    for ob in ll:ob.hide_render=True
    state(o,ll,0,0,1,1)
    for view in ['front','side','3q']:
        f.view(s,view);f.render(s,TMP/('retract-only-'+view+'.png'))
    for ob in ll:ob.hide_render=False
    state(o,ll,1)
    o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops))
    for view in ['front','side','3q']:
        f.view(s,view);f.render(s,TMP/('closed-recalc-'+view+'.png'))
    state(o,ll,0,1,1,1)
    for view in ['front','3q']:
        f.view(s,view);f.render(s,TMP/('combined-recalc-'+view+'.png'))
def state(o,ll,closed=0,large=0,left=0,right=0):
    f.state(o,ll,closed,large,left,right)
    lift=.6*closed*float(1-f.smooth(.75,1,closed))
    o.data.shape_keys.key_blocks['PinoMouthLift'].value=lift
    if 'PinoOralLiner' in bpy.data.objects:
        bpy.data.objects['PinoOralLiner'].data.shape_keys.key_blocks['OralClosed'].value=closed
        bpy.data.objects['PinoOralLiner'].data.shape_keys.key_blocks['OralLarge'].value=large
        bpy.data.objects['PinoOralLiner'].data.shape_keys.key_blocks['OralLift'].value=lift
        bpy.data.objects['PinoOralLiner'].data.shape_keys.key_blocks['OralOcclude'].value=float(f.smooth(.85,1,closed))
    for side,b in zip(['L','R'],[left,right]):
        settle=float(f.smooth(.9,.95,b))
        o.data.shape_keys.key_blocks['PinoEyeRetract_'+side].value=settle
        if 'PinoSkinClose_'+side in o.data.shape_keys.key_blocks:o.data.shape_keys.key_blocks['PinoSkinClose_'+side].value=settle
        keys=bpy.data.objects['PinoSoftLids_'+side].data.shape_keys.key_blocks
        knots=[0,.5,.75,.9];names=[None,'LidHalf','LidThreeQuarter','LidAlmostClosed']
        for name in [*names[1:],'LidClosed','LidRetreat']:keys[name].value=0
        if b<=.9:
            for i in range(1,len(knots)):
                if b<=knots[i]:
                    t=max(0,(b-knots[i-1])/(knots[i]-knots[i-1]))
                    if names[i-1]:keys[names[i-1]].value=1-t
                    keys[names[i]].value=t;break
        elif b<.95:
            keys['LidAlmostClosed'].value=1;keys['LidRetreat'].value=settle
        else:
            finish=float(f.smooth(.95,1,b));keys['LidAlmostClosed'].value=1-finish;keys['LidClosed'].value=finish;keys['LidRetreat'].value=1-finish
        if 'PinoLidHalf_'+side in o.data.shape_keys.key_blocks:
            o.data.shape_keys.key_blocks['PinoLidHalf_'+side].value=min(2*b,2-2*b)
            o.data.shape_keys.key_blocks['PinoLidClosed_'+side].value=max(0,2*b-1)
def static_diagnostic():
    bpy.ops.wm.open_mainfile(filepath=str(TMP/'candidate.blend'));o=bpy.data.objects['PINO_C_BASE_RIG_V001'];sc=bpy.context.scene;ll=[bpy.data.objects['PinoSoftLids_'+side] for side in ['L','R']]
    v=coords(o);tri=[p.vertices[:] for p in o.data.polygons];state(o,ll,1,0,1,1)
    before=[(k.name,k.value) for k in o.data.shape_keys.key_blocks];ev=f.evaluated(o)
    me=bpy.data.meshes.new('Independent posed normals');me.from_pydata(ev.tolist(),[],tri);me.update()
    for m in o.data.materials:me.materials.append(m)
    for p in me.polygons:p.use_smooth=True
    ob=bpy.data.objects.new('Independent posed mesh',me);sc.collection.objects.link(ob);o.hide_render=True
    for x in ll:x.hide_render=True
    f.display(sc,600)
    for view in ['front','side','3q']:
        f.view(sc,view);f.render(sc,TMP/('static-evaluated-'+view+'.png'))
    dump('evaluated-diagnostic.json',{'before_render':before,'after_render':[(k.name,k.value) for k in o.data.shape_keys.key_blocks],'deformation_max':float(np.linalg.norm(ev-v,axis=1).max()),'custom_normals':me.has_custom_normals})
def body():
    bpy.ops.wm.open_mainfile(filepath=str(AS/'rig-v001/pino-c-base-rig-v001-proof.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];r=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];sc=bpy.context.scene
    f.display(sc,360);records=[];banks={};posebanks={};mod=next(m for m in o.modifiers if m.type=='ARMATURE')
    sourceweights=[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices]
    names=[b.name for b in r.pose.bones]
    for label,frame in [('tail-left',13),('tail-right',37),('forepaw',121),('both-paws',169),('shallow-rest',211),('deep-rest',211)]:
        bpy.ops.wm.open_mainfile(filepath=str(AS/'rig-v001/pino-c-base-rig-v001-proof.blend'))
        o=bpy.data.objects['PINO_C_BASE_RIG_V001'];r=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];sc=bpy.context.scene;mod=next(m for m in o.modifiers if m.type=='ARMATURE');f.display(sc,360)
        sc.frame_set(frame)
        for ob in sc.objects:
            if ob.animation_data:ob.animation_data_clear()
            if ob.type=='MESH' and ob.data.shape_keys and ob.data.shape_keys.animation_data:ob.data.shape_keys.animation_data_clear()
        if label=='deep-rest':
            p=r.pose.bones['mixamorig:Hips'];p.location+=p.bone.matrix_local.to_3x3().inverted()@Vector((0,.075,-.115))
        bpy.context.view_layer.update();posebanks[label]=np.array([p.matrix[:] for p in r.pose.bones])
        for mode in ['DQ','LBS4']:
            for vi,ww in enumerate(sourceweights):
                for g,w in ww:o.vertex_groups[g].add([vi],w,'REPLACE')
            if mode=='LBS4':
                for vi,ww in enumerate(sourceweights):
                    ordered=sorted(ww,key=lambda p:p[1],reverse=True);total=sum(w for g,w in ordered[:4])
                    for g,w in ordered:
                        if (g,w) in ordered[:4]:o.vertex_groups[g].add([vi],w/total,'REPLACE')
                        else:o.vertex_groups[g].remove([vi])
            mod.use_deform_preserve_volume=mode=='DQ';bpy.context.view_layer.update();vv=f.evaluated(o);banks[label+'-'+mode]=vv
            records.append({'pose':label,'mode':mode,'zmin':float(vv[:,2].min()),'floor_penetration_vertices':int((vv[:,2]<-.001).sum()),'source_DQ_delta':0 if mode=='DQ' else float(np.linalg.norm(vv-banks[label+'-DQ'],axis=1).max())})
            for view in (['3q'] if mode=='DQ' else ['front','side','3q']):
                dr=Vector({'front':(0,-1,.04),'side':(1,0,.025),'3q':(1,-1,.10)}[view]).normalized();target=Vector((0,-.03,.48));sc.camera.location=target+dr*3;sc.camera.rotation_euler=(-dr).to_track_quat('-Z','Y').to_euler();sc.camera.data.ortho_scale=1.35
                f.render(sc,TMP/(label+'-'+mode+'-'+view+'.png'))
    np.savez_compressed(TMP/'body-poses.npz',**banks,**{k+'-matrices':v for k,v in posebanks.items()},bone_names=np.array(names))
    dump('body-diagnostic.json',records)
if __name__=='__main__':
    if '--build' in sys.argv:build()
    elif '--body' in sys.argv:body()
    elif '--static' in sys.argv:static_diagnostic()
    else:inspect()
