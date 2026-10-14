"""Read-only source inspection and isolated renders; never opens production blends."""
import json, struct, hashlib, io, sys
import subprocess, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/production/shushu/evidence/tripo-texture-v003'
SOURCE = ROOT/'shushu-geometry-v003-tripo.glb.glb'
EYE_CONFIG = json.loads(Path(sys.argv[sys.argv.index('--eye-config')+1]).read_text(encoding='utf-8')) if '--eye-config' in sys.argv else None
if EYE_CONFIG:
    OUT = ROOT/EYE_CONFIG['evidence']
    SOURCE = ROOT/EYE_CONFIG['base']
OUT.mkdir(parents=True,exist_ok=True)

def sha(data): return hashlib.sha256(data).hexdigest()

def read_glb(path):
    data = path.read_bytes()
    magic, version, length = struct.unpack_from('<4sII', data)
    assert (magic, version, length) == (b'glTF', 2, len(data))
    chunks = []; pos = 12
    while pos < len(data):
        size, kind = struct.unpack_from('<I4s', data, pos)
        chunks.append((kind, data[pos+8:pos+8+size])); pos += 8+size
    return json.loads(chunks[0][1]), chunks[1][1]

def inspect():
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = ROOT/'.git/shushu-tripo-texture-v003'
    tmp.mkdir(exist_ok=True)
    j,b = read_glb(SOURCE); rows=[]
    for i, im in enumerate(j['images']):
        v=j['bufferViews'][im['bufferView']]; start=v.get('byteOffset',0)
        data=b[start:start+v['byteLength']]
        names=[m['name'] for m in j['meshes'] if any(j['textures'][j['materials'][p['material']]['pbrMetallicRoughness']['baseColorTexture']['index']]['source']==i for p in m['primitives'])]
        path=tmp/(str(i)+'-'+names[0]+'.jpg');path.write_bytes(data)
        nodes=[n['name'] for n in j['nodes'] if n.get('mesh') in [k for k,m in enumerate(j['meshes']) if m['name'] in names]]
        rows.append({'index':i,'meshes':names,'nodes':nodes,'size':Image.open(io.BytesIO(data)).size,'sha256':sha(data),'source_buffer_view':im['bufferView']})
    (OUT/'source-inspection.json').write_text(json.dumps({'source_sha256':sha(SOURCE.read_bytes()),'images':rows,'meshes':j['meshes'],'materials':j['materials'],'nodes':j['nodes'],'animations':len(j.get('animations',[]))},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'images':rows,'nodes':j['nodes']},indent=2))

def protect():
    paths=subprocess.check_output(['git','ls-files','-z','assets/grimo','docs/production/shushu'],cwd=ROOT).decode().split('\0')
    paths+=subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    paths+=['shushu-geometry-v003-tripo.glb.glb']
    excluded=('scripts/blender/review-shushu-tripo','scripts/3d/patch-shushu-tripo-texture-v003.cjs', (EYE_CONFIG['evidence']+'/' if EYE_CONFIG else 'docs/production/shushu/evidence/tripo-texture-v003/'))
    protected={p:sha((ROOT/p).read_bytes()) for p in sorted(set(paths)) if p and (ROOT/p).is_file() and not p.startswith(excluded) and (not EYE_CONFIG or p!=EYE_CONFIG['candidate'])}
    (OUT/'protected-inputs.json').write_text(json.dumps(protected,indent=2)+'\n',encoding='utf-8')
    print('Protected',len(protected),'inputs')

