// Isolated mouth review. Reuses the already reviewed local eight-weight adapter.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
const root=process.cwd(),out='docs/production/shushu/evidence/production-rig-v004-mouth-b';
const asset='/assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-mouth-b-v001.glb';
let html=fs.readFileSync('docs/production/shushu/evidence/production-rig-v004-skin-compat/runtime.html','utf8');
html=html.replace("from './compat.mjs'","from '../production-rig-v004-skin-compat/compat.mjs'");
html=html.replace('Shushu v004 runtime diagnostic','Shushu mouth B candidate');
html=html.replace('v004 / reviewed appearance &amp; seat only — A / B HOLD','Shushu mouth B v001 / Human review pending');
html=html.replace('2026-10-15: forelimb deformation and mouth appearance HOLD. No replacement or Motion production. Diagnostic only.','口B専用候補。閉口 → 小 → 中 → 大 → 閉口を比較。原本置換はHuman判定後。PC local / 口以外の判定は既存Evidenceを参照。');
html=html.replace('max="821"','max="169"').replace("params.get('mode')||'stock'","params.get('mode')||'local8'");
html=html.replace("const source='/assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.glb';",`const source=params.has('before')?'/assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.glb':'${asset}';`);
html=html.replace('orthoHeight:.59','orthoHeight:.28');
html=html.replace("name==='side'?[-3,.5,0]:name==='3q'?[-2,.65,2.5]:[0,.5,3]","name==='side'?[-3,.615,0]:name==='3q'?[-2,.65,2.5]:[0,.615,3]").replace('camera.lookAt(0,.5,0)','camera.lookAt(0,.69,.02)');
// Optional readback probes join the diagnostic oracle only after installation.
// Their materials and vertex buffers keep the ordinary Engine skin path.
html=html.replace("if(mode==='full8'){document.querySelector",`if(params.has('gpu'))for(const name of ['Head','MouthInterior','OralBowl','Tongue']){
 const node=j.nodes.find(n=>n.name==='ShushuStatic_'+name),p=j.meshes[node.mesh].primitives[0],mi=meshes.find(m=>m.node.name===node.name),pos=access(p.attributes.POSITION),zero=new Float32Array(pos.length/3*4);
 affected.push({name:node.name,p,mi,skin:mi.skinInstance,morph:mi.morphInstance,pos,normal:access(p.attributes.NORMAL),w0:access(p.attributes.WEIGHTS_0),j0:access(p.attributes.JOINTS_0),w1:zero,j1:zero,targets:(p.targets||[]).map(t=>({p:t.POSITION!==undefined?access(t.POSITION):null,n:t.NORMAL!==undefined?access(t.NORMAL):null}))});
 }
 if(mode==='full8'){document.querySelector`);
