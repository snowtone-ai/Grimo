"""Targeted saved-asset verification; no render, scene mutation or app tests.

Optional --baseline-records is the pre-edit local object-record JSON. Published
validation records its checksum and exact changed/frozen object lists.
"""
import argparse
import hashlib
import json
import runpy
import sys
from pathlib import Path

import bpy
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
BUILD=runpy.run_path(str(ROOT/'scripts/blender/build-carol-v008.py'))


def records():
    result={}
    for o in bpy.context.scene.objects:
        if o.type not in {'MESH','CURVE'}: continue
        result[o.name]=dict(type=o.type,matrix=[list(r) for r in o.matrix_world],
            vertices=[list(v.co) for v in o.data.vertices] if o.type=='MESH' else [[list(p.co) for p in s.points] for s in o.data.splines],
            faces=[list(p.vertices) for p in o.data.polygons] if o.type=='MESH' else [],
            materials=[m.name for m in o.data.materials],modifiers=[(m.type,getattr(m,'levels',None)) for m in o.modifiers],hidden=o.hide_render)
    return json.loads(json.dumps(result))


def scene_records():
    result={}
    for o in bpy.context.scene.objects:
        if o.type in {'MESH','CURVE'}: continue
        result[o.name]=dict(type=o.type,matrix=[list(r) for r in o.matrix_world],
            hidden=o.hide_render,
            ortho_scale=o.data.ortho_scale if o.type=='CAMERA' else None,
            light_energy=o.data.energy if o.type=='LIGHT' else None,
            light_size=o.data.size if o.type=='LIGHT' else None,
            registration={k:o.get(k) for k in ('h','ground','origin') if k in o})
    return json.loads(json.dumps(result))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--baseline-records',type=Path)
    p.add_argument('--baseline-scene',type=Path)
    p.add_argument('--design-measurements',type=Path)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    scene=bpy.context.scene
    revision=scene['selected_revision']
    output=ROOT/f'tmp-carol-v008/revision-{revision}'
    m=json.loads((output/'measurements.json').read_text())
    assert BUILD['geometry_digest']()==m['geometry_digest']
    if args.design_measurements:
        assert json.loads(args.design_measurements.read_text())['geometry_digest']==m['geometry_digest']
    assert scene['saved_pose']=='NEUTRAL'
    assert len(bpy.data.actions)==0
    assert not any(o.type=='ARMATURE' or o.animation_data for o in scene.objects)
    assert not any(mesh.shape_keys or mesh.animation_data for mesh in bpy.data.meshes)
    assert not any(mat.animation_data or (mat.node_tree and mat.node_tree.animation_data) for mat in bpy.data.materials)
    assert not any(mod.type in {'BOOLEAN','REMESH','ARMATURE'} for o in scene.objects for mod in o.modifiers)
    assert not any(m['view_geometry_digests'][v]!=m['geometry_digest'] for v in ['front','side'])
    for name,digest in BUILD['REFERENCE_HASHES'].items():
        assert hashlib.sha256((BUILD['REFERENCE']/name).read_bytes()).hexdigest()==digest
    assert m['reference_registration']==BUILD['REGISTRATION']
    expected={'HEAD_CAGE','TORSO_CAGE','SHORT_NECK_SOCKET','SKIN_TAIL_CORE','MOUTH_closed','PHILTRUM','NOSE'}
    for side in ['L','R']:
        expected.update(prefix+side for prefix in ['EYE_','EYELID_','EAR_','FORE_','HIND_','HOOF_FORE_','HOOF_HIND_'])
    current=records()
    assert set(current)==expected
    assert not any(record['hidden'] for record in current.values())
    torso=m['human_fit']['torso']['maximum_evaluated_width_H']
    assert .598<=torso<=.600, torso
    checks={}
    for row,x,y in [('FORE',.390,.145),('HIND',.920,.245)]:
        for side,sign in [('L',1),('R',-1)]:
            support=bpy.data.objects[f'DEBUG_{row}_SUPPORT_{side}'].location
            assert max(abs(support[i]-[x,sign*y,0][i]) for i in range(3))<1e-7
            b=m['meshes'][f'HOOF_{row}_{side}']
            width=b['max'][1]-b['min'][1]; height=b['max'][2]-b['min'][2]
            assert abs(width/.219-1)<=.02
            assert abs(height/.111-1)<=.02
            assert abs(b['min'][2])<.0001
            hoof=bpy.data.objects[f'HOOF_{row}_{side}']
            assert hoof['toe_lobe_count']==3 and hoof['cleft_count']==2
            neighbors={v.index:set() for v in hoof.data.vertices}
            for edge in hoof.data.edges:
                a,c=edge.vertices
                neighbors[a].add(c);neighbors[c].add(a)
            reached={0};frontier=[0]
            while frontier:
                for index in neighbors[frontier.pop()]-reached:
                    reached.add(index);frontier.append(index)
            assert len(reached)==len(neighbors), 'Hoof mesh is disconnected'
            checks[f'HOOF_{row}_{side}']=dict(width_H=width,height_H=height,
                min_Z_H=b['min'][2],single_connected_mesh=True,continuous_sole=True)
    for side,sign in [('L',1),('R',-1)]:
        b=m['meshes']['EYE_'+side]
        width=b['max'][1]-b['min'][1];height=b['max'][2]-b['min'][2]
        center=(b['max'][1]+b['min'][1])/2
        assert abs(width-.137)<1e-6 and abs(height-.149)<1e-6
        assert abs(center-sign*.162)<1e-6
        checks['EYE_'+side]=dict(width_H=width,height_H=height,center_Y_H=center,
                                average_normal=list(sum((f.normal for f in bpy.data.objects['EYE_'+side].data.polygons),__import__('mathutils').Vector())/len(bpy.data.objects['EYE_'+side].data.polygons)))
    assert all(case['surface_intersection_pairs']>0 for case in m['attachment_diagnostics']['tail_pivot_probes'].values())
    result=dict(selected_revision=revision,reloaded_neutral_digest=m['geometry_digest'],
        clean_rebuild_matches_design=bool(args.design_measurements),
        reference_hashes_unchanged=True,registration_unchanged=True,
        numerical_checks=checks,exact_renderable_inventory=sorted(expected),
        hidden_alternate_body=False,view_specific_geometry=False,production_rig=False,animation=False,keyframes=False,
        boolean_or_remesh=False,neutral_saved=True,
        generator_sha256=hashlib.sha256((ROOT/'scripts/blender/build-carol-v008.py').read_bytes()).hexdigest(),
        packed_pigment_sha256=hashlib.sha256(np.array(bpy.data.images['EYE pigment diagnostic packed'].pixels[:],dtype=np.float32).tobytes()).hexdigest())
    if args.baseline_records:
        previous=json.loads(args.baseline_records.read_text())
        def geometric_record(record):
            result=dict(record)
            # Blender may enumerate identical UV-sphere polygons in a different
            # order on rebuild; compare connectivity, not polygon enumeration.
            result['faces']=sorted(tuple(sorted(face)) for face in record['faces'])
            return result
        changed=sorted(name for name in set(current)&set(previous)
                       if geometric_record(current[name])!=geometric_record(previous[name]))
        frozen=sorted(name for name in set(current)&set(previous)
                      if geometric_record(current[name])==geometric_record(previous[name]))
        expected_frozen={'NOSE','SKIN_TAIL_CORE','SHORT_NECK_SOCKET',
                         'FORE_L','FORE_R','HIND_L','HIND_R'}
        assert expected_frozen<=set(frozen), sorted(expected_frozen-set(frozen))
        assert {'TORSO_CAGE','HEAD_CAGE','EAR_L','EAR_R',
                'HOOF_FORE_L','HOOF_FORE_R','HOOF_HIND_L','HOOF_HIND_R'}<=set(changed)
        result.update(baseline_records_sha256=hashlib.sha256(args.baseline_records.read_bytes()).hexdigest(),
                      changed_objects=changed,frozen_objects=frozen,
                      removed_objects=sorted(set(previous)-set(current)),added_objects=sorted(set(current)-set(previous)))
    if args.baseline_scene:
        assert scene_records()==json.loads(args.baseline_scene.read_text())
        result['camera_light_landmark_reference_records_unchanged']=True
        result['baseline_scene_sha256']=hashlib.sha256(args.baseline_scene.read_bytes()).hexdigest()
    baseline_validation=ROOT/'docs/production/carol/evidence/reconstruction-v008/baseline-revision-12/validation.json'
    assert result['packed_pigment_sha256']==json.loads(baseline_validation.read_text())['packed_pigment_sha256']
    result['packed_pigment_unchanged']=True
    (output/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
