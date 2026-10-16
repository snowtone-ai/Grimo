// Loopback-only bounded review. No upload or production app changes.
import http from 'node:http';
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../..');
const evidence=path.join(root,'docs/production/jill/texture-return-v005');
const routes={
 '/':path.join(root,'scripts/3d/jill-texture-v005/viewer.html'),
 '/viewer.mjs':path.join(root,'scripts/3d/jill-texture-v005/viewer.mjs'),
 '/engine.mjs':process.env.JILL_PLAYCANVAS_MODULE||'C:/Users/chidj/project/プロダクト/Grimo/node_modules/playcanvas/build/playcanvas.mjs',
 '/model.glb':path.join(root,'assets/grimo/production/jill/tripo/texture-return-v005/jill-textured-review-bounded-v005.glb'),
 '/schedule.json':path.join(evidence,'runtime-schedule.json')
};
http.createServer(async(req,res)=>{
 try{
  if(req.method==='POST'&&req.url==='/evidence'){
   let data='';for await(const c of req){data+=c;if(data.length>3e6)throw Error('too large');}
   const result=JSON.parse(data);result.model_sha256=createHash('sha256').update(await readFile(routes['/model.glb'])).digest('hex');
   await writeFile(path.join(evidence,'playcanvas-runtime.json'),JSON.stringify(result,null,2)+'\n');res.end('saved');return;
  }
  const file=routes[req.url];if(req.method!=='GET'||!file){res.writeHead(404);res.end();return;}
  res.setHeader('Content-Type',file.endsWith('.mjs')?'text/javascript':file.endsWith('.html')?'text/html':file.endsWith('.json')?'application/json':'model/gltf-binary');res.setHeader('Cache-Control','no-store');res.end(await readFile(file));
 }catch(e){res.writeHead(500);res.end(e.message);}
}).listen(8846,'127.0.0.1',()=>console.log('Jill v005 review http://127.0.0.1:8846'));
