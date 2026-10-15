"""Package exact tested mesh samples, without repeating valid deformation renders.

Recheck every nonzero sample's recorded float64 hash; use a literal source copy
at zero strength to remove formula roundoff. This is diagnostic replay, not a rig.
"""
import bpy,json,hashlib,importlib.util,sys
from pathlib import Path
import numpy as np
from mathutils import Vector
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('pino_exercise',Path(__file__).with_name('exercise-pino-c-geometry.py'));e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
OUT,ASSET=e.OUT,e.ASSET;data=json.loads((OUT/'four-tests.json').read_text(encoding='utf-8'));normalizations=[];rechecked=0;samples=[]
def calculate(kind,s):
    if kind=='tail':return e.u.deform('tail',s)
    if kind=='eyes-L':return e.eyes(s,0)
    if kind=='eyes-R':return e.eyes(0,s)
    if kind=='eyes-both':return e.eyes(s,s)
    if kind=='raise-L':return e.arm_pose([1],s)
    if kind=='raise-R':return e.arm_pose([-1],s)
    if kind=='both':return e.arm_pose([1,-1],s,75)
    if kind=='food':return e.arm_pose([1],s,30)
    return e.rest(s)
for r in data['runs']:
    name,kind=r['name'],r['kind'];meta=e.create_fixture(name,calculate(kind,1));changed=[]
    for row in r['frames']:
        v=calculate(kind,row['strength']);h=hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()
        if row['strength']!=0:
            assert h==row['world_vertex_sha256'],(name,row['frame']);rechecked+=1
        elif h!=row['world_vertex_sha256']:
            old=row['world_vertex_sha256'];i=row['frame'];e.write_vertices(v)
            before={view:e.u.sha(e.MOTION/f'{name}-{i:03d}-{view}.png') for view in ['front','threequarter','side']}
            m=e.metrics(v,'tail' if kind=='tail' else kind,0);m.update(frame=i,strength=0.,fixture=e.fixture_metrics(v,meta));row.clear();row.update(m)
            for view in ['front','threequarter','side']:e.render_frame(name,i,view)
            changed.append(dict(frame=i,old_formula_sha256=old,exact_source_sha256=h,old_render_hashes=before,new_render_hashes={view:e.u.sha(e.MOTION/f'{name}-{i:03d}-{view}.png') for view in before}))
        samples.append((name,row['frame'],v))
    normalizations.append(dict(sequence=name,initial_formula_return_flag=r['neutral_return_exact'],changes=changed));r['neutral_return_exact']=bool(np.array_equal(calculate(kind,0),e.V))
if e.fixture:bpy.data.objects.remove(e.fixture,do_unlink=True);e.fixture=None
e.write_vertices(e.V);e.o.shape_key_add(name='Basis');frame=1
for name,i,v in samples:
    if i==0:bpy.context.scene.timeline_markers.new(name,frame=frame)
    if not np.array_equal(v,e.V):
        k=e.o.shape_key_add(name=f'sample-{frame:03d}-{name}')
        for vi,p in enumerate(v):k.data[vi].co=e.INV@Vector(p)
        for f,value in [(frame-1,0),(frame,1),(frame+1,0)]:k.value=value;k.keyframe_insert('value',frame=f)
    frame+=1
scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=frame-1;scene.render.fps=8;scene.frame_set(1)
scene['purpose']='Replay of actual tested duplicate-mesh samples; no production rig or approved motion'
scene['sole_geometry_master']=data['master']['source'];scene['appearance_reference']='original GLB; static derived export verified separately';scene['human_geometry_gate']='PENDING'
e.write_vertices(e.V)
exact=dict(local_vertices=np.array_equal(np.array([tuple(v.co) for v in e.me.vertices]),e.BASE_LOCAL),corner_normals=np.array_equal(np.array([tuple(n.vector) for n in e.me.corner_normals]),e.NORMAL_START))
assert all(exact.values()),exact
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'pino-c-master-derived-four-tests.blend'))
# Correct the half-eye endpoint supplement; all moving half-eye frames already used .5.
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.view_settings.exposure=-.3;e.write_vertices(e.eyes(.5,.5))
for view in ['front','threequarter','side']:e.render_frame('cycles-eyes-half',0,view)
e.write_vertices(e.V)
report=dict(nonzero_sample_hashes_rechecked=rechecked,replay_frames=len(samples),neutral_restoration_exact=exact,neutral_formula_normalization=normalizations,
    explanation='Zero-strength formulas had floating point subtract/add residue in initial diagnostic calculations. Use literal original vertices for zero strength. Saved source Neutral was already restored exactly. No nonzero trial was changed or rerun.',
    endpoint_correction='Half-eye Cycles supplement now uses .5 closure, matching its original actual moving trial.',human_geometry_gate='PENDING')
e.u.write_json(OUT/'replay-verification.json',report);data['replay_package']='replay-verification.json';e.u.write_json(OUT/'four-tests.json',data)
print('Replay verified:',len(samples),rechecked,exact)
