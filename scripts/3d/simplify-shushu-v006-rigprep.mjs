/** Offline attribute-aware reduction. Original assets and embedded images stay untouched. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const source = 'assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb';
const outdir = 'docs/production/shushu/evidence/tripo-rigprep-v006-lowpoly';
const output = process.argv[2] || 'assets/grimo/production/shushu/tripo/geometry-v003/rigprep/shushu-v006-rigprep-lowpoly-v001.glb';
const bodyTarget = Number(process.argv[3] || 9000);
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const bytes = fs.readFileSync(path.join(root, source));
if (sha(bytes) !== '9c479122232170f65a0f5976cf2c07180cf342c08f37a95d50b53a90ff34f10f') throw Error('Source hash mismatch');
const jl = bytes.readUInt32LE(12), original = JSON.parse(bytes.subarray(20,20+jl));
const bin = bytes.subarray(28+jl), doc = structuredClone(original);
const { MeshoptSimplifier: sim } = await import(pathToFileURL(path.join(root, 'node_modules/.pnpm/meshoptimizer@1.2.0/node_modules/meshoptimizer/meshopt_simplifier.js')));
await sim.ready;
function read(id) {
  const a=original.accessors[id], v=original.bufferViews[a.bufferView];
  const n={SCALAR:1,VEC2:2,VEC3:3}[a.type], size={5126:4,5125:4,5123:2}[a.componentType];
  if(v.byteStride && v.byteStride!==n*size) throw Error('Unexpected stride');
  const b=bin.subarray((v.byteOffset||0)+(a.byteOffset||0),(v.byteOffset||0)+(a.byteOffset||0)+a.count*n*size);
  const buf=b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength);
  return a.componentType===5126 ? new Float32Array(buf) : a.componentType===5125 ? new Uint32Array(buf) : new Uint16Array(buf);
}
const chunks=[];let offset=0;
doc.bufferViews=[];doc.accessors=[];
function view(b,target) {
  const pad=(4-offset%4)%4;if(pad){chunks.push(Buffer.alloc(pad));offset+=pad;}
  const id=doc.bufferViews.length;doc.bufferViews.push({buffer:0,byteOffset:offset,byteLength:b.length,...(target?{target}:{})});chunks.push(b);offset+=b.length;return id;
}
function access(a, type, componentType, target) {
  const n={SCALAR:1,VEC2:2,VEC3:3}[type], count=a.length/n;
  const min=Array(n).fill(Infinity), max=Array(n).fill(-Infinity);
  for(let i=0;i<a.length;i++){min[i%n]=Math.min(min[i%n],a[i]);max[i%n]=Math.max(max[i%n],a[i]);}
  const id=doc.accessors.length;doc.accessors.push({bufferView:view(Buffer.from(a.buffer,a.byteOffset,a.byteLength),target),componentType,count,type,min,max});return id;
}
for(let i=0;i<doc.images.length;i++) {
  const v=original.bufferViews[original.images[i].bufferView];doc.images[i].bufferView=view(bin.subarray(v.byteOffset||0,(v.byteOffset||0)+v.byteLength));
}
const records=[];
for(let mi=0;mi<original.meshes.length;mi++) {
  const node=original.nodes.find(n=>n.mesh===mi), name=node.name;
  const pr=original.meshes[mi].primitives[0];
  if(original.meshes[mi].primitives.length!==1 || pr.targets) throw Error('Unexpected primitive/shape keys');
  const p=read(pr.attributes.POSITION), normal=read(pr.attributes.NORMAL), uv=read(pr.attributes.TEXCOORD_0), ids=new Uint32Array(read(pr.indices));
  let reduced=ids, error=0, locked=0, lock=null, target=ids.length/3, repairPasses=0;
  function degenerateFaces(indices){
    const found=[];
    for(let i=0;i<indices.length;i+=3){
      const v0=3*indices[i],v1=3*indices[i+1],v2=3*indices[i+2];
      const u=[0,1,2].map(k=>p[v1+k]-p[v0+k]),v=[0,1,2].map(k=>p[v2+k]-p[v0+k]);
      const area=.5*Math.hypot(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);
      if(area<=1e-14)found.push([indices[i],indices[i+1],indices[i+2]]);
    }
    return found;
  }
  if(name.endsWith('_Head') || name.endsWith('_Torso')) {
    lock=new Uint8Array(p.length/3);
    for(let i=0;i<lock.length;i++) {
      const x=p[3*i], y=p[3*i+1], z=p[3*i+2];
      // Entire front expression/cheeks plus ear-to-shoulder lower head rim.
      const face=name.endsWith('_Head') && ((z>.12 && y>.49 && y<.78 && Math.abs(x)<.235) || y<.495);
      // Thin joint cross-section samples: knee, ankle, hip, shoulder/neck.
      const joint=name.endsWith('_Torso') && [0.065,0.13,0.205,0.265,0.46,0.505].some(h=>Math.abs(y-h)<.00045);
      if(face||joint){lock[i]=1;locked++;}
    }
    target=name.endsWith('_Head')?35000:bodyTarget;
    const attrs=new Float32Array(lock.length*5);
    for(let i=0;i<lock.length;i++){attrs.set(normal.subarray(3*i,3*i+3),5*i);attrs.set(uv.subarray(2*i,2*i+2),5*i+3);}
    for(let pass=0;pass<5;pass++){
      [reduced,error]=sim.simplifyWithAttributes(ids,p,3,attrs,5,[.1,.1,.1,.2,.2],lock,target*3,.003,['LockBorder','RegularizeLight']);
      const bad=degenerateFaces(reduced);if(!bad.length)break;
      // Re-run from the original mesh, protecting a local source patch.
      // Removing a collinear face would leave a topological opening.
      if(pass===4)throw Error('Could not preserve a nondegenerate closed surface');
      repairPasses++;
      for(const face of bad)for(const center of face)for(let v=0;v<lock.length;v++){
        if(Math.hypot(p[3*v]-p[3*center],p[3*v+1]-p[3*center+1],p[3*v+2]-p[3*center+2])<.007)lock[v]=1;
      }
    }
    locked=lock.reduce((sum,v)=>sum+v,0);
  }
  if(degenerateFaces(reduced).length)throw Error('Degenerate source or result');
  const used=Array.from(new Set(reduced)), remap=new Uint32Array(p.length/3);
  used.forEach((v,i)=>remap[v]=i);
  const q=doc.meshes[mi].primitives[0];
  for(const [key,id] of Object.entries(pr.attributes)) {
    const old=read(id), a=original.accessors[id], n={VEC2:2,VEC3:3}[a.type], next=new Float32Array(used.length*n);
    used.forEach((v,i)=>next.set(old.subarray(v*n,v*n+n),i*n));q.attributes[key]=access(next,a.type,5126,34962);
  }
  const newids=used.length<65536?new Uint16Array(reduced.length):new Uint32Array(reduced.length);
  for(let i=0;i<reduced.length;i++)newids[i]=remap[reduced[i]];
  q.indices=access(newids,'SCALAR',used.length<65536?5123:5125,34963);
  const protectedFaces=[];
  if(lock)for(let i=0;i<ids.length;i+=3)if(lock[ids[i]]&&lock[ids[i+1]]&&lock[ids[i+2]])protectedFaces.push([ids[i],ids[i+1],ids[i+2]].join(','));
  const resultFaces=new Set();for(let i=0;i<reduced.length;i+=3)resultFaces.add([reduced[i],reduced[i+1],reduced[i+2]].join(','));
  const lost=protectedFaces.filter(f=>!resultFaces.has(f)).length;
  if(lost)throw Error(`Lost protected faces: ${name} ${lost}`);
  records.push({name,before:ids.length/3,after:reduced.length/3,vertices:used.length,locked_vertices:locked,protected_faces:protectedFaces.length,protected_faces_lost:lost,degenerate_repair_passes:repairPasses,attribute_error:error,target});
  console.log(JSON.stringify(records.at(-1)));
}
const pad=(4-offset%4)%4;chunks.push(Buffer.alloc(pad));offset+=pad;doc.buffers=[{byteLength:offset}];
let json=Buffer.from(JSON.stringify(doc));json=Buffer.concat([json,Buffer.alloc((4-json.length%4)%4,32)]);
const header=Buffer.alloc(20);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+json.length+offset,8);header.writeUInt32LE(json.length,12);header.writeUInt32LE(0x4e4f534a,16);
const bh=Buffer.alloc(8);bh.writeUInt32LE(offset,0);bh.writeUInt32LE(0x004e4942,4);
const result=Buffer.concat([header,json,bh,...chunks]);
fs.mkdirSync(path.dirname(path.join(root,output)),{recursive:true});fs.writeFileSync(path.join(root,output),result);
fs.mkdirSync(path.join(root,outdir),{recursive:true});
fs.writeFileSync(path.join(root,outdir,'reduction.json'),JSON.stringify({source,source_sha256:sha(bytes),output,output_sha256:sha(result),meshoptimizer:'1.2.0',method:'simplifyWithAttributes; source vertices retained exactly; no texture transfer',flags:['LockBorder','RegularizeLight'],weights:[.1,.1,.1,.2,.2],target_error:.003,records,total_before:records.reduce((a,r)=>a+r.before,0),total_after:records.reduce((a,r)=>a+r.after,0)},null,2)+'\n');
