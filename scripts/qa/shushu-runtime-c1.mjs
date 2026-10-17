// Focused real-browser C1 evidence. Run against `next start`, never production.
// BASE_URL=http://127.0.0.1:3187 node scripts/qa/shushu-runtime-c1.mjs
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdir, writeFile, readFile, readdir } from 'node:fs/promises';
const base = process.env.BASE_URL || 'http://127.0.0.1:3187';
const out = 'output/playwright/shushu-c1';
await mkdir(out, { recursive: true });
const threeChunks=[];
const sw=await readFile('public/sw.js','utf8');
for(const file of await readdir('.next/static/chunks')) {
  if(!file.endsWith('.js'))continue;
  if(/PlayCanvas|Shushu v004|shushu:download/.test(await readFile('.next/static/chunks/'+file,'utf8'))) {
    assert(!sw.includes(file),'3D chunk must not be precached: '+file);
    threeChunks.push(file);
  }
}
const browser = await chromium.launch({headless:true,channel:'chrome'});
let context = await browser.newContext({viewport:{width:412,height:915},deviceScaleFactor:2});
const instrument = () => {
  const live = new Map(), contexts = [], observers = new Set(), raf = new Set();
  const listeners=[];
  const add=EventTarget.prototype.addEventListener,remove=EventTarget.prototype.removeEventListener;
  const capture=value=>typeof value==='boolean'?value:!!value?.capture;
  EventTarget.prototype.addEventListener=function(type,fn,options){
    if(['visibilitychange','webglcontextlost','webglcontextrestored','resize'].includes(type)&&!listeners.some(x=>x.target===this&&x.type===type&&x.fn===fn&&x.capture===capture(options)))listeners.push({target:this,type,fn,capture:capture(options)});
    return add.call(this,type,fn,options);
  };
  EventTarget.prototype.removeEventListener=function(type,fn,options){
    const i=listeners.findIndex(x=>x.target===this&&x.type===type&&x.fn===fn&&x.capture===capture(options));if(i>=0)listeners.splice(i,1);
    return remove.call(this,type,fn,options);
  };
  const originalGetContext = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function(...args) {
    const gl = originalGetContext.apply(this,args);
    if (gl && args[0] === 'webgl2' && !contexts.includes(gl)) {
      contexts.push(gl);
      for (const kind of ['Buffer','Texture','Shader','Program','Framebuffer','Renderbuffer','VertexArray','Query']) {
        const create = gl['create'+kind].bind(gl), remove = gl['delete'+kind].bind(gl);
        gl['create'+kind] = (...a) => { const value=create(...a);if(value)live.set(value,{kind,gl});return value; };
        gl['delete'+kind] = value => {live.delete(value);return remove(value);};
      }
    }
    return gl;
  };
  const NativeObserver = window.ResizeObserver;
  window.ResizeObserver = class extends NativeObserver {
    observe(...a){observers.add(this);return super.observe(...a);}
    disconnect(){observers.delete(this);return super.disconnect();}
  };
  const request=window.requestAnimationFrame.bind(window), cancel=window.cancelAnimationFrame.bind(window);
  window.requestAnimationFrame=fn=>{let id;id=request(t=>{raf.delete(id);fn(t);});raf.add(id);return id;};
  window.cancelAnimationFrame=id=>{raf.delete(id);cancel(id);};
  window.c1Resources=()=>({canvas:document.querySelectorAll('canvas').length,contexts:contexts.length,activeContexts:contexts.filter(gl=>!gl.isContextLost()).length,live:Object.fromEntries([...new Set([...live.values()].map(x=>x.kind))].map(kind=>[kind,[...live.values()].filter(x=>x.kind===kind&&!x.gl.isContextLost()).length])),listeners:listeners.length,observers:observers.size,raf:raf.size,heap:performance.memory?.usedJSHeapSize});
};
await context.addInitScript(instrument);
let page=await context.newPage();
const errors=[],requests=[],results={base,cycles:[]};
page.on('pageerror',e=>errors.push(e.message));
page.on('console',m=>{if(m.type()==='error')console.error('browser:',m.text());});
context.on('request',r=>requests.push(r.url()));
const waitReady=()=>page.locator('[data-shushu-state="ready"]').waitFor({timeout:120000});
try {
  for(const route of process.env.C1_FAULTS_ONLY?[]:['/tasks','/calendar']) {
    console.log('cold route',route);
    requests.length=0;
    await page.goto(base+route);
    await page.evaluate(async()=>{if('serviceWorker' in navigator)await Promise.race([navigator.serviceWorker.ready,new Promise(r=>setTimeout(r,8000))]);});
    await page.waitForTimeout(2500);
    const assets=requests.filter(x=>/media\.githubusercontent|raw\.githubusercontent|\.glb|shushu-runtime|playcanvas/i.test(x)||threeChunks.some(file=>x.includes(file)));
    // Hashed chunks are also checked by the production SW manifest inspection.
    assert.deepEqual(assets,[]);
    results[route]={requests:[...requests],resources:await page.evaluate(()=>window.c1Resources()),serviceWorkers:await page.evaluate(async()=>(await navigator.serviceWorker.getRegistrations()).map(r=>({scope:r.scope,active:!!r.active})))};
  }
  if(!process.env.C1_FAULTS_ONLY) {
    await page.getByRole('link',{name:'グリモ',exact:true}).click();
    console.log('waiting for Shushu');
    await waitReady();
    await page.screenshot({path:out+'/front.png'});
    results.firstRender=await page.evaluate(()=>({resources:window.c1Resources(),timings:performance.getEntriesByType('measure').filter(x=>x.name.startsWith('shushu:')).map(x=>({name:x.name,ms:x.duration}))}));
  }
  for(let i=0;i<(process.env.C1_FAULTS_ONLY?0:10);i++) {
    console.log('cycle',i+1);
    const loaded=await page.evaluate(()=>window.c1Resources());
    await page.getByRole('link',{name:'タスク',exact:true}).click();
    await page.waitForTimeout(350);
    const released=await page.evaluate(()=>window.c1Resources());
    results.cycles.push({cycle:i+1,loaded,released});
    assert.equal(released.canvas,0);assert.equal(released.observers,0);
    assert.equal(released.activeContexts,0);
    assert.equal(released.listeners,results['/calendar'].resources.listeners);
    assert(Object.values(released.live).every(value=>value===0));
    if(i<9){await page.getByRole('link',{name:'グリモ',exact:true}).click();await waitReady();}
  }
  // Fault injection must reach the network, rather than a successful SW cache.
  await context.close();
  context=await browser.newContext({viewport:{width:412,height:915},deviceScaleFactor:2});
  await context.addInitScript(instrument);
  page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await context.route('**/shushu-v004-motion-gate-v004.glb',r=>r.fulfill({status:503,headers:{'access-control-allow-origin':'*'},body:'injected C1 failure'}));
  await page.goto(base+'/grimo');
  await page.locator('[data-shushu-state="error"]').waitFor();
  results.failure=await page.evaluate(()=>window.c1Resources());
  await page.screenshot({path:out+'/failure.png'});
  await context.unroute('**/shushu-v004-motion-gate-v004.glb');
  await context.route('**/shushu-v004-motion-gate-v004.glb',r=>r.fulfill({status:200,headers:{'access-control-allow-origin':'*'},body:'version https://git-lfs.github.com/spec/v1\noid sha256:invalid\nsize 62567088\n'}));
  await page.getByRole('button',{name:'もう一度読み込む'}).click();
  await page.locator('[data-shushu-state="error"]').waitFor();
  results.lfsPointerRejection='PASS';
  await context.unroute('**/shushu-v004-motion-gate-v004.glb');
  await page.getByRole('button',{name:'もう一度読み込む'}).click();await waitReady();
  results.retry='PASS';
  await page.evaluate(()=>document.querySelector('canvas').getContext('webgl2').getExtension('WEBGL_lose_context').loseContext());
  await page.locator('[data-shushu-state="error"]').waitFor();
  results.contextLoss=await page.evaluate(()=>window.c1Resources());
  await page.getByRole('button',{name:'もう一度読み込む'}).click();await waitReady();
  results.contextRetry='PASS';
  await page.getByRole('link',{name:'タスク',exact:true}).click();
  let held;
  await context.route('**/shushu-v004-motion-gate-v004.glb',r=>{held=r;});
  const request=context.waitForEvent('request',{predicate:r=>r.url().endsWith('/shushu-v004-motion-gate-v004.glb')});
  await page.getByRole('link',{name:'グリモ',exact:true}).click();await request;
  await page.getByRole('link',{name:'タスク',exact:true}).click();
  await held.abort().catch(()=>{});
  await page.waitForTimeout(350);
  results.exitDuringDownload=await page.evaluate(()=>window.c1Resources());
  assert.equal(results.exitDuringDownload.activeContexts,0);
  assert.equal(results.exitDuringDownload.canvas,0);
  assert.deepEqual(errors,[]);
  results.status='PASS';
} catch(error) {results.status='FAIL';results.error=error.stack;throw error;}
finally {results.errors=errors;await writeFile(out+(process.env.C1_FAULTS_ONLY?'/faults.json':'/browser.json'),JSON.stringify(results,null,2));await browser.close();}
