"""Original-FBX-only Shushu reconstruction. Blender 5.2; no remote services.

Donor modules retain their proportions with local repairs and face topology edits.
The disposable shape controls demonstrate readiness, not a final game rig.
"""
import bpy,bmesh,math,json,sys,hashlib
from pathlib import Path
from collections import defaultdict,Counter
import numpy as np
from mathutils import Vector,Matrix,Quaternion
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v003'
ASSET=ROOT/'assets/grimo/production/shushu/blender/shushu-geometry-v003.blend'
PROOF=ASSET.with_name('shushu-geometry-v003-proof.blend')
STATIC=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/shushu-geometry-v003-tripo'
NAMES=['Head','Torso','Leg.R','Leg.L','Ear.L','Ear.R','Paw.L','Paw.R']
parts={};character=[];patches={};raw=None;cam=None;clay=None;controller=None;eye_fits={};face_bm=None;head_surface=None
render_records={}
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def mesh(name,verts,faces):
    m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update()
    o=bpy.data.objects.new(name,m);bpy.context.scene.collection.objects.link(o)
    if clay:m.materials.append(clay)
    for p in m.polygons:p.use_smooth=True
    return o
def components(m):
    parent=list(range(len(m.polygons)));edges=defaultdict(list)
    def root(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    for p in m.polygons:
        for e in p.edge_keys:edges[tuple(sorted(e))].append(p.index)
    for inc in edges.values():
        for i in inc[1:]:parent[root(i)]=root(inc[0])
    groups=defaultdict(list)
    for i in range(len(parent)):groups[root(i)].append(i)
    return sorted(groups.values(),key=len,reverse=True)
def evaluated(o):
    bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles()
    v=np.array([ev.matrix_world@v.co for v in m.vertices]);t=np.array([p.vertices[:] for p in m.loop_triangles]);ev.to_mesh_clear();return v,t
def shape(o,name,fn):
    if not o.data.shape_keys:o.shape_key_add(name='Basis')
    k=o.shape_key_add(name=name,from_mix=False)
    # Blender can copy the active key even at value zero. Always derive from rest.
    for v,b in zip(k.data,o.data.shape_keys.key_blocks['Basis'].data):v.co=fn(b.co.copy())
    return k
def tree(o):
    v,t=evaluated(o);return BVHTree.FromPolygons(v.tolist(),t.tolist(),all_triangles=True)
def activate(o):
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def import_source():
    global raw,clay
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.preferences.filepaths.save_version=0
    p=ROOT/'assets/grimo/production/shushu/tripo/candidate-b-8481/cute panda 3d model 8481.fbx'
    expected=json.loads((ROOT/'docs/production/shushu/evidence/candidate-b-8481/input-manifest.json').read_text())['files'][0]['sha256']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
    bpy.ops.import_scene.fbx(filepath=str(p));raw=next(o for o in bpy.data.objects if o.type=='MESH')
    coords=[raw.matrix_world@v.co for v in raw.data.vertices];raw.matrix_world=Matrix.Identity(4)
    for v,c in zip(raw.data.vertices,coords):v.co=c
    assert len(raw.data.polygons)==8481 and len(raw.data.vertices)==8259
    raw.name='Original_CandidateB_REFERENCE_ONLY';raw.data.materials.clear()
    clay=bpy.data.materials.new('Inspection clay - no texture');clay.diffuse_color=(.58,.58,.58,1);clay.use_nodes=True
    bs=clay.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.58,.58,.58,1);bs.inputs['Roughness'].default_value=.75
    raw.data.materials.append(clay)
    for p in raw.data.polygons:p.use_smooth=True
    groups=components(raw.data);polys=[list(p.vertices) for p in raw.data.polygons];rows=[]
    for i,g in enumerate(groups):
        ids=sorted({v for f in g for v in polys[f]});a=np.array([coords[v] for v in ids]);mp={v:j for j,v in enumerate(ids)}
        if i<8:
            o=mesh('Shushu_'+NAMES[i],a,[[mp[v] for v in polys[f]] for f in g]);parts[NAMES[i]]=o;character.append(o)
            o['part']=NAMES[i];o['donor']='original Candidate B FBX';o['donor_component']=i
        rows.append(dict(index=i,faces=len(g),verts=len(ids),bounds=[a.min(0).tolist(),a.max(0).tolist()],center=a.mean(0).tolist()))
    write('donor-components.json',rows)
    raw.hide_render=True;raw.hide_set(True)
    eye_diagnostics={}
    for side,index in [('R',14),('L',15)]:
        ids=sorted({v for f in groups[index] for v in polys[f]});a=np.array([coords[i] for i in ids]);mp={v:j for j,v in enumerate(ids)}
        cap=BVHTree.FromPolygons(a.tolist(),[[mp[v] for v in polys[f]] for f in groups[index]])
        front=[]
        for x in np.linspace(a[:,0].min()+.001,a[:,0].max()-.001,21):
            for z in np.linspace(a[:,2].min()+.001,a[:,2].max()-.001,25):
                hit=cap.ray_cast(Vector((float(x),-1,float(z))),Vector((0,1,0)))[0]
                if hit is not None:front.append(list(hit))
        a=np.array(front);x=a[:,0];z=a[:,2];A=np.array([np.ones(len(a)),x,z,x*x,x*z,z*z]).T
        eye_fits[side]=np.linalg.lstsq(A,a[:,1],rcond=None)[0]
        eye_diagnostics[side]=dict(front_envelope_samples=len(a),rms_fit_error=float(np.sqrt(np.mean((A@eye_fits[side]-a[:,1])**2))),max_fit_error=float(np.max(np.abs(A@eye_fits[side]-a[:,1]))))
    write('eye-source-envelope.json',eye_diagnostics)
    return coords,polys,groups
