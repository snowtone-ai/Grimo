// Focused browser evidence using repository's installed Playwright (no app build).
import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const out=path.resolve('docs/production/shushu/evidence/production-rig-v004-runtime');
const captures=path.resolve('output/playwright/shushu-v004-runtime');fs.mkdirSync(captures,{recursive:true});
const browser=await chromium.launch({headless:false,args:['--disable-background-timer-throttling','--disable-renderer-backgrounding']});
const context=await browser.newContext({viewport:{width:1080,height:700},deviceScaleFactor:1});
const results=[];
try{for(const mode of (process.argv[2]?[process.argv[2]]:['stock','four','full8'])){
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.stack));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 await page.goto('http://127.0.0.1:8766/docs/production/shushu/evidence/production-rig-v004-runtime/runtime.html?mode='+mode);
 await page.waitForFunction(()=>window.qaReady||window.qaError,{},{timeout:120000});const error=await page.evaluate(()=>window.qaError);if(error)throw Error(error);
 console.log('LOADED',mode);const summary=await page.evaluate(()=>qa.summary());
 const markers=JSON.parse(fs.readFileSync('docs/production/shushu/evidence/production-rig-v004/proof-timeline.json')).markers;
 const checks=mode==='full8'?[]:await page.evaluate(frames=>frames.map(f=>qa.verify(f)),markers.map(m=>m.frame));
 const states=[['neutral',1],['legs-forward',31],['seat',79],['seat-rest',103],['recover-load',121],['return',169],['half',237],['half-hold',549],['hold-both',533]];
 for(const [name,frame]of states)for(const view of ['front','side','3q']){
  await page.evaluate(({frame,view})=>{qa.sample(frame);qa.view(view)},{frame,view});await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  const filename=`${mode}-${name}-${view}.png`;await page.screenshot({path:path.join(captures,filename),clip:{x:0,y:0,width:640,height:640},timeout:60000});fs.copyFileSync(path.join(captures,filename),path.join(out,filename));
 }
 let benchmark=null,advance=[];
 if(mode!=='full8'){
  benchmark=await page.evaluate(()=>{qa.sample(1);qa.view('3q');return qa.measure(300)});
  advance=await page.evaluate(async()=>{const rows=[];for(const [frame,joint]of [[7,'mixamorig:Head'],[519,'mixamorig:LeftForeArm']]){qa.sample(frame);const n=qa.root.findByName(joint),before=Array.from(n.getWorldTransform().data),t0=qa.state().time;qa.root.anim.speed=1;for(let i=0;i<12;i++)await new Promise(requestAnimationFrame);qa.root.anim.speed=0;rows.push({joint,beforeTime:t0,afterTime:qa.state().time,matrixDelta:Math.max(...Array.from(n.getWorldTransform().data,(x,k)=>Math.abs(x-before[k])))});}return rows;});
  // Actual canvas playback, not interpolated offline frames. WebM captured in page.
  const video=await page.evaluate(async()=>{qa.sample(1);qa.view('3q');const chunks=[],rec=new MediaRecorder(document.querySelector('canvas').captureStream(24),{mimeType:'video/webm;codecs=vp9'});rec.ondataavailable=e=>chunks.push(e.data);const stopped=new Promise(r=>rec.onstop=r);rec.start();qa.root.anim.speed=1;await new Promise(r=>setTimeout(r,7200));qa.root.anim.speed=0;rec.stop();await stopped;const b=new Uint8Array(await new Blob(chunks).arrayBuffer());let s='';for(let i=0;i<b.length;i+=8192)s+=String.fromCharCode(...b.subarray(i,i+8192));return btoa(s);});fs.writeFileSync(path.join(out,mode+'-seat-return.webm'),Buffer.from(video,'base64'));
 }
 results.push({mode,summary,checks,benchmark,advance,errors});fs.writeFileSync(path.join(out,mode+'-runtime.json'),JSON.stringify(results.at(-1),null,2)+'\n');console.log('DONE',mode,JSON.stringify({benchmark,errors,advance}));await page.close();
}}finally{await browser.close();}
