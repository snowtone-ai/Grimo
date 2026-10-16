"""Focused same-condition saved-render comparison, not another 305-frame run."""
import bpy,json,hashlib,sys
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/jill/tripo';E=ROOT/'docs/production/jill/rig-pretexture-technical-v003';R=E/'renders';R.mkdir(exist_ok=True)
states=[('neutral',{}),('close-mid',{'mouth_close':.5}),('closed',{'mouth_close':1}),('open',{'mouth_open':1}),('blink-mid',{'blink.L':.5,'blink.R':.5}),('blink',{'blink.L':1,'blink.R':1}),('fold',{'wing_open.L':-1,'wing_open.R':-1}),('wing-open',{'wing_open.L':1,'wing_open.R':1})]
views={'front':(0,-1,0),'side':(1,0,0),'3q':(1,-2,.12),'back3q':(1,2,.1)}
if '--saved-returns' in sys.argv:
    for suffix in ['glb','fbx']:
        bpy.ops.wm.open_mainfile(filepath=str(E/'roundtrip'/('rig-image-only-'+suffix+'.blend')))
        s=bpy.context.scene;r=bpy.data.objects['JILL_RIG'];r.animation_data.action=None
        for name,values in [('closed',{'mouth_close':1}),('blink',{'blink.L':1,'blink.R':1})]:
            for k in json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())['authoring_properties']:r[k]=float(values.get(k,0))
            r.update_tag();bpy.context.view_layer.update();cam=s.camera;target=Vector((0,-.24,.68));cam.location=target+Vector((1,-2,.12)).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.44
            s.render.engine='BLENDER_WORKBENCH';s.display.shading.color_type='TEXTURE';s.render.resolution_x=480;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(R/f'returned-{suffix}-{name}.png');bpy.ops.render.render(write_still=True)
    sys.exit(0)
def hasharr(a):return hashlib.sha256(np.asarray(a).tobytes()).hexdigest()
def contract(o,r):
    m=o.data
    return {'basis':hasharr([v.co[:] for v in m.vertices]),'polygons':hasharr([v for p in m.polygons for v in p.vertices]),
        'keys':{k.name:hasharr([v.co[:] for v in k.data]) for k in m.shape_keys.key_blocks},
        'weights':hasharr([(v.index,g.group,g.weight) for v in m.vertices for g in v.groups]),
        'groups':[g.name for g in o.vertex_groups],
        'bones':[(b.name,b.parent.name if b.parent else None,hasharr(b.matrix_local)) for b in r.data.bones],
        'rig_drivers':[(f.data_path,f.array_index,f.driver.expression) for f in r.animation_data.drivers],
        'shape_drivers':[(f.data_path,f.array_index,f.driver.expression) for f in m.shape_keys.animation_data.drivers],
        'anchors':[(a.name,a.parent.name if a.parent else None,a.parent_bone,hasharr(a.matrix_basis)) for a in bpy.context.scene.objects if a.name.startswith('ANCHOR_')],
        'channels':{k:r[k] for k in json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())['authoring_properties']}}
contracts={};positions={};rows=[]
for source,path in [('v002',A/'rig-pretexture-v002/jill-rig-pretexture-v002.blend'),('v003',A/'rig-pretexture-technical-v003/jill-rig-texture-uv-v003.blend')]:
    bpy.ops.wm.open_mainfile(filepath=str(path));o=bpy.data.objects['Jill_Body'];r=bpy.data.objects['JILL_RIG'];s=bpy.context.scene;contracts[source]=contract(o,r)
    if source=='v003':
        previous=np.load(E/'before.npz')['uv'];assert np.array_equal(previous,np.array([x.uv[:] for x in o.data.uv_layers[1].data]))
        # Preserve donor layer against the actual previous saved source.
        donor=np.array([x.uv[:] for x in o.data.uv_layers[2].data]);positions['source_uv']=donor
    else:positions['source_uv_v002']=np.array([x.uv[:] for x in o.data.uv_layers[1].data])
    r.animation_data.action=None
    for name,vals in states:
        for k in contracts[source]['channels']:r[k]=float(vals.get(k,0))
        r.update_tag();bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();xyz=np.array([v.co[:] for v in me.vertices]);ev.to_mesh_clear()
        if source=='v002':positions[name]=xyz
        else:rows.append({'state':name,'evaluated_xyz_max_m':float(np.max(np.linalg.norm(xyz-positions[name],axis=1)))})
        face=name not in ['fold','wing-open'];target=Vector((0,-.24,.68) if face else (0,0,.5))
        vs=['front','side','3q'] if face else ['front','side','back3q']
        for view in vs:
            cam=s.camera;cam.location=target+Vector(views[view]).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.44 if face else 1.16
            s.render.engine='BLENDER_WORKBENCH';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=False;s.display.shading.show_shadows=True
            s.render.resolution_x=480;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(R/(source+'-'+name+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
        print('RENDERED',source,name,flush=True)
    if source=='v003':
        img=bpy.data.images.load(str(E/'diagnostic-uv0.png'))
        for mat in o.data.materials:
            n=mat.node_tree.nodes.new('ShaderNodeTexImage');n.image=img;mat.node_tree.nodes.active=n;mat.node_tree.links.new(n.outputs['Color'],mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
        s.display.shading.color_type='TEXTURE'
        for name,vals in [states[i] for i in [0,2,3,4,5,6,7]]:
            for k in contracts[source]['channels']:r[k]=float(vals.get(k,0))
            r.update_tag();bpy.context.view_layer.update()
            for view in ['3q'] if name not in ['fold','wing-open'] else ['front','back3q']:
                face=name not in ['fold','wing-open'];target=Vector((0,-.24,.68) if face else (0,0,.5));cam=s.camera;cam.location=target+Vector(views[view]).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.44 if face else 1.16
                s.render.filepath=str(R/('diagnostic-'+name+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
diff=[k for k in contracts['v002'] if contracts['v002'][k]!=contracts['v003'][k]]
report={'contract_equal':not diff,'contract_differences':diff,'contracts':contracts,'states':rows,'source_uv_exact':bool(np.array_equal(positions['source_uv'],positions['source_uv_v002'])),'render_conditions':{'engine':'Workbench actual saved renders','size':[480,480],'camera':'matched front/side/3Q; wings front/side/rear3Q','materials':'copies of same clay values; no geometry/normal changes'},'human_final_go':False}
(E/'preservation-proof.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
assert not diff and report['source_uv_exact'] and all(row['evaluated_xyz_max_m']==0 for row in rows)
