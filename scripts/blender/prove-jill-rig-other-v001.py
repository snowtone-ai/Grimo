"""Saved-blend controls, bounded real renders, sampled GLB export. No approved source edits."""
import bpy,json,math,sys,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/jill/tripo/rig-other-v001';E=ROOT/'docs/production/jill/rig-other-v001'
PREVIEW='--preview' in sys.argv
bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-other-v001.blend'))
s=bpy.context.scene;rig=bpy.data.objects['JILL_RIG'];body=bpy.data.objects['Jill_Body']
contract=json.loads((E/'control-contract.json').read_text());channels=list(contract['authoring_properties'])
def update():rig.update_tag();bpy.context.view_layer.update()
def reset():
    for key in channels:rig[key]=0.0
    rig.pose.bones['DEF_pelvis'].location=(0,0,0);update()
def apply(values,level=1):
    reset()
    for k,v in values.items():
        if k=='pelvis_down':rig.pose.bones['DEF_pelvis'].location=rig.data.bones['DEF_pelvis'].matrix_local.to_3x3().inverted()@Vector((0,0,-v*level))
        else:rig[k]=float(v*level)
    update()
def xyz(o=body):
    ob=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh();v=np.array([tuple(o.matrix_world@x.co) for x in m.vertices]);ob.to_mesh_clear();return v
CASES=[
 ('wing-L-open',{'wing_open.L':1,'wing_camber.L':.6}),
 ('wing-L-fold',{'wing_open.L':-1}),
 ('wing-R-open',{'wing_open.R':1,'wing_flap.R':.45}),
 ('wing-R-fold',{'wing_open.R':-1}),
 ('both-wings-open',{'wing_open.L':1,'wing_open.R':1,'wing_flap.L':.4,'wing_flap.R':.4}),
 ('both-wings-fold',{'wing_open.L':-1,'wing_open.R':-1}),
 ('paw-L-offer',{'paw_offer.L':1,'paw_turn.L':.3}),
 ('paw-R-offer',{'paw_offer.R':1,'paw_turn.R':-.3}),
 ('tail-left',{'tail_sway':1,'tail_curl':.25,'leaves_tail':.3}),
 ('tail-right',{'tail_sway':-1,'tail_curl':.25,'leaves_tail':-.3}),
 ('head-gaze',{'head_yaw':1,'head_nod':.4,'head_tilt':.3,'gaze_x.L':.7,'gaze_x.R':.7,'gaze_y.L':.4,'gaze_y.R':.4,'leaves_head.L':.3}),
 ('blink',{'blink.L':1,'blink.R':1,'smile.L':.6,'smile.R':.6}),
 ('mouth-close',{'mouth_close':1,'cheek_touch.L':.65}),
 ('mouth-open',{'mouth_open':1,'smile.L':.8,'smile.R':.8}),
 ('low-support',{'pelvis_down':.012,'foot_ik.L':1,'foot_ik.R':1,'head_nod':.5,'chest_lift':-.3}),
 ('combined-left',{'wing_open.L':.8,'wing_open.R':-.45,'paw_offer.L':.7,'tail_sway':.65,'head_yaw':-.5,'head_tilt':.3,'blink.R':.5,'mouth_close':.45,'chest_lift':.65,'breath':.7,'leaves_neck.L':.5,'leaves_head.R':.3,'chest_touch':.4}),
 ('combined-right',{'wing_open.R':.8,'wing_open.L':-.45,'paw_offer.R':.7,'tail_sway':-.65,'head_yaw':.5,'blink.L':.5,'mouth_close':.45,'chest_lift':.65,'leaves_neck.R':.5,'leaves_head.L':.3}),
 ('paw-IK-contact',{'paw_ik.L':1,'foot_ik.L':1,'foot_ik.R':1})]
reset();base=xyz();edges=np.array([tuple(e.vertices) for e in body.data.edges]);body.data.calc_loop_triangles();tris=np.array([tuple(t.vertices) for t in body.data.loop_triangles]);len0=np.linalg.norm(base[edges[:,0]]-base[edges[:,1]],axis=1)
area0=np.linalg.norm(np.cross(base[tris[:,1]]-base[tris[:,0]],base[tris[:,2]]-base[tris[:,0]]),axis=1)*.5
def mat(name,c):
    m=bpy.data.materials.new('CAPTURE_ONLY_'+name);m.diffuse_color=(*c,1);return m
def capture_materials():
    # Capture-only colors clarify eyelid surfaces; no textures or identity repainting.
    skin=mat('skin',(.59,.69,.53));eye=mat('eye',(.035,.065,.040));inside=mat('mouth',(.20,.055,.065))
    body.data.materials.append(skin);si=len(body.data.materials)-1;body.data.materials.append(eye);ei=len(body.data.materials)-1;body.data.materials.append(inside);mi=len(body.data.materials)-1
    components=np.load(E/'authority-parts.npz')['component']
    for p in body.data.polygons:
        p.material_index=ei if components[p.vertices[0]] in [98,99] else si
        q=base[list(p.vertices)].mean(0)
        if (q[0]/.044)**2+((q[2]-.605)/.037)**2<.85 and -.392<q[1]<-.33:p.material_index=mi
    for side in ['L','R']:bpy.data.objects[f'Jill_Lids.{side}'].data.materials.append(skin)
