"""Carol semantic coat reconstruction. Run with Blender 5.2, from repo root.

Authoring volumes are fused and softened into three editable regional surfaces.
Frozen Skin is loaded verbatim; historical ornaments are rigid geometry donors.
No camera-dependent geometry, projected authority texture, rig or animation.
"""
import bpy, bmesh, math, json, hashlib, sys
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-normal-semantic-v001.blend'
WORK=ROOT/'artifacts/carol-semantic'
SKIN=ASSET.with_name('carol-skin-default-v004.blend')
DONOR=ASSET.with_name('carol-normal-fleece-v002.blend')
SKIN_SHA='c14f15e35af18e17a63506ea1f4c8ec0f69cb4f52882d27cfa22cb01db7e1f7d'
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def linear(c): return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c)
def parent(ob,owner):
    bpy.context.view_layer.update(); m=ob.matrix_world.copy(); ob.parent=owner; ob.matrix_world=m
def owner(name,loc):
    ob=bpy.data.objects.new(name,None); bpy.context.scene.collection.objects.link(ob); ob.location=loc; return ob

def ellipsoid(name,c,r,rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=c)
    ob=bpy.context.object; ob.name=name; ob.scale=r; ob.rotation_euler=rot
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return ob

def fuse(name,forms,own,voxel=.006):
    parts=[ellipsoid(name+'_form',*f) for f in forms]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in parts:ob.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join(); ob=parts[0];ob.name=name
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    mod=ob.modifiers.new('Fuse continuous coat','REMESH');mod.mode='VOXEL';mod.voxel_size=voxel;mod.use_smooth_shade=True
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=ob.modifiers.new('Soft cloud junctions','SMOOTH');mod.factor=1.35;mod.iterations=10
    bpy.ops.object.modifier_apply(modifier=mod.name)
    for p in ob.data.polygons:p.use_smooth=True
    parent(ob,own);ob['motion_owner']=own.name;ob['construction']='Fused overlapping anatomical volumes with unequal cloud hierarchy'
    ob['topology_status']='EDITABLE_CANDIDATE_NOT_LOCKED'
    return ob

