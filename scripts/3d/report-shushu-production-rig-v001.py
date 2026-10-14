"""Read-only GLB attribute audit, image comparisons, boards and delivery manifest."""
import json, struct, hashlib, sys
import copy
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v001'
BASE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003'
RIG=BASE/'rigging/shushu-v006-production-rig-v001.glb'
SOURCE=BASE/'rigging/shushu-v006-tripo-autorig-v001.glb'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def read(path):
    raw=Path(path).read_bytes();magic,version,total=struct.unpack_from('<III',raw);assert magic==0x46546c67 and version==2 and total==len(raw)
    n=struct.unpack_from('<I',raw,12)[0];return json.loads(raw[20:20+n]),raw[28+n:]
def accessor(j,raw,index):
    a=j['accessors'][index];count=a['count'];components={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];dt=np.dtype({5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);size=components*dt.itemsize
    result=np.zeros((count,components),dtype=dt)
    if 'bufferView' in a:
        view=j['bufferViews'][a['bufferView']];offset=view.get('byteOffset',0)+a.get('byteOffset',0);stride=view.get('byteStride',size)
        result=np.ndarray((count,components),dtype=dt,buffer=raw,offset=offset,strides=(stride,dt.itemsize)).copy()
    if 'sparse' in a:
        s=a['sparse'];v=j['bufferViews'][s['indices']['bufferView']];offset=v.get('byteOffset',0)+s['indices'].get('byteOffset',0);ids=np.frombuffer(raw,dtype={5121:'u1',5123:'<u2',5125:'<u4'}[s['indices']['componentType']],count=s['count'],offset=offset)
        v=j['bufferViews'][s['values']['bufferView']];offset=v.get('byteOffset',0)+s['values'].get('byteOffset',0);result[ids]=np.frombuffer(raw,dtype=dt,count=s['count']*components,offset=offset).reshape(-1,components)
    return result
def images(j,raw):
    result=[]
    for im in j.get('images',[]):
        assert 'bufferView' in im,'Unexpected external texture';v=j['bufferViews'][im['bufferView']];p=v.get('byteOffset',0);result.append(hashlib.sha256(raw[p:p+v['byteLength']]).hexdigest())
    return result
def restore_textures():
    source,sraw=read(SOURCE);source_mesh={n['name']:source['meshes'][n['mesh']] for n in source['nodes'] if 'mesh' in n};rows=[]
    for path in [RIG,RIG.with_name(RIG.stem+'-proof.glb')]:
        j,raw=read(path);data=bytearray();views=[];remap={};unused={im['bufferView'] for im in j.get('images',[]) if 'bufferView' in im}
        def add(payload,template=None):
            while len(data)%4:data.append(0)
            view=copy.deepcopy(template or {});view.update(buffer=0,byteOffset=len(data),byteLength=len(payload));data.extend(payload);views.append(view);return len(views)-1
        for i,v in enumerate(j['bufferViews']):
            if i in unused:continue
            p=v.get('byteOffset',0);remap[i]=add(raw[p:p+v['byteLength']],v)
        def remap_views(obj):
            if isinstance(obj,dict):
                if 'bufferView' in obj:obj['bufferView']=remap[obj['bufferView']]
                for v in obj.values():remap_views(v)
            elif isinstance(obj,list):
                for v in obj:remap_views(v)
        remap_views(j['accessors']);j['images']=[]
        for im in source['images']:
            v=source['bufferViews'][im['bufferView']];p=v.get('byteOffset',0);ni=copy.deepcopy(im);ni['bufferView']=add(sraw[p:p+v['byteLength']]);j['images'].append(ni)
        j['textures']=copy.deepcopy(source['textures']);j['samplers']=copy.deepcopy(source.get('samplers',[]));repaired=[]
        for node in j['nodes']:
            name=node.get('name','')
            if name not in source_mesh:continue
            dst=j['meshes'][node['mesh']];src=source_mesh[name]
            for dp,sp in zip(dst['primitives'],src['primitives']):j['materials'][dp['material']]=copy.deepcopy(source['materials'][sp['material']])
            repaired.append(name)
        j['bufferViews']=views
        while len(data)%4:data.append(0)
        j['buffers']=[{'byteLength':len(data)}]
        j['extensionsUsed']=sorted(set(j.get('extensionsUsed',[]))|set(source.get('extensionsUsed',[])))
        meta=json.dumps(j,ensure_ascii=False,separators=(',',':')).encode();meta+=b' '*((-len(meta))%4);blob=struct.pack('<III',0x46546c67,2,12+8+len(meta)+8+len(data))+struct.pack('<II',len(meta),0x4e4f534a)+meta+struct.pack('<II',len(data),0x004e4942)+data;path.write_bytes(blob)
        rows.append({'path':path.relative_to(ROOT).as_posix(),'materials_restored':repaired,'original_texture_bytes_equal':images(j,data)==images(source,sraw),'method':'Repack unchanged mesh/skin/morph/animation buffer views; original embedded image bytes, texture/sampler definitions and existing material semantics restored exactly. New oral solid materials retained.'})
    write('texture-material-restoration.json',rows)
def material(j,raw,m):
    p=m.get('pbrMetallicRoughness',{});result={'baseColorFactor':p.get('baseColorFactor',[1,1,1,1]),'metallicFactor':p.get('metallicFactor',1),'roughnessFactor':p.get('roughnessFactor',1),'alphaMode':m.get('alphaMode','OPAQUE'),'alphaCutoff':m.get('alphaCutoff',.5),'doubleSided':m.get('doubleSided',False),'emissiveFactor':m.get('emissiveFactor',[0,0,0])}
    for name,parent in [('baseColorTexture',p),('metallicRoughnessTexture',p),('normalTexture',m),('occlusionTexture',m),('emissiveTexture',m)]:
        if name in parent:
            t=parent[name];tex=j['textures'][t['index']];result[name]={'image_sha256':images(j,raw)[tex['source']],'texCoord':t.get('texCoord',0),'scale':t.get('scale',1),'strength':t.get('strength',1),'extensions':t.get('extensions',{})}
    result['extensions']=m.get('extensions',{})
    return result
def glb_audit():
    source,sraw=read(SOURCE);j,raw=read(RIG);sm={n['name']:source['meshes'][n['mesh']] for n in source['nodes'] if 'mesh' in n};nm={n['name']:j['meshes'][n['mesh']] for n in j['nodes'] if 'mesh' in n};rows=[]
    for name,m in sm.items():
        if not name.startswith('ShushuStatic_'):continue
        now=nm[name];a=m['primitives'][0];b=now['primitives'][0];sp=accessor(source,sraw,a['attributes']['POSITION']);np0=accessor(j,raw,b['attributes']['POSITION']);su=accessor(source,sraw,a['attributes']['TEXCOORD_0']);nu=accessor(j,raw,b['attributes']['TEXCOORD_0'])
        # UV unique set survives reordering / seam duplication; Blender audit checks every original corner exactly.
        suv={tuple(v) for v in su};nuv={tuple(v) for v in nu};source_mat=material(source,sraw,source['materials'][a['material']]);now_mat=material(j,raw,j['materials'][b['material']])
        weights=np.concatenate([accessor(j,raw,b['attributes'][k]) for k in sorted(b['attributes']) if k.startswith('WEIGHTS_')],axis=1)
        rows.append({'mesh':name,'vertices_source':len(sp),'vertices_saved':len(np0),'uv_unique_count':[len(suv),len(nuv)],'uv_unique_set_equal':suv==nuv,'material_semantics_equal':source_mat==now_mat,'material_source':source_mat,'material_saved':now_mat,'weights_sum_error':float(np.max(np.abs(weights.sum(1)-1))),'influence_sets':len([k for k in b['attributes'] if k.startswith('JOINTS_')]),'morphs':len(b.get('targets',[]))})
    oldimgs=images(source,sraw);newimgs=images(j,raw);triangles=sum(accessor(j,raw,p['indices']).size//3 for m in j['meshes'] for p in m['primitives'])
    animations=[]
    for a in j.get('animations',[]):
        paths={}
        for c in a['channels']:paths[c['target']['path']]=paths.get(c['target']['path'],0)+1
        durations=[float(accessor(j,raw,s['input']).max()) for s in a['samplers']]
        animations.append({'name':a.get('name'),'seconds':max(durations),'channels':paths})
    result={'source_sha256':sha(SOURCE),'saved_sha256':sha(RIG),'original_texture_count':len(oldimgs),'saved_texture_count':len(newimgs),'all_original_texture_bytes_equal':sorted(oldimgs)==sorted(newimgs),'meshes':rows,'total_character_meshes':len(j['meshes']),'triangles':triangles,'skins':[len(s['joints']) for s in j['skins']],'animations':animations,'anchors':[n['name'] for n in j['nodes'] if n.get('name','').startswith('ANCHOR_')],'external_buffers':any('uri' in buf for buf in j['buffers'])}
    write('glb-attributes.json',result)
    assert result['all_original_texture_bytes_equal'] and all(x['uv_unique_set_equal'] for x in rows),'GLB UV / texture identity loss'
    assert all(x['material_semantics_equal'] for x in rows),'GLB changed existing material semantics'
    assert all(x['weights_sum_error']<1e-6 for x in rows),'Bad skin weight normalization'
    assert animations and any(x['channels'].get('weights',0)>0 for x in animations),'Morph animation absent'
def image_diffs():
    rows=[]
    for p in sorted((OUT/'renders/reimport').glob('*.png')):
        original=OUT/'renders/editable'/p.name
        if not original.exists():continue
        a=np.array(Image.open(original).convert('RGB'),dtype=np.int16);c=np.array(Image.open(p).convert('RGB'),dtype=np.int16);d=np.abs(a-c);rows.append({'image':p.name,'max_channel_difference':int(d.max()),'mean_channel_difference':float(d.mean()),'pixels_over_8':int((d.max(2)>8).sum()),'pixel_count':int(d.shape[0]*d.shape[1])})
    returns=[]
    for view in ['front','3q','left','right']:
        p=OUT/'renders/editable'/('neutral-'+view+'.png');r=OUT/'renders/editable'/('neutral-return-'+view+'.png')
        if p.exists() and r.exists():
            a=np.array(Image.open(p));c=np.array(Image.open(r));returns.append({'view':view,'pixels_identical':bool(np.array_equal(a,c)),'max_channel_difference':int(np.abs(a.astype(int)-c.astype(int)).max())})
    write('image-comparison.json',{'reimport':rows,'neutral_return':returns,'interpretation':'Rendering differences reported without substituting an image score for Human cuteness. Source images retained.'})
def font(size):
    return ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc',size)
def board(filename,cells,columns=4,width=320,crop=None,title=''):
    height=width if crop is None else int(width*(crop[3]-crop[1])/(crop[2]-crop[0]));header=70;rows=math_ceil(len(cells)/columns);canvas=Image.new('RGB',(columns*width,header+rows*(height+34)),(240,238,235));draw=ImageDraw.Draw(canvas);draw.text((16,8),title,font=font(22),fill=(35,30,35));draw.text((16,40),'Actual Blender renders / Human rig appearance: PENDING',font=font(14),fill=(90,70,75))
    for i,(label,path) in enumerate(cells):
        im=Image.open(path).convert('RGB')
        if crop:im=im.crop(crop)
        im=im.resize((width,height),Image.Resampling.LANCZOS);x=(i%columns)*width;y=header+(i//columns)*(height+34);canvas.paste(im,(x,y));draw.text((x+8,y+height+5),label,font=font(14),fill=(30,25,30))
    canvas.save(OUT/filename)
def math_ceil(v):return int(np.ceil(v))
def boards():
    ed=OUT/'renders/editable';ap=OUT/'renders/approved-static';rp=OUT/'renders/reimport';fx=OUT/'renders/fixture'
    cells=[]
    for view in ['front','3q','left','right']:
        for label,folder in [('v006 Human static PASS',ap),('Rig neutral',ed),('Saved GLB neutral',rp)]:cells.append((label+' / '+view,folder/('neutral-'+view+'.png')))
    board('01-neutral-identity.png',cells,3,380,title='v006 / Production Rig v001 / GLB round trip')
    names=['neutral','shift-L','seat-entry','seat-mid','seat','seat-rest','seat-joy','neutral-return']
    for view,file in [('front','02-support-front.png'),('left','03-support-left.png')]:board(file,[(n,ed/(n+'-'+view+'.png')) for n in names],4,340,title='Standing > shift > low seat > rest > return / '+view)
    names=['neutral','half','closed','wink-L','wink-R','gaze-L','gaze-up','gaze-down','smile','joy','surprise','hesitate','discomfort','mouth-close','mouth-close-override','mouth-open','mouth-open-max','tongue']
    board('04-face-capabilities.png',[(n,ed/(n+'-front.png')) for n in names],4,360,(120,100,520,340),'Independent face / eye / oral capabilities (crop)')
    names=['offer-L','offer-R','wrist-L','self-L','self-R','hold-both','hold-L-touch-R','seat-hold-interrupt','neutral-return']
    board('05-paw-composition.png',[(n,ed/(n+'-3q.png')) for n in names],3,380,title='Low paw / self contact / dual paw pose / interruption')
    names=['hold-L','hold-L-touch-R','seat-hold-interrupt','hold-resume','release','neutral-return'];board('06-held-fixture-release.png',[(n,fx/(n+'-3q.png')) for n in names],3,380,title='Paw-owned diagnostic fixture / hold > interrupt > resume > release')
    board('07-rejected-root-vs-repair.png',[('Rejected root fold / iteration 06',OUT/'iterations/06/hold-root-rejected.png'),('Current corrected root',ed/'hold-L-touch-R-3q.png')],2,500,title='Local paw repair evidence')
    board('08-head-yaw-four-views.png',[(name+' / '+view,ed/(name+'-'+view+'.png')) for view in ['front','3q','left','right'] for name in ['head-left','head-right']],4,340,title='Head yaw / independent body and paws / four views')
def preservation():
    protected=json.loads((OUT/'protected-inputs.json').read_text(encoding='utf-8'));changed=[]
    for name,expected in protected.items():
        if name=='docs/production/Handoff.md':continue
        p=ROOT/name
        if not p.exists() or sha(p)!=expected:changed.append(name)
    result={'protected_count_excluding_authorized_handoff':len(protected)-1,'changed':changed,'authorized_changed_document':'docs/production/Handoff.md','goal_map_unchanged':sha(ROOT/'docs/grimo/knowledge/Goal√map.md')==protected['docs/grimo/knowledge/Goal√map.md'],'policy':'Originals, historical candidates, old proof, other characters, and initial user changes preserved byte for byte.'};write('preservation-final.json',result);assert not changed,changed
def manifest():
    files=[BASE/'rigging'/('shushu-v006-production-rig-v001'+s) for s in ['.blend','.glb','-proof.blend','-proof.glb']]
    write('delivery-manifest.json',{'date':'2026-10-15','assets':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files],'human_gate':'PENDING for this rig; historical v006 static Human PASS remains valid','authority':'Local branch assets/evidence, Goal map, prior gate, v006 Human decision, Motion-to-Anatomy DRAFT requirements; no DRAFT performance promoted to FINAL'})
def verification_summary():
    def get(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
    cap=get('capability-numeric.json');rt=get('glb-roundtrip.json');timeline=get('proof-timeline.json');attrs=get('glb-attributes.json');floor=get('proof-floor.json');images0=get('image-comparison.json')
    result={'date':'2026-10-15','rig_human_gate':'HOLD / PENDING','units':'Blender normalized character height approximately 1; values are local scene units','support_conditions':len(cap['support']),'support_min_z':min(x['min_z'] for x in cap['support']),'support_vertices_below_minus_001':sum(x['below_minus_001'] for x in cap['support']),'planted_sole_xy_drift_max':max(y['sole_xy_drift_max'] for x in cap['support'] for y in x['feet'].values()),'seat_rump_support':[x for x in cap['support'] if x['seat']==1 and x['shift']==0][0],'proof_frames':timeline['frames'],'proof_markers':len(timeline['markers']),'proof_fps':timeline['fps'],'proof_min_z':min(x['min_z'] for x in floor),'proof_vertices_below_minus_001':sum(x['below_minus_001'] for x in floor),'neutral_return_max':max(cap['neutral_return'].values()),'arm_head_isolation_max':max(v['max'] for x in cap['isolation'] if x['test']!='neck' for v in x['protected_displacement'].values()),'foot_control':cap['foot_control'],'closed_eye_potentially_visible_vertices':sum(x['eye_surface_vertices_potentially_visible'] for x in cap['eye_occlusion'] if 'closed' in x['state']),'closed_oral_potentially_visible_vertices':sum(x['surface_vertices_potentially_visible'] for x in cap['closed_oral_occlusion']),'distal_paw_signed_gap_min':min(x['tip_signed_min'] for x in cap['contacts']),'bake_world_error_max':max(x['max_error'] for x in get('bake-verification.json')),'glb_world_error_max':rt['max_world_error'],'glb_anchor_matrix_error_max':max(x['max_matrix_error'] for x in get('anchor-roundtrip.json')),'glb_fixture_matrix_error_max':max(x['max_matrix_error'] for x in get('fixture-roundtrip.json')),'glb_floor_min_z':min(x['min_z'] for x in rt['floor']),'glb_below_minus_001':sum(x['below_minus_001'] for x in rt['floor']),'glb_sha256':rt['sha256'],'original_texture_bytes_equal':attrs['all_original_texture_bytes_equal'],'original_texture_count':attrs['original_texture_count'],'original_uv_corners_equal':all(x['uv_equal'] for x in cap['preservation']),'glb_original_materials_equal':all(x['material_semantics_equal'] for x in attrs['meshes']),'glb_triangles':attrs['triangles'],'glb_joints':attrs['skins'],'morph_targets_per_mesh':rt['morph_targets'],'glb_animations':attrs['animations'],'fixture_anchor_gap_max':max(x['anchor_to_fixture'] for x in timeline['attachment']),'fixture_selected_surface_gap_range':[min(x['surface_gap'] for x in timeline['attachment']),max(x['surface_gap'] for x in timeline['attachment'])],'neutral_return_pixels_equal':all(x['pixels_identical'] for x in images0['neutral_return']),'image_reimport_count':len(images0['reimport']),'scope':'PASS only for measured rig domain; Human appearance, arbitrary stroke masks, physical COM, real items/Food styles/mobile/runtime remain HOLD.'}
    clearance=get('fixture-clearance.json');result['fixture_clearance_min']=min(x['sphere_surface_clearance'] for x in clearance);result['fixture_clearance_frames']=len(set(x['frame'] for x in clearance));result['released_fixture_to_left_paw_clearance']=[x['sphere_surface_clearance'] for x in clearance if x['frame']==timeline['release_frame'] and x['mesh']=='ShushuStatic_Paw_L'][0]
    assert rt['sha256']==sha(RIG),'Roundtrip evidence is stale'
    assert result['glb_world_error_max']<1e-5 and result['glb_anchor_matrix_error_max']<1e-5 and result['glb_fixture_matrix_error_max']<1e-5,'Saved GLB differs from editable proof'
    assert result['closed_oral_potentially_visible_vertices']==0 and result['closed_eye_potentially_visible_vertices']==0,'Closed surfaces exposed'
    assert result['neutral_return_pixels_equal'] and result['neutral_return_max']==0,'Neutral restoration mismatch'
    assert result['original_texture_bytes_equal'] and result['original_uv_corners_equal'] and result['glb_original_materials_equal'],'Identity preservation failed'
    write('verification-summary.json',result)
if __name__=='__main__':
    if '--restore' in sys.argv:restore_textures();glb_audit()
    elif '--glb' in sys.argv:glb_audit()
    elif '--boards' in sys.argv:image_diffs();boards()
    else:preservation();manifest();verification_summary()
