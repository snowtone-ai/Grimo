/* Targeted review-page check. Leaves the requested maximized Chrome open. */
const {chromium}=require('playwright');
const fs=require('node:fs');const path=require('node:path');
const output=path.resolve(__dirname,'../../docs/production/carol/evidence/reconstruction-v006');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:false,args:['--start-maximized']});
 const context=await browser.newContext({viewport:null});const page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400&& !r.url().endsWith('favicon.ico'))errors.push(`${r.status()} ${r.url()}`)});
 await page.goto('http://127.0.0.1:3017/',{waitUntil:'networkidle'});
 const cdp=await context.newCDPSession(page);const {windowId}=await cdp.send('Browser.getWindowForTarget');
 await cdp.send('Browser.setWindowBounds',{windowId,bounds:{windowState:'maximized'}});
 const checks=[];
 for(const view of ['front','side','back','top','3q-left','3q-right']){
  await page.locator(`#views [data-view="${view}"]`).click();
  await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));
  const images=await page.locator('.stage').evaluateAll(stages=>stages.map(s=>({role:s.dataset.role,visible:[...s.querySelectorAll('img')].filter(i=>getComputedStyle(i).opacity==='1').map(i=>i.currentSrc.split('/').pop())})));
  if(images.some(p=>p.visible.length===0))throw Error(`Missing visible evidence: ${view}`);
  checks.push({view,images});
  if(['side','top','3q-left','3q-right'].includes(view))await page.screenshot({path:path.join(output,`review-${view}.png`)});
 }
 await page.locator('#views [data-view="front"]').click();
 for(const mode of ['overlay','difference','silhouette','clay']){
  await page.locator(`#modes [data-mode="${mode}"]`).click();
  await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));
  checks.push({mode,active:await page.locator('.stage[data-role="render"]').getAttribute('data-mode')});
 }
 await page.locator('#modes [data-mode="overlay"]').click();
 await page.locator('#opacity').fill('0.8');await page.locator('#opacity').dispatchEvent('input');
 const opacity=await page.locator('.stage[data-role="render"] .overlay-reference').evaluate(i=>getComputedStyle(i).opacity);
 if(opacity!=='0.8')throw Error(`Overlay opacity failed: ${opacity}`);
 await page.locator('#landmarks').check();const markers=await page.locator('.stage svg circle').count();if(!markers)throw Error('No landmarks drawn');
 await page.locator('#grid').check();if(await page.locator('.stage.grid').count()!==3)throw Error('Grid did not toggle');
 await page.locator('#reset').click();
 await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));
 await page.screenshot({path:path.join(output,'review-front.png')});
 const bounds=await cdp.send('Browser.getWindowBounds',{windowId});
 const report={status:errors.length?'FAIL':'PASS',scope:'Review UI only; not character acceptance',checks,opacity,landmark_count:markers,browser_bounds:bounds.bounds,final_view:'front',final_mode:'clay',page_errors:errors};
 fs.writeFileSync(path.join(output,'review-browser-qa.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:checks.length,landmarks:markers,window:bounds.bounds.windowState}));
 if(errors.length)throw Error(errors.join('\n'));
 browser.on('disconnected',()=>process.exit(0));
})().catch(e=>{console.error(e);process.exitCode=1});
