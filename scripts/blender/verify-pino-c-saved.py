"""Read back saved Master and actual sample replay; verify Neutral and playback."""
import bpy,json,sys,importlib.util
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('pino_prove',Path(__file__).with_name('prove-pino-c-geometry.py'));u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
ASSET,OUT=u.ASSET,u.OUT
def arrays(o):return np.array([tuple(v.co) for v in o.data.vertices]),np.array([tuple(n.vector) for n in o.data.corner_normals])
original=u.u.load(ASSET/'source/cute blue creature 3d model.fbx');base,normal=arrays(original);records={}
for filename in ['pino-c-master-retained.blend','pino-c-master-derived-four-tests.blend']:
    bpy.ops.wm.open_mainfile(filepath=str(ASSET/filename));o=next(x for x in bpy.context.scene.objects if x.type=='MESH');scene=bpy.context.scene;scene.frame_set(1);v,n=arrays(o)
    exact=dict(local_vertices=bool(np.array_equal(v,base)),corner_normals=bool(np.array_equal(n,normal)));assert all(exact.values()),exact
    if 'four-tests' in filename:
        d=json.loads((OUT/'four-tests.json').read_text(encoding='utf-8'));rows=[x for r in d['runs'] for x in r['frames']];assert len(rows)==scene.frame_end
        playback=[];largest=0.;zeros=0;source_world_hash=d['runs'][0]['frames'][0]['world_vertex_sha256']
        for f,row in enumerate(rows,1):
            scene.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();evaluated=o.evaluated_get(dg);mesh=evaluated.to_mesh();coords=np.array([tuple(v.co) for v in mesh.vertices]);evaluated.to_mesh_clear()
            active=[k for k in o.data.shape_keys.key_blocks[1:] if k.value!=0]
            is_neutral=row['world_vertex_sha256']==source_world_hash
            if is_neutral:
                assert not active and np.array_equal(coords,base),(f,'Neutral mismatch');zeros+=1
            else:
                assert len(active)==1 and active[0].value==1,(f,'active key mismatch')
                expected=np.array([tuple(v.co) for v in active[0].data]);err=float(np.max(np.abs(coords-expected)));largest=max(largest,err);assert err<=6e-8,(f,err)
            playback.append(dict(frame=f,neutral=is_neutral,active_samples=len(active)))
        records['playback']=dict(frames=len(rows),exact_neutral_frames=zeros,nonzero_sample_evaluation_max_abs_error=largest,frames_verified=playback)
        scene.frame_set(1)
        for x in list(scene.objects):
            if x.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(x,do_unlink=True)
        cam=u.setup(o)
        for view in ['front','front-left','left']:u.render(cam,f'replay-neutral-{view}',view)
    records[filename]=exact
u.write_json(OUT/'saved-file-verification.json',records);print('Saved files / replay verified',records['playback']['frames'])