def setup_render():
    global cam
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=20;s.cycles.use_denoising=True;s.render.resolution_x=640;s.render.resolution_y=720;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.world=bpy.data.worlds.new('Neutral world');s.world.use_nodes=True
    s.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.22
    s.view_settings.view_transform='AgX'
    for name,loc,power,size in [('Key',(-2,-3,4),200,2.5),('Fill',(3,-2,2),65,3),('Rim',(0,3,3),140,2)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
    cam=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO'
    ground=mesh('Inspection_Ground',[(-20,-20,-.002),(20,-20,-.002),(20,20,-.002),(-20,20,-.002)],[(0,1,2,3)])
    return cam
def clean_modules():
    stats={}
    for name,o in parts.items():
        bm=bmesh.new();bm.from_mesh(o.data)
        before=len(bm.verts);boundary=[e for e in bm.edges if e.is_boundary]
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00005)
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.00001)
        # Remove only small local fan defects inherited from the triangulated source.
        bad=[e for e in bm.edges if len(e.link_faces)>2]
        doomed=list({f for e in bad for f in e.link_faces})
        if doomed:bmesh.ops.delete(bm,geom=doomed,context='FACES')
        loose=[v for v in bm.verts if not v.link_faces]
        if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
        boundary=[e for e in bm.edges if e.is_boundary]
        if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        stats[name]=dict(original_vertices=before,filled_boundary_edges=len(boundary),nonmanifold=sum(not e.is_manifold for e in bm.edges))
        bm.to_mesh(o.data);bm.free();activate(o)
        # One subdivision removes the coarse source facets. No voxel remesh or broad relaxation.
        sub=o.modifiers.new('Single donor subdivision','SUBSURF');sub.levels=1
        bpy.ops.object.modifier_apply(modifier=sub.name)
        bm=bmesh.new();bm.from_mesh(o.data);boundary=[e for e in bm.edges if e.is_boundary]
        if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
    write('module-repair.json',stats)
    h=tree(parts['Head']);samples={}
    for x in [0,.025,.05,.09,.13,.18,.23]:
        samples[str(x)]=[[z,tuple(h.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))[0] or Vector((0,0,0)))[1]] for z in np.arange(.53,.751,.01)]
    write('native-face-depth-samples.json',samples)
def native_y(x,z):
    hit=head_surface.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))[0]
    assert hit is not None,(x,z)
    return hit.y
def eye_y(side,x,z):
    a=eye_fits[side];return float(a@np.array([1,x,z,x*x,x*z,z*z]))
def eye_point(side,a,r=1):
    s=1 if side=='L' else -1;tilt=s*math.radians(22)
    x=.052*r*math.cos(a);z=.068*r*math.sin(a)
    return s*.129+x*math.cos(tilt)-z*math.sin(tilt),.660+x*math.sin(tilt)+z*math.cos(tilt)
def mouth_point(a,opening=0,smile=0,surprise=0):
    x=(.026*(1-surprise)+.013*surprise)*math.cos(a)
    # Two small resting lobes under preserved native muzzle / philtrum.
    z=.600-.003*math.sin(math.pi*abs(x)/.026)+.004*smile*(abs(x)/.026)**2
    z+=(.001+.008*opening+.010*surprise)*math.sin(a)
    y=-.266+2.0*x*x+.10*(z-.600)
    return Vector((x,y,z))
def cut_patch(cx,cz,rx,rz,label):
    bm=face_bm;planes=[];tag=bm.verts.layers.int.get('motion_vertex') or bm.verts.layers.int.new('motion_vertex')
    for i in range(40):
        a=i/40*math.tau;n=Vector((math.cos(a)/rx,0,math.sin(a)/rz));planes.append(n)
        local=[f for f in bm.faces if not any(v[tag] for v in f.verts) and f.calc_center_median().y<-.07 and ((f.calc_center_median().x-cx)/rx)**2+((f.calc_center_median().z-cz)/rz)**2<2.2]
        geom=list({item for f in local for item in [f,*f.edges,*f.verts]})
        bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-7,plane_co=(cx+rx*math.cos(a),0,cz+rz*math.sin(a)),plane_no=n)
    doomed=[f for f in bm.faces if f.calc_center_median().y<-.07 and all(n.dot(f.calc_center_median()-Vector((cx,0,cz)))<1+1e-6 for n in planes)]
    bmesh.ops.delete(bm,geom=doomed,context='FACES')
    loose=[v for v in bm.verts if not v.link_faces]
    if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
    be=[e for e in bm.edges if e.is_boundary and all(v.co.y<-.07 and ((v.co.x-cx)/rx)**2+((v.co.z-cz)/rz)**2<1.18 for v in e.verts)]
    adj=defaultdict(list)
    for e in be:
        a,b=e.verts;adj[a].append(b);adj[b].append(a)
    assert adj and all(len(v)==2 for v in adj.values()),(label,'invalid patch boundary',Counter(map(len,adj.values())))
    start=min(adj,key=lambda v:v.co.x);bv=[start];prev=None;cur=start
    while True:
        nxt=next(v for v in adj[cur] if v!=prev)
        if nxt==start:break
        bv.append(nxt);prev,cur=cur,nxt;assert len(bv)<=len(adj)
    if len(bv)!=len(adj):
        loops=[bv];remaining=set(adj)-set(bv)
        while remaining:
            start=next(iter(remaining));loop=[start];prev=None;cur=start
            while True:
                nxt=next(v for v in adj[cur] if v!=prev)
                if nxt==start:break
                loop.append(nxt);prev,cur=cur,nxt
            remaining-=set(loop);loops.append(loop)
        print('PATCH_LOOPS',label,[len(loop) for loop in loops],flush=True)
        bv=max(loops,key=len)
        for loop in loops:
            if loop is not bv:
                es=[e for e in be if all(v in loop for v in e.verts)]
                bmesh.ops.holes_fill(bm,edges=es,sides=0)
    rows=[bv];data=[]
    for j in range(1,9):
        t=j/8;row=[]
        for v in bv:
            a=math.atan2((v.co.z-cz)/rz,(v.co.x-cx)/rx)
            if label=='Mouth':target=mouth_point(a)
            else:
                x,z=eye_point(label,a);target=Vector((x,eye_y(label,x,z)+.0007,z))
            x=(1-t)*v.co.x+t*target.x;z=(1-t)*v.co.z+t*target.z
            # Blend from the actual donor boundary; no analytic head-surface replacement.
            # Hermite continuation avoids retaining the old recessed eye or open-mouth bowl.
            w=smooth(0,1,t);y=(1-w)*v.co.y+w*target.y
            if label=='Mouth':y=(1-t)*v.co.y+t*target.y-.003*math.sin(math.pi*t)
            if label!='Mouth':
                yn=native_y(x,z);y=(1-smooth(.0,.65,t))*yn+smooth(.0,.65,t)*y
            nv=bm.verts.new((x,y,z));nv[tag]=1;row.append(nv);data.append((nv,t,a,v.co.copy(),target))
        rows.append(row)
        for i in range(len(row)):
            k=(i+1)%len(row);bm.faces.new((rows[-2][i],rows[-2][k],row[k],row[i]))
    return data
