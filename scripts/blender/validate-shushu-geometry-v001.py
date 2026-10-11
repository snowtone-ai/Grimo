"""Focused occlusion/support/contact and GLB round-trip validation, Blender 5.2."""
import bpy, sys, json, math, hashlib, importlib
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
build=importlib.import_module('build-shushu-geometry-v001')
audit=importlib.import_module('shushu-candidate-b-audit')
ROOT,OUT,GLB=build.ROOT,build.OUT,build.GLB

def tree_for(o):
    v,t=build.evaluated(o);return BVHTree.FromPolygons([Vector(p) for p in v],t.tolist(),all_triangles=True)

def nearest_error(a,b):
    tree=KDTree(len(b))
    for i,p in enumerate(b):tree.insert(Vector(p),i)
    tree.balance();return max(tree.find(Vector(p))[2] for p in a)

def main():
    bpy.ops.wm.open_mainfile(filepath=str(build.ASSET))
    scene=bpy.context.scene
    character=[o for o in bpy.data.objects if o.name.startswith('Shushu_') and o.type=='MESH']
    samples=[1,9,13,19,25,31,37,43,61,73,85,91,99,105,111,120]
    expected={}
    for frame in samples:
        scene.frame_set(frame);expected[frame]={o.name:build.evaluated(o)[0] for o in character}
    scene.frame_set(1)
    report={'samples':samples,'coordinates':'Blender Z up/front -Y -> GLB Y up/front +Z; normalized character height about 1, scene unit scale 1',
            'source_integrity':{},'face_visibility':{},'contacts':{},'topology':{}}
    report['animated_source_amplitudes']={str(frame):max(float(np.linalg.norm(verts-expected[1][name],axis=1).max()) for name,verts in expected[frame].items()) for frame in samples}
    assert report['animated_source_amplitudes']['13']>.05
    assert report['animated_source_amplitudes']['73']>.06
    manifest=json.loads((ROOT/'docs/production/shushu/evidence/candidate-b-8481/input-manifest.json').read_text(encoding='utf-8'))
    for row in manifest['files']:
        if row['path'].endswith(('.fbx','.glb')):
            actual=hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest();assert actual==row['sha256']
            report['source_integrity'][row['path']]=actual
    report['canonical_reference_hashes_unchanged']=all(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'] for row in manifest['references'])
    assert report['canonical_reference_hashes_unchanged']
    build.character=character;build.rig=bpy.data.objects['Shushu_DeformationRig'];build.proxy=bpy.data.objects['Reachable_Holding_Proxy']
    build.head=bpy.data.objects['Shushu_Head'];build.parts={o['part']:o for o in character if 'part' in o}
    build.cam=scene.camera
    for o in character:
        if o.data.shape_keys:o.data.shape_keys.animation_data_clear()
    build.rig.animation_data_clear()
    # Front occlusion samples test actual surface, not shape-key labels.
    for state in ['neutral','half','closed','left-closed','right-closed','gaze-blink']:
        build.apply_state(state);headtree=tree_for(build.head);rows={}
        for side in ['L','R']:
            eye=bpy.data.objects['Shushu_Eye.'+side];v,t=build.evaluated(eye)
            visible=[]
            for p in v:
                hit=headtree.ray_cast(Vector((p[0],-1,p[2])),Vector((0,1,0)))[0]
                visible.append(hit is None or hit.y>p[1]+2e-5)
            rows[side]={'exposed_eye_samples':int(sum(visible)),'total_eye_samples':len(v)}
        report['face_visibility'][state]=rows
    # Contact measured on whole evaluated surfaces. Signed distance from nearest surface normal.
    for state in ['hold','hold-touch']:
        build.apply_state(state);rows={}
        propv,propt=build.evaluated(build.proxy)
        for part in ['Torso','Head','Paw.L','Paw.R']:
            tree=tree_for(build.parts[part]);distances=[]
            for vertex in propv:
                point,normal,idx,d=tree.find_nearest(Vector(vertex))
                distances.append(d if (Vector(vertex)-point).dot(normal)>=0 else -d)
            rows[part]={'prop_vertex_signed_clearance_min':float(min(distances)),
                        'minimum_absolute_surface_gap':float(min(abs(d) for d in distances)),
                        'penetrating_samples_beyond_1e-4':sum(d<-.0001 for d in distances)}
        report['contacts'][state]=rows
    build.reset()
    for part in ['Head','Torso','Leg.L','Leg.R','Paw.L','Paw.R']:
        o=build.parts[part];edges={}
        for p in o.data.polygons:
            for e in p.edge_keys:edges[tuple(sorted(e))]=edges.get(tuple(sorted(e)),0)+1
        report['topology'][part]={'boundary_edges':sum(c==1 for c in edges.values()),'nonmanifold_edges':sum(c>2 for c in edges.values())}
    # Geometry-only artifact: evaluated neutral copies, no skin/morph/animation ownership.
    neutral=[]
    for o in character:
        ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
        m=bpy.data.meshes.new_from_object(ev);copy=bpy.data.objects.new(o.name+'_GeometryOnly',m)
        scene.collection.objects.link(copy);copy.matrix_world=o.matrix_world;neutral.append(copy)
    bpy.ops.object.select_all(action='DESELECT')
    for o in neutral:o.select_set(True)
    static=GLB.with_name('shushu-geometry-v001-static.glb')
    bpy.ops.export_scene.gltf(filepath=str(static),export_format='GLB',use_selection=True,export_animations=False,export_skins=False,export_morph=False,export_yup=True)
    for o in neutral:bpy.data.objects.remove(o,do_unlink=True)
    doc,binary=audit.glb(GLB)
    report['glb']={'sha256':hashlib.sha256(GLB.read_bytes()).hexdigest(),'nodes':len(doc['nodes']),
                   'skins':len(doc.get('skins',[])),'meshes':len(doc['meshes']),'animations':len(doc.get('animations',[])),
                   'joints':[[doc['nodes'][j]['name'] for j in skin['joints']] for skin in doc.get('skins',[])],
                   'channels':sum(len(a['channels']) for a in doc.get('animations',[])),
                   'morph_targets':{m['name']:len(m['primitives'][0].get('targets',[])) for m in doc['meshes']}}
    weight_error=0;max_influences=0
    for m in doc['meshes']:
        for p in m['primitives']:
            if 'WEIGHTS_0' in p['attributes']:
                w=audit.accessor(doc,binary,p['attributes']['WEIGHTS_0'])
                if w.dtype.kind!='f':w=w/(255 if w.dtype.itemsize==1 else 65535)
                weight_error=max(weight_error,float(np.abs(w.sum(1)-1).max()));max_influences=max(max_influences,int((w>0).sum(1).max()))
    report['glb']['weight_sum_max_error']=weight_error;report['glb']['max_influences']=max_influences
    (OUT/'focused-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    # Fresh scene ensures Blender constraints or source armatures cannot contribute.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
    bpy.ops.import_scene.gltf(filepath=str(GLB))
    actual={o.get('production_id',o.name):o for o in bpy.data.objects if o.type=='MESH'}
    print('IMPORTED_MESH_NAMES',list(actual))
    mesh_names={n['name']:doc['meshes'][n['mesh']]['name'] for n in doc['nodes'] if 'mesh' in n}
    roundtrip={};worst=0
    for frame in samples:
        bpy.context.scene.frame_set(frame);rows={}
        for name,verts in expected[frame].items():
            o=actual.get(name) or actual.get(name+'_Mesh')
            if o is None:o=actual.get(mesh_names.get(name,''))
            if o is None:o=next((o for o in actual.values() if o.parent and o.parent.name==name),None)
            if o is None:o=next((o for n,o in actual.items() if n.startswith(name)),None)
            assert o is not None,name
            v,t=build.evaluated(o);err=max(nearest_error(verts,v),nearest_error(v,verts))
            rows[name]=err;worst=max(worst,err)
        roundtrip[str(frame)]={'max_bidirectional_vertex_error':max(rows.values())}
    report['roundtrip']={'per_frame':roundtrip,'worst_error':worst,'pass_tolerance':2e-5,'pass':worst<2e-5}
    # One imported animated render exposes animation sampling failures visibly.
    bpy.context.scene.frame_set(73);build.cam=build.setup_render()
    build.render('roundtrip-rest',(1,-2,.08))
    sdoc,_=audit.glb(static)
    report['geometry_only']={'path':static.relative_to(ROOT).as_posix(),'skins':len(sdoc.get('skins',[])),
                             'animations':len(sdoc.get('animations',[])),
                             'morph_targets':sum(len(p.get('targets',[])) for m in sdoc['meshes'] for p in m['primitives'])}
    (OUT/'focused-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    # Fail reproducibly if the critical demonstrated capabilities regress.
    assert report['roundtrip']['pass'], report['roundtrip']
    for side in ['L','R']:
        assert report['face_visibility']['closed'][side]['exposed_eye_samples']==0
        assert report['face_visibility']['neutral'][side]['exposed_eye_samples']>0
    for state in ['hold','hold-touch']:
        assert all(row['penetrating_samples_beyond_1e-4']==0 for row in report['contacts'][state].values())
        for part in ['Paw.L','Paw.R']:
            assert report['contacts'][state][part]['minimum_absolute_surface_gap']<.0001
    assert all(row['nonmanifold_edges']==0 for row in report['topology'].values())
    measures=json.loads((OUT/'measurements.json').read_text())
    for part in ['Leg.L','Leg.R']:
        assert measures['states']['rest'][part]['minimum_z']>=0
        assert measures['states']['rest'][part]['sole_max_displacement']<1e-6
    assert measures['recovery_max_error']<1e-6
    assert max(measures['plush_feature_displacement'].values())<1e-6
    print('ROUNDTRIP',json.dumps(report['roundtrip']));print('CONTACTS',json.dumps(report['contacts']))
    print('FACE',json.dumps(report['face_visibility']));print('TOPOLOGY',json.dumps(report['topology']))

if __name__=='__main__':main()
