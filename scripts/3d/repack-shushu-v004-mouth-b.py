"""Restore source compressed images/materials while preserving exported numeric accessors."""
import sys,json,struct,hashlib,copy,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'
BASE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
SOURCE=BASE/'shushu-v006-production-rig-v004.glb'
TARGET=BASE/'shushu-v004-mouth-b-v001.glb'
s=importlib.util.spec_from_file_location('report',ROOT/'scripts/3d/report-shushu-production-rig-v001.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
sha=lambda b:hashlib.sha256(b).hexdigest()
def image_bytes(j,raw,im):
    v=j['bufferViews'][im['bufferView']];return raw[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
def main():
    src,sraw=p.read(SOURCE);j,raw=p.read(TARGET)
    before=[sha(p.accessor(j,raw,i).tobytes()) for i in range(len(j['accessors']))]
    blob=bytearray();views=[];remap={};image_views={im['bufferView'] for im in j['images']}
    def add(payload,template):
        while len(blob)%4:blob.append(0)
        v=copy.deepcopy(template);v.update(buffer=0,byteOffset=len(blob),byteLength=len(payload));views.append(v);blob.extend(payload);return len(views)-1
    for i,v in enumerate(j['bufferViews']):
        if i not in image_views:remap[i]=add(raw[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']],v)
    def refs(obj):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k=='bufferView':obj[k]=remap[v]
                else:refs(v)
        elif isinstance(obj,list):
            for item in obj:refs(item)
    refs(j['accessors'])
    srcnodes={n['name']:n for n in src['nodes'] if 'mesh' in n}
    head=src['meshes'][srcnodes['ShushuStatic_Head']['mesh']]['primitives'][0]
    headtexture=src['materials'][head['material']]['pbrMetallicRoughness']['baseColorTexture']['index']
    headimage=src['textures'][headtexture]['source'];rows=[]
    j['images']=copy.deepcopy(src['images'])
    for i,im in enumerate(j['images']):
        old=image_bytes(src,sraw,src['images'][i]);data=(OUT/'Head-mouth-b-local.png').read_bytes() if i==headimage else old
        im['bufferView']=add(data,{'buffer':0})
        if i==headimage:im['mimeType']='image/png'
        rows.append({'image':i,'name':im.get('name'),'source_sha256':sha(old),'output_sha256':sha(data),'unchanged':old==data,'local_head':i==headimage})
    j['textures']=copy.deepcopy(src['textures']);j['samplers']=copy.deepcopy(src.get('samplers',[]))
    oral={'ShushuStatic_MouthInterior','ShushuStatic_OralBowl','ShushuStatic_Tongue'}
    for n in j['nodes']:
        if 'mesh' not in n or n['name'] in oral:continue
        sp=src['meshes'][srcnodes[n['name']]['mesh']]['primitives'];dp=j['meshes'][n['mesh']]['primitives'];assert len(sp)==len(dp)
        for a,b in zip(sp,dp):j['materials'][b['material']]=copy.deepcopy(src['materials'][a['material']])
    j['bufferViews']=views;j['buffers']=[{'byteLength':len(blob)}]
    after=[sha(p.accessor(j,blob,i).tobytes()) for i in range(len(j['accessors']))];assert before==after
    data=json.dumps(j,separators=(',',':'),ensure_ascii=False).encode();data+=b' '*((-len(data))%4);blob+=b'\0'*((-len(blob))%4)
    TARGET.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(data)+len(blob))+struct.pack('<I4s',len(data),b'JSON')+data+struct.pack('<I4s',len(blob),b'BIN\0')+blob)
    result={'images':rows,'numeric_accessors':len(before),'numeric_accessor_bytes_unchanged':before==after,'source_materials_restored_except':sorted(oral),'candidate_sha256':sha(TARGET.read_bytes()),'candidate_bytes':TARGET.stat().st_size}
    (OUT/'texture-material-restoration.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps({k:v for k,v in result.items() if k!='images'},indent=2))
if __name__=='__main__':main()
