"""Read-only saved-file audit. Does not assert perceptual or motion approval."""
import bpy,hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v002.blend'
BASE=ROOT/'assets/grimo/production/carol/blender/carol-skin-final-v002.blend'
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v002'
bpy.ops.wm.open_mainfile(filepath=str(ASSET));sc=bpy.context.scene
report={'asset':ASSET.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(ASSET.read_bytes()).hexdigest(),
 'accepted_skin_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),
 'verified_starting_pushed_commit':'091487fb842b9698cb09e753a7e029b18482e9fa',
 'v001_human_review':'FAIL','v002_human_review':'PENDING','phase1_state':sc.get('phase1_state'),
 'motion_gate':'NOT_PERFORMED','deformation_gate':'NOT_PERFORMED','runtime_gate':'NOT_PERFORMED','device_gate':'NOT_PERFORMED',
 'third_party_source':'Savino Star, CC0; imported outline rounded and rebuilt with convex caps',
 'eye_dimensions_evidence':'eye-measurements.json',
 'camera_conditioned_geometry':False,'compositing':sc.render.use_compositing,
 'render':{'engine':sc.render.engine,'samples':sc.cycles.samples,'view_transform':sc.view_settings.view_transform,'exposure':sc.view_settings.exposure},
 'owners':{},'anchors':{},'hooves':[]}
for owner in ['FLEECE_HEAD_OWNER','FLEECE_TORSO_OWNER','TAIL_PIVOT']:
 report['owners'][owner]=[o.name for o in sc.objects if o.parent and o.parent.name==owner]
for name in ['fleece_front','pocket_front_L','pocket_front_R','gift_reveal']:
 o=bpy.data.objects[name];report['anchors'][name]={'parent':o.parent.name,'world_position':list(o.matrix_world.translation)}
for o in sc.objects:
 if o.name.startswith('HOOF_'):
  report['hooves'].append({'name':o.name,'vertices':len(o.data.vertices),'construction':'Single tapered brown solid; two localized distal incisions; continuous proximal body. Visible silhouette requires Human review.'})
report['non_finite_vertices']=sum(not all(math.isfinite(a) for a in v.co) for o in sc.objects if o.type=='MESH' for v in o.data.vertices)
assert report['non_finite_vertices']==0
assert report['accepted_skin_sha256']=='321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a'
assert len(report['hooves'])==4
for owner,children in report['owners'].items():
 assert children, 'Empty motion owner: '+owner
for name,anchor in report['anchors'].items():
 assert anchor['parent']=='FLEECE_TORSO_OWNER', name
report['regional_masks']={o.name:[g.name for g in o.vertex_groups] for o in sc.objects if o.name in ['FLEECE_HEAD_SURFACE','FLEECE_TORSO_SURFACE']}
assert len(report['regional_masks'])==2
for groups in report['regional_masks'].values():
 assert {'touch_L','touch_R','crown','face_frame','chest_front','central_back','rump','lower_belly'}<=set(groups)
report['external_images']=[{'name':im.name,'path':im.filepath,'packed':bool(im.packed_file)} for im in bpy.data.images if im.source=='FILE']
for im in bpy.data.images:
 if im.source=='FILE' and not im.packed_file:
  assert Path(bpy.path.abspath(im.filepath)).is_file(), 'Missing image: '+im.name
report['fleece_channels']={o.name:[k.name for k in o.data.shape_keys.key_blocks] for o in sc.objects if o.type=='MESH' and o.get('semantic_region') and o.data.shape_keys}
report['neutral_fleece_values']={o.name:{k.name:k.value for k in o.data.shape_keys.key_blocks if k.name!='Basis'} for o in sc.objects if o.type=='MESH' and (o.name.startswith('FLEECE_') or o.name=='TAIL_FLEECE_SHELL') and o.data.shape_keys}
assert all(abs(v)<1e-8 for obj in report['neutral_fleece_values'].values() for v in obj.values()), 'Fleece is not neutral'
report['limitations']=['No finished production rig or head-turn collision validation.','Local channels preserve authoring affordances, not completed motion.','Procedural material is Blender authoring material; runtime appearance unvalidated.','Human perceptual approval remains outstanding.']
(OUT/'asset-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['sha256','accepted_skin_sha256','non_finite_vertices']}))
