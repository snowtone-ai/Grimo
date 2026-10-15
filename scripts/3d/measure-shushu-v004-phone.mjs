// Real phone Chrome via its ADB-forwarded CDP. Only the already-open diagnostic tab is touched.
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {chromium} from 'playwright';
const out='docs/production/shushu/evidence/production-rig-v004-skin-compat';
const mode=process.argv[2]||'stock',seconds=Number(process.argv[3]||300);
const adb=(...args)=>execFileSync('adb',args,{encoding:'utf8',maxBuffer:5e6});
const browser=await chromium.connectOverCDP('http://127.0.0.1:9223'),context=browser.contexts()[0],page=context.pages().find(p=>p.url().includes('8766/'));
const cdp=await context.newCDPSession(page);await cdp.send('Network.enable');
const errors=[];page.on('pageerror',e=>errors.push(e.stack));
const url='http://127.0.0.1:8766/'+out+'/runtime.html?mode='+mode;
const report={mode,date:new Date().toISOString(),conditions:{seconds,canvas:'640x640 physical render pixels, DPR1; CSS fits phone viewport',foreground:true,usbCharging:true,noShadows:true,transport:'adb reverse localhost; not real network',order:'stock then local8; each load tested cold then warm',gpuTime:'UNKNOWN: EXT_disjoint_timer_query_webgl2 unavailable on this device'},environment:{devices:adb('devices','-l'),model:adb('shell','getprop','ro.product.marketname'),android:adb('shell','getprop','ro.build.version.release'),screen:adb('shell','wm','size'),density:adb('shell','wm','density'),refresh:adb('shell','settings','get','system','peak_refresh_rate')},loads:[],thermal:[]};
const save=()=>fs.writeFileSync(out+'/phone-'+mode+'-performance.json',JSON.stringify(report,null,2)+'\n');
const thermal=label=>{const row={label,date:new Date().toISOString(),battery:adb('shell','dumpsys','battery'),thermal:adb('shell','dumpsys','thermalservice'),chromeMemory:adb('shell','dumpsys','meminfo','com.android.chrome')};report.thermal.push(row);save();};
try {
 for(const cold of [true,false]){
  if(cold)await cdp.send('Network.clearBrowserCache');await cdp.send('Network.setCacheDisabled',{cacheDisabled:cold});
  if(!cold){await page.goto(url);await page.waitForFunction(()=>window.qaReady||window.qaError,{},{timeout:120000});}
  const start=Date.now();await page.goto(url);await page.waitForFunction(()=>window.qaReady||window.qaError,{},{timeout:120000});const error=await page.evaluate(()=>window.qaError);if(error)throw Error(error);
  report.loads.push({cache:cold?'cold cache disabled after clear':'warm HTTP cache enabled after cold',wallMs:Date.now()-start,...await page.evaluate(()=>({summary:qa.summary(),resources:performance.getEntriesByType('resource').map(r=>({name:r.name.split('/').at(-1),duration:r.duration,transferSize:r.transferSize,encodedBodySize:r.encodedBodySize,decodedBodySize:r.decodedBodySize})),navigation:performance.getEntriesByType('navigation').map(r=>({duration:r.duration,domInteractive:r.domInteractive,loadEventEnd:r.loadEventEnd})),heap:performance.memory?{usedJSHeapSize:performance.memory.usedJSHeapSize,totalJSHeapSize:performance.memory.totalJSHeapSize,jsHeapSizeLimit:performance.memory.jsHeapSizeLimit}:null,gpu:qa.gpuCapability}))});save();
 }
 await page.evaluate(()=>{qa.sample(1);qa.view('3q');qa.root.anim.speed=1;window.phoneRun={start:performance.now(),last:null,intervals:[],draws:[],triangles:[],contextLost:0,visibility:[],longTasks:[]};document.querySelector('canvas').addEventListener('webglcontextlost',()=>phoneRun.contextLost++);document.addEventListener('visibilitychange',()=>phoneRun.visibility.push({time:performance.now(),state:document.visibilityState}));try{new PerformanceObserver(list=>phoneRun.longTasks.push(...list.getEntries().map(e=>({start:e.startTime,duration:e.duration})))).observe({type:'longtask',buffered:false});}catch{};function loop(t){if(phoneRun.last!==null){phoneRun.intervals.push(t-phoneRun.last);phoneRun.draws.push(qa.app.stats.drawCalls.total);phoneRun.triangles.push(qa.app.stats.frame.triangles);}phoneRun.last=t;if(!phoneRun.done)requestAnimationFrame(loop);}requestAnimationFrame(loop);});
 thermal('playback start');console.log('START',mode,seconds);
 // Five-second intervals let the host keep reporting progress without holding a single tool call.
 for(let elapsed=0;elapsed<seconds;elapsed+=5){await new Promise(r=>setTimeout(r,Math.min(5,seconds-elapsed)*1000));if((elapsed+5)%60===0){thermal('elapsed '+(elapsed+5)+'s');console.log('PLAYING',mode,elapsed+5);}}
 report.playback=await page.evaluate(()=>{phoneRun.done=true;qa.root.anim.speed=0;const a=phoneRun.intervals.slice(),sorted=a.slice().sort((x,y)=>x-y),p=q=>sorted[Math.min(sorted.length-1,Math.floor(q*sorted.length))],sum=a.reduce((s,v)=>s+v,0),budget=1000/60;return {...phoneRun,elapsedMs:performance.now()-phoneRun.start,frames:a.length,rafP50Ms:p(.5),rafP95Ms:p(.95),rafP99Ms:p(.99),rafMaxMs:Math.max(...a),fps:1000*a.length/sum,jankGt25Ms:a.filter(v=>v>25).length,jankGt33_34Ms:a.filter(v=>v>33.34).length,estimatedMissed60HzSlots:a.reduce((s,v)=>s+Math.max(0,Math.round(v/budget)-1),0),drawCallsMean:phoneRun.draws.reduce((s,v)=>s+v,0)/a.length,summary:qa.summary(),heap:performance.memory?{used:performance.memory.usedJSHeapSize,total:performance.memory.totalJSHeapSize}:null};});
 thermal('playback end');save();
 // Real trusted touch events through Chrome Input, measured to next rAF. No claim about touch-to-photon.
 await page.locator('#play').scrollIntoViewIfNeeded();const box=await page.locator('#play').boundingBox();report.touch=[];
 for(let i=0;i<6;i++){await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:box.x+box.width/2,y:box.y+box.height/2}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));}
 report.touch=await page.evaluate(()=>qa.touchLog);await page.evaluate(()=>{qa.root.anim.speed=0;window.scrollTo(0,0)});
 // Foreground return for this tab; unrelated phone tabs and apps are left alone.
 await cdp.send('Page.setWebLifecycleState',{state:'frozen'});await new Promise(r=>setTimeout(r,1000));await cdp.send('Page.setWebLifecycleState',{state:'active'});await page.bringToFront();
 report.foregroundReturn=await page.evaluate(async()=>{const before=qa.state().time;qa.root.anim.speed=1;for(let i=0;i<15;i++)await new Promise(requestAnimationFrame);qa.root.anim.speed=0;return {before,after:qa.state().time,contextLost:phoneRun.contextLost,visibility:document.visibilityState};});
 report.errors=errors;save();console.log('DONE',mode,JSON.stringify({loads:report.loads.map(l=>({cache:l.cache,ready:l.summary.loadedMs,firstFrame:l.summary.firstFrameMs,wall:l.wallMs})),playback:{p50:report.playback.rafP50Ms,p95:report.playback.rafP95Ms,jank:report.playback.jankGt25Ms,frames:report.playback.frames,fps:report.playback.fps},touch:report.touch,errors}));
}finally{save();await browser.close();}
