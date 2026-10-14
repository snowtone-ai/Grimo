"""Factory-scene reload of saved diagnostic GLB; no production blend is written."""
import bpy, hashlib, json, math, sys
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/tripo-autorig-v001'
BASE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003'
PROBE=BASE/'rigging/shushu-v006-autorig-deformation-probe-v001.glb'
BLEND=BASE/'rigging/shushu-v006-autorig-deformation-probe-v001.blend'
def write(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def coords(objects):
    bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();result={}
    for o in objects:
        ev=o.evaluated_get(dep);me=ev.to_mesh();result[o.name]=np.array([ev.matrix_world@v.co for v in me.vertices]);ev.to_mesh_clear()
    return result
def setup():
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=False;scene.cycles.seed=0
    scene.render.threads_mode='FIXED';scene.render.threads=12;scene.render.resolution_percentage=100;scene.render.resolution_x=scene.render.resolution_y=768
    scene.world=bpy.data.worlds.new('Neutral soft review');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.8
    scene.view_settings.view_transform='AgX';scene.view_settings.look='None';scene.view_settings.exposure=-.5
    cam=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));scene.collection.objects.link(cam);scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.14
    for name,loc,energy,size in [('key',(-1,-2,2),90,1.5),('fill',(1,-1,1),40,1.5)]:
        light=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));scene.collection.objects.link(light);light.location=Vector((0,0,.65))+Vector(loc);light.rotation_euler=(Vector((0,0,.65))-light.location).to_track_quat('-Z','Y').to_euler();light.data.energy=energy;light.data.shape='DISK';light.data.size=size
    # Grid-free supporting plane used identically for all comparisons.
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,-.002));ground=bpy.context.object;ground.name='DiagnosticGround'
    mat=bpy.data.materials.new('Ground');mat.diffuse_color=(.65,.65,.65,1);ground.data.materials.append(mat)
    return scene,cam