def coat_forms():
    # X front->rear; Z ground->crown. Cheeks stop above the bare jaw.
    head=[((.385,0,.685),(.215,.288,.137)),
          ((.323,-.042,.793),(.133,.144,.100)),
          ((.408,.137,.762),(.135,.126,.107)),
          ((.440,-.162,.738),(.130,.130,.118)),
          ((.189,.045,.619),(.105,.126,.093)),
          ((.214,-.154,.637),(.115,.113,.100)),
          ((.245,.216,.610),(.108,.115,.111)),
          ((.290,-.320,.494),(.120,.083,.150)),
          ((.295,.320,.475),(.116,.085,.155)),
          ((.329,-.305,.371),(.104,.077,.074)),
          ((.342,.309,.368),(.103,.079,.075)),
          ((.426,-.290,.665),(.106,.094,.106)),
          ((.446,.282,.665),(.112,.094,.102)),
          ((.546,0,.660),(.127,.273,.127)),
          ((.235,-.048,.713),(.103,.106,.099)),
          ((.270,.192,.728),(.109,.107,.096))]
    body=[((.756,0,.520),(.406,.423,.339)),
          ((.475,0,.414),(.222,.335,.228)),
          ((.437,-.024,.186),(.160,.267,.079)),
          ((.716,-.087,.805),(.219,.228,.158)),
          ((.826,.170,.765),(.195,.184,.158)),
          ((.580,.232,.710),(.179,.205,.164)),
          ((.901,-.219,.666),(.191,.231,.208)),
          ((1.011,.104,.531),(.150,.284,.220)),
          ((.758,-.348,.505),(.200,.174,.202)),
          ((.760,.365,.525),(.194,.174,.181)),
          ((.536,-.295,.352),(.158,.138,.145)),
          ((.548,.296,.359),(.161,.139,.147)),
          ((.588,-.308,.265),(.185,.183,.123)),
          ((.694,.306,.246),(.212,.183,.104)),
          ((.926,-.284,.291),(.187,.166,.146)),
          ((.955,.274,.327),(.180,.189,.172)),
          ((1.050,-.130,.432),(.132,.229,.177)),
          ((.690,-.350,.603),(.113,.116,.136)),
          ((.888,.373,.538),(.115,.130,.128)),
          ((.956,-.293,.794),(.129,.158,.110)),
          ((.765,.357,.741),(.139,.121,.128)),
          ((.512,.413,.312),(.126,.121,.108)),
          ((.818,-.407,.349),(.115,.120,.104)),
          ((1.068,.173,.607),(.094,.146,.123)),
          ((.751,.018,.203),(.256,.263,.088)),
          ((.370,.213,.207),(.149,.146,.096)),
          ((.393,-.217,.217),(.151,.143,.101)),
          ((.365,.083,.163),(.100,.116,.064)),
          ((.408,-.126,.140),(.108,.121,.060)),
          ((.330,.237,.235),(.085,.098,.067)),
          ((1.015,-.018,.226),(.155,.285,.116)),
          ((1.102,.153,.225),(.104,.124,.089)),
          ((1.073,-.178,.203),(.108,.134,.080)),
          ((.790,-.235,.207),(.180,.155,.083)),
          ((.790,.235,.207),(.180,.155,.083))]
    # Unequal subordinate relief on selected outer caps; all fused into the
    # same coat. Tangent offsets keep clusters flowing across macro volumes.
    def relief(forms,indices,reference,size):
        extra=[]
        for i in indices:
            c,r=forms[i];c=Vector(c);r=Vector(r)
            n=(c-Vector(reference)).normalized()
            t=n.cross(Vector((1,0,0)))
            if t.length<.1:t=n.cross(Vector((0,1,0)))
            t.normalize();u=n.cross(t).normalized()
            offsets=[(-.42,-.12),(.28,.32),(.12,-.38)][:2+(i%3==0)]
            for j,(a,b) in enumerate(offsets):
                small=size*(.77+.14*((i+j)%3))
                p=c+Vector((n[k]*r[k]*.65 for k in range(3)))+t*(a*min(r))+u*(b*min(r))
                extra.append((tuple(p),(small,small*(1.1 if j==0 else .95),small*.91)))
        return extra
    head+=relief(head,[1,2,3,4,5,6,7,8,11,12,14,15],(.40,0,.57),.071)
    body+=relief(body,[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],(.75,0,.50),.091)
    tail=[((1.189,0,.414),(.080,.052,.051)),
          ((1.256,0,.442),(.083,.085,.084)),
          ((1.272,-.038,.476),(.054,.052,.048)),
          ((1.287,.042,.426),(.050,.056,.052)),
          ((1.270,-.032,.396),(.054,.055,.046))]
    return head,body,tail

def fleece_material():
    mat=bpy.data.materials.new('Carol dream cloud / continuous pearl azure');mat.use_nodes=True
    ns=mat.node_tree.nodes;lk=mat.node_tree.links;ns.clear()
    out=ns.new('ShaderNodeOutputMaterial');bs=ns.new('ShaderNodeBsdfPrincipled')
    bs.inputs['Roughness'].default_value=.78
    bs.inputs['Subsurface Weight'].default_value=.035
    bs.inputs['Specular IOR Level'].default_value=.24
    attr=ns.new('ShaderNodeVertexColor');attr.layer_name='DreamTint'
    tex=ns.new('ShaderNodeTexCoord');noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=35;noise.inputs['Detail'].default_value=2
    lk.new(tex.outputs['Generated'],noise.inputs['Vector'])
    ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.87,.88,.94,1);ramp.color_ramp.elements[1].color=(1,1,1,1)
    lk.new(noise.outputs['Fac'],ramp.inputs[0]);mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.22
    lk.new(attr.outputs['Color'],mix.inputs[1]);lk.new(ramp.outputs[0],mix.inputs[2])
    # Camera-independent, soft MToon-like normal ramp, plus real light/contact.
    geo=ns.new('ShaderNodeNewGeometry');dot=ns.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.55,-.30,.78);lk.new(geo.outputs['Normal'],dot.inputs[0])
    shade=ns.new('ShaderNodeMapRange');shade.interpolation_type='SMOOTHSTEP';shade.inputs['From Min'].default_value=-.28;shade.inputs['From Max'].default_value=.65;lk.new(dot.outputs['Value'],shade.inputs['Value'])
    tint=ns.new('ShaderNodeMixRGB');tint.name='Dream shadow tint';tint.inputs[1].default_value=(*linear((.74,.77,.99)),1);tint.inputs[2].default_value=(1,1,1,1);lk.new(shade.outputs[0],tint.inputs[0])
    shaded=ns.new('ShaderNodeMixRGB');shaded.blend_type='MULTIPLY';shaded.inputs[0].default_value=1;lk.new(mix.outputs[0],shaded.inputs[1]);lk.new(tint.outputs[0],shaded.inputs[2]);lk.new(shaded.outputs[0],bs.inputs['Base Color'])
    em=ns.new('ShaderNodeEmission');lk.new(shaded.outputs[0],em.inputs['Color'])
    comb=ns.new('ShaderNodeMixShader');comb.inputs[0].default_value=.38
    lk.new(em.outputs[0],comb.inputs[1]);lk.new(bs.outputs[0],comb.inputs[2]);lk.new(comb.outputs[0],out.inputs['Surface'])
    return mat

