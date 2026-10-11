"""Measured source integrity, face occlusion, support/contact and interchange."""
import bpy,sys,json,math,hashlib,importlib
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
b=importlib.import_module('build-shushu-geometry-v002');a=importlib.import_module('shushu-candidate-b-audit')

def init(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    b.character=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Shushu_')]
    b.parts={o['part']:o for o in b.character if 'part' in o}
    b.eyes={s:bpy.data.objects['Shushu_Eye.'+s] for s in ['L','R']}
    b.rig=bpy.data.objects['Shushu_DeformationRig'];b.proxy=bpy.data.objects['Reachable_Holding_Proxy'];b.cam=bpy.context.scene.camera

def tree(o):
    v,t=b.evaluated(o);return BVHTree.FromPolygons([Vector(p) for p in v],t.tolist(),all_triangles=True)

def error(x,y):
    def near(x,y):
        k=KDTree(len(y))
        for i,p in enumerate(y):k.insert(Vector(p),i)
        k.balance();return max(k.find(Vector(p))[2] for p in x)
    return max(near(x,y),near(y,x))

def surface_metrics(o):
    v,t=b.evaluated(o);vol=float(abs(np.einsum('ij,ij->i',v[t[:,0]],np.cross(v[t[:,1]],v[t[:,2]])).sum()/6))
    return dict(minimum_z=float(v[:,2].min()),volume=vol,ground_samples=int((v[:,2]<.003).sum()),bounds=[v.min(0).tolist(),v.max(0).tolist()])

def main():
    report={'source_integrity':{},'face_visibility':{},'states':{},'contacts':{},'topology':{}}
    init(b.ASSET)
    source_manifest=json.loads((b.ROOT/'docs/production/shushu/evidence/candidate-b-8481/input-manifest.json').read_text())
    refs=source_manifest['references']
    for line in (b.ROOT/'assets/grimo/production/shushu/image-reference/reference-pack-v001/sha256.txt').read_text(encoding='utf-8-sig').splitlines():
        if line.strip():
            digest,path=line.split('  ',1)
            refs.append(dict(path=Path(path).relative_to(b.ROOT).as_posix(),sha256=digest.lower()))
    for row in source_manifest['files']+refs:
        if row['path'].endswith(('.png','.fbx','.glb')):
            h=hashlib.sha256((b.ROOT/row['path']).read_bytes()).hexdigest()
            assert h==row['sha256'];report['source_integrity'][row['path']]=h
    b.reset();neutral={o.name:b.evaluated(o)[0] for o in b.character}
    for o in b.character:
        edges={}
        for p in o.data.polygons:
            for e in p.edge_keys:edges[tuple(sorted(e))]=edges.get(tuple(sorted(e)),0)+1
        report['topology'][o.name]={'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),
            'quads':sum(len(p.vertices)==4 for p in o.data.polygons),'boundary_edges':sum(x==1 for x in edges.values()),
            'nonmanifold_edges':sum(x>2 for x in edges.values()),'uv_layers':len(o.data.uv_layers),'vertex_colors':len(o.data.color_attributes)}
    for name in ['neutral','half','closed','smile','left-closed','right-closed','gaze-blink']:
        b.state(name);h=tree(b.parts['Head']);rows={}
        for s in ['L','R']:
            v,t=b.evaluated(b.eyes[s]);exposed=0
            for p in v:
                hit=h.ray_cast(Vector((p[0],-1,p[2])),Vector((0,1,0)))[0]
                exposed+=hit is None or hit.y>p[1]+2e-5
            rows[s]={'exposed_eye_samples':int(exposed),'total_eye_samples':len(v)}
        report['face_visibility'][name]=rows
    for name in ['neutral','rest','seat-0.25','seat-0.5','seat-0.75','seat','offer','groom','chest-groom','head-turn','combined','pressure']:
        b.state(name);report['states'][name]={part:surface_metrics(o) for part,o in b.parts.items()}
        for part in ['Leg.L','Leg.R']:
            o=b.parts[part];v,t=b.evaluated(o);n=neutral[o.name]
            ids=[x.index for x in o.data.vertices if x.co.z<.0121]
            report['states'][name][part]['sole_max_displacement']=float(np.linalg.norm(v[ids]-n[ids],axis=1).max())
            edges=np.array([e.vertices[:] for e in o.data.edges]);nlen=np.linalg.norm(n[edges[:,0]]-n[edges[:,1]],axis=1)
            ratio=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1)/np.maximum(nlen,1e-10)
            report['states'][name][part]['edge_ratio_min_max']=[float(ratio.min()),float(ratio.max())]
    for name in ['hold','hold-touch']:
        b.state(name);pv,pt=b.evaluated(b.proxy);rows={}
        for part in ['Torso','Head','Paw.L','Paw.R']:
            t=tree(b.parts[part]);ds=[]
            for v in pv:
                p,n,_,d=t.find_nearest(Vector(v));ds.append(d if (Vector(v)-p).dot(n)>=0 else -d)
            rows[part]={'minimum_signed_clearance':min(ds),'minimum_absolute_gap':min(abs(x) for x in ds),'penetrating_samples_beyond_1e-4':sum(x<-.0001 for x in ds)}
        report['contacts'][name]=rows
    b.state('groom')
    cheek=tree(b.parts['Head']);paw,_=b.evaluated(b.parts['Paw.L']);ds=[cheek.find_nearest(Vector(p))[3] for p in paw]
    report['self_groom_min_surface_gap']=float(min(ds))
    signed=[]
    for q in paw:
        p,n,_,d=cheek.find_nearest(Vector(q));signed.append(d if (Vector(q)-p).dot(n)>=0 else -d)
    report['self_groom_signed_clearance_min']=min(signed)
    report['self_groom_penetrating_samples_beyond_1e-3']=sum(x<-.001 for x in signed)
    bone=b.rig.data.bones['Paw.L'];direction=(bone.tail_local-bone.head_local).normalized()
    distal=[v.index for v in b.parts['Paw.L'].data.vertices if (v.co-bone.head_local).dot(direction)>.135]
    report['self_groom_distal_signed_min']=min(signed[i] for i in distal)
    report['self_groom_distal_penetrating_samples_beyond_1e-3']=sum(signed[i]<-.001 for i in distal)
    b.state('chest-groom');chest=tree(b.parts['Torso']);paw,_=b.evaluated(b.parts['Paw.L'])
    report['chest_groom_min_surface_gap']=float(min(chest.find_nearest(Vector(p))[3] for p in paw))
    report['paw_free_surface_clearance']={}
    for name in ['neutral','offer','groom','chest-groom','hold','hold-touch']:
        b.state(name);v,_=b.evaluated(b.parts['Paw.L']);rows={}
        for part in ['Head','Torso']:
            target=tree(b.parts[part]);ds=[]
            for i in distal:
                p,n,_,d=target.find_nearest(Vector(v[i]));ds.append(d if (Vector(v[i])-p).dot(n)>=0 else -d)
            rows[part]={'minimum_signed_clearance':min(ds),'penetrating_samples_beyond_1e-3':sum(x<-.001 for x in ds)}
        report['paw_free_surface_clearance'][name]=rows
    report['paw_right_free_surface_clearance']={}
    bone=b.rig.data.bones['Paw.R'];direction=(bone.tail_local-bone.head_local).normalized()
    right_ids=[v.index for v in b.parts['Paw.R'].data.vertices if (v.co-bone.head_local).dot(direction)>.135]
    for name in ['hold','hold-touch']:
        b.state(name);v,_=b.evaluated(b.parts['Paw.R']);rows={}
        for part in ['Head','Torso']:
            target=tree(b.parts[part]);ds=[]
            for i in right_ids:
                p,n,_,d=target.find_nearest(Vector(v[i]));ds.append(d if (Vector(v[i])-p).dot(n)>=0 else -d)
            rows[part]={'minimum_signed_clearance':min(ds),'penetrating_samples_beyond_1e-3':sum(x<-.001 for x in ds)}
        report['paw_right_free_surface_clearance'][name]=rows
    b.state('offer');report['independent_paw_opposite_error']=float(np.linalg.norm(b.evaluated(b.parts['Paw.R'])[0]-neutral['Shushu_Paw.R'],axis=1).max())
    report['seated_support_sweep']={}
    for s in np.linspace(0,1,41):
        b.state('seat-'+str(s));report['seated_support_sweep'][str(s)]={p:surface_metrics(b.parts[p]) for p in ['Leg.L','Leg.R','Torso']}
    b.state('mouth-open');h=tree(b.parts['Head']);center_z=.610;visible=0;samples=0
    for ix in range(-3,4):
        for iz in range(-3,4):
            x=ix*.001;z=center_z+iz*.001
            if x*x+(z-center_z)**2>.003**2:continue
            samples+=1;hit=h.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))[0]
            visible+=hit is None or hit.y>b.front_y(x,z)+.003
    report['mouth_reception_probe']={'pellet_radius':.003,'position':[0,b.front_y(0,center_z),center_z],
        'head_aperture_clear_samples':int(visible),'total_samples':samples,'scope':'Head aperture only; no full Food animation/consumption or Tripo compatibility claim.'}
    b.state('pressure');report['protected_eye_pressure_displacement']=max(float(np.linalg.norm(b.evaluated(o)[0]-neutral[o.name],axis=1).max()) for o in b.eyes.values())
    report['protected_feature_pressure_displacement']={o.name:float(np.linalg.norm(b.evaluated(o)[0]-neutral[o.name],axis=1).max())
        for o in b.character if 'part' not in o}
    b.reset();report['recovery_max_error']=max(float(np.linalg.norm(b.evaluated(o)[0]-neutral[o.name],axis=1).max()) for o in b.character)
    print('LOCAL_FACE',report['face_visibility'],flush=True)
    print('LOCAL_SEAT',{k:(v['minimum_z'],v['ground_samples']) for k,v in report['states']['seat'].items()},flush=True)
    # Actual static GLB/FBX reimports in fresh scenes, with count/bounds and surfaces.
    export_names=[o.name for o in b.character]
    for ext in ['glb','fbx']:
        bpy.ops.wm.read_factory_settings(use_empty=True);path=b.STATIC.with_suffix('.'+ext)
        if ext=='glb':bpy.ops.import_scene.gltf(filepath=str(path))
        else:bpy.ops.import_scene.fbx(filepath=str(path),use_custom_props=True)
        actual=[o for o in bpy.data.objects if o.type=='MESH'];rows={}
        for name in export_names:
            o=next(o for o in actual if o.get('production_id',o.name)==name or o.name==name or o.name==name+'.001')
            v,t=b.evaluated(o);rows[name]={'bidirectional_error':error(neutral[name],v),'polygons':len(o.data.polygons),'vertices':len(o.data.vertices)}
        report['static_'+ext]={'path':path.relative_to(b.ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'mesh_count':len(actual),'armatures':sum(o.type=='ARMATURE' for o in bpy.data.objects),
            'shape_keys':sum(bool(o.data.shape_keys) for o in actual),'animation_actions':len(bpy.data.actions),
            'uv_layers':sum(len(o.data.uv_layers) for o in actual),'worst_error':max(x['bidirectional_error'] for x in rows.values()),'meshes':rows}
        report['static_'+ext].update(material_slots=sum(len(o.data.materials) for o in actual),vertex_colors=sum(len(o.data.color_attributes) for o in actual))
        if ext=='glb':
            doc,_=a.glb(path);report['static_glb'].update(skins=len(doc.get('skins',[])),animations=len(doc.get('animations',[])),textures=len(doc.get('textures',[])),
                materials=len(doc.get('materials',[])),morph_targets=sum(len(p.get('targets',[])) for m in doc['meshes'] for p in m['primitives']))
    init(b.PROOF);manifest=json.loads((b.OUT/'build-manifest.json').read_text());samples=list(map(int,manifest['animation_samples']))
    expected={}
    for frame in samples:
        bpy.context.scene.frame_set(frame);expected[frame]={o.name:b.evaluated(o)[0] for o in b.character}
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(b.GLB))
    actual=[o for o in bpy.data.objects if o.type=='MESH'];rt={}
    for frame in samples:
        bpy.context.scene.frame_set(frame);err=[]
        for name,v in expected[frame].items():
            o=next(o for o in actual if o.get('production_id',o.name)==name or o.name==name or o.name==name+'.001')
            err.append(error(v,b.evaluated(o)[0]))
        rt[str(frame)]=max(err)
    report['proof_roundtrip']={'sample_count':len(samples),'per_frame':rt,'worst_error':max(rt.values()),'tolerance':2e-5}
    report['verdict']={'face_closure':all(report['face_visibility']['closed'][s]['exposed_eye_samples']==0 for s in ['L','R']),
        'static_roundtrip':all(report['static_'+ext]['worst_error']<2e-5 for ext in ['glb','fbx']),
        'proof_roundtrip':report['proof_roundtrip']['worst_error']<2e-5,
        'seated_ground':all(row['minimum_z']>=-1e-4 for row in report['states']['seat'].values()),
        'seated_support_sweep':all(abs(row['minimum_z']-.001)<2e-5 and row['ground_samples']>0 for state in report['seated_support_sweep'].values() for part,row in state.items() if part.startswith('Leg')),
        'self_contact':all(row['penetrating_samples_beyond_1e-3']==0 for name in ['groom','chest-groom'] for row in report['paw_free_surface_clearance'][name].values()),
        'offer_hold_free_paw':all(row['penetrating_samples_beyond_1e-3']==0 for name in ['offer','hold','hold-touch'] for row in report['paw_free_surface_clearance'][name].values()),
        'holding_fixture':all(row['penetrating_samples_beyond_1e-4']==0 for state in report['contacts'].values() for row in state.values()),
        'right_holding_free_paw':all(row['penetrating_samples_beyond_1e-3']==0 for state in report['paw_right_free_surface_clearance'].values() for row in state.values()),
        'mouth_clearance':report['mouth_reception_probe']['head_aperture_clear_samples']==report['mouth_reception_probe']['total_samples'],
        'human_geometry':'PENDING','tripo_compatibility':'UNKNOWN'}
    (b.OUT/'focused-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    assert all(v is True for v in report['verdict'].values() if isinstance(v,bool)),report['verdict']
    print('VERDICT',report['verdict']);print('FACE',report['face_visibility']);print('SEAT',{k:(v['minimum_z'],v['ground_samples']) for k,v in report['states']['seat'].items()});print('CONTACTS',report['contacts']);print('ROUNDTRIP',report['proof_roundtrip']['worst_error'])

if __name__=='__main__':main()
