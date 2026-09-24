"""Ear-only candidate. Run with Blender --background --python this-file.

Hand-authored asymmetric section cage; no fitting optimizer. Test shape keys
are provisional, zero at rest, and are not a production rig.
"""
import hashlib
import importlib.util
import json
import math
import struct
import sys
import tempfile
from pathlib import Path

import bpy
import bmesh
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/grimo/production/carol/blender/carol-hero-modules-v003.blend'
OUTPUT = SOURCE.with_name('carol-ear-production-v001.blend')
OUT = ROOT / 'docs/production/carol/evidence/ear-production-v001'
TMP = Path(tempfile.gettempdir()) / 'carol-ear-v001'
AUTH = ROOT / 'assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.png'
HEAD = 'f4c4d465b0adcb2ee8b7d95fe22aa9a3d4c878d5'
EARS = {'EAR_L', 'EAR_R'}
# u, upper, lower, anterior breadth, posterior breadth, anterior/posterior offset,
# pink upper border. Values are local H units, independently editable.
STATIONS = [
    (0.000, .040, -.036, .029, .031, .000, -.020),
    (0.014, .052, -.047, .034, .034, .000, -.022),
    (0.040, .055, -.085, .044, .040, .000, -.034),
    (0.085, .037, -.144, .057, .055, -.004, -.066),
    (0.145, .009, -.187, .071, .066, -.006, -.107),
    (0.210, -.022, -.235, .076, .070, -.003, -.117),
    (0.270, -.052, -.229, .075, .068, .002, -.110),
    (0.315, -.068, -.222, .077, .060, .007, -.125),
    (0.345, -.078, -.196, .073, .056, .010, -.175),
    (0.365, -.095, -.185, .056, .042, .012, -.169),
    (0.380, -.112, -.170, .027, .023, .012, -.159),
    (0.387, -.125, -.154, .012, .010, .012, -.148),
]
ROOT_POS = Vector((.352, .205, .566))
SWEEP = math.radians(35)
NC = 16


def local_cage():
    vertices = []
    for u, top, bottom, front, back, offset, pink in STATIONS:
        depth_gain=1+.20*min(1,u/.085)
        front*=depth_gain;back*=depth_gain
        height = top-bottom
        rim = min(.016, height*.17)
        lower_pink=bottom+rim
        pink = max(lower_pink+.0008, min(top-rim, pink))
        basin = min(.008, front*.16, height*.06,(pink-lower_pink)*.22)
        # Closed non-elliptical perimeter: convex back, rounded lower rim,
        # recessed pink basin, overhanging upper brown cushion, soft crown.
        section = [
            (0, top), (.70*back, top-height*.12), (back, top-height*.42),
            (.82*back, bottom+height*.18), (.28*back, bottom),
            (-front*.58, bottom), (-front*.94, bottom+rim*.45),
            (-front, lower_pink), (-front+basin*.65, lower_pink+(pink-lower_pink)*.20),
            (-front+basin, (lower_pink+pink)/2),
            (-front+basin*.65, lower_pink+(pink-lower_pink)*.80), (-front, pink),
            (-front-rim*.20, pink+rim*.65),
            (-front*.94, pink+(top-pink)*.48),
            (-front*.60, top-height*.08), (-front*.22, top),
        ]
        vertices.extend((offset+x, u, z+.040*u/.387) for x,z in section)
    faces, mats = [], []
    for i in range(len(STATIONS)-1):
        for j in range(NC):
            a=i*NC+j; b=i*NC+(j+1)%NC
            faces.append((a,b,b+NC,a+NC))
            mats.append(1 if 7 <= j <= 10 and i < 9 else 0)
    faces.extend([tuple(reversed(range(NC))), tuple((len(STATIONS)-1)*NC+j for j in range(NC))])
    mats.extend([0,0])
    return vertices, faces, mats