def render():
    import bpy
    from mathutils import Vector
    bpy.ops.wm.read_factory_settings(use_empty=True)
    path=Path(sys.argv[sys.argv.index('--asset')+1]) if '--asset' in sys.argv else SOURCE
    version='candidate' if path!=SOURCE else 'before'
    (OUT/f'{version}-render-source.json').write_text(json.dumps({'asset_sha256':sha(path.read_bytes()),'blender_version':bpy.app.version_string},indent=2)+'\n')
    bpy.ops.import_scene.gltf(filepath=str(path))
    objects=[o for o in bpy.data.objects if o.type=='MESH']
    bounds={o.name: {'min':[min((o.matrix_world@v.co)[i] for v in o.data.vertices) for i in range(3)],'max':[max((o.matrix_world@v.co)[i] for v in o.data.vertices) for i in range(3)],'vertices':len(o.data.vertices),'polygons':len(o.data.polygons)} for o in objects}
    (OUT/'imported-bounds.json').write_text(json.dumps(bounds,indent=2)+'\n')
    # Emission exposes the existing color without light/shadow ambiguity.
    for mat in bpy.data.materials:
        nodes=mat.node_tree.nodes; links=mat.node_tree.links
        tex=next(n for n in nodes if n.type=='TEX_IMAGE')
        output=next(n for n in nodes if n.type=='OUTPUT_MATERIAL')
        emission=nodes.new('ShaderNodeEmission'); links.new(tex.outputs['Color'],emission.inputs['Color']); links.new(emission.outputs[0],output.inputs['Surface'])
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=False
    scene.render.resolution_x=1024;scene.render.resolution_y=1024;scene.render.resolution_percentage=100
    scene.world=bpy.data.worlds.new('Review neutral');scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.72,.72,.72,1)
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    head=next(o for o in objects if o.name=='ShushuStatic_Head')
    mn,mx=bounds[head.name]['min'],bounds[head.name]['max']
    target=Vector(((mn[0]+mx[0])/2,(mn[1]+mx[1])/2,(mn[2]+mx[2])/2))
    camdata=bpy.data.cameras.new('ReviewCamera');cam=bpy.data.objects.new('ReviewCamera',camdata);scene.collection.objects.link(cam);scene.camera=cam
    camdata.type='ORTHO'; camdata.ortho_scale=(mx[0]-mn[0])*1.18
    views={'front':(0,-1,0),'left-three-quarter':(-.707,-.707,0),'right-three-quarter':(.707,-.707,0),'left-side':(-1,0,0),'right-side':(1,0,0)}
    if EYE_CONFIG: views.update(EYE_CONFIG.get('extra_views',{}))
    folder=OUT/'renders';folder.mkdir(exist_ok=True)
    cameras={}
    for name,direction in views.items():
        d=Vector(direction); cam.location=target+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(folder/f'{version}-{name}.png');bpy.ops.render.render(write_still=True)
        cameras[name]={'target':list(target),'direction':list(d),'orthographic_scale':camdata.ortho_scale,'resolution':[1024,1024],'color':'Standard / emission base color','engine':'CYCLES','samples':8,'denoise':False}
    if '--diagnose' in sys.argv:
        d=Vector(views['front']);cam.location=target+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
        for label,keep in [('head-only',['ShushuStatic_Head']),('modules-only',[o.name for o in objects if o!=head])]:
            for o in objects:o.hide_render=o.name not in keep
            scene.render.filepath=str(folder/f'diagnostic-{label}.png');bpy.ops.render.render(write_still=True)
        for o in objects:o.hide_render=False
        mat=bpy.data.materials.new('Diagnostic flat Head');mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear()
        em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.92,.84,.76,1);out=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(em.outputs[0],out.inputs[0])
        head.data.materials.clear();head.data.materials.append(mat)
        scene.render.filepath=str(folder/'diagnostic-flat-head.png');bpy.ops.render.render(write_still=True)
    if EYE_CONFIG and EYE_CONFIG.get('diagnostic_views') and version=='before':
        for o in objects:o.hide_render=o!=head
        for name in EYE_CONFIG['diagnostic_views']:
            d=Vector(views[name]);cam.location=target+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
            scene.render.filepath=str(folder/f'diagnostic-head-only-{name}.png');bpy.ops.render.render(write_still=True)
        flat=bpy.data.materials.new('Diagnostic flat fur Head');flat.use_nodes=True;nodes=flat.node_tree.nodes;nodes.clear()
        em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.92,.84,.76,1);out=nodes.new('ShaderNodeOutputMaterial');flat.node_tree.links.new(em.outputs[0],out.inputs[0])
        head.data.materials.clear();head.data.materials.append(flat)
        for o in objects:o.hide_render=False
        for name in EYE_CONFIG['diagnostic_views']:
            d=Vector(views[name]);cam.location=target+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
            scene.render.filepath=str(folder/f'diagnostic-flat-head-{name}.png');bpy.ops.render.render(write_still=True)
    (OUT/f'{version}-cameras.json').write_text(json.dumps(cameras,indent=2)+'\n')
    print('ISOLATED_RENDER_COMPLETE',version,flush=True)

