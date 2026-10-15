// Isolated compatibility experiment. Never writes the approved asset or old evidence.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import http from 'node:http';
import {execFileSync} from 'node:child_process';
const root=process.cwd(),out='docs/production/shushu/evidence/production-rig-v004-skin-compat';
fs.mkdirSync(out,{recursive:true});
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
if(!fs.existsSync(out+'/protected-inputs.json')) {
 const files=execFileSync('git',['ls-files','-z','--cached','--others','--exclude-standard'],{maxBuffer:20e6}).toString().split('\0').filter(Boolean);
 const rows=files.filter(p=>!p.includes('production-rig-v004-skin-compat')&&!p.includes('shushu-v004-skin-compat')).filter(p=>fs.existsSync(p)&&fs.statSync(p).isFile()).map(p=>({path:p,sha256:sha(fs.readFileSync(p))}));
 fs.writeFileSync(out+'/protected-inputs.json',JSON.stringify(rows,null,2)+'\n');
}
let html=fs.readFileSync('docs/production/shushu/evidence/production-rig-v004-runtime/runtime.html','utf8');
html=html.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">');
html=html.replace('v004 / Human appearance PASS 2026-10-15','v004 / reviewed appearance &amp; seat only — A / B HOLD');
html=html.replace('Runtime / mobile Gate independent. Diagnostic only.','2026-10-15: forelimb deformation and mouth appearance HOLD. No replacement or Motion production. Diagnostic only.');
html=html.replace('</style>','@media(max-width:900px){canvas{width:min(100vw,640px)!important;height:auto!important}aside{position:static;width:auto;padding:8px}button{min-height:44px}} </style>');
html=html.replace("const params=new URLSearchParams", "import {installCompat} from './compat.mjs';\nconst params=new URLSearchParams");
html=html.replace("graphicsDeviceOptions:{antialias:true", "graphicsDeviceOptions:{deviceTypes:['webgl2'],antialias:true");
html=html.replace("const url=mode==='four'?", "const url=mode==='optimized'?'./shushu-v004-optimized4.glb':mode==='four'?");
html=html.replace("if(mode==='full8'){document.querySelector", "await installCompat({qa:window.qa,affected,access,j,Mat4,transform,norm,dist,mode,camera,light,app});\n if(mode==='full8'){document.querySelector");
fs.writeFileSync(out+'/runtime.html',html);
if(process.argv.includes('--serve')) {
 const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.webm':'video/webm'};
 http.createServer((req,res)=>{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname),p=path.resolve(root,'.'+pathname);
  const allowed=pathname.startsWith('/docs/production/shushu/evidence/production-rig-v004-')||pathname.startsWith('/node_modules/playcanvas/build/')||pathname==='/assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.glb';
  if(!allowed||!p.startsWith(root+path.sep)||!fs.existsSync(p)||!fs.statSync(p).isFile()){res.writeHead(404);res.end();return;}
  // Enable a real warm HTTP-cache trial; CDP Network.clearBrowserCache + cacheDisabled for cold.
  res.setHeader('Cache-Control','public, max-age=3600');res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);
 }).listen(8766,'127.0.0.1',()=>console.log('Skin compatibility viewer ready on 8766'));
}
