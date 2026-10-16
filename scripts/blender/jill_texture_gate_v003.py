"""Local-only Jill UV gate. Never changes the v002 source or runs Tripo.

Blender 5.2: --background --python this.py -- dump|build|owners
"""
import bpy, json, sys, hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-v002'
A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-technical-v003'
E=ROOT/'docs/production/jill/rig-pretexture-technical-v003'
A.mkdir(exist_ok=True); E.mkdir(exist_ok=True)
COMMAND=sys.argv[sys.argv.index('--')+1]
def write(n,x): (E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def open_source():
    bpy.ops.wm.open_mainfile(filepath=str(OLD/'jill-rig-pretexture-v002.blend'))
    return bpy.data.objects['Jill_Body'],bpy.data.objects['JILL_RIG']
def dump(o,label):
    m=o.data;m.calc_loop_triangles()
    np.savez_compressed(E/(label+'.npz'),xyz=np.array([v.co[:] for v in m.vertices]),
        tris=np.array([t.vertices[:] for t in m.loop_triangles]),
        loops=np.array([t.loops[:] for t in m.loop_triangles]),
        polygons=np.array([t.polygon_index for t in m.loop_triangles]),
        uv=np.array([x.uv[:] for x in m.uv_layers.active.data]),
        material=np.array([m.polygons[t.polygon_index].material_index for t in m.loop_triangles]))
def ownership(o):
    m=o.data;reg=np.load(ROOT/'docs/production/jill/rig-pretexture-v002/surface-contract.npz')['regions']
    comp=np.load(ROOT/'docs/production/jill/rig-other-v001/authority-parts.npz')['component']
    leaves={x['component']:x for x in json.loads((ROOT/'docs/production/jill/rig-other-v001/build-report.json').read_text())['leaves']}
    slots={};owners=[];oldmats=list(m.materials)
    for p in m.polygons:
        ci=int(comp[p.vertices[0]]) if max(p.vertices)<len(comp) else -1
        name=reg[p.index];original_mi=p.material_index
        if name=='original':
            if ci in [98,99]:name='eye_'+('L' if ci==99 else 'R')
            elif ci in [1,2,4]:name='wing_'+('R' if ci==1 else 'L')+'_'+('front' if p.normal.y<-.25 else 'back' if p.normal.y>.25 else 'edge')
            elif ci in leaves:
                leaf=leaves[ci];bone=leaf['bone'];gi=o.vertex_groups.get(bone)
                weight=sum(sum(g.weight for g in m.vertices[vi].groups if g.group==gi.index) for vi in p.vertices)/len(p.vertices) if gi else 1
                name='leaf_'+leaf['region']+'_'+leaf['side']+'_'+('root' if weight<.5 else 'surface')
            else:name='body_skin'
        if name not in slots:
            mat=oldmats[original_mi].copy();mat.name='JILL_'+name;slots[name]=len(m.materials);m.materials.append(mat)
            # Explicit UV0 binding prevents accidental fallback to preserved UV1/2.
            mat['paint_owner']=name;mat['uv_contract']='Jill_Texture_UV0_v003 / TEXCOORD_0'
        p.material_index=slots[name];owners.append(name)
    # Remove unused old slots; Blender remaps indices without changing faces.
    for i in range(len(oldmats)):m.materials.pop(index=0)
    write('material-ownership.json',{'polygon_owners':owners,'slots':[m.name for m in o.data.materials],
        'rule':'No shared atlas coordinates. Eyeballs, lids, skin, cavity, tongue, teeth are disjoint. Wing front/back/edge by rest normal y; includes frame. Leaf root by inherited owner weight <.5.',
        'hidden_faces':'All polygon owners have atlas coverage. Neutral camera visibility is not Tripo painting coverage. Use owner masks for explicit fill and inspect posed return.',
        'clover':'Body L/R require independent atlas regions; no mirroring permitted. Decorative placement still Human review.'})
if COMMAND=='dump':
    o,r=open_source();dump(o,'before')
    write('intake.json',{'blender':bpy.app.version_string,'uv_layers':[u.name for u in o.data.uv_layers],
        'active':o.data.uv_layers.active_index,'materials':[m.name for m in o.data.materials],
        'bones':len(r.data.bones),'morphs':[k.name for k in o.data.shape_keys.key_blocks][1:],
        'properties':list(json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())['authoring_properties']),
        'uv_operator_docs':bpy.ops.uv.pack_islands.__doc__+'\n'+bpy.ops.uv.smart_project.__doc__})
if COMMAND=='owners':
    bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-texture-uv-v003.blend'))
    o=bpy.data.objects['Jill_Body'];ownership(o)
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(A/'jill-rig-texture-uv-v003.blend'))
    dump(o,'after')