def posed_local(vertices, lift=0, turn=0):
    # Integrate rotated spine segments; rigidly rotate each cross section.
    # First two root stations stay fixed. Rotation grows toward the soft tip.
    spines=[]; rotations=[]
    for i, station in enumerate(STATIONS):
        u=station[0]; t=max(0,(u-.04)/(.387-.04)); w=t*t*(3-2*t)
        rot=Matrix.Rotation(math.radians(turn)*w,3,'Z') @ Matrix.Rotation(math.radians(lift)*w,3,'X')
        neutral=Vector((0,u,-math.tan(math.radians(18))*u))
        if i == 0: spine=neutral
        else:
            prev=STATIONS[i-1][0]
            segment=Vector((0,u-prev,-math.tan(math.radians(18))*(u-prev)))
            spine=spines[-1]+((rot+rotations[-1])*.5) @ segment
        spines.append(spine); rotations.append(rot)
    result=[]
    for index, point in enumerate(vertices):
        i=index//NC; u=STATIONS[i][0]
        neutral=Vector((0,u,-math.tan(math.radians(18))*u))
        result.append(spines[i]+rotations[i] @ (Vector(point)-neutral))
    return result


def world(point, sign):
    x,u,z=point
    return Vector((ROOT_POS.x+x*math.cos(SWEEP)+u*math.sin(SWEEP),
                   sign*(ROOT_POS.y-x*math.sin(SWEEP)+u*math.cos(SWEEP)), ROOT_POS.z+z))


def snapshot(ob):
    h=hashlib.sha256()
    if ob.type=='MESH':
        for v in ob.data.vertices: h.update(struct.pack('<3f',*v.co))
        for p in ob.data.polygons:
            h.update(struct.pack('<II',len(p.vertices),p.material_index))
            for i in p.vertices: h.update(struct.pack('<I',i))
        if ob.data.shape_keys:
            for key in ob.data.shape_keys.key_blocks:
                for v in key.data: h.update(struct.pack('<3f',*v.co))
    return {'matrix': [round(x,7) for row in ob.matrix_world for x in row],
            'mesh_and_shape_keys':h.hexdigest(),
            'counts':[len(ob.data.vertices),len(ob.data.polygons)] if ob.type=='MESH' else None,
            'materials':[m.name if m else None for m in ob.data.materials] if ob.type=='MESH' else [],
            'parent':ob.parent.name if ob.parent else None,
            'modifiers':[(m.name,m.type) for m in ob.modifiers]}


def material(name,color):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=.48
    p.inputs['Subsurface Weight'].default_value=.045
    return m


def mesh_check(ob):
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)
    bpy.context.view_layer.update()
    dep=bpy.context.evaluated_depsgraph_get()
    ev=ob.evaluated_get(dep);mesh=ev.data
    bm=bmesh.new();bm.from_mesh(mesh)
    nonmanifold=sum(not e.is_manifold for e in bm.edges)
    signed_volume=bm.calc_volume(signed=True);volume=abs(signed_volume);bm.free()
    mesh.calc_loop_triangles()
    tris=[tuple(t.vertices) for t in mesh.loop_triangles]
    tree=BVHTree.FromPolygons([v.co for v in mesh.vertices],tris,all_triangles=True,epsilon=0)
    crosses={(min(a,b),max(a,b)) for a,b in tree.overlap(tree)
             if a!=b and not set(tris[a]).intersection(tris[b])}
    result={'finite':all(math.isfinite(c) for v in mesh.vertices for c in v.co),
            'nonmanifold_edges':nonmanifold,'nonadjacent_triangle_intersections':len(crosses),
            'volume_H3':volume,'outward_normals':signed_volume>0,'evaluated_vertices':len(mesh.vertices)}
    return result


def render(name,direction,target,scale,visible=None,size=(640,640),up='Y',roll=0):
    scene=bpy.context.scene;oldcam=scene.camera
    scene.frame_set(scene.frame_current)
    states={o.name:o.hide_render for o in bpy.data.objects}
    if visible is not None:
        for o in bpy.data.objects:
            if o.type in {'MESH','CURVE','SURFACE'}:o.hide_render=o.name not in visible
    data=bpy.data.cameras.new('TEMP ear evidence');cam=bpy.data.objects.new('TEMP ear evidence',data)
    scene.collection.objects.link(cam);cam.location=Vector(target)+Vector(direction)
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z',up).to_euler()
    if roll:cam.rotation_euler=(cam.rotation_euler.to_matrix() @ Matrix.Rotation(roll,3,'Z')).to_euler()
    data.type='ORTHO';data.ortho_scale=scale;scene.camera=cam
    scene.render.resolution_x,scene.render.resolution_y=size
    scene.render.resolution_percentage=100;scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.render.filepath=str(TMP/(name+'.png'));bpy.ops.render.render(write_still=True)
    scene.camera=oldcam;bpy.data.objects.remove(cam,do_unlink=True)
    for n,h in states.items():bpy.data.objects[n].hide_render=h


