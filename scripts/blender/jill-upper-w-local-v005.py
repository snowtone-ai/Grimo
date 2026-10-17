"""Scoped upper-mouth diagnosis and repair. Never modifies the v004 source."""
import bpy, json, ast, sys
from functools import lru_cache
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005'
E=ROOT/'docs/production/jill/texture-return-v005/upper-w-local'
(E/'renders').mkdir(parents=True,exist_ok=True)
tree=ast.parse((ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8'))
ns={'__file__':str(ROOT/'scripts/blender/jill-texture-review-v005.py')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and not any(isinstance(t,ast.Name) and t.id=='cmd' for t in n.targets)],type_ignores=[]),'<helpers>','exec'),ns)
def write(n,d):(E/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def repair(o):
    m=o.data;basis=np.array([v.co[:] for v in m.shape_keys.key_blocks['Basis'].data]);regions=np.load(ROOT/'docs/production/jill/rig-pretexture-v002/surface-contract.npz')['regions']
    rep=json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/repair-report.json').read_text());outer=next(x['boundary_vertices'] for x in rep['local_changes'] if x.get('graft')=='mouth')
    skin=set();adj={};inner=set()
    for p in m.polygons:
        reg=regions[p.index]
        if reg=='mouth-skin':
            skin.update(p.vertices)
            for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]]):adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
        elif reg=='mouth-inner':inner.update(p.vertices)
    rim=skin&inner;dist={i:0 for i in outer};todo=list(outer)
    while todo:
        new=[]
        for i in todo:
            for j in adj[i]:
                if j not in dist:dist[j]=dist[i]+1;new.append(j)
        todo=new
    bvh=BVHTree.FromPolygons([Vector(v) for v in basis],[list(p.vertices) for p in m.polygons if regions[p.index]=='original' and m.materials[p.material_index].get('paint_owner')=='body_skin'],all_triangles=False)
    # Locate the actual existing muzzle's lower W edge by its depth discontinuity.
    @lru_cache(None)
    def edge(x):
        zs=np.linspace(.628,.649,421);ys=[]
        for z in zs:
            p,_,_,_=bvh.ray_cast(Vector((float(x),-1,float(z))),Vector((0,1,0)),1.5);ys.append(p.y if p else 0.)
        jumps=np.diff(ys);jumps[np.array(ys[1:])>-.40]=0
        j=int(np.argmin(jumps))+1
        return np.array([x,ys[j]+.00045,zs[j]+.00035])
    # Row ordering is inherited from the authored 64-sample collar.
    ordered=sorted(rim);upper=set(ordered[:33]);targets={i:edge(basis[i,0]) for i in upper}
    legacy=[i for i,p in enumerate(basis) if i<28050 and abs(p[0])<.044 and .618<p[2]<edge(p[0])[2]-.0012 and p[1]<-.36]
    exterior=BVHTree.FromPolygons([Vector(v) for v in basis],[list(p.vertices) for p in m.polygons if regions[p.index]=='original' and m.materials[p.material_index].get('paint_owner')=='body_skin' and not set(p.vertices)&set(legacy)],all_triangles=False)
    # Corner target should remain below the host and join the unmodified lower lip.
    write('rim-targets.json',[{'id':i,'before':basis[i].tolist(),'target':p.tolist()} for i,p in targets.items()])
    before={k.name:np.array([v.co[:] for v in k.data]) for k in m.shape_keys.key_blocks}
    # Every collar row has one rim endpoint; identify via stable generated indexing.
    # Added collar vertices are contiguous per radial row (12 samples after outer).
    row_rim={i:i+(12-dist[i]) for i in skin if dist[i]>0}
    changed={}
    coef=np.array(json.loads((ROOT/'docs/production/jill/mouth-profile-v004/host-fit.json').read_text())['coefficients'])
    def surf(x,z):
        X=x/.07;Z=(z-.605)/.045
        return np.array([1,Z,Z*Z,Z**3,X*X,X*X*Z,X*X*Z*Z,X**4])@coef
    for key in m.shape_keys.key_blocks:
        q=before[key.name].copy();isclose=key.name=='FACE_MouthClose'
        for i in skin:
            if not dist[i]:
                if isclose:
                    p,_,_,_=exterior.ray_cast(Vector((float(q[i,0]),-1,float(q[i,2]))),Vector((0,1,0)),1.5)
                    if p is not None and p.y<-.385:q[i,1]=max(q[i,1],p.y+.002)
                continue
            ri=row_rim[i];t=dist[i]/12
            if ri in targets:
                dest=targets[ri].copy();dest[2]+=.00012 if isclose else 0
                # Keep semantic smile deltas relative to the unchanged W root.
                delta=dest-before[key.name][ri];q[i]+=delta*t
                # Bury the upper collar beneath the real host, not a second rim.
                # Use the smooth collar depth, avoiding folds from host recess rays.
            elif isclose:
                # Lower closing edge must meet the W, with no new rest-shape edit.
                dest=edge(basis[ri,0]);dest[2]-=.00012
                delta=dest-before[key.name][ri];q[i,2]+=delta[2]*t;q[i,1]+=delta[1]*t**3
            else:
                continue
            if ri in targets:
                q[i,1]=surf(q[i,0],q[i,2])+.0015*(1-t)**3-.0005*(1-(1-t)**3)
                dest=edge(basis[ri,0]);q[i,1]+=(dest[1]-(surf(dest[0],dest[2])-.0005))*t**3
            if isclose:
                p,_,_,_=exterior.ray_cast(Vector((float(q[i,0]),-1,float(q[i,2]))),Vector((0,1,0)),1.5)
                if p is not None and p.y<-.385:q[i,1]=max(q[i,1],p.y+.002)
        # Existing oral bowl follows the repaired rim, decaying toward its centre.
        # Eight rings were authored as convex combinations of each rim vertex.
        rim_order=sorted(rim)
        inner_only=sorted(inner-skin);assert len(inner_only)==513
        for j in range(8):
            t=(j+1)/9
            for col,ri in enumerate(rim_order):
                vi=inner_only[j*64+col]
                q[vi]+=(q[ri]-before[key.name][ri])*(1-t)
                if ri in upper or isclose:
                    center=before[key.name][inner_only[-1]]
                    q[vi,1]=(1-t)*q[ri,1]+t*center[1]+.006*np.sin(np.pi*t)
                if not isclose and q[vi,2]>.610:
                    w=np.clip((q[vi,2]-.610)/.010,0,1);w=w*w*(3-2*w)
                    q[vi,1]=q[vi,1]*(1-w)+(surf(q[vi,0],q[vi,2])-.002)*w
        # Existing short fangs follow the upper W instead of floating at old rim.
        teeth=sorted({i for p in m.polygons if regions[p.index]=='teeth' for i in p.vertices})
        for i in teeth:
            x,y,z=q[i];dest=edge(.025 if x>0 else -.025)
            if not isclose:q[i,2]+=dest[2]-.623;q[i,1]=surf(x,q[i,2])-.003+(y-before[key.name][i,1])
        key.data.foreach_set('co',q.astype(np.float32).ravel())
        ids=np.flatnonzero(np.linalg.norm(q-before[key.name],axis=1)>1e-8)
        changed[key.name]={'ids':ids.tolist(),'max_m':float(np.linalg.norm(q-before[key.name],axis=1).max()),'bounds_before':[before[key.name][ids].min(0).tolist(),before[key.name][ids].max(0).tolist()] if len(ids) else None}
    m.vertices.foreach_set('co',np.array([v.co[:] for v in m.shape_keys.key_blocks['Basis'].data],np.float32).ravel());m.update()
    write('geometry-delta.json',{'method':'Upper auxiliary collar/bowl follows existing W; close-key contacts W; original body vertices untouched. Original internal texels are masked separately, never recessed.','legacy_excluded_from_exterior_probe_ids':legacy,'keys':changed})
    return before
