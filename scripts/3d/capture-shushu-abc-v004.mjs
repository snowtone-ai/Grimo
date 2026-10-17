// PC Chrome + actual PlayCanvas product loader/controller. No mobile operations.
import fs from 'node:fs';import path from 'node:path';import os from 'node:os';import {spawn} from 'node:child_process';import {createHash} from 'node:crypto';
const out='docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004',folder=out+'/pc',asset='assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v004.glb';fs.mkdirSync(folder,{recursive:true});
const sha=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex'),wait=ms=>new Promise(r=>setTimeout(r,ms));
const chrome=spawn('C:/Program Files/Google/Chrome/Application/chrome.exe',['--headless=new','--remote-debugging-port=9231','--user-data-dir='+path.join(os.tmpdir(),'shushu-abc-v004-chrome'),'--no-first-run','--no-default-browser-check','--window-size=1100,800','about:blank'],{windowsHide:true,stdio:'ignore'});
let ws;try{
 let pages;for(let i=0;i<100;i++){try{pages=await(await fetch('http://127.0.0.1:9231/json/list')).json();break;}catch{await wait(250);}}
 ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});let serial=0;const pending=new Map(),errors=[];
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++serial;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
 const ev=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 const save=(n,data)=>fs.writeFileSync(folder+'/'+n,JSON.stringify(data,null,2)+'\n');
 await send('Runtime.enable');await send('Page.enable');await send('Page.navigate',{url:'http://127.0.0.1:8771/'+out+'/runtime.html'});
 for(let i=0;i<480;i++){let v;try{v=await ev('window.qaError||window.qaReady||false')}catch{}if(v===true)break;if(v)throw Error(v);if(i===479)throw Error('qaReady timeout');await wait(250);}
 save('environment.json',{asset,sha256:sha(asset),modules:['shushu-v004-loader-v004.mjs','shushu-v004-deformation-v003.mjs'].map(n=>({path:n,sha256:sha('assets/grimo/production/shushu/runtime/'+n)})),summary:await ev('qa.summary()'),mobile:'UNKNOWN; no device operations'});
 const frames=[1,103,477,493,509,533,549,825,837,849,861,969,981,1041,1053,1065,1077,1085,1089,1095,1101,1107,1113,1117,1125,1137,1149];
 const audits=[];for(const f of frames)audits.push(await ev(`qa.verify(${f},'engine-nlerp')`));save('saved-runtime-correspondence.json',{errors,audits});if(audits.some(a=>a.maxMorph>1e-5||a.maxAnchor>1e-5||a.missing.length))throw Error('Saved/runtime mismatch');
 for(const f of [1089,1113])save('gpu-'+f+'.json',await ev(`qa.gpuCapture(${f})`));
 // Keep a baked surface witness, then replace the viewer's model with the real loader.
 const controls=JSON.parse(fs.readFileSync(out+'/paw-control-timeline.json','utf8'));
 await ev(`window.controlRows=${JSON.stringify(controls)};window.witnesses=[];void 0`);
 for(const f of frames)await ev(`(()=>{const surface=qa.surfaceNormals(${f}),anchors=qa.state().anchors;witnesses.push({f:${f},surface,anchors});})()`);
 const correspondence=await ev(`(async()=>{
  const pc=await import('/node_modules/playcanvas/build/playcanvas.mjs'),{loadShushuCandidate}=await import('/assets/grimo/production/shushu/runtime/shushu-v004-loader-v004.mjs');window.oldQaRoot=qa.root;qa.deformation.dispose();oldQaRoot.enabled=false;
  const c=await loadShushuCandidate({pc,app:qa.app,url:'/${asset}'});window.productionCandidate=c;c.entity.addComponent('anim',{activate:true});if(c.resource.animations.length!==1)throw Error('Unexpected clips');c.entity.anim.assignAnimation('Proof',c.resource.animations[0].resource);c.entity.anim.speed=0;
  const raw=f=>{const index=Math.max(0,Math.min(controlRows.frames.length-1,f-1)),a=Math.floor(index),b=Math.min(a+1,controlRows.frames.length-1),t=index-a;return Object.fromEntries(controlRows.keys.map((k,i)=>[k,controlRows.frames[a][i]*(1-t)+controlRows.frames[b][i]*t]));};window.rawControls=raw;
  const rows=[];for(const snap of witnesses){c.entity.anim.baseLayer.activeStateCurrentTime=snap.f/24;c.entity.anim.update(0);for(const s of c.deformation.streams.filter(x=>x.name.includes('Paw_')))for(let i=0;i<s.targets.length;i++)s.morph.setWeight(i,0);c.pawControls.set(raw(snap.f));await new Promise(r=>qa.app.once('frameend',r));let position=0,normal=0,anchor=0;
   for(const s of c.deformation.streams){const ref=snap.surface.meshes.find(x=>x.name===s.name);for(let i=0;i<s.surface.p.length;i++){position=Math.max(position,Math.abs(s.surface.p[i]-ref.position[i]));normal=Math.max(normal,Math.abs(s.surface.n[i]-ref.normal[i]));}}
   for(const a of snap.anchors){const m=c.entity.findByName(a.name).getWorldTransform().data;for(let i=0;i<16;i++)anchor=Math.max(anchor,Math.abs(m[i]-a.matrix[i]));}rows.push({frame:snap.f,position,normal,anchor});
  }
  const snap=witnesses.find(x=>x.f===1089);c.pawControls.set(null);c.entity.anim.baseLayer.activeStateCurrentTime=1089/24;c.entity.anim.update(0);await new Promise(r=>qa.app.once('frameend',r));let returnPosition=0,returnAnchor=0;
  for(const a of c.deformation.streams){const ref=snap.surface.meshes.find(x=>x.name===a.name);for(let i=0;i<a.surface.p.length;i++)returnPosition=Math.max(returnPosition,Math.abs(a.surface.p[i]-ref.position[i]));}
  for(const a of snap.anchors){const matrix=c.entity.findByName(a.name).getWorldTransform().data;for(let i=0;i<16;i++)returnAnchor=Math.max(returnAnchor,Math.abs(matrix[i]-a.matrix[i]));}
  const returnToClip={frame:1089,position:returnPosition,anchor:returnAnchor};c.pawControls.set(raw(1149));
  qa.root=c.entity;qa.sample=f=>{c.entity.anim.baseLayer.activeStateCurrentTime=f/24;c.entity.anim.update(0);c.pawControls.set(raw(f));};qa.state=()=>({time:c.entity.anim.baseLayer.activeStateCurrentTime,anchors:c.entity.findByName('ANCHOR_Hold.L').getPosition().toString()});return {rows,returnToClip,scope:'Actual product loader. Paw baked weights deliberately zeroed before raw Purpose/Wrist/Seat controls. Current actual surface and all seven anchor matrices compared.'};
 })()`);save('product-raw-controller.json',correspondence);if(correspondence.returnToClip.position>1e-5||correspondence.returnToClip.anchor>1e-4||correspondence.rows.some(r=>r.position>1e-5||r.normal>1e-4||r.anchor>1e-4))throw Error('Raw controller mismatch');
 const ledger=[];const capture=async(name,f,view,mouth=false)=>{await ev(`qa.sample(${f});qa.focus('${view}',${mouth});new Promise(r=>qa.app.once('frameend',()=>requestAnimationFrame(r)))`);const bytes=Buffer.from(await ev("document.querySelector('canvas').toDataURL('image/png').split(',')[1]"),'base64');fs.writeFileSync(folder+'/'+name+'.png',bytes);ledger.push({file:name+'.png',frame:f,view,mouth,sha256:createHash('sha256').update(bytes).digest('hex')});};
 for(const f of [1,103,1041,1053,1077,1089,1095,1101,1113,1117,1125,1149])for(const view of ['front','side','3q','3qR'])await capture('f'+f+'-'+view,f,view);
 for(const f of [825,837,849,861,885,897,969,1113,1117])await capture('mouth-f'+f,f,'front',true);
 save('capture-ledger.json',{route:'production loader/controller',resolution:[640,640],assetSha256:sha(asset),images:ledger});
 if(!process.argv.includes('--stills-only')){
  const video=await ev(`(async()=>{qa.focus('3q',false);const canvas=document.querySelector('canvas'),chunks=[],frames=[],rec=new MediaRecorder(canvas.captureStream(24),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:5000000});rec.ondataavailable=e=>chunks.push(e.data);qa.sample(993);await new Promise(r=>qa.app.once('frameend',r));rec.start();
   for(let f=993;f<=1149;f++){qa.sample(f);await new Promise(r=>qa.app.once('frameend',r));frames.push({frame:f,time:qa.state().time,at:performance.now()});await new Promise(r=>setTimeout(r,1000/24));}rec.stop();await new Promise(r=>rec.onstop=r);const data=await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result.split(',')[1]);fr.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});return {data,frames};})()`);
  const bytes=Buffer.from(video.data,'base64');fs.writeFileSync(folder+'/composition-3q.webm',bytes);save('video-ledger.json',{assetSha256:sha(asset),sha256:createHash('sha256').update(bytes).digest('hex'),frames:video.frames,scope:'Actual PC product frameend recording; MediaRecorder timing includes rendering latency, not fixed-FPS export.'});
 }
 const lifecycle=await ev(`(async()=>{const c=productionCandidate;c.pawControls.set(null);const before=qa.app.graphicsDevice.buffers.size;c.dispose();c.dispose();await new Promise(r=>qa.app.once('frameend',r));return {before,after:qa.app.graphicsDevice.buffers.size,idempotentDispose:true,oldRootStillDisabled:oldQaRoot.enabled===false};})()`);save('lifecycle.json',lifecycle);save('errors.json',errors);if(errors.length)throw Error('Browser runtime errors');console.log('PC_PRODUCT_COMPLETE',JSON.stringify(lifecycle));
}finally{ws?.close();chrome.kill();}
