"""Save/reload, adversarial expression review and transport of the local Jill mouth repair."""
import ast, json, sys, hashlib, math
from pathlib import Path
from collections import Counter
import bpy, numpy as np
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'docs/production/jill/mouth-integration-v006'
A=ROOT/'assets/grimo/production/jill/tripo/mouth-integration-v006'
SOURCE=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005/jill-textured-rig-v005.blend'
BLEND=A/'jill-textured-rig-v006.blend'
tree=ast.parse((ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8').replace("'back3q':(1,2,.12)","'left3q':(-1,-2,.12),'back3q':(1,2,.12)"))
ns={'__file__':str(ROOT/'scripts/blender/jill-texture-review-v005.py')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and not any(isinstance(t,ast.Name) and t.id=='cmd' for t in n.targets)],type_ignores=[]),'<helpers>','exec'),ns)
ns['E']=E
CASES=dict(ns['STATES'])
CASES.update({'smile-L':{'smile.L':1},'smile-R':{'smile.R':1},'smile-both':{'smile.L':1,'smile.R':1},'open-smile':{'mouth_open':1,'smile.L':1,'smile.R':1},'closed-open-smile':{'mouth_close':1,'mouth_open':1,'smile.L':1,'smile.R':1}})
def write(name,data):(E/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def select(o,r):
    bpy.ops.object.select_all(action='DESELECT')
    for x in [o,r]+[a for a in bpy.context.scene.objects if a.name.startswith('ANCHOR_')]:x.select_set(True)
    bpy.context.view_layer.objects.active=r
def export(path,animate=False):
    opts=dict(filepath=str(path),export_format='GLB',use_selection=True,export_animations=animate,export_skins=True,export_morph=True,export_extras=True,export_cameras=False,export_lights=False,export_def_bones=False,export_all_influences=False,export_influence_nb=4,export_image_format='AUTO')
    if animate:opts.update(export_animation_mode='SCENE',export_force_sampling=True,export_frame_range=True,export_frame_step=1,export_bake_animation=True,export_morph_animation=True)
    bpy.ops.export_scene.gltf(**opts)
def xyz(o):
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();q=np.array([list(o.matrix_world@v.co) for v in me.vertices]);ev.to_mesh_clear();return q
cmd=sys.argv[sys.argv.index('--')+1]
if cmd=='prepare':
    o,r=ns['openfile'](A/'jill-mouth-integrated-patch-v006.blend')
    print('CHANNELS',list(ns['CHANNELS']),flush=True)
    print('DRIVERS',[(f.data_path,f.driver.expression,[(v.name,v.targets[0].data_path) for v in f.driver.variables]) for f in o.data.shape_keys.animation_data.drivers],flush=True)
    # Closing has explicit priority over simultaneous opening/smile, including intermediates.
    driver_delta=[]
    for f in o.data.shape_keys.animation_data.drivers:
        if any(k in f.data_path for k in ['FACE_MouthOpen','FACE_Smile.']):
            old=f.driver.expression
            var=f.driver.variables.get('close_gate') or f.driver.variables.new();var.name='close_gate';var.type='SINGLE_PROP';var.targets[0].id=r;var.targets[0].data_path='["mouth_close"]'
            f.driver.expression='min(max(p,0),1)*(1-min(max(close_gate,0),1))'
            driver_delta.append({'path':f.data_path,'before':old,'after':f.driver.expression})
    o['texture_status']='v006 integrated mouth / technical review candidate / Human exterior GO pending'
    o['mouth_repair']='One connected local skin/lip/cavity; original v005 texture unchanged; close input gates open/smile'
    ns['pose'](r,{});bpy.ops.file.pack_all();bpy.context.preferences.filepaths.save_version=0
    before=ns['contract'](o,r);bpy.ops.wm.save_as_mainfile(filepath=str(BLEND));o,r=ns['openfile'](BLEND)
    after=ns['contract'](o,r);assert before==after,'Save/reload contract drift'
    write('saved-blend-proof.json',{'pass':before==after,'candidate_contract':after,'driver_delta':driver_delta,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()})
    select(o,r);export(A/'jill-textured-rig-v006.glb')
    snapshots={}
    for state,vals in CASES.items():
        ns['pose'](r,vals);snapshots[state]={'channels':vals,'bones':{b.name:{'position':list(b.location),'rotation':list(b.rotation_quaternion),'scale':list(b.scale)} for b in r.pose.bones},'morphs':{k.name:float(k.value) for k in o.data.shape_keys.key_blocks[1:]}}
    write('review-states.json',snapshots)
    ns['pose'](r,{})
if cmd=='sweep':
    o,r=ns['openfile'](BLEND);m=o.data
    channels=list(ns['CHANNELS']);assert not set().union(*(set(v) for v in CASES.values()))-set(channels)
    rows=[]
    for state,vals in CASES.items():
        ns['pose'](r,vals)
        if state in ['smile-L','smile-R','smile-both','open-smile','closed-open-smile','recovery']:
            for view in ['front','side','3q']:ns['render']('check-'+state,view)
        rows.append({'state':state,'morphs':{k.name:float(k.value) for k in m.shape_keys.key_blocks[1:] if k.value}})
    samples=[]
    for close in [0,.25,.5,.75,1]:
        for opened in [0,.5,1]:
            vals={'mouth_close':close,'mouth_open':opened,'smile.L':1,'smile.R':.5}
            ns['pose'](r,vals);samples.append({'channels':vals,'morphs':{k.name:float(k.value) for k in m.shape_keys.key_blocks[1:] if k.value}})
            ns['render']('sweep-c'+str(close)+'-o'+str(opened),'3q')
    ns['pose'](r,{});ns['render']('check-recovery','front')
    write('expression-sweep.json',{'states':rows,'overlap_samples':samples,'recovery_max_delta_m':float(np.max(abs(xyz(o)-np.array([list(o.matrix_world@v.co) for v in m.vertices]))))})
if cmd=='clip':
    o,r=ns['openfile'](BLEND);s=bpy.context.scene;s.render.fps=24;schedule=[]
    # Existing representative body checks plus expression arbitration, without motion production.
    names=['mouth-closed','mouth-small','mouth-large','smile-L','smile-R','open-smile','closed-open-smile','blink-half','blink-full','wings-open','wings-fold','tail','combined']
    for i,name in enumerate(names):
        for offset,values in [(0,{}),(8,CASES[name]),(16,{})]:
            frame=1+i*22+offset;s.frame_set(frame);ns['pose'](r,values)
            for k in ns['CHANNELS']:r.keyframe_insert(data_path='["'+k+'"]',frame=frame)
        schedule.append({'name':name,'peak_seconds':(1+i*22+8)/24,'peak_frame':1+i*22+8})
    r.animation_data.action.name='Jill_Integrated_Mouth_Review_v006'
    for layer in r.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for point in fc.keyframe_points:point.interpolation='LINEAR'
    s.frame_start=1;s.frame_end=1+(len(names)-1)*22+16;s.frame_set(1)
    select(o,r);export(A/'jill-review-bounded-v006.glb',True)
    write('runtime-schedule.json',{'scope':'Local mouth repair and representative body/expression transport; not all production motions/mobile certification','time_basis':'Blender frame / 24 retained in glTF','duration':s.frame_end/24,'cases':schedule})
if cmd=='interaction':
    o,r=ns['openfile'](BLEND);neutral=xyz(o);rows=[]
    for name,vals in {
        'touch-L':{'cheek_touch.L':1,'mouth_open':.7},
        'touch-R':{'cheek_touch.R':1,'mouth_close':.6},
        'touch-both-closed':{'cheek_touch.L':1,'cheek_touch.R':1,'mouth_close':1},
        'head-left-open':{'head_yaw':-1,'head_nod':.7,'mouth_open':1},
        'head-right-closed':{'head_yaw':1,'head_tilt':-.7,'mouth_close':1},
        'breath-closed':{'breath':1,'chest_lift':1,'mouth_close':1},
    }.items():
        ns['pose'](r,vals)
        for view in ['front','side','3q']:ns['render']('interaction-'+name,view)
    for channel,meta in ns['CHANNELS'].items():
        for value in sorted(set(meta['range']+[0])):
            ns['pose'](r,{channel:value});q=xyz(o)
            rows.append({'channel':channel,'value':value,'finite':bool(np.isfinite(q).all()),'max_displacement_m':float(np.max(np.linalg.norm(q-neutral,axis=1)))})
    ns['pose'](r,{});recover=xyz(o)
    write('all-channel-sanity.json',{'pass':all(x['finite'] for x in rows),'samples':rows,'neutral_recovery_max_delta_m':float(np.max(abs(recover-neutral))),'scope':'All 39 authoring channels at declared min/zero/max: finite geometry and neutral recovery only. Visual motion GO is not inferred from this.'})
if cmd=='compare':
    for label,path in [('before',SOURCE),('after',BLEND)]:
        o,r=ns['openfile'](path)
        for state in ['neutral','mouth-closed','mouth-small','mouth-large','combined','recovery']:
            ns['pose'](r,CASES[state])
            for view in ['front','side','3q','left3q']:ns['render'](label+'-'+state,view)
if cmd=='motion-envelope':
    o,r=ns['openfile'](BLEND)
    for channel,meta in ns['CHANNELS'].items():
        for value in sorted(set(meta['range'])-{0}):
            ns['pose'](r,{channel:value})
            for view in ['front','side','3q']:ns['render']('channel-'+channel+'-'+str(value),view,False)
    ns['pose'](r,{})
    for view in ['front','side','3q','back3q','back']:ns['render']('whole-neutral',view,False)