def build_face():
    global face_bm,head_surface
    head=parts['Head'];head_surface=tree(head);face_bm=bmesh.new();face_bm.from_mesh(head.data)
    for side,s in [('L',1),('R',-1)]:patches[side]=cut_patch(s*.129,.660,.082,.092,side)
    patches['Mouth']=cut_patch(0,.575,.063,.046,'Mouth')
    face_bm.verts.index_update()
    for key,data in patches.items():patches[key]=[(v.index,t,a,b,tar) for v,t,a,b,tar in data]
    bmesh.ops.recalc_face_normals(face_bm,faces=list(face_bm.faces));face_bm.to_mesh(head.data);face_bm.free()
    for poly in head.data.polygons:poly.use_smooth=True
    for label,data in patches.items():
        for idx,t,a,b,tar in data:
            co=head.data.vertices[idx].co;assert abs(co.x-((1-t)*b.x+t*tar.x))<1e-5 and abs(co.z-((1-t)*b.z+t*tar.z))<1e-5,(label,idx,tuple(co),tuple(b),tuple(tar))
    for side,s in [('L',1),('R',-1)]:
        k=shape(head,'Blink.'+side,lambda p:p)
        for idx,t,a,b,tar in patches[side]:
            seam=.640+s*.24*(tar.x-s*.129)+.006*(1-((tar.x-s*.129)/.058)**2)
            x=(1-t)*b.x+t*tar.x;z=(1-t)*b.z+t*seam
            # The closing lid follows the eye envelope. Bridging to a fitted
            # forehead surface leaves a deep empty wedge in three-quarter view.
            w=smooth(0,1,t);y=(1-w)*b.y+w*(eye_y(side,x,z)-.004)
            y=(1-smooth(0,.65,t))*native_y(x,z)+smooth(0,.65,t)*y
            k.data[idx].co=(x,y,z)
        correct=shape(head,'Corrective.HalfBlink.'+side,lambda p:p)
        basis=head.data.shape_keys.key_blocks['Basis']
        for idx,t,a,b,tar in patches[side]:
            mid=(basis.data[idx].co+k.data[idx].co)*.5
            tilt=s*math.radians(22)
            # Keep both canthi on the original cap. The upper lid does most of
            # the closing; translating a smaller ellipse can expose the corner.
            lv=(.012 if math.sin(a)>=0 else .058)*math.sin(a)
            hx=s*.129+.052*math.cos(a)*math.cos(tilt)-lv*math.sin(tilt)
            hz=.660+.052*math.cos(a)*math.sin(tilt)+lv*math.cos(tilt)
            x=(1-t)*b.x+t*hx;z=(1-t)*b.z+t*hz
            target_y=eye_y(side,hx,hz)-.006
            w=smooth(0,1,t);y=(1-w)*b.y+w*target_y
            y=(1-smooth(0,.65,t))*native_y(x,z)+smooth(0,.65,t)*y
            xx=x-s*.129;zz=z-.660
            u=xx*math.cos(tilt)+zz*math.sin(tilt);v=-xx*math.sin(tilt)+zz*math.cos(tilt)
            radius=(u/.052)**2+(v/.068)**2
            if radius<1.04 and t>.15:y=min(y,eye_y(side,x,z)-.006)
            correct.data[idx].co+=Vector((x,y,z))-mid
        driver=correct.driver_add('value').driver;var=driver.variables.new();var.name='blink';var.type='SINGLE_PROP';var.targets[0].id_type='KEY';var.targets[0].id=head.data.shape_keys
        var.targets[0].data_path=f'key_blocks["Blink.{side}"].value';driver.expression='max(0,1-abs(blink-0.5)*2)'
        # Eye cap retains donor depth and tilt, becomes recessed only while closing.
        verts=[Vector((s*.129,eye_y(side,s*.129,.660),.660))];faces=[];n=64
        for j in range(1,9):
            for i in range(n):
                x,z=eye_point(side,i/n*math.tau,j/8);verts.append((x,eye_y(side,x,z),z))
        for i in range(n):faces.append((0,1+i,1+(i+1)%n))
        for j in range(7):
            for i in range(n):
                a=1+j*n+i;b=1+j*n+(i+1)%n;faces.append((a,a+n,b+n,b))
        # Continue the source-derived front cap under the lids. A front-only
        # sheet exposes empty space through partially closed lids in side views.
        for radius,depth in [(1.30,.001),(1.38,.025),(.8,.10)]:
            start=len(verts);previous=start-n
            for i in range(n):
                x,z=eye_point(side,i/n*math.tau,radius);verts.append((x,eye_y(side,x,z)+depth,z))
            for i in range(n):
                a=previous+i;b=previous+(i+1)%n;faces.append((a,a+n,b+n,b))
        rear=len(verts);verts.append((s*.129,eye_y(side,s*.129,.660)+.12,.660));start=rear-n
        for i in range(n):faces.append((start+i,rear,start+(i+1)%n))
        eye=mesh('Shushu_Eye.'+side,verts,faces);character.append(eye);eye['part']='Eye.'+side
        shape(eye,'Blink.'+side,lambda p:p)
        retract=shape(eye,'Corrective.ClosedRetraction.'+side,lambda p:p+Vector((0,.012,0)))
        driver=retract.driver_add('value').driver;var=driver.variables.new();var.name='blink';var.type='SINGLE_PROP';var.targets[0].id_type='KEY';var.targets[0].id=eye.data.shape_keys
        var.targets[0].data_path=f'key_blocks["Blink.{side}"].value';driver.expression='max(0,min(1,(blink-0.8)/0.2))**2'
        for label,dx,dz in [('GazeLeft',-.004,0),('GazeRight',.004,0),('GazeUp',0,.003),('GazeDown',0,-.003)]:
            def gaze(p):
                w=max(0,1-((p.x-s*.129)/.065)**2-((p.z-.660)/.08)**2)**2
                depth=p.y-eye_y(side,p.x,p.z)
                p.x+=dx*w;p.z+=dz*w;p.y=eye_y(side,p.x,p.z)+depth;return p
            shape(eye,label,gaze)
    for name,op,sm,su in [('MouthOpen',1,0,0),('GentleSmile',0,1,0),('Surprise',0,0,1)]:
        k=shape(head,name,lambda p:p)
        for idx,t,a,b,tar in patches['Mouth']:k.data[idx].co+=(mouth_point(a,op,sm,su)-tar)*t*t
    # Recessed bowl attached to the exact moving mouth edge; front faces never cover it.
    verts=[Vector((0,-.224,.598))];n=64
    for i in range(n):verts.append(mouth_point(i/n*math.tau)+Vector((0,.0005,0)))
    mouth=mesh('Shushu_MouthInterior',verts,[(0,1+(i+1)%n,1+i) for i in range(n)]);character.append(mouth);mouth['part']='MouthInterior'
    for name,op,sm,su in [('MouthOpen',1,0,0),('GentleSmile',0,1,0),('Surprise',0,0,1)]:
        k=shape(mouth,name,lambda p:p)
        for i,v in enumerate(list(k.data)[1:]):v.co=mouth_point(i/n*math.tau,op,sm,su)+Vector((0,.0005,0))
    happy=shape(head,'HappyLids',lambda p:p)
    for side,s in [('L',1),('R',-1)]:
        for idx,t,a,b,tar in patches[side]:happy.data[idx].co.z+=.012*max(0,1-((tar.x-s*.129)/.066)**2)*t*t
    def cheek(p):
        w=math.exp(-2*(((p.x-.240)/.055)**2+((p.y+.165)/.08)**2+((p.z-.559)/.055)**2))*(1-smooth(.585,.612,p.z))*smooth(.18,.21,p.x)
        p.x-=.015*w;p.y+=.006*w;return p
    shape(head,'CheekPressure.L',cheek)
    sub=head.modifiers.new('Lid surface continuity','SUBSURF');sub.levels=1;sub.render_levels=1
    # A real inner lid wall closes the parallax gap between skin and eye.
    # Restrict thickness to the two orbital patches; keep other source surfaces.
    for side in ['L','R']:
        lid_group=head.vertex_groups.new(name='Local eyelid thickness.'+side)
        for idx,t,a,b,tar in patches[side]:lid_group.add([idx],t*t,'REPLACE')
        wall=head.modifiers.new('Inner eyelid wall.'+side,'SOLIDIFY');wall.thickness=.030;wall.offset=-1
        wall.vertex_group=lid_group.name;wall.thickness_vertex_group=0;wall.use_rim=True;wall.use_rim_only=True
        driver=wall.driver_add('thickness').driver;var=driver.variables.new();var.name='blink';var.type='SINGLE_PROP';var.targets[0].id_type='KEY';var.targets[0].id=head.data.shape_keys
        var.targets[0].data_path=f'key_blocks["Blink.{side}"].value';driver.expression='0.030*max(0,min(1,(1-blink)/0.1))'