if COMMAND=='build':
    body,r=open_source();original_mesh=body.data
    # Use a bare temporary UV workspace: edit operators must not touch shape keys,
    # skin attributes or cached attributes on the production mesh.
    m=bpy.data.meshes.new('TEMP_UV_WORKSPACE');m.from_pydata([v.co[:] for v in original_mesh.vertices],[],[p.vertices[:] for p in original_mesh.polygons]);m.update()
    for p,q in zip(m.polygons,original_mesh.polygons):p.material_index=q.material_index
    o=bpy.data.objects.new('TEMP_UV_WORKSPACE',m);bpy.context.scene.collection.objects.link(o)
    for u in original_mesh.uv_layers:
        out=m.uv_layers.new(name=u.name);out.data.foreach_set('uv',np.array([x.uv[:] for x in u.data],dtype=np.float32).ravel())
    baseline_uv=[np.array([x.uv[:] for x in u.data]) for u in m.uv_layers]
    # Preserve BOTH preexisting layers verbatim. New active goes first for UV0.
    prior=m.uv_layers[0];prior.name='v002_Previous_Active_Preserved'
    active=m.uv_layers.new(name='Jill_Texture_UV0_v003')
    active.data.foreach_set('uv',baseline_uv[0].astype(np.float32).ravel())
    m.uv_layers.active_index=2;active.active_render=True
    reg=np.load(ROOT/'docs/production/jill/rig-pretexture-v002/surface-contract.npz')['regions']
    audit=json.loads((E/'before-uv-audit.json').read_text())
    bad=set(p for row in audit['overlap_examples'] for p in row['polygons'])
    # Only problematic donor polygons and added facial surfaces are reprojected.
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.context.tool_settings.mesh_select_mode=(False,False,True)
    def project(ids):
        print('PROJECT',len(ids),flush=True)
        bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='DESELECT');bpy.ops.object.mode_set(mode='OBJECT')
        for p in m.polygons:p.select=p.index in ids
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.smart_project(angle_limit=.65,island_margin=0,area_weight=0,correct_aspect=False,scale_to_bounds=False)
        bpy.ops.object.mode_set(mode='OBJECT')
    for region in sorted(set(reg)-{'original'}):project(set(np.flatnonzero(reg==region)))
    for bi,pi in enumerate(sorted(bad)):
        project({pi})
        # Separate the locally repaired face from former neighbouring UV edges.
        ids=list(m.polygons[pi].loop_indices);q=np.array([m.uv_layers.active.data[li].uv[:] for li in ids]);q=(q-q.min(0))/max(np.ptp(q,axis=0).max(),1e-12)
        for li,xy in zip(ids,q):m.uv_layers.active.data[li].uv=(xy[0]+2*(bi+1),xy[1]+2)
    # One inherited collinear geometric triangle is retained, but must have a
    # nondegenerate UV for interchange. Give its whole quad a convex UV outline.
    import math
    pi=14456;p=m.polygons[pi]
    for j,li in enumerate(p.loop_indices):m.uv_layers.active.data[li].uv=(200+math.cos(j*math.tau/len(p.vertices)),2+math.sin(j*math.tau/len(p.vertices)))
    for p in m.polygons:p.select=True
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.select_all(action='SELECT');bpy.ops.uv.average_islands_scale()
    bpy.ops.object.mode_set(mode='OBJECT')
    print('AVERAGED',flush=True)
    active=m.uv_layers.active
    # Eye detail gets a deliberate 2x linear density allocation, separately owned.
    for p in m.polygons:
        if p.material_index==1:
            for li in p.loop_indices:active.data[li].uv*=2
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(rotate=True,scale=True,merge_overlap=False,margin_method='FRACTION',margin=12/4096,shape_method='CONCAVE')
    bpy.ops.object.mode_set(mode='OBJECT')
    print('PACKED',flush=True)
    active=m.uv_layers.active
    # Small atlas edge gutter; preserve island aspect and packing distances.
    for x in active.data:x.uv=(x.uv.x*.996+.002,x.uv.y*.996+.002)
    # Blender export order is collection order, not active index. Recreate UVs with new atlas first.
    layers=[(u.name,np.array([x.uv[:] for x in u.data])) for u in m.uv_layers]
    while m.uv_layers:m.uv_layers.remove(m.uv_layers[-1])
    for name,arr in [layers[2],layers[0],layers[1]]:
        u=m.uv_layers.new(name=name);u.data.foreach_set('uv',arr.astype(np.float32).ravel())
    m.uv_layers.active_index=0;m.uv_layers[0].active_render=True
    assert np.array_equal(np.array([x.uv[:] for x in m.uv_layers[1].data]),baseline_uv[0])
    assert np.array_equal(np.array([x.uv[:] for x in m.uv_layers[2].data]),baseline_uv[1])
    while original_mesh.uv_layers:original_mesh.uv_layers.remove(original_mesh.uv_layers[-1])
    for u in m.uv_layers:
        out=original_mesh.uv_layers.new(name=u.name);out.data.foreach_set('uv',np.array([x.uv[:] for x in u.data],dtype=np.float32).ravel())
    original_mesh.uv_layers.active_index=0;original_mesh.uv_layers[0].active_render=True
    bpy.data.objects.remove(o,do_unlink=True);o=body;m=original_mesh
    ownership(o)
    o['texture_status']='v003 UV-only derivative. Original active and donor UV preserved exactly in layers 1/2. Human final GO pending.'
    r['status']='PRETEXTURE_TECHNICAL_REVIEW_V003 / HUMAN_FINAL_GO_PENDING'
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(A/'jill-rig-texture-uv-v003.blend'))
    dump(o,'after')
    write('uv-repair.json',{'reprojected_original_polygons':sorted(bad),'reprojected_regions':sorted(set(reg)-{'original'}),
        'geometry_changes':False,'old_active_exact':True,'source_uv_exact':True,'island_scale':'average surface area, eyes 2x linear',
        'padding_request':'12/4096 fraction, then global .996 scale and .002 offset','uv_order':[u.name for u in m.uv_layers]})
