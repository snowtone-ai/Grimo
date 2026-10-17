import {Application,Entity,Color,Vec3,Vec4,PROJECTION_ORTHOGRAPHIC,version,RESOLUTION_AUTO,FILLMODE_NONE} from '/engine.mjs';
const canvas=document.querySelector('canvas'),status=document.querySelector('#state'),slider=document.querySelector('#time');
const app=new Application(canvas,{graphicsDeviceOptions:{antialias:true,preserveDrawingBuffer:true,deviceTypes:['webgl2']}});
app.scene.ambientLight=new Color(.65,.65,.65);app.setCanvasFillMode(FILLMODE_NONE);app.setCanvasResolution(RESOLUTION_AUTO);
function resize(){const h=Math.min(640,Math.floor(innerHeight*.65));canvas.style.height=h+'px';app.resizeCanvas(innerWidth,h);}addEventListener('resize',resize);resize();
const config=await(await fetch('/review-config.json')).json(),side=config.leftSide?-1:1;
const cameras=[],dirs=[new Vec3(0,0,3),new Vec3(3*side,0,0),new Vec3(1.5*side,.12,3)];let face=false,playing=false;
for(let i=0;i<3;i++){const c=new Entity(['Front','Side','3Q'][i]);c.addComponent('camera',{projection:PROJECTION_ORTHOGRAPHIC,orthoHeight:.61,clearColor:new Color(.87,.89,.85),rect:new Vec4(i/3,0,1/3,1),priority:i});app.root.addChild(c);cameras.push(c);}
function aim(){cameras.forEach((c,i)=>{const target=face?new Vec3(0,.68,.24):new Vec3(0,.5,0);c.setPosition(target.clone().add(dirs[i]));c.lookAt(target);c.camera.orthoHeight=face?.245:.65;});}aim();
for(const [i,rot] of [[0,[45,35,0]],[1,[35,160,0]]]){const e=new Entity('ReviewLight'+i);e.addComponent('light',{type:'directional',intensity:i?.45:1.1,color:new Color(1,1,1)});e.setEulerAngles(...rot);app.root.addChild(e);}
app.start();
const load=(url,type)=>new Promise((resolve,reject)=>app.assets.loadFromUrl(url,type,(e,a)=>e?reject(e):resolve(a)));
try{
 const asset=await load('/model.glb','container'),resource=asset.resource,entity=resource.instantiateRenderEntity();app.root.addChild(entity);
 const hasClip=resource.animations.length>0;
 if(!hasClip&&!config.mouthControls)throw Error('Missing bounded review clip');
 let layer={activeStateCurrentTime:0};
 if(hasClip){entity.addComponent('anim',{activate:true});entity.anim.assignAnimation('Review',resource.animations[0].resource);layer=entity.anim.baseLayer;layer.play('Review');entity.anim.speed=0;}
 else{document.querySelector('#play').disabled=true;slider.disabled=true;}
 const meshes=entity.findComponents('render').flatMap(c=>c.meshInstances),anchors=entity.find(n=>n.name.startsWith('ANCHOR_')),schedule=hasClip?await(await fetch('/schedule.json')).json():{cases:[]};
 slider.max=hasClip?resource.animations[0].resource.duration:0;
 const samples=[],errors=[];let tag='neutral',elapsed=0,previous='',mouthReview=null;
 if(config.mouthControls){const {installMouthReview}=await import('/mouth-review.mjs');mouthReview=installMouthReview({app,entity,onManual:()=>{playing=false;tag='direct-mouth';if(entity.anim)entity.anim.enabled=false;}});}
 const resumeClip=()=>{mouthReview?.stop();if(entity.anim)entity.anim.enabled=true;};
 const report=()=>({engine:version,scope:'Desktop WebGL2 bounded texture review; no general authoring solver or mobile certification',meshInstances:meshes.length,skinInstances:meshes.filter(m=>m.skinInstance).length,morphInstances:meshes.filter(m=>m.morphInstance).length,morphTargets:meshes.map(m=>m.morphInstance?.morph?.targets?.length??0),anchors:anchors.map(n=>n.name),materials:meshes.map(m=>({name:m.material.name,diffuseMapUv:m.material.diffuseMapUv,diffuseTexture:m.material.diffuseMap?{width:m.material.diffuseMap.width,height:m.material.diffuseMap.height}:null})),samples,errors,directMouth:mouthReview?.report(),human_visual_go:false});
 document.querySelector('#play').onclick=()=>{resumeClip();playing=!playing;};
 slider.oninput=()=>{resumeClip();playing=false;tag='manual';layer.activeStateCurrentTime=Number(slider.value);};
 document.querySelector('#face').onclick=()=>{face=!face;aim();};
 document.querySelector('#save').onclick=async()=>{await fetch('/evidence',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(report())});status.textContent+='\nSaved evidence';};
 for(const item of [{name:'neutral',peak_seconds:0},...schedule.cases]){const b=document.createElement('button');b.textContent=item.name;b.onclick=()=>{resumeClip();playing=false;tag=item.name;layer.activeStateCurrentTime=item.peak_seconds;};document.querySelector('#cases').appendChild(b);}
 app.on('update',dt=>{if(entity.anim)entity.anim.speed=playing?1:0;elapsed+=dt;});
 app.on('frameend',()=>{
  const time=layer.activeStateCurrentTime;slider.value=time;const key=tag+':'+time.toFixed(3);
  if(key!==previous&&samples.length<1000){previous=key;const positions={};for(const name of ['DEF_head','DEF_wing_outer.L','DEF_wing_outer.R','DEF_tail_02']){const n=entity.findByName(name),p=n?.getPosition();if(p)positions[name]=[p.x,p.y,p.z];}
   const anchorPositions=anchors.map(n=>{const p=n.getPosition();return [p.x,p.y,p.z];});const weights=meshes[0]?.morphInstance?.morph.targets.map((_,i)=>meshes[0].morphInstance.getWeight(i));
   const row={tag,time,positions,anchorPositions,weights};if(!Number.isFinite(time)||anchorPositions.flat().some(x=>!Number.isFinite(x)))errors.push('nonfinite runtime state');samples.push(row);
  }
  status.textContent=`Engine ${version} | ${meshes.length} materials / ${meshes.filter(m=>m.skinInstance).length} skins / ${anchors.length} anchors | ${tag} ${time.toFixed(3)}s\n${config.appearanceStatus||'HOLD: Human appearance, horn boundary/colour and clover placement require review.'}`;
 });
}catch(e){status.textContent=e.stack;throw e;}
