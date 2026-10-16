"""Saved-blend/static-GLB reimport checks for changed texture/face risks."""
import bpy,json,sys,importlib.util,hashlib,struct
from pathlib import Path
import numpy as np
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/texture-return-v005';A=ROOT/'assets/grimo/production/jill/tripo/texture-return-v005'
spec=importlib.util.spec_from_file_location('review',ROOT/'scripts/blender/jill-texture-review-v005.py')
# Read only helper declarations: importing the driver would execute a CLI mode.
import ast
tree=ast.parse((ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8'))
code=ast.Module(body=[n for n in tree.body if not(isinstance(n,ast.If) and isinstance(n.test,ast.Compare)) and not(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='cmd' for t in n.targets))],type_ignores=[])
ns={ '__file__':str(ROOT/'scripts/blender/jill-texture-review-v005.py')};exec(compile(code,'<review helpers>','exec'),ns)
bpy.ops.wm.open_mainfile(filepath=str(A/'jill-textured-rig-v005.blend'));o=bpy.data.objects['Jill_Body'];r=bpy.data.objects['JILL_RIG'];r.animation_data.action=None
def xyz(ob):
    ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();q=np.array([list(ob.matrix_world@v.co) for v in me.vertices]);ev.to_mesh_clear();return q
expected={};morphs={};states=['neutral','blink-half','blink-full','mouth-closed','mouth-small','mouth-large','recovery']
for state in states:
    ns['pose'](r,ns['STATES'][state]);expected[state]=xyz(o);morphs[state]={k.name:float(k.value) for k in o.data.shape_keys.key_blocks[1:]}
ns['pose'](r,{})
uvtrees={};source_rows={}
for mat in o.data.materials:
    owner=mat.get('paint_owner');rows=[(o.data.loops[li].vertex_index,list(o.data.uv_layers[0].data[li].uv)) for p in o.data.polygons if o.data.materials[p.material_index]==mat for li in p.loop_indices]
    kd=KDTree(len(rows))
    for i,(vi,uv) in enumerate(rows):kd.insert((*uv,0),i)
    kd.balance();uvtrees[owner]=kd;source_rows[owner]=rows
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(A/'jill-textured-rig-v005.glb'))
meshes=[x for x in bpy.context.scene.objects if x.type=='MESH' and any(mod.type=='ARMATURE' for mod in x.modifiers)];rigs=[x for x in bpy.context.scene.objects if x.type=='ARMATURE'];anchors=[x for x in bpy.context.scene.objects if x.name.startswith('ANCHOR_')]
print('REIMPORT_MESHES',[(x.name,len(x.data.materials),len(x.data.vertices)) for x in meshes],flush=True)
bindings={};uvmax=0.;missing=[];covered=set()
for ob in meshes:
    pos=xyz(ob);byvertex={}
    for p in ob.data.polygons:
        owner=ob.data.materials[p.material_index].get('paint_owner');assert owner in uvtrees,owner
        for li in p.loop_indices:
            vi=ob.data.loops[li].vertex_index;uv=ob.data.uv_layers[0].data[li].uv
            matches=[(source_rows[owner][j][0],dist) for co,j,dist in uvtrees[owner].find_range((*uv,0),2e-6) if np.linalg.norm(expected['neutral'][source_rows[owner][j][0]]-pos[vi])<2e-6]
            if not matches:missing.append((ob.name,vi,owner));continue
            ids=set(i for i,d in matches);assert len(ids)==1,('Ambiguous UV/owner/position vertex',vi,ids)
            src=next(iter(ids));byvertex[vi]=src;covered.add(src);uvmax=max(uvmax,max(d for i,d in matches))
    assert len(byvertex)==len(ob.data.vertices)
    bindings[ob.name]=np.array([byvertex[i] for i in range(len(ob.data.vertices))])
rows=[]
for state in states:
    for ob in meshes:
        for k in ob.data.shape_keys.key_blocks:k.value=morphs[state].get(k.name,0)
        ob.data.update();ob.update_tag()
    bpy.context.view_layer.update();delta=max(float(np.linalg.norm(xyz(ob)-expected[state][bindings[ob.name]],axis=1).max()) for ob in meshes)
    rows.append({'state':state,'max_position_delta_m':delta,'pass':delta<2e-6})
    # Fresh import is actually rendered; texture/material routing is observable.
    s=bpy.context.scene;camdata=bpy.data.cameras.new('ReimportReviewCamera');cam=bpy.data.objects.new('ReimportReviewCamera',camdata);s.collection.objects.link(cam);s.camera=cam
    for view in ['front','side','3q']:ns['render']('reimport-'+state,view)
    bpy.data.objects.remove(cam,do_unlink=True)
blob=(A/'jill-textured-rig-v005.glb').read_bytes();size=struct.unpack_from('<I',blob,12)[0];g=json.loads(blob[20:20+size]);texcoords=sorted({mat['pbrMetallicRoughness']['baseColorTexture'].get('texCoord',0) for mat in g['materials']})
report={'pass':not missing and all(row['pass'] for row in rows) and len(anchors)==16 and [len(r.data.bones) for r in rigs]==[130] and texcoords==[0], 'source_vertices_covered':len(covered),'uv_max_delta':uvmax,'unmatched':len(missing),'bones':[len(r.data.bones) for r in rigs],'anchors':len(anchors),'material_count':len(g['materials']),'morph_counts':[len(m.get('extras',{}).get('targetNames',[])) for m in g['meshes']],'uv_attributes':sorted({k for m in g['meshes'] for p in m['primitives'] for k in p['attributes'] if k.startswith('TEXCOORD')}),'basecolor_texcoords':texcoords,'states':rows,'scope':'Face Morph, UV/owner/materials/skin/anchors through actual fresh GLB import. Body motions are independently sampled in the bounded PlayCanvas clip.'}
(E/'reimport-proof.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps(report,indent=2),flush=True);assert report['pass']
