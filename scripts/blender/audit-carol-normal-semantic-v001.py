"""Reopen candidate, compare frozen Skin, inspect new coat and attachments."""
import bpy,bmesh,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-normal-semantic-v001.blend'
SKIN=ASSET.with_name('carol-skin-default-v004.blend')
OUT=ROOT/'docs/production/carol/evidence/normal-semantic-v001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def signature(ob):
    h=hashlib.sha256();h.update(ob.type.encode());h.update(str([list(r) for r in ob.matrix_world]).encode())
    if ob.type=='MESH':
        for v in ob.data.vertices:h.update(str(tuple(v.co)).encode())
        for p in ob.data.polygons:h.update(str((tuple(p.vertices),p.material_index,p.use_smooth)).encode())
        for attr in ob.data.attributes:
            h.update(str((attr.name,attr.data_type,attr.domain)).encode())
            prop='color' if attr.data_type.endswith('COLOR') else 'vector' if attr.data_type=='FLOAT_VECTOR' else 'value' if attr.data_type in ['FLOAT','INT','BOOLEAN'] else None
            if prop:
                for d in attr.data:h.update(str(getattr(d,prop)).encode())
        if ob.data.shape_keys:
            for key in ob.data.shape_keys.key_blocks:
                h.update(str((key.name,key.value)).encode())
                for p in key.data:h.update(str(tuple(p.co)).encode())
    elif ob.type=='CURVE':
        for s in ob.data.splines:
            for p in s.points:h.update(str(tuple(p.co)).encode())
            for p in s.bezier_points:h.update(str((tuple(p.co),tuple(p.handle_left),tuple(p.handle_right))).encode())
    for m in ob.modifiers:
        h.update(str((m.type,m.name)).encode())
        for p in m.bl_rna.properties:
            if p.type in ['BOOLEAN','INT','FLOAT','ENUM','STRING'] and p.identifier!='rna_type':h.update(str((p.identifier,getattr(m,p.identifier))).encode())
    return h.hexdigest()
def matsig(mat):
    def value(v):
        try:return list(v)
        except:return str(v)
    data=[(n.name,n.type,[(i.name,value(i.default_value)) for i in n.inputs if hasattr(i,'default_value')]) for n in mat.node_tree.nodes]
    links=[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in mat.node_tree.links]
    return hashlib.sha256(json.dumps([data,links],sort_keys=True).encode()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SKIN))
baseline={ob.name:signature(ob) for ob in bpy.context.scene.objects if ob.type in ['MESH','CURVE']}
materials={ob.name:[matsig(m) for m in ob.data.materials] for ob in bpy.context.scene.objects if ob.type in ['MESH','CURVE']}
bpy.ops.wm.open_mainfile(filepath=str(ASSET))
same={name:signature(bpy.data.objects[name])==s for name,s in baseline.items()}
same_mats={name:[matsig(m) for m in bpy.data.objects[name].data.materials]==s for name,s in materials.items()}
report={'asset_sha256':sha(ASSET),'frozen_skin_sha256':sha(SKIN),'skin_geometry_unchanged':same,'skin_materials_unchanged':same_mats,'coat':{},'missing_images':[], 'human_visual_approval':False}
assert all(same.values()),same
assert all(same_mats.values()),same_mats
original=bpy.data.objects['CENTRAL_CHASSIS'];support=bpy.data.objects['CANDIDATE_NECK_SUPPORT']
assert original.hide_render and not support.hide_render
a=np.array([v.co[:] for v in original.data.vertices]);b=np.array([v.co[:] for v in support.data.vertices])
assert np.array_equal(a[a[:,2]>=.255],b[a[:,2]>=.255]),'Candidate helper changed visible upper face'
report['candidate_neck_support']={'original_chassis_retained_hidden':True,'upper_face_z_ge_0255_unchanged':True,'max_displacement':float(np.linalg.norm(a-b,axis=1).max()),'changed_vertices':int(np.count_nonzero(np.linalg.norm(a-b,axis=1)>1e-7)),'purpose':'Candidate-only low neck accommodation behind the bare jaw; not a Skin revision'}
for name in ['HeadFleece','BodyFleece','TailFleece']:
    ob=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(ob.data)
    pts=np.array([ob.matrix_world@v.co for v in ob.data.vertices]);volume=bm.calc_volume(signed=True)
    unseen=set(bm.verts);components=[]
    while unseen:
        seed=unseen.pop();stack=[seed];count=1
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                other=e.other_vert(v)
                if other in unseen:unseen.remove(other);stack.append(other);count+=1
        components.append(count)
    info={'vertices':len(bm.verts),'faces':len(bm.faces),'triangles':sum(len(f.verts)-2 for f in bm.faces),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'degenerate_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'signed_volume':volume,'components':sorted(components,reverse=True),'finite':bool(np.isfinite(pts).all()),'bounds':np.column_stack((pts.min(axis=0),pts.max(axis=0))).tolist(),'owner':ob.parent.name}
    assert info['finite'] and info['non_manifold_edges']==0 and info['degenerate_faces']==0 and volume>0 and len(components)==1,info
    report['coat'][name]=info;bm.free()
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file and not Path(bpy.path.abspath(im.filepath)).exists():report['missing_images'].append(im.filepath)
assert not report['missing_images'],report['missing_images']
report['generator_sha256']=sha(ROOT/'scripts/blender/build-carol-normal-semantic-v001.py')
report['ornament_contact']={}
trees={}
for region,name in [('head','HeadFleece'),('body','BodyFleece')]:
    ob=bpy.data.objects[name]
    trees[region]=BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],[tuple(p.vertices) for p in ob.data.polygons])
for ob in bpy.context.scene.objects:
    if 'surface_owner' not in ob:continue
    distances=[]
    for v in ob.data.vertices:
        p=ob.matrix_world@v.co;hit,n,_,d=trees[ob['surface_owner']].find_nearest(p)
        distances.append(d if (p-hit).dot(n)>=0 else -d)
    contact={'owner':ob.parent.name,'region':ob['surface_owner'],'minimum_signed_surface_distance':min(distances),'maximum_signed_surface_distance':max(distances),'embedded_vertices':sum(d<0 for d in distances)}
    assert contact['minimum_signed_surface_distance']<.003,'Floating ornament: '+ob.name
    report['ornament_contact'][ob.name]=contact
authority=json.loads((ROOT/'assets/grimo/source/carol/approved-3d/authority.json').read_text())
report['authority_verification']={a['path']:sha(ROOT/a['path']).lower()==a['sha256'].lower() for a in authority['authorityOrder']}
assert all(report['authority_verification'].values()),report['authority_verification']
report['technical_sanity']='PASS';report['scope']='Neutral geometry/material/source integrity only; no motion/topology/runtime approval'
OUT.mkdir(parents=True,exist_ok=True);(OUT/'asset-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'technical_sanity':'PASS','skin_objects':len(same),'coat':report['coat']}))
