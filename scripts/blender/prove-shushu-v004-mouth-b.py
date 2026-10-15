"""Focused editable diagnostic action / saved GLB / roundtrip renders for mouth B."""
import bpy,sys,json,importlib.util
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('mouthb',ROOT/'scripts/blender/repair-shushu-v004-mouth-b.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
OUT=r.OUT;PROOF=r.ASSET.with_name(r.ASSET.stem+'-proof.blend')
MARKS=[(1,0,0),(13,.2,0),(25,.55,0),(37,1,0),(49,.55,0),(61,.2,0),(73,0,0),(85,0,1),(97,.2,1),(109,.55,1),(121,1,1),(133,0,1),(145,1,1),(157,0,1),(169,0,0)]
def evaluate(o):
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([ev.matrix_world@v.co for v in m.vertices]);ev.to_mesh_clear();return p
def export():
    rig=r.load();r.b.reset(rig);scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=169;scene.render.fps=24
    meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')];anchors=[o for o in bpy.data.objects if o.name.startswith('ANCHOR_')]
    for frame,opening,seat in MARKS:
        for prop,value in {'MouthOpen':opening,'Seat':seat,'MouthClose':1 if frame==145 else 0,'Tongue':1 if frame in [145,157] else 0}.items():rig[prop]=float(value);rig.keyframe_insert(data_path='["'+prop+'"]',frame=frame)
    for layer in rig.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for key in fc.keyframe_points:key.interpolation='LINEAR'
    scene.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(PROOF))
    pose={};morph={};anchor={};reference={};ar={n.name:[] for n in anchors};sample=set(f for f,_,_ in MARKS)|{7,19,31,43,55,67}
    for frame in range(1,170):
        scene.frame_set(frame);bpy.context.view_layer.update();pose[frame]={pb.name:pb.matrix.copy() for pb in rig.pose.bones}
        morph[frame]={o.name:{k.name:float(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.shape_keys.key_blocks[k.name].value) for k in o.data.shape_keys.key_blocks[1:]} for o in meshes if o.data.shape_keys}
        anchor[frame]={o.name:o.matrix_basis.copy() for o in anchors}
        for o in anchors:ar[o.name].append(np.array(o.matrix_world))
        if frame in sample:
            for o in meshes:reference[o.name+'__'+str(frame)]=evaluate(o).astype(np.float32)
    np.savez_compressed(OUT/'saved-reference.npz',**reference);np.savez_compressed(OUT/'anchor-reference.npz',**ar)
    for obj in [rig]+anchors:
        if obj.animation_data:
            obj.animation_data.action=None
            for fc in list(obj.animation_data.drivers):obj.driver_remove(fc.data_path,fc.array_index)
    for pb in rig.pose.bones:
        for c in list(pb.constraints):pb.constraints.remove(c)
        pb.rotation_mode='QUATERNION'
    for o in meshes:
        if o.data.shape_keys and o.data.shape_keys.animation_data:
            o.data.shape_keys.animation_data.action=None
            for fc in list(o.data.shape_keys.animation_data.drivers):o.data.shape_keys.driver_remove(fc.data_path,fc.array_index)
    for frame in range(1,170):
        scene.frame_set(frame)
        for pb in rig.pose.bones:
            pb.matrix_basis=pb.bone.convert_local_to_pose(pose[frame][pb.name],pb.bone.matrix_local,parent_matrix=pose[frame][pb.parent.name] if pb.parent else Matrix.Identity(4),parent_matrix_local=pb.parent.bone.matrix_local if pb.parent else Matrix.Identity(4),invert=True)
            for path in ['location','rotation_quaternion','scale']:pb.keyframe_insert(data_path=path,frame=frame)
        for name,keys in morph[frame].items():
            for key,value in keys.items():k=bpy.data.objects[name].data.shape_keys.key_blocks[key];k.value=value;k.keyframe_insert(data_path='value',frame=frame)
        for o in anchors:
            o.matrix_basis=anchor[frame][o.name]
            for path in ['location','rotation_euler','scale']:o.keyframe_insert(data_path=path,frame=frame)
    scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT')
    for o in [rig]+meshes+anchors:o.select_set(True)
    bpy.context.view_layer.objects.active=rig
    bpy.ops.export_scene.gltf(filepath=str(r.GLB),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_frame_step=1,export_force_sampling=True,export_bake_animation=True,export_anim_scene_split_object=False,export_nla_strips_merged_animation_name='MouthB_Diagnostic_NotProduction',export_optimize_animation_size=False,export_skins=True,export_all_influences=True,export_morph=True,export_morph_animation=True,export_apply=False,export_keep_originals=False,export_extras=True)
    r.write('diagnostic-timeline.json',{'fps':24,'frames':169,'states':[{'frame':f,'MouthOpen':o,'Seat':s,'MouthClose':1 if f==145 else 0,'Tongue':1 if f in [145,157] else 0} for f,o,s in MARKS],'scope':'Focused mouth diagnostic; no production Motion adopted. source times f/24.'})
    print('MOUTH_B_EXPORTED',flush=True)
