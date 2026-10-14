const fs=require('fs'); const crypto=require('crypto'); const path=require('path');
const input=process.argv[2],output=process.argv[3],depth=Number(process.argv[4]);
if(!input||!output||!Number.isFinite(depth)||depth<0||depth>.02)throw Error('usage: input.glb output.glb depth_m (0..0.02)');
const raw=fs.readFileSync(input),len=raw.readUInt32LE(12);if(raw.toString('ascii',0,4)!=='glTF'||raw.readUInt32LE(8)!==raw.length)throw Error('Invalid GLB');
const j=JSON.parse(raw.subarray(20,20+len)),bin=raw.subarray(28+len);
const names=['ShushuStatic_Eye_L','ShushuStatic_Eye_R'];const indices=[];
for(const name of names){const i=j.nodes.findIndex(n=>n.name===name);if(i<0||j.nodes[i].translation)throw Error('Unexpected eye node '+name);indices.push(i);j.nodes[i].translation=[0,0,-depth]}
let json=Buffer.from(JSON.stringify(j));json=Buffer.concat([json,Buffer.alloc((4-json.length%4)%4,32)]);
const header=Buffer.alloc(12),jh=Buffer.alloc(8),bh=Buffer.alloc(8);header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+json.length+bin.length,8);jh.writeUInt32LE(json.length);jh.write('JSON',4);bh.writeUInt32LE(bin.length);bh.write('BIN\0',4);
const final=Buffer.concat([header,jh,json,bh,bin]);fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,final);
const sourceJ=JSON.parse(raw.subarray(20,20+len)),diff=[];for(let i=0;i<j.nodes.length;i++)if(JSON.stringify(j.nodes[i])!==JSON.stringify(sourceJ.nodes[i]))diff.push(i);
if(JSON.stringify(diff)!==JSON.stringify(indices.sort((a,b)=>a-b))||!final.subarray(28+json.length).equals(bin))throw Error('Unexpected change');
console.log(JSON.stringify({source_sha256:crypto.createHash('sha256').update(raw).digest('hex'),candidate_sha256:crypto.createHash('sha256').update(final).digest('hex'),eyes:names,glTF_node_translation_z:-depth,other_nodes_identical:true,binary_identical:true}));
