// Composite the ImageGen local repair into selected existing Head texels only.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const zlib = require('zlib');
const sharp = require(process.env.SHUSHU_SHARP_MODULE || 'sharp');
const root = path.resolve(__dirname, '../..');
const config = process.argv[3] ? JSON.parse(fs.readFileSync(process.argv[3], 'utf8')) : null;
const out = path.join(root, config?.evidence || 'docs/production/shushu/evidence/tripo-texture-v003');
const candidate = path.join(root, config?.candidate || 'assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v001.glb');
const hash = x => crypto.createHash('sha256').update(x).digest('hex');
function projectionMap(view) {
  const name=path.join(out,`projection-map-${view}.json`);
  return JSON.parse(fs.existsSync(name)?fs.readFileSync(name,'utf8'):zlib.gunzipSync(fs.readFileSync(`${name}.gz`)).toString('utf8'));
}
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
function seamBridge(buf,x,y,points,radius,fade) {
  if(y<points[0][1]||y>points.at(-1)[1])return sample(buf,x,y);
  let k=0;while(k+1<points.length-1&&y>points[k+1][1])k++;
  const [ax,ay]=points[k],[bx,by]=points[k+1];
  const center=ax+(bx-ax)*(y-ay)/(by-ay);
  if(Math.abs(x-center)>=radius)return sample(buf,x,y);
  const left=sample(buf,center-radius,y),right=sample(buf,center+radius,y);
  const t=(x-center+radius)/(2*radius);
  const bridge=left.map((v,c)=>v*(1-t)+right[c]*t);
  const smooth=t=>{t=Math.max(0,Math.min(1,t));return t*t*(3-2*t)};
  const weight=smooth((y-fade[0])/(fade[1]-fade[0]))*smooth((fade[3]-y)/(fade[3]-fade[2]));
  const native=sample(buf,x,y);
  return native.map((v,c)=>v*(1-weight)+bridge[c]*weight);
}
function seamGeneratedCorrection(before,generated,x,y,points,radius,fade) {
  if(y<points[0][1]||y>points.at(-1)[1])return sample(before,x,y);
  let k=0;while(k+1<points.length-1&&y>points[k+1][1])k++;
  const [ax,ay]=points[k],[bx,by]=points[k+1];
  const center=ax+(bx-ax)*(y-ay)/(by-ay),distance=Math.abs(x-center);
  if(distance>=radius)return sample(before,x,y);
  const t=(x-center+radius)/(2*radius),smooth=z=>{z=Math.max(0,Math.min(1,z));return z*z*(3-2*z)};
  const left=sample(generated,center-radius,y).map((v,c)=>v-sample(before,center-radius,y)[c]);
  const right=sample(generated,center+radius,y).map((v,c)=>v-sample(before,center+radius,y)[c]);
  const native=sample(before,x,y),made=sample(generated,x,y);
  const edge=smooth(Math.min(x-center+radius,center+radius-x)/18);
  const vertical=smooth((y-fade[0])/(fade[1]-fade[0]))*smooth((fade[3]-y)/(fade[3]-fade[2]));
  return native.map((v,c)=>v+(made[c]-v-left[c]*(1-t)-right[c]*t)*edge*vertical);
}
async function furComposite(original, edit) {
  const generatedBoard=await sharp(edit).resize(2048,2048).removeAlpha().raw().toBuffer();
  const panels={}, before={}, biases={};
  const panelPositions={'left-side':[0,0],'right-side':[1024,0],top:[0,1024]};
  for(const view of config.fur_views || Object.keys(panelPositions)) {
    const xy=panelPositions[view];if(!xy)throw Error('Unsupported fur view '+view);
    panels[view]=await sharp(generatedBoard,{raw:{width:2048,height:2048,channels:3}}).extract({left:xy[0],top:xy[1],width:1024,height:1024}).raw().toBuffer();
    before[view]=await sharp(path.join(out,`renders/before-${view}.png`)).removeAlpha().raw().toBuffer();
    biases[view]=[0,1,2].map(c=>config.color_match_probes[view].reduce((sum,[x,y])=>sum+sample(panels[view],x,y)[c]-sample(before[view],x,y)[c],0)/config.color_match_probes[view].length);
  }
  const protectedMask=Buffer.alloc(2048*2048);
  for(const folder of ['tripo-texture-v003','tripo-eye-outline-v002']) {
    const m=await sharp(path.join(root,'docs/production/shushu/evidence',folder,'textures/changed-texels.png')).greyscale().raw().toBuffer();
    for(let i=0;i<m.length;i++)if(m[i])protectedMask[i]=255;
  }
  const selected=new Map();
  for(const view of Object.keys(panels)) {
    const polys=Object.entries(config.masks).filter(([k])=>k.startsWith(view)).map(([,p])=>p);
    const core=projectionMap(view);
    for(const [x,y,sx,sy] of core) {
      const active=polys.filter(p=>inside(sx,sy,p));if(!active.length)continue;
      const distance=Math.max(...active.map(p=>Math.min(...p.map((v,k)=>segmentDistance(sx,sy,v,p[(k+1)%p.length])))));
      const t=Math.min(1,distance/config.feather_screen_pixels),weight=t*t*(3-2*t);
      for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++) {
        const xx=x+dx,yy=y+dy,key=yy*2048+xx;
        if(xx<0||xx>=2048||yy<0||yy>=2048||protectedMask[key])continue;
        const old=selected.get(key);if(!old||weight>old[5])selected.set(key,[xx,yy,sx,sy,view,weight]);
      }
    }
  }
  const result=Buffer.from(original),mask=Buffer.alloc(2048*2048);let changed=0,rejectedTarget=0;
  const map=[...selected.values()];
  for(const [x,y,sx,sy,view,weight] of map) {
    const source=sample(before[view],sx,sy);
    const trace=config.seam_rebuild_centerlines?.[view];
    const mode=config.seam_material_modes?.[view] || config.seam_material_mode;
    const material=trace?(mode==='imagegen'?seamGeneratedCorrection(before[view],panels[view],sx,sy,trace,config.seam_rebuild_radius,config.seam_rebuild_vertical_fade):seamBridge(before[view],sx,sy,trace,config.seam_rebuild_radius,config.seam_rebuild_vertical_fade)):sample(panels[view],sx,sy);
    // A render includes lighting. Transfer only the local repair difference to
    // the atlas, otherwise the same lighting is baked into the texture twice.
    const i=(y*2048+x)*3;
    const color=material.map((v,c)=>Math.max(0,Math.min(255,trace?(mode==='bridge-absolute'?v:original[i+c]+v-source[c]):v-biases[view][c])));
    // Do not copy actual pink ears, dark features, or shifted model background.
    if(source[0]<180||source[1]<(view==='top'?145:170)||color[0]<220||color[1]<195) {rejectedTarget++;continue;}
    for(let c=0;c<3;c++)result[i+c]=Math.round(original[i+c]*(1-weight)+color[c]*weight);
    if(!result.subarray(i,i+3).equals(original.subarray(i,i+3))){mask[y*2048+x]=255;changed++;}
  }
  fs.writeFileSync(path.join(out,'applied-projection-map.json.gz'),zlib.gzipSync(JSON.stringify(map)+'\n',{level:6}));
  return {result,mask,map,changed,rejectedTarget,coreMap:map,probes:config.color_match_probes,biases};
}
async function main() {
  const source = readGlb(path.join(root, config?.base || 'shushu-geometry-v003-tripo.glb.glb'));
  if (hash(source.raw) !== (config?.base_sha256 || '338ad5f8c67906917579ddbb804a4f7f51d8fec6c42328bb545adc87c1bf077b')) throw Error('Source changed');
  const edit = process.argv[2]; if (!edit) throw Error('Provide local ImageGen edit path');
  const dir = path.join(out, 'textures'); fs.mkdirSync(dir, {recursive:true});
  fs.copyFileSync(edit, path.join(dir, 'imagegen-local-repair-projection.png'));
  const metadata = await sharp(edit).metadata();
  const generated = await sharp(edit).resize(1024,1024).removeAlpha().raw().toBuffer();
  const original = await sharp(imageBytes(source,4)).removeAlpha().raw().toBuffer();
  let result,mask,map,coreMap,probes,biases,changed,rejectedTarget;
  if(config?.mode==='fur-seam') ({result,mask,map,coreMap,probes,biases,changed,rejectedTarget}=await furComposite(original,edit));
  else {
  result = Buffer.from(original); mask = Buffer.alloc(2048*2048);
  const masks=JSON.parse(fs.readFileSync(path.join(out,'projection-masks.json')));
  const polygons=config ? Object.values(masks) : [masks['mouth-screen-left'],masks['mouth-screen-right']];
  // Default preserves the historical mouth-only candidate; configured eye mode
  // selects only the independently traced duplicate bands on the v001 base.
  coreMap = JSON.parse(fs.readFileSync(path.join(out,'projection-map.json'))).filter(p=>polygons.some(poly=>inside(p[2],p[3],poly)));
  const expanded = new Map(coreMap.map(p=>[p[1]*2048+p[0],p]));
  // Include two atlas texels around mapped UV edges so bilinear sampling cannot
  // reintroduce the old JPEG color from island padding. Core samples take priority.
  for(const [x,y,sx,sy] of coreMap)for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++) {
    const xx=x+dx,yy=y+dy,key=yy*2048+xx;
    if(xx>=0&&xx<2048&&yy>=0&&yy<2048&&!expanded.has(key))expanded.set(key,[xx,yy,sx,sy]);
  }
  map=[...expanded.values()];
  fs.writeFileSync(path.join(out,'applied-projection-map.json'),JSON.stringify(map)+'\n');
  const beforeRender=await sharp(path.join(out,'renders/before-front.png')).removeAlpha().raw().toBuffer();
  probes=config ? config.color_match_probes : [[430,570],[594,570],[395,720],[629,720]];
  biases=probes.map(([x,y])=>sample(generated,x,y).map((v,c)=>v-sample(beforeRender,x,y)[c]));
  changed = 0; rejectedTarget = 0;
  for (const [x,y,sx,sy] of map) {
    const i = (y*2048+x)*3;
    const outer=config && [...polygons.slice(0,2),...polygons.slice(4)].some(p=>inside(sx,sy,p));
    const sourceScreen=sample(beforeRender,sx,sy);
    const bias=biases[config ? ((outer?0:2)+(sx>512?1:0)) : (sy<630?0:2)+(sx>512?1:0)];
    const color = sample(generated,sx,sy).map((v,c)=>Math.max(0,Math.min(255,v-bias[c]))), targetLuma=.2126*color[0]+.7152*color[1]+.0722*color[2];
    // Eye mode protects the dark rim and rejects generated dark features.
    // Legacy mouth mode samples only repaired cream to avoid copying the smile.
    if (config ? (sourceScreen[0]<120 || sourceScreen[1]<60 || color[0]<180 || color[1]<100) : targetLuma < 210) { rejectedTarget++; continue; }
    const nearby = polygons.filter(p => sx >= Math.min(...p.map(v=>v[0])) && sx <= Math.max(...p.map(v=>v[0])) && sy >= Math.min(...p.map(v=>v[1])) && sy <= Math.max(...p.map(v=>v[1])));
    const distance = Math.min(...nearby.flatMap(p => p.map((v,k)=>segmentDistance(sx,sy,v,p[(k+1)%p.length]))));
    const t = Math.min(1,distance/1), fade=Math.max(0,Math.min(1,(650-sy)/30)), weight=config?(outer?fade*fade*(3-2*fade):1):t*t*(3-2*t);
    for (let c=0;c<3;c++) result[i+c]=Math.round(original[i+c]*(1-weight)+color[c]*weight);
    if (!result.subarray(i,i+3).equals(original.subarray(i,i+3))) {mask[y*2048+x]=255;changed++;}
  }
  }
  const png = await sharp(result,{raw:{width:2048,height:2048,channels:3}}).png().toBuffer();
  fs.writeFileSync(path.join(dir,config?'head-before.png':'head-before.jpg'),imageBytes(source,4));
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
  if(config) Object.assign(report,{scope:'Both eye-surround duplicate bands only; v001 mouth retained',appearance_completion:'Awaiting saved GLB visual review',head_encoding:'Lossless PNG retained; decoded pixels outside selected texels exactly preserved',rejected_protected_dark_targets:rejectedTarget});
  if(config) {
    delete report.rejected_noncream_targets;
    report.repair_config_sha256=hash(fs.readFileSync(process.argv[3]));
    report.imagegen.input_edit_sha256=hash(fs.readFileSync(edit));
    report.source_render_sha256=hash(fs.readFileSync(path.join(out,'renders/before-front.png')));
    report.patch_color_method='Generated local single-boundary pink/cream material sampled at matched screen coordinates; local color probes match unchanged neighboring pink and cream; outer-band edits taper into the protected blush between screen y620 and y650. Protected dark screen pixels and generated dark targets excluded; 2 atlas texels of padding.';
  }
  if(config?.mode==='fur-seam') Object.assign(report,{scope:config.scope || 'Only bilateral ear-to-shoulder fur seam; Human-approved eyes and mouth protected',eye_repair_human_gate:'APPROVED by current explicit Human message',appearance_completion:'Local saved-GLB visual review recorded separately; Human PENDING',core_projection_texels_by_view:Object.fromEntries((config.fur_views || ['left-side','right-side','top']).map(view=>[view,projectionMap(view).length])),imagegen:{...report.imagegen,projection_size:[2048,2048],panel_size:[1024,1024]},patch_color_method:'Left profile: local cream bridge across traced seam. Right profile: built-in ImageGen clean material registered to the saved render, with edge-matched correction transferred to Head texels. Screen masks and vertical fades are local; 2 atlas texels of padding are included; prior eye/mouth changed texels are excluded.'});
  fs.writeFileSync(path.join(out,'candidate-validation.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
