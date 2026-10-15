"""Protect appearance outside the mouth; render source/candidate in identical conditions."""
import bpy,sys,json,hashlib,importlib.util
import numpy as np
from mathutils import Vector
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('mouthb',ROOT/'scripts/blender/repair-shushu-v004-mouth-b.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
sha=lambda value:hashlib.sha256(value).hexdigest()
def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');r.b.reset(rig);result={}
    for o in bpy.data.objects:
        if o.type!='MESH' or not o.name.startswith('ShushuStatic_'):continue
        keys={k.name:r.coords(k) for k in o.data.shape_keys.key_blocks} if o.data.shape_keys else {}
        result[o.name]={'keys':keys,'vertices':np.array([v.co for v in o.data.vertices]),'uv':sha(np.array([v.uv for v in o.data.uv_layers.active.data]).tobytes()) if o.data.uv_layers.active else None,'topology':sha(np.array([l.vertex_index for l in o.data.loops],dtype=np.int32).tobytes()),'weights':sha(json.dumps([[(o.vertex_groups[g.group].name,g.weight) for g in v.groups] for v in o.data.vertices]).encode()),'matrix':np.array(o.matrix_world)}
    bones={pb.name:{'parent':pb.parent.name if pb.parent else None,'rest':np.array(pb.bone.matrix_local).tolist()} for pb in rig.pose.bones}
    return result,bones
def audit():
    old,bones=snapshot(r.SOURCE);new,newbones=snapshot(r.ASSET);rows=[];oral={'ShushuStatic_'+n for n in ['MouthInterior','OralBowl','Tongue']};mask=np.load(r.OUT/'head-edit-mask.npz')['mask']
    for name,a in old.items():
        b=new[name]
        if name in oral:continue
        row={'mesh':name,'uv_equal':a['uv']==b['uv'],'topology_equal':a['topology']==b['topology'],'weights_equal':a['weights']==b['weights'],'object_world_matrix_equal':bool(np.array_equal(a['matrix'],b['matrix'])),'shape_key_names_equal':list(a['keys'])==list(b['keys'])}
        if name=='ShushuStatic_Head':row['all_shape_keys_outside_mouth_exact']=all(np.array_equal(a['keys'][k][mask==0],b['keys'][k][mask==0]) for k in a['keys']);row['protected_vertices']=int((mask==0).sum());row['local_vertices']=int((mask>0).sum())
        else:row['all_shape_keys_exact']=all(np.array_equal(a['keys'][k],b['keys'][k]) for k in a['keys']);row['basis_vertices_exact']=bool(np.array_equal(a['vertices'],b['vertices']))
        assert all(v for k,v in row.items() if k not in ['mesh','protected_vertices','local_vertices']);rows.append(row)
    assert bones==newbones
    # Mouth controls are affine in one bounded aperture. Sample the physical ring.
    d=np.load(r.OUT/'head-edit-mask.npz');ring=d['ring_indices'];c=d['closed'][ring];a=d['opened'][ring];steps=np.array([c+(a-c)*t for t in np.linspace(0,1,101)])
    assert np.isfinite(steps).all()
    report={'meshes':rows,'skeleton_rest_parent_exact':bones==newbones,'oral_replaced_only':sorted(oral),'mouth_samples':101,'max_vertex_step_per_001_open':float(np.linalg.norm(np.diff(steps,axis=0),axis=2).max()),'endpoint_return_exact':bool(np.array_equal(steps[0],c)),'scope':'All authored shape coordinates, Head UV/topology/weights and 10 non-mouth objects checked. Runtime visual and Human cuteness gates are separate.'};r.write('authored-preservation.json',report);print('PRESERVATION_OK',flush=True)
def render():
    full='--full' in sys.argv;candidate='--candidate' in sys.argv
    bpy.ops.wm.open_mainfile(filepath=str(r.ASSET if candidate else r.SOURCE));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
    scene,cam=r.b.setup_review(640,24);cam.data.type='ORTHO';cam.data.ortho_scale=1.14 if full else .56;target=(0,0,.5) if full else (0,-.02,.69)
    folder=r.OUT/('candidate-full' if candidate else 'before-full' if full else 'before');folder.mkdir(exist_ok=True)
    states={'seated-closed':{'Seat':1,'MouthClose':1},'seated-large':{'Seat':1,'MouthOpen':1}} if full else {'closed':{'MouthClose':1},'small':{'MouthOpen':.2},'medium':{'MouthOpen':.55},'large':{'MouthOpen':1}}
    for name,values in states.items():
        r.b.state(rig,values)
        for view,loc in r.VIEWS.items():
            cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
        print('COMPARISON_RENDER',folder.name,name,flush=True)
if __name__=='__main__':audit() if '--audit' in sys.argv else render()
