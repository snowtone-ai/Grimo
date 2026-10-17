"""Local integrated-mouth development; immutable v005 source, separate v006 outputs."""
import ast,json,sys,math
from pathlib import Path
from collections import Counter,defaultdict
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'docs/production/jill/mouth-integration-v006'
A=ROOT/'assets/grimo/production/jill/tripo/mouth-integration-v006'
E.mkdir(exist_ok=True);A.mkdir(exist_ok=True);(E/'renders').mkdir(exist_ok=True)
tree=ast.parse((ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8'))
ns={'__file__':str(ROOT/'scripts/blender/jill-texture-review-v005.py')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and not any(isinstance(t,ast.Name) and t.id=='cmd' for t in n.targets)],type_ignores=[]),'<helpers>','exec'),ns)
ns['E']=E
o,r=ns['openfile'](ROOT/'assets/grimo/production/jill/tripo/texture-return-v005/jill-textured-rig-v005.blend')
m=o.data;v=np.array([x.co[:] for x in m.vertices]);regions=np.load(ROOT/'docs/production/jill/rig-pretexture-v002/surface-contract.npz')['regions']
def write(name,data):(E/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
cmd=sys.argv[sys.argv.index('--')+1]
if cmd=='patch':
    import bmesh
    source_bvh=BVHTree.FromPolygons([Vector(p) for p in v],[list(p.vertices) for p in m.polygons if regions[p.index]=='original' and m.materials[p.material_index].get('paint_owner')=='body_skin'],all_triangles=False)
    probe=json.loads((E/'cut-probe.json').read_text());boundary=probe['loops'][0];N=len(boundary)
    profile=np.array(json.loads((E/'w-profile.json').read_text()))
    coef=np.array(json.loads((ROOT/'docs/production/jill/mouth-profile-v004/host-fit.json').read_text())['coefficients'])
    def surf(x,z):
        X=x/.07;Z=(z-.605)/.045
        return np.array([1,Z,Z*Z,Z**3,X*X,X*X*Z,X*X*Z*Z,X**4])@coef
    # Exclude the legacy fang discontinuities from the lip profile.
    clean=profile[(abs(profile[:,0])<.027)|(abs(profile[:,0])>.039)].copy()
    symmetric=[]
    for x in np.linspace(0,.044,89):
        symmetric.append([x,(np.interp(x,clean[:,0],clean[:,1])+np.interp(-x,clean[:,0],clean[:,1]))/2,(np.interp(x,clean[:,0],clean[:,2])+np.interp(-x,clean[:,0],clean[:,2]))/2])
    symmetric=np.array(symmetric)
    for column in [1,2]:symmetric[:,column]=np.convolve(np.pad(symmetric[:,column],(3,3),mode='edge'),np.ones(7)/7,mode='valid')
    def wp(x):return np.array([x,np.interp(abs(x),symmetric[:,0],symmetric[:,1]),np.interp(abs(x),symmetric[:,0],symmetric[:,2])])
    before={k.name:np.array([x.co[:] for x in k.data]) for k in m.shape_keys.key_blocks}
    before['FACE_MouthClose'][:28050]=v[:28050];before['FACE_MouthOpen'][:28050]=v[:28050]
    templates={}
    for reg in ['mouth-skin','mouth-inner']:
        templates[reg]=[{'uv':[[tuple(m.uv_layers[layer].data[li].uv) for li in p.loop_indices] for layer in range(3)],'mi':p.material_index,'n':len(p.vertices)} for p in m.polygons if regions[p.index]==reg]
    teeth=sorted({i for p in m.polygons if regions[p.index]=='teeth' for i in p.vertices})
    for key,q in before.items():
        for i in teeth:
            x,y,z=v[i];point=wp(.025 if x>0 else -.025)
            q[i]=v[i]+np.array([0,point[1]-v[i,1]+.002,point[2]-.623-.001])
            if key=='FACE_MouthClose':q[i,1]+=.03;q[i,2]=point[2]-.004
    for key in m.shape_keys.key_blocks:key.data.foreach_set('co',before[key.name].astype(np.float32).ravel())
    m.vertices.foreach_set('co',before['Basis'].astype(np.float32).ravel());m.update()
    bm=bmesh.new();bm.from_mesh(m);bm.faces.ensure_lookup_table();bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.index in set(probe['removed']) or regions[f.index] in ['mouth-skin','mouth-inner']],context='FACES_ONLY')
    layers={key:bm.verts.layers.shape.get(key) for key in before};uvlayers=list(bm.loops.layers.uv.values())
    area=sum(v[boundary[i],0]*v[boundary[(i+1)%N],2]-v[boundary[i],2]*v[boundary[(i+1)%N],0] for i in range(N))
    if area<0:boundary=list(reversed(boundary))
    verts=[bm.verts[i] for i in boundary];params=[]
    raw=np.unwrap([math.atan2((v[i,2]-.590)/.065,v[i,0]/.075) for i in boundary])
    # Isotonic angular correspondence prevents a source-notch from folding a lip row.
    blocks=[]
    for a in raw:
        blocks.append([float(a),1])
        while len(blocks)>1 and blocks[-2][0]>blocks[-1][0]:
            b,n=blocks.pop();a,k=blocks.pop();blocks.append([(a*k+b*n)/(k+n),k+n])
    angles=np.concatenate([np.full(n,a) for a,n in blocks]);angles+=np.arange(N)*.001
    angles=angles[0]+(angles-angles[0])*2*math.pi/(angles[-1]-angles[0]+2*math.pi/N)
    write('parameters.json',{'boundary':boundary,'raw':raw.tolist(),'angles':angles.tolist()})
    source_angles=np.mod(angles,2*math.pi);order=np.argsort(source_angles)
    source_angles=source_angles[order];boundary=[boundary[i] for i in order];verts=[verts[i] for i in order]
    sample_angles=np.linspace(0,2*math.pi,64,endpoint=False)
    for angle in sample_angles:
        U=math.cos(angle);upper=math.sin(angle)>=0
        params.append((U,upper))
    def lip(U,upper,key):
        x=.044*U;top=wp(x);lower=.575+.047*abs(U)**1.8+(wp(.044)[2]-.622)*abs(U)**3
        z=top[2]+.0002 if upper else lower
        if key=='FACE_MouthClose':z=top[2]+(.00015 if upper else -.00015)
        if key=='FACE_MouthOpen' and not upper:z-=.013*(1-U*U)
        if key in ['FACE_Smile.L','FACE_Smile.R'] and not upper:z+=.004*max(U*(1 if key.endswith('.L') else -1),0)**2*(1-U*U)
        y=top[1]+.0003 if upper or key=='FACE_MouthClose' else surf(x,z)-.0004
        if not upper and key!='FACE_MouthClose':y=y*(1-abs(U)**8)+(top[1]+.0003)*abs(U)**8
        return np.array([x,y,z])
    def newvert(pos):
        vt=bm.verts.new(pos['Basis'])
        for key,layer in layers.items():vt[layer]=pos[key]
        return vt
    pools={}
    for reg,items in templates.items():pools[reg,4]=[t for t in items if t['n']==4];pools[reg,3]=[t for t in items if t['n']==3]
    skin_triangles=[]
    for item in pools['mouth-skin',4][:150]:
        for indices in [(0,1,2),(0,2,3)]:skin_triangles.append({'mi':item['mi'],'uv':[[coords[i] for i in indices] for coords in item['uv']]})
    pools['mouth-skin',3]=skin_triangles;pools['mouth-skin',4]=pools['mouth-skin',4][150:]
    counters={(reg,n):0 for reg,n in pools}
    def face(vs,reg):
        choices=pools[reg,len(vs)];idx=counters[reg,len(vs)];assert idx<len(choices),(reg,idx,len(choices));template=choices[idx];counters[reg,len(vs)]+=1
        f=bm.faces.new(vs);f.material_index=template['mi'];f.smooth=True
        for j,l in enumerate(f.loops):
            for layer,values in zip(uvlayers,template['uv']):l[layer].uv=values[j]
    def outer(key,angle):
        positions=before[key][boundary];aa=np.r_[source_angles[-1]-2*math.pi,source_angles,source_angles[0]+2*math.pi];pp=np.vstack([positions[-1],positions,positions[0]])
        return np.array([np.interp(angle,aa,pp[:,axis]) for axis in range(3)])
    grid=[];nr=10
    for ring in range(nr):
        t=.35+.65*ring/(nr-1);row=[]
        for angle,(U,upper) in zip(sample_angles,params):
            pos={}
            for key,q in before.items():
                rest_lip=lip(U,upper,'Basis');polar=math.atan2((rest_lip[2]-.590)/.065,rest_lip[0]/.075)%(2*math.pi)
                start=outer(key,polar);inner=lip(U,upper,key);p=(1-t)*start+t*inner
                p[1]=surf(p[0],p[2])+(1-t)**3*(start[1]-surf(start[0],start[2]))+t**3*(inner[1]-surf(inner[0],inner[2]))
                if upper:
                    hit,_,_,_=source_bvh.ray_cast(Vector((float(p[0]),-1,float(p[2]))),Vector((0,1,0)),1.5)
                    if hit is not None:
                        edge=wp(p[0]);blend=math.exp(-((p[2]-edge[2])**2+max(abs(p[0])-.044,0)**2)/.003**2)
                        target=hit.y*(1-blend)+edge[1]*blend
                        # Exact shared border, sampled approved muzzle surface inward.
                        sampled=target+(start[1]-(source_bvh.ray_cast(Vector((float(start[0]),-1,float(start[2]))),Vector((0,1,0)),1.5)[0].y))*(1-t)**3
                        field_weight=math.sin(angle)**2
                        p[1]=p[1]*(1-field_weight)+sampled*field_weight
                pos[key]=p
            row.append(newvert(pos))
        grid.append(row)
    # Constrained triangulation avoids folds at concave source-border notches.
    from mathutils.geometry import delaunay_2d_cdt
    M=64;inputs=verts+grid[0];coords=[Vector((a.co.x,a.co.z)) for a in inputs]
    constraints=[(i,(i+1)%N) for i in range(N)]+[(N+i,N+(i+1)%M) for i in range(M)]
    cv,ce,cf,orig,_,_=delaunay_2d_cdt(coords,constraints,[],0,1e-8)
    mapped=[]
    for p,ids in zip(cv,orig):
        if ids:mapped.append(inputs[ids[0]]);continue
        best=None
        for a,b in constraints:
            d=coords[b]-coords[a];t=max(0,min(1,(p-coords[a]).dot(d)/d.length_squared));distance=(p-(coords[a]+d*t)).length
            if best is None or distance<best[0]:best=(distance,a,b,t)
        distance,a,b,t=best;assert distance<2e-6,('CDT interpolation',distance)
        mapped.append(newvert({key:(1-t)*np.array(inputs[a][layer])+t*np.array(inputs[b][layer]) for key,layer in layers.items()}))
    def inside(p,polygon):
        x,y=p;result=False
        for a,b in zip(polygon,polygon[1:]+polygon[:1]):
            if (a.y>y)!=(b.y>y) and x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x:result=not result
        return result
    count=0
    for ids in cf:
        center2=sum((cv[i] for i in ids),Vector((0,0)))/len(ids)
        if inside(center2,coords[:N]) and not inside(center2,coords[N:]):
            face([mapped[i] for i in ids],'mouth-skin');count+=1
    write('border-triangulation.json',{'input':len(inputs),'output':len(cv),'triangles':count,'new_intersections':sum(not ids for ids in orig)})
    N=M
    for j in range(nr-1):
        for i in range(N):
            k=(i+1)%N;face([grid[j][i],grid[j][k],grid[j+1][k],grid[j+1][i]],'mouth-skin')
    rim=grid[-1];bowl=[rim];oralnr=5
    for j in range(1,oralnr+1):
        t=j/(oralnr+1);row=[]
        for U,upper in params:
            pos={}
            for key in before:
                center=np.array([0,-.345,.607 if key!='FACE_MouthClose' else .628]);pos[key]=(1-t)*lip(U,upper,key)+t*center;pos[key][1]+=.009*math.sin(math.pi*t)
            row.append(newvert(pos))
        bowl.append(row)
    center=newvert({key:np.array([0,-.345,.628 if key=='FACE_MouthClose' else .607]) for key in before})
    for j in range(oralnr):
        for i in range(N):
            k=(i+1)%N;face([bowl[j][i],bowl[j][k],bowl[j+1][k],bowl[j+1][i]],'mouth-inner')
    # Fan triangles receive unique original oral UV triangles.
    triangles=[]
    for template in [t for t in templates['mouth-inner'] if t['n']==3]:
        for half in [0,1]:
            values=[]
            for coords in template['uv']:
                a,b,c=map(np.array,coords);mid=(a+b)/2
                values.append([a.tolist(),mid.tolist(),c.tolist()] if half==0 else [mid.tolist(),b.tolist(),c.tolist()])
            triangles.append({'mi':template['mi'],'uv':values})
    for i in range(N):
        k=(i+1)%N;temp=triangles[i];f=bm.faces.new([bowl[-1][i],bowl[-1][k],center]);f.material_index=temp['mi'];f.smooth=True
        for j,l in enumerate(f.loops):
            for layer,values in zip(uvlayers,temp['uv']):l[layer].uv=values[j]
    bm.verts.ensure_lookup_table()
    for loop in probe['loops'][1:]:
        # These old tooth remnants lie behind the retained W; cap them in oral material.
        f=bm.faces.new([bm.verts[i] for i in reversed(loop)]);f.material_index=templates['mouth-inner'][0]['mi']
        for l in f.loops:
            for layer in uvlayers:l[layer].uv=templates['mouth-inner'][0]['uv'][0][0]
    bm.normal_update();bm.to_mesh(m);bm.free();m.update()
    o.vertex_groups['DEF_head'].add(list(range(len(v),len(m.vertices))),1.,'REPLACE')
    for key in m.shape_keys.key_blocks:
        actual=np.array([x.co[:] for x in key.data]);assert np.max(abs(actual[:len(v)]-before[key.name]))<1e-6,key.name
    for state in ['neutral','mouth-closed','mouth-small','mouth-large','combined']:
        ns['pose'](r,ns['STATES'][state])
        for view in ['front','side','3q']:ns['render']('patch-'+state,view,True)
    ns['pose'](r,{});bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(A/'jill-mouth-integrated-patch-v006.blend'))
    write('patch-trial.json',{'removed_original_faces':probe['removed'],'shared_boundary':boundary,'new_vertices':len(m.vertices)-len(v),'templates_used':{str(k):v for k,v in counters.items()},'status':'DEVELOPMENT / NOT APPROVED'})