def paint(ob,mat,kind):
    pts=np.array([ob.matrix_world@v.co for v in ob.data.vertices]);x,y,z=pts.T
    if kind=='head':
        w=.18*np.exp(-((x-.48)/.19)**2-((abs(y)-.28)/.19)**2-((z-.67)/.20)**2)
    elif kind=='tail':w=.12*np.exp(-((z-.408)/.052)**2)
    else:
        w=.90*np.exp(-((x-.65)/.37)**2-((abs(y)-.31)/.29)**2-((z-.72)/.25)**2)
        w+=.24*np.exp(-((x-.48)/.22)**2-((abs(y)-.35)/.25)**2-((z-.29)/.16)**2)
        w+=.20*np.exp(-((x-.37)/.23)**2-(y/.32)**2-((z-.21)/.15)**2)
        w=np.clip(w,0,.82)
    pearl=np.array(linear((.99,.974,1.0)));blue=np.array(linear((.32,.48,1.0)))
    if kind=='body':w=np.clip(w*1.20,0,.97)
    col=pearl[None,:]*(1-w[:,None])+blue[None,:]*w[:,None]
    a=ob.data.color_attributes.new(name='DreamTint',type='FLOAT_COLOR',domain='POINT')
    a.data.foreach_set('color',np.column_stack((col,np.ones(len(col)))).ravel())
    ob.data.materials.clear();ob.data.materials.append(mat)

def bvh(obs):
    verts=[];faces=[]
    for ob in obs:
        offset=len(verts);verts += [ob.matrix_world@v.co for v in ob.data.vertices]
        faces += [tuple(offset+i for i in p.vertices) for p in ob.data.polygons]
    return BVHTree.FromPolygons(verts,faces)

