"""Export texture-only neutral surfaces; reopen saved rig and reimport both formats.

No Tripo operation. Comparisons distinguish surface/UV agreement from visual GO.
"""
import bpy,json,hashlib,struct,sys
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-v002'
E=ROOT/'docs/production/jill/rig-pretexture-v002'
def write(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2,default=lambda value:value.item())+'\n',encoding='utf8')
def coords(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([tuple(o.matrix_world@v.co) for v in m.vertices]);ev.to_mesh_clear();return p
def dist(a,b):
 kd=KDTree(len(b))
 for i,p in enumerate(b):kd.insert(Vector(p),i)
 kd.balance();d=np.array([kd.find(Vector(p))[2] for p in a]);return float(d.max())
def corners(o):
 m=o.data;uv=m.uv_layers[0]
 return np.array([(*tuple(o.matrix_world@m.vertices[l.vertex_index].co),*tuple(uv.data[l.index].uv)) for l in m.loops])
def unique(a,dec=5):return np.unique(np.round(a,dec),axis=0)
def signature(a):return hashlib.sha256(unique(a).astype('<f8').tobytes()).hexdigest()
def anchorpos():
 out={}
 for o in bpy.context.scene.objects:
  if o.name.startswith('ANCHOR_'):out[o.name]=np.array(o.matrix_world.translation)
 for arm in [o for o in bpy.context.scene.objects if o.type=='ARMATURE']:
  for b in arm.pose.bones:
   if b.name.startswith('ANCHOR_'):out[b.name]=np.array((arm.matrix_world@b.matrix).translation)
 return out
bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-pretexture-v002.blend'))
s=bpy.context.scene;r=bpy.data.objects['JILL_RIG'];b=bpy.data.objects['Jill_Body']
proof=np.load(E/'proof-positions.npz');schedule=json.loads((E/'proof-schedule.json').read_text())
used=sorted({i for p in b.data.polygons for i in p.vertices});refs={};reopen=[]
# One peak per case, plus half and return of the composite; bounded sampling.
cases=[(c['name']+'-peak',c['peak'],c['name']+'-12') for c in schedule]
cases += [('combined-L-half',schedule[-2]['half'],'combined-L-6'),('combined-L-return',schedule[-2]['return'],'combined-L-24')]
for label,frame,key in cases:
 s.frame_set(frame);r.update_tag();bpy.context.view_layer.update();p=coords(b)
 refs[label]=(p[used],anchorpos());reopen.append({'case':label,'frame':frame,'saved_max_delta':float(np.linalg.norm(p-proof[key],axis=1).max())})
channels=list(json.loads((E/'control-contract.json').read_text())['authoring_properties'])
r.animation_data.action=None
for k in channels:r[k]=0.
r.update_tag();bpy.context.view_layer.update()
neutral=coords(b);ev=b.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=bpy.data.meshes.new_from_object(ev,preserve_all_data_layers=True,depsgraph=bpy.context.evaluated_depsgraph_get())
obj=bpy.data.objects.new('Jill_Texture_Input_Neutral',mesh);s.collection.objects.link(obj);obj.matrix_world=b.matrix_world.copy()
# The upload has one unambiguous UV layer and no rig, morph, anchors or animation.
while len(mesh.uv_layers)>1:mesh.uv_layers.remove(mesh.uv_layers[-1])
expected=corners(obj)
for o in s.objects:o.select_set(False)
obj.select_set(True);bpy.context.view_layer.objects.active=obj
if '--verify-only' not in sys.argv:
 bpy.ops.export_scene.gltf(filepath=str(A/'jill-texture-input-neutral-v002.glb'),export_format='GLB',use_selection=True,export_animations=False,export_skins=False,export_morph=False,export_extras=False,export_cameras=False,export_lights=False)
 bpy.ops.export_scene.fbx(filepath=str(A/'jill-texture-input-neutral-v002.fbx'),use_selection=True,object_types={'MESH'},use_mesh_modifiers=False,add_leaf_bones=False,bake_anim=False,axis_forward='-Z',axis_up='Y',path_mode='AUTO',use_triangles=True)
uvs=np.array([tuple(x.uv) for x in mesh.uv_layers[0].data]);mesh.calc_loop_triangles();areas=[]
for t in mesh.loop_triangles:
 q=uvs[list(t.loops)];areas.append(abs(np.cross(q[1]-q[0],q[2]-q[0]))*.5)
uv_report={'active':'Tripo_Input_UV','source_layer':'v002_Source_UV_Preserved','active_range':[uvs.min(0).tolist(),uvs.max(0).tolist()],
 'triangles':len(areas),'zero_area_uv_triangles':int(np.count_nonzero(np.array(areas)<1e-12)),
 'texture_input_one_uv':len(mesh.uv_layers)==1,'expected_unique_position_uv_signature_round_1e5':signature(expected),
 'note':'Unique position/UV corner comparison tolerates seam splits and triangulation. Does not prove paint quality, padding or absence of overlaps.'}
write('uv-validation.json',uv_report)
static=[]
for suffix in ['glb','fbx']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 path=A/('jill-texture-input-neutral-v002.'+suffix)
 if suffix=='glb':bpy.ops.import_scene.gltf(filepath=str(path))
 else:bpy.ops.import_scene.fbx(filepath=str(path),use_anim=False)
 ob=[o for o in bpy.context.scene.objects if o.type=='MESH'];got=np.concatenate([corners(o) for o in ob])
 # Separate position+UV nearest comparison avoids rounding-boundary artifacts.
 kd=KDTree(len(expected))
 for i,p in enumerate(expected[:,:3]):kd.insert(Vector(p),i)
 kd.balance();errors=[]
 for p in got:
  near=kd.find_range(Vector(p[:3]),2e-6)
  errors.append(min((np.linalg.norm(expected[i,3:]-p[3:]) for _,i,_ in near),default=99.))
 row={'format':suffix,'mesh_count':len(ob),'armatures':sum(o.type=='ARMATURE' for o in bpy.context.scene.objects),'morph_count':sum(len(o.data.shape_keys.key_blocks)-1 if o.data.shape_keys else 0 for o in ob),
 'unique_corner_signature_round_1e5':signature(got),'signature_equal':signature(got)==signature(expected),'position_max_delta':dist(got[:,:3],expected[:,:3]),'uv_max_delta_nearest_position':max(errors)}
 row['surface_uv_pass']=row['position_max_delta']<2e-6 and row['uv_max_delta_nearest_position']<2e-6
 static.append(row)
# Parse actual delivered rig structure, then fresh import at authored 24 fps.
blob=(A/'jill-rig-pretexture-v002.glb').read_bytes();n=struct.unpack_from('<I',blob,12)[0];g=json.loads(blob[20:20+n])
structure={'skins':[len(x['joints']) for x in g.get('skins',[])],'morph_names':[m.get('extras',{}).get('targetNames',[]) for m in g['meshes']],
 'anchors':[x.get('name') for x in g['nodes'] if x.get('name','').startswith('ANCHOR_')],
 'animations':[{'name':a.get('name'),'paths':sorted({c['target']['path'] for c in a['channels']})} for a in g.get('animations',[])],
 'uv_sets':sorted({k for m in g['meshes'] for p in m['primitives'] for k in p['attributes'] if k.startswith('TEXCOORD')})}
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=24
bpy.ops.import_scene.gltf(filepath=str(A/'jill-rig-pretexture-v002.glb'))
s=bpy.context.scene;ob=[o for o in s.objects if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)];rows=[]
assert len(ob)==len(g['meshes']),'Imported skin meshes differ from GLB structure'
for label,frame,key in cases:
 s.frame_set(frame);bpy.context.view_layer.update();got=np.concatenate([coords(o)[sorted({i for p in o.data.polygons for i in p.vertices})] for o in ob]);ref,ap=refs[label];aq=anchorpos()
 rows.append({'case':label,'frame':frame,'import_to_saved_max':dist(got,ref),'saved_to_import_max':dist(ref,got),
 'import_bounds':[got.min(0).tolist(),got.max(0).tolist()],'reference_bounds':[ref.min(0).tolist(),ref.max(0).tolist()],
 'anchor_count':len(aq),'anchor_max_delta':max((float(np.linalg.norm(ap[k]-aq[k])) for k in ap if k in aq),default=99.)})
passed=all(x['surface_uv_pass'] for x in static) and all(x['saved_max_delta']<1e-5 for x in reopen) and all(x['import_to_saved_max']<1e-5 and x['saved_to_import_max']<1e-5 and x['anchor_count']==16 and x['anchor_max_delta']<1e-5 for x in rows)
write('roundtrip-validation.json',{'bounded_pass':passed,'tolerance_m':1e-5,'blender_reopen':reopen,'texture_input_neutral_vs_saved_rig_max':float(np.linalg.norm(neutral-proof['neutral'],axis=1).max()),'static_inputs':static,'rig_glb_structure':structure,'rig_glb_reimport':rows,'boundary':'Only imported skinned meshes and vertices used by rendered polygons compared. Blender-import-created Icosphere bone-display helper excluded, absent in GLB mesh structure. Saved proof playback only; arbitrary runtime semantic solver and Human visual GO are not certified.'})
print('PACKAGE_COMPLETE',passed)
if not passed:sys.exit(2)
