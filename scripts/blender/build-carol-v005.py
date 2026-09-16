"""Zero-based authored volumes. No imports or geometry from previous Carols.

Stage primary is intentionally isolated from face/motif/detail construction.
Run in Blender background; preserve editable design masses in hidden collection.
"""
import bpy, bmesh, math, json, sys, argparse, runpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/hero-geometry-v005'
DATA=json.loads((OUT/'landmark-measurements.json').read_text())
P=argparse.ArgumentParser(); P.add_argument('--stage',default='primary'); P.add_argument('--iteration',type=int,default=1)
ARGS=P.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
SC=bpy.context.scene
HERO=bpy.data.collections.new('Carol_v005_Primary'); SC.collection.children.link(HERO)
GUIDES=bpy.data.collections.new('Reference_Locked'); SC.collection.children.link(GUIDES)
ROOTOBJ=bpy.data.objects.new('Carol_v005',None); HERO.objects.link(ROOTOBJ)
def material(name,color,rough=.65):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Roughness'].default_value=rough
    return m
CLAY=material('Diagnostic_Clay',(.58,.62,.70))
def meshobj(name,verts,faces,mat=CLAY):
    m=bpy.data.meshes.new(name); m.from_pydata(verts,[],faces); m.update()
    bm=bmesh.new(); bm.from_mesh(m); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(m); bm.free()
    ob=bpy.data.objects.new(name,m); HERO.objects.link(ob); ob.parent=ROOTOBJ; m.materials.append(mat)
    for p in m.polygons:p.use_smooth=True
    return ob
def volume(name,center,radius,mat=CLAY,rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=32,location=center)
    ob=bpy.context.object; ob.name=name
    for co in list(ob.users_collection): co.objects.unlink(ob)
    HERO.objects.link(ob); ob.parent=ROOTOBJ; ob.scale=radius; ob.rotation_euler=rot
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.data.materials.append(mat)
    for p in ob.data.polygons:p.use_smooth=True
    return ob
def union(name,objects,voxel=.035):
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]; bpy.ops.object.join(); ob=objects[0]; ob.name=name
    mod=ob.modifiers.new('Volume union','REMESH'); mod.mode='VOXEL'; mod.voxel_size=voxel; mod.use_smooth_shade=True
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=ob.modifiers.new('Soften volume junctions','SMOOTH'); mod.factor=1; mod.iterations=4; bpy.ops.object.modifier_apply(modifier=mod.name)
    return ob
def ear(name,side,mat=CLAY):
    # Authored root-to-tip sections: a thick bowl, not a pink plate insert.
    sec=[(.82,-1.67,1.38,.09,.06),(1.15,-1.49,1.27,.22,.105),(1.46,-1.20,1.15,.245,.12),(1.62,-.93,1.10,.15,.10),(1.66,-.80,1.13,.012,.018)]
    verts=[]; faces=[]
    for x,y,z,w,d in sec:
        for j in range(32):
            a=math.tau*j/32
            verts.append((side*x,y+d*math.cos(a),z+w*math.sin(a)))
    for i in range(len(sec)-1):
        for j in range(32):faces.append((i*32+j,i*32+(j+1)%32,(i+1)*32+(j+1)%32,(i+1)*32+j))
    faces += [tuple(reversed(range(32))),tuple(range(128,160))]
    ob=meshobj(name,verts,faces,mat)
    mod=ob.modifiers.new('Soft ear silhouette','SUBSURF'); mod.levels=2
    return ob
def primary():
    masses=[('head_crown',(0,-.76,2.10),(1.09,.98,.88)),('head_front',(0,-1.14,1.48),(1.35,.78,.91)),('shoulder_L',(-.70,-.45,1.48),(.63,.74,.96)),('shoulder_R',(.71,-.40,1.52),(.63,.77,.92)),('body_center',(0,.58,1.27),(1.02,1.04,.92)),('rear_upper',(-.08,.99,1.57),(.96,.75,.74)),('rear_lower',(.04,1.14,.87),(1.08,.65,.55)),('front_lower_L',(-.67,-1.12,.69),(.54,.57,.36)),('front_lower_R',(.61,-1.14,.67),(.57,.58,.37))]
    ob=union('Primary_Fleece_Envelope',[volume('Primary_'+n,c,r) for n,c,r in masses])
    volume('Primary_Face',(.025,-1.73,1.13),(.84,.29,.57))
    ear('Primary_Ear_L',-1); ear('Primary_Ear_R',1)
    for side in [-1,1]:
        for y,label in [(-.95,'F'),(1.27,'R')]:
            hoof=volume('Primary_Hoof_'+label+str(side),(side*.59,y,.25),(.29,.34,.30))
            for v in hoof.data.vertices: v.co.z=max(v.co.z,-.25)
    volume('Primary_Rear_Tuft',(0,1.93,1.67),(.41,.39,.43))
    return masses