if cmd=='cutprobe':
    import bmesh
    edge=np.array(json.loads((E/'w-profile.json').read_text()))
    def wz(x):return float(np.interp(x,edge[:,0],edge[:,2]))
    removed=[]
    for p in m.polygons:
        if regions[p.index]!='original' or m.materials[p.material_index].get('paint_owner')!='body_skin':continue
        x,y,z=np.mean(v[list(p.vertices)],axis=0)
        rho=(x/.075)**2+((z-.604)/.065)**2
        top=.6525
        oldfang=.028<abs(x)<.039 and .620<z<.640 and -.44<y<-.38
        if rho<1 and z<top and -.44<y<-.30 or oldfang:removed.append(p.index)
    sourcefaces=[p for p in m.polygons if regions[p.index]=='original' and m.materials[p.material_index].get('paint_owner')=='body_skin']
    removed=set(removed)
    for _ in range(8):
        kept=[p for p in sourcefaces if p.index not in removed]
        ec=Counter(tuple(sorted((a,b))) for p in kept for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]]))
        bc=Counter(i for e,n in ec.items() if n==1 for i in e)
        bad={i for i,n in bc.items() if n>2 and abs(v[i,0])<.09 and .53<v[i,2]<.65 and v[i,1]<-.30}
        if not bad:break
        removed.update(p.index for p in kept if set(p.vertices)&bad)
    removed=sorted(removed)
    faces=[list(p.vertices) for p in m.polygons if regions[p.index]=='original' and m.materials[p.material_index].get('paint_owner')=='body_skin' and p.index not in set(removed)]
    count=Counter(tuple(sorted((a,b))) for f in faces for a,b in zip(f,f[1:]+f[:1]))
    boundary=[e for e,n in count.items() if n==1 and all(abs(v[i,0])<.11 and .50<v[i,2]<.68 and v[i,1]<-.25 for i in e)]
    adj=defaultdict(list)
    for a,b in boundary:adj[a].append(b);adj[b].append(a)
    assert all(len(j)==2 for j in adj.values()),{i:len(j) for i,j in adj.items() if len(j)!=2}
    loops=[];todo=set(adj)
    while todo:
        start=min(todo);loop=[start];prev=None;now=start
        while True:
            todo.discard(now);nxt=[j for j in adj[now] if j!=prev]
            if not nxt or nxt[0]==start:break
            prev,now=now,nxt[0]
            if now in loop:break
            loop.append(now)
        loops.append(loop)
    write('cut-probe.json',{'removed':removed,'boundary':boundary,'loops':loops,'degrees':{str(i):len(j) for i,j in adj.items()},'points':{str(i):v[i].tolist() for i in adj}})
    bm=bmesh.new();bm.from_mesh(m);bm.faces.ensure_lookup_table()
    cut=[f for f in bm.faces if f.index in set(removed) or regions[f.index] in ['mouth-skin','mouth-inner','tongue','teeth']]
    bmesh.ops.delete(bm,geom=cut,context='FACES_ONLY');bm.to_mesh(m);bm.free()
    bpy.context.scene.display.shading.color_type='TEXTURE'
    for view in ['front','side','3q']:ns['render']('cut-probe',view,True)
    print('CUT',len(removed),'loops',[len(x) for x in loops],flush=True)
