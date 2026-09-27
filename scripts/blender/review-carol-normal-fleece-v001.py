"""Saved-asset audit and bounded Phase-1 deformation diagnostics; never saves poses."""
import bpy,bmesh,json,math,hashlib
import struct
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v001.blend'
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v001'
bpy.ops.wm.open_mainfile(filepath=str(ASSET)); sc=bpy.context.scene
rows=[]
def signature(o):
 return hashlib.sha256(b''.join(struct.pack('fff',*v.co) for v in o.data.vertices)).hexdigest()
baseline_names=['CENTRAL_CHASSIS','EYE_L','EYE_R','EYELID_L','EYELID_R','EAR_L','EAR_R','FORE_L','FORE_R','HIND_L','HIND_R','SKIN_TAIL_CORE','NOSE']
current={n:signature(bpy.data.objects[n]) for n in baseline_names}
base=ROOT/'assets/grimo/production/carol/blender/carol-skin-final-v002.blend'
with bpy.data.libraries.load(str(base),link=False) as (src,dst):
 dst.objects=list(baseline_names)
unchanged={n:current[n]==signature(o) for n,o in zip(baseline_names,dst.objects)}
diffs={}
for n,baseob in zip(baseline_names,dst.objects):
 ob=bpy.data.objects[n]; pairs=[(v,b) for v,b in zip(ob.data.vertices,baseob.data.vertices) if (v.co-b.co).length>1e-7]
 diffs[n]={'changed_vertices':len(pairs),'max_displacement_H':max(((v.co-b.co).length for v,b in pairs),default=0),'changed_baseline_bounds':[[min(b.co[i] for v,b in pairs),max(b.co[i] for v,b in pairs)] for i in range(3)] if pairs else None}
for o in dst.objects:bpy.data.objects.remove(o,do_unlink=True)
for o in sc.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data)
 row={'name':o.name,'vertices':len(o.data.vertices),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'non_finite_vertices':sum(not all(math.isfinite(x) for x in v.co) for v in o.data.vertices)}
 bm.free()
 if o.get('semantic_region'):
  row.update(region=o['semantic_region'],owner=o['motion_owner'],shape_keys=[k.name for k in o.data.shape_keys.key_blocks],parent=o.parent.name)
 rows.append(row)
deps=bpy.context.evaluated_depsgraph_get(); points=[]; triangles=0
for o in sc.objects:
 if o.type!='MESH':continue
 ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();triangles+=len(me.loop_triangles)
 points.extend(o.matrix_world@v.co for v in me.vertices);ev.to_mesh_clear()
report={'asset':str(ASSET.relative_to(ROOT)),'sha256':hashlib.sha256(ASSET.read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'accepted_skin_vertex_geometry_unchanged':unchanged,'hoof_change':'Existing three-toe modules enlarged to Normal visible authority, same planted support centers; applies to both visibility modes in this candidate. Original accepted Skin file unmodified.','bounds_H':[[min(p[i] for p in points),max(p[i] for p in points)] for i in range(3)],'evaluated_mesh_triangles':triangles,'objects':rows,'drivers':sum(len(o.animation_data.drivers) for o in sc.objects if o.animation_data),'camera_conditioned_geometry':False,'human_approval':False,'diagnostic_scope':'Neutral views, local contact and opening shape samples, independent tail. No full rig, animated motion, runtime, or Human deformation gate claimed.'}
report['skin_geometry_diffs']=diffs
report['hidden_abdomen_change']='Only underside behind X=.46 and below Z=.23 tucked inside fleece to eliminate visible bare belly band; accepted Skin source untouched.'
(OUT/'asset-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sc.camera=bpy.data.objects['REVIEW_front']
for o in sc.objects:
 if o.get('semantic_region')=='face_frame' and 'L' in o.name:o.data.shape_keys.key_blocks['Local_contact_compress'].value=1
sc.render.filepath=str(OUT/'diagnostic-cheek-compress.png');bpy.ops.render.render(write_still=True)
for o in sc.objects:
 if o.type=='MESH' and o.data.shape_keys:
  for k in o.data.shape_keys.key_blocks:k.value=0
  if o.get('semantic_region') in ['face_frame','chest_front']:o.data.shape_keys.key_blocks['Face_opening_corrective'].value=1
sc.render.filepath=str(OUT/'diagnostic-opening.png');bpy.ops.render.render(write_still=True)
for o in sc.objects:
 if o.type=='MESH' and o.data.shape_keys:
  for k in o.data.shape_keys.key_blocks:k.value=0
bpy.data.objects['TAIL_PIVOT'].rotation_euler.y=math.radians(-20)
sc.camera=bpy.data.objects['REVIEW_side'];sc.render.filepath=str(OUT/'diagnostic-tail.png');bpy.ops.render.render(write_still=True)
