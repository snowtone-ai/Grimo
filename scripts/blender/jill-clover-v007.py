"""Image-only Canonical thigh marking; preserve the Human-approved v006 mouth."""
import ast, json, sys, hashlib
from pathlib import Path
import bpy, numpy as np

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets/grimo/production/jill/tripo/clover-v007'
E=ROOT/'docs/production/jill/clover-v007'
SOURCE=ROOT/'assets/grimo/production/jill/tripo/mouth-integration-v006/jill-textured-rig-v006.blend'
A.mkdir(exist_ok=True);E.mkdir(exist_ok=True);(E/'renders').mkdir(exist_ok=True)
tree=ast.parse((ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8').replace("'back3q':(1,2,.12)","'left3q':(-1,-2,.12),'back3q':(1,2,.12)"))
ns={'__file__':str(ROOT/'scripts/blender/jill-texture-review-v005.py')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and not any(isinstance(t,ast.Name) and t.id=='cmd' for t in n.targets)],type_ignores=[]),'<helpers>','exec'),ns)
ns['E']=E
cmd=sys.argv[sys.argv.index('--')+1]
o,r=ns['openfile'](SOURCE);m=o.data

def write(name,data):(E/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def select():
    bpy.ops.object.select_all(action='DESELECT')
    for ob in [o,r]+[x for x in bpy.context.scene.objects if x.name.startswith('ANCHOR_')]:ob.select_set(True)
    bpy.context.view_layer.objects.active=r

if cmd=='surface':
    m.calc_loop_triangles();q=np.array([v.co[:] for v in m.vertices]);tris=[];uv=[]
    for t in m.loop_triangles:
        if m.materials[t.material_index].get('paint_owner')!='body_skin':continue
        p=q[list(t.vertices)]
        if p[:,0].min()>-.12 or p[:,0].max()<-.25 or p[:,2].min()>.28 or p[:,2].max()<.12 or p[:,1].min()>-.12:continue
        if np.dot(t.normal,(-.5,-.866,0))<.15:continue
        tris.append(p);uv.append([m.uv_layers[0].data[i].uv[:] for i in t.loops])
    np.savez_compressed(E/'thigh-surface.npz',xyz=tris,uv=uv)
    write('projection.json',{'human_decision':'2026-10-18: add clover according to Canonical','surface':'Canonical visible thigh, front-left image side; model X negative. No back/opposite-side duplicate','center':[-.181,-.21,.205],'tangent':[.8660254,-.5,0],'width_m':.073,'height_m':.090,'triangles':len(tris)})
if cmd=='build':
    before=ns['contract'](o,r);ns['bind'](o,A/'jill-basecolor-v007.png')
    o['texture_status']='v007 Canonical thigh clover candidate; mouth Human GO 2026-10-18; full model HOLD'
    r['texture_review']='v007 image-only clover; approved v006 mouth and all rig data retained'
    bpy.ops.file.pack_all();bpy.context.preferences.filepaths.save_version=0
    blend=A/'jill-textured-rig-v007.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));o,r=ns['openfile'](blend);m=o.data
    after=ns['contract'](o,r);assert before==after,'Geometry/UV/rig/morph/driver drift'
    write('preservation.json',{'pass':True,'contract_exact':True,'before':before,'after':after,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scope':'All geometry, topology, UVs, weights, Morphs, drivers, bones, anchors and channels exact. BaseColor image only.'})
    select();bpy.ops.export_scene.gltf(filepath=str(A/'jill-textured-rig-v007.glb'),export_format='GLB',use_selection=True,export_animations=False,export_skins=True,export_morph=True,export_extras=True,export_cameras=False,export_lights=False,export_def_bones=False,export_all_influences=False,export_influence_nb=4,export_image_format='AUTO')
    for state in ['neutral','mouth-closed','mouth-small','mouth-large','combined','recovery']:
        ns['pose'](r,ns['STATES'][state])
        for view in ['front','side','left3q']:ns['render'](state,view,False)
    ns['pose'](r,{})
    for view in ['back','left']:ns['render']('neutral',view,False)
    # Same-camera face pixels prove the approved mouth was preserved by this image-only edit.
    for state in ['neutral','mouth-closed','mouth-small','mouth-large','recovery']:
        ns['pose'](r,ns['STATES'][state]);ns['render']('face-'+state,'front')
if cmd=='detail':
    from mathutils import Vector
    o,r=ns['openfile'](A/'jill-textured-rig-v007.blend');s=bpy.context.scene;cam=s.camera
    target=Vector((-.18,-.21,.205));s.render.engine='BLENDER_WORKBENCH'
    s.display.shading.color_type='TEXTURE';s.display.shading.show_cavity=False;s.display.shading.show_shadows=True;s.display.shading.light='STUDIO';s.display.shading.studiolight_rotate_z=.4
    s.render.resolution_x=800;s.render.resolution_y=800;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
    for view,direction in [('front',(0,-1,.02)),('3q',(-1,-2,.05))]:
        cam.location=target+Vector(direction).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.14
        s.render.filepath=str(E/f'clover-detail-{view}.png');bpy.ops.render.render(write_still=True)
