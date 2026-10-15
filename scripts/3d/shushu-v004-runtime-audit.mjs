// Narrow v004 diagnostic: no source asset writes. node ... [--serve]
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const out=path.join(root,'docs/production/shushu/evidence/production-rig-v004-runtime');
const source='assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.glb';
const candidate='docs/production/shushu/evidence/production-rig-v004-runtime/shushu-v004-runtime-4w-probe.glb';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const bytes=fs.readFileSync(path.join(root,source)),length=bytes.readUInt32LE(12);
const doc=JSON.parse(bytes.subarray(20,20+length)),bin=bytes.subarray(length+28);
const dims={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16};
const sizes={5121:1,5123:2,5125:4,5126:4};
function read(id){const a=doc.accessors[id],v=doc.bufferViews[a.bufferView],d=dims[a.type],s=sizes[a.componentType],o=(v.byteOffset||0)+(a.byteOffset||0),r=[];for(let i=0;i<a.count;i++)for(let c=0;c<d;c++)r.push(bin[a.componentType===5126?'readFloatLE':a.componentType===5123?'readUInt16LE':a.componentType===5125?'readUInt32LE':'readUInt8'](o+i*(v.byteStride||d*s)+c*s));return r;}
fs.mkdirSync(out,{recursive:true});
const write=(n,v)=>fs.writeFileSync(path.join(out,n),JSON.stringify(v,null,2)+'\n');
const groups={base:new Set(),morph:new Set(),animation:new Set(),skin:new Set()};
let triangles=0;const weights=[];
const next=structuredClone(doc),nextBin=Buffer.from(bin);
for(const [mi,m]of doc.meshes.entries())for(const [pi,p]of m.primitives.entries()){
 Object.values(p.attributes).forEach(i=>groups.base.add(i));groups.base.add(p.indices);triangles+=doc.accessors[p.indices].count/3;
 for(const t of p.targets||[])Object.values(t).forEach(i=>groups.morph.add(i));
 if(p.attributes.WEIGHTS_1===undefined)continue;
 const primary=read(p.attributes.WEIGHTS_0),secondary=read(p.attributes.WEIGHTS_1);
 const a=doc.accessors[p.attributes.WEIGHTS_0],v=doc.bufferViews[a.bufferView];
 if(a.componentType!==5126||v.byteStride)throw Error('Unsupported weight layout');
 let affected=0,max=0,sum=0;for(let i=0;i<a.count;i++){
  const dropped=secondary.slice(i*4,i*4+4).reduce((a,b)=>a+b,0),total=primary.slice(i*4,i*4+4).reduce((a,b)=>a+b,0);
  if(dropped>0)affected++;max=Math.max(max,dropped);sum+=dropped;
  // Assert exporter already sorted the primary four. No speculative pruning.
  if(Math.min(...primary.slice(i*4,i*4+4))<Math.max(...secondary.slice(i*4,i*4+4))-1e-7)throw Error('Primary weights are not top four');
  for(let k=0;k<4;k++)nextBin.writeFloatLE(primary[i*4+k]/total,(v.byteOffset||0)+(a.byteOffset||0)+(i*4+k)*4);
 }
 weights.push({mesh:m.name,vertices:a.count,affected,secondaryMax:max,secondaryMean:sum/a.count});
 delete next.meshes[mi].primitives[pi].attributes.JOINTS_1;delete next.meshes[mi].primitives[pi].attributes.WEIGHTS_1;
}
for(const a of doc.animations)for(const s of a.samplers){groups.animation.add(s.input);groups.animation.add(s.output);}
for(const s of doc.skins)groups.skin.add(s.inverseBindMatrices);
const costs={};for(const [name,set]of Object.entries(groups)){const views=new Set();for(const id of set){const a=doc.accessors[id];if(a.bufferView!==undefined)views.add(a.bufferView);if(a.sparse){views.add(a.sparse.indices.bufferView);views.add(a.sparse.values.bufferView);}}costs[name]=[...views].reduce((s,i)=>s+doc.bufferViews[i].byteLength,0);}
costs.texture=doc.images.reduce((s,i)=>s+doc.bufferViews[i.bufferView].byteLength,0);
// Keep all untouched bytes/accessors, even unused secondary data: lossless layout isolation.
const json=Buffer.from(JSON.stringify(next));const padded=Buffer.alloc(Math.ceil(json.length/4)*4,32);json.copy(padded);
const packed=Buffer.alloc(28+padded.length+nextBin.length);packed.writeUInt32LE(0x46546c67,0);packed.writeUInt32LE(2,4);packed.writeUInt32LE(packed.length,8);packed.writeUInt32LE(padded.length,12);packed.writeUInt32LE(0x4e4f534a,16);padded.copy(packed,20);packed.writeUInt32LE(nextBin.length,20+padded.length);packed.writeUInt32LE(0x004e4942,24+padded.length);nextBin.copy(packed,28+padded.length);
fs.writeFileSync(path.join(root,candidate),packed);
write('asset-costs.json',{source,candidate,sourceSha256:hash(bytes),candidateSha256:hash(packed),bytes:bytes.length,candidateBytes:packed.length,triangles,meshes:doc.meshes.length,joints:doc.skins.map(s=>s.joints.length),textures:doc.images.length,costs,weights,morphTargets:doc.meshes.map(m=>({mesh:m.name,count:m.primitives[0].targets?.length||0})),note:'Costs are unique bufferView bytes within each category; sparse views included. Candidate preserves unused secondary buffers to isolate normalization. Not a size optimization.'});
// Full start-state protection, including pre-existing untracked user inputs; omit own outputs.
if(!fs.existsSync(path.join(out,'protected-inputs.json'))){
 const {execFileSync}=await import('node:child_process');
 const tracked=execFileSync('git',['ls-files','-z'],{cwd:root,maxBuffer:20e6}).toString().split('\0').filter(Boolean);
 const untracked=execFileSync('git',['ls-files','--others','--exclude-standard','-z'],{cwd:root,maxBuffer:20e6}).toString().split('\0').filter(Boolean);
 const rows=[];for(const p of [...tracked,...untracked]){if(p.includes('production-rig-v004-runtime')||p===candidate||p.includes('shushu-v004-runtime'))continue;const f=path.join(root,p);if(fs.statSync(f).isFile())rows.push({path:p,sha256:hash(fs.readFileSync(f))});}write('protected-inputs.json',rows);
}
if(process.argv.includes('--serve')){
 const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.glb':'model/gltf-binary'};
 http.createServer((req,res)=>{const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);const permitted=pathname==='/'+source||pathname==='/'+candidate||pathname.startsWith('/node_modules/playcanvas/build/')||pathname.startsWith('/docs/production/shushu/evidence/production-rig-v004-runtime/');const p=path.resolve(root,'.'+pathname);if(!permitted||!p.startsWith(root+path.sep)||!fs.existsSync(p)||!fs.statSync(p).isFile()){res.writeHead(404);res.end();return;}res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);}).listen(8766,'127.0.0.1',()=>console.log('http://127.0.0.1:8766/docs/production/shushu/evidence/production-rig-v004-runtime/runtime.html'));
}
