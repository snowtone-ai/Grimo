import {Application,Entity,Color,Vec3,Vec4,PROJECTION_ORTHOGRAPHIC,version,RESOLUTION_AUTO,FILLMODE_NONE} from '/engine.mjs';
const canvas=document.querySelector('canvas'),state=document.querySelector('#state'),slider=document.querySelector('#time');
const app=new Application(canvas,{graphicsDeviceOptions:{antialias:true,preserveDrawingBuffer:true,deviceTypes:['webgl2']}});
app.scene.ambientLight=new Color(.65,.65,.65);
app.setCanvasFillMode(FILLMODE_NONE);app.setCanvasResolution(RESOLUTION_AUTO);
function resize(){const width=innerWidth,height=Math.min(520,Math.floor(innerHeight*.65));canvas.style.height=height+'px';app.resizeCanvas(width,height);}addEventListener('resize',resize);resize();
const cameras=[],dirs=[new Vec3(0,0,3),new Vec3(3,0,0),new Vec3(1.5,.12,3)];let face=false,playing=true;
for(let i=0;i<3;i++){
 const c=new Entity(['Front','Side','3Q'][i]);c.addComponent('camera',{projection:PROJECTION_ORTHOGRAPHIC,orthoHeight:.57,clearColor:new Color(.87,.89,.85),rect:new Vec4(i/3,0,1/3,1),priority:i});app.root.addChild(c);cameras.push(c);
}
function aim(){cameras.forEach((c,i)=>{const target=face?new Vec3(0,.68,.24):new Vec3(0,.5,0);c.setPosition(target.clone().add(dirs[i]));c.lookAt(target);c.camera.orthoHeight=face?.25:.73;});}aim();
for(const [i,rot] of [[0,[45,35,0]],[1,[35,160,0]]]){const e=new Entity('ReviewLight'+i);e.addComponent('light',{type:'directional',intensity:i?.45:1.1,color:new Color(1,1,1)});e.setEulerAngles(...rot);app.root.addChild(e);}
app.start();
const load=(url,type)=>new Promise((resolve,reject)=>app.assets.loadFromUrl(url,type,(e,a)=>e?reject(e):resolve(a)));
try{
 const asset=await load('/model.glb','container'),resource=asset.resource,entity=resource.instantiateRenderEntity();app.root.addChild(entity);
 if(!resource.animations.length)throw Error('missing proof clip');
 entity.addComponent('anim',{activate:true});entity.anim.assignAnimation('Proof',resource.animations[0].resource);const layer=entity.anim.baseLayer;layer.play('Proof');
 const meshes=entity.findComponents('render').flatMap(c=>c.meshInstances),anchors=entity.find(n=>n.name.startsWith('ANCHOR_'));
 const original=meshes.map(m=>m.material);let checker=false,grid=null;
 const duration=resource.animations[0].resource.duration;slider.max=duration;
 const samples=[],errors=[];let elapsed=0,last=-1,saved=false;
 const report=()=>({engine:version,scope:'Local desktop WebGL2 sampled GLB proof, three simultaneous cameras; no arbitrary runtime solver or phone certification',duration,meshInstances:meshes.length,skinInstances:meshes.filter(m=>m.skinInstance).length,morphInstances:meshes.filter(m=>m.morphInstance).length,morphTargets:meshes.map(m=>m.morphInstance?.morph?.targets?.length??0),anchors:anchors.map(x=>x.name),samples,errors});
 async function save(){await fetch('/evidence',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(report())});}
 document.querySelector('#play').onclick=()=>playing=!playing;
 slider.oninput=()=>{playing=false;layer.activeStateCurrentTime=Number(slider.value);};
 document.querySelector('#face').onclick=()=>{face=!face;aim();};
 document.querySelector('#checker').onclick=async()=>{if(!grid)grid=await load('/uv-checker.png','texture');checker=!checker;meshes.forEach((m,i)=>{if(checker){const material=original[i].clone();material.diffuseMap=grid.resource;material.diffuse.set(1,1,1);material.update();m.material=material;}else m.material=original[i];});};
 document.querySelector('#save').onclick=save;
 document.querySelector('#record').onclick=()=>{
  layer.activeStateCurrentTime=0;playing=true;samples.length=0;face=false;aim();
  const stream=canvas.captureStream(24),recorder=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9'}),chunks=[];
  recorder.ondataavailable=e=>chunks.push(e.data);recorder.onstop=async()=>{await fetch('/video',{method:'POST',body:new Blob(chunks,{type:'video/webm'})});stream.getTracks().forEach(t=>t.stop());await save();document.querySelector('#record').textContent='連続再生を保存済み';};
  recorder.start();setTimeout(()=>recorder.stop(),(duration+.25)*1000);
 };
 for(const [i,name] of ['mouth','blink','head','wing L','wing R','fold','paw L','paw R','tail/leaf','composite L','composite R'].entries()){
  const button=document.createElement('button');button.textContent=name;button.onclick=()=>{playing=false;layer.activeStateCurrentTime=(i*28+12)/24;};document.querySelector('#cases').appendChild(button);
 }
 app.on('update',dt=>{entity.anim.speed=playing?1:0;elapsed+=dt;});
 app.on('frameend',()=>{
  const t=layer.activeStateCurrentTime;if(!Number.isFinite(t))errors.push('nonfinite time');slider.value=t;
  const frame=Math.floor(t*24);
  if(frame!==last&&playing){last=frame;const positions={};for(const name of ['DEF_head','DEF_wing_outer.L','DEF_wing_outer.R','DEF_paw.L','DEF_paw.R','DEF_tail_02']){const n=entity.findByName(name);if(n){const p=n.getPosition();positions[name]=[p.x,p.y,p.z];}}
   const morphs=meshes.map(m=>m.morphInstance?m.morphInstance.morph.targets.map((_,i)=>m.morphInstance.getWeight(i)):[]);
   const anchor=anchors[0]?.getPosition();if(samples.length<1000)samples.push({frame,time:t,positions,morphs,anchor0:anchor?[anchor.x,anchor.y,anchor.z]:null});
  }
  state.textContent=`Engine ${version} | ${meshes.length} meshes / ${meshes.filter(m=>m.skinInstance).length} skins / ${anchors.length} anchors | ${t.toFixed(2)} s / ${duration.toFixed(2)} s | ${playing?'playing':'paused'} | HOLD: lid/muzzle collars and root appearance require further work`;
  if(elapsed>duration+2&&!saved){saved=true;save();}
 });
}catch(e){state.textContent=e.stack;throw e;}
