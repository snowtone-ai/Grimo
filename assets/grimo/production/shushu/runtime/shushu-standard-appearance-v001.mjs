// Independent, removable default equipment for the approved v004 body.
// All assets are owned per character; no source geometry/skin/morph is edited.
let sequence=0;
export async function installShushuStandardAppearance({pc,app,entity,flowerUrl,padsUrl,readAsset,signal}) {
 const assets=[];let flower,anchor,torso,material,original,disposed=false;
 async function load(name,type,url,data={}) {
  // Prevent another instance's unload from invalidating this one's resources.
  const bytes=await readAsset(url),contents=type==='container'?bytes:new Blob([bytes],{type:'image/png'});
  let ownedUrl=url+(url.includes('?')?'&':'?')+'shushuEquipment='+(++sequence),objectUrl;
  if(type==='texture'){objectUrl=URL.createObjectURL(contents);ownedUrl=objectUrl;}
  const asset=new pc.Asset(name,type,{url:ownedUrl,...(type==='container'?{contents}:{}),...(type==='texture'?{filename:'shushu-hind-sole-pads-v001.png'}:{})},data);assets.push(asset);app.assets.add(asset);
  try{await new Promise((resolve,reject)=>{asset.once('load',resolve);asset.once('error',reject);app.assets.load(asset);});signal.throwIfAborted();asset.file.contents=null;return asset;}finally{if(objectUrl)URL.revokeObjectURL(objectUrl);}
 }
 function dispose(){
  if(disposed)return;disposed=true;
  if(torso&&material){torso.material=original;material.destroy();}
  anchor?.destroy();for(const asset of assets){asset.unload();app.assets.remove(asset);}
 }
 try{
  const head=entity.findByName('mixamorig:Head');if(!head)throw Error('Standard appearance requires v004 Head');
  torso=entity.findComponents('render').flatMap(c=>c.meshInstances).find(m=>m.node.name==='ShushuStatic_Torso');if(!torso)throw Error('Missing v004 Torso');
  const item=await load('Shushu two-blossom head item','container',flowerUrl);
  flower=item.resource.instantiateRenderEntity();
  // The item was authored in the same neutral coordinate frame as the body.
  // Put a real local anchor at its crown mount; then preserve the item pose.
  const crown=new pc.Mat4().setTRS(new pc.Vec3(.08,.916,.105),new pc.Quat(),pc.Vec3.ONE);
  const inverseHead=new pc.Mat4().copy(head.getWorldTransform()).invert();
  const local=new pc.Mat4().mul2(inverseHead,crown);
  anchor=new pc.Entity('ANCHOR_HeadFlower.v001');head.addChild(anchor);
  anchor.setLocalPosition(local.getTranslation());anchor.setLocalRotation(new pc.Quat().setFromMat4(local));anchor.setLocalScale(local.getScale());
  const itemLocal=new pc.Mat4().mul2(new pc.Mat4().copy(crown).invert(),flower.getWorldTransform());
  anchor.addChild(flower);flower.setLocalPosition(itemLocal.getTranslation());flower.setLocalRotation(new pc.Quat().setFromMat4(itemLocal));flower.setLocalScale(itemLocal.getScale());
  original=torso.material;
  const pads=await load('Shushu bilateral hind sole pads','texture',padsUrl,{flipY:original.diffuseMap.flipY,srgb:true,mipmaps:true});
  material=original.clone();material.name='ShushuStandard_HindSoles_v001';material.diffuseMap=pads.resource;material.update();torso.material=material;
  let enabled=true;
  return {anchor,flower,assets,setEnabled(value){if(disposed)return;enabled=!!value;anchor.enabled=enabled;torso.material=enabled?material:original;},get enabled(){return enabled;},dispose,scope:'Two principal five-petal sakura + small central overlap + five leaves, one Head-local item; existing hind soles only: one central + three upper pads each. Human PENDING; phone UNKNOWN.'};
 }catch(error){flower?.destroy();dispose();throw error;}
}