def reset():
    for o in character:
        if o.data.shape_keys:
            for k in o.data.shape_keys.key_blocks:
                if not k.name.startswith('Corrective.'):k.value=0
        o.data.update();o.update_tag()

def seat_point(p,t,part):
    p=p.copy()
    if part=='Torso':
        old=p.copy();low=1-smooth(.23,.42,old.z)
        front=smooth(.015,.19,-old.y)*math.exp(-((old.z-.24)/.115)**2)
        p+=Vector((0,.06*t,-.129*t))
        p.x*=1+.035*t*low
        p.y+=t*(.035*front+.014*low*smooth(.01,.15,old.y))
        p.z+=.036*t*front
    elif part.startswith('Leg.'):
        s=1 if part.endswith('L') else -1
        c=Vector((s*.14,0,.06))
        q=Quaternion((0,0,1),s*math.radians(12)*t)@Quaternion((1,0,0),-math.radians(68)*t)
        foot_z=seat_foot_height[(part,round(t,4))]
        cnew=Vector((s*(.14+.05*t),-.178*t,foot_z))
        w=smooth(.080,.238,p.z)
        axis=Vector((s*.14,0,p.z))
        foot=cnew+q@(axis-c)
        hip=axis+Vector((s*.008*t,.065*t,-.09*t))
        center=foot.lerp(hip,w)+Vector((s*.012*t*math.sin(math.pi*w),.012*t*math.sin(math.pi*w),.008*t*math.sin(math.pi*w)))
        thigh=Quaternion((0,0,1),s*math.radians(5)*t)@Quaternion((1,0,0),-math.radians(90)*t)
        frame=q.slerp(thigh,w)
        p=center+frame@(p-axis)
    else:p+=Vector((0,.04*t,-.129*t))
    return p

