"""Independent geometry audit and controlled neutral views, Blender background."""
import bpy, bmesh, numpy as np, json, struct, sys, math, itertools
from pathlib import Path
from collections import defaultdict, Counter
from mathutils import Vector, Matrix
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_ray_tri

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/candidate-b-8481'
SRC=ROOT/'assets/grimo/production/shushu/tripo/candidate-b-8481'
BLEND=ROOT/'assets/grimo/production/shushu/blender/shushu-candidate-b-feasibility.blend'
RENDERS=OUT/'renders'

def write(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def glb(p):
    data=p.read_bytes(); pos=12; doc=None; binary=None
    while pos<len(data):
        n,t=struct.unpack_from('<II',data,pos); pos+=8
        if t==0x4e4f534a: doc=json.loads(data[pos:pos+n])
        if t==0x004e4942: binary=data[pos:pos+n]
        pos+=n
    return doc,binary

def accessor(doc,binary,index):
    a=doc['accessors'][index]; v=doc['bufferViews'][a['bufferView']]
    dtype={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
    width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
    stride=v.get('byteStride',np.dtype(dtype).itemsize*width)
    return np.ndarray((a['count'],width),dtype=dtype,buffer=binary,
                      offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(stride,np.dtype(dtype).itemsize)).copy()

def coords(obj): return np.array([list(obj.matrix_world@v.co) for v in obj.data.vertices])

def intersection_pairs(vertices,triangles):
    """Strict transverse intersections. Shared-index neighbors and coplanar pairs excluded."""
    vec=[Vector(v) for v in vertices]; faces=[tuple(map(int,t)) for t in triangles]
    tree=BVHTree.FromPolygons(vec,faces,all_triangles=True,epsilon=0)
    hits=[]; candidates=tree.overlap(tree); seen=set()
    for a,b in candidates:
        if a>=b or (a,b) in seen: continue
        seen.add((a,b)); ia,ib=faces[a],faces[b]
        if set(ia)&set(ib): continue
        found=False
        for t,u in [(ia,ib),(ib,ia)]:
            for j in range(3):
                origin=vec[t[j]]; delta=vec[t[(j+1)%3]]-origin
                if delta.length<1e-10: continue
                hit=intersect_ray_tri(vec[u[0]],vec[u[1]],vec[u[2]],delta,origin,True)
                if hit is not None:
                    fraction=(hit-origin).dot(delta)/delta.length_squared
                    if 1e-6<fraction<1-1e-6:
                        found=True;break
            if found:break
        if found:hits.append((a,b))
    locations=np.array([(vertices[triangles[a]].mean(0)+vertices[triangles[b]].mean(0))/2 for a,b in hits])
    return {'strict_transverse_pairs':len(hits),'examples':hits[:12],
            'example_centers':locations[:12].tolist(),
            'method':'BVH candidates + strict interior edge/triangle segment crossing; shared vertices excluded; coplanar overlaps UNKNOWN'}

def mesh_audit(v,faces,self_intersections=True):
    edges=defaultdict(list); used=set(); p=list(range(len(faces)))
    def find(i):
        while p[i]!=i:p[i]=p[p[i]];i=p[i]
        return i
    def union(a,b):p[find(a)]=find(b)
    for i,f in enumerate(faces):
        used.update(f)
        for j in range(len(f)):
            a,b=int(f[j]),int(f[(j+1)%len(f)]);edges[tuple(sorted((a,b)))].append((i,a<b))
    for inc in edges.values():
        for x in inc[1:]:union(inc[0][0],x[0])
    components=defaultdict(list)
    for i in range(len(faces)):components[find(i)].append(i)
    groups=sorted(components.values(),key=len,reverse=True)
    boundary=[e for e,inc in edges.items() if len(inc)==1]
    bad=[e for e,inc in edges.items() if len(inc)>2]
    winding=[e for e,inc in edges.items() if len(inc)==2 and inc[0][1]==inc[1][1]]
    graph=defaultdict(set)
    for a,b in boundary:graph[a].add(b);graph[b].add(a)
    seen=set(); loops=chains=branches=0; boundary_groups=[]
    for start in graph:
        if start in seen:continue
        stack=[start]; group=[];seen.add(start)
        while stack:
            x=stack.pop();group.append(x)
            for y in graph[x]:
                if y not in seen:seen.add(y);stack.append(y)
        degrees=[len(graph[x]) for x in group]
        if all(d==2 for d in degrees):loops+=1
        elif max(degrees)<=2:chains+=1
        else:branches+=1
        boundary_groups.append({'vertices':len(group),'bounds':[v[group].min(0).tolist(),v[group].max(0).tolist()]})
    tris=np.array([f for f in faces if len(f)==3],dtype=int)
    # Fan triangulation only for area of quads, not an FBX/GLB correspondence assumption.
    alltris=np.array([(f[0],f[j],f[j+1]) for f in faces for j in range(1,len(f)-1)])
    points=v[alltris]; crosses=np.cross(points[:,1]-points[:,0],points[:,2]-points[:,0]);area=np.linalg.norm(crosses,axis=1)/2
    lengths=np.stack([np.linalg.norm(points[:,(i+1)%3]-points[:,i],axis=1) for i in range(3)],axis=1)
    aspect=lengths.max(1)**2/np.maximum(2*area,1e-20)
    dup_pos=len(v)-len(np.unique(v,axis=0)); keys=[tuple(sorted(map(int,f))) for f in faces]
    mid=lambda es:[{'edge':list(e),'center':v[list(e)].mean(0).tolist(),'length':float(np.linalg.norm(v[e[0]]-v[e[1]]))} for e in es]
    facecenters=np.array([v[list(f)].mean(0) for f in faces])
    faceareas=[]; offset=0
    for f in faces:faceareas.append(float(area[offset:offset+len(f)-2].sum()));offset+=len(f)-2
    fa=np.array(faceareas)
    vp=list(range(len(v)))
    def vfind(a):
        while vp[a]!=a:vp[a]=vp[vp[a]];a=vp[a]
        return a
    for f in faces:
        for i in f[1:]:vp[vfind(int(i))]=vfind(int(f[0]))
    vg=defaultdict(list)
    for i,f in enumerate(faces):vg[vfind(int(f[0]))].append(i)
    vertex_groups=sorted(vg.values(),key=len,reverse=True)
    result={'vertices':len(v),'polygons':len(faces),'triangles':sum(len(f)-2 for f in faces),
            'polygon_sizes':dict(Counter(map(len,faces))),'edges':len(edges),
            'boundary_edges':len(boundary),'nonmanifold_gt2':len(bad),'inconsistent_winding_edges':len(winding),
            'boundary_graph':{'closed_loops':loops,'open_chains':chains,'branched':branches},
            'edge_connected_components':len(groups),'largest_component_faces':len(groups[0]),
            'vertex_connected_components':len(vertex_groups),'vertex_component_faces_top10':[len(g) for g in vertex_groups[:10]],
            'tiny_components_lt10':sum(len(g)<10 for g in groups),
            'tiny_component_area_fraction':float(sum(fa[g].sum() for g in groups if len(g)<10)/fa.sum()),
            'components_top10':[{'faces':len(g),'area':float(fa[g].sum()),'bounds':[facecenters[g].min(0).tolist(),facecenters[g].max(0).tolist()]} for g in groups[:10]],
            'degenerate_area_lt1e-12':int((area<1e-12).sum()),'duplicate_faces':len(keys)-len(set(keys)),
            'exact_duplicate_positions':dup_pos,'unused_vertices':len(v)-len(used),
            'bounds':[v.min(0).tolist(),v.max(0).tolist()],'area':float(area.sum()),
            'triangle_area_percentiles':dict(zip(['min','p01','p50','p99','max'],np.percentile(area,[0,1,50,99,100]).tolist())),
            'longest_edge_over_altitude_percentiles':dict(zip(['p50','p95','p99','max'],np.percentile(aspect,[50,95,99,100]).tolist())),
            'aspect_gt10':int((aspect>10).sum()),'nonmanifold_locations':mid(bad),
            'winding_locations':mid(winding),'largest_boundary_groups':sorted(boundary_groups,key=lambda g:g['vertices'],reverse=True)[:12],
            'height_bands':[{'band':[i/5,(i+1)/5],'faces':int(((facecenters[:,1]>=i/5)&(facecenters[:,1]<(i+1)/5)).sum()),
                            'area':float(fa[(facecenters[:,1]>=i/5)&(facecenters[:,1]<(i+1)/5)].sum())} for i in range(5)]}
    if self_intersections and len(tris)==len(faces):result['self_intersections']=intersection_pairs(v,tris)
    return result

def setup_render():
    s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=560;s.render.resolution_y=640;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.film_transparent=False
    s.display.shading.light='STUDIO';s.display.shading.studiolight_rotate_z=.4
    s.display.shading.color_type='SINGLE';s.display.shading.single_color=(.65,.68,.73)
    s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
    s.display.shading.background_type='WORLD';s.world.color=(.82,.84,.88)
    s.view_settings.view_transform='Standard'
    cam=bpy.data.objects.new('DiagnosticCamera',bpy.data.cameras.new('DiagnosticCamera'));s.collection.objects.link(cam);s.camera=cam
    cam.data.type='ORTHO';cam.data.ortho_scale=1.2
    return cam

def render(cam,name,direction,target=(0,0,.5),scale=1.2,wire=False):
    d=Vector(direction).normalized();cam.location=Vector(target)+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    bpy.context.scene.render.filepath=str(RENDERS/(name+'.png'));bpy.ops.render.render(write_still=True)

def main():
    RENDERS.mkdir(parents=True,exist_ok=True);BLEND.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    doc,binary=glb(SRC/'cute panda 3d model 8481.glb');primitive=doc['meshes'][0]['primitives'][0]
    v=accessor(doc,binary,primitive['attributes']['POSITION']).astype(float)
    faces=accessor(doc,binary,primitive['indices']).reshape(-1,3).astype(int)
    raw=mesh_audit(v,faces.tolist())
    normals=accessor(doc,binary,primitive['attributes']['NORMAL']).astype(float)
    tri=v[faces];face_normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);face_normals/=np.linalg.norm(face_normals,axis=1)[:,None]
    dots=(normals[faces].mean(1)*face_normals).sum(1)
    raw['exported_normal_alignment']={'normal_length_min_max':[float(np.linalg.norm(normals,axis=1).min()),float(np.linalg.norm(normals,axis=1).max())],
                                      'triangles_average_vertex_normal_opposes_face':int((dots<0).sum()),'mean_dot_percentiles':np.percentile(dots,[0,1,50,99,100]).tolist()}
    weld=[]
    for tolerance in [1e-7,1e-5,1e-4]:
        q=np.round(v/tolerance).astype(np.int64);_,first,inv=np.unique(q,axis=0,return_index=True,return_inverse=True)
        a=mesh_audit(v[first],inv[faces].tolist(),False)
        weld.append({'tolerance':tolerance,'method':'quantized-position bins; nearby pairs across bin edges may remain; bins may falsely merge nearby layers',
                     **{k:a[k] for k in ['vertices','boundary_edges','nonmanifold_gt2','edge_connected_components','degenerate_area_lt1e-12']}})
    bpy.ops.import_scene.fbx(filepath=str(SRC/'cute panda 3d model 8481.fbx'))
    fbx=[o for o in bpy.context.scene.objects if o.type=='MESH'][0];fv=np.array([list(x.co) for x in fbx.data.vertices])
    hierarchy=[{'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'matrix_world':[list(r) for r in o.matrix_world],
                'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale)} for o in bpy.context.scene.objects]
    ffaces=[list(p.vertices) for p in fbx.data.polygons]
    auditfbx=mesh_audit(fv,ffaces,False)
    world=coords(fbx);tree=KDTree(len(v))
    for i,p in enumerate(v):tree.insert(Vector(p),i)
    tree.balance();best=None
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([-1,1],repeat=3):
            trans=world[:,perm]*signs; scale=(v.max(0)-v.min(0)).max()/(trans.max(0)-trans.min(0)).max()
            trans*=scale;trans+=(v.min(0)+v.max(0)-trans.min(0)-trans.max(0))/2
            samples=trans[::20];err=max(tree.find(Vector(p))[2] for p in samples)
            if best is None or err<best[0]:best=(err,perm,signs,scale,trans)
    distances=[];mapping=[]
    for p in best[4]:_,index,d=tree.find(Vector(p));distances.append(d);mapping.append(index)
    source_poly_edges=set(tuple(sorted((mapping[f[i]],mapping[f[(i+1)%len(f)]]))) for f in ffaces for i in range(len(f)))
    glb_edges=set(tuple(sorted((int(f[i]),int(f[(i+1)%3])))) for f in faces for i in range(3))
    correspondence={'normalized_world_axis_permutation':best[1],'axis_signs':best[2],'scale':best[3],
                    'max_vertex_distance':max(distances),'rms_vertex_distance':float(np.sqrt(np.mean(np.array(distances)**2))),
                    'unique_nearest_vertex_mapping':len(set(mapping)),'all_fbx_polygon_edges_present_in_glb':source_poly_edges<=glb_edges,
                    'glb_additional_edges':len(glb_edges-source_poly_edges),'fbx_expected_triangles':sum(len(f)-2 for f in ffaces)}
    triset=set(tuple(sorted(map(int,t))) for t in faces);mismatches=[]
    for i,f in enumerate(ffaces):
        f=[mapping[x] for x in f]
        if len(f)==3:good=tuple(sorted(f)) in triset
        else:
            good=any(all(tuple(sorted(t)) in triset for t in pair) for pair in [
                [(f[0],f[1],f[2]),(f[0],f[2],f[3])],[(f[0],f[1],f[3]),(f[1],f[2],f[3])]])
        if not good:mismatches.append(i)
    correspondence['fbx_polygons_without_matching_glb_triangulation']=len(mismatches)
    # Normalize the copied FBX using the measured correspondence; keep source files untouched.
    fbx.matrix_world=Matrix.Identity(4)
    for vertex,p in zip(fbx.data.vertices,best[4]):vertex.co=(p[0],-p[2],p[1])
    fbx.data.update();fbx.name='CandidateB_RawFBX_Copy';fbx['role']='Unmodified topology diagnostic copy, coordinate normalized'
    cam=setup_render()
    views={'front':(0,-1,0),'left-facing':(1,0,0),'right-facing':(-1,0,0),'back':(0,1,0),'front-threequarter':(1,-1,.15),'rear-threequarter':(-1,1,.15),'top':(0,-.1,1),'underside':(0,-.1,-1)}
    for name,d in views.items():
        if '--measure-only' not in sys.argv:render(cam,'neutral-'+name,d)
    wire=fbx.modifiers.new('Diagnostic wire only','WIREFRAME');wire.thickness=.00065;wire.use_replace=False
    for name in ['front','left-facing','right-facing','back','front-threequarter']:
        if '--measure-only' not in sys.argv:render(cam,'wire-'+name,views[name])
    fbx.modifiers.remove(wire)
    report={'blender_version':bpy.app.version_string,'coordinates':'raw GLB x/right, y/up, z/front; Blender x/right, y/back, z/up',
            'glb_raw':raw,'fbx_local':auditfbx,'position_weld_probes':weld,'correspondence':correspondence,
            'fbx_original_hierarchy':hierarchy,
            'fbx_object':{'name':fbx.name,'uv_layers':len(fbx.data.uv_layers),'materials':len(fbx.data.materials),'shape_keys':bool(fbx.data.shape_keys)},
            'glb_structure':{'nodes':doc.get('nodes',[]),'mesh_count':len(doc['meshes']),'primitive_count':len(doc['meshes'][0]['primitives']),
                             'attributes':primitive['attributes'],'materials':doc.get('materials',[]),'images':doc.get('images',[]),
                             'textures':doc.get('textures',[]),'skins':doc.get('skins',[]),'animations':doc.get('animations',[]),'morph_targets':primitive.get('targets',[])}}
    write('independent-audit.json',report)
    if '--measure-only' not in sys.argv and '--refresh-views' not in sys.argv:bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    print('AUDIT_COMPLETE',json.dumps(correspondence))

if __name__=='__main__':main()
