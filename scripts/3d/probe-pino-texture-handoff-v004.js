async (page) => {
 await page.setViewportSize({width:900,height:850});await page.reload();await page.waitForFunction(()=>window.proof?.ready);
 const states=['neutral','contact','rest','tail-L','tail-R','half','near','closed','wink','combined'];const records=[];
 for(const name of states){
  await page.evaluate(n=>{window.proof.state(n);window.proof.view(['half','near','closed','wink'].includes(n)?'front':'3q',['half','near','closed','wink'].includes(n));},name);
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  records.push(await page.evaluate(n=>{const p=window.proof;return {name:n,skin_matrices:p.mi.find(x=>x.skinInstance).skinInstance.matrices.map(m=>Array.from(m.data)),weights:p.morphs.map(m=>m.morph.targets.map((t,i)=>({name:t.name,weight:m.getWeight(i)}))).flat().filter(t=>t.weight),errors:[...p.errors]};},name));
  if(['contact','rest','closed','wink'].includes(name))await page.locator('canvas').screenshot({path:'artifacts/pino-texture-v004/runtime-'+name+'.png'});
 }
 const summary=await page.evaluate(()=>({engine:window.proof.engine,instances:window.proof.mi.length,bone_names:window.proof.mi.find(x=>x.skinInstance).skinInstance.bones.map(b=>b.name),skins:window.proof.mi.filter(x=>x.skinInstance).length,morphs:window.proof.morphs.map(m=>({targets:m.morph.targets.length,all_normals:m.morph.targets.every(t=>!!t.morphNormals)})),errors:window.proof.errors}));return {summary,records};
}
