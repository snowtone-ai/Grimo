"""Bilateral local lid/skin join correction and conformal Blink; no topology/UV/rig changes."""
import ast,json,sys,hashlib,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets/grimo/production/jill/tripo/eye-join-v009'
E=ROOT/'docs/production/jill/eye-join-v009'
SOURCE=ROOT/'assets/grimo/production/jill/tripo/clover-v007/jill-textured-rig-v007.blend'
A.mkdir(exist_ok=True);E.mkdir(exist_ok=True)
tree=ast.parse((ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8').replace("'back3q':(1,2,.12)","'left3q':(-1,-2,.12),'back3q':(1,2,.12)"))
ns={'__file__':str(ROOT/'scripts/blender/jill-texture-review-v005.py')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and not any(isinstance(t,ast.Name) and t.id=='cmd' for t in n.targets)],type_ignores=[]),'<helpers>','exec'),ns)
ns['E']=E;cmd=sys.argv[sys.argv.index('--')+1];o,r=ns['openfile'](SOURCE);m=o.data
def write(name,d):(E/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
if cmd=='surface':
    m.calc_loop_triangles();v=np.array([p.co[:] for p in m.vertices]);xyz=[];uv=[]
    for t in m.loop_triangles:
        if m.materials[t.material_index].get('paint_owner')!='body_skin':continue
        p=v[list(t.vertices)]
        if p[:,2].max()<.595 or p[:,2].min()>.755 or p[:,1].min()>-.18 or p[:,0].min()>.205 or p[:,0].max()<-.205:continue
        xyz.append(p);uv.append([m.uv_layers[0].data[i].uv[:] for i in t.loops])
    np.savez_compressed(E/'host-surface.npz',xyz=xyz,uv=uv)
    write('host-surface.json',{'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'triangles':len(xyz),'owner':'body_skin','uv':'existing UV0, unchanged'})
if cmd=='build':
    before=ns['contract'](o,r);original=np.array([[p.co[:] for p in k.data] for k in m.shape_keys.key_blocks])
    v=np.array([p.co[:] for p in m.vertices]);comp=np.load(ROOT/'docs/production/jill/rig-other-v001/authority-parts.npz')['component']
    bvh=BVHTree.FromPolygons([Vector(p) for p in v],[list(p.vertices) for p in m.polygons if m.materials[p.material_index].get('paint_owner')=='body_skin'])
    def design(u,z):return np.array([np.ones_like(u),u,z,u*u,u*z,z*z]).T
    for side,ci,sgn in [('L',99,1),('R',98,-1)]:
     ids=sorted({i for p in m.polygons if m.materials[p.material_index].get('paint_owner')=='lids-'+side for i in p.vertices});eyeids=np.flatnonzero(comp==ci);eye=v[eyeids];c=eye.mean(0);n=np.array([sgn*.52,-.85,0]);n/=np.linalg.norm(n);tan=np.array([.85,sgn*.52,0]);tan/=np.linalg.norm(tan);q=np.c_[(v-c)@tan,v[:,2]-c[2],(v-c)@n];eu=q[eyeids];ru=max(abs(eu[:,0]));rz=max(abs(eu[:,1]));coef=np.linalg.lstsq(design(eu[:,0],eu[:,1]),eu[:,2],rcond=None)[0];res=max(eu[:,2]-design(eu[:,0],eu[:,1])@coef)+.0008;blink=m.shape_keys.key_blocks['FACE_Blink.'+side]
     for ix,oi in enumerate(ids[:64]):
      oq=q[oi].copy();oq[:2]*=1.4/1.18;wp=c+tan*oq[0]+[0,0,oq[1]];hit=bvh.ray_cast(Vector(wp+n),Vector(-n),2);assert hit[0] is not None;outer=np.array(hit[0])-n*.0008;oq[2]=(outer-c)@n;inner=q[ids[64+ix*14+13]].copy();inner[2]+=.0001;sq=inner.copy();theta=math.atan2(oq[1]/rz,oq[0]/ru);sq[0]=ru*math.cos(theta);sq[1]=.0045-.010*abs(sq[0]/ru)**1.7;outerres=oq[2]-float(design(oq[0],oq[1])@coef);innerres=inner[2]-float(design(inner[0],inner[1])@coef)
      for j in range(15):
       vi=oi if j==0 else ids[64+ix*14+j-1];t=j/14;p=(1-t)*oq+t*inner;closed=(1-t)*oq+t*sq;p[2]=float(design(p[0],p[1])@coef)+(1-t)**2*outerres+t*t*innerres;closed[2]=float(design(closed[0],closed[1])@coef)+(1-t)**2*outerres+t*t*res;new=c+tan*p[0]+[0,0,p[1]]+n*p[2];end=c+tan*closed[0]+[0,0,closed[1]]+n*closed[2];delta=new-v[vi]
       for k in m.shape_keys.key_blocks:k.data[vi].co=end if k==blink else np.array(k.data[vi].co)+delta
     for vi in eyeids:blink.data[vi].co=v[vi]
    m.vertices.foreach_set('co',np.array([p.co[:] for p in m.shape_keys.key_blocks['Basis'].data],dtype=np.float32).ravel());m.update()
    after=ns['contract'](o,r)
    for field in ['topology','owners','uv','weights','groups','bones','drivers','anchors','channels']:assert before[field]==after[field],field
    current=np.array([[p.co[:] for p in k.data] for k in m.shape_keys.key_blocks]);delta=current-original
    lids={i for p in m.polygons if m.materials[p.material_index].get('paint_owner') in ['lids-L','lids-R'] for i in p.vertices}
    allowed=set(lids);allowed.update(np.flatnonzero(np.isin(comp,[98,99])))
    changed=set(np.flatnonzero(np.max(abs(delta),axis=(0,2))>1e-7));assert changed<=allowed
    basechanged=set(np.flatnonzero(np.max(abs(delta[0]),axis=1)>1e-7));assert basechanged<=lids
    for ki,k in enumerate(m.shape_keys.key_blocks):
        if k.name in ['FACE_Blink.L','FACE_Blink.R']:continue
        assert np.max(abs((current[ki]-current[0])-(original[ki]-original[0])))<2e-7,k.name
    write('preservation.json',{'pass':True,'before':before,'after':after,'changed_basis_vertices':len(basechanged),'changed_any_key_vertices':len(changed),'allowed_lid_vertices':len(lids),'all_non_blink_morph_relative_deltas_exact_tolerance_m':2e-7,'scope':'Existing lid positions and Blink targets only; original eye Basis, all other geometry, topology, 3 UVs, weights, drivers, 130 bones, 39 channels, 20 Morphs and 16 anchors preserved.'})

    ns['bind'](o,A/'jill-basecolor-v009.png')
    o['texture_status']='v009 bilateral lid/skin join correction; mouth/clover Human GO; eye review pending'
    r['texture_review']='v009 local lid join and Blink correction; original eye Basis and approved features preserved'
    bpy.ops.file.pack_all();bpy.context.preferences.filepaths.save_version=0
    blend=A/'jill-textured-rig-v009.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));o,r=ns['openfile'](blend)
    assert after==ns['contract'](o,r),'Saved/reopened model drift'
    bpy.ops.object.select_all(action='DESELECT')
    for ob in [o,r]+[x for x in bpy.context.scene.objects if x.name.startswith('ANCHOR_')]:ob.select_set(True)
    bpy.context.view_layer.objects.active=r
    bpy.ops.export_scene.gltf(filepath=str(A/'jill-textured-rig-v009.glb'),export_format='GLB',use_selection=True,export_animations=False,export_skins=True,export_morph=True,export_extras=True,export_cameras=False,export_lights=False,export_def_bones=False,export_all_influences=False,export_influence_nb=4,export_image_format='AUTO')
    states={s:ns['STATES'][s] for s in ['neutral','mouth-closed','mouth-small','mouth-large','combined','recovery']}
    for b in [.25,.5,.75,1]:states['blink-'+str(b)]={'blink.L':b,'blink.R':b}
    states.update({'wink-L':{'blink.L':1},'wink-R':{'blink.R':1}})
    for axis in ['x','y']:
        for value in [-1,1]:states[f'gaze-{axis}-{value}']={f'gaze_{axis}.L':value,f'gaze_{axis}.R':value}
    write('saved-states.json',states)
    for s,values in states.items():
        ns['pose'](r,values)
        for view in ['front','side','3q','left3q']:ns['render'](s,view)
    ns['pose'](r,{})
    for view in ['front','side','left3q']:ns['render']('body',view,False)
if cmd=='before':
    for s,values in {'neutral':{},'blink-half':{'blink.L':.5,'blink.R':.5},'blink-full':{'blink.L':1,'blink.R':1}}.items():
        ns['pose'](r,values)
        for view in ['front','side','3q','left3q']:ns['render']('before-'+s,view)
if cmd=='clip':
    # Reuse the existing bounded motion schedule, baking the unchanged drivers.
    # This is a local QA clip, not full motion production.
    o,r=ns['openfile'](A/'jill-textured-rig-v009.blend');snapshots={}
    for state,values in ns['STATES'].items():
        ns['pose'](r,values);snapshots[state]={'channels':values,'morphs':{k.name:float(k.value) for k in o.data.shape_keys.key_blocks[1:]}}
    write('review-states.json',snapshots)
    ns['OUT']=A;ns['BLEND']=A/'jill-textured-rig-v009.blend'
    src=(ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8').replace('jill-textured-review-bounded-v005.glb','jill-review-bounded-v009.glb').replace('Jill_Texture_Review_Bounded_v005','Jill_Eye_Review_Bounded_v009')
    clip=next(n for n in ast.parse(src).body if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and isinstance(n.test.comparators[0],ast.Constant) and n.test.comparators[0].value=='clip')
    exec(compile(ast.Module(body=clip.body,type_ignores=[]),'<existing bounded clip>','exec'),ns)
