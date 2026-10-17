"""Diagnose oral/exterior overlap in the donor; no source or Master writes."""
import bpy,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/pino/evidence/tripo-gem-cleanup-v002'
DONOR=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v001/pino-c-v005-tripo-donor-original.glb'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(DONOR))
main=bpy.data.objects['PINO_C_BASE_RIG_V001_TRIPO_INPUT'];oral=bpy.data.objects['PinoOralLiner_TRIPO_INPUT']
bvh=BVHTree.FromPolygons([main.matrix_world@v.co for v in main.data.vertices],[list(f.vertices) for f in main.data.polygons],all_triangles=True)
p=np.array([oral.matrix_world@v.co for v in oral.data.vertices]);tri=np.array([list(f.vertices) for f in oral.data.polygons]);hits=[]
for v in p:
 hit,normal,face,dist=bvh.ray_cast(Vector((v[0],-.65,v[2])),Vector((0,1,0)),1.3)
 hits.append(list(hit) if hit is not None else [float('nan')]*3)
hits=np.array(hits);gap=p[:,1]-hits[:,1]
repaired=p.copy();clearance=.001
# Resolve only observed front contact, preserving the deeper regular cavity.
# Do not bury legitimate interior surfaces merely to match an oral-hidden control.
repaired[:,1]=np.maximum(p[:,1],hits[:,1]+clearance)
report={'oral_vertices':len(p),'ray_hits':int(np.isfinite(gap).sum()),'front_depth_gap_min':float(np.nanmin(gap)),'front_depth_gap_max':float(np.nanmax(gap)),'vertices_within_0_1mm_of_exterior':int((abs(gap)<.0001).sum()),'vertices_in_front_of_exterior':int((gap<0).sum()),'method':'front ray against existing main surface; diagnosis only, never Rig return'}
report.update({'clearance_target':clearance,'post_min_vertex_front_clearance':float((repaired[:,1]-hits[:,1]).min()),'moved_vertices':int(((repaired-p)[:,1]>1e-9).sum()),'max_depth_change':float((repaired-p)[:,1].max()),'cavity_not_forced_invisible':True})
assert (repaired[:,1]-hits[:,1]).min()>.00099
np.savez(OUT/'oral-contact.npz',positions=p,triangles=tri,front_hits=hits,repaired_positions=repaired,uv=np.array([tuple(v.uv) for v in oral.data.uv_layers.active.data]).reshape(-1,3,2))
(OUT/'overlap-diagnosis.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(report,indent=2))
