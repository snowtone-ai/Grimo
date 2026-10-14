"""Exact texture preservation, unretouched comparison boards and delivery hashes."""
import sys, json, hashlib, struct, copy, importlib.util, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v002'
RIG=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v002.glb'
spec=importlib.util.spec_from_file_location('report_v001',Path(__file__).with_name('report-shushu-production-rig-v001.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r);r.OUT=OUT;r.RIG=RIG

def textures():
    source,sraw=r.read(r.SOURCE);source_mesh={n['name']:source['meshes'][n['mesh']] for n in source['nodes'] if 'mesh' in n};rows=[]
    for path in [RIG,RIG.with_name(RIG.stem+'-proof.glb'),RIG.with_name(RIG.stem+'-contacts.glb')]:
        j,raw=r.read(path);numeric_before=hashlib.sha256(b''.join(r.accessor(j,raw,i).tobytes() for i in range(len(j['accessors'])))).hexdigest();data=bytearray();views=[];remap={};unused={im['bufferView'] for im in j.get('images',[]) if 'bufferView' in im}
        def add(payload,template=None):
            while len(data)%4:data.append(0)
            view=copy.deepcopy(template or {});view.update(buffer=0,byteOffset=len(data),byteLength=len(payload));data.extend(payload);views.append(view);return len(views)-1
        for i,view in enumerate(j['bufferViews']):
            if i in unused:continue
            start=view.get('byteOffset',0);remap[i]=add(raw[start:start+view['byteLength']],view)
        def remap_views(obj):
            if isinstance(obj,dict):
                if 'bufferView' in obj:obj['bufferView']=remap[obj['bufferView']]
                for val in obj.values():remap_views(val)
            elif isinstance(obj,list):
                for val in obj:remap_views(val)
        remap_views(j['accessors']);j['images']=[]
        for im in source['images']:
            view=source['bufferViews'][im['bufferView']];start=view.get('byteOffset',0);ni=copy.deepcopy(im);ni['bufferView']=add(sraw[start:start+view['byteLength']]);j['images'].append(ni)
        j['textures']=copy.deepcopy(source['textures']);j['samplers']=copy.deepcopy(source.get('samplers',[]))
        for node in j['nodes']:
            if node.get('name') not in source_mesh:continue
            for dp,sp in zip(j['meshes'][node['mesh']]['primitives'],source_mesh[node['name']]['primitives']):j['materials'][dp['material']]=copy.deepcopy(source['materials'][sp['material']])
        j['bufferViews']=views
        while len(data)%4:data.append(0)
        j['buffers']=[{'byteLength':len(data)}];extensions=sorted(set(j.get('extensionsUsed',[]))|set(source.get('extensionsUsed',[])))
        if extensions:j['extensionsUsed']=extensions
        else:j.pop('extensionsUsed',None)
        meta=json.dumps(j,ensure_ascii=False,separators=(',',':')).encode();meta+=b' '*((-len(meta))%4)
        path.write_bytes(struct.pack('<III',0x46546c67,2,12+8+len(meta)+8+len(data))+struct.pack('<II',len(meta),0x4e4f534a)+meta+struct.pack('<II',len(data),0x004e4942)+data)
        numeric_after=hashlib.sha256(b''.join(r.accessor(j,data,i).tobytes() for i in range(len(j['accessors'])))).hexdigest()
        assert numeric_before==numeric_after,'Numeric accessor changed during texture restoration'
        assert r.images(j,data)==r.images(source,sraw),'Original image bytes changed'
        rows.append({'path':path.relative_to(ROOT).as_posix(),'original_images_equal':True,'accessor_sha_before':numeric_before,'accessor_sha_after':numeric_after,'geometry_skin_morph_animation_buffers':'Every decoded accessor unchanged; numeric reimport evidence remains applicable across metadata-only correction'})
    r.write('texture-material-restoration.json',rows);r.glb_audit()

def boards():
    before=OUT/'renders/before';after=OUT/'renders/candidate';reimport=OUT/'renders/reimport';fx=OUT/'renders/fixture'
    r.board('00-neutral-identity.png',[(label+' / '+view,folder/('neutral-'+view+'.png')) for view in ['front','3q-L','3q-R','left','right'] for label,folder in [('v006 Human static PASS',OUT/'renders/approved-static'),('v001',before),('v002 candidate',after)]],3,360,title='Approved identity / inherited rig / v002 Neutral')
    for view,name in [('front','01-seat-front.png'),('left','02-seat-side.png')]:
        cells=[(label+' / '+state,folder/(state+'-'+view+'.png')) for state in ['seat-entry','seat-quarter','seat-mid','seat-three-quarter','seat'] for label,folder in [('v001',before),('v002 candidate',after)]]
        r.board(name,cells,2,420,title='Seat transition / v001 > v002 / Human PENDING')
    cells=[];crops=OUT/'renders/face-crops';crops.mkdir(exist_ok=True)
    for state in ['half','closed','seat-rest','seat-joy','seat-lowhead','seat-shift-L','seat-shift-R']:
        box=(120,180,520,430) if state.startswith('seat') else (120,100,520,350)
        for label,folder in [('v001',before),('v002 candidate',after)]:
            cropped=crops/(folder.name+'-'+state+'.png');Image.open(folder/(state+'-front.png')).crop(box).save(cropped);cells.append((label+' / '+state,cropped))
    r.board('03-face-before-after.png',cells,2,500,title='Face / low head and shifted support / Human PENDING')
    states=['seat','seat-lowhead','seat-shift-L','seat-shift-R','extreme-face']
    r.board('04-five-view-composition.png',[(state+' / '+view,after/(state+'-'+view+'.png')) for state in states for view in ['front','3q-L','3q-R','left','right']],5,300,title='Composed poses / five fixed cameras / Human PENDING')
    states=['hold-L-touch-R','hold-conflict-L','hold-conflict-R','stroke-belly-start','stroke-belly-end','stroke-reverse','interrupt-return','neutral-return']
    r.board('05-composition-return.png',[(state,after/(state+'-3q-L.png')) for state in states],4,380,title='Independent hold / touch / stroke / return')
    if '--early' in sys.argv:return
    states=['proxy-both-acquire','proxy-both-seat','proxy-both-interrupt','proxy-both-resume','proxy-both-release','food-small','food-lick','food-drink','food-large']
    r.board('06-proxy-contact.png',[(state,fx/(state+'-3q-L.png')) for state in states],3,380,title='Diagnostic fixtures / product fit HOLD / Human PENDING')
    states=['neutral','seat','seat-rest','seat-joy','extreme-face','stroke-belly-end','neutral-return']
    r.board('07-blender-glb.png',[(label+' / '+state,folder/(state+'-front.png')) for state in states for label,folder in [('Editable Blender',after),('Reimported GLB',reimport)]],2,380,title='Saved GLB comparison / separate numeric correspondence')
    rows=[]
    for state in states:
        for view in ['front','3q-L','3q-R','left','right']:
            a=np.asarray(Image.open(after/(state+'-'+view+'.png')).convert('RGB')).astype(float);c=np.asarray(Image.open(reimport/(state+'-'+view+'.png')).convert('RGB')).astype(float)
            rows.append({'state':state,'view':view,'mean_abs_RGB_255':float(abs(a-c).mean()),'max_abs_RGB':float(abs(a-c).max()),'note':'Render-path/normal/light differences are visual evidence; numeric vertex and texture audits decide interchange integrity'})
    r.write('render-roundtrip-difference.json',rows)

def preservation():
    initial=json.loads((OUT/'protected-inputs.json').read_text(encoding='utf-8'));changes=[]
    for name,expected in initial.items():
        path=ROOT/name
        if not path.exists() or r.sha(path)!=expected:changes.append(name)
    allowed=['docs/production/Handoff.md','docs/production/shushu-v002-inspect.log']
    unexpected=[name for name in changes if name not in allowed]
    r.write('protected-input-verification.json',{'initial_count':len(initial),'changed':changes,'authorized_changes':allowed,'created_output_relocation':'This run created docs/production/shushu-v002-inspect.log during initial inspection; it was moved into production-rig-v002/inspect.log. It is not a pre-existing user input.','unexpected_changes':unexpected})
    assert not unexpected,'Protected input changed: '+repr(unexpected)

def manifest():
    files=sorted([*OUT.rglob('*'),*RIG.parent.glob('*production-rig-v002*')])
    r.write('delivery-manifest.json',{'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':r.sha(p)} for p in files if p.is_file() and p.name!='delivery-manifest.json'],'approval':'Human PENDING; product/mobile HOLD'})