fs.writeFileSync(out+'/runtime.html',html);
if(process.argv.includes('--validate')) {
 const {inspectGlb}=await import('./glb-metrics.mjs');const report=await inspectGlb(asset.slice(1));fs.writeFileSync(out+'/glb-validation.json',JSON.stringify(report,null,2)+'\n');
 if(report.validator.errors)throw Error('GLB validator errors');console.log('GLB_VALIDATED',JSON.stringify(report.validator));
}
if(process.argv.includes('--serve')) {
 const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.webm':'video/webm'};
 http.createServer((req,res)=>{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname),p=path.resolve(root,'.'+pathname);
  const allowed=pathname.startsWith('/docs/production/shushu/evidence/production-rig-v004-')||pathname.startsWith('/node_modules/playcanvas/build/')||pathname===asset||pathname==='/assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.glb';
  if(!allowed||!p.startsWith(root+path.sep)||!fs.existsSync(p)||!fs.statSync(p).isFile()){res.writeHead(404);res.end();return;}
  res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);
 }).listen(8767,'127.0.0.1',()=>console.log('Mouth B local review on http://127.0.0.1:8767/'+out+'/runtime.html'));
}
if(process.argv.includes('--capture')) {
 const {chromium}=await import('@playwright/test');
 const browser=await chromium.launch({headless:true,channel:'chrome'}),page=await browser.newPage({viewport:{width:1100,height:750},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.stack));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 const before=process.argv.includes('--before');
 await page.goto('http://127.0.0.1:8767/'+out+'/runtime.html'+(before?'?before=1':''));
 await page.waitForFunction(()=>window.qaReady||window.qaError,{},{timeout:120000});
 if(await page.evaluate(()=>window.qaError))throw Error(await page.evaluate(()=>window.qaError));
 const frames=before?[['before',1]]:[['closed',1],['small',13],['medium',25],['large',37]],views=['front','side','3q'];
 fs.mkdirSync(out+'/runtime',{recursive:true});const audits=[];
 async function capture(name,frame,view,full=false){
  await page.evaluate(({frame,view,full})=>{qa.sample(frame);qa.view(view);if(full){const c=qa.app.root.findByName('ReviewCamera');c.camera.orthoHeight=.57;c.lookAt(0,.5,0);}else qa.app.root.findByName('ReviewCamera').camera.orthoHeight=.28;},{frame,view,full});
  await page.evaluate(()=>new Promise(r=>qa.app.once('frameend',()=>requestAnimationFrame(r))));
  const data=await page.locator('canvas').evaluate(c=>c.toDataURL('image/png').split(',')[1]);fs.writeFileSync(out+'/runtime/'+name+'-'+view+'.png',Buffer.from(data,'base64'));
 }
 for(const [name,frame] of frames){for(const view of views)await capture(name,frame,view);audits.push(await page.evaluate(f=>qa.verify(f),frame));}
 if(before){fs.writeFileSync(out+'/runtime-before-checks.json',JSON.stringify({errors,audits},null,2)+'\n');await browser.close();process.exit(0);}
 for(const [name,frame] of [['seated-closed',85],['seated-large',121],['close-priority',145],['tongue',157],['return',169]])for(const view of views)await capture(name,frame,view,true);
 // Deterministic real Engine frames, including intermediate opening and return.
 for(const view of ['front','3q','side']) {
  const data=await page.evaluate(async view=>{
   qa.root.anim.speed=0;qa.view(view);qa.app.root.findByName('ReviewCamera').camera.orthoHeight=.28;
   qa.sample(1);await new Promise(r=>qa.app.once('frameend',r));
   const canvas=document.querySelector('canvas'),chunks=[],rec=new MediaRecorder(canvas.captureStream(24),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:3000000});rec.ondataavailable=e=>chunks.push(e.data);rec.start();await new Promise(r=>setTimeout(r,350));
   for(let f=2;f<=73;f++){qa.sample(f);await new Promise(r=>qa.app.once('frameend',r));await new Promise(r=>setTimeout(r,1000/24));}
   await new Promise(r=>setTimeout(r,500));
   rec.stop();await new Promise(r=>rec.onstop=r);const blob=new Blob(chunks,{type:'video/webm'});return await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result.split(',')[1]);fr.readAsDataURL(blob);});
  },view);fs.writeFileSync(out+'/runtime/closed-open-closed-'+view+'.webm',Buffer.from(data,'base64'));
 }
 const summary=await page.evaluate(()=>({summary:qa.summary(),adapter:qa.adapter}));
 for(const frame of [7,19,31,43,55,67,73,85,97,109,121,133,145,157,169])audits.push(await page.evaluate(f=>qa.verify(f),frame));
 fs.writeFileSync(out+'/runtime-checks.json',JSON.stringify({errors,...summary,audits,phone:'Out of scope by Human: PC comparison only'},null,2)+'\n');
 await browser.close();if(errors.length||audits.some(a=>a.maxMorph>1e-5||a.maxAnchor>1e-5))throw Error('Runtime checks failed');console.log('CAPTURED',JSON.stringify({errors,states:frames,views,audits:audits.length,summary:summary.summary.engine}));
}
if(process.argv.includes('--gpu')) {
 const {chromium}=await import('@playwright/test');const browser=await chromium.launch({headless:true,channel:'chrome'}),page=await browser.newPage({viewport:{width:1100,height:750}});
 await page.goto('http://127.0.0.1:8767/'+out+'/runtime.html?gpu=1');await page.waitForFunction(()=>window.qaReady||window.qaError,{},{timeout:120000});
 if(await page.evaluate(()=>window.qaError))throw Error(await page.evaluate(()=>window.qaError));
 const frames=[];for(const f of [1,13,25,37,85,121,145,169])frames.push(await page.evaluate(f=>qa.gpuCapture(f),f));
 fs.writeFileSync(out+'/gpu-mouth-readback.json',JSON.stringify({scope:'Actual GPU vertex shader readback. Original adapter applies to three body meshes only; four mouth/Head probes added to oracle after installation without altering their render buffers/materials.',frames},null,2)+'\n');await browser.close();console.log('GPU_MOUTH_READBACK_SAVED');
}
