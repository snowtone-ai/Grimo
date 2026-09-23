"""Bounded v013-A semantic anterior replacement. Run with Blender --background.

No historical builder is executed. v010/v011 supply registration and mesh checks.
The 24-edge orbital basins belong to the chassis; the optical lenses are separate.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import bpy
import bmesh
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/grimo/production/carol/blender/carol-v012.blend'
ASSET = SOURCE.with_name('carol-v013.blend')
OUT = ROOT / 'docs/production/carol/evidence/reconstruction-v013'
TMP = ROOT / 'tmp-carol-v013'
SOURCE_SHA = 'c2aa573baa3dc5723d6b20b80ba5355fb464606f2e0814a1ee81747c532a2055'
SOURCE_COMMIT = '9d39680389b20677b6627491fd79bd6acbc51658'
spec = importlib.util.spec_from_file_location('v011', Path(__file__).with_name('build-carol-v011.py'))
v11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v11)
v10, v8 = v11.v10, v11.v8
CHANGED = {'CENTRAL_CHASSIS', 'EYE_L', 'EYE_R', 'EYELID_L', 'EYELID_R', 'MOUTH_closed', 'PHILTRUM', 'NOSE'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def rear_record(ob):
    groups = {ob.vertex_groups[n].index for n in ('ABDOMEN', 'RUMP')}
    ids = {v.index for v in ob.data.vertices if any(g.group in groups for g in v.groups)}
    coords = {i: tuple(ob.data.vertices[i].co) for i in ids}
    # Coordinate-keyed faces/edges are independent of new anterior vertex indices.
    return dict(vertices=sorted(coords.values()),
                faces=sorted(tuple(sorted(coords[i] for i in p.vertices))
                             for p in ob.data.polygons if set(p.vertices) <= ids),
                edges=sorted(tuple(sorted(coords[i] for i in e.vertices))
                             for e in ob.data.edges if set(e.vertices) <= ids))


def face_x(y, z):
    return .022 + 3.3*y*y + .10*(z-.418)**2 - .007*math.exp(-(y/.055)**2-((z-.37)/.045)**2)


def build(old, skin, brown):
    bm = bmesh.new()
    labels = {}
    def vertex(p, label):
        v = bm.verts.new(p)
        labels[v] = label
        return v
    def face(vs, material=0):
        f = bm.faces.new(vs)
        f.material_index = material
        return f
    def bridge(a, b, material=0):
        assert len(a) == len(b)
        for i in range(len(a)):
            j = (i+1) % len(a)
            face((a[i], a[j], b[j], b[i]), material)
    def disk(loop, label, depth=0):
        n = len(loop)//4
        perimeter = ([(i,0) for i in range(n)] + [(n,j) for j in range(n)]
                     + [(i,n) for i in range(n,0,-1)] + [(0,j) for j in range(n,0,-1)])
        grid = dict(zip(perimeter, loop))
        for i in range(1,n):
            for j in range(1,n):
                u,v = i/n,j/n
                p = (grid[i,0].co*(1-v)+grid[i,n].co*v+grid[0,j].co*(1-u)+grid[n,j].co*u
                     -grid[0,0].co*(1-u)*(1-v)-grid[n,0].co*u*(1-v)
                     -grid[0,n].co*(1-u)*v-grid[n,n].co*u*v)
                p.x += depth*math.sin(math.pi*u)*math.sin(math.pi*v)
                grid[i,j] = vertex(p,label)
        for i in range(n):
            for j in range(n):
                face((grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))

    # Face fields: medial muzzle strip, superior forehead, inferior cheeks.
    ys = [-.305,-.275,-.24,-.20,-.162,-.124,-.084,-.049,0,
          .049,.084,.124,.162,.20,.24,.275,.305]
    zs = [.265,.302,.3407,.3793,.418,.4567,.4953,.534,.605]
    grid = {}
    for i,y in enumerate(ys):
        for j,z in enumerate(zs):
            if 1<i<7 and 1<j<7 or 9<i<15 and 1<j<7:
                continue
            yy,zz = y,z
            if j in (0,8):
                zz += (.026 if j==0 else -.042)*(abs(y)/.305)**3
            if i in (0,16):
                yy *= 1-.16*(abs(z-.418)/.187)**2
            grid[i,j] = vertex((face_x(yy,zz),yy,zz), 'FOREHEAD' if j>=7 else 'MUZZLE' if 7<=i<=9 else 'CHEEK')
    for i in range(16):
        for j in range(8):
            if (1<=i<7 or 9<=i<15) and 1<=j<7:
                continue
            face((grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))
    apertures = {}
    for side, start, cy in [('R',1,-.162),('L',9,.162)]:
        perimeter = ([(i,1) for i in range(start,start+6)] + [(start+6,j) for j in range(1,7)]
                     + [(i,7) for i in range(start+6,start,-1)] + [(start,j) for j in range(7,1,-1)])
        outside = [grid[k] for k in perimeter]
        for v in outside:
            labels[v] = 'R3_'+side
        # Each R0-R2 ring has 24 continuous, pole-free vertices. The corners
        # are samples, never topology poles. R3 distributes to named fields.
        prior = outside
        for label, scale, offset in [('R2',1.18,.009),('R1',1.055,-.003),('R0',1.0,-.001)]:
            ring=[]
            for j in range(24):
                t = -3*math.pi/4 + j*2*math.pi/24
                y,z = cy+.0685*scale*math.cos(t), .418+.0745*scale*math.sin(t)
                ring.append(vertex((face_x(y,z)+offset,y,z),label+'_'+side))
            bridge(prior,ring,1 if label=='R0' else 0)
            prior=ring
            if label=='R0': apertures[side]=[list(v.co) for v in ring]
        # A genuine recessed basin closes the central skin surface behind
        # the optical object. No hidden duplicate shell is introduced.
        basin=[]
        for j in range(24):
            t=-3*math.pi/4+j*2*math.pi/24
            y,z=cy+.0685*.90*math.cos(t),.418+.0745*.90*math.sin(t)
            basin.append(vertex((face_x(y,z)+.022,y,z),'ORBIT_BASIN_'+side))
        bridge(prior,basin)
        disk(basin,'ORBIT_BASIN_'+side,.025)

    perimeter = ([(i,0) for i in range(16)]+[(16,j) for j in range(8)]
                 +[(i,8) for i in range(16,0,-1)]+[(0,j) for j in range(8,0,-1)])
    prior = [grid[k] for k in perimeter]
    # The face is a semantic patch. These are anatomical section controls,
    # not a UV sphere and not the historical cube-derived connectivity.
    angles=[]
    previous=0
    for i,v in enumerate(prior):
        t=math.atan2(v.co.y/.305,(v.co.z-.435)/.17)
        if i:
            while t>=previous:t-=2*math.pi
        angles.append(t);previous=t
    start_angle=-3*math.pi/4
    def ring(n, label, bottom, top, width, xbottom, xtop, xside, blend=1):
        row=[]
        for j in range(n):
            regular=start_angle-2*math.pi*j/n
            t=angles[j]*(1-blend)+regular*blend if n==48 else regular
            s,c=math.sin(t),math.cos(t)
            x=xside+(xtop-xside)*max(c,0)**2+(xbottom-xside)*max(-c,0)**2
            z=(top+bottom)/2+(top-bottom)/2*c
            row.append(vertex((x,width*s,z),label))
        return row
    sections=[
        ('CRANIUM_FRONT',.245,.680,.315,.185,.235,.300,.35),
        ('CRANIUM_DORSAL',.249,.716,.315,.270,.350,.390,1),
        ('CRANIUM_POSTERIOR',.265,.676,.285,.330,.455,.475,1),
        ('J0_JAW_TURNOVER',.277,.585,.256,.355,.545,.505,1),
        ('J1_SUBJAW_FLEX',.250,.489,.240,.375,.585,.492,1),
        ('C0_CHEST_CREST',.184,.447,.258,.300,.605,.463,1),
        ('C1_CHEST_BLEND',.120,.425,.283,.400,.619,.495,1),
    ]
    for label,bottom,top,width,xb,xt,xs,blend in sections:
        new=ring(48,label,bottom,top,width,xb,xt,xs,blend)
        bridge(prior,new);prior=new
    # Density changes live in the chest blend, outside jaw/flex/orbital rows.
    # A 4-to-2 patch uses three quads, creating only valence 3/5 transitions.
    new=ring(32,'CHEST_DENSITY_OUTER',.102,.419,.296,.472,.627,.532)
    for k in range(8):
        a=[prior[(6*k+j)%48] for j in range(7)]
        b=[new[(4*k+j)%32] for j in range(5)]
        face((a[0],a[1],b[1],b[0]));face((a[1],a[2],a[3],b[1]));face((a[3],a[4],b[2],b[1]))
        face((a[4],a[5],b[3],b[2]));face((a[5],a[6],b[4],b[3]))
    prior=new
    new=ring(16,'CHEST_DENSITY_INNER',.094,.416,.302,.532,.634,.558)
    for k in range(8):
        a=[prior[(4*k+j)%32] for j in range(5)]
        b=[new[(2*k+j)%16] for j in range(3)]
        face((a[0],a[1],b[1],b[0]));face((a[1],a[2],a[3],b[1]));face((a[3],a[4],b[2],b[1]))
    prior=new
    groups={old.vertex_groups[n].index:n for n in ('ABDOMEN','RUMP')}
    retained={}
    for v in old.data.vertices:
        labels_old=[groups[g.group] for g in v.groups if g.group in groups]
        if labels_old:retained[v.index]=vertex(v.co,labels_old[0])
    for p in old.data.polygons:
        if all(i in retained for i in p.vertices):face([retained[i] for i in p.vertices])
    # The source's first retained station includes its exact nonplanar .575
    # interface. Extract its open perimeter from retained topology, not X alone.
    border=[v for v in retained.values() if any(e.is_boundary for e in v.link_edges)]
    assert len(border)==16, len(border)
    center_z=(.089+.414)/2
    def phase(v):
        t=math.atan2(v.co.y/.3055,(v.co.z-center_z)/((.414-.089)/2))
        return (start_angle-t)%(2*math.pi)
    border.sort(key=phase)
    # Avoid float wrap at the starting sample by choose the nearest sample.
    pivot=min(range(16),key=lambda i:abs(math.atan2(math.sin(math.atan2(border[i].co.y/.3055,(border[i].co.z-center_z)/.1625)-start_angle),math.cos(math.atan2(border[i].co.y/.3055,(border[i].co.z-center_z)/.1625)-start_angle))))
    border=border[pivot:]+border[:pivot]
    bridge(prior,border)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.verts.index_update()
    group_ids={name:[v.index for v,label in labels.items() if label==name] for name in set(labels.values())}
    data=bpy.data.meshes.new('v013 semantic anterior cage')
    bm.to_mesh(data);bm.free()
    ob=bpy.data.objects.new('CENTRAL_CHASSIS',data)
    bpy.context.scene.collection.objects.link(ob)
    data.materials.append(skin);data.materials.append(brown)
    for p in data.polygons:p.use_smooth=True
    for label,ids in group_ids.items():ob.vertex_groups.new(name=label).add(ids,1,'REPLACE')
    sub=ob.modifiers.new('Editable Catmull-Clark surface','SUBSURF')
    sub.levels=sub.render_levels=2
    ob['architecture']='Option D: semantic anterior replacement; integrated 24-edge orbital basins; J0/J1/C0/C1; source T0/rear'
    return ob,apertures


def optics(pigment):
    for side,cy in [('L',.162),('R',-.162)]:
        vertices=[(face_x(cy,.418)-.030,cy,.418)]
        uv=[(.5,.5)]
        n,rings=48,8
        for k in range(1,rings+1):
            r=1.065*k/rings
            for j in range(n):
                t=2*math.pi*j/n
                y,z=cy+.0685*r*math.cos(t),.418+.0745*r*math.sin(t)
                x=face_x(y,z)-.030*(1-r*r)+.004*r**8
                vertices.append((x,y,z));uv.append((.5+.5*r*math.cos(t),.5+.5*r*math.sin(t)))
        faces=[(0,1+j,1+(j+1)%n) for j in range(n)]
        for k in range(rings-1):
            for j in range(n):
                a=1+k*n+j;b=1+k*n+(j+1)%n;faces.append((a,b,b+n,a+n))
        ob=v8.mesh('EYE_'+side,vertices,faces,pigment)
        layer=ob.data.uv_layers.new(name='APERTURE_UV')
        for p in ob.data.polygons:
            for i in p.loop_indices:layer.data[i].uv=uv[ob.data.loops[i].vertex_index]
        ob['optical_relief_H']=.030
        ob['outer_edge']='Oversized optical edge behind integrated R0/R1; visual occlusion requires review'


def render(views):
    scene=bpy.context.scene
    scene.render.resolution_x=scene.render.resolution_y=480
    scene.render.resolution_percentage=100
    scene.cycles.samples=16
    before=v8.geometry_digest()
    for view in views:
        cam=bpy.data.objects['CAM '+view] if view in ('front','side') else v8.camera('TEMP '+view,(-3,-3,1.3) if view=='3q' else (.55,0,4),(.62,0,.40) if view=='3q' else (.55,0,0))
        scene.camera=cam
        scene.render.filepath=str(TMP/('skin-'+view+'.png' if view in ('front','side') else 'diagnostic-'+view+'.png'))
        assert v8.geometry_digest()==before
        bpy.ops.render.render(write_still=True)
        if view not in ('front','side'):bpy.data.objects.remove(cam,do_unlink=True)
    scene.camera=bpy.data.objects['CAM front']


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--render',default='')
    parser.add_argument('--finalize-failure',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.finalize_failure:
        finalize_failure()
        return
    TMP.mkdir(exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA
    hashes={n:hashlib.sha256((v8.REFERENCE/n).read_bytes()).hexdigest()==h for n,h in v8.REFERENCE_HASHES.items()}
    assert all(hashes.values())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    v11.verify_registration()
    scene=bpy.context.scene
    frozen={o.name:v11.frozen_record(o) for o in scene.objects if o.name not in CHANGED}
    old=bpy.data.objects['CENTRAL_CHASSIS']
    rear_before=rear_record(old)
    skin=old.data.materials[0];brown=bpy.data.objects['NOSE'].data.materials[0];pigment=bpy.data.objects['EYE_L'].data.materials[0]
    old.name='SOURCE_CHASSIS_TEMP'
    ob,apertures=build(old,skin,brown)
    bpy.data.objects.remove(old,do_unlink=True)
    for name in CHANGED-{'CENTRAL_CHASSIS','NOSE'}:
        bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
    optics(pigment)
    mouth=[]
    for j in range(49):
        y=-.0455+.091*j/48;z=.3542-.0065*math.sin(math.pi*abs(y)/.0455)
        mouth.append((face_x(y,z)-.002,y,z))
    v8.tube('MOUTH_closed',mouth,.0028,brown)
    v8.tube('PHILTRUM',[(face_x(0,z)-.002,0,z) for z in (.370,.3542)],.0025,brown)
    bpy.data.objects['NOSE'].location.x=face_x(0,.378)-.010
    bpy.context.view_layer.update()
    rear_after=rear_record(ob)
    assert rear_after==rear_before
    fixed={n:v11.frozen_record(bpy.data.objects[n])==r for n,r in frozen.items()}
    assert all(fixed.values()),fixed
    top=v10.topology(ob)
    control=v10.intersections(ob.data)
    bm=bmesh.new();bm.from_mesh(ob.data)
    normals=all(e.is_contiguous for e in bm.edges)
    duplicate=len({tuple(sorted(v.index for v in f.verts)) for f in bm.faces})!=len(bm.faces)
    valences={v.index:len(v.link_edges) for v in bm.verts}
    bm.free()
    zone_audit={}
    for name in ['R0_L','R1_L','R2_L','R0_R','R1_R','R2_R','J0_JAW_TURNOVER','J1_SUBJAW_FLEX','C0_CHEST_CREST']:
        g=ob.vertex_groups[name].index
        ids=[v.index for v in ob.data.vertices if any(x.group==g for x in v.groups)]
        zone_audit[name]=dict(count=len(ids),valences=sorted(set(valences[i] for i in ids)))
    passed=(top['components']==1 and top['nonmanifold_edges']==0 and top['degenerate_faces']==0
            and control['count']==0 and normals and not duplicate
            and all(r['valences']==[4] for r in zone_audit.values()))
    result=dict(candidate='v013-A',source_commit=SOURCE_COMMIT,source_v012_sha256=SOURCE_SHA,
                architecture=ob['architecture'],topology=top,control_disjoint_intersections=control,
                consistent_normals=normals,duplicate_faces=duplicate,semantic_flow=zone_audit,
                rear_fingerprint_before=digest(rear_before),rear_fingerprint_after=digest(rear_after),
                rear_correspondence='Exact float coordinates plus coordinate-keyed faces/edges of source ABDOMEN/RUMP, including .575 interface',
                rear_retained_vertices=len(rear_before['vertices']),rear_preserved=True,
                frozen_objects=fixed,reference_hashes_verified=hashes,reference_registration_verified=True,
                aperture_control_H=apertures,optical_relief_H=.030,
                cheap_technical_gate='PASS' if passed else 'FAIL',technical_static_gate='NOT_COMPLETED' if passed else 'FAIL',
                executor_status='STATIC_REVIEW_PENDING' if passed else 'TECHNICAL_FAIL',
                human_geometry_gate='NOT_REVIEW_READY',motion_probe='NOT_RUN_STATIC_PREREQUISITE_PENDING',
                phase_b='NOT_STARTED',phase_c='NOT_STARTED',ear_seating_delta_H=0,
                production_rig=False,animation=False,fleece=False,glb=False,runtime=False)
    scene['selected_candidate']='v013-A'
    scene['candidate_role']='DIAGNOSTIC ONLY — NOT PROMOTED'
    scene['human_geometry_gate']='NOT_REVIEW_READY'
    scene['stage']=result['executor_status']
    scene.camera=bpy.data.objects['CAM front']
    before=v8.geometry_digest()
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    bpy.ops.wm.open_mainfile(filepath=str(ASSET))
    assert v8.geometry_digest()==before
    assert rear_record(bpy.data.objects['CENTRAL_CHASSIS'])==rear_before
    assert all(v11.frozen_record(bpy.data.objects[n])==r for n,r in frozen.items())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA
    result.update(serialization_geometry_match=True,rear_fingerprint_after_reload=digest(rear_record(bpy.data.objects['CENTRAL_CHASSIS'])))
    result['frozen_objects_after_reload']=True
    result['source_v012_unchanged']=True
    v10.write(OUT/'measurements.json',result)
    print('V013_CHEAP_GATE '+json.dumps(dict(topology=top,gate=result['cheap_technical_gate'],control_intersections=control['count'],rear_preserved=True)),flush=True)
    if passed and args.render:render(args.render.split(','))


def finalize_failure():
    """Disposition only; do not change geometry or rerun its passing checks."""
    result=json.loads((OUT/'measurements.json').read_text())
    assert result['cheap_technical_gate']=='FAIL'
    bpy.ops.wm.open_mainfile(filepath=str(ASSET))
    ob=bpy.data.objects['CENTRAL_CHASSIS']
    # Wire-only inspection data, not beauty renders or a visual acceptance test.
    def wire(data):
        return dict(vertices=[list(v.co) for v in data.vertices],edges=[list(e.vertices) for e in data.edges])
    cage=wire(ob.data)
    evaluated=wire(ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).data)
    groups={g.index:g.name for g in ob.vertex_groups}
    cage['labels']=[[groups[g.group] for g in v.groups] for v in ob.data.vertices]
    v10.write(TMP/'wire.json',dict(control=cage,evaluated=evaluated))
    result.update(
        selected_attempt='A — DIAGNOSTIC ONLY; NOT PROMOTED',attempts_executed=['A'],
        executor_status='TECHNICAL_FAIL',executor_visual_precheck='NOT_RUN_TECHNICAL_GATE_FAILED',
        skin_front='NOT_RUN_TECHNICAL_GATE_FAILED',skin_side='NOT_RUN_TECHNICAL_GATE_FAILED',
        eye_socket='NOT_RUN_TECHNICAL_GATE_FAILED',derived_3q_top='NOT_RUN_TECHNICAL_GATE_FAILED',
        motion_probe='NOT_RUN_TECHNICAL_GATE_FAILED',human_geometry_gate='NOT_REVIEW_READY',
        candidate_role='DIAGNOSTIC ONLY — NOT PROMOTED',
        blockers=['36 disjoint control-face intersection pairs: the lateral face boundary and initial cranial loft overlap. The anterior replacement is not a valid exterior.',
                  'No Front/Side visual decision is eligible. Jaw/chest shape, visible aperture, lens-edge occlusion and cranial/ear fit remain unproven.'],
        attempts_b_c='NOT_RUN: A is not structurally correct; B requires a structurally correct A and C requires a near-review B.',
        evaluated_intersections='NOT_RUN_CHEAP_GATE_FAILED',adjacent_overlap_audit='NOT_RUN_CHEAP_GATE_FAILED',
        subdivision_evaluation='EVALUATES_FOR_WIRE_DIAGNOSTIC; geometric cleanliness not established',
        evidence_limit='Diagnostic sheet contains explicit NOT RUN cells; structure sheet is wire-only. No shaded candidate/overlay/derived renders were generated.',
        support_centers_H=dict(fore=.390,hind=.920,spacing=.530),
        visible_aperture_contract_H=dict(width=.137,height=.149,centers=[-.162,.162],status='CAGE_AUTHORED; evaluated visible opening not accepted'),
        toolset='Existing Blender 5.2 background Python + bmesh/mathutils, inherited targeted validators, Python/Pillow evidence, Git/LFS. No plugin/config/dependency changes; multi_agent=false.')
    for key in ('candidate_role','human_geometry_gate','motion_probe','executor_visual_precheck'):
        bpy.context.scene[key]=result[key]
    bpy.context.scene['stage']='TECHNICAL_FAIL'
    bpy.context.scene['saved_pose']='NEUTRAL'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    result['asset_sha256']=hashlib.sha256(ASSET.read_bytes()).hexdigest()
    v10.write(OUT/'measurements.json',result)
    omit={'aperture_control_H','frozen_objects'}
    v10.write(OUT/'validation.json',{k:v for k,v in result.items() if k not in omit})
    print('V013_FINAL_DISPOSITION TECHNICAL_FAIL; NOT_REVIEW_READY; no geometry change',flush=True)


if __name__=='__main__':main()