def projection():
    """Map selected existing Head texels to the verified orthographic image."""
    import bpy
    import numpy as np
    from mathutils import Vector
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(SOURCE))
    head=bpy.data.objects['ShushuStatic_Head']; mesh=head.data
    mesh.calc_loop_triangles(); uv=mesh.uv_layers.active.data
    view=(sys.argv[sys.argv.index('--projection-view')+1] if '--projection-view' in sys.argv else EYE_CONFIG.get('projection_view','front')) if EYE_CONFIG else 'front'
    camera=json.loads((OUT/'before-cameras.json').read_text())[view]
    target=camera['target']; scale=camera['orthographic_scale']
    direction=Vector(camera['direction']).normalized();rotation=(-direction).to_track_quat('-Z','Y')
    right=rotation@Vector((1,0,0));up=rotation@Vector((0,1,0));inverse=head.matrix_world.inverted()
    eye=[[389,508],[397,519],[405,545],[408,573],[405,599],[396,624],[382,643],[360,658],[332,666],[308,667],[308,661],[332,660],[357,652],[377,637],[389,617],[397,596],[400,573],[398,548],[391,524]]
    mouth=[[405,629],[432,629],[434,646],[451,652],[459,665],[467,714],[451,721],[428,713],[415,685],[408,660]]
    masks={'eye-screen-left':eye,'eye-screen-right':[[1024-x,y] for x,y in eye], 'mouth-screen-left':mouth,'mouth-screen-right':[[1024-x,y] for x,y in mouth]}
    if EYE_CONFIG: masks=({k:v for k,v in EYE_CONFIG['masks'].items() if k.startswith(view)} if EYE_CONFIG.get('mode')=='fur-seam' else EYE_CONFIG['masks'])
    points=[p for poly in masks.values() for p in poly]
    xmin,xmax=min(p[0] for p in points),max(p[0] for p in points)
    ymin,ymax=min(p[1] for p in points),max(p[1] for p in points)
    if not EYE_CONFIG: xmin,xmax,ymin,ymax=300,724,500,720
    (OUT/(f'projection-masks-{view}.json' if EYE_CONFIG and EYE_CONFIG.get('mode')=='fur-seam' else 'projection-masks.json')).write_text(json.dumps(masks,indent=2)+'\n')
    def inside(x,y,poly):
        hit=np.zeros(x.shape,dtype=bool)
        for p,q in zip(poly,poly[1:]+poly[:1]):
            if p[1]==q[1]:continue
            hit^=((p[1]>y)!=(q[1]>y)) & (x<(q[0]-p[0])*(y-p[1])/(q[1]-p[1])+p[0])
        return hit
    mapping={}
    for tri in mesh.loop_triangles:
        world=np.array([head.matrix_world@mesh.vertices[v].co for v in tri.vertices])
        if view=='front':
            if world[:,1].min()>-.1 or tri.normal.y>-.15:continue
        elif (head.matrix_world.to_3x3()@tri.normal).dot(direction)<.15:continue
        relative=world-np.array(target)
        screen=np.column_stack((relative@np.array(right)/scale*1024+512,512-relative@np.array(up)/scale*1024))
        if screen[:,0].max()<xmin or screen[:,0].min()>xmax or screen[:,1].max()<ymin or screen[:,1].min()>ymax:continue
        tex=np.array([[uv[i].uv.x*2048,(1-uv[i].uv.y)*2048] for i in tri.loops])
        lo=np.maximum(np.floor(tex.min(0)).astype(int),0);hi=np.minimum(np.ceil(tex.max(0)).astype(int),2047)
        xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1))
        matrix=np.column_stack((tex[0]-tex[2],tex[1]-tex[2]))
        if abs(np.linalg.det(matrix))<1e-8:continue
        a,b=(np.linalg.inv(matrix)@np.stack((xx.ravel()+.5-tex[2,0],yy.ravel()+.5-tex[2,1]))).reshape(2,*xx.shape)
        c=1-a-b; valid=(a>=0)&(b>=0)&(c>=0)
        sx=a*screen[0,0]+b*screen[1,0]+c*screen[2,0];sy=a*screen[0,1]+b*screen[1,1]+c*screen[2,1]
        selected=np.zeros(xx.shape,dtype=bool)
        for poly in masks.values():selected|=inside(sx,sy,poly)
        for x,y,u,v in zip(xx[valid&selected],yy[valid&selected],sx[valid&selected],sy[valid&selected]):
            # Exclude concealed texels: do not paint a rear or hidden Head face.
            origin=Vector(target)+right*((u-512)/1024*scale)+up*((512-v)/1024*scale)+direction*3
            hit,loc,normal,face=head.ray_cast(inverse@origin,inverse.to_3x3()@(-direction))
            if not hit or face!=tri.polygon_index:continue
            mapping[(int(x),int(y))]=[int(x),int(y),round(float(u),4),round(float(v),4)]
    (OUT/(f'projection-map-{view}.json' if EYE_CONFIG and EYE_CONFIG.get('mode')=='fur-seam' else 'projection-map.json')).write_text(json.dumps(list(mapping.values()),separators=(',',':'))+'\n')
    print('Selected Head texels',len(mapping),flush=True)