def render(label,view,close=True):
    s=bpy.context.scene;target=Vector((0,-.37,.625) if close else (0,-.24,.68))
    direction={'front':(0,-1,.02),'side':(1,0,.02),'3q':(1,-2,.06),'left3q':(-1,-2,.06)}[view]
    cam=s.camera;cam.location=target+Vector(direction).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.18 if close else .45
    s.render.engine='BLENDER_WORKBENCH';s.display.shading.show_cavity=False;s.display.shading.show_shadows=True;s.display.shading.light='STUDIO';s.display.shading.studiolight_rotate_z=.4
    s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(E/'renders'/f'{label}-{view}.png');bpy.ops.render.render(write_still=True)
def alpha_bind(o):
    img=bpy.data.images.load(str(BASE/'jill-basecolor-upper-w-local-v005.png'),check_existing=False)
    for mat in o.data.materials:
        if mat.get('paint_owner')!='body_skin':continue
        nt=mat.node_tree;tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE');tex.image=img
        cutoff=nt.nodes.new('ShaderNodeMath');cutoff.operation='GREATER_THAN';cutoff.inputs[1].default_value=.5;nt.links.new(tex.outputs['Alpha'],cutoff.inputs[0]);nt.links.new(cutoff.outputs[0],nt.nodes.get('Principled BSDF').inputs['Alpha']);mat.surface_render_method='DITHERED'
