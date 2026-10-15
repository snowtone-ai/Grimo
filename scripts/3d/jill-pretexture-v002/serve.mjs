// Task-local viewer, no service credentials, upload or production app changes.
import http from 'node:http';
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../..');
const evidence=path.join(root,'docs/production/jill/rig-pretexture-v002');
const routes={
 '/':path.join(root,'scripts/3d/jill-pretexture-v002/viewer.html'),
 '/viewer.mjs':path.join(root,'scripts/3d/jill-pretexture-v002/viewer.mjs'),
 '/engine.mjs':process.env.JILL_PLAYCANVAS_MODULE || 'C:/Users/chidj/project/プロダクト/Grimo/node_modules/playcanvas/build/playcanvas.mjs',
 '/model.glb':path.join(root,'assets/grimo/production/jill/tripo/rig-pretexture-v002/jill-rig-pretexture-v002.glb'),
 '/uv-checker.png':path.join(evidence,'uv-checker.png')
 ,'/playback':path.join(root,'scripts/3d/jill-pretexture-v002/playback.html')
 ,'/continuous.mp4':path.join(evidence,'bounded-continuous-front-side-3q.mp4')
};
const server=http.createServer(async(req,res)=>{
 try{
  if(req.method==='POST'&&req.url==='/video'){
   const chunks=[];let size=0;for await(const chunk of req){size+=chunk.length;if(size>30e6)throw Error('too large');chunks.push(chunk);}
   await writeFile(path.join(evidence,'playcanvas-continuous.webm'),Buffer.concat(chunks));res.end('saved');return;
  }
  if(req.method==='POST'&&req.url==='/evidence'){
   let data='';for await(const chunk of req){data+=chunk;if(data.length>2e6)throw Error('too large');}
   const result=JSON.parse(data);result.model_sha256=createHash('sha256').update(await readFile(routes['/model.glb'])).digest('hex');await writeFile(path.join(evidence,'playcanvas-runtime.json'),JSON.stringify(result,null,2)+'\n');res.end('saved');return;
  }
  const file=routes[req.url];if(req.method!=='GET'||!file){res.writeHead(404);res.end();return;}
  res.setHeader('Content-Type',file.endsWith('.mjs')?'text/javascript':file.endsWith('.html')?'text/html':file.endsWith('.png')?'image/png':file.endsWith('.mp4')?'video/mp4':'model/gltf-binary');
  res.setHeader('Cache-Control','no-store');res.end(await readFile(file));
 }catch(e){res.writeHead(500);res.end(e.message);}
});
server.listen(8842,'127.0.0.1',()=>console.log('Jill review http://127.0.0.1:8842'));