def boards():
    from PIL import Image, ImageDraw
    import numpy as np
    views=['front','left-three-quarter','right-three-quarter','left-side','right-side']
    sheet=Image.new('RGB',(1536,5*544),(245,242,239));draw=ImageDraw.Draw(sheet)
    differences={}
    for row,name in enumerate(views):
        before=Image.open(OUT/'renders'/f'before-{name}.png').convert('RGB')
        after=Image.open(OUT/'renders'/f'candidate-{name}.png').convert('RGB')
        a,b=np.array(before),np.array(after);delta=np.abs(a.astype(int)-b.astype(int));changed=np.any(delta>0,axis=2)
        visible=np.any(delta>3,axis=2);yy,xx=np.where(visible)
        differences[name]={'different_pixels':int(changed.sum()),'above_3_levels_pixels':int(visible.sum()),'above_3_levels_bbox':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())] if len(xx) else None,'max_channel_delta':int(delta.max())}
        differences[name]['eye_and_upper_face_pixels_changed']=int(changed[:625].sum())
        if not EYE_CONFIG: assert not changed[:625].any(),'Unexpected eye / upper face render change'
        if EYE_CONFIG and name=='front':
            outside=changed.copy()
            for poly in EYE_CONFIG['masks'].values():
                px,py=zip(*poly)
                outside[max(0,min(py)-6):min(1024,max(py)+7),max(0,min(px)-6):min(1024,max(px)+7)]=False
            assert not outside.any(),'Unexpected non-eye render change'
            differences[name]['outside_eye_regions_pixels']=int(outside.sum())
            differences[name]['mouth_and_lower_face_pixels_changed']=int(changed[670:].sum())
        diff=Image.fromarray(np.minimum(delta*4,255).astype('uint8'))
        for col,(label,im) in enumerate([('BEFORE / source GLB',before),('CANDIDATE / saved GLB',after),('DIFFERENCE x4',diff)]):
            draw.text((col*512+10,row*544+8),f'{name} - {label}',fill=(40,30,30))
            sheet.paste(im.resize((512,512)),(col*512,row*544+32))
        if name=='front' and not EYE_CONFIG:
            outside=changed.copy();outside[490:732,230:795]=False
            differences[name]['outside_eye_mouth_bounding_region_pixels']=int(outside.sum())
    sheet.save(OUT/'01-five-angle-before-candidate-difference.png')
    ref=Image.open(ROOT/'assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_front.png').convert('RGB').crop((0,70,1086,785))
    panel=Image.new('RGB',(1536,544),(245,242,239));draw=ImageDraw.Draw(panel)
    for col,(label,im) in enumerate([('Approved Body-only / face crop',ref),('BEFORE / source GLB',Image.open(OUT/'renders/before-front.png')),('CANDIDATE / saved GLB',Image.open(OUT/'renders/candidate-front.png'))]):
        draw.text((col*512+10,8),label,fill=(40,30,30));im.thumbnail((512,512));panel.paste(im,(col*512+(512-im.width)//2,32+(512-im.height)//2))
    panel.save(OUT/'00-authority-before-candidate.png')
    panel=Image.new('RGB',(1536,1088),(245,242,239));draw=ImageDraw.Draw(panel)
    for row,(view,reference) in enumerate([('left-side','right'),('right-side','left')]):
        ref=Image.open(ROOT/f'assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_{reference}.png').convert('RGB')
        ref=ref.crop((0,0,ref.width,round(ref.height*.56)))
        for col,(label,im) in enumerate([('Approved Body-only / head crop',ref),('BEFORE / source GLB',Image.open(OUT/'renders'/f'before-{view}.png')),('CANDIDATE / saved GLB',Image.open(OUT/'renders'/f'candidate-{view}.png'))]):
            draw.text((col*512+10,row*544+8),f'{view} - {label}',fill=(40,30,30));im.thumbnail((512,512));panel.paste(im,(col*512+(512-im.width)//2,row*544+32+(512-im.height)//2))
    panel.save(OUT/'02-approved-sides-before-candidate.png')
    if EYE_CONFIG:
        panel=Image.new('RGB',(1710,1654),(245,242,239));draw=ImageDraw.Draw(panel)
        for row,(side,box) in enumerate([('screen-left',(145,425,430,690)),('screen-right',(595,425,880,690))]):
            for col,version in enumerate(['before','candidate']):
                im=Image.open(OUT/'renders'/f'{version}-front.png').crop(box).resize((855,795))
                draw.text((col*855+10,row*827+8),f'{side} / {version} saved GLB / crop x3',fill=(40,30,30))
                panel.paste(im,(col*855,row*827+32))
        panel.save(OUT/'04-eye-closeups.png')
    # Original model renders above remain unretouched. Boards only scale/layout.
    cameras=json.loads((OUT/'before-cameras.json').read_text());assert cameras==json.loads((OUT/'candidate-cameras.json').read_text())
    protected=json.loads((OUT/'protected-inputs.json').read_text())
    changed_inputs=[p for p,h in protected.items() if not (ROOT/p).exists() or sha((ROOT/p).read_bytes())!=h]
    assert not changed_inputs,changed_inputs
    validation=json.loads((OUT/'candidate-validation.json').read_text())
    candidate_render=json.loads((OUT/'candidate-render-source.json').read_text())
    assert candidate_render['asset_sha256']==validation['candidate_sha256'],'Stale candidate renders'
    manifest={'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'rendered_candidate_sha256':candidate_render['asset_sha256'],'protected_inputs_checked':len(protected),'changed_protected_inputs':changed_inputs,'matched_cameras':True,'render_differences':differences,'files':{p.relative_to(OUT).as_posix():sha(p.read_bytes()) for p in sorted(OUT.rglob('*.png'))}}
    (OUT/'review-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k!='files'},indent=2))

if __name__=='__main__':
    if '--inspect' in sys.argv: inspect()
    if '--protect' in sys.argv: protect()
    if '--render' in sys.argv: render()
    if '--projection' in sys.argv: projection()
    if '--boards' in sys.argv: boards()