def main():
    OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((AUTH.parents[1]/'authority.json').read_text())
    sha=hashlib.sha256(AUTH.read_bytes()).hexdigest()
    entry=next(x for x in manifest['authorityOrder'] if x['role']=='localized_ear_module_authority')
    assert sha==entry['sha256'].lower()
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));bpy.context.scene.frame_set(1)
    frozen={o.name:snapshot(o) for o in bpy.data.objects if o.name not in EARS}
    brown=material('CAROL ear production cocoa',(.12,.035,.015))
    pink=material('CAROL ear production seated blush',(.75,.16,.135))
    vertices,faces,mats=local_cage()
    for sign,suffix in [(1,'L'),(-1,'R')]:
        ob=bpy.data.objects['EAR_'+suffix];ob.shape_key_clear();ob.vertex_groups.clear();ob.modifiers.clear()
        mesh=bpy.data.meshes.new('Carol asymmetric ear cage '+suffix)
        mesh.from_pydata([world(v,sign) for v in vertices],[],faces);mesh.update()
        mesh.materials.append(brown);mesh.materials.append(pink)
        for p,m in zip(mesh.polygons,mats):p.material_index=m;p.use_smooth=True
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(mesh);bm.free()
        ob.data=mesh
        for region,center in [('ROOT',0),('PROXIMAL',.22),('MID',.50),('DISTAL',.78),('TIP',1)]:
            group=ob.vertex_groups.new(name=region)
            for i,v in enumerate(vertices):
                weight=max(0,1-abs(v[1]/.387-center)/.28)
                if weight:group.add([i],weight,'REPLACE')
        ob.shape_key_add(name='Basis',from_mix=False).value=0
        for name,lift,turn in [('TEST lift',12,0),('TEST droop',-14,0),('TEST attention flick',5,12)]:
            key=ob.shape_key_add(name=name,from_mix=False);key.value=0
            for p,v in zip(key.data,posed_local(vertices,lift,turn)):p.co=world(v,sign)
        mod=ob.modifiers.new('Editable soft ear surface','SUBSURF');mod.levels=2;mod.render_levels=2
        ob['ear_controls']='PROVISIONAL TEST shape keys; independent L/R; zero at neutral. Not a production rig.'
        ob['local_axes']='u=root to tip; x=posterior; z=up. R reflects Y, with recalculated outward normals.'
        ob['root_position_H']=list(world((0,0,0),sign))
    bpy.context.view_layer.update()
    assert all(snapshot(bpy.data.objects[n])==s for n,s in frozen.items())
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT));bpy.ops.wm.open_mainfile(filepath=str(OUTPUT))
    assert all(snapshot(bpy.data.objects[n])==s for n,s in frozen.items())
    checks={};ear=bpy.data.objects['EAR_R']
    for pose in ['Basis','TEST lift','TEST droop','TEST attention flick']:
        if pose!='Basis':ear.data.shape_keys.key_blocks[pose].value=1
        checks[pose]=mesh_check(ear)
        if pose!='Basis':ear.data.shape_keys.key_blocks[pose].value=0
    left=bpy.data.objects['EAR_L'];right=bpy.data.objects['EAR_R']
    mirror=max((Vector((a.co.x,-a.co.y,a.co.z))-b.co).length for a,b in zip(left.data.vertices,right.data.vertices))
    bpy.context.view_layer.update()
    head_tree=BVHTree.FromObject(bpy.data.objects['CENTRAL_CHASSIS'],bpy.context.evaluated_depsgraph_get())
    roots={}
    for sign,ob in [(1,left),(-1,right)]:
        root=world((0,0,.002),sign)
        nearest,normal,_,distance=head_tree.find_nearest(root)
        roots[ob.name]={'root_center_inside_head':(root-nearest).dot(normal)<0,
                       'root_center_surface_distance_H':distance,
                       'test_root_station_max_displacement_H':max((k.data[i].co-ob.data.vertices[i].co).length
                           for k in ob.data.shape_keys.key_blocks for i in range(NC*3))}
    for value in checks.values():value['volume_ratio_to_neutral']=value['volume_H3']/checks['Basis']['volume_H3']
    image=bpy.data.images.load(str(AUTH),check_existing=False);dimensions=list(image.size);bpy.data.images.remove(image)
    validation={'source_branch':'origin/codex/carol-hero-modules-v003','source_head':HEAD,
                'donor':str(SOURCE.relative_to(ROOT)).replace('\\','/'),
                'donor_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                'authority_sha256':sha,'authority_dimensions':dimensions,
                'output_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                'changed_objects':sorted(EARS),'frozen_objects':{'count':len(frozen),'equal_after_reload':True,
                    'record_sha256':{n:hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest() for n,v in frozen.items()}},
                'same_geometry_all_views':True,'cage_vertices_per_ear':len(vertices),
                'pink_same_closed_mesh':True,'mirror_max_error_H':mirror,
                'positive_scale':all(min(o.scale)>0 for o in [left,right]),'poses':checks,'attachment':roots,
                'neutral_test_controls_zero':all(k.value==0 for o in [left,right] for k in o.data.shape_keys.key_blocks),
                'front_root_to_tip_station_angle_degrees':math.degrees(math.atan2(.1015,.387*math.cos(SWEEP)-.012*math.sin(SWEEP))),
                'human_review':'REQUIRED; no perceptual approval claimed'}
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    assert all(c['finite'] and c['outward_normals'] and c['nonmanifold_edges']==0 and c['nonadjacent_triangle_intersections']==0 for c in checks.values()), checks
    assert all(r['root_center_inside_head'] and r['test_root_station_max_displacement_H']<1e-6 for r in roots.values()), roots
    scene=bpy.context.scene;scene.cycles.samples=32;scene.cycles.use_denoising=True
    # Module cameras use the ear's local spatial frame; attached views use world axes.
    center=world((0,.19,-.074),1)
    dfront=Vector((-math.cos(SWEEP),math.sin(SWEEP),0))
    dside=Vector((math.sin(SWEEP),math.cos(SWEEP),0))
    for label,d in [('front',dfront*4),('side',-dside*4),('top',Vector((0,0,4))),('3q',-dside*2+dfront*3+Vector((0,0,.7)))]:
        if label=='top':
            # Top camera uses the same physical ear; roll aligns root on right.
            render('ear-'+label,d,center,.49,{'EAR_L'},roll=-math.pi/2-SWEEP)
        else:render('ear-'+label,d,center,.49,{'EAR_L'})
    render('attached-front',(-4,0,0),(.50,0,.46),1.37,size=(960,900))
    render('attached-side',(0,-4,0),(.56,0,.46),1.48,size=(1080,900))
    ear=left
    for label,pose in [('neutral',None),('lift','TEST lift'),('droop','TEST droop'),('attention','TEST attention flick')]:
        if pose:ear.data.shape_keys.key_blocks[pose].value=1
        render('pose-'+label,dfront*4,center,.49,{'EAR_L'},size=(500,500))
        if pose:ear.data.shape_keys.key_blocks[pose].value=0
    # Existing fleece is loaded only for diagnostic renders, after the candidate
    # was saved. It is not accepted geometry and is not added to the output blend.
    probe=SOURCE.with_name('carol-hero-experience-probe-v001.blend')
    with bpy.data.libraries.load(str(probe),link=False) as (src,dst):
        dst.objects=['DONOR Carol_Fleece_Continuous']
    fleece=dst.objects[0];scene.collection.objects.link(fleece)
    scene.frame_set(1)
    render('fleece-front',(-4,0,0),(.50,0,.46),1.37,size=(640,600))
    render('fleece-side',(0,-4,0),(.56,0,.46),1.48,size=(720,600))
    print('EAR_PRODUCTION_COMPLETE',json.dumps({'frozen':len(frozen),'checks':checks}))


if __name__=='__main__':main()
