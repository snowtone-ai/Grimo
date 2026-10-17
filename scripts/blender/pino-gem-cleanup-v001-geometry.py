"""Read-only surface correspondence diagnosis, never used for master transfer."""
import bpy,json,itertools
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/tripo-gem-cleanup-v001'
source=ROOT/'assets/grimo/production/pino/candidate-c/pretexture-reliability-v005/pino-c-v005-tripo-input.glb'
donor=ROOT/'assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v001/pino-c-v005-tripo-donor-original.glb'
def load(path):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path));rows={}
 for ob in bpy.data.objects:
  if ob.type!='MESH':continue
  role='oral' if 'Oral' in ob.name else 'lidL' if 'Lid' in ob.name and '_L' in ob.name else 'lidR' if 'Lid' in ob.name else 'main'
  p=np.array([ob.matrix_world@v.co for v in ob.data.vertices]);tri=np.array([list(f.vertices) for f in ob.data.polygons]);rows[role]=(p[tri],ob.name)
 return rows
s=load(source);d=load(donor);height=max(t[:,:,2].max() for t,n in s.values());scale=1/height
report={'source_height':float(height),'diagnostic_uniform_scale':float(scale),'changes_to_assets':False,'roles':{}}
perms=list(itertools.permutations(range(3)))
for role,(dt,name) in d.items():
 st=s[role][0]*scale;centers=st.mean(1);kd=KDTree(len(st))
 for i,p in enumerate(centers):kd.insert(Vector(p),i)
 kd.balance();matches=[];errors=[]
 for t in dt:
  candidates=[i for p,i,dist in kd.find_n(Vector(t.mean(0)),8)]
  score=np.array([[np.linalg.norm(st[i][list(perm)]-t,axis=1).max() for perm in perms] for i in candidates]);ci,pi=np.unravel_index(score.argmin(),score.shape);matches.append(candidates[ci]);errors.append(float(score[ci,pi]))
 report['roles'][role]={'source_faces':len(st),'donor_faces':len(dt),'unique_source_faces_matched':len(set(matches)),'max_vertex_error_after_diagnostic_scale':max(errors),'p95_vertex_error':float(np.percentile(errors,95)),'source_name':s[role][1],'donor_name':name,'all_faces_bijective':len(st)==len(dt)==len(set(matches))}
 if role=='oral':
  ob=bpy.data.objects[name];uv=np.array([tuple(x.uv) for x in ob.data.uv_layers.active.data]);np.savez(OUT/'oral-diagnostic.npz',triangles=dt,uv=uv.reshape(-1,3,2))
(OUT/'geometry-correspondence.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
