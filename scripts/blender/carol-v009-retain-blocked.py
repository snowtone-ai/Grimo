"""Reload/measure the bounded Phase A failure and retain its honest evidence.

No geometry correction or motion test. Run after build --attempt 2.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
import bpy
import bmesh
from mathutils.bvhtree import BVHTree

spec=importlib.util.spec_from_file_location('v9',Path(__file__).with_name('build-carol-v009.py'))
v9=importlib.util.module_from_spec(spec);spec.loader.exec_module(v9)
out=v9.OUT
source=out/'phase-a-attempt-2'/'measurements.json'
data=json.loads(source.read_text())
blockers=[
    'Phase A failed: lower cheek retains a hard shelf instead of a rounded jaw.',
    'Continuous neck/chest loft stretches the under-chin surface; softness and very short transition are not established.',
    'Side and 3Q face/eye identity still do not materially match the locked Skin references.',
    'Ear reconstruction was not started: temporary v008 ears retain the rejected root and Top rod collapse.',
    'Hoof reconstruction was not started: temporary v008 hooves retain the rejected tire-like 3Q form.',
    'No internally valid integrated static candidate; motion readiness is unproven.',
]
bpy.ops.wm.open_mainfile(filepath=str(v9.BASE))
baseline={o.name:v9.record(o) for o in bpy.context.scene.objects if o.type in {'MESH','CAMERA','EMPTY'}}
torso=[list(v.co) for v in bpy.data.objects['TORSO_CAGE'].data.vertices if v.co.x>=.5749]
reference_objects={o.name:dict(o.items()) for o in bpy.context.scene.objects if o.name.startswith('REFERENCE ')}
pigment=bpy.data.images['EYE pigment diagnostic packed']
pigment_hash=hashlib.sha256(bytes(pigment.packed_file.data)).hexdigest()

bpy.ops.wm.open_mainfile(filepath=str(v9.ASSET))
scene=bpy.context.scene
assert scene['selected_candidate']=='v009-A2'
digest=v9.v8.geometry_digest()
assert digest==data['geometry_digest']
assert reference_objects=={o.name:dict(o.items()) for o in scene.objects if o.name.startswith('REFERENCE ')}
assert pigment_hash==hashlib.sha256(bytes(bpy.data.images['EYE pigment diagnostic packed'].packed_file.data)).hexdigest()
frozen={name:v9.record(bpy.data.objects[name])==baseline[name] for name in data['frozen_objects']}
assert all(frozen.values())
for name,h in data['reference_hashes'].items():
    assert hashlib.sha256((v9.v8.REFERENCE/name).read_bytes()).hexdigest()==h
chassis=bpy.data.objects['CENTRAL_CHASSIS']
central_coords=[list(v.co) for v in chassis.data.vertices]
assert all(p in central_coords for p in torso)
ev=chassis.evaluated_get(bpy.context.evaluated_depsgraph_get())
points=[v.co.copy() for v in ev.data.vertices]
torso_points=[p for p in points if p.x>=.575]
torso_width=max(p.y for p in torso_points)-min(p.y for p in torso_points)
assert .598<=torso_width<=.600

bm=bmesh.new();bm.from_mesh(chassis.data)
topology=dict(vertices=len(bm.verts),edges=len(bm.edges),faces=len(bm.faces),
              euler_characteristic=len(bm.verts)-len(bm.edges)+len(bm.faces),
              nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),
              all_quads=all(len(f.verts)==4 for f in bm.faces))
bm.free()
assert topology['nonmanifold_edges']==0 and topology['all_quads']

# Disjoint-face surface intersections diagnose foldovers despite manifoldness.
# This is a geometric diagnostic, never a visual approval substitute.
polyverts=[list(p.vertices) for p in ev.data.polygons]
tree=BVHTree.FromPolygons(points,polyverts)
overlaps={(min(a,b),max(a,b)) for a,b in tree.overlap(tree)
          if a!=b and set(polyverts[a]).isdisjoint(polyverts[b])}
topology['evaluated_disjoint_face_intersection_pairs']=len(overlaps)

eyes={}
for name in ['EYE_L','EYE_R']:
    m=data['meshes'][name]
    center=(m['min'][1]+m['max'][1])/2
    assert abs(m['span'][1]-.137)<1e-6
    assert abs(m['span'][2]-.149)<1e-6
    assert abs(abs(center)-.162)<1e-6
    eyes[name]=dict(width_H=m['span'][1],height_H=m['span'][2],center_Y_H=center,depth_X_H=m['span'][0])
for name in [n for n in data['meshes'] if n.startswith('HOOF')]:
    m=data['meshes'][name]
    assert .2146<=m['span'][1]<=.2234 and .1088<=m['span'][2]<=.1132
    assert abs(m['min'][2])<.0001
assert not any(o.type=='ARMATURE' or o.animation_data for o in scene.objects)
assert not any(m.type in {'BOOLEAN','REMESH','ARMATURE'} for o in scene.objects for m in o.modifiers)
assert all(n not in bpy.data.objects for n in ['HEAD_CAGE','SHORT_NECK_SOCKET','TORSO_CAGE'])
if overlaps:
    blockers.insert(2,'Evaluated central chassis has non-adjacent face intersections; a watertight control cage is not a clean exterior.')
scene['stage']='BLOCKED_AT_V009_PHASE_A_ARCHITECTURE'
scene['human_geometry_gate']='PENDING HUMAN REVIEW'
scene['static_visual_status']='FAIL; do not advance to Phase B'
scene['motion_preflight']='NOT_RUN_STATIC_PREREQUISITE_FAILED'
scene.camera=bpy.data.objects['CAM front']
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(v9.ASSET))

validation=dict(candidate='v009-A2',technical_status='RECORDED; visual failure takes precedence',
    reloaded_neutral_digest=digest,build_digest_matches=True,central_topology=topology,
    reference_hashes_unchanged=True,reference_registration_unchanged=True,
    frozen_objects=frozen,torso_control_vertices_from_X_0575_exact=True,
    torso_evaluated_width_H=torso_width,eyes=eyes,packed_pigment_sha256=pigment_hash,
    support_centers_H=dict(FORE=.390,HIND=.920,spacing=.530),
    human_geometry_gate='PENDING HUMAN REVIEW',static_visual_status='FAIL',
    motion_preflight='NOT_RUN_STATIC_PREREQUISITE_FAILED',blockers=blockers,
    production_rig=False,animation=False,fleece=False,glb_export=False,runtime=False,
    source_blend_sha256=hashlib.sha256(v9.BASE.read_bytes()).hexdigest(),
    retained_blend_sha256=hashlib.sha256(v9.ASSET.read_bytes()).hexdigest(),
    generator_sha256=hashlib.sha256(Path(v9.__file__).read_bytes()).hexdigest())
data.update(static_visual_status='FAIL',executor_disposition='BLOCKED_AT_V009_PHASE_A_ARCHITECTURE',
            motion_preflight='NOT_RUN_STATIC_PREREQUISITE_FAILED',blockers=blockers,
            torso_evaluated_width_H=torso_width,central_topology=topology,
            attempts=dict(architecture_implementation='A1',one_bounded_correction='A2',integrated_correction='NOT_REACHED'))
(out/'measurements.json').write_text(json.dumps(data,indent=2)+'\n')
(out/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')

# One final Top diagnostic documents unchanged temporary ears. No Phase B work.
scene.camera=v9.v8.camera('TEMP top',(.65,0,4),(.65,0,.20))
assert v9.v8.geometry_digest()==digest
scene.render.filepath=str(out/'diagnostic-top.png')
bpy.ops.render.render(write_still=True)
print(json.dumps(dict(torso_width_H=torso_width,topology=topology,status=scene['stage'])))
