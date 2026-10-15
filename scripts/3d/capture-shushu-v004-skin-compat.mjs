import fs from 'node:fs';
import {chromium} from 'playwright';
const out='docs/production/shushu/evidence/production-rig-v004-skin-compat',tmp='output/playwright/shushu-v004-skin-compat';
fs.mkdirSync(tmp,{recursive:true});
const action=process.argv[2]||'smoke',mode=process.argv[3]||'local8',mobile=process.argv.includes('--mobile');
const browser=mobile?await chromium.connectOverCDP('http://127.0.0.1:9223'):await chromium.launch({headless:false,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--disable-background-timer-throttling','--disable-renderer-backgrounding']});
const context=mobile?browser.contexts()[0]:await browser.newContext({viewport:{width:1080,height:760},deviceScaleFactor:1});
const page=mobile?context.pages().find(p=>p.url().includes('8766/')):await context.newPage();
if(!page)throw Error('Open the diagnostic Chrome tab on the phone first');
const errors=[];page.on('pageerror',e=>errors.push(e.stack));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
const write=(name,data)=>fs.writeFileSync(out+'/'+name,JSON.stringify(data,null,2)+'\n');
try{
 const cdp=await context.newCDPSession(page);await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
 await page.goto('http://127.0.0.1:8766/'+out+'/runtime.html?mode='+mode);
 await page.waitForFunction(()=>window.qaReady||window.qaError,{},{timeout:120000});
 const error=await page.evaluate(()=>window.qaError);if(error)throw Error(error);
 const summary=await page.evaluate(()=>({summary:qa.summary(),adapter:qa.adapter,gpu:qa.gpuCapability}));
 console.log('READY',mode,mobile?'PHONE':'DESKTOP',JSON.stringify({load:summary.summary.loadedMs,adapter:summary.adapter,gpu:summary.gpu}));
 const markers=JSON.parse(fs.readFileSync('docs/production/shushu/evidence/production-rig-v004/proof-timeline.json')).markers.map(m=>m.frame);
 if(action==='fit') {
  const frames=[...new Set([...markers,...markers.slice(1).map((f,i)=>(f+markers[i])/2)])].sort((a,b)=>a-b);
  const data=await page.evaluate(frames=>qa.fitData(frames),frames);write('fit-data.json',data);console.log('FIT',data.entries.length,frames.length);
 }else if(action==='audit') {
  const frames=[...new Set([...markers,...Array.from({length:1641},(_,i)=>1+i*.5)])].sort((a,b)=>a-b),audit=[],binding=[],gpu=[];
  // Batches keep diagnostic CPU work from looking like frame-time measurement.
  for(let i=0;i<frames.length;i+=40){audit.push(...await page.evaluate(fs=>fs.map(f=>qa.compatAudit(f)),frames.slice(i,i+40)));if(i%200===0)console.log('AUDIT',i,frames.length);}
  for(const f of markers)binding.push(await page.evaluate(f=>{const v=qa.verify(f,'engine-nlerp');delete v.skin;return v},f));
  if(mode==='local8')for(const f of [...markers,...[4.5,34.5,78.5,103.5,121.5,168.5,548.5]])gpu.push(await page.evaluate(f=>qa.gpuCapture(f),f));
  write((mobile?'phone-':'desktop-')+mode+'-audit.json',{summary,audit,binding,gpu,errors});
  console.log('RESULT',JSON.stringify({position:Math.max(...audit.flatMap(r=>r.meshes.map(m=>m.positionMax))),normal:Math.max(...audit.flatMap(r=>r.meshes.map(m=>m.normalMaxDeg))),gpuSamples:gpu.length,gpuErrors:gpu.flatMap(g=>g.captures.filter(c=>c.error)),errors}));
 }else if(action==='capture'||action==='defects') {
  const poses=[['neutral',1],['legs-forward',31],['mid-transition',58.5],['seat',79],['seat-rest',103],['recover-load',121],['mid-return',142.5],['return',169],['half',237],['half-hold',549],['hold-both',533]];
  const defectPoses=[['neutral',1],['offer-L',477],['wrist-L',493],['self-L',509],['self-R',517],['hold-both',533],['half-hold',549],['mouth-closed',333],['mouth-small',345],['mouth-medium',349],['mouth-large',357]];
  if(action==='defects')poses.splice(0,poses.length,...defectPoses);
  const shots=[];for(const shade of ['lit','unlit','normal']){
   await page.evaluate(s=>qa.shading(s),shade);
   for(const [name,frame]of (shade==='lit'?poses:poses.filter(p=>['seat','mid-transition','half-hold','mouth-closed','mouth-medium','mouth-large','self-L'].includes(p[0]))))for(const view of ['front','side','3q']){
    await page.evaluate(({frame,view})=>{qa.sample(frame);qa.view(view)},{frame,view});await page.evaluate(()=>new Promise(r=>qa.app.once('frameend',()=>requestAnimationFrame(r))));
    const filename=`${mobile?'phone':'desktop'}-${mode}-${shade}-${name}-${view}.png`;
    const png=await page.evaluate(()=>document.querySelector('canvas').toDataURL('image/png').split(',')[1]);fs.writeFileSync(tmp+'/'+filename,Buffer.from(png,'base64'));fs.copyFileSync(tmp+'/'+filename,out+'/'+filename);shots.push(filename);
   }
  }
  await page.evaluate(()=>qa.shading('lit'));
  // Actual canvas playback, including the full-eight CPU reference, with identical animation clock.
  const video=await page.evaluate(async()=>{qa.sample(1);qa.view('3q');const chunks=[],rec=new MediaRecorder(document.querySelector('canvas').captureStream(24),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:3000000});rec.ondataavailable=e=>chunks.push(e.data);const stop=new Promise(r=>rec.onstop=r);rec.start();qa.root.anim.speed=1;await new Promise(r=>setTimeout(r,7400));qa.root.anim.speed=0;rec.stop();await stop;const bytes=new Uint8Array(await new Blob(chunks).arrayBuffer());let s='';for(let i=0;i<bytes.length;i+=8192)s+=String.fromCharCode(...bytes.subarray(i,i+8192));return btoa(s);});
  fs.writeFileSync(out+`/${mobile?'phone':'desktop'}-${mode}-seat-return.webm`,Buffer.from(video,'base64'));write(`${mobile?'phone':'desktop'}-${mode}-${action}.json`,{summary,shots,method:'640x640 actual WebGL canvas PNG readback. CDP beyond-viewport screenshots are not used.',errors});
  if(action==='defects'){
   const sequence=[];for(const view of ['side','3q'])for(let frame=505;frame<=541;frame+=3){await page.evaluate(({frame,view})=>{qa.sample(frame);qa.view(view)},{frame,view});await page.evaluate(()=>new Promise(r=>qa.app.once('frameend',r)));const n=`${mobile?'phone':'desktop'}-${mode}-arm-${frame}-${view}.png`,png=await page.evaluate(()=>document.querySelector('canvas').toDataURL().split(',')[1]);fs.writeFileSync(out+'/'+n,Buffer.from(png,'base64'));sequence.push(n);}
   // Actual continuous arm / mouth playback excerpts, no generated interpolation.
   for(const [label,start,duration]of [['arm',505,1.6],['mouth',333,1.15]])for(const view of ['side','3q']){
    const encoded=await page.evaluate(async({start,duration,view})=>{qa.sample(start);qa.view(view);const chunks=[],rec=new MediaRecorder(document.querySelector('canvas').captureStream(24),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:3000000});rec.ondataavailable=e=>chunks.push(e.data);const stopped=new Promise(r=>rec.onstop=r);rec.start();qa.root.anim.speed=1;await new Promise(r=>setTimeout(r,duration*1000));qa.root.anim.speed=0;rec.stop();await stopped;const bytes=new Uint8Array(await new Blob(chunks).arrayBuffer());let s='';for(let i=0;i<bytes.length;i+=8192)s+=String.fromCharCode(...bytes.subarray(i,i+8192));return btoa(s)},{start,duration,view});fs.writeFileSync(out+`/${mobile?'phone':'desktop'}-${mode}-${label}-${view}.webm`,Buffer.from(encoded,'base64'));
   }write(`${mobile?'phone':'desktop'}-${mode}-sequences.json`,{sequence,errors});
  }
 }else {
  const gpu=await page.evaluate(()=>qa.gpuCapture(79));
  await page.locator('canvas').screenshot({path:tmp+'/smoke.png'});write('smoke-'+(mobile?'phone':'desktop')+'.json',{summary,gpu,errors});console.log('GPU',JSON.stringify(gpu),'ERRORS',errors);
 }
}finally{if(!mobile)await browser.close();else await browser.close();}