seat_foot_height={}
def build_body():
    # Sample a rotating foot and curved leg centerline, preserving radial thickness.
    for t in [.25,.5,.75,1.]:
        for part in ['Leg.L','Leg.R']:
            s=1 if part.endswith('L') else -1;c=Vector((s*.14,0,.06))
            q=Quaternion((0,0,1),s*math.radians(12)*t)@Quaternion((1,0,0),-math.radians(68)*t)
            seat_foot_height[(part,round(t,4))]=.001-min((q@(v.co-c)).z for v in parts[part].data.vertices if v.co.z<.085)
        for o in character:
            part=o.get('part','Head');shape(o,f'Seat{int(t*100):03d}',lambda p:seat_point(p,t,part))
    for side,s in [('L',1),('R',-1)]:
        o=parts['Paw.'+side];anchor=Vector((s*.16,.025,.46));tip=Vector((s*.315,-.030,.340));axis=tip-anchor
        targets={'Hold':Vector((s*.122,-.265,.362)), 'Offer':Vector((s*.155,-.310,.375))}
        if side=='L':targets['SelfContact']=Vector((.267,-.155,.550))
        for label,dest in targets.items():
            rotation=axis.rotation_difference(dest-anchor)
            def deform(p):
                w=smooth(.025,.145,(p-anchor).length)
                out=anchor+Quaternion().slerp(rotation,w)@(p-anchor)
                if label in ['Hold','Offer']:out+=Vector((-s*.018,-.050,.006 if label=='Offer' else 0))*w*w
                if label=='SelfContact':out+=Vector((.050,-.045,-.015))*w*w
                return out
            shape(o,label+'.'+side,deform)
    for o in character:
        part=o.get('part','')
        if part in ['Head','Ear.L','Ear.R','Eye.L','Eye.R','MouthInterior']:
            pivot=Vector((0,.02,.52))
            face_keys=[k for k in o.data.shape_keys.key_blocks if k.name!='Basis' and not k.name.startswith('Seat')]
            for label,axis,angle in [('HeadTurn.L',(0,0,1),22),('HeadTurn.R',(0,0,1),-22),('HeadTilt.L',(0,1,0),12),('HeadTilt.R',(0,1,0),-12),('HeadRest',(1,0,0),10)]:
                q=Quaternion(axis,math.radians(angle));shape(o,label,lambda p:pivot+q@(p-pivot))
                # Rotate facial deltas with the head, not in the original world
                # frame. Otherwise a closed eye separates when the head tilts.
                for face_key in face_keys:
                    c=shape(o,'Corrective.Compose.'+label+'.'+face_key.name,lambda p:p)
                    for dest,face,basis in zip(c.data,face_key.data,o.data.shape_keys.key_blocks['Basis'].data):
                        delta=face.co-basis.co;dest.co+=q@delta-delta
                    driver=c.driver_add('value').driver
                    for varname,keyname in [('head',label),('face',face_key.name)]:
                        var=driver.variables.new();var.name=varname;var.type='SINGLE_PROP';var.targets[0].id_type='KEY';var.targets[0].id=o.data.shape_keys;var.targets[0].data_path=f'key_blocks["{keyname}"].value'
                    driver.expression='head*face'
        if part=='Torso':
            def breath(p):
                w=math.exp(-((p.z-.36)/.13)**2);p.x*=1+.008*w;p.y*=1+.008*w;return p
            shape(o,'Breath',breath)

def sit(t):
    for a in [25,50,75,100]:key(f'Seat{a:03d}',max(0,1-abs(t-a/100)/.25))

def pose(name):
    reset()
    if name.startswith('seat'):sit(float(name[4:])/100)
    elif name=='hold':key('Hold.L');key('Hold.R')
    elif name=='offer':key('Offer.L');key('Offer.R')
    elif name=='self-contact':key('SelfContact.L',.6);key('HeadTilt.L',.9);key('CheekPressure.L',.15)
    elif name=='rest':sit(1);key('HeadRest');key('Blink.L',.7);key('Blink.R',.7)
    elif name=='turn-tilt':key('HeadTurn.L');key('HeadTilt.L')

