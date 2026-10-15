"""Read-only author/saved-GLB comparison for Human A/B HOLD. No blend/GLB saves."""
import bpy,sys,json,importlib.util
from pathlib import Path
from mathutils import Vector
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-skin-compat'
spec=importlib.util.spec_from_file_location('v004_proof',ROOT/'scripts/blender/prove-shushu-production-rig-v004.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
kind=sys.argv[sys.argv.index('--kind')+1] if '--kind' in sys.argv else 'author'
if kind=='author':bpy.ops.wm.open_mainfile(filepath=str(q.v.PROOF))
else:q.p.import_saved(q.v.GLB)
meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')]
for o in bpy.data.objects:
    if o.type=='MESH' and o not in meshes:o.hide_render=True
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
if '--normals-only' in sys.argv:
    folder=OUT/('blender-'+kind);folder.mkdir(exist_ok=True)
    for frame in [1,477,493,509,517,533,549]:
        bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();data={}
        for o in meshes:
            if not o.name.startswith('ShushuStatic_Paw'):continue
            ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles()
            data[o.name+'-p']=np.array([ev.matrix_world@v.co for v in m.vertices])
            nm=ev.matrix_world.to_3x3().inverted().transposed()
            data[o.name+'-n']=np.array([(nm@n.vector).normalized() for n in m.vertex_normals])
            data[o.name+'-tri']=np.array([list(t.vertices) for t in m.loop_triangles])
            ev.to_mesh_clear()
        np.savez_compressed(folder/f'normals-{frame}.npz',**data)
    print('NORMALS_DONE',kind,flush=True);sys.exit(0)
scene,cam=q.b.setup_review(640,12)
cam.data.type='ORTHO';cam.data.ortho_scale=1.18
folder=OUT/('blender-'+kind);folder.mkdir(exist_ok=True)
views={'front':(0,-3,.5),'side':(-3,0,.5),'3q':(-2,-2.5,.65)}
def camera(view):
    cam.location=views[view];cam.rotation_euler=(Vector((0,0,.5))-cam.location).to_track_quat('-Z','Y').to_euler()
def evaluated(o):
    return q.b.evaluated(o)[0]
def dump_frame(frame):
    scene.frame_set(frame);bpy.context.view_layer.update()
    row={'frame':frame,'meshes':{},'bones':{}}
    for name in ['LeftArm','LeftForeArm','LeftHand','RightArm','RightForeArm','RightHand']:
        pb=rig.pose.bones.get('mixamorig:'+name)
        if pb:row['bones'][name]={'head':list(rig.matrix_world@pb.head),'tail':list(rig.matrix_world@pb.tail),'matrix':list(map(list,rig.matrix_world@pb.matrix))}
    for o in meshes:
        if not any(t in o.name for t in ['Paw','Head','MouthInterior','LidWall','Tongue']):continue
        p=evaluated(o);shapes=o.data.shape_keys
        row['meshes'][o.name]={'vertices':len(p),'bounds':[p.min(0).tolist(),p.max(0).tolist()],'activeShapes':{k.name:float(k.value) for k in shapes.key_blocks[1:] if abs(k.value)>1e-7} if shapes else {}}
    return row
frames=sorted(set([1,169,333,345,349,357,477,493,509,517,533,549]+list(range(505,542,3))))
inventory={'kind':kind,'blender':bpy.app.version_string,'source':str(q.v.PROOF if kind=='author' else q.v.GLB),'frames':[],'objects':[]}
scene.frame_set(1)
for o in meshes:
    keys=o.data.shape_keys
    inventory['objects'].append({'name':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'modifiers':[{'name':m.name,'type':m.type,'preserveVolume':getattr(m,'use_deform_preserve_volume',None)} for m in o.modifiers],
    'shapeNames':[k.name for k in keys.key_blocks] if keys else [],'materials':[{'name':m.name,'images':[{'name':n.image.name,'size':list(n.image.size)} for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]} for m in o.data.materials if m]})
    if o.name.startswith('ShushuStatic_Paw'):
        groupnames={g.index:g.name for g in o.vertex_groups}
        weights=[{groupnames[g.group]:g.weight for g in v.groups if g.weight>1e-7} for v in o.data.vertices]
        (folder/(o.name+'-weights.json')).write_text(json.dumps({'basis':[list(v.co) for v in o.data.vertices],'weights':weights,'polygons':[list(p.vertices) for p in o.data.polygons]},indent=2)+'\n')
for f in frames:
    row=dump_frame(f);inventory['frames'].append(row)
    is_sequence=505<=f<=541
    selected=['side','3q'] if is_sequence or f in [477,493,549] else ['front','side','3q'] if f in [1,333,345,349,357] else ['side','3q']
    for view in selected:
        camera(view);scene.render.filepath=str(folder/f'f{f}-{view}.png');bpy.ops.render.render(write_still=True)
    print('DEFECT_FRAME',kind,f,flush=True)
(folder/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
print('READ_ONLY_DIAGNOSIS_DONE',kind,flush=True)
