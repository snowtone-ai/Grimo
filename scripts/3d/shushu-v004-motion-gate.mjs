// Reuse the established viewer and compatibility adapter; isolated candidate only.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';
const root=process.cwd(),base='docs/production/shushu/evidence/production-rig-v004-motion-ready',final=process.argv.includes('--v002'),out=base+(final?'/final-v002':'');
const asset='/assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-'+(final?'v002':'v001')+'.glb';
if(final)fs.copyFileSync(base+'/surface-normals.mjs',out+'/surface-normals.mjs');
let html=fs.readFileSync('docs/production/shushu/evidence/production-rig-v004-skin-compat/runtime.html','utf8');
html=html.replace("from './compat.mjs'","from '../production-rig-v004-skin-compat/compat.mjs'");
// Keep the established compatibility adapter's GPU readback, with its normal
// oracle matched to this candidate's evaluated-surface correction.
let compat=fs.readFileSync(base+'/../production-rig-v004-skin-compat/compat.mjs','utf8');
compat=compat.replace('const {full,normal}=contributions(a,i,mats),p=','const contribution=contributions(a,i,mats),full=contribution.full,normal=qa.normalRepair?.enabled&&a.surface?Array.from(a.surface.n.subarray(i*3,i*3+3)):contribution.normal,p=');
if(!compat.includes('normal=qa.normalRepair?.enabled'))throw Error('GPU oracle patch did not match');
compat=compat.replace('skinOnlyNormalDeg:skinOnlyNormal','skinOnlyNormalDeg:qa.normalRepair?.enabled&&a.surface?null:skinOnlyNormal,normalOracle:qa.normalRepair?.enabled&&a.surface?"current evaluated surface NORMAL stream":"exported morph/skin normal"');
fs.writeFileSync(out+'/compat.mjs',compat);
html=html.replace("from '../production-rig-v004-skin-compat/compat.mjs'","from './compat.mjs'");
html=html.replace('Shushu v004 runtime diagnostic','Shushu A/B Motion Gate');
html=html.replace('v004 / reviewed appearance &amp; seat only — A / B HOLD','Shushu v004 A/B Gate / Human PENDING');
html=html.replace('2026-10-15: forelimb deformation and mouth appearance HOLD. No replacement or Motion production. Diagnostic only.','W口を保ち鼻下の紐を局所除去。前肢の面法線候補。Human局所確認までMotion量産HOLD。');
html=html.replace('max="821"','max="993"').replace("params.get('mode')||'stock'","params.get('mode')||'local8'");
html=html.replace("const source='/assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.glb';",`const source='${asset}';`);
html=html.replace("import {installCompat}","import {installSurfaceNormals} from './surface-normals.mjs';\nimport {installCompat}");
html=html.replace("if(mode==='full8'){document.querySelector",`installSurfaceNormals({qa:window.qa,affected,access,Mat4,app,enabled:!params.has('sourceNormals')});
 qa.focus=(view,mouth=false)=>{qa.view(view);camera.camera.orthoHeight=mouth?.28:.59;if(mouth){camera.setPosition(...(view==='side'?[-3,.615,0]:view==='3q'?[-2,.65,2.5]:[0,.615,3]));camera.lookAt(0,.69,.02);}};
 if(mode==='full8'){document.querySelector`);
fs.writeFileSync(out+'/runtime.html',html);
if(process.argv.includes('--validate')){
 const {inspectGlb}=await import('./glb-metrics.mjs');const report=await inspectGlb(asset.slice(1));fs.writeFileSync(out+'/glb-validation.json',JSON.stringify(report,null,2)+'\n');if(report.validator.errors)throw Error('GLB errors');console.log(report.validator);
}
if(process.argv.includes('--serve')){
 const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.webm':'video/webm','.mp4':'video/mp4'};
 http.createServer((req,res)=>{const url=decodeURIComponent(new URL(req.url,'http://localhost').pathname),p=path.resolve(root,'.'+url);
 const allowed=url.startsWith('/docs/production/shushu/evidence/production-rig-v004-')||url.startsWith('/node_modules/playcanvas/build/')||['v001','v002'].some(v=>url==='/assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-'+v+'.glb');
 if(!allowed||!p.startsWith(root+path.sep)||!fs.existsSync(p)||!fs.statSync(p).isFile()){res.writeHead(404);res.end();return;}
 res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);
 }).listen(8768,'127.0.0.1',()=>console.log('A/B gate on http://127.0.0.1:8768/'+out+'/runtime.html'));
}
