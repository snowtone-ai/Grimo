"""Compare scoped editable contracts and render the opposite mouth profile."""
import bpy,json,ast,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/mouth-profile-v004';A=ROOT/'assets/grimo/production/jill/tripo';R=E/'renders'
tree=ast.parse((ROOT/'scripts/blender/review-jill-texture-v003.py').read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['hasharr','contract']],type_ignores=[]),'<v003 contract functions>','exec'),globals())
data={};geometry={};uvs={};poly={};state_positions={};rows=[]
for label,path in [('v003',A/'rig-pretexture-technical-v003/jill-rig-texture-uv-v003.blend'),('v004',A/'mouth-profile-v004/jill-rig-mouth-profile-v004.blend')]:
    bpy.ops.wm.open_mainfile(filepath=str(path));o=bpy.data.objects['Jill_Body'];r=bpy.data.objects['JILL_RIG'];m=o.data;s=bpy.context.scene
    data[label]=contract(o,r);geometry[label]={k.name:np.array([v.co[:] for v in k.data]) for k in m.shape_keys.key_blocks};uvs[label]=[(u.name,hasharr([v.uv[:] for v in u.data])) for u in m.uv_layers]
    poly[label]=[(tuple(p.vertices),p.material_index) for p in m.polygons]
    if label=='v004':
        m.calc_loop_triangles();np.savez_compressed(E/'after.npz',xyz=geometry[label]['Basis'],tris=np.array([t.vertices[:] for t in m.loop_triangles]),loops=np.array([t.loops[:] for t in m.loop_triangles]),polygons=np.array([t.polygon_index for t in m.loop_triangles]),uv=np.array([v.uv[:] for v in m.uv_layers[0].data]))
    r.animation_data.action=None
    for name,values in [('neutral',{}),('close-mid',{'mouth_close':.5}),('closed',{'mouth_close':1}),('open',{'mouth_open':1})]:
        for k in data[label]['channels']:r[k]=float(values.get(k,0))
        r.update_tag();bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();xyz=np.array([v.co[:] for v in me.vertices]);ev.to_mesh_clear()
        if label=='v003':state_positions[name]=xyz
        else:
            delta=np.linalg.norm(xyz-state_positions[name],axis=1);rows.append({'state':name,'evaluated_changed_vertices':int(sum(delta>1e-8)),'evaluated_max_m':float(delta.max())})
        for view,direction in [('left-side',(-1,0,0)),('left-3q',(-1,-2,.12))]:
            target=Vector((0,-.24,.68));cam=s.camera;cam.location=target+Vector(direction).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.44
            s.render.engine='BLENDER_WORKBENCH';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=False;s.display.shading.show_shadows=True
            s.render.resolution_x=480;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(R/f'{label}-{name}-{view}.png');bpy.ops.render.render(write_still=True)
report=json.loads((E/'repair-report.json').read_text());allowed=set(report['affected_vertices'])|set(map(int,report['local_host_y_fairing']))|set(report['close_exposed_skin_retreat_removed'])
unaffected=np.array([i for i in range(len(geometry['v003']['Basis'])) if i not in allowed]);keychecks={k:{'outside_local_scope_exact':bool(np.array_equal(geometry['v003'][k][unaffected],geometry['v004'][k][unaffected])),'xz_exact':bool(np.array_equal(geometry['v003'][k][:,[0,2]],geometry['v004'][k][:,[0,2]]))} for k in geometry['v003']}
other=[k for k in data['v003'] if k not in ['basis','keys'] and data['v003'][k]!=data['v004'][k]]
proof={'unchanged_contract_differences':other,'uv_all_layers_exact':uvs['v003']==uvs['v004'],'uv_layer_hashes':uvs['v004'],'polygon_indices_and_material_owners_exact':poly['v003']==poly['v004'],'keys':keychecks,'states':rows,'original_muzzle_vertices_faired':len(report['local_host_y_fairing']),'close_front_skin_retreat_removed':len(report['close_exposed_skin_retreat_removed']),'counts':{'bones':len(data['v004']['bones']),'channels':len(data['v004']['channels']),'morphs':len(data['v004']['keys'])-1,'anchors':len(data['v004']['anchors'])},'human_final_go':False}
proof['pass']=not other and proof['uv_all_layers_exact'] and proof['polygon_indices_and_material_owners_exact'] and all(all(c.values()) for c in keychecks.values())
(E/'preservation-proof.json').write_text(json.dumps(proof,indent=2)+'\n');assert proof['pass']