def arrange():
    for name in ['CHARACTER_EDITABLE','SOURCE_REFERENCE_ONLY','INSPECTION_ONLY']:
        if name not in bpy.data.collections:
            c=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(c)
    for o in list(bpy.context.scene.objects):
        dest='CHARACTER_EDITABLE' if o in character else ('SOURCE_REFERENCE_ONLY' if o.name.startswith('Original_') else 'INSPECTION_ONLY')
        for c in list(o.users_collection):c.objects.unlink(o)
        bpy.data.collections[dest].objects.link(o)
    bpy.data.collections['SOURCE_REFERENCE_ONLY'].hide_render=True
    note=bpy.data.texts.new('READ_ME_v003')
    note.write('Original Candidate B donor only. Geometry and disposable pose proof; not a final rig.\n'
               'All facial keys are explicitly relative to Basis. Use values 0..1.\n'
               'Seat025/050/075/100 are sampled poses: crossfade adjacent keys, never add all four.\n'
               'Reset all keys to zero for the neutral source-derived shape.\n'
               'Static FBX/GLB exclude this source collection, the stage, materials, keys and actions.\n'
               'Research and review: docs/production/shushu/evidence/geometry-v003/.\n'
               'Human Geometry Gate pending. Tripo runtime acceptance UNKNOWN; no upload performed.\n')

def build_prop():
    pose('hold');trees=[tree(parts['Paw.'+s]) for s in ['L','R']];body=tree(parts['Torso'])
    candidates=[]
    for y in np.linspace(-.34,-.275,27):
        for z in np.linspace(.345,.410,27):
            c=Vector((0,float(y),float(z)));ds=[tr.find_nearest(c)[3] for tr in trees];r=sum(ds)/2
            # The sphere must be outside the abdomen and bounded by both paws.
            clearance=body.find_nearest(c)[3]-r
            if .048<r<.092 and clearance>.002:
                score=abs(r-.068)+2*abs(ds[0]-ds[1])+abs(y+.305)*.1
                candidates.append((score,c,r,ds,clearance))
    assert candidates,'No nonpenetrating bounded hold found'
    _,c,r,ds,clearance=min(candidates,key=lambda v:v[0])
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=20,radius=r,location=c)
    prop=bpy.context.object;prop.name='Inspection_HeldProp';prop.data.materials.append(clay)
    for f in prop.data.polygons:f.use_smooth=True
    prop['inspection_only']=True;prop['radius']=r;prop['hold_center']=list(c)
    for col in list(prop.users_collection):col.objects.unlink(prop)
    bpy.data.collections['INSPECTION_ONLY'].objects.link(prop)
    prop.hide_render=True;prop.hide_set(True)
    write('hold-contact.json',dict(center=list(c),radius=r,paw_surface_distance=ds,paw_gap=[d-r for d in ds],torso_clearance=clearance,meaning='Tangent inspection sphere; no grasp force or collision simulation claim.'))
    reset();return prop

def validate_geometry():
    reset();neutral={o.name:evaluated(o)[0] for o in character};stats={}
    for o in character:
        bm=bmesh.new();bm.from_mesh(o.data)
        stats[o.name]=dict(vertices=len(bm.verts),faces=len(bm.faces),boundary_edges=sum(e.is_boundary for e in bm.edges),nonmanifold_branch_edges=sum(len(e.link_faces)>2 for e in bm.edges))
        bm.free()
    ground=[]
    for t in np.linspace(0,1,41):
        reset();sit(float(t));row={'sit':float(t)}
        for part in ['Leg.L','Leg.R','Torso']:row[part+'_min_z']=float(evaluated(parts[part])[0][:,2].min())
        ground.append(row)
    coverage={}
    for amount in [0,.5,1]:
        reset();key('Blink.L',amount);key('Blink.R',amount);head=tree(parts['Head']);row={}
        for side in ['L','R']:
            eye=next(o for o in character if o.get('part')=='Eye.'+side);v=evaluated(eye)[0];hidden=0;total=0
            # Interior cap samples only; ignore the coincident edge itself.
            for p in v[1:1+6*64:3]:
                hit=head.ray_cast(Vector((float(p[0]),-1,float(p[2]))),Vector((0,1,0)))[0]
                total+=1;hidden+=bool(hit is not None and hit.y<float(p[1])-.00005)
            row[side]=dict(occluded=hidden,total=total,fraction=hidden/total)
        coverage[str(amount)]=row
    pose('self-contact');head=tree(parts['Head']);vv=evaluated(parts['Paw.L'])[0]
    signed=[];all_nearest=[]
    for p,b in zip(vv,parts['Paw.L'].data.shape_keys.key_blocks['Basis'].data):
        if p[2]>.49 and (b.co-Vector((.16,.025,.46))).length>.145:
            hit,n,idx,d=head.find_nearest(Vector(p));all_nearest.append(d)
            if d<.025:signed.append(d if (Vector(p)-hit).dot(n)>=0 else -d)
    reset();deviation=max(float(np.abs(evaluated(o)[0]-neutral[o.name]).max()) for o in character)
    result=dict(meshes=stats,seat_ground_sweep=ground,blink_cap_occlusion=coverage,neutral_reset_max_coordinate_error=deviation,
                self_contact_signed_nearest=dict(min=min(signed),max=max(signed),samples=len(signed),nearest_distance=min(all_nearest),note='Distal paw only, within .025 of head; excludes shoulder attachment. Signed local-normal proxy, not a global inside/outside or collision solver. Visual review required.'),
                human_gate='PENDING',tripo_studio='UNKNOWN_NO_UPLOAD')
    write('geometry-checks.json',result)
    assert deviation<1e-7
    assert all(row['Leg.L_min_z']>-.001 and row['Leg.R_min_z']>-.001 for row in ground),'leg below support plane'
    assert all(coverage['1'][s]['fraction']>.98 for s in ['L','R']),'closed lid exposes eye'
    return result

def merged(objects):
    verts=[];faces=[]
    for o in objects:
        v,t=evaluated(o);offset=len(verts);verts.extend(v.tolist());faces.extend((t+offset).tolist())
    return verts,faces

