"""Carol v011: bounded section and ocular refinement of v010-A3.

Run in Blender background with -- --attempt 1 --render. No new topology
family, booleans, remesh, rig, reference fitting, or camera-dependent form.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
sys.dont_write_bytecode=True
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'assets/grimo/production/carol/blender/carol-v010.blend'
ASSET=BASE.with_name('carol-v011.blend')
OUT=ROOT/'docs/production/carol/evidence/reconstruction-v011'
TMP=ROOT/'tmp-carol-v011'
SOURCE='9569bea8e08e0e068ed7debadf242419e9655a40'
spec=importlib.util.spec_from_file_location('v010',Path(__file__).with_name('build-carol-v010.py'))
v10=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v10)
v9,v8=v10.v9,v10.v8
write,lerp_table,cap_quad=v10.write,v10.lerp_table,v10.cap_quad
facial_frame=v10.facial_frame
CHANGED={'CENTRAL_CHASSIS','EYE_L','EYE_R','EYELID_L','EYELID_R','MOUTH_closed','PHILTRUM','NOSE'}


def chassis(skin, refinement):
    attempt=3  # Frozen v010-A3 patch connectivity; not the v011 attempt index.
    verts, faces, labels, ids = [], [], [], {}
    def vertex(p, label):
        i = len(verts)
        verts.append(tuple(p)); labels.append(label)
        return i
    def cube(i, j, k):
        key = i, j, k
        if key not in ids:
            u, v, w = (c/4-1 for c in key)
            d = Vector((u, v, w)).normalized()
            # Start from the same v010-A3 cube coordinates and Y/Z. Elliptic
            # depth sections replace the shoulder-producing cubic; A3 below
            # additionally rounds interior underside Z, not the lateral rim.
            low=max(0,-d.z)
            z=.449+(.258*d.z if d.z>=0 else -.216*low**.65)
            y=.311*d.y*(1+.025*low)
            # A3 rounds the sagittal underside while leaving the lateral
            # Front contour fixed (the correction vanishes at d.x == 0).
            if refinement>=3 and d.z<0:
                z+=.216*(low**.65-low**.95)*d.x*d.x
            cx=.320+.036*max(d.z,0)-.070*low+(.025 if refinement>=3 else .050)*low**4
            x=cx+.290*d.x
            r=math.hypot(d.x,d.y)
            c=d.x/r if r>1e-8 else 0
            x-=.014*math.exp(-((z-.374)/.050)**2-(y/.070)**2)*max(0,-c)**4
            if refinement>=3 and d.x<0:
                # A curved orbital bowl with finite curvature in both axes.
                # Its shallower lateral tangent avoids the v010 1.12 ramp;
                # its seat restores Side location without reducing aperture.
                dy=abs(y)-.162
                weight=.96*math.exp(-(dy/.170)**6-((z-.418)/.160)**6)
                t=min(1,-d.x/.45)
                weight*=t*t*(3-2*t)
                target=.140+.60*dy+.015*(dy/.090)**2+.012*((z-.418)/.090)**2
                x=x*(1-weight)+target*weight
            ids[key] = vertex((x, y, z), 'HEAD')
        return ids[key]
    # Six cube-derived patches. Remove one coherent posterior ventral strip,
    # including the lowest quarter of the back patch; keep the whole front jaw.
    for axis in range(3):
        free = [a for a in range(3) if a != axis]
        for fixed in [0, 8]:
            for a in range(8):
                for b in range(8):
                    if axis == 2 and fixed == 0 and a >= 4:
                        continue
                    if axis == 0 and fixed == 8 and b < 2:
                        continue
                    keys = []
                    for da, db in [(0,0), (1,0), (1,1), (0,1)]:
                        q = [0,0,0];q[axis]=fixed;q[free[0]]=a+da;q[free[1]]=b+db
                        keys.append(cube(*q))
                    faces.append(tuple(keys))
    # Width samples 0..8, path samples 0..6 (bottom, then low rear patch).
    def edge(i, j):
        return cube(4+i, j, 0) if i <= 4 else cube(8, j, i-4)
    head = ([edge(0,j) for j in range(8)]
            +[edge(i,8) for i in range(6)]
            +[edge(6,j) for j in range(8,0,-1)]
            +[edge(i,0) for i in range(6,0,-1)])
    # Chest opening inherits correspondence from the head patch, not from
    # independently oriented, densely sampled rings. A3 offsets are retained.
    portal = []
    for h in head:
        p = Vector(verts[h])
        lateral = abs(p.y)/.25
        q = p+Vector((.024, math.copysign(.022*lateral, p.y), -.024-.025*lateral))
        if attempt >= 2:
            q = Vector((p.x+.040, p.y*.78, p.z-.026))
        portal.append(vertex(q, 'NECK_TRANSITION'))
    def bridge(a, b):
        assert len(a) == len(b)
        faces.extend((a[j], a[(j+1)%len(a)], b[(j+1)%len(b)], b[j]) for j in range(len(a)))
    if attempt == 3:
        bridge(head, portal)
    else:
        middle = [vertex(Vector(verts[a]).lerp(Vector(verts[b]), .5), 'NECK_TRANSITION') for a,b in zip(head,portal)]
        bridge(head, middle);bridge(middle, portal)
    # Semantic map around the open upper chest boundary.
    mapping = {}
    for h, q in zip(head, portal):
        for i in range(7):
            for j in range(9):
                if h == edge(i,j):mapping[i,j]=q
    rings = []
    for i in range(7):
        left = Vector(verts[mapping[i,0]])
        right = Vector(verts[mapping[i,8]])
        x, width, zside = right.x, right.y, right.z
        bottom = lerp_table([(s[1],s[2]) for s in v8.TORSO_STATIONS], x)[0]
        ring = []
        for j in range(16):
            if j <= 8:
                if i in {0,6}:
                    ring.append(mapping[i,j])
                elif j == 0 or j == 8:
                    ring.append(mapping[i,j])
                else:
                    ring.append(None)  # intentionally absent upper chest
            else:
                t = math.pi*(j-8)/8
                ring.append(vertex((x, width*math.cos(t), zside-(zside-bottom)*math.sin(t)), 'CHEST'))
        rings.append(ring)
    for i in range(6):
        for j in range(8,16):
            k=(j+1)%16
            faces.append((rings[i][j],rings[i][k],rings[i+1][k],rings[i+1][j]))
    # Small anterior chest patch, closed with a 4x4 quad disk.
    start = [Vector(verts[k]) for k in rings[0]]
    prior = rings[0]
    if attempt == 1:
        for factor, x in [(.64,.268),(.12,.252)]:
            center = Vector((x,0,.194))
            new = [vertex((center.x, p.y*factor, center.z+(p.z-.218)*factor), 'CHEST') for p in start]
            bridge(prior,new);prior=new
    cap_start=len(verts)
    cap_quad(prior, verts, faces, vertex, 'CHEST')
    if attempt >= 2:
        for i in range(cap_start,len(verts)):
            p=Vector(verts[i])
            # A1 exposed a concave top cap quad beside the neck strip.
            # Seat the disk behind its top rim; do not relax contact tests.
            p.x += .015 if refinement>=2 else -.010
            if refinement>=3:
                p.x-=.025*min(1,max(0,(.200-p.z)/.055))
            verts[i]=tuple(p)
    # Reconstruct only the defective .575 seam. From .730 rearward, all old
    # 16-sample station coordinates and their topology are retained exactly.
    prior = rings[-1]
    for region,x,bottom,top,width,exponent in v8.TORSO_STATIONS[4:]:
        points=[]
        for j in range(16):
            theta=-math.pi/2+math.pi*j/8
            s,c=math.sin(theta),math.cos(theta)
            xx=x
            if x == .575:
                xx += .064*max(c,0)**2
            points.append((xx,width*v8.signed_power(s,exponent),
                           (bottom+top)/2+(top-bottom)/2*v8.signed_power(c,exponent)))
        new=[vertex(p,'ABDOMEN' if x<=.730 else 'RUMP') for p in points]
        bridge(prior,new);prior=new
    # Preserve the legacy rear cap as part of the successful rear body.
    # Loop rotation aligns the fan apex with the original +Z sample.
    prior=prior[4:]+prior[:4]
    faces.extend((prior[0],prior[j],prior[j+1],prior[j+2]) for j in range(1,14,2))
    used=sorted({i for f in faces for i in f});remap={v:i for i,v in enumerate(used)}
    ob=v8.mesh('CENTRAL_CHASSIS',[verts[i] for i in used], [tuple(remap[i] for i in f) for f in faces],skin,2)
    for label in ['HEAD','FACE','FOREHEAD','LOWER_CHEEK','NECK_TRANSITION','CHEST','ABDOMEN','RUMP']:
        group=ob.vertex_groups.new(name=label)
        selected=[remap[i] for i in used if labels[i]==label or labels[i]=='HEAD' and
                  (label=='FACE' and verts[i][0]<.24 and .30<verts[i][2]<.57 or
                   label=='FOREHEAD' and verts[i][2]>.53 or
                   label=='LOWER_CHEEK' and verts[i][2]<.345)]
        if selected:group.add(selected,1,'REPLACE')
    ob['architecture']='cube-derived cranial patches; anterior ventral jaw; matched short neck strip; open chest patch; retained rear stations'
    return ob


def eyes(ob,skin,brown,pigment):
    relief=.040
    surface,offset=facial_frame(ob)
    n,rings=64,12
    for side,sign in [('L',1),('R',-1)]:
        center_y=sign*.162
        p,normal,vertical,horizontal=surface(center_y,.418)
        vertices=[offset(center_y,.418,relief)]
        uv=[(.5,.5)]
        for k in range(1,rings+1):
            r=k/rings
            for j in range(n):
                t=2*math.pi*j/n
                y=center_y+sign*.0685*r*math.cos(t);z=.418+.0745*r*math.sin(t)
                vertices.append(offset(y,z,.0005+(relief-.0005)*(math.sqrt(1-(.88*r)**2)-math.sqrt(1-.88**2))/(1-math.sqrt(1-.88**2))))
                uv.append(((1+r*math.cos(t))/2,(1+r*math.sin(t))/2))
        faces=[(0,1+j,1+(j+1)%n) for j in range(n)]
        for k in range(rings-1):
            for j in range(n):
                a=1+k*n+j;b=1+k*n+(j+1)%n;faces.append((a,b,b+n,a+n))
        eye=v8.mesh('EYE_'+side,vertices,faces,pigment)
        eye['surface_frame']=json.dumps(dict(normal=list(normal),vertical=list(vertical),horizontal=list(horizontal)))
        eye['normal_relief_H']=relief
        layer=eye.data.uv_layers.new(name='APERTURE_UV')
        for poly in eye.data.polygons:
            for i in poly.loop_indices:layer.data[i].uv=uv[eye.data.loops[i].vertex_index]
        vertices=[]
        for r,d in [(1,.0009),(1.025,.0027),(1.07,.0013),(1.13,-.0006)]:
            for j in range(n):
                t=2*math.pi*j/n
                vertices.append(offset(center_y+sign*.0685*r*math.cos(t),.418+.0745*r*math.sin(t),d))
        faces=[]
        for k in range(3):
            for j in range(n):
                a=k*n+j;b=k*n+(j+1)%n;faces.append((a,b,b+n,a+n))
        lid=v8.mesh('EYELID_'+side,vertices,faces,skin)
        lid.data.materials.append(brown)
        for p in lid.data.polygons:
            if p.index<n:p.material_index=1
        for label,above in [('UPPER_LID',True),('LOWER_LID',False)]:
            g=lid.vertex_groups.new(name=label)
            g.add([i for i,p in enumerate(vertices) if (p.z>=.418)==above],1,'REPLACE')
    mouth=[]
    for j in range(49):
        y=-.0455+.091*j/48;z=.3542-.0065*math.sin(math.pi*abs(y)/.0455)
        mouth.append(offset(y,z,.002))
    v8.tube('MOUTH_closed',mouth,.0028,brown)
    v8.tube('PHILTRUM',[offset(0,.370,.002),offset(0,.3542,.002)],.0025,brown)
    nose=bpy.data.objects['NOSE']
    nose.location.x=surface(0,.378)[0].x-.010


def frozen_record(o):
    record=dict(geometry=v9.record(o),hide_render=o.hide_render,
                properties={k:str(o[k]) for k in o.keys()},
                materials=[m.name if m else None for m in o.data.materials] if o.type=='MESH' else [],
                modifiers=[(m.type,getattr(m,'levels',None),getattr(m,'render_levels',None)) for m in o.modifiers])
    if o.type=='EMPTY' and o.empty_display_type=='IMAGE':
        record.update(size=o.empty_display_size,color=list(o.color),image=o.data.name)
    if o.type=='LIGHT':record.update(energy=o.data.energy,color=list(o.data.color),size=o.data.size)
    return record


def verify_registration():
    for reg in v8.REGISTRATION.values():
        o=bpy.data.objects['REFERENCE '+reg['file']]
        assert all(o[k]==reg[k] for k in ['h','ground','origin'])
        width,height=o.data.size[:]
        horizontal=(width/2-reg['origin'])/reg['h']
        vertical=(reg['ground']-height/2)/reg['h']
        target=(1.4,-horizontal,vertical) if reg['view']=='front' else (horizontal,1,vertical)
        assert (o.location-Vector(target)).length<1e-6
        assert abs(o.empty_display_size-width/reg['h'])<1e-6


def projection_metrics():
    """Whole ocular cap bounds; evidence, not a substitute for visual review."""
    rotation=(Vector((.62,0,.40))-Vector((-3,-3,1.3))).to_track_quat('-Z','Y')
    axes={'front':(Vector((0,-1,0)),Vector((0,0,1))),
          'side':(Vector((1,0,0)),Vector((0,0,1))),
          '3q':(rotation@Vector((1,0,0)),rotation@Vector((0,1,0)))}
    result={}
    for name in ['EYE_L','EYE_R']:
        o=bpy.data.objects[name]
        points=[o.matrix_world@v.co for v in o.data.vertices]
        result[name]={}
        for view,(right,up) in axes.items():
            width=max(p.dot(right) for p in points)-min(p.dot(right) for p in points)
            height=max(p.dot(up) for p in points)-min(p.dot(up) for p in points)
            result[name][view]=dict(width_H=width,height_H=height,width_height_ratio=width/height)
    return result


def finalize_failure(attempt):
    """Archive inspected A3 without further geometry work or a motion probe."""
    assert attempt==3, 'The recorded final disposition applies only to A3'
    directory=TMP/'attempt-3'
    result=json.loads((directory/'measurements.json').read_text())
    assert result['technical_static_gate']=='PASS'
    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    baseline={o.name:frozen_record(o) for o in bpy.context.scene.objects if o.name not in CHANGED}
    old_projection=projection_metrics()
    bpy.ops.wm.open_mainfile(filepath=str(directory/'candidate.blend'))
    bpy.context.view_layer.update()
    assert v8.geometry_digest()==result['geometry_digest']
    assert all(frozen_record(bpy.data.objects[n])==r for n,r in baseline.items())
    verify_registration()
    source_unchanged=hashlib.sha256(BASE.read_bytes()).hexdigest()==result['source_v010_sha256']
    assert source_unchanged
    blockers=[
        'Side lower-cheek / chest still presents a long oblique underside rather than the required short soft turn.',
        'Side eye projection is too narrow and the cap remains too exposed relative to locked Skin Side; multi-view socket identity is unresolved.',
        'Top posterior shoulders are rounded, but the local anterior orbital shaping retains a slight taper; full cranial coherence is not accepted.',
    ]
    result.update(executor_visual_precheck='FAIL',
                  visual_views=dict(skin_front='Front aperture locks preserved; no meaningful silhouette drift; softer Front retained',
                                    skin_side='FAIL: persistent oblique under-jaw surface and narrow exposed eye',
                                    diagnostic_3q='Horizontal stretch substantially reduced; overall eye/socket gate still fails',
                                    diagnostic_top='Posterolateral shoulders removed; slight anterior taper remains'),
                  motion_clearance='NOT_RUN_EXECUTOR_VISUAL_PRECHECK_FAILED',
                  human_geometry_gate='NOT_REVIEW_READY',
                  status='BLOCKED_AT_V011_PHASE_A_VISUAL_RECONSTRUCTION',
                  selected_attempt='A3 — diagnostic only; not promoted',blockers=blockers,
                  source_v010_unchanged=source_unchanged,
                  ocular_projection_v010=old_projection,ocular_projection_v011=projection_metrics(),
                  support_centers_H=dict(fore=.390,hind=.920,spacing=.530),
                  eye_contract_H=dict(width=.137,height=.149,centers=[-.162,.162]),
                  attempt_budget='EXHAUSTED_AFTER_A3; no A4')
    scene=bpy.context.scene
    scene['stage']=result['status']
    scene['candidate_role']='DIAGNOSTIC ONLY — NOT PROMOTED'
    for key in ['executor_visual_precheck','motion_clearance','human_geometry_gate']:
        scene[key]=result[key]
    scene.camera=bpy.data.objects['CAM front']
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    # Reload is a serialization/frozen-state check, not another geometry attempt.
    bpy.ops.wm.open_mainfile(filepath=str(ASSET))
    bpy.context.view_layer.update()
    assert v8.geometry_digest()==result['geometry_digest']
    fixed={n:frozen_record(bpy.data.objects[n])==r for n,r in baseline.items()}
    assert all(fixed.values())
    write(OUT/'measurements.json',result)
    write(directory/'measurements.json',result)
    validation={k:result[k] for k in ['candidate','topology','technical_static_gate','adjacency_audit',
        'identical_face_connectivity','topology_family_retained','reference_hashes_verified',
        'reference_registration_verified','rear_control_max_delta_H','head_control_front_yz_max_delta_H',
        'source_v010_sha256','source_v010_unchanged','geometry_digest','executor_visual_precheck',
        'visual_views','motion_clearance','human_geometry_gate','blockers','phase_b','phase_c',
        'production_rig','animation','fleece','glb','runtime']}
    validation.update(control_disjoint_intersections=result['control']['count'],
                      evaluated_disjoint_intersections=result['evaluated']['count'],
                      frozen_objects_after_reload=fixed,
                      diagnostic_v011_sha256=hashlib.sha256(ASSET.read_bytes()).hexdigest())
    write(OUT/'validation.json',validation)
    for index in [1,2]:
        evidence=json.loads((TMP/f'attempt-{index}'/'measurements.json').read_text())
        evidence.update(executor_visual_precheck='NOT_RUN_TECHNICAL_GATE_FAILED' if index==1 else 'FAIL',
                        motion_clearance='NOT_RUN',human_geometry_gate='NOT_REVIEW_READY',
                        rejection=('Two adjacent control contacts at anterior chest cap; disjoint checks alone were zero.' if index==1 else
                                   'Top and 3Q improved, but Side eye too far forward/exposed and under-cheek too long.'))
        write(OUT/f'attempt-{index}.json',evidence)
    print('FINAL_DIAGNOSTIC '+json.dumps(dict(asset=str(ASSET),frozen=all(fixed.values()),status=result['status'])),flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--attempt',type=int,choices=[1,2,3],required=True)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--finalize-failure',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.finalize_failure:
        finalize_failure(args.attempt)
        return
    directory=TMP/f'attempt-{args.attempt}'
    directory.mkdir(parents=True,exist_ok=True)
    hashes={n:hashlib.sha256((v8.REFERENCE/n).read_bytes()).hexdigest()==h for n,h in v8.REFERENCE_HASHES.items()}
    assert all(hashes.values())
    source_hash=hashlib.sha256(BASE.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    verify_registration()
    scene=bpy.context.scene
    frozen={o.name:frozen_record(o) for o in scene.objects if o.name not in CHANGED}
    old=bpy.data.objects['CENTRAL_CHASSIS']
    old_coords=[v.co.copy() for v in old.data.vertices]
    old_faces=[tuple(p.vertices) for p in old.data.polygons]
    head_group=old.vertex_groups['HEAD'].index
    head_ids=[v.index for v in old.data.vertices if any(g.group==head_group for g in v.groups)]
    skin=old.data.materials[0]
    brown=bpy.data.objects['NOSE'].data.materials[0]
    pigment=bpy.data.objects['EYE_L'].data.materials[0]
    for name in CHANGED-{'NOSE'}:bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
    ob=chassis(skin,args.attempt)
    bpy.context.view_layer.update()
    assert [tuple(p.vertices) for p in ob.data.polygons]==old_faces, 'Topology-family change forbidden'
    rear=max((ob.data.vertices[i].co-p).length for i,p in enumerate(old_coords) if p.x>=.730-1e-7)
    yz=max(abs(ob.data.vertices[i].co[j]-old_coords[i][j]) for i in head_ids for j in [1,2])
    top=v10.topology(ob)
    control=v10.intersections(ob.data)
    evaluated_data=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    evaluated=v10.intersections(evaluated_data)
    adjacency=dict(control=v10.adjacency_audit(ob.data),evaluated=v10.adjacency_audit(evaluated_data))
    passing=(top['components']==1 and top['nonmanifold_edges']==0 and top['all_quads'] and top['euler']==2
             and top['degenerate_faces']==0 and control['count']==evaluated['count']==0
             and all(v['improper_contacts']==0 for v in adjacency.values()) and rear<1e-7)
    result=dict(candidate=f'v011-A{args.attempt}',source_commit=SOURCE,source_v010_sha256=source_hash,
                architecture=ob['architecture'],topology_family_retained=True,identical_face_connectivity=True,
                topology=top,control=control,evaluated=evaluated,adjacency_audit=adjacency,
                reference_hashes=v8.REFERENCE_HASHES,reference_hashes_verified=hashes,
                reference_registration=v8.REGISTRATION,reference_registration_verified=True,
                rear_control_max_delta_H=rear,head_control_front_yz_max_delta_H=yz,
                technical_static_gate='PASS' if passing else 'FAIL',executor_visual_precheck='NOT_RUN',
                motion_clearance='NOT_RUN',human_geometry_gate='NOT_REVIEW_READY',
                production_rig=False,animation=False,fleece=False,glb=False,runtime=False,
                phase_b='NOT_STARTED',phase_c='NOT_STARTED')
    write(directory/'measurements.json',result)
    print('TECHNICAL_GATE '+json.dumps({k:result[k] for k in ['candidate','topology','control','evaluated','adjacency_audit','technical_static_gate']}),flush=True)
    if not passing:return
    eyes(ob,skin,brown,pigment)
    bpy.context.view_layer.update()
    fixed={n:frozen_record(bpy.data.objects[n])==value for n,value in frozen.items()}
    assert all(fixed.values()),fixed
    assert not any(o.type=='ARMATURE' or o.animation_data for o in scene.objects)
    result['frozen_objects']=fixed
    result['bounds']={}
    for name in ['CENTRAL_CHASSIS','EYE_L','EYE_R']:
        data=bpy.data.objects[name].evaluated_get(bpy.context.evaluated_depsgraph_get()).data
        lo=[min(v.co[i] for v in data.vertices) for i in range(3)]
        hi=[max(v.co[i] for v in data.vertices) for i in range(3)]
        result['bounds'][name]=dict(min=lo,max=hi,span=[b-a for a,b in zip(lo,hi)])
    for name in ['EYE_L','EYE_R']:
        bounds=result['bounds'][name]
        assert abs(bounds['span'][1]-.137)<1e-6 and abs(bounds['span'][2]-.149)<1e-6
        assert abs(abs((bounds['min'][1]+bounds['max'][1])/2)-.162)<1e-6
    scene['selected_candidate']=result['candidate']
    scene['stage']='V011_PHASE_A_TECHNICAL_PASS; executor visual review pending'
    scene['candidate_role']='UNREVIEWED DIAGNOSTIC'
    scene['executor_visual_precheck']='NOT_RUN'
    scene['human_geometry_gate']='NOT_REVIEW_READY'
    scene['motion_clearance']='NOT_RUN'
    scene['saved_pose']='NEUTRAL'
    scene.camera=bpy.data.objects['CAM front']
    result['geometry_digest']=v8.geometry_digest()
    write(directory/'measurements.json',result)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(directory/'candidate.blend'))
    if args.render:v10.renders(directory)


if __name__=='__main__':main()
