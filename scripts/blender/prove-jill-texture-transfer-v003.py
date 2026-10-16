"""Synthetic image/material return test, never a Tripo result or formal texture.

Export the frozen neutral twice; verify both formats, bind only returned images
to the original rig materials, save/reopen and export/reimport a rig GLB.
"""
import bpy,json,sys,hashlib,struct
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-technical-v003';E=ROOT/'docs/production/jill/rig-pretexture-technical-v003'
D=E/'roundtrip';D.mkdir(exist_ok=True)
def write(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def open_rig():
    bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-texture-uv-v003.blend'))
    r=bpy.data.objects['JILL_RIG'];o=bpy.data.objects['Jill_Body'];r.animation_data.action=None
    for k in json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())['authoring_properties']:r[k]=0.
    r.update_tag();bpy.context.view_layer.update();return o,r
def bind(o,img):
    for m in o.data.materials:
        uv=m.node_tree.nodes.new('ShaderNodeUVMap');uv.uv_map='Jill_Texture_UV0_v003'
        n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=img
        m.node_tree.links.new(uv.outputs['UV'],n.inputs['Vector']);m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
        m.node_tree.nodes.active=n
def select(objects):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
def glb(path,objects,rig=False):
    select(objects);bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,
        export_animations=False,export_skins=rig,export_morph=rig,export_extras=rig,export_cameras=False,export_lights=False,
        export_def_bones=False,export_all_influences=False,export_influence_nb=4)
def corners(objects):
    rows=[]
    for o in objects:
        ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh()
        for p in m.polygons:
            owner=m.materials[p.material_index].get('paint_owner',m.materials[p.material_index].name.removeprefix('JILL_').split('.')[0])
            for li in p.loop_indices:
                v=m.vertices[m.loops[li].vertex_index]
                rows.append((tuple(o.matrix_world@v.co),tuple(m.uv_layers[0].data[li].uv),owner))
        ev.to_mesh_clear()
    return rows
def dump_triangles(o,path):
    m=o.data;m.calc_loop_triangles()
    np.savez_compressed(path,xyz=np.array([tuple(o.matrix_world@v.co) for v in m.vertices]),tris=np.array([t.vertices[:] for t in m.loop_triangles]),uv=np.array([[m.uv_layers[0].data[li].uv[:] for li in t.loops] for t in m.loop_triangles]),owners=np.array([m.materials[m.polygons[t.polygon_index].material_index].name.removeprefix('JILL_').split('.')[0] for t in m.loop_triangles]))
def check(expected,got):
    kd=KDTree(len(expected))
    for i,(p,uv,owner) in enumerate(expected):kd.insert(Vector(p),i)
    kd.balance();bad=0;uvmax=0;posmax=0
    for p,uv,owner in got:
        matches=[(co,i,d) for co,i,d in kd.find_range(Vector(p),2e-6) if expected[i][2]==owner]
        if not matches:bad+=1;continue
        co,i,delta=min(matches,key=lambda x:np.linalg.norm(np.array(expected[x[1]][1])-uv))
        posmax=max(posmax,float(delta));uvmax=max(uvmax,float(np.linalg.norm(np.array(expected[i][1])-uv)))
    return {'corners':len(got),'unmatched_position_owner':bad,'position_max_m':posmax,'uv_max':uvmax,'pass':bad==0 and uvmax<2e-6}
candidate_sha=hashlib.sha256((A/'jill-rig-texture-uv-v003.blend').read_bytes()).hexdigest()
o,r=open_rig();s=bpy.context.scene
# Diagnostic UV image is deliberately asymmetric, so UV0/UV1 or flips are visible.
img=bpy.data.images.load(str(E/'diagnostic-uv0.png'),check_existing=False);img.colorspace_settings.name='sRGB'
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=bpy.data.meshes.new_from_object(ev,preserve_all_data_layers=True,depsgraph=bpy.context.evaluated_depsgraph_get())
static=bpy.data.objects.new('Jill_Texture_Input_Neutral_v003',m);s.collection.objects.link(static);static.matrix_world=o.matrix_world.copy()
while len(m.uv_layers)>1:m.uv_layers.remove(m.uv_layers[-1])
expected=corners([static])
# Upload candidates contain only appearance-preserving clay materials, no test image.
glb(A/'jill-texture-input-neutral-v003.glb',[static])
select([static]);bpy.ops.export_scene.fbx(filepath=str(A/'jill-texture-input-neutral-v003.fbx'),use_selection=True,object_types={'MESH'},use_mesh_modifiers=False,add_leaf_bones=False,bake_anim=False,axis_forward='-Z',axis_up='Y',use_triangles=True)
# The diagnostic fixture represents a returned image on the same atlas.
bind(static,img);glb(D/'synthetic-return.glb',[static])
select([static]);bpy.ops.export_scene.fbx(filepath=str(D/'synthetic-return.fbx'),use_selection=True,object_types={'MESH'},use_mesh_modifiers=False,add_leaf_bones=False,bake_anim=False,axis_forward='-Z',axis_up='Y',use_triangles=True,path_mode='COPY',embed_textures=True)
dump_triangles(static,D/'target-neutral.npz')
for x in m.uv_layers[0].data:x.uv.x=1-x.uv.x
changed=bpy.data.images.load(str(E/'diagnostic-uv-changed.png'),check_existing=False)
for mat in static.data.materials:
    for n in mat.node_tree.nodes:
        if n.type=='TEX_IMAGE':n.image=changed