def pbr_setup():
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12
    s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[0].default_value=(.6,.65,.55,1);s.world.node_tree.nodes.get('Background').inputs[1].default_value=.8
    if not any(o.type=='LIGHT' for o in s.objects):
        for pos,power,size in [((-.8,-1.5,2),65,2),((1,-.5,1),20,2)]:
            data=bpy.data.lights.new('LocalReviewSoftbox','AREA');data.energy=power;data.shape='DISK';data.size=size;ob=bpy.data.objects.new(data.name,data);s.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector((0,-.3,.63))-ob.location).to_track_quat('-Z','Y').to_euler()
    s.view_settings.view_transform='Standard'
cmd=sys.argv[sys.argv.index('--')+1]
if cmd=='diagnose':
    o,r=ns['openfile'](BASE/'jill-textured-rig-v005.blend');m=o.data
    for label in ['texture','clay','owners']:
        bpy.context.scene.display.shading.color_type='TEXTURE' if label=='texture' else 'MATERIAL'
        for mat in m.materials:
            owner=mat.get('paint_owner');mat.diffuse_color=({'body_skin':(.15,.55,.85,1),'mouth-skin':(.95,.65,.12,1),'mouth-inner':(.25,.01,.025,1),'tongue':(.8,.12,.2,1),'teeth':(.9,.9,.9,1)}.get(owner,(.4,.6,.3,1)) if label=='owners' else (.65,.65,.65,1))
        for view in ['front','3q']:render('diagnosis-'+label,view)
    v=[x.co.copy() for x in m.vertices];m.calc_loop_triangles();tris=[list(t.vertices) for t in m.loop_triangles];bvh=BVHTree.FromPolygons(v,tris,all_triangles=True)
    rows=[]
    for x in [0,.01,.02,.03,.04,.05]:
        for z in np.arange(.617,.650,.001):
            p,n,i,d=bvh.ray_cast(Vector((x,-1,float(z))),Vector((0,1,0)),1.5)
            if p is not None:rows.append({'x':x,'z':float(z),'y':p.y,'polygon':m.loop_triangles[i].polygon_index,'owner':m.materials[m.polygons[m.loop_triangles[i].polygon_index].material_index].get('paint_owner')})
    write('diagnosis-rays.json',rows)
    write('scene.json',{'objects':[(x.name,x.type) for x in bpy.context.scene.objects],'owners':[(x.name,x.get('paint_owner')) for x in m.materials]})
if cmd=='profile':
    o,r=ns['openfile'](BASE/'jill-textured-rig-v005.blend');m=o.data
    v=[x.co.copy() for x in m.vertices]
    polys=[list(p.vertices) for p in m.polygons if m.materials[p.material_index].get('paint_owner')=='body_skin']
    bvh=BVHTree.FromPolygons(v,polys,all_triangles=False)
    profile=[]
    for x in np.linspace(-.055,.055,111):
        line=[]
        for z in np.linspace(.620,.648,281):
            p,n,i,d=bvh.ray_cast(Vector((float(x),-1,float(z))),Vector((0,1,0)),1.5)
            if p is not None:line.append([float(z),p.y])
        profile.append({'x':float(x),'line':line})
    write('host-profile.json',profile)
    # Diagnostic only: remove the overlying upper collar to see what is behind it.
    import bmesh
    bm=bmesh.new();bm.from_mesh(m);bm.faces.ensure_lookup_table()
    faces=[f for f in bm.faces if m.materials[f.material_index].get('paint_owner')=='mouth-skin' and f.calc_center_median().z>.6215]
    bmesh.ops.delete(bm,geom=faces,context='FACES');bm.to_mesh(m);bm.free()
    bpy.context.scene.display.shading.color_type='TEXTURE'
    for view in ['front','3q']:render('diagnosis-upper-collar-removed',view)
