"""Carol v010 Phase A: cube patches, a head-owned jaw, and matched chest edges.

Blender --background --python scripts/blender/build-carol-v010.py -- --attempt 1
Only a technically valid attempt is saved, under tmp-carol-v010 for review.
No automatic promotion, rig, remesh, Boolean, reference or camera changes.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'assets/grimo/production/carol/blender/carol-v009.blend'
ASSET = BASE.with_name('carol-v010.blend')
OUT = ROOT/'docs/production/carol/evidence/reconstruction-v010'
TMP = ROOT/'tmp-carol-v010'
SOURCE = '5de182d5eab04f84e3fa46926a953efa3527d679'
spec = importlib.util.spec_from_file_location('v009_helpers', Path(__file__).with_name('build-carol-v009.py'))
v9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v9)
v8 = v9.v8


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')


def lerp_table(rows, t):
    for a, b in zip(rows, rows[1:]):
        if t <= b[0]:
            u = max(0, (t-a[0])/(b[0]-a[0]))
            return tuple(x+(y-x)*u for x, y in zip(a[1:], b[1:]))
    return rows[-1][1:]


def chassis(skin, attempt):
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
            z = .4745+.2415*d.z
            # Locked silhouette interpretation; independent of camera or pose.
            width, front, rear = lerp_table([
                (.233, .000, .270, .270),
                (.253, .171, .111, .413),
                (.295, .280, .034, .501),
                (.345, .305, .019, .551),
                (.418, .301, .042, .592),
                (.490, .286, .060, .615),
                (.560, .263, .087, .613),
                (.630, .219, .146, .582),
                (.682, .145, .237, .507),
                (.716, .000, .360, .360),
            ], z)
            r = math.hypot(d.x, d.y)
            c, s = (d.x/r, d.y/r) if r > 1e-8 else (0, 0)
            depth = .25*c+.75*c**3
            x = (front+rear)/2+(rear-front)/2*depth
            y = width*s
            # A small round muzzle, subordinate to the cheek volume.
            x -= .013*math.exp(-((z-.374)/.045)**2-(y/.070)**2)*max(0, -c)**4
            if attempt >= 2:
                # Analytic rounded cage avoids a conical interpolated pole and
                # the diamond-like transverse section of A1.
                low=max(0,-d.z)
                z=.449+(.258*d.z if d.z>=0 else -.216*low**.65)
                y=.311*d.y*(1+.025*low)
                cx=.320+.036*max(d.z,0)-.070*low
                x=cx+.290*r*(.6*c+.4*c**3)
                x-=.014*math.exp(-((z-.374)/.050)**2-(y/.070)**2)*max(0,-c)**4
                if c<0:
                    weight=.85*math.exp(-((abs(y)-.162)/.105)**4-((z-.418)/.125)**4)
                    target=.126+.84*(abs(y)-.162)+.005*((z-.418)/.0745)**2
                    if attempt == 3:
                        weight=.90*math.exp(-((abs(y)-.162)/.150)**4-((z-.418)/.130)**4)
                        target=.161+1.12*(abs(y)-.162)+.005*((z-.418)/.0745)**2
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
    # independently oriented, densely sampled rings. Its front gap is .024 H.
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
            p=Vector(verts[i]);p.x-=(.010 if attempt==3 else .040)
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


def cap_quad(loop, verts, faces, vertex, label):
    # Coons quad disk, 16 boundary edges, no center fan pole.
    grid={}
    perimeter=([(i,0) for i in range(4)]+[(4,j) for j in range(4)]
               +[(i,4) for i in range(4,0,-1)]+[(0,j) for j in range(4,0,-1)])
    grid.update(zip(perimeter,loop))
    for i in range(1,4):
        for j in range(1,4):
            u,v=i/4,j/4
            p=(Vector(verts[grid[i,0]])*(1-v)+Vector(verts[grid[i,4]])*v
               +Vector(verts[grid[0,j]])*(1-u)+Vector(verts[grid[4,j]])*u
               -Vector(verts[grid[0,0]])*(1-u)*(1-v)-Vector(verts[grid[4,0]])*u*(1-v)
               -Vector(verts[grid[0,4]])*(1-u)*v-Vector(verts[grid[4,4]])*u*v)
            grid[i,j]=vertex(p,label)
    for i in range(4):
        for j in range(4):faces.append((grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))


def intersections(data):
    points=[v.co.copy() for v in data.vertices]
    polys=[list(p.vertices) for p in data.polygons]
    tree=BVHTree.FromPolygons(points,polys)
    pairs=sorted({tuple(sorted((a,b))) for a,b in tree.overlap(tree)
                  if a!=b and set(polys[a]).isdisjoint(polys[b])})
    proof=[]
    for a,b in pairs[:12]:
        proof.append(dict(pair=[a,b],faces=[[list(points[i]) for i in polys[k]] for k in [a,b]]))
    return dict(count=len(pairs),pairs=proof)


def topology(ob):
    bm=bmesh.new();bm.from_mesh(ob.data)
    seen=set();components=0
    for v in bm.verts:
        if v in seen:continue
        components+=1;stack=[v]
        while stack:
            v=stack.pop()
            if v in seen:continue
            seen.add(v);stack.extend(e.other_vert(v) for e in v.link_edges)
    result=dict(vertices=len(bm.verts),edges=len(bm.edges),faces=len(bm.faces),
                components=components,nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),
                all_quads=all(len(f.verts)==4 for f in bm.faces),euler=len(bm.verts)-len(bm.edges)+len(bm.faces),
                degenerate_faces=sum(f.calc_area()<1e-12 for f in bm.faces))
    bm.free();return result


def adjacency_audit(data):
    """Do not discard entire face pairs merely because they share a vertex.

    Test tessellated adjacent faces as well. Only a shared vertex/edge itself
    is legitimate contact. Coplanar overlap must have zero clipped area.
    Float32 geometric tolerance: 5e-7 H; no original disjoint pair is removed.
    """
    data.calc_loop_triangles()
    points=[v.co.copy() for v in data.vertices]
    triangles=[tuple(t.vertices) for t in data.loop_triangles]
    owners=[t.polygon_index for t in data.loop_triangles]
    incident={i:[] for i in range(len(points))}
    for i,tri in enumerate(triangles):
        for v in tri:incident[v].append(i)
    # Enumerate incidence explicitly: Blender's triangle overlap routine can
    # suppress shared-vertex pairs internally, before caller-side filtering.
    pairs={tuple(sorted((a,b))) for faces in incident.values() for a,b in itertools.combinations(faces,2)
           if owners[a]!=owners[b]}
    failures=[];tested=0;eps=5e-7
    def contact_allowed(p,common):
        if len(common)==1:return (p-points[common[0]]).length<=eps
        a,b=(points[i] for i in common[:2]);d=b-a
        t=max(0,min(1,(p-a).dot(d)/d.length_squared))
        return (p-(a+t*d)).length<=eps
    def segment_triangle(p,q,a,b,c):
        # mathutils arithmetic is float32. Near-coplanar shared-edge rays
        # suffer catastrophic cancellation there; operate on Python doubles.
        def sub(a,b):return tuple(float(a[i])-float(b[i]) for i in range(3))
        def dot(a,b):return sum(x*y for x,y in zip(a,b))
        def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
        d=sub(q,p);e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
        if abs(det)<1e-15:return None
        s=sub(p,a);u=dot(s,h)/det;v=dot(d,cross(s,e1))/det;t=dot(e2,cross(s,e1))/det
        if -1e-7<=t<=1+1e-7 and u>=-1e-7 and v>=-1e-7 and u+v<=1+1e-7:
            return Vector(tuple(float(p[i])+t*d[i] for i in range(3)))
        return None
    def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
    def coplanar_area(a,b,normal):
        drop=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=drop]
        poly=[tuple(p[i] for i in axes) for p in a];clip=[tuple(p[i] for i in axes) for p in b]
        direction=1 if cross2((clip[1][0]-clip[0][0],clip[1][1]-clip[0][1]),(clip[2][0]-clip[0][0],clip[2][1]-clip[0][1]))>=0 else -1
        for u,v in zip(clip,clip[1:]+clip[:1]):
            edge=(v[0]-u[0],v[1]-u[1])
            def distance(p):return direction*cross2(edge,(p[0]-u[0],p[1]-u[1]))
            previous=poly;poly=[]
            if not previous:return 0
            for p,q in zip(previous,previous[1:]+previous[:1]):
                dp,dq=distance(p),distance(q)
                if dp>=0:poly.append(p)
                if (dp>=0)!=(dq>=0):
                    t=dp/(dp-dq);poly.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
        return abs(sum(cross2(p,q) for p,q in zip(poly,poly[1:]+poly[:1])))/2
    for a,b in sorted(pairs):
        tested+=1;ta,tb=triangles[a],triangles[b];common=sorted(set(ta)&set(tb))
        pa,pb=[points[i] for i in ta],[points[i] for i in tb]
        na=(pa[1]-pa[0]).cross(pa[2]-pa[0]);nb=(pb[1]-pb[0]).cross(pb[2]-pb[0])
        witness=None
        if na.length<1e-14 or nb.length<1e-14:
            witness='degenerate triangle'
        elif na.normalized().cross(nb.normalized()).length<1e-6 and abs((pb[0]-pa[0]).dot(na.normalized()))<eps:
            if coplanar_area(pa,pb,na)>1e-12:witness='positive coplanar overlap area'
        else:
            for p,q in [(pa,pb),(pb,pa)]:
                for j in range(3):
                    h=segment_triangle(p[j],p[(j+1)%3],*q)
                    if h is not None and not contact_allowed(h,common):witness=list(h)
        if witness is not None:failures.append(dict(faces=[owners[a],owners[b]],triangles=[a,b],witness=witness))
    return dict(tested_adjacent_triangle_pairs=tested,improper_contacts=len(failures),proof=failures[:12],tolerance_H=eps)


def finalize_failure():
    """Archive the visually rejected A3, retaining the v009 baseline unchanged."""
    directory=TMP/'attempt-3'
    result=json.loads((directory/'measurements.json').read_text())
    baseline_hash=hashlib.sha256(BASE.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    changed={'CENTRAL_CHASSIS','EYE_L','EYE_R','EYELID_L','EYELID_R','MOUTH_closed','PHILTRUM','NOSE'}
    # Broaden object fingerprints to include modifiers, material membership,
    # reference registration properties, and camera/light data after reload.
    def frozen_record(o):
        record=dict(geometry=v9.record(o),hide_render=o.hide_render,
                    properties={k:str(o[k]) for k in o.keys()},
                    materials=[m.name if m else None for m in o.data.materials] if o.type=='MESH' else [],
                    modifiers=[(m.type,getattr(m,'levels',None),getattr(m,'render_levels',None)) for m in o.modifiers])
        if o.type=='EMPTY' and o.empty_display_type=='IMAGE':record.update(size=o.empty_display_size,color=list(o.color),image=o.data.name)
        if o.type=='LIGHT':record.update(energy=o.data.energy,color=list(o.data.color),size=o.data.size)
        return record
    baseline={o.name:frozen_record(o) for o in bpy.context.scene.objects if o.name not in changed}
    source_nose_matrix=bpy.data.objects['NOSE'].matrix_world.copy()
    bpy.ops.wm.open_mainfile(filepath=str(directory/'candidate.blend'))
    ob=bpy.data.objects['CENTRAL_CHASSIS']
    bpy.context.view_layer.update()
    evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    adjacent=dict(control=adjacency_audit(ob.data),evaluated=adjacency_audit(evaluated))
    fixed={n:frozen_record(bpy.data.objects[n])==h for n,h in baseline.items()}
    hashes={n:hashlib.sha256((v8.REFERENCE/n).read_bytes()).hexdigest()==h for n,h in v8.REFERENCE_HASHES.items()}
    assert all(fixed.values()) and all(hashes.values())
    reloaded_digest=v8.geometry_digest()
    if reloaded_digest!=result['geometry_digest']:
        # Early attempt evidence was fingerprinted before the depsgraph had
        # propagated the nose's seating translation. Prove that sole cause;
        # restore the saved matrix without altering the actual candidate.
        nose=bpy.data.objects['NOSE'];saved=nose.matrix_world.copy()
        nose.matrix_world=source_nose_matrix
        assert v8.geometry_digest()==result['geometry_digest'], 'Unexplained candidate change'
        nose.matrix_world=saved
        bpy.context.view_layer.update()
        assert v8.geometry_digest()==reloaded_digest
        result['pre_save_digest_correction']='Pending nose matrix only; saved candidate geometry unchanged'
        result['geometry_digest']=reloaded_digest
    assert all(a['improper_contacts']==0 for a in adjacent.values()), adjacent
    blockers=[
        'The wider Side ocular aperture becomes a horizontally stretched aperture in derived 3Q; the eye/socket system does not yet preserve Carol identity across views.',
        'Derived Top retains pronounced angular posterolateral cranial shoulders and a wedge-like anterior volume instead of a convincingly rounded single head.',
        'The lower cheek shelf is removed, but the oblique under-jaw plane is still too dominant relative to the soft locked Skin Side; visual reconstruction remains unapproved.',
    ]
    result.update(executor_visual_precheck='FAIL',motion_clearance='NOT_RUN_EXECUTOR_VISUAL_PRECHECK_FAILED',
                  human_geometry_gate='NOT_REVIEW_READY',status='BLOCKED_AT_V010_PHASE_A_VISUAL_RECONSTRUCTION',
                  selected_attempt='A3 — retained diagnostic only; no accepted candidate',blockers=blockers,
                  adjacency_audit=adjacent,retained_v009_sha256=baseline_hash,
                  rear_control_comparison_tolerance_H=1e-7,
                  support_centers_H=dict(fore=.390,hind=.920,spacing=.530),
                  eye_contract_H=dict(width=.137,height=.149,centers=[-.162,.162]),
                  phase_b='NOT_STARTED',phase_c='NOT_STARTED',attempt_budget='EXHAUSTED_AFTER_A3; no A4')
    scene=bpy.context.scene
    scene['stage']='BLOCKED_AT_V010_PHASE_A_VISUAL_RECONSTRUCTION; A3 REJECTED BY EXECUTOR; not Human-review-ready'
    scene['human_geometry_gate']='NOT_REVIEW_READY'
    scene['executor_visual_precheck']='FAIL'
    scene['motion_clearance']='NOT_RUN_EXECUTOR_VISUAL_PRECHECK_FAILED'
    scene['candidate_role']='DIAGNOSTIC ONLY — NOT PROMOTED'
    scene.camera=bpy.data.objects['CAM front']
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    write(OUT/'measurements.json',result)
    write(OUT/'validation.json',dict(candidate='v010-A3',technical_static_gate='PASS',
         topology=result['topology'],control_disjoint_intersections=0,evaluated_disjoint_intersections=0,
         adjacency_audit=adjacent,frozen_objects_after_reload=fixed,reference_hashes_unchanged=hashes,
         reference_registration_unchanged=True,geometry_digest=result['geometry_digest'],
         rear_control_stations_from_0730_unchanged=True,source_v009_unchanged=hashlib.sha256(BASE.read_bytes()).hexdigest()==baseline_hash,
         rear_control_comparison_tolerance_H=1e-7,
         source_v009_sha256=baseline_hash,diagnostic_v010_sha256=hashlib.sha256(ASSET.read_bytes()).hexdigest(),
         executor_visual_precheck='FAIL',motion_clearance=result['motion_clearance'],human_geometry_gate='NOT_REVIEW_READY',
         blockers=blockers,production_rig=False,animation=False,fleece=False,glb=False,runtime=False))
    for attempt in [1,2]:
        data=json.loads((TMP/f'attempt-{attempt}'/'measurements.json').read_text())
        data.update(executor_visual_precheck='FAIL',human_geometry_gate='NOT_REVIEW_READY',
                    motion_clearance='NOT_RUN_EXECUTOR_VISUAL_PRECHECK_FAILED',
                    rejection=('Outward chest rim, pointed crown, and diamond-shaped head.' if attempt==1 else 'Residual anterior chest lip and insufficient Side ocular visibility.'))
        write(OUT/f'attempt-{attempt}.json',data)
    source_audit=TMP/'source-audit.json'
    if not source_audit.exists():source_audit=OUT/'source-intersection-audit.json'
    audit=json.loads(source_audit.read_text())
    write(OUT/'source-intersection-audit.json',{k:audit[k] for k in ['hashes_verified','control','evaluated']})
    print('FINAL_REJECTED_DIAGNOSTIC '+json.dumps(dict(adjacency=adjacent,frozen=all(fixed.values()),asset=str(ASSET))),flush=True)


def facial_frame(ob):
    bpy.context.view_layer.update()
    data=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    tree=BVHTree.FromPolygons([v.co for v in data.vertices],[list(p.vertices) for p in data.polygons])
    def surface(y,z):
        p,n,_,_=tree.ray_cast(Vector((-1,y,z)),Vector((1,0,0)))
        if p is None:raise ValueError('Eye aperture left facial surface')
        if n.x>0:n=-n
        vertical=(Vector((0,0,1))-n*n.z).normalized()
        horizontal=vertical.cross(n).normalized()
        return p,n,vertical,horizontal
    def offset(y,z,d=0):
        # Solve the projected contract in the actual local surface frame.
        # This retains exact Front dimensions while the relief follows normal.
        yy,zz=y,z
        for _ in range(5):
            p,n,_,_=surface(yy,zz)
            yy=y-n.y*d;zz=z-n.z*d
        p,n,_,_=surface(yy,zz)
        return p+n*d
    return surface,offset


def eyes(ob,skin,brown,pigment):
    surface,offset=facial_frame(ob)
    n,rings=64,12
    for side,sign in [('L',1),('R',-1)]:
        center_y=sign*.162
        p,normal,vertical,horizontal=surface(center_y,.418)
        vertices=[offset(center_y,.418,.023)]
        uv=[(.5,.5)]
        for k in range(1,rings+1):
            r=k/rings
            for j in range(n):
                t=2*math.pi*j/n
                y=center_y+sign*.0685*r*math.cos(t);z=.418+.0745*r*math.sin(t)
                vertices.append(offset(y,z,.0005+.0225*(1-r*r)))
                uv.append(((1+r*math.cos(t))/2,(1+r*math.sin(t))/2))
        faces=[(0,1+j,1+(j+1)%n) for j in range(n)]
        for k in range(rings-1):
            for j in range(n):
                a=1+k*n+j;b=1+k*n+(j+1)%n;faces.append((a,b,b+n,a+n))
        eye=v8.mesh('EYE_'+side,vertices,faces,pigment)
        eye['surface_frame']=json.dumps(dict(normal=list(normal),vertical=list(vertical),horizontal=list(horizontal)))
        eye['normal_relief_H']=.023
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


def renders(directory):
    scene=bpy.context.scene
    digest=v8.geometry_digest()
    scene.render.resolution_x=scene.render.resolution_y=480
    scene.cycles.samples=16
    for name in ['front','side','3q','top']:
        if name in {'front','side'}:cam=bpy.data.objects['CAM '+name]
        else:cam=v8.camera('TEMP '+name,(-3,-3,1.3) if name=='3q' else (.55,0,4),(.62,0,.40) if name=='3q' else (.55,0,0))
        scene.camera=cam
        assert v8.geometry_digest()==digest
        scene.render.filepath=str(directory/(('skin-' if name in {'front','side'} else 'diagnostic-')+name+'.png'))
        bpy.ops.render.render(write_still=True)
        if name in {'3q','top'}:bpy.data.objects.remove(cam,do_unlink=True)
    scene.camera=bpy.data.objects['CAM front']


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--attempt',type=int,choices=[1,2,3],default=1)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--finalize-failure',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.finalize_failure:
        finalize_failure();return
    directory=TMP/f'attempt-{args.attempt}'
    directory.mkdir(parents=True,exist_ok=True)
    assert all(hashlib.sha256((v8.REFERENCE/n).read_bytes()).hexdigest()==h for n,h in v8.REFERENCE_HASHES.items())
    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene=bpy.context.scene
    changed={'CENTRAL_CHASSIS','EYE_L','EYE_R','EYELID_L','EYELID_R','MOUTH_closed','PHILTRUM','NOSE'}
    frozen={o.name:v9.record(o) for o in scene.objects if o.name not in changed}
    old=bpy.data.objects['CENTRAL_CHASSIS']
    rear={tuple(v.co) for v in old.data.vertices if v.co.x>=.730-1e-7}
    skin=old.data.materials[0];brown=bpy.data.objects['NOSE'].data.materials[0]
    pigment=bpy.data.objects['EYE_L'].data.materials[0]
    for name in changed-{'NOSE'}:bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
    ob=chassis(skin,args.attempt)
    bpy.context.view_layer.update()
    top=topology(ob)
    control=intersections(ob.data)
    evaluated=intersections(ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).data)
    fixed={n:v9.record(bpy.data.objects[n])==h for n,h in frozen.items()}
    rear_retained=all(any((Vector(p)-v.co).length<1e-7 for v in ob.data.vertices) for p in rear)
    passing=(top['components']==1 and top['nonmanifold_edges']==0 and top['all_quads'] and top['euler']==2
             and top['degenerate_faces']==0 and control['count']==evaluated['count']==0
             and all(fixed.values()) and rear_retained)
    result=dict(candidate=f'v010-A{args.attempt}',source_commit=SOURCE,architecture=ob['architecture'],
                topology=top,control=control,evaluated=evaluated,frozen_objects=fixed,
                rear_control_stations_from_0730_unchanged=rear_retained,
                rear_control_comparison_tolerance_H=1e-7,
                reference_hashes=v8.REFERENCE_HASHES,reference_registration=v8.REGISTRATION,
                technical_static_gate='PASS' if passing else 'FAIL',executor_visual_precheck='NOT_RUN',
                motion_clearance='NOT_RUN',human_geometry_gate='NOT_REVIEW_READY',
                production_rig=False,animation=False,fleece=False,glb=False,runtime=False)
    write(directory/'measurements.json',result)
    print('FAST_GATE '+json.dumps({k:result[k] for k in ['candidate','topology','technical_static_gate','rear_control_stations_from_0730_unchanged']}),flush=True)
    print('INTERSECTIONS',control['count'],evaluated['count'],flush=True)
    if not passing:return
    eyes(ob,skin,brown,pigment)
    bpy.context.view_layer.update()
    assert not any(o.type=='ARMATURE' or o.animation_data for o in scene.objects)
    scene['selected_candidate']=result['candidate']
    scene['stage']='V010_PHASE_A_TECHNICAL_PASS; executor visual review pending; Human Gate not approved'
    scene['saved_pose']='NEUTRAL'
    scene.camera=bpy.data.objects['CAM front']
    result['geometry_digest']=v8.geometry_digest()
    result['bounds']={}
    deps=bpy.context.evaluated_depsgraph_get()
    for name in ['CENTRAL_CHASSIS','EYE_L','EYE_R']:
        data=bpy.data.objects[name].evaluated_get(deps).data
        lo=[min(v.co[i] for v in data.vertices) for i in range(3)]
        hi=[max(v.co[i] for v in data.vertices) for i in range(3)]
        result['bounds'][name]=dict(min=lo,max=hi,span=[b-a for a,b in zip(lo,hi)])
    write(directory/'measurements.json',result)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(directory/'candidate.blend'))
    if args.render:renders(directory)


if __name__=='__main__':main()
