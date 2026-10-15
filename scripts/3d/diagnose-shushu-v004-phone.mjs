// Focused read-only follow-up: surface oracle, loop binding and trusted touch.
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {chromium} from 'playwright';
const out='docs/production/shushu/evidence/production-rig-v004-skin-compat';
const browser=await chromium.connectOverCDP('http://127.0.0.1:9223'),context=browser.contexts()[0],page=context.pages().find(p=>p.url().includes('8766/'));
const cdp=await context.newCDPSession(page);await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
try{
 const report={date:new Date().toISOString(),modes:{}};
 for(const mode of ['stock','local8']){
  await page.goto('http://127.0.0.1:8766/'+out+'/runtime.html?mode='+mode);await page.waitForFunction(()=>window.qaReady);
  const result={};
  result.neutralReturn=await page.evaluate(()=>{qa.sample(1);const a=qa.state();qa.sample(549);qa.sample(821);const b=qa.state();return {from:549,to:821,baseline:1,jointMatrixMax:Math.max(...a.joints.flatMap((j,i)=>j.matrix.map((x,k)=>Math.abs(x-b.joints[i].matrix[k])))),anchorMatrixMax:Math.max(...a.anchors.flatMap((j,i)=>j.matrix.map((x,k)=>Math.abs(x-b.anchors[i].matrix[k])))),morphMax:Math.max(...a.morphs.flatMap((m,i)=>m.weights.map((x,k)=>Math.abs(x-b.morphs[i].weights[k])))),anchors:b.anchors.length};});
  result.draws=await page.evaluate(async()=>{
   qa.sample(1);qa.view('3q');qa.root.anim.speed=1;
   const gl=qa.app.graphicsDevice.gl,original=gl.drawElements,rows=[];let row={indexedCalls:0,triangles:0};
   gl.drawElements=function(mode,count,...rest){row.indexedCalls++;if(mode===gl.TRIANGLES)row.triangles+=count/3;return original.call(this,mode,count,...rest)};
   try{for(let i=0;i<60;i++){await new Promise(r=>qa.app.once('frameend',r));rows.push(row);row={indexedCalls:0,triangles:0};}}
   finally{gl.drawElements=original;qa.root.anim.speed=0;}
   return {method:'Actual WebGL drawElements calls over 60 animated frames. Offscreen Morph drawArrays passes excluded. Existing app.stats.frame.triangles counter was zero and is unavailable.',rows};
  });
  if(mode==='local8'){
   const surfaces=await page.evaluate(()=>[1,477,493,509,517,533,549].map(f=>qa.surface(f)));fs.writeFileSync(out+'/surface-oracle.json',JSON.stringify(surfaces));
   result.loop=await page.evaluate(()=>{const d=qa.summary().duration;qa.sample(533);const a=qa.state();qa.root.anim.baseLayer.activeStateCurrentTime=533/24+8*d;qa.root.anim.update(0);const b=qa.state();return {duration:d,offsetCycles:8,time:b.time,jointMatrixMax:Math.max(...a.joints.flatMap((j,i)=>j.matrix.map((x,k)=>Math.abs(x-b.joints[i].matrix[k])))),morphMax:Math.max(...a.morphs.flatMap((m,i)=>m.weights.map((x,k)=>Math.abs(x-b.morphs[i].weights[k]))))};});
   result.mouthIsolation={method:'Temporarily hide MouthInterior, OralBowl and Tongue in the diagnostic viewer; restore all visibility afterward. Original GLB/Texture unchanged.',frames:[333,357]};
   for(const frame of [333,357]){
    const png=await page.evaluate(async frame=>{qa.sample(frame);qa.view('front');const parts=qa.meshes.filter(m=>/MouthInterior|OralBowl|Tongue/.test(m.node.name)),visibility=parts.map(m=>m.visible);parts.forEach(m=>m.visible=false);await new Promise(r=>qa.app.once('frameend',r));const png=document.querySelector('canvas').toDataURL().split(',')[1];parts.forEach((m,i)=>m.visible=visibility[i]);return png;},frame);
    fs.writeFileSync(out+'/phone-local8-mouth-head-only-'+frame+'.png',Buffer.from(png,'base64'));
   }
  }
  await page.evaluate(()=>{qa.sample(533);qa.view('side');qa.touchLog=[];});await page.locator('#play').scrollIntoViewIfNeeded();const box=await page.locator('#play').boundingBox();result.touch=[];
  for(let i=0;i<6;i++){
   const before=await page.evaluate(()=>qa.root.anim.speed);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:box.x+box.width/2,y:box.y+box.height/2}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(400);result.touch.push({before,after:await page.evaluate(()=>qa.root.anim.speed)});
  }
  result.pointerEvents=await page.evaluate(()=>qa.touchLog);await page.evaluate(()=>{qa.root.anim.speed=0;qa.sample(533);qa.view('side');window.scrollTo(0,0)});await page.waitForTimeout(150);
  fs.writeFileSync(out+'/phone-'+mode+'-android-screen.png',execFileSync('adb',['exec-out','screencap','-p'],{maxBuffer:15e6}));
  report.modes[mode]=result;
 }
 fs.writeFileSync(out+'/phone-focused-checks.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
}finally{await browser.close();}
