"""Bounded Carol local correction; source inspection, F1/F2, E1/E2 and final validation.

Run Blender --background --python this-file -- --stage inspect|face|ear|final.
All temporary renders and attempt blends live outside the repository.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
SOURCE_HEAD = '880b35506c0b085fdbb4081c1de6c3f9bdc4e58a'
SOURCE = ROOT/'assets/grimo/production/carol/blender/carol-ear-production-v002.blend'
OUTPUT = SOURCE.with_name('carol-face-ear-production-v003.blend')
OUT = ROOT/'docs/production/carol/evidence/face-ear-production-v003'
TMP = Path(tempfile.gettempdir())/'carol-face-ear-v003'
TMP.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location('ear_v002', Path(__file__).with_name('build-carol-ear-production-v002.py'))
ear = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ear)
ear.TMP = TMP
FACE = {'CENTRAL_CHASSIS', 'NOSE', 'MOUTH_closed', 'PHILTRUM'}
FACE_VISIBLE = FACE | {'EYE_L', 'EYE_R', 'EYELID_L', 'EYELID_R'}
# E1: move breadth from distal wedge into middle, then progressively taper.
# Root 0/.014/.040 and distal endpoint are copied from v002 without edits.
E1_STATIONS = ear.STATIONS[:3] + [
    (.085, .033, -.136, .047, .035, .004, -.061),
    (.145, .004, -.180, .076, .054, .016, -.102),
    (.210, -.028, -.212, .086, .064, .040, -.117),
    (.270, -.059, -.218, .074, .052, .046, -.114),
    (.315, -.078, -.207, .061, .040, .034, -.120),
    (.345, -.091, -.192, .053, .034, .019, -.166),
] + ear.STATIONS[9:]
E2_STATIONS = ear.STATIONS[:3] + [
    (.085, .033, -.136, .047, .035, .003, -.061),
    (.145, .004, -.180, .074, .053, .010, -.102),
    (.210, -.028, -.212, .079, .054, .014, -.117),
    (.270, -.059, -.218, .064, .043, .015, -.114),
    (.315, -.078, -.207, .051, .033, .010, -.120),
    (.345, -.091, -.192, .047, .031, .008, -.166),
] + ear.STATIONS[9:]

def ear_renders(prefix):
    render_setup()
    center=ear.world((0,.19,-.074),1)
    front=Vector((-math.cos(ear.SWEEP),math.sin(ear.SWEEP),0))
    side=Vector((math.sin(ear.SWEEP),math.cos(ear.SWEEP),0))
    for label,d in [('front',front*4),('side',-side*4),('top',Vector((0,0,4))),('3q',-side*2+front*3+Vector((0,0,.7)))]:
        ear.render(prefix+'-ear-'+label,d,center,.49,{'EAR_L'},size=(720,720),roll=-math.pi/2-ear.SWEEP if label=='top' else 0)

def apply_ear(stations):
    ear.STATIONS=stations
    vertices,faces,mats=ear.local_cage()
    for suffix,sign in [('L',1),('R',-1)]:
        o=bpy.data.objects['EAR_'+suffix]
        assert len(o.data.vertices)==192
        for p,v in zip(o.data.vertices,vertices):p.co=ear.world(v,sign)
        for p,v in zip(o.data.shape_keys.key_blocks['Basis'].data,vertices):p.co=ear.world(v,sign)
        for name,lift,turn in [('TEST lift',12,0),('TEST droop',-14,0),('TEST attention flick',5,12)]:
            key=o.data.shape_keys.key_blocks[name];key.value=0
            for p,v in zip(key.data,ear.posed_local(vertices,lift,turn)):p.co=ear.world(v,sign)
        o.data.update()
    bpy.context.view_layer.update()

def ear_attempt(attempt):
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    frozen={o.name:ear.snapshot(o) for o in bpy.data.objects if o.name not in ear.EARS}
    stations=E1_STATIONS if attempt==1 else E2_STATIONS
    apply_ear(stations)
    assert all(ear.snapshot(bpy.data.objects[n])==v for n,v in frozen.items())
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(TMP/f'E{attempt}.blend'))
    write(TMP/f'E{attempt}.json',dict(attempt=f'E{attempt}',stations=stations,non_ear_objects_equal=True,changed_objects=['EAR_L','EAR_R']))
    ear_renders(f'E{attempt}')

def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')

def coords(o):
    return [list(v.co) for v in o.data.vertices] if o.type == 'MESH' else []

def topology(o):
    bm=bmesh.new(); bm.from_mesh(o.data)
    seen=set(); components=0
    for v in bm.verts:
        if v in seen: continue
        components+=1; stack=[v]
        while stack:
            v=stack.pop()
            if v in seen: continue
            seen.add(v); stack.extend(e.other_vert(v) for e in v.link_edges)
    result=dict(vertices=len(bm.verts),edges=len(bm.edges),faces=len(bm.faces),
                quads=sum(len(f.verts)==4 for f in bm.faces),components=components,
                nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),
                euler=len(bm.verts)-len(bm.edges)+len(bm.faces),
                connectivity_sha256=hashlib.sha256(json.dumps([list(p.vertices) for p in o.data.polygons]).encode()).hexdigest())
    bm.free(); return result

def tree(o):
    bpy.context.view_layer.update()
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return BVHTree.FromPolygons([ev.matrix_world@v.co for v in ev.data.vertices], [list(p.vertices) for p in ev.data.polygons])

def sample(t,y,z):
    hit=t.ray_cast(Vector((-2,y,z)),Vector((1,0,0)))
    assert hit[0] is not None, (y,z)
    return hit[0].x

def eye_seating(old,new):
    result={}
    for name in ['EYE_L','EYE_R','EYELID_L','EYELID_R']:
        o=bpy.data.objects[name];a=[];b=[]
        for v in o.data.vertices:
            p=o.matrix_world@v.co
            a.append(sample(old,p.y,p.z)-p.x);b.append(sample(new,p.y,p.z)-p.x)
        result[name]=dict(source_min_relief_H=min(a),candidate_min_relief_H=min(b),
            max_surface_advance_H=max(x-y for x,y in zip(a,b)),
            newly_covered_control_points=sum(x>=0 and y<0 for x,y in zip(a,b)),
            source_covered_control_points=sum(x<0 for x in a),candidate_covered_control_points=sum(x<0 for x in b))
    return result

def render_setup():
    scene=bpy.context.scene
    scene.render.use_compositing=False; scene.render.use_sequencer=False
    scene.render.engine='CYCLES'; scene.cycles.samples=32; scene.cycles.use_denoising=True
    scene.render.threads_mode='FIXED'; scene.render.threads=12

def face_renders(prefix):
    render_setup()
    for view,d in [('side',(0,-4,0)),('front',(-4,0,0)),('3q',(-3,-3,.65))]:
        ear.render(prefix+'-face-'+view,d,(.28,0,.47),.66,FACE_VISIBLE,size=(720,720))
    # Fixed source-reference registration, no candidate-dependent fitting.
    for view in ['side','front']:
        ref=bpy.data.objects['REFERENCE carol_skin_'+view+'.png']
        w,h=ref.data.size; ppH=ref['h']; ground=ref['ground']; origin=ref['origin']
        center=((w/2-origin)/ppH,0,(ground-h/2)/ppH) if view=='side' else (.5,-(w/2-origin)/ppH,(ground-h/2)/ppH)
        ear.render(prefix+'-skin-'+view,(0,-4,0) if view=='side' else (-4,0,0),center,max(w,h)/ppH,FACE_VISIBLE|{'EAR_L','EAR_R','FORE_L','FORE_R','HIND_L','HIND_R'}|{o.name for o in bpy.data.objects if o.name.startswith('HOOF_') or 'TAIL' in o.name},size=(w,h))

def inspect():
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    head=bpy.data.objects['CENTRAL_CHASSIS']; t=tree(head)
    records={o.name:ear.snapshot(o) for o in bpy.data.objects}
    data=dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(), objects=records,
              topology=topology(head),vertices=coords(head),
              groups={g.name:[v.index for v in head.data.vertices if any(x.group==g.index and x.weight>0 for x in v.groups)] for g in head.vertex_groups},
              references={o.name:dict(properties={k:o[k] for k in o.keys()},image_size=list(o.data.size),location=list(o.location)) for o in bpy.data.objects if o.type=='EMPTY' and o.empty_display_type=='IMAGE'},
              cameras={o.name:dict(location=list(o.location),rotation=list(o.rotation_euler),scale=o.data.ortho_scale) for o in bpy.data.objects if o.type=='CAMERA'},
              features={n:dict(type=bpy.data.objects[n].type,location=list(bpy.data.objects[n].location),bounds=[list(v) for v in bpy.data.objects[n].bound_box]) for n in FACE_VISIBLE if n!='CENTRAL_CHASSIS'},
              sagittal_samples=[dict(z=z,x=sample(t,0,z)) for z in [.30,.32,.34,.3542,.365,.374,.39,.41,.43,.45]])
    write(TMP/'source.json',data)
    print('SOURCE_INSPECT',json.dumps({k:v for k,v in data.items() if k not in ['vertices','objects','groups']}))
    print('LOCAL_FACE_VERTICES',json.dumps([(v.index,list(v.co),[head.vertex_groups[g.group].name for g in v.groups]) for v in head.data.vertices if abs(v.co.y)<.16 and .29<v.co.z<.44 and v.co.x<.2]))
    face_renders('source')

def face_attempt(attempt):
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    baseline={o.name:ear.snapshot(o) for o in bpy.data.objects}
    head=bpy.data.objects['CENTRAL_CHASSIS']; before=coords(head); old=tree(head)
    group=head.vertex_groups['FACE'].index
    weights={}
    for v in head.data.vertices:
        x,y,z=v.co
        if not any(g.group==group and g.weight>0 for g in v.groups):continue
        if x>=.20 or abs(y)>=.084 or not .31<z<.43:continue
        if attempt==2 and abs(y)>1e-8:continue
        # Compact smooth field, narrower than inner eyelid boundary (.084595 H).
        w=(1-(y/.084)**2)**2 * (1-((z-.367)/.063)**2)**2
        weights[v.index]=w
    # F2 narrows the same hypothesis after F1's evaluated field reached eye rims.
    peak=.025 if attempt==1 else .020
    for i,w in weights.items():head.data.vertices[i].co.x-=peak*w/max(weights.values())
    head.data.update(); new=tree(head)
    seats={}
    nose=bpy.data.objects['NOSE']; p=nose.matrix_world.translation
    dx=sample(new,p.y,p.z)-sample(old,p.y,p.z)
    nose.location.x+=dx
    seats['NOSE']=dict(method='rigid X shift from evaluated surface delta at existing center Y/Z',delta_x_H=dx,
                       baseline_center_relief_H=sample(old,p.y,p.z)-p.x)
    for name in ['MOUTH_closed','PHILTRUM']:
        o=bpy.data.objects[name]; shifts=[]; relief=[]
        for spline in o.data.splines:
            for p in spline.points:
                q=o.matrix_world@Vector(p.co[:3]); a=sample(old,q.y,q.z); b=sample(new,q.y,q.z)
                p.co.x+=b-a; shifts.append(b-a); relief.append(a-q.x)
            for p in spline.bezier_points:
                for prop in ['co','handle_left','handle_right']:
                    q=o.matrix_world@getattr(p,prop); a=sample(old,q.y,q.z); b=sample(new,q.y,q.z)
                    getattr(p,prop).x+=b-a
                    if prop=='co':shifts.append(b-a);relief.append(a-q.x)
        seats[name]=dict(method='preserve source relief at each evaluated surface sample, X only',min_delta_x_H=min(shifts),max_delta_x_H=max(shifts),source_relief_range_H=[min(relief),max(relief)])
    bpy.context.view_layer.update()
    assert all(ear.snapshot(bpy.data.objects[n])==r for n,r in baseline.items() if n not in FACE)
    assert topology(head)==json.loads((TMP/'source.json').read_text())['topology']
    data=dict(attempt='F'+str(attempt),peak_control_displacement_H=peak,
              changed_vertices=[dict(index=i,before=before[i],after=list(head.data.vertices[i].co)) for i in weights],
              changed_objects=sorted(n for n in baseline if ear.snapshot(bpy.data.objects[n])!=baseline[n]),
              features=seats,eye_surface_seating=eye_seating(old,new),other_objects_unchanged=True,
              sagittal_samples=[dict(z=z,source_x=sample(old,0,z),candidate_x=sample(new,0,z),delta_x=sample(new,0,z)-sample(old,0,z)) for z in [.30,.32,.34,.3542,.365,.374,.39,.41,.43,.45]],
              yz_max_delta_H=max(abs(v.co[a]-before[v.index][a]) for v in head.data.vertices for a in [1,2]))
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(TMP/f'F{attempt}.blend'))
    write(TMP/f'F{attempt}.json',data)
    print('FACE_ATTEMPT',json.dumps(data))
    face_renders(f'F{attempt}')

def scalar_properties(block):
    result={}
    for p in block.bl_rna.properties:
        if p.identifier in {'rna_type','session_uid'}:continue  # runtime ID changes on every load
        try:
            value=getattr(block,p.identifier)
            if p.type in {'BOOLEAN','INT','FLOAT','STRING','ENUM'}:
                result[p.identifier]=list(value) if getattr(p,'is_array',False) else (sorted(value) if isinstance(value,set) else value)
        except (AttributeError,TypeError):pass
    return result

def detailed_record(o):
    r=ear.snapshot(o)
    r['matrix']=[x for row in o.matrix_world for x in row]
    r['groups']={g.name:[(v.index,vg.weight) for v in o.data.vertices for vg in v.groups if vg.group==g.index] for g in o.vertex_groups} if o.type=='MESH' else {}
    r['modifiers']=[scalar_properties(m) for m in o.modifiers]
    r['visibility']=[o.hide_render,o.hide_viewport,o.hide_get()]
    if o.type in {'CAMERA','LIGHT','CURVE'}:r['data_properties']=scalar_properties(o.data)
    if o.type=='EMPTY':
        r['empty']=dict(size=o.empty_display_size,display=o.empty_display_type,color=list(o.color),
                        custom={k:o[k] for k in o.keys() if isinstance(o[k],(int,float,str))},
                        image=o.data.name if o.data else None)
    return r

def materials_record():
    result={}
    # Unreferenced v001 material datablocks in the source are not serialized by
    # Blender. Compare every material actually used by any source/candidate object.
    used={m.name for o in bpy.data.objects if hasattr(o.data,'materials') for m in o.data.materials if m}
    for m in bpy.data.materials:
        if m.name not in used:continue
        result[m.name]=dict(properties=scalar_properties(m),nodes=[dict(name=n.name,type=n.bl_idname,
            properties=scalar_properties(n),inputs={s.name:list(s.default_value) if hasattr(s.default_value,'__len__') and not isinstance(s.default_value,str) else s.default_value for s in n.inputs if hasattr(s,'default_value') and isinstance(s.default_value,(int,float,str,bool)) or hasattr(s,'default_value') and type(s.default_value).__name__ in {'bpy_prop_array','Vector','Color'}}) for n in m.node_tree.nodes] if m.use_nodes else [],
            links=[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links] if m.use_nodes else [])
    return result

def feature_points(o):
    if o.type=='MESH':return [o.matrix_world@v.co for v in o.data.vertices]
    points=[]
    for s in o.data.splines:
        points.extend(o.matrix_world@Vector(p.co[:3]) for p in s.points)
        for p in s.bezier_points:points.extend(o.matrix_world@v for v in [p.co,p.handle_left,p.handle_right])
    return points

def final_candidate(selected_ear):
    OUT.mkdir(parents=True,exist_ok=True)
    previous=json.loads((OUT/'validation.json').read_text()) if (OUT/'validation.json').exists() else None
    reuse_ears=bool(previous and selected_ear=='source' and previous['ear']['selected']=='source' and previous['source_asset_sha256']==hashlib.sha256(SOURCE.read_bytes()).hexdigest())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    baseline={o.name:detailed_record(o) for o in bpy.data.objects}
    materials=materials_record(); head=bpy.data.objects['CENTRAL_CHASSIS']
    before=coords(head); source_topology=topology(head); old_tree=tree(head)
    source_checks=previous['source_technical_checks'] if reuse_ears else {n:ear.mesh_check(bpy.data.objects[n]) for n in ['CENTRAL_CHASSIS','EAR_L','EAR_R']}
    feature_before={n:feature_points(bpy.data.objects[n]) for n in FACE_VISIBLE-{'CENTRAL_CHASSIS'}}
    ear_before={n:coords(bpy.data.objects[n]) for n in ear.EARS}
    # Source ear evidence shares the candidate cameras without fitting.
    if not all((TMP/('source-ear-'+v+'.png')).exists() for v in ['front','side','top','3q']):ear_renders('source')
    bpy.ops.wm.open_mainfile(filepath=str(TMP/'F1.blend'))
    f1=json.loads((TMP/'F1.json').read_text());f1['eye_surface_seating']=eye_seating(old_tree,tree(bpy.data.objects['CENTRAL_CHASSIS']))
    f1['executor_visual_precheck']='FAIL';f1['rejection']='Evaluated surface newly covers 7 eye points and 6 lid points per side; source eye seating not preserved.'
    bpy.ops.wm.open_mainfile(filepath=str(TMP/'F2.blend'))
    if selected_ear=='E2':apply_ear(E2_STATIONS)
    allowed=FACE | (ear.EARS if selected_ear=='E2' else set())
    bpy.context.view_layer.update()
    assert set(baseline)==set(o.name for o in bpy.data.objects)
    mismatch={n:{k:[v.get(k),detailed_record(bpy.data.objects[n]).get(k)] for k in v if v.get(k)!=detailed_record(bpy.data.objects[n]).get(k)} for n,v in baseline.items() if n not in allowed and detailed_record(bpy.data.objects[n])!=v}
    assert not mismatch, mismatch
    if materials_record()!=materials:
        write(TMP/'material-before.json',materials);write(TMP/'material-after.json',materials_record())
        raise AssertionError('Material record mismatch; see temporary before/after diagnostics')
    bpy.context.scene['stage']='READY_FOR_HUMAN_FACE_EAR_REVIEW; no authority promotion'
    bpy.context.scene['selected_candidate']='F2 / '+selected_ear
    bpy.context.preferences.filepaths.save_version=0
    saved={o.name:detailed_record(o) for o in bpy.data.objects}
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT)); bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))
    assert all(detailed_record(bpy.data.objects[n])==v for n,v in saved.items())
    assert materials_record()==materials
    head=bpy.data.objects['CENTRAL_CHASSIS']; after=coords(head); new_tree=tree(head)
    face_check=ear.mesh_check(head)
    assert source_topology==topology(head)
    deltas=[Vector(b)-Vector(a) for a,b in zip(before,after)]
    changed=[i for i,d in enumerate(deltas) if d.length>0]
    assert changed==[38,39]
    assert all(d.y==d.z==0 for d in deltas)
    assert max(d.length for d in deltas)<.02000001
    seating=eye_seating(old_tree,new_tree)
    assert all(v['newly_covered_control_points']==0 for v in seating.values()),seating
    # Frozen curves retain every control point's Y/Z. Nose is a rigid translation.
    feature_checks={}
    for n,oldpoints in feature_before.items():
        newpoints=feature_points(bpy.data.objects[n])
        yz=max(abs(a[k]-b[k]) for a,b in zip(oldpoints,newpoints) for k in [1,2])
        assert yz==0
        entry=dict(yz_max_delta_H=yz)
        if n in {'MOUTH_closed','PHILTRUM'}:
            ownership=max(abs((sample(old_tree,a.y,a.z)-a.x)-(sample(new_tree,b.y,b.z)-b.x)) for a,b in zip(oldpoints,newpoints))
            assert ownership<1e-6
            entry['max_source_relief_preservation_error_H']=ownership
        if n=='NOSE':
            center=bpy.data.objects[n].matrix_world.translation
            entry['center_relief_H']=sample(new_tree,center.y,center.z)-center.x
            entry['local_mesh_unchanged']=baseline[n]['mesh_and_shape_keys']==saved[n]['mesh_and_shape_keys']
            assert entry['local_mesh_unchanged'] and abs(entry['center_relief_H']-.01)<1e-6
        feature_checks[n]=entry
    poses={};roots={}
    for n in sorted(ear.EARS):
        o=bpy.data.objects[n];poses[n]=previous['ear']['poses'][n] if reuse_ears else {}
        if not reuse_ears:
            for pose in ['Basis','TEST lift','TEST droop','TEST attention flick']:
                if pose!='Basis':o.data.shape_keys.key_blocks[pose].value=1
                poses[n][pose]=ear.mesh_check(o)
                if pose!='Basis':o.data.shape_keys.key_blocks[pose].value=0
        for c in poses[n].values():c['volume_ratio_to_neutral']=c['volume_H3']/poses[n]['Basis']['volume_H3']
        sign=1 if n=='EAR_L' else -1
        root=ear.world((0,0,.002),sign);near,normal,_,dist=new_tree.find_nearest(root)
        roots[n]=dict(root_center_inside_head=(root-near).dot(normal)<0,root_surface_distance_H=dist,
                      root_source_coordinate_delta_H=max((Vector(ear_before[n][i])-o.data.vertices[i].co).length for i in range(48)),
                      test_root_station_max_displacement_H=max((k.data[i].co-o.data.vertices[i].co).length for k in o.data.shape_keys.key_blocks for i in range(48)),
                      topology=topology(o))
    left,right=[bpy.data.objects[n] for n in ['EAR_L','EAR_R']]
    mirror=max((Vector((a.co.x,-a.co.y,a.co.z))-b.co).length for a,b in zip(left.data.vertices,right.data.vertices))
    assert mirror==0
    checks=[face_check]+[c for p in poses.values() for c in p.values()]
    assert all(c['finite'] and c['nonmanifold_edges']==0 and c['outward_normals'] and c['nonadjacent_triangle_intersections']==0 for c in checks),checks
    assert all(r['root_center_inside_head'] and r['root_source_coordinate_delta_H']==0 and r['test_root_station_max_displacement_H']<1e-6 for r in roots.values())
    authority={}
    manifest=json.loads((ROOT/'assets/grimo/source/carol/approved-3d/authority.json').read_text())
    for entry in manifest['authorityOrder']:
        p=entry['path']
        raw=subprocess.check_output(['git','show',SOURCE_HEAD+':'+p],cwd=str(ROOT)) if p.endswith('.md') else (ROOT/p).read_bytes()
        digest=hashlib.sha256(raw).hexdigest();assert digest==entry['sha256'].lower()
        authority[p]=dict(sha256=digest,status='PASS',bytes_basis='canonical Git LF blob' if p.endswith('.md') else 'source file')
    changed_objects=sorted(n for n in baseline if baseline[n]!=saved[n])
    validation=dict(source_branch='origin/codex/setup-codegraph-mcp',source_head=SOURCE_HEAD,
        branch='codex/carol-face-ear-production-v003',source_asset_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        candidate=str(OUTPUT.relative_to(ROOT)).replace('\\','/'),output_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        authority_preflight='PASS',authority=authority,manifest_repair='pre-existing authority manifest hash drift repaired; no authority content or authority ordering changed.',
        face_executor_visual_precheck='PASS',ear_executor_visual_precheck='FAIL',technical_validation='PASS',
        face=dict(selected='F2',attempts_used=2,source_topology=source_topology,final_topology=topology(head),
                  max_control_displacement_H=max(d.length for d in deltas),changed_vertices=changed,
                  control_yz_unchanged=True,check=face_check,features=feature_checks,eye_surface_seating=seating),
        ear=dict(selected=selected_ear,disposition='EAR_V003_NOT_PROMOTED',attempts_used=2,mirror_error_H=mirror,poses=poses,roots=roots,
                 pink_same_closed_shell=True,materials_unchanged=True,controls_saved_zero=all(k.value==0 for o in [left,right] for k in o.data.shape_keys.key_blocks)),
        frozen=dict(changed_objects=changed_objects,unchanged_count=len(baseline)-len(changed_objects),
                    all_other_objects_exact=True,all_in_use_material_records_exact=True,save_reload_all_object_records_equal=True,
                    serialization_note='Blender session_uid is transient; two unreferenced v001 material datablocks are omitted automatically by Blender save. No in-use material changes.',
                    eye_lid_digest_equality={n:baseline[n]['mesh_and_shape_keys']==saved[n]['mesh_and_shape_keys'] for n in ['EYE_L','EYE_R','EYELID_L','EYELID_R']},
                    source_record_sha256={n:hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest() for n,v in baseline.items()}),
        source_technical_checks=source_checks,registration=dict(normal_side='Fixed source h=916 / ground=998 / origin=144; no fitting',
            skin_side_overlay='PROBE_INVALID: inherited registration does not align current approved Skin Side face landmarks; qualitative reference only',
            skin_front_overlay='Inspect as diagnostic; no candidate camera fitting',all_saved_camera_and_reference_objects_unchanged=True),
        state='READY_FOR_HUMAN_FACE_EAR_REVIEW',human_review='REQUIRED; no Human Geometry, identity, cuteness or final production PASS')
    write(OUT/'validation.json',validation)
    write(OUT/'measurements.json',dict(face=json.loads((TMP/'F2.json').read_text()),face_rejected_attempt=f1,ear_attempts={n:json.loads((TMP/(n+'.json')).read_text()) for n in ['E1','E2']}))
    render_setup()
    for view,d,target,scale in [('front',(-4,0,0),(.50,0,.46),1.37),('side',(0,-4,0),(.56,0,.46),1.48),('3q',(-3,-3,1.0),(.50,0,.46),1.45)]:
        ear.render('candidate-attached-'+view,d,target,scale,size=(960,900))
    center=ear.world((0,.19,-.074),1);front=Vector((-math.cos(ear.SWEEP),math.sin(ear.SWEEP),0))
    for label,pose in [('neutral',None),('lift','TEST lift'),('droop','TEST droop'),('attention','TEST attention flick')]:
        if reuse_ears and (TMP/('candidate-pose-'+label+'.png')).exists():continue
        if pose:left.data.shape_keys.key_blocks[pose].value=1
        ear.render('candidate-pose-'+label,front*4,center,.49,{'EAR_L'},size=(560,560))
        if pose:left.data.shape_keys.key_blocks[pose].value=0
    # Existing non-final fleece is a post-save occlusion diagnostic only.
    probe=SOURCE.with_name('carol-hero-experience-probe-v001.blend')
    with bpy.data.libraries.load(str(probe),link=False) as (src,dst):dst.objects=['DONOR Carol_Fleece_Continuous']
    fleece=dst.objects[0];bpy.context.scene.collection.objects.link(fleece)
    for view,d,target,scale in [('front',(-4,0,0),(.50,0,.46),1.37),('side',(0,-4,0),(.56,0,.46),1.48)]:
        ear.render('candidate-fleece-'+view,d,target,scale,size=(640,600))
    print('FINAL_VALIDATION',json.dumps(dict(technical='PASS',changed=changed_objects,roots=roots,poses=poses)))

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--stage',choices=['inspect','face','ear','final'],required=True)
    parser.add_argument('--attempt',type=int,choices=[1,2],default=1)
    parser.add_argument('--ear-selected',choices=['source','E2'],default='source')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.stage=='inspect':inspect()
    elif args.stage=='face':face_attempt(args.attempt)
    elif args.stage=='ear':ear_attempt(args.attempt)
    elif args.stage=='final':final_candidate(args.ear_selected)

if __name__=='__main__':main()
