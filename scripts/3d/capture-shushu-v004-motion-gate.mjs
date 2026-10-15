// Native CDP transport. Restricts phone operations to the existing Shushu tab.
import fs from 'node:fs';import path from 'node:path';import os from 'node:os';
import {spawn,execFileSync} from 'node:child_process';
const out='docs/production/shushu/evidence/production-rig-v004-motion-ready'+(process.argv.includes('--v002')?'/final-v002':'');
const phone=process.argv.includes('--phone'),before=process.argv.includes('--source-normals');
const port=phone?9223:9224,host='http://127.0.0.1:'+port;
const label=(phone?'phone':'desktop')+(before?'-source-normals':'')+(process.argv.includes('--face-smoke')?'-face-smoke':''),folder=out+'/'+label;
fs.mkdirSync(folder,{recursive:true});
const wait=ms=>new Promise(r=>setTimeout(r,ms));let chrome;
if(!phone){
 const executable='C:/Program Files/Google/Chrome/Application/chrome.exe';
 chrome=spawn(executable,['--headless=new','--remote-debugging-port='+port,'--user-data-dir='+path.join(os.tmpdir(),'shushu-motion-gate-chrome'),'--no-first-run','--no-default-browser-check','--window-size=1100,800','about:blank'],{windowsHide:true,stdio:'ignore'});
}
let pages;
for(let i=0;i<120;i++){try{pages=await(await fetch(host+'/json/list')).json();break;}catch{await wait(250);}}
const target=phone?pages.find(p=>p.type==='page'&&/127\.0\.0\.1:876[68]\/docs\/production\/shushu\//.test(p.url)):pages.find(p=>p.type==='page');
if(!target)throw Error('No authorized Shushu diagnostic tab');
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
let serial=0;const pending=new Map(),errors=[];
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);};
function send(method,params={}){return new Promise((resolve,reject)=>{const id=++serial;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});}
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
const save=(name,data)=>fs.writeFileSync(folder+'/'+name,JSON.stringify(data,null,2)+'\n');
await send('Page.enable');await send('Runtime.enable');
const url='http://127.0.0.1:8768/'+out+'/runtime.html'+(before?'?sourceNormals=1':'');
await send('Page.navigate',{url});await send('Page.bringToFront');
for(let i=0;i<480;i++){const ready=await evaluate('window.qaError||window.qaReady||false');if(ready===true)break;if(ready)throw Error(ready);await wait(250);if(i===479)throw Error('qaReady timeout');}
await evaluate('qa.root.anim.speed=0;window.scrollTo(0,0)');
// Keep the authorized diagnostic visible through the sustained device test.
await evaluate("navigator.wakeLock?.request('screen').then(x=>window.gateWakeLock=x).catch(()=>null)");
save('environment.json',await evaluate(`({summary:qa.summary(),normalRepair:{...qa.normalRepair,times:undefined},gpu:qa.gpuCapability,visibility:document.visibilityState,url:location.href,date:new Date().toISOString()})`));
async function capture(name,frame,view,mouth=false){
 await evaluate(`qa.sample(${frame});qa.focus(${JSON.stringify(view)},${mouth});new Promise(r=>qa.app.once('frameend',()=>requestAnimationFrame(r)))`);
 const png=await evaluate("document.querySelector('canvas').toDataURL('image/png').split(',')[1]");fs.writeFileSync(folder+'/'+name+'-'+view+'.png',Buffer.from(png,'base64'));
}
if(process.argv.includes('--gpu-only')){
 for(const frame of [1,477,493,509,517,533,549]){
  await capture('gpu-frame'+frame,frame,'3q',false);
  await evaluate(`qa.surfaceNormals(${frame})`);
  save('gpu-'+frame+'.json',await evaluate(`qa.gpuCapture(${frame})`));
 }
}else if(process.argv.includes('--face-smoke')){
 for(const [name,f] of [['closed',825],['medium',849],['large',861]])for(const view of ['front','side','3q'])await capture(name,f,view,true);
 save('timing.json',await evaluate('({lastTimes:qa.normalRepair.times.slice(-100),scope:qa.normalRepair.scope})'));
}else if(process.argv.includes('--smoke')){
 await capture('hold',533,'side');save('surface-533.json',await evaluate('qa.surfaceNormals(533)'));console.log('SMOKE',label,await evaluate('qa.summary().unmaskedRenderer'));
}else{
 const rows=[['closed',825,true],['small',837,true],['medium',849,true],['large',861,true],['neutral',1,false],['seat',103,false],['offer',477,false],['wrist',493,false],['self',509,false],['self-r',517,false],['hold',533,false],['seat-hold',549,false],['return',993,false],['close-priority',969,true],['tongue',981,true]];
 const audits=[];
 for(const [name,frame,mouth] of rows){
  for(const view of ['front','side','3q'])await capture(name,frame,view,mouth);
  audits.push(await evaluate(`qa.verify(${frame},'engine-nlerp')`));console.log('CAPTURE',label,name);
 }
 for(const frame of [1,477,493,509,517,533,549]){
  save('surface-'+frame+'.json',await evaluate(`qa.surfaceNormals(${frame})`));
  if(before)save('exported-normal-'+frame+'.json',await evaluate(`qa.surface(${frame})`));
  if(!before){await evaluate(`qa.surfaceNormals(${frame})`);save('gpu-'+frame+'.json',await evaluate(`qa.gpuCapture(${frame})`));}
 }
 for(let frame=505;frame<=541;frame+=3)for(const view of ['side','3q'])await capture('f'+frame,frame,view,false);
 if(!before)for(const [name,start,end,mouth] of [['mouth',825,897,true],['arm',477,557,false],['seat-return',1,169,false]])for(const view of ['front','side','3q']){
  const data=await evaluate(`(async()=>{
   qa.root.anim.speed=0;qa.focus('${view}',${mouth});qa.sample(${start});await new Promise(r=>qa.app.once('frameend',r));
   const canvas=document.querySelector('canvas'),chunks=[],rec=new MediaRecorder(canvas.captureStream(24),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:3000000});rec.ondataavailable=e=>chunks.push(e.data);rec.start();await new Promise(r=>setTimeout(r,200));
   for(let f=${start};f<=${end};f++){qa.sample(f);await new Promise(r=>qa.app.once('frameend',r));await new Promise(r=>setTimeout(r,1000/24));}
   await new Promise(r=>setTimeout(r,200));rec.stop();await new Promise(r=>rec.onstop=r);return await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result.split(',')[1]);fr.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});})()`);
  fs.writeFileSync(folder+'/'+name+'-'+view+'.webm',Buffer.from(data,'base64'));console.log('VIDEO',label,name,view);
 }
 if(!before){
  const seconds=process.argv.includes('--measure')?300:30;
  if(phone)save('device-start.json',{devices:execFileSync('adb',['devices','-l'],{encoding:'utf8'}),marketname:execFileSync('adb',['shell','getprop','ro.product.marketname'],{encoding:'utf8'}),battery:execFileSync('adb',['shell','dumpsys','battery'],{encoding:'utf8'}),thermal:execFileSync('adb',['shell','dumpsys','thermalservice'],{encoding:'utf8'})});
  await evaluate(`qa.sample(477);qa.focus('3q',false);qa.normalRepair.times.length=0;qa.root.anim.speed=1;window.gatePerf={last:null,intervals:[],lost:0};document.querySelector('canvas').addEventListener('webglcontextlost',()=>gatePerf.lost++);window.gateTick=t=>{if(gatePerf.last!==null)gatePerf.intervals.push(t-gatePerf.last);gatePerf.last=t;if(!gatePerf.done)requestAnimationFrame(gateTick);};requestAnimationFrame(gateTick);`);
  for(let i=0;i<seconds;i+=10){await wait(Math.min(10,seconds-i)*1000);console.log('MEASURE',label,i+10);}
  save('performance.json',await evaluate(`(()=>{gatePerf.done=true;qa.root.anim.speed=0;const a=gatePerf.intervals.slice().sort((a,b)=>a-b),b=qa.normalRepair.times.slice().sort((a,b)=>a-b),q=(v,p)=>v[Math.min(v.length-1,Math.floor(v.length*p))];return {seconds:${seconds},samples:a.length,rafP50:q(a,.5),rafP95:q(a,.95),rafP99:q(a,.99),rafMax:q(a,1),jankGt25:a.filter(t=>t>25).length,normalCpuP50:q(b,.5),normalCpuP95:q(b,.95),normalCpuMax:q(b,1),contextLoss:gatePerf.lost,gpuTime:'UNKNOWN; rAF is not GPU time',summary:qa.summary(),intervals:gatePerf.intervals,normalCpuTimes:qa.normalRepair.times};})()`));
  if(phone){save('device-end.json',{battery:execFileSync('adb',['shell','dumpsys','battery'],{encoding:'utf8'}),thermal:execFileSync('adb',['shell','dumpsys','thermalservice'],{encoding:'utf8'})});const screen=execFileSync('adb',['exec-out','screencap','-p'],{maxBuffer:10e6});fs.writeFileSync(folder+'/android-screen.png',screen);}
 }
 save('checks.json',{errors,audits,sourceNormals:before});
 if(errors.length||audits.some(a=>a.maxMorph>1e-5||a.maxAnchor>1e-5||a.missing.length))throw Error('Runtime correspondence failure');
}
ws.close();if(chrome)chrome.kill();console.log('DONE',label);