def imported():
    p=r.module('proof001','scripts/blender/prove-shushu-production-rig-v001.py');p.import_saved(r.GLB)
def verify():
    imported();scene=bpy.context.scene;meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')]
    ref=np.load(OUT/'saved-reference.npz');from mathutils.kdtree import KDTree
    # Fully open coordinates distinguish upper/lower contact vertices which are
    # deliberately coincident at closure. Use a fixed mapping for every state.
    maps={};rows=[];scene.frame_set(37)
    for o in meshes:
        p=ref[o.name+'__37'];tree=KDTree(len(p))
        for i,q in enumerate(p):tree.insert(q,i)
        tree.balance();maps[o.name]=np.array([tree.find(v)[1] for v in evaluate(o)])
    frames=sorted(set(int(k.rsplit('__',1)[1]) for k in ref.files))
    for frame in frames:
        scene.frame_set(frame)
        for o in meshes:
            a=evaluate(o);expected=ref[o.name+'__'+str(frame)][maps[o.name]];rows.append({'frame':frame,'mesh':o.name,'max_position_error':float(np.linalg.norm(a-expected,axis=1).max())})
    ar=np.load(OUT/'anchor-reference.npz');anchor_error=0
    for frame in range(1,170):
        scene.frame_set(frame)
        for name in ar.files:anchor_error=max(anchor_error,float(abs(np.array(bpy.data.objects[name].matrix_world)-ar[name][frame-1]).max()))
    result={'rows':rows,'max_position_error':max(x['max_position_error'] for x in rows),'anchor_max_matrix_error':anchor_error,'mapping':'Fixed nearest fully-open frame 37 coordinates; separates coincident closed upper/lower lip vertices. Reused for all 21 samples.','nearest_mapping_limit':'Coincident UV split vertices can have different ownership; this focused action uses zero paw controls, and positions remain separately checked.'};r.write('saved-roundtrip.json',result)
    assert result['max_position_error']<1e-5 and anchor_error<1e-5
    print('ROUNDTRIP',result['max_position_error'],anchor_error,flush=True)
def renders():
    saved='--saved' in sys.argv
    if saved:imported()
    else:bpy.ops.wm.open_mainfile(filepath=str(PROOF))
    scene,cam=r.b.setup_review(640,24);cam.data.type='ORTHO';cam.data.ortho_scale=.56
    folder=OUT/('saved' if saved else 'author');folder.mkdir(exist_ok=True)
    for name,frame in [('closed',1),('small',13),('medium',25),('large',37)]:
        scene.frame_set(frame)
        for view,loc in r.VIEWS.items():
            cam.location=loc;cam.rotation_euler=(Vector((0,-.02,.69))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
        print('PROOF_RENDER',saved,name,flush=True)
if __name__=='__main__':
    if '--export' in sys.argv:export()
    elif '--refresh-texture' in sys.argv:
        r.ASSET=PROOF;r.texture()
    elif '--verify' in sys.argv:verify()
    elif '--render' in sys.argv:renders()