def render_views(scene,cam,tag):
    cameras={}
    for view,direction in [('front',(0,-1,0)),('3q',(-math.sqrt(.5),-math.sqrt(.5),0)),('side',(-1,0,0))]:
        d=Vector(direction);cam.location=Vector((0,0,.5))+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();path=OUT/'renders'/f'{tag}-{view}.png';scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        cameras[view]={'location':list(cam.location),'rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,'target':[0,0,.5],'resolution':[768,768],'samples':16,'seed':0,'lighting':'original material / AgX exposure -0.5 / same ground at -0.002'}
    return cameras
def review():
    (OUT/'renders').mkdir(exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=24
    bpy.ops.import_scene.gltf(filepath=str(PROBE));meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')];rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');scene=bpy.context.scene
    scene.frame_set(0);base=coords(meshes);states=json.loads((OUT/'poses.json').read_text(encoding='utf-8'));scene,cam=setup();records={};measure=[]
    for s in states:
        scene.frame_set(s['time']*24);v=coords(meshes);measure.append({'name':s['name'],'frame':scene.frame_current,'max_mesh_displacement':{n:float(np.linalg.norm(v[n]-base[n],axis=1).max()) for n in base}});records[s['name']]=render_views(scene,cam,s['name']);print('POSE_DONE',s['name'],flush=True)
    scene.frame_start=0;scene.frame_end=states[-1]['time']*24;scene.frame_set(0)
    for s in states:scene.timeline_markers.new(s['name'],frame=s['time']*24)
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    audit={'blender':bpy.app.version_string,'saved_glb_sha256':sha(PROBE),'saved_blend_sha256':sha(BLEND),'armature_bones':len(rig.data.bones),'armature_matrix':list(map(list,rig.matrix_world)),'actions':[{'name':a.name,'frame_range':list(a.frame_range)} for a in bpy.data.actions],'cameras':records,'deformation':measure,'meshes':[{'name':o.name,'uv_layers':len(o.data.uv_layers),'armature_modifiers':[m.object.name for m in o.modifiers if m.type=='ARMATURE'],'shape_keys':0 if not o.data.shape_keys else len(o.data.shape_keys.key_blocks)} for o in meshes]};write('blender-reload.json',audit)
    # Independently reload input and the saved probe with animation disabled at rest.
    for tag,path in [('input-neutral',BASE/'rigging/shushu-v006-tripo-autorig-v001.glb'),('saved-neutral',PROBE),('lowpoly',BASE/'rigprep/shushu-v006-rigprep-lowpoly-v001.glb'),('v006',BASE/'texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb')]:
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=24;bpy.ops.import_scene.gltf(filepath=str(path));bpy.context.scene.frame_set(0);scene,cam=setup();records[tag]=render_views(scene,cam,tag);print('BASE_DONE',tag,flush=True)
    write('cameras.json',records)
def v003():
    rows={}
    for tag in ['shushu-geometry-v003','shushu-geometry-v003-proof']:
        path=ROOT/'assets/grimo/production/shushu/blender'/f'{tag}.blend';bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
        row={'sha256':sha(path),'frame_range':[scene.frame_start,scene.frame_end],'fps':scene.render.fps,'armatures':[],'shape_keys':{},'controls':{},'actions':[],'drivers':[]}
        for o in bpy.data.objects:
            if o.type=='ARMATURE':row['armatures'].append({'name':o.name,'bones':[b.name for b in o.data.bones],'pose_properties':{b.name:{k:str(b[k]) for k in b.keys()} for b in o.pose.bones if b.keys()}})
            if o.keys():row['controls'][o.name]={k:str(o[k]) if len(str(o[k]))<200 else {'length':len(str(o[k])),'sha256':hashlib.sha256(str(o[k]).encode()).hexdigest()} for k in o.keys()}
            if o.type=='MESH' and o.data.shape_keys:
                sk=o.data.shape_keys;row['shape_keys'][o.name]=[k.name for k in sk.key_blocks]
                if sk.animation_data:
                    row['drivers'] += [{'owner':o.name,'path':d.data_path,'expression':d.driver.expression,'variables':[{'name':v.name,'targets':[{'id':t.id.name if t.id else None,'data_path':t.data_path} for t in v.targets]} for v in d.driver.variables]} for d in sk.animation_data.drivers]
        row['actions']=[{'name':a.name,'frame_range':list(a.frame_range)} for a in bpy.data.actions];rows[tag]=row
    write('v003-readonly-inventory.json',rows);print('V003_READONLY_DONE',flush=True)
def contact():
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=24;bpy.ops.import_scene.gltf(filepath=str(PROBE));meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ShushuStatic_')];scene=bpy.context.scene;scene.frame_set(9*24);v=coords(meshes);paw=next(o for o in meshes if o.name=='ShushuStatic_Paw_L')
    points=v[paw.name];anchor=points[points[:,1].argmin()];radius=.035;center=anchor+np.array([0,-radius,0]);scene,cam=setup()
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=radius,location=center);prop=bpy.context.object;prop.name='Inspection_Tangent_Target_NOT_HELD';mat=bpy.data.materials.new('Diagnostic apricot');mat.diffuse_color=(.9,.3,.04,1);prop.data.materials.append(mat)
    rows=[];cams={}
    for name,frame in [('contact-tangent',9*24),('contact-release',10*24)]:
        scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();distances={}
        for o in meshes:
            ev=o.evaluated_get(deps);me=ev.to_mesh();verts=[ev.matrix_world@p.co for p in me.vertices];tree=BVHTree.FromPolygons(verts,[list(p.vertices) for p in me.polygons]);nearest=tree.find_nearest(Vector(center));distances[o.name]=None if nearest is None else float(nearest[3]-radius);ev.to_mesh_clear()
        rows.append({'name':name,'frame':frame,'sphere_center':center.tolist(),'radius':radius,'surface_distance_minus_radius':distances});cams[name]=render_views(scene,cam,name)
    write('contact-check.json',{'type':'single geometric tangency to forwardmost LEFT paw vertex; no holding, pressure, muscle model or stability PASS','poses':rows,'cameras':cams});print('CONTACT_DONE',flush=True)
if __name__=='__main__':
    v003() if '--v003' in sys.argv else contact() if '--contact' in sys.argv else review()
