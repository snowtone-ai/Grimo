"""Image-only derived Jill candidate and focused rendered review."""
import bpy,json,sys,hashlib,ast
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/jill/tripo';E=ROOT/'docs/production/jill/texture-return-v005';OUT=A/'texture-return-v005'
SOURCE=A/'mouth-profile-v004/jill-rig-mouth-profile-v004.blend';BLEND=OUT/'jill-textured-rig-v005.blend';GLB=OUT/'jill-textured-rig-v005.glb'
CHANNELS=json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())['authoring_properties']
STATES={'neutral':{},'blink-half':{'blink.L':.5,'blink.R':.5},'blink-full':{'blink.L':1,'blink.R':1},'mouth-closed':{'mouth_close':1},'mouth-small':{'mouth_close':.5},'mouth-large':{'mouth_open':1},'wings-open':{'wing_open.L':1,'wing_open.R':1},'wings-fold':{'wing_open.L':-1,'wing_open.R':-1},'tail':{'tail_sway':.7,'tail_curl':.5,'leaves_tail':.6},'combined':{'blink.L':.5,'blink.R':.5,'mouth_open':.5,'wing_open.L':.65,'wing_open.R':.65,'tail_sway':-.5,'head_yaw':.4},'recovery':{}}
def write(name,data):(E/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def openfile(path):
    bpy.ops.wm.open_mainfile(filepath=str(path));o=bpy.data.objects['Jill_Body'];r=bpy.data.objects['JILL_RIG']
    if r.animation_data:r.animation_data.action=None
    pose(r,{})
    return o,r
def pose(r,values):
    assert not(set(values)-set(CHANNELS)),('Unknown authoring channel',set(values)-set(CHANNELS))
    for k in CHANNELS:r[k]=float(values.get(k,0))
    r.update_tag();bpy.context.view_layer.update()
def contract(o,r):
    h=lambda a:hashlib.sha256(np.asarray(a).tobytes()).hexdigest();m=o.data
    return {'basis':h([v.co[:] for v in m.vertices]),'topology':h([v for p in m.polygons for v in p.vertices]),'owners':[m.materials[p.material_index].get('paint_owner') for p in m.polygons],
        'uv':{u.name:h([v.uv[:] for v in u.data]) for u in m.uv_layers},'keys':{k.name:h([v.co[:] for v in k.data]) for k in m.shape_keys.key_blocks},'weights':h([(v.index,g.group,g.weight) for v in m.vertices for g in v.groups]),'groups':[g.name for g in o.vertex_groups],
        'bones':[(b.name,b.parent.name if b.parent else None,h(b.matrix_local)) for b in r.data.bones],
        'drivers':[(f.data_path,f.array_index,f.driver.expression) for block in [r,m.shape_keys] for f in block.animation_data.drivers],
        'anchors':[(a.name,a.parent.name if a.parent else None,a.parent_bone,h(a.matrix_basis)) for a in bpy.context.scene.objects if a.name.startswith('ANCHOR_')],'channels':list(CHANNELS)}
def bind(o,path):
    img=bpy.data.images.load(str(path),check_existing=False);img.colorspace_settings.name='sRGB'
    for m in o.data.materials:
        nt=m.node_tree
        for n in list(nt.nodes):
            if n.type in ['TEX_IMAGE','UVMAP']:nt.nodes.remove(n)
        uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map='Jill_Texture_UV0_v003'
        tex=nt.nodes.new('ShaderNodeTexImage');tex.image=img;tex.interpolation='Linear';tex.extension='EXTEND';nt.nodes.active=tex
        nt.links.new(uv.outputs['UV'],tex.inputs['Vector']);bs=nt.nodes.get('Principled BSDF');nt.links.new(tex.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.82;bs.inputs['Metallic'].default_value=0.
    return img
def render(name,view,face=True,pbr=False):
    s=bpy.context.scene;target=Vector((0,-.24,.68) if face else (0,0,.5));d={'front':(0,-1,.02),'side':(1,0,.02),'left':(-1,0,.02),'3q':(1,-2,.12),'back3q':(1,2,.12),'back':(0,1,.05)}[view]
    cam=s.camera;cam.location=target+Vector(d).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.45 if face else 1.22
    s.render.engine='CYCLES' if pbr else 'BLENDER_WORKBENCH'
    if pbr:s.cycles.samples=24
    s.display.shading.color_type='TEXTURE';s.display.shading.show_cavity=False;s.display.shading.show_shadows=True;s.display.shading.light='STUDIO';s.display.shading.studiolight_rotate_z=.4
    s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
    path=E/'renders'/f'{name}-{view}.png';path.parent.mkdir(exist_ok=True);s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
    print('RENDER',path.name,flush=True)
cmd=sys.argv[sys.argv.index('--')+1]
if cmd=='raw':
    o,r=openfile(SOURCE);bind(o,OUT/'source/original-basecolor-0.jpg')
    for state in ['neutral','blink-full','mouth-closed']:
        pose(r,STATES[state])
        for view in ['front','side','3q']:render('raw-'+state,view)
    pose(r,{});render('raw-body','3q',False);render('raw-body','back',False)
if cmd=='lid-field':
    from mathutils.kdtree import KDTree
    o,r=openfile(SOURCE);m=o.data;neutral=np.array([list(o.matrix_world@v.co) for v in m.vertices]);pose(r,STATES['blink-full']);ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();closed=np.array([list(o.matrix_world@v.co) for v in me.vertices]);ev.to_mesh_clear()
    with np.load(E/'face-owner-correspondence.npz') as packed:d={k:packed[k] for k in ['source_owner','source_xyz','source_uv']}
    rows=[];values=[]
    for owner in ['lids-L','lids-R']:
        entries=[(m.loops[li].vertex_index,list(m.uv_layers[0].data[li].uv)) for p in m.polygons if m.materials[p.material_index].get('paint_owner')==owner for li in p.loop_indices];kd=KDTree(len(entries))
        for i,(vi,uv) in enumerate(entries):kd.insert((uv[0],1-uv[1],0),i)
        kd.balance()
        for ti in np.flatnonzero(d['source_owner']==owner):
            hs=[]
            for p,uv in zip(d['source_xyz'][ti],d['source_uv'][ti]):
                xyz=np.array([p[0],-p[2],p[1]]);matches={entries[j][0] for co,j,dist in kd.find_range((*uv,0),2e-6) if np.linalg.norm(neutral[entries[j][0]]-xyz)<2e-6};assert len(matches)==1,(ti,matches);hs.append(closed[next(iter(matches)),2])
            rows.append(ti);values.append(hs)
    np.savez_compressed(E/'lid-closed-height.npz',source_triangle=np.array(rows),closed_height=np.array(values));write('lid-colour-field.json',{'method':'Protected eyelid colour sampled in full-blink evaluated geometry; continuous across meeting upper/lower lid edges. Texture only, all shape keys and mesh unchanged.','triangles':len(rows),'human_visual_go':False})
if cmd=='build':
    assert json.loads((E/'correspondence.json').read_text())['pass']
    o,r=openfile(SOURCE);before=contract(o,r);bind(o,OUT/'jill-basecolor-v005.png');o['texture_status']='Tripo 4K image-only review candidate / Human appearance HOLD';r['texture_review']='v005 / no Human exterior GO / no full motion production'
    bpy.ops.file.pack_all();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(BLEND));o,r=openfile(BLEND);after=contract(o,r)
    diffs=[k for k in before if before[k]!=after[k]];write('preservation.json',{'pass':not diffs,'differences':diffs,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'before':before,'after':after});assert not diffs
    bpy.ops.object.select_all(action='DESELECT');objects=[o,r]+[a for a in bpy.context.scene.objects if a.name.startswith('ANCHOR_')]
    for ob in objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=o
    bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,export_animations=False,export_skins=True,export_morph=True,export_extras=True,export_cameras=False,export_lights=False,export_def_bones=False,export_all_influences=False,export_influence_nb=4,export_image_format='AUTO')
    # Authoring-channel snapshots are a bounded runtime reference, not motion clips.
    snapshots={}
    for state,vals in STATES.items():
        pose(r,vals);snapshots[state]={'channels':vals,'bones':{b.name:{'position':list(b.location),'rotation':list(b.rotation_quaternion),'scale':list(b.scale)} for b in r.pose.bones},'morphs':{k.name:float(k.value) for k in o.data.shape_keys.key_blocks[1:]}}
    write('review-states.json',snapshots);pose(r,{})
