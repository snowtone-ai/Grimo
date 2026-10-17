"""Local host-eye texture repair. No geometry, UV, rig or Morph changes."""
import ast,json,sys,hashlib
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets/grimo/production/jill/tripo/eye-boundary-v008'
E=ROOT/'docs/production/jill/eye-boundary-v008'
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
    before=ns['contract'](o,r);ns['bind'](o,A/'jill-basecolor-v008.png')
    o['texture_status']='v008 local host-eye residual cleanup; mouth/clover Human GO; eye review pending'
    r['texture_review']='v008 texture only; all geometry, UV, Morph, rig and approved features retained'
    bpy.ops.file.pack_all();bpy.context.preferences.filepaths.save_version=0
    blend=A/'jill-textured-rig-v008.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));o,r=ns['openfile'](blend)
    after=ns['contract'](o,r);assert before==after,'Geometry/UV/rig/Morph drift'
    write('preservation.json',{'pass':True,'contract_exact':True,'before':before,'after':after,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scope':'BaseColor only; every vertex, polygon, 3 UV layers, weight, Morph coordinate, driver, 130 bones, 39 channels and 16 anchors exact vs approved v007 baseline.'})
    bpy.ops.object.select_all(action='DESELECT')
    for ob in [o,r]+[x for x in bpy.context.scene.objects if x.name.startswith('ANCHOR_')]:ob.select_set(True)
    bpy.context.view_layer.objects.active=r
    bpy.ops.export_scene.gltf(filepath=str(A/'jill-textured-rig-v008.glb'),export_format='GLB',use_selection=True,export_animations=False,export_skins=True,export_morph=True,export_extras=True,export_cameras=False,export_lights=False,export_def_bones=False,export_all_influences=False,export_influence_nb=4,export_image_format='AUTO')
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
    o,r=ns['openfile'](A/'jill-textured-rig-v008.blend');snapshots={}
    for state,values in ns['STATES'].items():
        ns['pose'](r,values);snapshots[state]={'channels':values,'morphs':{k.name:float(k.value) for k in o.data.shape_keys.key_blocks[1:]}}
    write('review-states.json',snapshots)
    ns['OUT']=A;ns['BLEND']=A/'jill-textured-rig-v008.blend'
    src=(ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8').replace('jill-textured-review-bounded-v005.glb','jill-review-bounded-v008.glb').replace('Jill_Texture_Review_Bounded_v005','Jill_Eye_Review_Bounded_v008')
    clip=next(n for n in ast.parse(src).body if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and isinstance(n.test.comparators[0],ast.Constant) and n.test.comparators[0].value=='clip')
    exec(compile(ast.Module(body=clip.body,type_ignores=[]),'<existing bounded clip>','exec'),ns)