def render(name,direction,target=(0,0,.50),scale=1.18):
    cam=s.camera;t=Vector(target);cam.location=t+Vector(direction).normalized()*5;cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale
    s.render.image_settings.file_format='PNG';s.render.film_transparent=False;s.render.filepath=str(E/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)
VIEWS={'front':(0,-1,0),'side':(1,0,0),'3q':(1,-2,.15)}
if PREVIEW:
    capture_materials()
    for name,values in [('neutral',{}),CASES[1],CASES[6],CASES[11],CASES[15]]:
        apply(values)
        for view,d in VIEWS.items():render('preview-'+name+'-'+view,d)
    print('PREVIEW_COMPLETE');sys.exit(0)

# First evaluate the saved authoring rig, then save an editable sparse proof action.
reports=[];samples={'neutral':base};frames=[]
for ci,(name,values) in enumerate(CASES):
    rows=[];start=1+ci*20
    for offset,level in [(0,0),(5,.5),(10,1),(15,.5),(20,0)]:
        frame=start+offset;s.frame_set(frame);apply(values,level)
        p=xyz();length=np.linalg.norm(p[edges[:,0]]-p[edges[:,1]],axis=1);ratio=length[len0>1e-7]/len0[len0>1e-7]
        area=np.linalg.norm(np.cross(p[tris[:,1]]-p[tris[:,0]],p[tris[:,2]]-p[tris[:,0]]),axis=1)*.5
        r={'frame':frame,'level':level,'finite':bool(np.isfinite(p).all()),'max_displacement':float(np.linalg.norm(p-base,axis=1).max()),'edge_ratio_min':float(ratio.min()),'edge_ratio_max':float(ratio.max()),'new_degenerate_triangles':int(np.sum((area<1e-10)&(area0>1e-10)))}
        if level==0:r['return_delta']=r['max_displacement']
        rows.append(r)
        for key in channels:rig.keyframe_insert(data_path='["'+key+'"]',frame=frame)
        rig.pose.bones['DEF_pelvis'].keyframe_insert(data_path='location',frame=frame)
        if offset in [5,10,20]:samples[f'{name}-{offset}']=p
    reports.append({'name':name,'values':values,'samples':rows,'start_frame':start,'peak_frame':start+10,'return_frame':start+20})
    frames.append({'name':name,'half':start+5,'peak':start+10,'return':start+20})
rig.animation_data.action.name='Jill_Representative_Control_Proof'
for slot in rig.animation_data.action.layers:
    for strip in slot.strips:
        for bag in strip.channelbags:
            for fc in bag.fcurves:
                for k in fc.keyframe_points:k.interpolation='LINEAR'
s.frame_start=1;s.frame_end=1+len(CASES)*20;s.render.fps=30;s.frame_set(1);update()
bpy.ops.wm.save_as_mainfile(filepath=str(A/'jill-rig-other-v001.blend'))
# Export with original materials; capture colors below never enter the saved artifact.
for o in s.objects:o.select_set(o.type!='CAMERA' and not o.name.startswith('CTRL_'))
bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.gltf(filepath=str(A/'jill-rig-other-v001.glb'),export_format='GLB',use_selection=True,
 export_animations=True,export_animation_mode='SCENE',export_force_sampling=True,export_frame_range=True,
 export_frame_step=1,export_bake_animation=True,export_skins=True,export_def_bones=False,
 export_morph=True,export_morph_animation=True,export_all_influences=False,export_influence_nb=4,
 export_extras=True,export_cameras=False,export_lights=False,export_optimize_animation_size=True)
np.savez_compressed(E/'proof-positions.npz',**samples)
(E/'proof-schedule.json').write_text(json.dumps(frames,indent=2),encoding='utf8')
(E/'pose-validation.json').write_text(json.dumps({'saved_blend_reopened':True,'cases':reports,'human_visual':'PENDING','scope':'Bounded sampled control proof, no full Motion library, not continuous collision guarantee.'},indent=2),encoding='utf8')
if '--no-render' in sys.argv:
    print('PROOF_EXPORT_COMPLETE_NO_RENDER',len(frames),s.frame_end);sys.exit(0)
capture_materials();s.frame_set(1);update()
for view,d in VIEWS.items():render('neutral-'+view,d)
MID={'both-wings-fold','paw-L-offer','blink','combined-left','low-support'}
RETURN={'both-wings-fold','blink','combined-left','low-support'}
for case in frames:
    for phase in (['half','peak','return'] if case['name'] in RETURN else ['half','peak'] if case['name'] in MID else ['peak']):
        s.frame_set(case[phase]);update()
        for view,d in VIEWS.items():render(case['name']+'-'+phase+'-'+view,d)
    if case['name'] in ['blink','mouth-close','mouth-open','head-gaze']:
        s.frame_set(case['peak']);update();render(case['name']+'-face-3q',(1,-2,.10),(0,-.23,.70),.52)
print('PROOF_EXPORT_RENDER_COMPLETE',len(frames),s.frame_end)