if cmd=='inspect':
    m.calc_loop_triangles()
    ids=[p.index for p in m.polygons if regions[p.index]=='original' and m.materials[p.material_index].get('paint_owner')=='body_skin']
    faces=[list(m.polygons[i].vertices) for i in ids]
    bvh=BVHTree.FromPolygons([Vector(p) for p in v],faces,all_triangles=False)
    edge=[]
    for x in np.linspace(-.055,.055,221):
        zs=np.linspace(.626,.649,461);ys=[]
        for z in zs:
            p,_,_,_=bvh.ray_cast(Vector((float(x),-1,float(z))),Vector((0,1,0)),1.5);ys.append(p.y if p else 0)
        dy=np.diff(ys);dy[np.array(ys[1:])>-.4]=0;j=int(np.argmin(dy))+1
        edge.append([float(x),ys[j],float(zs[j])])
    write('w-profile.json',edge)
    local=[i for i in ids if (lambda p: abs(p[0])<.075 and .55<p[2]<.66 and p[1]<-.33)(np.mean(v[list(m.polygons[i].vertices)],axis=0))]
    triangles=[t for t in m.loop_triangles if t.polygon_index in set(local)]
    np.savez_compressed(E/'local-source.npz',vertices=v,faces=np.array([list(t.vertices) for t in triangles]),face_ids=[t.polygon_index for t in triangles],normals=np.array([t.normal[:] for t in triangles]))
    edges=Counter(tuple(sorted((a,b))) for f in faces for a,b in zip(f,f[1:]+f[:1]));boundary=[list(e) for e,n in edges.items() if n==1 and all(abs(v[i,0])<.10 and .53<v[i,2]<.67 and v[i,1]<-.3 for i in e)]
    write('source-boundary.json',{'edges':boundary,'points':{str(i):v[i].tolist() for e in boundary for i in e},'local_faces':len(local)})
    print('LOCAL',len(local),'BOUNDARY',len(boundary),flush=True)
