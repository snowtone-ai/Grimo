"""Byte-preserving intake. Run with ordinary Python; no Tripo operations."""
from pathlib import Path
import hashlib, json, struct, shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/production/shushu/evidence/candidate-b-8481'
SOURCE = ROOT / 'assets/grimo/production/shushu/tripo/candidate-b-8481'
FILES = ['cute panda 3d model 8481.fbx', 'cute panda 3d model 8481.glb',
         'shushu_mesh_audit_data.json', 'shushu_topology_zones.json',
         'shushu_clay_5view_comparison.png', 'shushu_quad_topology_visual.png']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def glb_read(p):
    data=p.read_bytes()
    magic,version,length=struct.unpack_from('<4sII',data)
    assert magic==b'glTF' and version==2 and length==len(data)
    offset=12; chunks=[]; doc=None; binary=None
    while offset<len(data):
        n,t=struct.unpack_from('<II',data,offset); offset+=8
        payload=data[offset:offset+n]; assert len(payload)==n
        chunks.append({'type':t,'bytes':n}); offset+=n
        if t==0x4e4f534a: doc=json.loads(payload)
        if t==0x004e4942: binary=payload
    assert offset==len(data) and doc is not None
    return doc,binary,chunks

def main():
    OUT.mkdir(parents=True,exist_ok=True); SOURCE.mkdir(parents=True,exist_ok=True)
    rows=[]
    for name in FILES:
        target=(SOURCE if name.endswith(('.fbx','.glb')) else OUT/'historical')/name
        original=ROOT/name
        p=original if original.exists() else target
        assert p.exists(),name
        row={'original_path':name,'path':target.relative_to(ROOT).as_posix(),
             'bytes':p.stat().st_size,'sha256':sha(p),
             'role':'Original Tripo source' if name.endswith(('.fbx','.glb')) else 'Historical supplied diagnostics; secondary evidence'}
        if p.suffix=='.fbx':
            header=p.read_bytes()[:27]
            assert header[:23]==b'Kaydara FBX Binary  \x00\x1a\x00'
            row['fbx_version']=struct.unpack_from('<I',header,23)[0]
        elif p.suffix=='.glb':
            doc,_,chunks=glb_read(p)
            row['glb']={'asset':doc['asset'],'chunks':chunks,'nodes':doc.get('nodes',[]),
                        'meshes':doc.get('meshes',[]),'materials':doc.get('materials',[]),
                        'images':doc.get('images',[]),'skins':len(doc.get('skins',[])),
                        'animations':len(doc.get('animations',[])),'extensionsUsed':doc.get('extensionsUsed',[])}
        elif p.suffix=='.json':
            doc=json.loads(p.read_text(encoding='utf-8'))
            row['json']={'root_type':type(doc).__name__,'keys':list(doc),'formal_schema_present':'$schema' in doc,
                         'note':'multi-candidate content; only B independently validated'}
        else:
            with Image.open(p) as im:
                row['image']={'format':im.format,'size':list(im.size),'mode':im.mode}; im.verify()
        target.parent.mkdir(parents=True,exist_ok=True)
        if p!=target:
            assert not target.exists(),target
            shutil.move(str(p),str(target))
        assert sha(target)==row['sha256']
        rows.append(row)
    refs=[]
    for p in sorted((ROOT/'assets/grimo/source/shushu').rglob('*.png')):
        with Image.open(p) as im: size=list(im.size); im.verify()
        refs.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p),'size':size})
    audit=json.loads((OUT/'historical/shushu_mesh_audit_data.json').read_text())['B 8481']
    assert audit['sha256']['fbx']==rows[0]['sha256'] and audit['sha256']['glb']==rows[1]['sha256']
    manifest={'input_head':'65dcab996f0963ae2054d8474f07cf0fafaca608','files':rows,'references':refs,
              'historical_B_hash_match':True,'tripo_trials':{'remaining':1,'untouched':True}}
    (OUT/'input-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'files':[{k:r[k] for k in ['path','bytes','sha256']} for r in rows],'hash_match':True},indent=2))

if __name__=='__main__': main()
