// Local PC evidence only. No device bridge or external service.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';
const root=process.cwd(),base='docs/production/shushu/evidence/production-rig-v004-motion-ready',out=base+'/final-v004';
let html=fs.readFileSync(base+'/final-v003/runtime.html','utf8').replaceAll('shushu-v004-motion-gate-v003.glb','shushu-v004-motion-gate-v004.glb').replace('v003：W口・鼻下紐除去を維持し局所面と前肢接触を修正。製品制御経路を実機検証。最終Human外観GO待ち／原本置換・Motion量産HOLD。','v004 別名再審査候補。Human外観GO待ち。PC検証用。スマホ再検証UNKNOWN。原本置換・Motion量産HOLD。');
fs.writeFileSync(out+'/runtime.html',html);fs.copyFileSync(base+'/final-v003/compat.mjs',out+'/compat.mjs');
if(process.argv.includes('--serve')){
 const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.webm':'video/webm','.mp4':'video/mp4'};
 http.createServer((req,res)=>{const url=decodeURIComponent(new URL(req.url,'http://localhost').pathname),p=path.resolve(root,'.'+url),allowed=url.startsWith('/'+base+'/')||url.startsWith('/node_modules/playcanvas/build/')||url.startsWith('/assets/grimo/production/shushu/runtime/')||/^\/assets\/grimo\/production\/shushu\/tripo\/geometry-v003\/rigging\/shushu-v004-motion-gate-v00[34]\.glb$/.test(url);
  if(!allowed||!p.startsWith(root+path.sep)||!fs.existsSync(p)||!fs.statSync(p).isFile()){res.writeHead(404);res.end();return;}res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);
 }).listen(8771,'127.0.0.1',()=>console.log('PC candidate http://127.0.0.1:8771/'+out+'/runtime.html'));
}
