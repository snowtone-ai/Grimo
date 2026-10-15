"""Bounded diagnostic duplicates, unchanged delivery, multi-view comparisons.

No source/final vertices or normals are edited. Trial stripping is quarantined.
Run with Blender --background --factory-startup --python <this file>.
"""
import bpy,bmesh,json,math,hashlib,struct,sys
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import convex_hull_2d
sys.path.insert(0,str(Path(__file__).parent))
import importlib.util
spec=importlib.util.spec_from_file_location('pino_audit',Path(__file__).with_name('audit-pino-c-geometry.py'))
u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
ROOT,ASSET,OUT=u.ROOT,u.ASSET,u.OUT
RENDERS=OUT/'renders';RENDERS.mkdir(exist_ok=True)
RAW=np.load(OUT/'glb-diagnostic-arrays.npz');V,T,L=[RAW[k] for k in ['vertices','triangles','components']]
SOURCE=ASSET/'source/cute blue creature 3d model.glb'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def write_json(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def winding(points,triangles):
    out=[]
    for i in range(0,len(points),24):
        q=V[triangles][None,:,:,:]-points[i:i+24,None,None,:]
        a,b,c=q[:,:,0],q[:,:,1],q[:,:,2]
        na,nb,nc=[np.linalg.norm(x,axis=-1) for x in [a,b,c]]
        det=np.einsum('ijk,ijk->ij',a,np.cross(b,c))
        den=na*nb*nc+np.einsum('ijk,ijk->ij',a,b)*nc+np.einsum('ijk,ijk->ij',b,c)*na+np.einsum('ijk,ijk->ij',c,a)*nb
        out.extend(np.sum(2*np.arctan2(det,den),axis=1)/(4*np.pi))
    return np.array(out)

def component_analysis():
    records=[]
    for k in sorted(set(L)):
        fs=T[L[T[:,0]]==k];es=defaultdict(list)
        for i,t in enumerate(fs):
            for a,b in zip(t,np.roll(t,-1)):es[tuple(sorted((int(a),int(b))))].append(i)
        parent=list(range(len(fs)))
        def find(a):
            while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
            return a
        for ids in es.values():
            if len(ids)==2:parent[find(ids[0])]=find(ids[1])
        islands=Counter(find(i) for i in range(len(fs)))
        records.append(dict(id=int(k),boundary_edges=sum(len(v)==1 for v in es.values()),overconnected_edges=sum(len(v)>2 for v in es.values()),
            manifold_edge_face_islands=sorted(islands.values(),reverse=True),unique_positions=len(np.unique(V[L==k],axis=0))))
    inner_points=np.concatenate([V[L==5],V[T[L[T[:,0]]==5]].mean(axis=1)])
    w=winding(inner_points,T[L[T[:,0]]==2])
    return dict(components=records,tail_inner_in_outer_winding=dict(samples=len(w),min=float(w.min()),max=float(w.max()),percentiles=np.percentile(w,[0,1,50,99,100]).tolist()),
        tail_body_shared_vertices=0,tail_component_ids=[2,5],body_component_id=0,
        note='Raw vertex-index connectivity; face islands split only across non-2-face edges. Winding is diagnostic because outer tail is nonmanifold.')

def make_trial():
    raw=SOURCE.read_bytes();jn,jt=struct.unpack_from('<II',raw,12);j=json.loads(raw[20:20+jn]);bn,bt=struct.unpack_from('<II',raw,20+jn);blob=bytearray(raw[28+jn:28+jn+bn])
    accessor=j['accessors'][j['meshes'][0]['primitives'][0]['indices']]
    bv=j['bufferViews'][accessor['bufferView']];idx=np.frombuffer(blob,dtype='<u4',count=accessor['count'],offset=bv.get('byteOffset',0)+accessor.get('byteOffset',0)).reshape(-1,3).copy()
    # Blender importer retains the source vertex/index ordering (asserted here).
    assert np.array_equal(idx,T)
    keep=L[idx[:,0]]!=5;newidx=idx[keep].astype('<u4').tobytes()
    newbv=dict(buffer=0,byteOffset=len(blob),byteLength=len(newidx),target=34963);j['bufferViews'].append(newbv);blob.extend(newidx)
    accessor.update(bufferView=len(j['bufferViews'])-1,byteOffset=0,count=int(keep.sum()*3),min=[int(idx[keep].min())],max=[int(idx[keep].max())]);j['buffers'][0]['byteLength']=len(blob)
    jb=json.dumps(j,separators=(',',':')).encode();jb+=b' '*((-len(jb))%4);blob.extend(b'\0'*((-len(blob))%4))
    out=OUT/'trial-inner-tail-removed.glb';length=12+8+len(jb)+8+len(blob)
    out.write_bytes(struct.pack('<III',0x46546c67,2,length)+struct.pack('<II',len(jb),0x4e4f534a)+jb+struct.pack('<II',len(blob),0x004e4942)+blob)
    # Original binary payload preserved as prefix; new indices are the only active data change.
    return out,dict(removed_component=5,removed_triangles=int((~keep).sum()),remaining_triangles=int(keep.sum()),original_binary_prefix_unchanged=True,
        positions_normals_buffers_byte_exact=True,materials_json_unchanged=True,adoption='PENDING_RENDER_COMPARISON; quarantined diagnostic')

def consistency():
    f=np.load(OUT/'fbx-diagnostic-arrays.npz');fv,ft=f['vertices'],f['triangles']
    indexed=np.linalg.norm(fv-V,axis=1)
    # Quantize only for index-mapped face *comparison*, never source editing.
    fset=Counter(tuple(sorted(map(int,t))) for t in ft);gset=Counter(tuple(sorted(map(int,t))) for t in T)
    def sample_distance(points,verts,tris):
        tree=BVHTree.FromPolygons([Vector(p) for p in verts],tris.tolist(),all_triangles=True)
        return np.array([tree.find_nearest(Vector(p))[3] for p in points])
    fd=sample_distance(np.concatenate([fv,fv[ft].mean(axis=1)]),V,T)
    gd=sample_distance(np.concatenate([V,V[T].mean(axis=1)]),fv,ft)
    corner=[]
    for ext in ['fbx','glb']:
        o=u.load(ASSET/'source'/f'cute blue creature 3d model.{ext}')
        normals=np.array([tuple(o.matrix_world.to_3x3()@n.vector) for n in o.data.corner_normals])
        sums=np.zeros_like(V);cnt=np.zeros(len(V))
        for i,loop in enumerate(o.data.loops):sums[loop.vertex_index]+=normals[i];cnt[loop.vertex_index]+=1
        sums/=cnt[:,None];length=np.linalg.norm(sums,axis=1);sums/=np.maximum(length,1e-30)[:,None];corner.append(sums)
    valid=(np.linalg.norm(corner[0],axis=1)>.5)&(np.linalg.norm(corner[1],axis=1)>.5)
    angles=np.degrees(np.arccos(np.clip(np.sum(corner[0][valid]*corner[1][valid],axis=1),-1,1)))
    return dict(vertex_index_max_distance=float(indexed.max()),index_topology_triangles_only_in_fbx=sum((fset-gset).values()),index_topology_triangles_only_in_glb=sum((gset-fset).values()),
        sampled_bidirectional_surface_max_distance=float(max(fd.max(),gd.max())),samples_per_direction=[len(fd),len(gd)],
        vertex_mean_custom_normal_angle_deg_max=float(angles.max()) if len(angles) else None,vertex_mean_custom_normal_angle_deg_p99=float(np.percentile(angles,99)) if len(angles) else None,undefined_vertex_mean_normals=int(sum(~valid)),
        caveat='Vertex-mean normals do not prove all split-corner normals. FBX ngons are retessellated by Blender. Cross-format differences are reported; do not replace either original.')

def setup(o):
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=False;s.cycles.seed=0
    s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=-.3;s.view_settings.gamma=1
    s.world=bpy.data.worlds.new('Audit world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.22,.22,1)
    s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25
    for name,loc,power,size in [('key',(2,-3,4),160,4),('fill',(-3,-1,2),70,3),('rim',(0,3,3),120,3)]:
        ld=bpy.data.lights.new(name,'AREA');lo=bpy.data.objects.new(name,ld);s.collection.objects.link(lo);lo.location=loc;ld.energy=power;ld.shape='DISK';ld.size=size;lo.rotation_euler=(Vector((0,0,.5))-lo.location).to_track_quat('-Z','Y').to_euler()
    cam=bpy.data.objects.new('Audit camera',bpy.data.cameras.new('Audit camera'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.19
    return cam

VIEWS={'front':(0,-1,.08),'front-left':(1,-1,.12),'left':(1,0,.04),'rear-left':(1,1,.12),'back':(0,1,.08),'right':(-1,0,.04),'front-right':(-1,-1,.12),'top':(0,-.01,1),'underside':(0,-.01,-1)}
def render(cam,path,view='front',target=(0,0,.50),scale=1.19):
    d=Vector(VIEWS.get(view,view)).normalized();cam.location=Vector(target)+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    bpy.context.scene.render.filepath=str(RENDERS/(path+'.png'));bpy.ops.render.render(write_still=True)

def surface_stats(v):
    base=V[T];new=v[T];base_edges=base[:,[1,2,0]]-base;new_edges=new[:,[1,2,0]]-new
    ratio=np.linalg.norm(new_edges,axis=-1)/np.linalg.norm(base_edges,axis=-1)
    cross=np.cross(new[:,1]-new[:,0],new[:,2]-new[:,0]);areas=np.linalg.norm(cross,axis=1)/2
    tree=BVHTree.FromPolygons([Vector(p) for p in v],T.tolist(),all_triangles=True)
    pairs=[(a,b) for a,b in tree.overlap(tree) if a<b and set(T[a]).isdisjoint(T[b])]
    by=Counter(tuple(sorted((int(L[T[a,0]]),int(L[T[b,0]])))) for a,b in pairs)
    return dict(edge_ratio_min=float(ratio.min()),edge_ratio_max=float(ratio.max()),edge_ratio_p01_p99=np.percentile(ratio,[1,99]).tolist(),
        degenerate_triangles=int(sum(areas<1e-12)),disjoint_intersection_pairs=len(pairs),body_self_intersections=by.get((0,0),0),tail_body_intersections=by.get((0,2),0)+by.get((0,5),0),
        floor_penetration_below_minus_1e_6=int(sum(v[:,2]<-1e-6)),lowest_z=float(v[:,2].min()))

def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)

def deform(kind,strength):
    v=V.copy()
    if kind=='tail':
        mask=np.isin(L,[2,5])&(V[:,1]>.015);p=v[mask];y=p[:,1]-.015;theta=math.radians(20)*strength;k=theta/.415
        if abs(k)>1e-10:
            ang=k*y;c,s=np.cos(ang),np.sin(ang);x=p[:,0].copy();p[:,0]=(1-c)/k+c*x;p[:,1]=.015+s/k-s*x
        v[mask]=p
    elif kind in ['paw-L','paw-R','paws-both']:
        for side in ([1] if kind=='paw-L' else [-1] if kind=='paw-R' else [1,-1]):
            # In this front=-Y, up=+Z coordinate system, anatomical L=+X.
            mask=(L==0)&(side*V[:,0]>.17)&(V[:,2]>.16)&(V[:,2]<.52)
            p=V[mask];pivot=np.array([side*.19,-.12,.45]);q=p-pivot
            w=smooth(.17,.245,side*p[:,0])*smooth(.16,.28,p[:,2])*(1-smooth(.43,.52,p[:,2]));ang=math.radians(-30)*strength*w
            c,s=np.cos(ang),np.sin(ang);z=q[:,2].copy();y=q[:,1].copy();q[:,1]=c*y-s*z;q[:,2]=s*y+c*z;v[mask]=q+pivot
    elif kind=='low-rest':
        # Foot-locked crouch screening, NOT an approved rest pose or rig solution.
        w=smooth(.10,.48,V[:,2]);v[:,2]-=.14*strength*w
        v[:,1]-=.055*strength*smooth(.25,.65,V[:,2])
        # Tail remains a follower, not a support column. No ground translation.
    return v

def proof():
    o=u.load(SOURCE);cam=setup(o);bpy.context.preferences.filepaths.save_version=0
    o.name='DIAGNOSTIC_ONLY_Pino_C';basis=o.shape_key_add(name='Basis')
    measurements={};basefeet=(L==0)&(V[:,2]<.045)
    for kind,values in [('tail',np.linspace(-1,1,21)),('paw-L',np.linspace(0,1,11)),('paw-R',np.linspace(0,1,11)),('paws-both',np.linspace(0,1,11)),('low-rest',np.linspace(0,1,15))]:
        rows=[]
        for f in values:
            v=deform(kind,float(f));r=surface_stats(v);r.update(strength=float(f),locked_foot_vertex_max_displacement=float(np.linalg.norm(v[basefeet]-V[basefeet],axis=1).max()));rows.append(r)
        measurements[kind]=rows
        for name,f in [('end',-1 if kind=='tail' else 1)]+([('opposite',1)] if kind=='tail' else []):
            key=o.shape_key_add(name=f'{kind}-{name}');v=deform(kind,f)
            for i,p in enumerate(v):key.data[i].co=p
            key.value=1
            render(cam,f'probe-{kind}-{name}-front','front')
            render(cam,f'probe-{kind}-{name}-side','left')
            key.value=0
    # A reversible diagnostic sequence uses shape-key endpoints on a copy only.
    scene=bpy.context.scene;scene.frame_end=240
    for i,key in enumerate(list(o.data.shape_keys.key_blocks)[1:]):
        for frame,value in [(1,0),(20+i*35,0),(35+i*35,1),(50+i*35,0),(240,0)]:key.value=value;key.keyframe_insert('value',frame=frame)
    scene.frame_set(1);scene['purpose']='DIAGNOSTIC ONLY: synthetic bounded deformations; no production rig or final pose approval'
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'pino-c-diagnostic-proof.blend'))
    measurements['neutral_return_exact']=all(np.array_equal(deform(k,0),V) for k in ['tail','paw-L','paw-R','paws-both','low-rest'])
    measurements['scope']='69 sampled synthetic deformations on a duplicate; no rig, approved angular range, or final Motion PASS'
    write_json(OUT/'deformation-probes.json',measurements)

def support():
    mask=(L==0)&(V[:,2]<=.001);points=V[mask];idx=convex_hull_2d([Vector((p[0],p[1])) for p in points]);hull=points[idx,:2]
    feet={}
    for side,name in [(1,'anatomical-L'),(-1,'anatomical-R')]:
        pts=V[(L==0)&(side*V[:,0]>0)&(V[:,2]<.045)]
        feet[name]=dict(vertices=len(pts),min_z=float(pts[:,2].min()),bounds=[pts.min(axis=0).tolist(),pts.max(axis=0).tolist()])
    return dict(floor_z=0,tolerance=.001,contact_vertices=len(points),contact_hull_xy=hull.tolist(),feet=feet,tail_min_z=float(V[np.isin(L,[2,5]),2].min()),
        center_of_mass='UNKNOWN: overlapping/nonmanifold shells and unknown density; vertex centroid is not COM',dynamic_support='UNKNOWN; footprint and foot locks only')

def main():
    write_json(OUT/'component-analysis.json',component_analysis());write_json(OUT/'fbx-glb-consistency.json',consistency());write_json(OUT/'support.json',support())
    trial,meta=make_trial();write_json(OUT/'trial.json',meta)
    for tag,path in [('source',SOURCE),('retained',ASSET/'delivery/pino-c-retained.glb'),('trial',trial)]:
        o=u.load(path);cam=setup(o)
        for view in VIEWS:render(cam,f'{tag}-{view}',view)
        if tag=='source':
            render(cam,'detail-eyes','front',(0,-.28,.65),.40)
            render(cam,'detail-paws-belly','front',(0,-.15,.30),.77)
            render(cam,'detail-tail-root','rear-left',(0,.10,.27),.62)
            bpy.context.preferences.filepaths.save_version=0;bpy.context.scene['status']='UNCHANGED C SOURCE / HUMAN GEOMETRY GATE / TRIPO HOLD'
            bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'pino-c-unchanged-review.blend'))
    proof()
    write_json(OUT/'run.json',dict(blender=bpy.app.version_string,source_sha256=sha(SOURCE),script_sha256=sha(Path(__file__)),render=dict(engine='Cycles CPU',samples=32,denoise=False,seed=0,resolution=[640,640],color='Standard exposure -0.3',views=VIEWS),
        source_files_modified=False,delivery_mesh_edits=False,trial='quarantined; decision depends on pixel comparison'))

if __name__=='__main__':main()