def export_static():
    reset();STATIC.parent.mkdir(parents=True,exist_ok=True);dg=bpy.context.evaluated_depsgraph_get();copies=[]
    for o in character:
        m=bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=False,depsgraph=dg)
        # Zero-weight rim regions can produce zero-area faces; omit them from
        # the static interchange mesh while preserving the evaluated surface.
        bm=bmesh.new();bm.from_mesh(m);flat=[f for f in bm.faces if f.calc_area()<1e-12]
        if flat:bmesh.ops.delete(bm,geom=flat,context='FACES')
        bm.to_mesh(m);bm.free();m.update()
        m.materials.clear()
        for uv in list(m.uv_layers):m.uv_layers.remove(uv)
        cp=bpy.data.objects.new(o.name.replace('Shushu_','ShushuStatic_'),m);bpy.context.scene.collection.objects.link(cp);copies.append(cp)
    bpy.ops.object.select_all(action='DESELECT')
    for o in copies:o.select_set(True)
    bpy.context.view_layer.objects.active=copies[0]
    bpy.ops.export_scene.fbx(filepath=str(STATIC.with_suffix('.fbx')),use_selection=True,object_types={'MESH'},bake_anim=False,add_leaf_bones=False,axis_forward='-Z',axis_up='Y')
    bpy.ops.export_scene.gltf(filepath=str(STATIC.with_suffix('.glb')),export_format='GLB',use_selection=True,export_materials='NONE',export_animations=False,export_texcoords=False,export_yup=True)
    base,tri=merged(copies);baseline=BVHTree.FromPolygons(base,tri,all_triangles=True);checks={}
    for o in copies:bpy.data.objects.remove(o,do_unlink=True)
    for ext in ['fbx','glb']:
        before=set(bpy.data.objects)
        if ext=='fbx':bpy.ops.import_scene.fbx(filepath=str(STATIC.with_suffix('.fbx')))
        else:bpy.ops.import_scene.gltf(filepath=str(STATIC.with_suffix('.glb')))
        imported=set(bpy.data.objects)-before;meshes=[o for o in imported if o.type=='MESH'];v,t=merged(meshes);rt=BVHTree.FromPolygons(v,t,all_triangles=True)
        a=max(baseline.find_nearest(Vector(p))[3] for p in v);b=max(rt.find_nearest(Vector(p))[3] for p in base)
        checks[ext]=dict(meshes=len(meshes),vertices=len(v),triangles=len(t),forward_max_surface_error=a,reverse_max_surface_error=b,shape_keys=sum(o.data.shape_keys is not None for o in meshes),armatures=sum(o.type=='ARMATURE' for o in imported),uv_layers=sum(len(o.data.uv_layers) for o in meshes),bytes=STATIC.with_suffix('.'+ext).stat().st_size,sha256=hashlib.sha256(STATIC.with_suffix('.'+ext).read_bytes()).hexdigest())
        assert max(a,b)<2e-5 and len(meshes)==len(character)
        assert checks[ext]['shape_keys']==checks[ext]['armatures']==checks[ext]['uv_layers']==0
        for o in imported:bpy.data.objects.remove(o,do_unlink=True)
    write('static-roundtrip.json',checks)

def make_proof(prop):
    s=bpy.context.scene;s.render.fps=24;s.frame_start=1;s.frame_end=285
    frames=[(1,'neutral'),(9,'half'),(13,'closed'),(17,'half'),(23,'neutral'),(29,'wink'),(35,'neutral'),(41,'gaze-left'),(47,'gaze-right'),(53,'gaze-up'),(59,'neutral'),(65,'mouth-open'),(71,'smile'),(77,'surprise'),(83,'neutral'),(89,'turn-tilt'),(101,'neutral'),(109,'seat25'),(117,'seat50'),(125,'seat75'),(133,'seat100'),(149,'rest'),(157,'seat100'),(165,'seat75'),(173,'seat50'),(181,'seat25'),(189,'neutral'),(201,'offer'),(213,'hold'),(225,'hold'),(237,'release'),(249,'neutral'),(261,'self-contact'),(273,'neutral'),(285,'neutral')]
    c=Vector(prop['hold_center'])
    for frame,state in frames:
        pose(state)
        if state in ['half','closed']:key('Blink.L',.5 if state=='half' else 1);key('Blink.R',.5 if state=='half' else 1)
        if state=='wink':key('Blink.L')
        if state.startswith('gaze-'):key({'gaze-left':'GazeLeft','gaze-right':'GazeRight','gaze-up':'GazeUp'}[state])
        if state=='mouth-open':key('MouthOpen',.8)
        if state=='smile':key('GentleSmile');key('Blink.L',.22);key('Blink.R',.22)
        if state=='surprise':key('Surprise')
        if state=='release':key('Offer.L',.6);key('Offer.R',.6)
        for o in character:
            if o.data.shape_keys:
                for k in list(o.data.shape_keys.key_blocks)[1:]:
                    if not k.name.startswith('Corrective.'):k.keyframe_insert('value',frame=frame)
        prop.hide_render=not (201<=frame<=237);prop.keyframe_insert('hide_render',frame=frame)
        prop.hide_viewport=prop.hide_render;prop.keyframe_insert('hide_viewport',frame=frame)
        prop.location=c+(Vector((0,-.12,.025)) if state=='release' else Vector((0,0,0)));prop.keyframe_insert('location',frame=frame)
        s.timeline_markers.new(state,frame=frame)
    # Linear curves keep sampled poses and support positions bounded.
    for action in bpy.data.actions:
        for layer in action.layers:
            for strip in layer.strips:
                for slot in action.slots:
                    bag=strip.channelbag(slot)
                    if bag:
                        for fc in bag.fcurves:
                            for p in fc.keyframe_points:p.interpolation='CONSTANT' if fc.data_path in ['hide_render','hide_viewport'] else 'LINEAR'
    prop.hide_set(False);s.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(PROOF))