def runtime_weights():
    j,raw=r.read(RIG);rows=[]
    for mesh in j['meshes']:
        for primitive in mesh['primitives']:
            attrs=primitive['attributes']
            if 'WEIGHTS_1' not in attrs:continue
            w=r.accessor(j,raw,attrs['WEIGHTS_1']);rows.append({'mesh':mesh['name'],'vertices_with_secondary_weights':int((w.sum(1)>0).sum()),'secondary_weight_sum_max':float(w.sum(1).max())})
    r.write('runtime-weight-limit.json',{'engine':'Installed PlayCanvas 2.22.2','primary_source':'node_modules/playcanvas/build/playcanvas.mjs gltfToEngineSemanticMap lines 93943–93959 maps JOINTS_0/WEIGHTS_0, no JOINTS_1/WEIGHTS_1','affected':rows,'gate':'Full stock PlayCanvas skin deformation HOLD; load/clip/morph/anchor test is separate. Preserve six-influence rig and its proven deformation; do not silently prune or change PWA.'})

def pc_reference():
    j,raw=r.read(RIG);animation=j['animations'][0];parents={child:index for index,node in enumerate(j['nodes']) for child in node.get('children',[])}
    samplers=[(r.accessor(j,raw,s['input']),r.accessor(j,raw,s['output'])) for s in animation['samplers']]
    chosen=[i for i,n in enumerate(j['nodes']) if n.get('name','').startswith('ANCHOR_') or n.get('name','').endswith((':Head',':LeftForeArm',':RightForeArm'))];states=[]
    for mark in json.loads((OUT/'proof-timeline.json').read_text(encoding='utf-8'))['markers']:
        # Blender's saved glTF timestamps retain frame 1 at 1/fps, rather than
        # rebasing the first sample to zero. Match the actual exported channels.
        time=mark['frame']/24;values={};morph={}
        for channel in animation['channels']:
            target=channel['target'];times,output=samplers[channel['sampler']];index=int(np.argmin(abs(times.ravel()-time)))
            assert abs(float(times.ravel()[index])-time)<2e-5,'Sample timestamp missing'
            if target['path']=='weights':
                count=len(j['meshes'][j['nodes'][target['node']]['mesh']]['primitives'][0]['targets']);weights=output.reshape(len(times),count)[index];morph[j['nodes'][target['node']]['name']]=weights.tolist()
            else:values[(target['node'],target['path'])]=output[index].ravel()
        cache={}
        def world(i):
            if i in cache:return cache[i]
            node=j['nodes'][i];t=values.get((i,'translation'),node.get('translation',[0,0,0]));s=values.get((i,'scale'),node.get('scale',[1,1,1]));q=np.array(values.get((i,'rotation'),node.get('rotation',[0,0,0,1])));q=q/np.linalg.norm(q);x,y,z,w=q
            local=np.eye(4);local[:3,:3]=np.array([[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]])@np.diag(s);local[:3,3]=t
            if 'matrix' in node:local=np.array(node['matrix']).reshape(4,4).T
            cache[i]=world(parents[i])@local if i in parents else local;return cache[i]
        states.append({'state':mark['name'],'time':time,'nodes':{j['nodes'][i]['name']:world(i).flatten(order='F').tolist() for i in chosen},'morphs':morph})
    r.write('runtime-reference.json',{'glb_sha256':r.sha(RIG),'method':'Direct glTF channel sampling at exact authored marker times, quaternion/TRS parent accumulation; column-major engine matrices','states':states})

if __name__=='__main__':
    if '--textures' in sys.argv:textures()
    elif '--boards' in sys.argv:boards()
    elif '--preserve' in sys.argv:preservation()
    elif '--runtime-weights' in sys.argv:runtime_weights()
    elif '--pc-reference' in sys.argv:pc_reference()
    else:preservation();manifest()
