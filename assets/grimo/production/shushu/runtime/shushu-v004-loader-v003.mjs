// Production-facing loader for the separate v003 candidate, PlayCanvas 2.22.2.
// No diagnostic viewer, Blender, camera, timeline-frame or DOM dependency.
// The caller chooses and plays separately authored/baked clips on `entity`.
import {installShushuDeformation} from './shushu-v004-deformation-v003.mjs';
let candidateSequence=0;

// Re-evaluate purpose arbitration after animation blending. Blending two baked
// endpoint clips alone would omit their pose-space midpoint volume correction.
// Body/face animation remains caller-owned; pass the matching current Seat.
function installPawControls({pc,app,entity,deformation,streams}) {
 const clamp=x=>Math.max(0,Math.min(1,Number(x)||0));
 const paws=streams.filter(a=>a.name.startsWith('ShushuStatic_Paw_')).map(a=>{
  const side=a.name.endsWith('_L')?'L':'R',anchor=entity.findByName('ANCHOR_Hold.'+side);
  const keys=a.names.map((name,index)=>{const m=/^PoseSpace\.(.+)\.(\d+)\.S([\d.]+)\.W(-?[\d.]+)$/.exec(name);if(!m)throw Error('Unknown Paw target '+name);return {index,mode:m[1],t:Number(m[2])/1000,seat:Number(m[3]),wrist:Number(m[4])};});
  return {a,side,anchor,keys,index:-1};
 });
 const forward=new pc.Vec3(),point=new pc.Vec3();
 function gap(){entity.getWorldTransform().transformVector(new pc.Vec3(0,0,.031),forward);}
 deformation.update(true);gap();
 for(const p of paws){
  const rest=p.anchor.getPosition().clone().sub(forward),pos=p.a.surface.p;let best=Infinity;
  for(let i=0;i<pos.length/3;i++){const d=Math.hypot(pos[i*3]-rest.x,pos[i*3+1]-rest.y,pos[i*3+2]-rest.z);if(d<best){best=d;p.index=i;}}
  if(best>1e-4)throw Error('Cannot calibrate neutral Hold surface '+p.side+' / '+best);
 }
 let current=null;const times=[];
 function weights(){
  if(!current)return;
  const started=performance.now(),seat=clamp(current.Seat);
  for(const p of paws){
   const h=clamp(current['Hold.'+p.side]),c=(1-h)*clamp(current['SelfContact.'+p.side]),o=(1-h)*(1-clamp(current['SelfContact.'+p.side]))*clamp(current['Offer.'+p.side]),amount=h+c+o;
   const purpose={Hold:h,SelfContact:c,Offer:o},wrist=Math.max(-1,Math.min(1,Number(current['Wrist.'+p.side])||0));
   for(const k of p.keys){
    const pair=k.mode.split('~');let a=k.mode==='NeutralWrist'?1:pair.length===2?4*purpose[pair[0]]*purpose[pair[1]]/Math.max(.000001,amount*amount):purpose[k.mode]/Math.max(.000001,amount);
    const weight=a*Math.max(0,1-Math.abs(amount-k.t)*8)*Math.max(0,1-Math.abs(seat-k.seat)*2)*Math.max(0,1-Math.abs(wrist-k.wrist));p.a.morph.setWeight(k.index,weight);
   }
  }
  times.push(performance.now()-started);if(times.length>30000)times.shift();
 }
 function anchors(){if(!current)return;if(!deformation.enabled)deformation.update(true);gap();for(const p of paws){const pos=p.a.surface.p,i=p.index*3;point.set(pos[i]+forward.x,pos[i+1]+forward.y,pos[i+2]+forward.z);p.anchor.setPosition(point);}}
 // Deformation's prerender listener runs first and computes these same weights'
 // current surface. Anchor updates then follow that evaluated surface.
 // Application update fires after systems.animationUpdate in Engine 2.22.2.
 // `postupdate` is not an Application event; using it would silently leave
 // animated endpoint weights in charge after a caller supplied new purposes.
 app.on('update',weights);app.on('prerender',anchors);
 return {set(values,{defer=false}={}){current=values?{...values}:null;if(!defer)weights();},times,get enabled(){return current!==null;},scope:'Bounded purpose/Wrist/Seat interpolation and Hold anchors; caller owns body/face pose and Seat correspondence; direct old arm FK clips are not supported.',dispose(){app.off('update',weights);app.off('prerender',anchors);current=null;}};
}