if cmd in ['trial','field']:
    o,r=ns['openfile'](BASE/'jill-textured-rig-v005.blend');repair(o)
    if cmd=='field':sys.exit(0)
    bpy.context.scene.display.shading.color_type='TEXTURE'
    for state in ['neutral','mouth-closed','mouth-small','mouth-large']:
        ns['pose'](r,ns['STATES'][state])
        for view in ['front','3q','side']:render('trial-'+state,view)
if cmd=='build':
    o,r=ns['openfile'](BASE/'jill-textured-rig-v005.blend');contract=ns['contract'](o,r);repair(o);alpha_bind(o)
    after=ns['contract'](o,r);diff=[k for k in contract if contract[k]!=after[k]];assert set(diff)=={'basis','keys'}
    write('preservation.json',{'pass':True,'allowed_differences':diff,'before':contract,'after':after,'counts':{'bones':130,'channels':39,'morphs':20,'anchors':16},'source_original_geometry_retained':True})
    o['upper_w_status']='LOCAL REPAIR CANDIDATE / Human HOLD / evaluate actual closed and transition renders'
    bpy.ops.file.pack_all();bpy.context.preferences.filepaths.save_version=0
    path=BASE/'jill-upper-w-local-v005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path));o,r=ns['openfile'](path);assert ns['contract'](o,r)==after
    bpy.ops.object.select_all(action='DESELECT')
    for ob in [o,r]+[a for a in bpy.context.scene.objects if a.name.startswith('ANCHOR_')]:ob.select_set(True)
    bpy.context.view_layer.objects.active=o
    bpy.ops.export_scene.gltf(filepath=str(BASE/'jill-upper-w-local-v005.glb'),export_format='GLB',use_selection=True,export_animations=False,export_skins=True,export_morph=True,export_extras=True,export_cameras=False,export_lights=False,export_def_bones=False,export_all_influences=False,export_influence_nb=4,export_image_format='AUTO')
    ns.update({'E':E,'BLEND':path,'OUT':BASE})
    # Reuse the existing bounded authoring snapshot/clip exporter with new output.
    block=next(n for n in tree.body if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and isinstance(n.test.comparators[0],ast.Constant) and n.test.comparators[0].value=='clip')
    source=ast.unparse(ast.Module(body=block.body,type_ignores=[])).replace('jill-textured-review-bounded-v005.glb','jill-upper-w-review-bounded-v005.glb')
    exec(compile(source,'<bounded clip>','exec'),ns)
if cmd=='pbr-test':
    o,r=ns['openfile'](BASE/'jill-upper-w-local-v005.blend');pbr_setup()
    for state in ['neutral','mouth-closed','mouth-small']:
        ns['pose'](r,ns['STATES'][state]);ns['E']=E
        # ns renderer selects Cycles when pbr=True, retaining shared framing.
        ns['render']('pbr-'+state,'3q',True,True)
if cmd=='review':
    for label,file in [('before','jill-textured-rig-v005.blend'),('after','jill-upper-w-local-v005.blend')]:
        o,r=ns['openfile'](BASE/file);bpy.context.scene.display.shading.color_type='TEXTURE'
        for state in ['neutral','mouth-closed','mouth-small','mouth-large','combined','recovery']:
            ns['pose'](r,ns['STATES'][state])
            for view in ['front','side','3q','left3q']:render(label+'-'+state,view,False)
        ns['pose'](r,{})
        for view in ['front','3q']:render(label+'-detail',view)
if cmd=='audit':
    saved={}
    for label,file in [('before','jill-textured-rig-v005.blend'),('after','jill-upper-w-local-v005.blend')]:
        o,r=ns['openfile'](BASE/file);saved[label]={k.name:np.array([v.co[:] for v in k.data]) for k in o.data.shape_keys.key_blocks}
    rows={k:{'original_28050_exact':bool(np.array_equal(saved['before'][k][:28050],saved['after'][k][:28050])),'changed_vertices':int(np.count_nonzero(np.linalg.norm(saved['before'][k]-saved['after'][k],axis=1)>1e-8))} for k in saved['before']}
    assert all(x['original_28050_exact'] for x in rows.values())
    write('original-body-preservation.json',{'pass':True,'keys':rows,'scope':'All original 28050 vertices exact in all 21 key blocks. Only auxiliary mouth vertices change.'})