def camera(name,pos,target,scale=5.8,persp=False):
    d=bpy.data.cameras.new(name); ob=bpy.data.objects.new(name,d); SC.collection.objects.link(ob)
    ob.location=pos; ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler(); d.type='PERSP' if persp else 'ORTHO'; d.ortho_scale=scale; d.lens=58
    ob['review_only']=True; ob.lock_location=(True,)*3; ob.lock_rotation=(True,)*3
    return ob
CAMS={
 'front':camera('Review_Front',(0,-12,1.5),(0,0,1.5)),
 'side':camera('Review_Side',(12,0,1.5),(0,0,1.5)),
 'back':camera('Review_Back',(0,12,1.5),(0,0,1.5)),
 'top':camera('Review_Top',(0,0,14),(0,0,0)),
 'three-quarter':camera('Review_ThreeQuarter',(-8,-10,6),(0,0,1.5)),
 'perspective':camera('Review_Hero',(0,-10,3.3),(0,0,1.5),persp=True)}
CAMS['top'].rotation_euler.z=math.pi
def guides():
    for view,p in DATA['plates'].items():
        ob=bpy.data.objects.new('REF_LOCKED_'+view,None); GUIDES.objects.link(ob); ob.empty_display_type='IMAGE'
        ob.data=bpy.data.images.load(str(ROOT/'assets/grimo/source/carol/approved-3d'/p['file'])); ob.data.pack()
        ob.empty_display_size=max(p['width_px'],p['height_px'])/p['pixels_per_unit']; ob.color[3]=.25
        u0,v0=p['origin_px']; cx=(p['width_px']/2-u0)/p['pixels_per_unit']; cz=(v0-p['height_px']/2)/p['pixels_per_unit']
        if view=='front': ob.location=(cx,2.8,cz); ob.rotation_euler=(math.pi/2,0,0)
        if view=='back': ob.location=(-cx,-2.8,cz); ob.rotation_euler=(math.pi/2,0,math.pi)
        if view=='side': ob.location=(2.8,cx,cz); ob.rotation_euler=(math.pi/2,0,-math.pi/2)
        if view=='top': ob.location=(cx,-cz,-.2); ob.rotation_euler=(0,0,0); ob.scale.y=-1
        ob.hide_render=True; ob.hide_select=True; ob.lock_location=(True,)*3; ob.lock_rotation=(True,)*3; ob.lock_scale=(True,)*3
        ob['registration']=json.dumps(p)
    GUIDES.hide_render=True
def settings():
    SC.render.engine='BLENDER_WORKBENCH'; SC.render.resolution_x=1000; SC.render.resolution_y=1000; SC.render.resolution_percentage=100
    SC.render.image_settings.file_format='PNG'; SC.render.image_settings.color_mode='RGBA'; SC.render.film_transparent=True
    SC.display.shading.light='STUDIO'; SC.display.shading.studiolight_rotate_z=.35; SC.display.shading.color_type='MATERIAL'
    SC.display.shading.show_shadows=True; SC.display.shading.show_cavity=True; SC.display.shading.cavity_type='BOTH'; SC.display.shading.curvature_ridge_factor=1.0; SC.display.shading.curvature_valley_factor=.7
    SC.view_settings.view_transform='Standard'; SC.view_settings.look='Medium High Contrast'
def render(view,path):
    SC.camera=CAMS[view]; SC.render.filepath=str(path); bpy.ops.render.render(write_still=True)
