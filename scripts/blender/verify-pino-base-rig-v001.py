"""Reopen saved authoring/proof, check Neutral and compare fixed appearance.
Three matched Cycles views only; no frame dump and no runtime certification.
"""
import bpy,json,math,hashlib,sys
import numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/pino/candidate-c';D=A/'rig-v001';OUT=ROOT/'docs/production/pino/evidence/rig-v001'
REF=np.load(OUT/'reference-arrays.npz');V=REF['vertices'];local=REF['local']
def coords(o):
 bpy.context.view_layer.update();e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());return np.array([tuple(e.matrix_world@p.co) for p in e.data.vertices])
def dump(n,x):(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
results={}
for file in ['pino-c-base-rig-v001.blend','pino-c-base-rig-v001-proof.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(D/file));o=bpy.data.objects['PINO_C_BASE_RIG_V001'];rig=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001']
 r={'basis_exact':np.array_equal(np.array([p.co[:] for p in o.data.vertices]),local),'bone_count':len(rig.data.bones),'unassigned':sum(not v.groups for v in o.data.vertices),
 'weight_sum_max_error':max(abs(sum(g.weight for g in v.groups)-1) for v in o.data.vertices),'max_influences':max(len(v.groups) for v in o.data.vertices)}
 if 'proof' in file:
  timeline=json.loads((OUT/'proof-timeline.json').read_text());ends=[1,49,55,103,109,181,187,235]
  r['neutral_returns']=[]
  for frame in ends:
   bpy.context.scene.frame_set(frame);r['neutral_returns'].append({'frame':frame,'max_world_delta':float(np.linalg.norm(coords(o)-V,axis=1).max())})
  # Inspect actual interpolated transitions, not just keyed endpoints.
  samples=[4,10,64,118,166,196,208,220,232];r['transition_samples']=[]
  for frame in samples:
   bpy.context.scene.frame_set(frame);v=coords(o);r['transition_samples'].append({'frame':frame,'below_floor_vertices':int(np.sum(v[:,2]<-.001)),'min_z':float(v[:,2].min()),'finite':bool(np.isfinite(v).all()),'max_displacement':float(np.linalg.norm(v-V,axis=1).max())})
  records=json.loads((OUT/'deformation-metrics.json').read_text());errors=[]
  labels=REF['components']
  for record in records:
   bpy.context.scene.frame_set(record['frame']);v=coords(o)
   td=float(np.linalg.norm(v[np.isin(labels,[2,5])]-V[np.isin(labels,[2,5])],axis=1).max())
   ed={side:float(np.linalg.norm(v[labels==comp]-V[labels==comp],axis=1).max()) for side,comp in [('L',9),('R',8)]}
   errors.append({'frame':record['frame'],'tail_displacement_error':abs(td-record['tail_max_displacement']),'eye_displacement_error':max(abs(ed[s]-record['opposite_eye_displacement'][s]) for s in ed)})
  r['saved_keyed_pose_checks']=errors
 else:r['neutral_max_world_delta']=float(np.linalg.norm(coords(o)-V,axis=1).max())
 results[file]=r
dump('saved-verification.json',results)
assert all(r['basis_exact'] and r['unassigned']==0 and r['weight_sum_max_error']<1e-6 for r in results.values())
assert max(x['max_world_delta'] for x in results['pino-c-base-rig-v001-proof.blend']['neutral_returns'])<1e-6
assert max(max(e['tail_displacement_error'],e['eye_displacement_error']) for e in results['pino-c-base-rig-v001-proof.blend']['saved_keyed_pose_checks'])<1e-5
assert all(e['finite'] and e['below_floor_vertices']==0 for e in results['pino-c-base-rig-v001-proof.blend']['transition_samples'])
if '--quick' in sys.argv:sys.exit(0)
bpy.ops.wm.open_mainfile(filepath=str(D/'pino-c-base-rig-v001.blend'));mesh=bpy.data.objects['PINO_C_BASE_RIG_V001'];scene=bpy.context.scene;cam=scene.camera
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(A/'source/cute blue creature 3d model.glb'));ref=next(o for o in set(bpy.data.objects)-before if o.type=='MESH')
result={'reference_sha256':hashlib.sha256((A/'source/cute blue creature 3d model.glb').read_bytes()).hexdigest(),
 'mesh_local_positions_exact':np.array_equal(np.array([v.co[:] for v in ref.data.vertices]),local),
 'triangle_indices_exact':[tuple(p.vertices) for p in mesh.data.polygons]==[tuple(p.vertices) for p in ref.data.polygons],
 'corner_normals_exact':np.array_equal(np.array([n.vector[:] for n in ref.data.corner_normals]),np.array([n.vector[:] for n in mesh.data.corner_normals])),
 'uv_count':[len(mesh.data.uv_layers),len(ref.data.uv_layers)],'material_base_color':[list(o.data.materials[0].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value) for o in [mesh,ref]]}
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=False;scene.cycles.seed=41015;scene.render.resolution_x=512;scene.render.resolution_y=512
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.25,.30,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
for name,pos,power,size in [('Key',(-3,-4,5),450,4),('Fill',(3,-2,2),180,3)]:
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,.45))-o.location).to_track_quat('-Z','Y').to_euler();d.energy=power;d.shape='DISK';d.size=size
for view,dr in [('front',(0,-1,.04)),('side',(1,0,.025)),('threequarter',(1,-1,.1))]:
 dr=Vector(dr).normalized();cam.location=Vector((0,-.08,.47))+dr*3;cam.rotation_euler=(-dr).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.34
 for label,object in [('reference',ref),('candidate',mesh)]:
  ref.hide_render=object!=ref;mesh.hide_render=object!=mesh;scene.render.filepath=str(OUT/f'neutral-{label}-{view}.png');bpy.ops.render.render(write_still=True)
dump('neutral-reference-data.json',result)
print('PINO_VERIFY',json.dumps(results))