export function decodeShushuGlb(bytes) {
 const dv=new DataView(bytes);
 if(dv.getUint32(0,true)!==0x46546c67||dv.getUint32(4,true)!==2||dv.getUint32(8,true)!==bytes.byteLength)throw Error('Expected complete glTF 2 GLB');
 let json,bin;
 for(let offset=12;offset<bytes.byteLength;){const length=dv.getUint32(offset,true),type=dv.getUint32(offset+4,true);if(type===0x4e4f534a)json=JSON.parse(new TextDecoder().decode(new Uint8Array(bytes,offset+8,length)));if(type===0x004e4942)bin=offset+8;offset+=length+8;}
 if(!json||bin===undefined||json.buffers.length!==1||json.buffers[0].uri)throw Error('Expected embedded candidate GLB');
 const dimensions={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16},sizes={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4},cache=new Map();
 const raw=(offset,type)=>{switch(type){case 5120:return dv.getInt8(offset);case 5121:return dv.getUint8(offset);case 5122:return dv.getInt16(offset,true);case 5123:return dv.getUint16(offset,true);case 5125:return dv.getUint32(offset,true);case 5126:return dv.getFloat32(offset,true);default:throw Error('Unsupported component type '+type);}};
 function access(id){
  if(cache.has(id))return cache.get(id);
  const a=json.accessors[id],dim=dimensions[a.type],size=sizes[a.componentType];if(!dim||!size)throw Error('Unsupported candidate accessor');
  const values=new Float32Array(a.count*dim),value=offset=>{const v=raw(offset,a.componentType);if(!a.normalized||a.componentType===5126)return v;const max={5120:127,5121:255,5122:32767,5123:65535,5125:4294967295}[a.componentType];return Math.max(-1,v/max);};
  if(a.bufferView!==undefined){const b=json.bufferViews[a.bufferView],base=bin+(b.byteOffset||0)+(a.byteOffset||0),stride=b.byteStride||size*dim;for(let i=0;i<a.count;i++)for(let k=0;k<dim;k++)values[i*dim+k]=value(base+i*stride+k*size);}
  if(a.sparse){const s=a.sparse,indices=json.bufferViews[s.indices.bufferView],data=json.bufferViews[s.values.bufferView];for(let i=0;i<s.count;i++){const n=raw(bin+(indices.byteOffset||0)+(s.indices.byteOffset||0)+i*sizes[s.indices.componentType],s.indices.componentType);for(let k=0;k<dim;k++)values[n*dim+k]=value(bin+(data.byteOffset||0)+(s.values.byteOffset||0)+(i*dim+k)*size);}}
  cache.set(id,values);return values;
 }
 return {json,access};
}

export async function loadShushuCandidate({pc,app,url,normalsEnabled=true}) {
 const response=await fetch(url);if(!response.ok)throw Error('Shushu GLB HTTP '+response.status);
 // The container handler caches by URL. Give each owned parse a distinct key:
 // unloading it must never destroy a resource used by another instance/asset.
 // `contents` reuses the one download; the cache key is not fetched again.
 const cacheUrl=url+(url.includes('?')?'&':'?')+'shushuOwnedParse='+(++candidateSequence);
 const bytes=await response.arrayBuffer(),{json,access}=decodeShushuGlb(bytes),asset=new pc.Asset('Shushu v004 v003 candidate','container',{url:cacheUrl,contents:bytes});app.assets.add(asset);
 let entity,deformation,pawControls;
 try{
  await new Promise((resolve,reject)=>{asset.once('load',resolve);asset.once('error',reject);app.assets.load(asset);});
  entity=asset.resource.instantiateRenderEntity();app.root.addChild(entity);
  const meshes=entity.findComponents('render').flatMap(c=>c.meshInstances),streams=[];
  for(const m of json.meshes){
   if(m.primitives.length!==1)throw Error('Candidate contract requires one primitive per mesh');
   const p=m.primitives[0],a=p.attributes;if(a.WEIGHTS_1===undefined&&!m.name.startsWith('ShushuStatic_Paw_'))continue;
   const mi=meshes.find(x=>x.node.name===m.name);if(!mi?.skinInstance||!mi.morphInstance)throw Error('Missing candidate skin/morph '+m.name);
   const zero=new Float32Array(access(a.POSITION).length/3*4);
   streams.push({name:m.name,names:m.extras?.targetNames||[],mi,skin:mi.skinInstance,morph:mi.morphInstance,indices:access(p.indices),pos:access(a.POSITION),normal:access(a.NORMAL),j0:access(a.JOINTS_0),j1:a.JOINTS_1===undefined?zero:access(a.JOINTS_1),w0:access(a.WEIGHTS_0),w1:a.WEIGHTS_1===undefined?zero:access(a.WEIGHTS_1),targets:(p.targets||[]).map(t=>({p:t.POSITION===undefined?null:access(t.POSITION),n:t.NORMAL===undefined?null:access(t.NORMAL)}))});
  }
  if(streams.length!==3)throw Error('Expected the candidate Torso compatibility and two Paw normal streams');
  deformation=installShushuDeformation({pc,app,streams,normalsEnabled});
  pawControls=installPawControls({pc,app,entity,deformation,streams});
  // Parsing above and the container handler shared one download.
  asset.file.contents=null;
  let disposed=false;
  return {entity,resource:asset.resource,deformation,pawControls,asset,dispose(){if(disposed)return;disposed=true;pawControls.dispose();deformation.dispose();entity.destroy();asset.unload();app.assets.remove(asset);}};
 }catch(error){pawControls?.dispose();deformation?.dispose();entity?.destroy();asset.unload();app.assets.remove(asset);throw error;}
}
