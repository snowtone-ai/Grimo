"""Targeted post-reload geometry and visible Front eye-aperture diagnostics."""
import hashlib
import json
import math
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/hero-modules-v003'
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-hero-modules-v003.blend'
bpy.ops.wm.open_mainfile(filepath=str(ASSET))
report=json.loads((OUT/'validation.json').read_text(encoding='utf8'))
assert hashlib.sha256(ASSET.read_bytes()).hexdigest()==report['output_blend_sha256']


def topology(ob):
    bm=bmesh.new();bm.from_mesh(ob.data)
    bad=sum(1 for e in bm.edges if not e.is_manifold)
    remaining=set(bm.verts);components=0
    while remaining:
        components+=1
        stack=[remaining.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                other=e.other_vert(v)
                if other in remaining:
                    remaining.remove(other);stack.append(other)
    bm.free()
    return {'boundary_or_nonmanifold_edges':bad,'connected_components':components,
            'vertices':len(ob.data.vertices),'faces':len(ob.data.polygons)}


checks={n:topology(bpy.data.objects[n]) for n in
        ['EAR_L','EAR_R','HOOF_FORE_L','HOOF_FORE_R','HOOF_HIND_L','HOOF_HIND_R']}
assert all(v['boundary_or_nonmanifold_edges']==0 and v['connected_components']==1 for v in checks.values())
report['topology']=checks


def tree_for(ob):
    deps=bpy.context.evaluated_depsgraph_get()
    evaluated=ob.evaluated_get(deps)
    mesh=evaluated.to_mesh()
    tree=BVHTree.FromPolygons([v.co.copy() for v in mesh.vertices],
                              [list(p.vertices) for p in mesh.polygons])
    evaluated.to_mesh_clear()
    return tree


chassis=tree_for(bpy.data.objects['CENTRAL_CHASSIS'])
visible={}
step=.0005
for side,sign in [('L',1),('R',-1)]:
    eye=tree_for(bpy.data.objects['EYE_'+side])
    lid=tree_for(bpy.data.objects['EYELID_'+side])
    center=sign*.162
    ys=[];zs=[]
    for iy in range(297):
        y=center-.074+iy*step
        for iz in range(321):
            z=.418-.080+iz*step
            origin=Vector((-1,y,z));direction=Vector((1,0,0))
            e=eye.ray_cast(origin,direction)[3]
            if e is None:continue
            l=lid.ray_cast(origin,direction)[3]
            c=chassis.ray_cast(origin,direction)[3]
            if e+1e-5<min([v for v in (l,c) if v is not None] or [float('inf')]):
                ys.append(y);zs.append(z)
    visible[side]={'width_H':round(max(ys)-min(ys)+step,5),
                   'height_H':round(max(zs)-min(zs)+step,5),
                   'center_y_H':round((min(ys)+max(ys))/2,5),
                   'center_z_H':round((min(zs)+max(zs))/2,5)}
report['eye_metrics']['raycast_visible_front']=visible
report['eye_metrics']['front_aperture_within_tolerance']=all(
    abs(v['width_H']-.137)<=.0015 and abs(v['height_H']-.149)<=.0015 and
    abs(abs(v['center_y_H'])-.162)<=.0015 for v in visible.values())
# Geometric side silhouette check: the optical shell remains behind the
# anterior head profile across the eye-height band in the neutral pose.
head_x=min(v.co.x for v in bpy.data.objects['CENTRAL_CHASSIS'].data.vertices if .34<=v.co.z<=.50)
eye_x=min(v.co.x for s in ('L','R') for v in bpy.data.objects['EYE_'+s].data.vertices)
report['eye_metrics']['side_silhouette_bulge_H']=round(max(0,head_x-eye_x),5)
ear=report['ear_parameters'];hoof=report['hoof_parameters']
report['ear_angle_degrees']=round(math.degrees(math.atan2(ear['drop'],ear['lateral'])),4)
hoof_bounds=report['module_records']['HOOF_FORE_R']['world_bounds']
report['hoof_visible_width_H']=round(hoof_bounds['max'][1]-hoof_bounds['min'][1],5)
report['hoof_visible_crown_H']=hoof['crown']
report['hoof_full_mesh_height_H']=round(hoof_bounds['max'][2]-hoof_bounds['min'][2],5)
report['final_disposition']='STALLED_PARAMETERIZATION'
report['executor_visual_precheck']='REJECTED: ear Front/Side/Top and hoof Top remain visibly unlike localized authority.'
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps({'topology':checks,'eye':report['eye_metrics']},indent=2),flush=True)