def key(name,value=1):
    for o in character:
        if o.data.shape_keys and name in o.data.shape_keys.key_blocks:o.data.shape_keys.key_blocks[name].value=value
def render(name,direction=(0,-1,.04),target=(0,0,.49),scale=1.15):
    d=Vector(direction).normalized();cam.location=Vector(target)+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    bpy.context.scene.render.filepath=str(OUT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)
    render_records[name]=dict(direction=list(direction),target=list(target),orthographic_scale=scale,engine=bpy.context.scene.render.engine,resolution=[640,720])
def main():
    global cam,character,parts,clay,raw
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'renders').mkdir(exist_ok=True)
    if any(arg in sys.argv for arg in ['--face-only','--character-only']) and (OUT/'review-cameras.json').exists():render_records.update(json.loads((OUT/'review-cameras.json').read_text()))
    import_source();setup_render()
    if '--inspect' in sys.argv:
        for o in character:o.hide_render=True
        raw.hide_render=False
        for name,direction,target,scale in [('donor-front',(0,-1,0),(0,0,.49),1.15),('donor-left',(-1,0,0),(0,0,.49),1.15),('donor-face',(0,-1,0),(0,-.04,.67),.58),('donor-face-side',(-1,0,0),(0,-.04,.67),.58)]:render(name,direction,target,scale)
        print('INSPECT_COMPLETE',flush=True);return
    clean_modules()
    build_face()
    build_body()
    reset();arrange()
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    bpy.ops.wm.open_mainfile(filepath=str(ASSET))
    cam=bpy.data.objects['ReviewCamera'];character=[o for o in bpy.data.objects if o.name.startswith('Shushu_')]
    parts={n:bpy.data.objects['Shushu_'+n] for n in NAMES}
    raw=bpy.data.objects['Original_CandidateB_REFERENCE_ONLY'];clay=bpy.data.materials['Inspection clay - no texture']
    prop=build_prop();validate_geometry();export_static()
    if '--no-render' in sys.argv:
        reset();bpy.ops.wm.save_as_mainfile(filepath=str(ASSET));make_proof(prop);print('V003_BUILD_COMPLETE',flush=True);return
    if '--quick' in sys.argv:
        bpy.context.scene.render.engine='BLENDER_WORKBENCH';s=bpy.context.scene
        s.display.shading.light='STUDIO';s.display.shading.show_shadows=False;s.display.shading.show_cavity=True;s.display.shading.color_type='SINGLE'
    views=[('front',(0,-1,0)),('left',(1,0,0)),('right',(-1,0,0)),('three-quarter',(1,-1,0)),('rear',(0,1,0))]
    if '--face-only' in sys.argv:views=[]
    for name,d in views:render('neutral-'+name,d)
    for o in character:o.hide_render=True
    raw.hide_render=False;raw.hide_set(False);bpy.data.collections['SOURCE_REFERENCE_ONLY'].hide_render=False
    for name,d in ([] if '--character-only' in sys.argv else views):render('donor-'+name,d)
    if '--character-only' not in sys.argv:render('donor-face',(0,-1,0),(0,-.04,.65),.50)
    raw.hide_render=True;raw.hide_set(True);bpy.data.collections['SOURCE_REFERENCE_ONLY'].hide_render=True
    for o in character:o.hide_render=False
    for state in ['neutral','half','closed','reopen','wink','gaze-left','gaze-right','mouth-open','smile','surprise']:
        reset()
        if state in ['half','closed']:key('Blink.L',.5 if state=='half' else 1);key('Blink.R',.5 if state=='half' else 1)
        if state=='mouth-open':key('MouthOpen')
        if state=='wink':key('Blink.L')
        if state.startswith('gaze-'):key('GazeLeft' if state=='gaze-left' else 'GazeRight')
        if state=='smile':key('GentleSmile');key('Blink.L',.22);key('Blink.R',.22)
        if state=='surprise':key('Surprise')
        render('face-'+state,(0,-1,0),(0,-.04,.65),.50)
        if state=='neutral':render('face-neutral-side',(1,0,0),(0,-.04,.65),.58)
        if state=='smile':render('face-smile-three-quarter',(1,-1,0),(0,-.04,.65),.58)
    for amount,label in [(.7,'partial'),(1,'closed')]:
        reset();key('Blink.L',amount);key('Blink.R',amount)
        render('face-'+label+'-three-quarter',(1,-1,0),(0,-.04,.65),.58)
    for state in (['rest'] if '--face-only' in sys.argv else ['seat25','seat50','seat75','seat100','hold','offer','self-contact','turn-tilt','rest']):
        pose(state)
        prop.hide_render=state!='hold'
        prop.hide_set(state!='hold')
        render(state,(1,-1,.12))
        if state=='seat100':
            render('seated-front',(0,-1,0));render('seated-left',(1,0,0))
            render('seated-rear-three-quarter',(1,.35,.10))
        if state=='hold':render('hold-front',(0,-1,0))
        if state=='self-contact':render('self-contact-detail',(1,-1,0),(0,-.04,.59),.72)
    reset();prop.hide_render=True
    render('release',(1,-1,.12))
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    make_proof(prop)
    write('review-cameras.json',render_records)
    print('V003_BUILD_COMPLETE',flush=True)
if __name__=='__main__':main()