glb(D/'synthetic-return-uv-changed.glb',[static])
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(D/'synthetic-return-uv-changed.glb'))
ob=next(o for o in bpy.context.scene.objects if o.type=='MESH');dump_triangles(ob,D/'returned-uv-changed.npz')
rows=[]
for suffix in ['glb','fbx']:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if suffix=='glb':bpy.ops.import_scene.gltf(filepath=str(D/('synthetic-return.'+suffix)))
    else:bpy.ops.import_scene.fbx(filepath=str(D/('synthetic-return.'+suffix)),use_anim=False)
    objects=[x for x in bpy.context.scene.objects if x.type=='MESH'];got=corners(objects)
    textures=[n.image for x in objects for mat in x.data.materials for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
    assert textures and all(list(i.size)==[4096,4096] for i in textures),'Missing diagnostic image'
    row={'format':suffix,**check(expected,got),'reverse':check(got,expected),'texture_dimensions':list(textures[0].size),'uv_layers':{x.name:[u.name for u in x.data.uv_layers] for x in objects},'armatures':sum(x.type=='ARMATURE' for x in bpy.context.scene.objects)}
    # Compare decoded pixel arrays, not image filename alone.
    decoded=np.empty(len(textures[0].pixels),dtype=np.float32);textures[0].pixels.foreach_get(decoded)
    reference=bpy.data.images.load(str(E/'diagnostic-uv0.png'),check_existing=False);refpixels=np.empty(len(reference.pixels),dtype=np.float32);reference.pixels.foreach_get(refpixels)
    row['decoded_pixel_max_delta']=float(np.max(abs(decoded-refpixels)));del decoded,refpixels
    assert row['pass'] and row['reverse']['pass'] and row['decoded_pixel_max_delta']<1/255
    returned=D/('returned-image-'+suffix+'.png');textures[0].filepath_raw=str(returned);textures[0].file_format='PNG';textures[0].save()
    o,r=open_rig();bind(o,bpy.data.images.load(str(returned),check_existing=False))
    bpy.ops.file.pack_all();bpy.context.preferences.filepaths.save_version=0
    path=D/('rig-image-only-'+suffix+'.blend');bpy.ops.wm.save_as_mainfile(filepath=str(path));bpy.ops.wm.open_mainfile(filepath=str(path))
    o=bpy.data.objects['Jill_Body'];r=bpy.data.objects['JILL_RIG'];row['saved_rig_uv0']=o.data.uv_layers[0].name;row['saved_bones']=len(r.data.bones);row['saved_morphs']=len(o.data.shape_keys.key_blocks)-1
    glb(D/('rig-image-only-'+suffix+'.glb'),[r,o]+[a for a in bpy.context.scene.objects if a.name.startswith('ANCHOR_')],True)
    blob=(D/('rig-image-only-'+suffix+'.glb')).read_bytes();size=struct.unpack_from('<I',blob,12)[0];g=json.loads(blob[20:20+size])
    row['rig_glb_uv_attributes']=sorted({k for mesh in g['meshes'] for p in mesh['primitives'] for k in p['attributes'] if k.startswith('TEXCOORD')})
    row['basecolor_texcoords']=sorted({mat['pbrMetallicRoughness']['baseColorTexture'].get('texCoord',0) for mat in g['materials']})
    row['rig_glb_joint_counts']=[len(s['joints']) for s in g['skins']]
    row['rig_glb_morph_counts']=[len(mesh.get('extras',{}).get('targetNames',[])) for mesh in g['meshes']]
    assert row['basecolor_texcoords']==[0] and set(row['rig_glb_joint_counts'])=={130} and set(row['rig_glb_morph_counts'])=={20}
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(D/('rig-image-only-'+suffix+'.glb')))
    meshes=[x for x in bpy.context.scene.objects if x.type=='MESH' and any(mod.type=='ARMATURE' for mod in x.modifiers)]
    row['saved_glb_reimport']=check(expected,corners(meshes));write('transfer-progress.json',row);assert row['saved_glb_reimport']['pass']
    rows.append(row)
assert candidate_sha==hashlib.sha256((A/'jill-rig-texture-uv-v003.blend').read_bytes()).hexdigest(),'Candidate changed during proof'
write('transfer-proof.json',{'pass':True,'candidate_sha256':candidate_sha,'synthetic_only':True,'real_tripo_return':'UNKNOWN','paths':rows,'rule':'Image-only application; no returned geometry, bones, weights, morphs or anchors adopted. UV0 explicit, old UV1/2 retained in editable rig. Neutral-only format proof; existing 305-frame proof not repeated.'})
