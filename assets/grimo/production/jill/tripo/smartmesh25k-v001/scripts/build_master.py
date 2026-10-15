"""Single editing lineage: immutable FBX -> editable Blender master -> optional GLB."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *

VIEWS=[
 ('front',(0,-1,0),(0,0,.5),1.16),
 ('left-facing-side',(1,0,0),(0,0,.5),1.16),
 ('right-facing-side',(-1,0,0),(0,0,.5),1.16),
 ('back',(0,1,0),(0,0,.5),1.16),
 ('front-three-quarter',(1,-2,.45),(0,0,.5),1.16),
 ('opposite-front-three-quarter',(-1,-2,.45),(0,0,.5),1.16),
 ('rear-three-quarter',(1,2,.4),(0,0,.5),1.16),
 ('wing-underside',(1,1,-.8),(0,.05,.53),.96),
 ('wing-root-left',(1,1,.2),(.18,.06,.52),.48),
 ('wing-root-right',(-1,1,.2),(-.18,.06,.52),.48),
 ('tail-root',(1,1,.15),(0,.19,.29),.64),
 ('soles',(0,-.3,-1),(0,0,.09),.66),
 ('face-front',(0,-1,0),(0,-.20,.72),.60),
 ('face-three-quarter',(1,-2,.15),(0,-.18,.72),.60),
]

if __name__=='__main__':
    selection=json.loads((EVIDENCE/'editing-source-selection.json').read_text())
    assert selection['selected_editing_source'].endswith('.fbx')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene; scene.world=bpy.data.worlds.new('ReviewWorld')
    bpy.ops.import_scene.fbx(filepath=str(ASSET/selection['selected_editing_source']))
    original=next(o for o in scene.objects if o.type=='MESH')
    original.name='REFERENCE_FBX_UNEDITED'; original.color=(.58,.68,.55,1)
    original['role']='Unedited import of SHA256 5e9339437af5ad209c01597997006e96bd90d5489a08c28531ab5faa2b3f31db'
    mesh=original.data; remove=set(selection['fbx_remove_face_ids'])
    keep=[p.index for p in mesh.polygons if p.index not in remove]
    coords=[tuple(v.co) for v in mesh.vertices]
    saved_normals=[tuple(n.vector) for n in mesh.corner_normals]
    def subset(name,face_ids):
        me=bpy.data.meshes.new(name); me.from_pydata(coords,[],[list(mesh.polygons[i].vertices) for i in face_ids]); me.update()
        ob=bpy.data.objects.new(name,me); scene.collection.objects.link(ob); ob.matrix_world=original.matrix_world.copy(); ob.color=original.color
        for mat in mesh.materials:me.materials.append(mat)
        normals=[]
        for p,idx in zip(me.polygons,face_ids):
            src=mesh.polygons[idx]; p.use_smooth=src.use_smooth; p.material_index=src.material_index
            normals.extend(saved_normals[k] for k in src.loop_indices)
        me.normals_split_custom_set(normals)
        att=me.attributes.new('source_fbx_polygon_id','INT','FACE')
        for d,idx in zip(att.data,face_ids):d.value=idx
        return ob
    candidate=subset('JILL_GEOMETRY_MASTER',keep)
    candidate['authority']='SOLE EDITABLE GEOMETRY MASTER. Source FBX only. Basis is repaired neutral. Human Gate PENDING.'
    candidate['repair']='Only 10 confirmed plate polygons (12 triangles) omitted; all source vertex coordinates and retained polygons/corner normals preserved.'
    plates=subset('ARCHIVE_REMOVED_PLATES',sorted(remove)); plates.color=(.9,.12,.12,1); plates.hide_render=True; plates.hide_set(True)
    old=audit(original); new=audit(candidate)
    coord_equal=all(tuple(a.co)==tuple(b.co) for a,b in zip(mesh.vertices,candidate.data.vertices))
    face_equal=all(tuple(mesh.polygons[i].vertices)==tuple(p.vertices) for i,p in zip(keep,candidate.data.polygons))
    normal_error=max((Vector(saved_normals[k])-candidate.data.corner_normals[n].vector).length for n,k in enumerate(k for i in keep for k in mesh.polygons[i].loop_indices))
    report={'source':'FBX only','before':old,'after':new,'omitted_fbx_polygon_ids':sorted(remove),
            'all_28050_vertex_coordinates_bitwise_equal':coord_equal,'all_retained_polygon_indices_equal':face_equal,
            'max_retained_corner_normal_difference':normal_error,
            'source_fbx_material_datablocks_shared':list(mesh.materials)==list(candidate.data.materials),
            'normal_note':'Imported FBX corner normals explicitly restored to retained corners.',
            'no_new_boundary_edges':False}
    def boundary_set(me):
        counts={}
        for p in me.polygons:
            for e in p.edge_keys:counts[e]=counts.get(e,0)+1
        return {e for e,n in counts.items() if n==1}
    report['new_boundary_edge_ids']=[list(e) for e in boundary_set(candidate.data)-boundary_set(mesh)]
    report['no_new_boundary_edges']=not report['new_boundary_edge_ids']
    assert coord_equal and face_equal and report['no_new_boundary_edges'] and old['triangles']-new['triangles']==12
    write_json('repair-validation.json',report)
    setup_render(scene)
    for label,obj in [('before-fbx',original),('after-fbx',candidate)]:
        original.hide_render=obj!=original; candidate.hide_render=obj!=candidate
        for name,d,t,s in VIEWS:render(scene,label+'-'+name,d,t,s)
    original.hide_render=True; original.hide_set(True); candidate.hide_render=False; candidate.hide_set(False)
    # Organize and retain reference/removal layers in the .blend for reversible review.
    for name,objects in [('00_REFERENCE_FBX_LOCKED',[original]),('01_EDITABLE_MASTER',[candidate]),('02_REMOVED_PLATES_ARCHIVE',[plates])]:
        col=bpy.data.collections.new(name); scene.collection.children.link(col)
        for ob in objects:
            for parent in list(ob.users_collection):parent.objects.unlink(ob)
            col.objects.link(ob)
        if 'MASTER' not in name:col.hide_render=True; col.hide_viewport=True
    bpy.ops.object.select_all(action='DESELECT');candidate.select_set(True);bpy.context.view_layer.objects.active=candidate
    setup_camera(scene,(1,-2,.45),(0,0,.5),1.16)
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'jill-geometry-master.blend'))
    print('REPAIR_COMPLETE',json.dumps({k:v for k,v in report.items() if k not in ['before','after']}))