def ornaments(head,body,head_owner,body_owner):
    with bpy.data.libraries.load(str(DONOR),link=False) as (src,dst):
        dst.objects=[n for n in src.objects if n.startswith('STAR_') and not n.endswith('_anchor') or n=='MOON']
    imported={}
    for ob in dst.objects:
        bpy.context.scene.collection.objects.link(ob);m=ob.matrix_world.copy();ob.parent=None;ob.matrix_world=m;imported[ob.name]=ob
    targets={'STAR_brow':((.12,-.015,.665),(-1,0,0),'head'),
      'STAR_crown':((.18,0,.830),(-1,0,.20),'head'),
      'STAR_chest':((.32,-.025,.178),(-1,0,-.10),'body'),
      'STAR_lower_left':((.44,.430,.302),(-.8,.5,0),'body'),
      'STAR_upper_left':((.56,.422,.573),(-.8,.5,.05),'body'),
      'STAR_rump':((.960,-.420,.40),(0,-1,0),'body'),
      'STAR_rump_L':((.960,.420,.40),(0,1,0),'body'),
      'MOON':((.62,.367,.764),(-.85,.52,.10),'body')}
    trees={'head':bvh([head]),'body':bvh([body])}
    for name,(target,normal,region) in targets.items():
        ob=imported[name]; pts=np.array([ob.matrix_world@v.co for v in ob.data.vertices]);center=Vector(pts.mean(axis=0))
        # Historical star front is -X; crescent is also authored around that axis.
        values,axes=np.linalg.eigh(np.cov(pts.T));old_normal=Vector(axes[:,0])
        outward=Vector((-1,1,0)) if name=='MOON' else Vector((0,-1 if name=='STAR_rump' else 1,0)) if name in ['STAR_rump','STAR_rump_L'] else Vector((-1,0,0))
        if old_normal.dot(outward)<0:old_normal=-old_normal
        n=Vector(normal).normalized();t=Vector(target)
        hit,hn,_,_=trees[region].ray_cast(t+n*2,-n,4)
        if hit is None:raise RuntimeError('No ornament surface: '+name)
        rot=old_normal.rotation_difference(n).to_matrix().to_4x4()
        # Center of rigid thickness sits just outward of surface; rear touches fleece.
        dest=hit+n*.013
        transform=Matrix.Translation(dest)@rot@Matrix.Translation(-center)
        for piece in [ob,imported.get(name+'_glint')]:
            if piece:
                piece.matrix_world=transform@piece.matrix_world;parent(piece,head_owner if region=='head' else body_owner)
        ob['surface_owner']=region;ob['contact_policy']='Rigid ornament seated on local coat surface'

def presentation():
    sc=bpy.context.scene
    for ob in list(bpy.data.objects):
        if ob.type in ['CAMERA','LIGHT']:bpy.data.objects.remove(ob,do_unlink=True)
    target=Vector((.61,0,.49))
    for yaw in [0,15,30,45,-45,90,-90,135,180]:
        name='front' if yaw==0 else 'side' if yaw==90 else 'rear' if yaw==180 else f'yaw{yaw:+03d}'
        a=math.radians(yaw);pos=target+Vector((-4*math.cos(a),4*math.sin(a),0))
        d=bpy.data.cameras.new('VIEW_'+name);d.type='ORTHO';d.ortho_scale=1.52
        ob=bpy.data.objects.new('VIEW_'+name,d);sc.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler()
    for name,pos,scale,typ in [('top',(.62,0,4),1.52,'ORTHO'),('hero',(-2.6,2.0,1.20),1.52,'PERSP')]:
        d=bpy.data.cameras.new('VIEW_'+name);d.type=typ;d.ortho_scale=scale;d.lens=80
        ob=bpy.data.objects.new('VIEW_'+name,d);sc.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(target-Vector(pos)).to_track_quat('-Z','Y').to_euler()
    for name,pos,power,size in [('Key',(-3,-2,4),85,4),('Fill',(-3,3,2),45,4),('Rim',(3,1,3),70,3)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
        ob=bpy.data.objects.new(name,d);sc.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()
    sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.86,.90,1,1);sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
    sc.render.engine='CYCLES';sc.cycles.samples=32;sc.cycles.use_denoising=True
    sc.render.resolution_x=sc.render.resolution_y=640;sc.render.resolution_percentage=100
    sc.render.film_transparent=True;sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
    sc.camera=bpy.data.objects['VIEW_front']

