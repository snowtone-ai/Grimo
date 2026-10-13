// Composite the ImageGen local repair into selected existing Head texels only.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const sharp = require(process.env.SHUSHU_SHARP_MODULE || 'sharp');
const root = path.resolve(__dirname, '../..');
const out = path.join(root, 'docs/production/shushu/evidence/tripo-texture-v003');
const candidate = path.join(root, 'assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v001.glb');
const hash = x => crypto.createHash('sha256').update(x).digest('hex');
function readGlb(file) {
  const raw = fs.readFileSync(file), size = raw.readUInt32LE(12);
  return { raw, json: JSON.parse(raw.subarray(20, 20 + size)), bin: raw.subarray(28 + size) };
}
function imageBytes(g, index) {
  const v = g.json.bufferViews[g.json.images[index].bufferView];
  return g.bin.subarray(v.byteOffset || 0, (v.byteOffset || 0) + v.byteLength);
}
function segmentDistance(x, y, p, q) {
  const dx = q[0]-p[0], dy = q[1]-p[1];
  const t = Math.max(0, Math.min(1, ((x-p[0])*dx+(y-p[1])*dy)/(dx*dx+dy*dy)));
  return Math.hypot(x-p[0]-t*dx, y-p[1]-t*dy);
}
function sample(buf, x, y) {
  x = Math.max(0, Math.min(1022.999, x-.5)); y = Math.max(0, Math.min(1022.999, y-.5));
  const ix = Math.floor(x), iy = Math.floor(y), a = x-ix, b = y-iy;
  return [0,1,2].map(c => (1-b)*((1-a)*buf[(iy*1024+ix)*3+c]+a*buf[(iy*1024+ix+1)*3+c]) + b*((1-a)*buf[((iy+1)*1024+ix)*3+c]+a*buf[((iy+1)*1024+ix+1)*3+c]));
}
function inside(x,y,poly) {
  let hit=false;
  for(let k=0;k<poly.length;k++) {
    const p=poly[k],q=poly[(k+1)%poly.length];
    if((p[1]>y)!==(q[1]>y) && x<(q[0]-p[0])*(y-p[1])/(q[1]-p[1])+p[0])hit=!hit;
  }
  return hit;
}
async function main() {
  const source = readGlb(path.join(root, 'shushu-geometry-v003-tripo.glb.glb'));
  if (hash(source.raw) !== '338ad5f8c67906917579ddbb804a4f7f51d8fec6c42328bb545adc87c1bf077b') throw Error('Source changed');
  const edit = process.argv[2]; if (!edit) throw Error('Provide local ImageGen edit path');
  const dir = path.join(out, 'textures'); fs.mkdirSync(dir, {recursive:true});
  fs.copyFileSync(edit, path.join(dir, 'imagegen-local-repair-projection.png'));
  const metadata = await sharp(edit).metadata();
  const generated = await sharp(edit).resize(1024,1024).removeAlpha().raw().toBuffer();
  const original = await sharp(imageBytes(source,4)).removeAlpha().raw().toBuffer();
  const result = Buffer.from(original), mask = Buffer.alloc(2048*2048);
  const masks=JSON.parse(fs.readFileSync(path.join(out,'projection-masks.json')));
  const polygons=[masks['mouth-screen-left'],masks['mouth-screen-right']];
  // Eye trial was visually inconclusive. Final review candidate repairs only
  // confirmed mouth ghosts and preserves all eye-surround Head texels.
  const coreMap = JSON.parse(fs.readFileSync(path.join(out,'projection-map.json'))).filter(p=>polygons.some(poly=>inside(p[2],p[3],poly)));
  const expanded = new Map(coreMap.map(p=>[p[1]*2048+p[0],p]));
  // Include two atlas texels around mapped UV edges so bilinear sampling cannot
  // reintroduce the old JPEG color from island padding. Core samples take priority.
  for(const [x,y,sx,sy] of coreMap)for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++) {
    const xx=x+dx,yy=y+dy,key=yy*2048+xx;
    if(xx>=0&&xx<2048&&yy>=0&&yy<2048&&!expanded.has(key))expanded.set(key,[xx,yy,sx,sy]);
  }
  const map=[...expanded.values()];
  fs.writeFileSync(path.join(out,'applied-projection-map.json'),JSON.stringify(map)+'\n');
  const beforeRender=await sharp(path.join(out,'renders/before-front.png')).removeAlpha().raw().toBuffer();
  const probes=[[430,570],[594,570],[395,720],[629,720]];
  const biases=probes.map(([x,y])=>sample(generated,x,y).map((v,c)=>v-sample(beforeRender,x,y)[c]));
  let changed = 0, rejectedTarget = 0;
  for (const [x,y,sx,sy] of map) {
    const i = (y*2048+x)*3;
    const bias=biases[(sy<630?0:2)+(sx>512?1:0)];
    const color = sample(generated,sx,sy).map((v,c)=>Math.max(0,Math.min(255,v-bias[c]))), targetLuma=.2126*color[0]+.7152*color[1]+.0722*color[2];
    // Sample only repaired cream, so the central smile/tongue cannot be copied
    // into a second position when the generated preview has small alignment drift.
    if (targetLuma < 210) { rejectedTarget++; continue; }
    const nearby = polygons.filter(p => sx >= Math.min(...p.map(v=>v[0])) && sx <= Math.max(...p.map(v=>v[0])) && sy >= Math.min(...p.map(v=>v[1])) && sy <= Math.max(...p.map(v=>v[1])));
    const distance = Math.min(...nearby.flatMap(p => p.map((v,k)=>segmentDistance(sx,sy,v,p[(k+1)%p.length]))));
    const t = Math.min(1,distance/1), weight=t*t*(3-2*t);
    for (let c=0;c<3;c++) result[i+c]=Math.round(original[i+c]*(1-weight)+color[c]*weight);
    if (!result.subarray(i,i+3).equals(original.subarray(i,i+3))) {mask[y*2048+x]=255;changed++;}
  }
  const png = await sharp(result,{raw:{width:2048,height:2048,channels:3}}).png().toBuffer();
  fs.writeFileSync(path.join(dir,'head-before.jpg'),imageBytes(source,4));
  fs.writeFileSync(path.join(dir,'head-candidate.png'),png);
  await sharp(mask,{raw:{width:2048,height:2048,channels:1}}).png().toFile(path.join(dir,'changed-texels.png'));
  // Append replacement image. All original binary data stays byte-identical.
  const j=structuredClone(source.json), offset=source.bin.length;
  j.images[4]={...j.images[4],bufferView:j.bufferViews.length,mimeType:'image/png'};
  j.bufferViews.push({buffer:0,byteOffset:offset,byteLength:png.length});
  j.buffers[0].byteLength=offset+png.length;
  let json=Buffer.from(JSON.stringify(j));json=Buffer.concat([json,Buffer.alloc((4-json.length%4)%4,32)]);
  const bin=Buffer.concat([source.bin,png,Buffer.alloc((4-png.length%4)%4)]);
  const header=Buffer.alloc(12),jh=Buffer.alloc(8),bh=Buffer.alloc(8);
  header.write('glTF');header.writeUInt32LE(2,4);header.writeUInt32LE(28+json.length+bin.length,8);
  jh.writeUInt32LE(json.length);jh.write('JSON',4);bh.writeUInt32LE(bin.length);bh.write('BIN\0',4);
  fs.mkdirSync(path.dirname(candidate),{recursive:true});fs.writeFileSync(candidate,Buffer.concat([header,jh,json,bh,bin]));
  const reread=readGlb(candidate);
  const subtrees=['meshes','accessors','nodes','materials','textures','samplers','skins','animations','scenes','scene','extensions','extensionsUsed','extensionsRequired'];
  const unchanged=Object.fromEntries(subtrees.map(k=>[k,JSON.stringify(j[k])===JSON.stringify(source.json[k])]));
  if (!Object.values(unchanged).every(Boolean) || !reread.bin.subarray(0,source.bin.length).equals(source.bin)) throw Error('Unexpected non-image change');
  const otherImages=source.json.images.map((_,i)=>i).filter(i=>i!==4).map(i=>({index:i,sha256:hash(imageBytes(source,i)),identical:imageBytes(source,i).equals(imageBytes(reread,i))}));
  const allowed=new Set(map.map(([x,y])=>y*2048+x));let outside=0;
  for(let p=0;p<2048*2048;p++) if(!allowed.has(p)&&!original.subarray(p*3,p*3+3).equals(result.subarray(p*3,p*3+3)))outside++;
  if(outside || !otherImages.every(i=>i.identical))throw Error('Unexpected texture change');
  const report={source_sha256:hash(source.raw),candidate:path.relative(root,candidate).replaceAll('\\','/'),candidate_sha256:hash(fs.readFileSync(candidate)),human_gate:'PENDING',scope:'Confirmed mouth ghosts only; eye edit rejected and reverted',appearance_completion:'WITHHELD; eye contour unresolved',imagegen:{tool:'built-in image_gen',original_size:[metadata.width,metadata.height],projection_size:[1024,1024],preview_is_not_model_evidence:true},core_projection_texels:coreMap.length,atlas_padding_texels:2,color_match_probes:probes,color_match_biases:biases,selected_head_texels:map.length,changed_head_texels:changed,head_total_texels:2048*2048,changed_outside_projection_mask:outside,rejected_noncream_targets:rejectedTarget,unchanged_json_subtrees:unchanged,original_binary_prefix_identical:true,other_images:otherImages,head_encoding:'JPEG decoded to lossless PNG; decoded pixels outside selected texels exactly preserved'};
  fs.writeFileSync(path.join(out,'candidate-validation.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