def secondary():
    for name in ['Primary_Fleece_Envelope','Primary_Rear_Tuft']:
        bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
    banks=runpy.run_path(str(Path(__file__).with_name('carol-v005-clouds.py')))['BANKS2' if ARGS.iteration>=2 else 'BANKS']
    designed=bpy.data.collections.new('Design_Masses_EDITABLE_hidden'); SC.collection.children.link(designed)
    pieces=[]
    for region,tuples in banks.items():
        for i,t in enumerate(tuples):
            ob=volume(f'Design_{region}_{i:02d}',t[:3],t[3:]); ob['region']=region
            source=ob.copy(); source.data=ob.data.copy(); designed.objects.link(source)
            pieces.append(ob)
    designed.hide_render=True; designed.hide_viewport=True
    pieces += [volume('Core_Head',(0,-.68,1.58),(.94,.84,1.02)),volume('Core_Body',(0,.56,1.16),(.86,1.00,.66))]
    if ARGS.iteration>=3:
        pieces += [volume('Core_Shoulder',(0,-.1,1.38),(1.01,1.12,.84)),volume('ShoulderFill_L',(-.99,-.58,1.40),(.34,.49,.48)),volume('ShoulderFill_R',(.99,-.55,1.38),(.34,.51,.49))]
    ob=union('Carol_Fleece_Hero',pieces,.018); ob['construction']='Explicit regional 3D banks, editable source volumes retained; voxel union; no radial field or source mesh'
    if ARGS.iteration>=2:
        bpy.context.view_layer.objects.active=ob
        mod=ob.modifiers.new('Round cloud junctions','SMOOTH'); mod.factor=1.4; mod.iterations=14 if ARGS.iteration>=3 else 35
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return ob
def proxy(fleece):
    import numpy as np
    m=material('Proxy_Fleece_WhiteBlue',(.81,.85,1),.72)
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Subsurface Weight'].default_value=.07
    bpy.context.view_layer.update()
    attr=fleece.data.color_attributes.new(name='Cloud_Palette',type='FLOAT_COLOR',domain='POINT')
    for i,v in enumerate(fleece.data.vertices):
        p=fleece.matrix_world@v.co
        blue=math.exp(-(((p.x+.85)/.67)**2+((p.y+.55)/.95)**2+((p.z-2.00)/.58)**2)*1.2)
        blue += .45*math.exp(-(((p.y-.65)/1.1)**2+((p.z-1.73)/.5)**2))
        blue=min(.90,blue); white=(.91,.87,.98); azure=(.31,.41,.91)
        attr.data[i].color=(*(white[k]*(1-blue)+azure[k]*blue for k in range(3)),1)
    nd=m.node_tree.nodes.new('ShaderNodeVertexColor');nd.layer_name='Cloud_Palette';m.node_tree.links.new(nd.outputs['Color'],bs.inputs['Base Color'])
    fleece.data.materials.clear();fleece.data.materials.append(m)
    SC.render.engine='CYCLES'; SC.cycles.samples=24; SC.cycles.use_denoising=True
    SC.world=bpy.data.worlds.new('Diagnostic_Studio'); SC.world.use_nodes=True; SC.world.node_tree.nodes['Background'].inputs[0].default_value=(.60,.67,.84,1); SC.world.node_tree.nodes['Background'].inputs[1].default_value=.5
    for name,pos,power,size in [('Key',(-4,-5,7),700,5),('Fill',(4,-3,4),450,4),('Rim',(1,4,6),800,4)]:
        d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.shape='DISK';d.size=size
        ob=bpy.data.objects.new(name,d); SC.collection.objects.link(ob); ob.location=pos;ob.rotation_euler=(Vector((0,0,1.5))-ob.location).to_track_quat('-Z','Y').to_euler()
    SC.view_settings.view_transform='AgX'; SC.view_settings.look='AgX - Medium High Contrast'
if __name__=='__main__':
    primary(); guides(); settings()
    if ARGS.stage in ['secondary','parts','hero']:
        fleece=secondary()
    if ARGS.stage in ['parts','hero']:
        runpy.run_path(str(Path(__file__).with_name('carol-v005-parts.py')))['build'](globals())
        proxy(fleece)
    folder=OUT/'iterations'/f'{ARGS.stage}-{ARGS.iteration:02d}'; folder.mkdir(parents=True,exist_ok=True)
    for view in ['front','side','back','top','three-quarter']:render(view,folder/f'{view}.png')
    bpy.context.preferences.filepaths.save_version=0
    dest=ROOT/'artifacts/carol-v005'; dest.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(dest/f'{ARGS.stage}.blend'))
