"""Bounded Carol v009 Phase A: authored continuous chassis and ocular caps.

Uses the immutable v008 scene only for frozen modules, cameras and pigment.
No Boolean, remesh, joined intersecting shells, rig, export or per-view edits.
Run with Blender --background --python this-file -- --attempt 1.
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
BASE = ROOT/'assets/grimo/production/carol/blender/carol-v008.blend'
ASSET = BASE.with_name('carol-v009.blend')
OUT = ROOT/'docs/production/carol/evidence/reconstruction-v009'
spec = importlib.util.spec_from_file_location('v008_frozen', Path(__file__).with_name('build-carol-v008.py'))
v8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v8)


def record(obj):
    result = dict(matrix=[list(r) for r in obj.matrix_world], type=obj.type,
                  parent=obj.parent.name if obj.parent else None)
    if obj.type == 'MESH':
        result.update(vertices=[list(v.co) for v in obj.data.vertices],
                      faces=[list(p.vertices) for p in obj.data.polygons])
    if obj.type == 'CAMERA':
        result.update(ortho_scale=obj.data.ortho_scale, camera_type=obj.data.type)
    return hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()


def chassis(skin, attempt):
    # A single swept manifold, from skull apex through lower cheek and short
    # turning neck to the frozen longitudinal torso. No buried exterior shell.
    verts, faces, loops, tags = [], [], [], []
    def add(points, region):
        ids = list(range(len(verts), len(verts)+len(points)))
        verts.extend(points)
        if loops:
            a, b = loops[-1], ids
            if len(a) == len(b):
                faces.extend((a[j],a[(j+1)%len(a)],b[(j+1)%len(b)],b[j]) for j in range(len(a)))
            else:
                assert len(a) == 2*len(b)
                # Authored 4-edge to 2-edge quad reduction. The pole pairs are
                # on transitional loops, not on the eye aperture or torso.
                for j in range(0,len(b),2):
                    p=[a[(2*j+k)%len(a)] for k in range(5)]
                    q=[b[(j+k)%len(b)] for k in range(3)]
                    faces.extend([(p[0],p[1],q[1],q[0]),
                                  (p[1],p[2],p[3],q[1]),
                                  (p[3],p[4],q[2],q[1])])
        loops.append(ids)
        tags.append(region)

    sections = list(reversed(v8.HEAD_SECTIONS[3:]))
    if attempt==2: sections.append((.292,.260,.230,.290))
    for z,cx,rx,ry in sections:
        pts=[]
        for j in range(64):
            t=2*math.pi*j/64
            c,s=math.cos(t),math.sin(t)
            y=ry*v8.signed_power(s,.90)
            x=cx+rx*v8.cranial_depth(c)
            x-=.020*math.exp(-((z-.368)/.049)**2)*math.exp(-(y/.080)**2)*max(0,-c)**8
            if c<0:
                u=(abs(y)-.162)/.0685
                w=(z-.418)/.0745
                r=math.hypot(u,w)
                a=max(0,min(1,(1.8-r)/.65));a=a*a*(3-2*a)
                target=.130+(abs(y)-.162)*(1.00 if attempt==1 else .72)+.006*w*w
                x=x*(1-a)+target*a
            # Continuous curvature along the lower cheek instead of a flat
            # horizontal lower rim. Rear height follows the short transition.
            low=max(0,(.40-z)/.085)
            zz=z+low*(.030*max(c,0)**2-.012*s*s)
            pts.append((x,y,zz))
        add(pts,'FOREHEAD' if z>=.50 else 'FACE' if z>=.34 else 'LOWER_CHEEK')

    # Explicit short cross-sections. Tuple: front X/Z, rear X/Z, half-width,
    # samples. A turn in the section plane makes one neck/chest surface.
    transitions=[
        (.075,.265,.545,.350,.271,64,'LOWER_CHEEK'),
        (.155,.230,.563,.360,.237,32,'NECK_TRANSITION'),
        (.240,.215,.574,.379,.226,16,'NECK_TRANSITION'),
        (.280,.158,.581,.404,.249,16,'CHEST'),
        (.365,.118,.590,.419,.268,16,'CHEST'),
    ]
    if attempt==2:
        transitions=[
            (.062,.267,.535,.360,.275,64,'LOWER_CHEEK'),
            (.115,.247,.552,.367,.247,64,'NECK_TRANSITION'),
            (.200,.220,.570,.383,.235,64,'NECK_TRANSITION'),
            (.280,.158,.581,.404,.249,64,'CHEST'),
            (.365,.118,.590,.419,.268,32,'CHEST'),
        ]
    for fx,fz,rx,rz,width,n,region in transitions:
        pts=[]
        for j in range(n):
            t=2*math.pi*j/n;c=math.cos(t);s=math.sin(t)
            pts.append(((fx+rx)/2+(rx-fx)/2*c,
                        width*v8.signed_power(s,.90),
                        (fz+rz)/2+(rz-fz)/2*c))
        add(pts,region)
    for region,x,bottom,top,width,exponent in v8.TORSO_STATIONS[3:]:
        pts=[]
        for j in range(16):
            t=2*math.pi*j/16;c=math.cos(t);s=math.sin(t)
            # Only upper chest is moved rearward to meet the continuous neck;
            # .575/.730 and all rear stations retain their original vertices.
            xx=x+(.145*max(c,0)**2 if x==.450 else 0)
            zz=(bottom+top)/2+(top-bottom)/2*v8.signed_power(c,exponent)
            if x==.450: zz-=.024*max(c,0)**2
            pts.append((xx,width*v8.signed_power(s,exponent),zz))
        add(pts,'CHEST' if region=='chest' else 'ABDOMEN' if region=='abdomen' else 'RUMP')
    for loop in (loops[0],loops[-1]):
        for j in range(1,len(loop)-2,2):
            faces.append((loop[0],loop[j],loop[j+1],loop[j+2]))
    ob=v8.mesh('CENTRAL_CHASSIS',verts,faces,skin,2)
    for name in ['HEAD','FACE','LOWER_CHEEK','FOREHEAD','NECK_TRANSITION','CHEST','ABDOMEN','RUMP']:
        group=ob.vertex_groups.new(name=name)
        for ids,tag in zip(loops,tags):
            if tag==name or name=='HEAD' and tag in {'FACE','FOREHEAD','LOWER_CHEEK'}:
                group.add(ids,1,'REPLACE')
    ob['architecture']='one authored quad surface; 64/32/16 section bridge; no intersecting exterior owners'
    return ob


def ocular(side,sign,sample,skin,brown,pigment):
    n,rings=96,20
    radius_y,radius_z=.0685,.0745
    center=Vector(sample(sign*.162,.418))
    boundary=[Vector(sample(sign*(.162+radius_y*math.cos(2*math.pi*j/n)),
                            .418+radius_z*math.sin(2*math.pi*j/n))) for j in range(n)]
    relief=.029
    def point(r,j):
        # Partial oblique ellipsoid, seated at the cranial perimeter. Radial
        # form no longer follows the cranial interior as a shallow decal.
        p=center.lerp(boundary[j],r)
        sag=(math.sqrt(1-.80*r*r)-math.sqrt(.20))/(1-math.sqrt(.20))
        p.x-=.0008+relief*sag
        return tuple(p)
    verts=[(center.x-relief-.0008,center.y,center.z)]
    uv=[(.5,.5)]
    for k in range(1,rings+1):
        r=k/rings
        for j in range(n):
            verts.append(point(r,j))
            t=2*math.pi*j/n
            uv.append(((1+r*math.cos(t))/2,(1+r*math.sin(t))/2))
    faces=[(0,1+j,1+(j+1)%n) for j in range(n)]
    for k in range(rings-1):
        for j in range(n):
            a=1+k*n+j;b=1+k*n+(j+1)%n
            faces.append((a,b,b+n,a+n))
    ob=v8.mesh('EYE_'+side,verts,faces,pigment)
    layer=ob.data.uv_layers.new(name='APERTURE_UV')
    for poly in ob.data.polygons:
        for i in poly.loop_indices: layer.data[i].uv=uv[ob.data.loops[i].vertex_index]
    ob['architecture']='embedded partial ellipsoid ocular cap; seated perimeter'
    ob['central_sag_H']=relief
    verts=[]
    # Six lid/socket loops for a future closure prototype; no rig claim.
    for r,d in [(1,.0012),(1.015,.0028),(1.035,.004),(1.065,.0028),(1.10,.0009),(1.16,-.0005)]:
        for j in range(n):
            t=2*math.pi*j/n
            verts.append(sample(sign*(.162+radius_y*r*math.cos(t)),.418+radius_z*r*math.sin(t),d))
    faces=[]
    for k in range(5):
        for j in range(n):
            a=k*n+j;b=k*n+(j+1)%n;faces.append((a,b,b+n,a+n))
    lid=v8.mesh('EYELID_'+side,verts,faces,skin)
    lid.data.materials.append(brown)
    for p in lid.data.polygons:
        if p.index<n: p.material_index=1
    for name,predicate in [('UPPER_LID',lambda z:z>=.418),('LOWER_LID',lambda z:z<=.418)]:
        g=lid.vertex_groups.new(name=name)
        g.add([i for i,p in enumerate(verts) if predicate(p[2])],1,'REPLACE')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--attempt',type=int,choices=[1,2],default=1)
    parser.add_argument('--resolution',type=int,default=480)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    directory=OUT/f'phase-a-attempt-{args.attempt}'
    directory.mkdir(parents=True,exist_ok=True)
    for name,digest in v8.REFERENCE_HASHES.items():
        assert hashlib.sha256((v8.REFERENCE/name).read_bytes()).hexdigest()==digest
    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene=bpy.context.scene
    frozen={o.name:record(o) for o in scene.objects if o.type in {'MESH','CAMERA','EMPTY'}}
    skin=bpy.data.objects['HEAD_CAGE'].data.materials[0]
    brown=bpy.data.objects['HOOF_FORE_L'].data.materials[0]
    pigment=bpy.data.objects['EYE_L'].data.materials[0]
    for name in ['HEAD_CAGE','TORSO_CAGE','SHORT_NECK_SOCKET','EYE_L','EYE_R','EYELID_L','EYELID_R','MOUTH_closed','PHILTRUM']:
        bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
    central=chassis(skin,args.attempt)
    sample=v8.facial_surface(central)
    for side,sign in [('L',1),('R',-1)]: ocular(side,sign,sample,skin,brown,pigment)
    mouth=[]
    for j in range(49):
        y=-.0455+.091*j/48;z=.3542-.0065*math.sin(math.pi*abs(y)/.0455)
        mouth.append(sample(y,z,.002))
    v8.tube('MOUTH_closed',mouth,.0028,brown)
    v8.tube('PHILTRUM',[sample(0,.370,.002),sample(0,.3542,.002)],.0025,brown)
    scene['stage']='V009_PHASE_A_UNREVIEWED; Human Geometry Gate PENDING HUMAN REVIEW'
    scene['selected_candidate']=f'v009-A{args.attempt}'
    if 'selected_revision' in scene: del scene['selected_revision']
    scene.render.resolution_x=scene.render.resolution_y=args.resolution
    scene.cycles.samples=16
    scene.camera=bpy.data.objects['CAM front']
    bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    meshes={}
    for o in scene.objects:
        if o.type!='MESH':continue
        ev=o.evaluated_get(deps)
        pts=[o.matrix_world@v.co for v in ev.data.vertices]
        bounds=[[min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]]
        meshes[o.name]=dict(min=bounds[0],max=bounds[1],span=[bounds[1][i]-bounds[0][i] for i in range(3)])
    bm=bmesh.new();bm.from_mesh(central.data)
    nonmanifold=sum(not e.is_manifold for e in bm.edges)
    seen=set();components=0
    for vert in bm.verts:
        if vert.index in seen: continue
        components+=1;stack=[vert]
        while stack:
            v=stack.pop()
            if v.index in seen:continue
            seen.add(v.index);stack.extend(e.other_vert(v) for e in v.link_edges)
    bm.free()
    changed={o.name:record(o)==frozen[o.name] for o in scene.objects if o.name in frozen and o.type in {'MESH','CAMERA','EMPTY'}}
    frozen_names=['EAR_L','EAR_R','FORE_L','FORE_R','HIND_L','HIND_R','HOOF_FORE_L','HOOF_FORE_R','HOOF_HIND_L','HOOF_HIND_R','SKIN_TAIL_CORE','TAIL_PIVOT','CAM front','CAM side']
    assert all(changed[n] for n in frozen_names)
    assert nonmanifold==0 and components==1
    assert all(len(p.vertices)==4 for p in central.data.polygons)
    assert not any(o.type=='ARMATURE' or o.animation_data for o in scene.objects)
    digest=v8.geometry_digest()
    result=dict(candidate=f'v009-A{args.attempt}',source_commit='2583c23949487b2cb15a243001858bb06f358d9b',
                phase='A',human_geometry_gate='PENDING HUMAN REVIEW',static_visual_status='UNREVIEWED',
                reference_hashes=v8.REFERENCE_HASHES,reference_registration=v8.REGISTRATION,
                central_architecture=central['architecture'],eye_architecture='embedded partial ellipsoid; 0.029 H sag; six lid loops',
                ear_architecture='UNCHANGED V008 TEMPORARY; Phase B not reached',
                hoof_architecture='UNCHANGED V008 TEMPORARY; Phase C not reached',
                geometry_digest=digest,meshes=meshes,
                central_topology=dict(connected_components=components,nonmanifold_edges=nonmanifold,all_quads=True,
                                      vertices=len(central.data.vertices),faces=len(central.data.polygons)),
                frozen_objects={n:changed[n] for n in frozen_names},
                motion_preflight='NOT_RUN; static prerequisite pending',
                torso_stations_frozen_from_X=.575,support_targets=v8.SUPPORT,
                production_rig=False,animation=False,fleece=False,glb_export=False,runtime=False)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    (directory/'measurements.json').write_text(json.dumps(result,indent=2)+'\n')
    for name in ['front','side','3q']:
        if name=='3q':cam=v8.camera('TEMP 3q',(-3,-3,1.3),(.62,0,.40))
        else:cam=bpy.data.objects['CAM '+name]
        scene.camera=cam
        assert v8.geometry_digest()==digest
        scene.render.filepath=str(directory/(('diagnostic-' if name=='3q' else 'skin-')+name+'.png'))
        bpy.ops.render.render(write_still=True)
        if name=='3q':bpy.data.objects.remove(cam,do_unlink=True)
    print('V009_PHASE_A_COMPLETE '+str(directory))


if __name__=='__main__':main()