if cmd=='render':
    o,r=openfile(BLEND)
    for state,vals in STATES.items():
        pose(r,vals);face=state not in ['wings-open','wings-fold','tail','combined']
        for view in ['front','side','3q']:render('candidate-'+state,view,face)
        if not face:render('candidate-'+state,'back3q',False)
    pose(r,{});render('candidate-body','3q',False);render('candidate-body','back',False)
if cmd=='clip':
    o,r=openfile(BLEND);s=bpy.context.scene;s.render.fps=24;schedule=[]
    cases=['mouth-closed','mouth-small','mouth-large','blink-half','blink-full','wings-open','wings-fold','tail','combined']
    for i,name in enumerate(cases):
        for offset,values in [(0,{}),(6,STATES[name]),(12,{})]:
            frame=1+i*16+offset;s.frame_set(frame);pose(r,values)
            for k in CHANNELS:r.keyframe_insert(data_path='["'+k+'"]',frame=frame)
        schedule.append({'name':name,'peak_seconds':(1+i*16+6)/24,'peak_frame':1+i*16+6})
    r.animation_data.action.name='Jill_Texture_Review_Bounded_v005'
    for layer in r.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for point in fc.keyframe_points:point.interpolation='LINEAR'
    s.frame_start=1;s.frame_end=1+(len(cases)-1)*16+12;s.frame_set(1)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in [o,r]+[a for a in s.objects if a.name.startswith('ANCHOR_')]:ob.select_set(True)
    bpy.context.view_layer.objects.active=r
    bpy.ops.export_scene.gltf(filepath=str(OUT/'jill-textured-review-bounded-v005.glb'),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_force_sampling=True,export_frame_range=True,export_frame_step=1,export_bake_animation=True,export_skins=True,export_def_bones=False,export_morph=True,export_morph_animation=True,export_all_influences=False,export_influence_nb=4,export_extras=True,export_cameras=False,export_lights=False)
    write('runtime-schedule.json',{'scope':'Bounded texture review only; no full motion production or general 39-channel runtime solver','time_basis':'glTF exporter retains Blender frame/24 timestamps, including first frame 1/24','duration':s.frame_end/24,'cases':schedule})
