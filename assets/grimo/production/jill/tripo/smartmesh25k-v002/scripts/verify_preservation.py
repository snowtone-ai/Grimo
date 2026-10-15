"""Saved candidate vs saved sole source, and hashes of protected inputs. No save."""
import bpy,json,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[7];OLD=ROOT/'assets/grimo/production/jill/tripo/smartmesh25k-v001'
E=ROOT/'docs/production/jill/evidence/smartmesh25k-v002'
o=bpy.data.objects['JILL_GEOMETRY_MASTER'];m=o.data;s=bpy.context.scene;s.frame_set(1)
with bpy.data.libraries.load(str(OLD/'jill-geometry-master.blend'),link=False) as (src,dst):dst.objects=['JILL_GEOMETRY_MASTER']
old=dst.objects[0];om=old.data
ref=bpy.data.collections.new('READ_ONLY_VERIFICATION_REFERENCE');s.collection.children.link(ref);ref.objects.link(old)
old.hide_render=True;old.hide_set(True);bpy.context.view_layer.update()
local=np.array([tuple(v.co) for v in m.vertices]);prev=np.array([tuple(v.co) for v in om.vertices]);delta=np.linalg.norm(local-prev,axis=1)
changed=np.where(delta>0)[0];edit=json.loads((E/'repair.json').read_text());allow=set(edit['changed_neutral_vertex_ids'])
def action_data(mesh):
    action=mesh.shape_keys.animation_data.action
    return [[fc.data_path,fc.array_index,[(tuple(pt.co),pt.interpolation) for pt in fc.keyframe_points]] for layer in action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
polyeq=[tuple(p.vertices) for p in m.polygons]==[tuple(p.vertices) for p in om.polygons]
expected=json.loads((E/'protected-inputs.json').read_text());now={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in expected}
mismatch=[p for p in expected if now[p]!=expected[p]]
saved=json.loads((E/'saved-gate-validation.json').read_text())
report={'candidate_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
 'protected_file_count':len(expected),'protected_hash_mismatches':mismatch,'retained_polygon_vertex_lists_exact':polyeq,
 'neutral_vertices_changed':len(changed),'changed_only_declared_local_vertices':set(changed)==allow,
 'outside_local_edit_max_delta':float(delta[[i for i in range(len(delta)) if i not in allow]].max()),
 'all_body_wings_leaves_tail_feet_neutral_vertices_exact':bool(np.all(delta[[i for i in range(len(delta)) if i not in allow]]==0)),
 'bounds_exact':bool(np.array_equal(local.min(0),prev.min(0)) and np.array_equal(local.max(0),prev.max(0))),
 'object_matrix_exact':o.matrix_world==old.matrix_world,
 'candidate_material_names':[x.name for x in m.materials], 'candidate_uv_layers':[x.name for x in m.uv_layers],
 'test_animation_timing_and_interpolation_exact':action_data(m)==action_data(om),
 'all_neutral_returns_exact':all(sample.get('neutral_delta',0)==0 for c in saved['cases'] for sample in c['samples']),
 'all_independence_samples_exact':all(sample['max_nontarget_displacement']==0 and sample['face_feet_max_displacement']==0 for c in saved['cases'] for sample in c['samples']),
 'sampled_max_nontarget_displacement':max(sample['max_nontarget_displacement'] for c in saved['cases'] for sample in c['samples']),
 'sampled_max_face_feet_displacement':max(sample['face_feet_max_displacement'] for c in saved['cases'] for sample in c['samples']),
 'sampled_independence_within_1e_7':all(sample['max_nontarget_displacement']<1e-7 and sample['face_feet_max_displacement']<1e-7 for c in saved['cases'] for sample in c['samples']),
 'no_new_sampled_degenerate_triangles':all(sample['new_degenerate_triangles']==0 for c in saved['cases'] for sample in c['samples']),
 'formal_rig_created':False,'formal_texture_created':False,'derived_exports_created':False,
 'note':'Preservation and sampled diagnostics do not approve appearance or Motion. No export needed before Human Geometry approval.'}
assert not mismatch and polyeq and report['changed_only_declared_local_vertices'] and report['all_neutral_returns_exact']
assert report['outside_local_edit_max_delta']==0 and report['bounds_exact'] and report['test_animation_timing_and_interpolation_exact']
(E/'preservation-validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report),flush=True)