def build():
    assert sha(SKIN)==SKIN_SHA
    bpy.ops.wm.open_mainfile(filepath=str(SKIN));bpy.context.scene.frame_set(1)
    # Candidate-only internal accommodation: keep the original chassis intact
    # and hide it; render a copy with ONLY the low neck behind the bare jaw
    # recessed. Face above .255, support arrangement and standalone Skin stay
    # byte/coordinate-identical. This is not a Skin baseline revision.
    source=bpy.data.objects['CENTRAL_CHASSIS'];support=source.copy();support.data=source.data.copy();support.name='CANDIDATE_NECK_SUPPORT';bpy.context.scene.collection.objects.link(support)
    source.hide_render=True;source.hide_set(True)
    for key in support.data.shape_keys.key_blocks if support.data.shape_keys else [support.data]:
        points=key.data if hasattr(key,'data') else key.vertices
        for p in points:
            z=p.co.z
            if z<.255 and p.co.x<.40:
                t=max(0,min(1,(.255-z)/.105));t=t*t*(3-2*t)
                p.co.x+=.105*t;p.co.y*=1-.065*t
    support['candidate_local_only']='Low neck recessed behind bare jaw; original frozen chassis retained hidden; face above z=.255 unchanged'
    ho=owner('FLEECE_HEAD_OWNER',(.37,0,.57));bo=owner('FLEECE_TORSO_OWNER',(.73,0,.49))
    forms=coat_forms();head=fuse('HeadFleece',forms[0],ho);body=fuse('BodyFleece',forms[1],bo)
    tail=fuse('TailFleece',forms[2],bpy.data.objects['TAIL_PIVOT'],.004)
    mat=fleece_material()
    for ob,k in [(head,'head'),(body,'body')]:paint(ob,mat,k)
    tailmat=mat.copy();tailmat.name='Carol independent pearl tail';tailmat.node_tree.nodes['Dream shadow tint'].inputs[1].default_value=(*linear((.87,.89,1.0)),1);paint(tail,tailmat,'tail')
    ornaments(head,body,ho,bo);presentation()
    sc=bpy.context.scene;sc['production_state']='NORMAL_SEMANTIC_CANDIDATE';sc['frozen_skin_sha256']=SKIN_SHA;sc['generator_sha256']=sha(Path(__file__))
    sc['authority_note']='Human semantic spec; Front/Side visible authority; inferred unseen geometry'
    sc['human_visual_approval']=False
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.data.orphans_purge(do_local_ids=True,do_recursive=True)
    ASSET.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    print('SAVED',sha(ASSET))

def render():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));sc=bpy.context.scene
    assert sc['generator_sha256']==sha(Path(__file__)),'Rebuild after changing the generator'
    views=ARGS[ARGS.index('--views')+1].split(',') if '--views' in ARGS else ['front','yaw+15','yaw+30','yaw+45','yaw-45','side','yaw-90','yaw+135','rear','top','hero']
    mode=ARGS[ARGS.index('--mode')+1] if '--mode' in ARGS else 'beauty'
    folder=ROOT/'docs/production/carol/evidence/normal-semantic-v001'/mode if '--final' in ARGS else WORK/(ARGS[ARGS.index('--folder')+1] if '--folder' in ARGS else 'draft')
    folder.mkdir(parents=True,exist_ok=True)
    if '--size' in ARGS:sc.render.resolution_x=sc.render.resolution_y=int(ARGS[ARGS.index('--size')+1])
    if mode!='beauty':
        mat=bpy.data.materials.new('DIAGNOSTIC '+mode);mat.use_nodes=True;n=mat.node_tree.nodes;lk=mat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial')
        shader=n.new('ShaderNodeEmission' if mode=='silhouette' else 'ShaderNodeBsdfDiffuse');shader.inputs['Color'].default_value=(.025,.025,.035,1) if mode=='silhouette' else (.52,.52,.52,1);lk.new(shader.outputs[0],out.inputs['Surface'])
        for ob in sc.objects:
            if ob.type in ['MESH','CURVE']:
                ob.data.materials.clear();ob.data.materials.append(mat)
                if ob.type=='MESH':
                    for p in ob.data.polygons:p.material_index=0
    manifest={'asset_sha256':sha(ASSET),'generator_sha256':sha(Path(__file__)),'blender_version':bpy.app.version_string,'mode':mode,'views':{}}
    for v in views:
        sc.camera=bpy.data.objects['VIEW_'+v];sc.render.filepath=str(folder/(v+'.png'));bpy.ops.render.render(write_still=True)
        manifest['views'][v]={'sha256':sha(folder/(v+'.png')),'camera_matrix':[list(row) for row in sc.camera.matrix_world],'ortho_scale':sc.camera.data.ortho_scale,'size':[sc.render.resolution_x,sc.render.resolution_y]}
    assert sha(ASSET)==manifest['asset_sha256'],'Saved candidate changed while rendering'
    (folder/'render-manifest.json').write_text(json.dumps(manifest,indent=2))

if __name__=='__main__':
    WORK.mkdir(parents=True,exist_ok=True)
    render() if 'render' in ARGS else build()
