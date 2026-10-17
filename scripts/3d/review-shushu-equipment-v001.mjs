// Local scoped static evidence server. It never rewrites historical review files.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';
const root=process.cwd(),base='/docs/production/shushu/evidence/',assets='/assets/grimo/production/shushu/';
const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.webm':'video/webm','.md':'text/plain;charset=utf-8'};
http.createServer((req,res)=>{const url=decodeURIComponent(new URL(req.url,'http://localhost').pathname),p=path.resolve(root,'.'+url);
 const allowed=url.startsWith(base)||url.startsWith(assets)||url.startsWith('/node_modules/playcanvas/build/')||url==='/assets/grimo/source/shushu/shushu-Identity-canonical.png';
 if(!allowed||!p.startsWith(root+path.sep)||!fs.existsSync(p)||!fs.statSync(p).isFile()){res.writeHead(404);res.end();return;}
 res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);
}).listen(8772,'127.0.0.1',()=>console.log('Shushu equipment review http://127.0.0.1:8772/docs/production/shushu/evidence/standard-appearance-v001/index.html'));
