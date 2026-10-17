// Loopback-only bounded review. No upload or production app changes.
import http from 'node:http';
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../..');
const evidence=process.env.JILL_REVIEW_EVIDENCE||path.join(root,'docs/production/jill/texture-return-v005');
const routes={
 '/':path.join(root,'scripts/3d/jill-texture-v005/viewer.html'),
 '/viewer.mjs':path.join(root,'scripts/3d/jill-texture-v005/viewer.mjs'),
 '/engine.mjs':process.env.JILL_PLAYCANVAS_MODULE||'C:/Users/chidj/project/プロダクト/Grimo/node_modules/playcanvas/build/playcanvas.mjs',
 '/model.glb':process.env.JILL_REVIEW_MODEL||path.join(root,'assets/grimo/production/jill/tripo/texture-return-v005/jill-textured-review-bounded-v005.glb'),
 '/schedule.json':path.join(evidence,'runtime-schedule.json')
};
if(process.env.JILL_REVIEW_MOUTH_CONTROLS==='1'){
 routes['/mouth-controller.mjs']=path.join(root,'scripts/3d/jill-mouth-v006/mouth-controller.mjs');
 routes['/mouth-review.mjs']=path.join(root,'scripts/3d/jill-mouth-v006/review-controls.mjs');
}
http.createServer(async(req,res)=>{
 try{
  if(req.method==='GET'&&req.url==='/review-config.json'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify({mouthControls:process.env.JILL_REVIEW_MOUTH_CONTROLS==='1',leftSide:process.env.JILL_REVIEW_LEFT_SIDE==='1',appearanceStatus:process.env.JILL_REVIEW_APPEARANCE_STATUS||null}));return;}
  if(req.method==='POST'&&req.url==='/evidence'){
   let data='';for await(const c of req){data+=c;if(data.length>3e6)throw Error('too large');}
   const result=JSON.parse(data);result.model_sha256=createHash('sha256').update(await readFile(routes['/model.glb'])).digest('hex');
   const capture=process.env.JILL_REVIEW_CAPTURE||'playcanvas-runtime.json';
   if(!/^[\w.-]+\.json$/.test(capture))throw Error('Invalid evidence filename');
   await writeFile(path.join(evidence,capture),JSON.stringify(result,null,2)+'\n');res.end('saved');return;
  }
  const file=routes[req.url];if(req.method!=='GET'||!file){res.writeHead(404);res.end();return;}
  let body=await readFile(file);
  if(file.endsWith('.html')&&process.env.JILL_REVIEW_LABEL)body=Buffer.from(body.toString().replaceAll('Texture v005',process.env.JILL_REVIEW_LABEL));
  res.setHeader('Content-Type',file.endsWith('.mjs')?'text/javascript':file.endsWith('.html')?'text/html':file.endsWith('.json')?'application/json':'model/gltf-binary');res.setHeader('Cache-Control','no-store');res.end(body);
 }catch(e){res.writeHead(500);res.end(e.message);}
}).listen(Number(process.env.JILL_REVIEW_PORT||8846),'127.0.0.1',()=>console.log('Jill v005 review http://127.0.0.1:'+String(process.env.JILL_REVIEW_PORT||8846)));
