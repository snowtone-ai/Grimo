import {VertexBuffer,VertexFormat,VertexIterator,TYPE_FLOAT32,SHADERLANGUAGE_GLSL,ShaderChunks} from '/node_modules/playcanvas/build/playcanvas.mjs';

// Only this diagnostic viewer uses the adapter. The GLB, skin/rest, Morphs and Anchors stay intact.
export async function installCompat({qa,affected,Mat4,transform,norm,dist,mode,light,app}) {
 const originalView=qa.view;qa.view=view=>{document.querySelector('#view').value=view;return originalView(view)};
 const optimized=mode==='optimized'?await (await fetch('./optimized-weights.json')).json():null;
 const skinChunk=ShaderChunks.get(app.graphicsDevice,SHADERLANGUAGE_GLSL).get('skinVS');
 const adapter=[];
 if(mode==='local8')for(const a of affected) {
  const mesh=a.mi.mesh,old=mesh.vertexBuffer,format=old.format;
  if(format.elements.some(e=>['TEXCOORD6','TEXCOORD7'].includes(e.name)))throw Error('Extra attribute collision');
  const desc=format.elements.map(e=>({semantic:e.name,components:e.numComponents,type:e.dataType,normalize:e.normalize,asInt:e.asInt}));
  desc.push({semantic:'TEXCOORD6',components:4,type:TYPE_FLOAT32},{semantic:'TEXCOORD7',components:4,type:TYPE_FLOAT32});
  const vb=new VertexBuffer(app.graphicsDevice,new VertexFormat(app.graphicsDevice,desc),old.numVertices);
  const src=new VertexIterator(old),dst=new VertexIterator(vb),streams={};
  for(const e of format.elements){const data=[];src.readData(e.name,data);dst.writeData(e.name,data,old.numVertices);streams[e.name]=data;}
  dst.writeData('TEXCOORD6',a.j1,old.numVertices);dst.writeData('TEXCOORD7',a.w1,old.numVertices);dst.end();
  mesh.vertexBuffer=vb;mesh.updateRenderStates();
  // Exact copy check includes Morph's vertex ID if present in this buffer.
  const check=new VertexIterator(vb);for(const e of format.elements){const data=[];check.readData(e.name,data);if(data.some((v,i)=>v!==streams[e.name][i]))throw Error('Base attribute changed '+e.name);}
  const material=a.mi.material.clone();material.shaderChunksVersion='2.22';
  material.setAttribute('compat_joint1','TEXCOORD6');material.setAttribute('compat_weight1','TEXCOORD7');
  const chunk=skinChunk.replace('mat4 getSkinMatrix(', 'mat4 getSkinMatrix4(')+`
attribute vec4 compat_joint1;
attribute vec4 compat_weight1;
mat4 getSkinMatrix(const in vec4 indicesFloat, const in vec4 weights) {
    return getSkinMatrix4(indicesFloat, weights) + getSkinMatrix4(compat_joint1, compat_weight1);
}`;
  material.getShaderChunks(SHADERLANGUAGE_GLSL).set('skinVS',chunk);material.update();a.mi.material=material;
  adapter.push({mesh:a.name,vertices:old.numVertices,addedVBBytes:vb.numBytes-old.numBytes,baseStreamsExact:true});
  old.destroy();
 }
 const rows=affected.flatMap(a=>Array.from({length:a.pos.length/3},(_,i)=>({a,i})).filter(({i})=>a.w1.subarray(i*4,i*4+4).some(w=>w>0)));
 function evaluated(a,i) {
  const p=Array.from(a.pos.subarray(i*3,i*3+3)),n=Array.from(a.normal.subarray(i*3,i*3+3));
  for(let t=0;t<a.targets.length;t++){const w=a.morph.getWeight(t),target=a.targets[t];if(!w)continue;for(let c=0;c<3;c++){if(target.p)p[c]+=w*target.p[i*3+c];if(target.n)n[c]+=w*target.n[i*3+c];}}
  return {p,n};
 }
 function matrices(a){return a.skin.bones.map((b,i)=>new Mat4().mul2(b.getWorldTransform(),a.skin.skin.inverseBindPose[i]).data);}
 function influences(a,i){return Array.from({length:8},(_,k)=>({id:(k<4?a.j0:a.j1)[i*4+k%4],w:(k<4?a.w0:a.w1)[i*4+k%4]}));}
 function contributions(a,i,mats,local=null) {
  const {p,n}=local||evaluated(a,i),inf=influences(a,i),points=inf.map(x=>transform(mats[x.id],p)),normals=inf.map(x=>transform(mats[x.id],n,0));
  const full=[0,0,0],normal=[0,0,0];for(let k=0;k<8;k++)for(let c=0;c<3;c++){full[c]+=inf[k].w*points[k][c];normal[c]+=inf[k].w*normals[k][c];}
  return {inf,points,normals,full,normal};
 }
 // Diagnostic oracle export; never replaces authored normals or geometry.
 qa.surface=frame=>{qa.sample(frame);return {frame,meshes:affected.map(a=>{const mats=matrices(a),p=[],n=[];for(let i=0;i<a.pos.length/3;i++){const c=contributions(a,i,mats);p.push(c.full);n.push(norm(c.normal));}return {name:a.name,position:p,normal:n};})};};
 qa.fitData=frames=>{
  const entries=rows.map(({a,i})=>({mesh:a.name,vertex:i,influences:influences(a,i),gram:Array(64).fill(0)}));
  for(const frame of frames){qa.sample(frame);const mats=new Map(affected.map(a=>[a,matrices(a)]));rows.forEach(({a,i},r)=>{
   const {points,normals,full,normal}=contributions(a,i,mats.get(a)),scale=.05/Math.max(Math.hypot(...normal),1e-8);
   const d=points.map((p,k)=>[...p.map((v,c)=>v-full[c]),...normals[k].map((v,c)=>(v-normal[c])*scale)]);
   for(let k=0;k<8;k++)for(let l=0;l<8;l++)entries[r].gram[k*8+l]+=d[k].reduce((s,v,c)=>s+v*d[l][c],0);
  });}return {frames,normalScaleH:.05,entries};
 };
 qa.compatAudit=(frame,all=false)=>{
  qa.sample(frame);const result=[];
  for(const a of affected){const mats=matrices(a);let positionMax=0,normalMax=0,squared=0,worst=-1;
   const opt=optimized?.meshes[a.name];
   for(let i=0;i<a.pos.length/3;i++){
    if(!all&&!a.w1.subarray(i*4,i*4+4).some(w=>w))continue;
    const {inf,points,normals,full,normal}=contributions(a,i,mats),p=[0,0,0],n=[0,0,0];
    const weights=mode==='local8'||mode==='full8'?inf.map(x=>x.w):mode==='optimized'?Array.from(opt.weights.slice(i*4,i*4+4)):inf.slice(0,4).map(x=>x.w/inf.slice(0,4).reduce((s,x)=>s+x.w,0));
    for(let k=0;k<weights.length;k++){let slot=k;if(mode==='optimized')slot=inf.findIndex(x=>x.id===opt.joints[i*4+k]);for(let c=0;c<3;c++){p[c]+=weights[k]*points[slot][c];n[c]+=weights[k]*normals[slot][c];}}
    const e=dist(p,full),angle=Math.acos(Math.max(-1,Math.min(1,norm(n).reduce((s,v,c)=>s+v*norm(normal)[c],0))))*180/Math.PI;
    if(e>positionMax){positionMax=e;worst=i;}normalMax=Math.max(normalMax,angle);squared+=e*e;
   }result.push({mesh:a.name,positionMax,normalMaxDeg:normalMax,worstVertex:worst,rmsOverAllVertices:Math.sqrt(squared/(a.pos.length/3))});
  }return {frame,meshes:result};
 };
 // CPU full-eight reference is rendered at each frame; animated reference is diagnostic, never benchmarked.
 if(mode==='full8'){app.on('update',()=>qa.skinAudit(true));document.querySelector('#play').disabled=false;}
 qa.shading=name=>{
  if(!qa.savedMaterials)qa.savedMaterials=qa.meshes.map(m=>m.material);
  qa.meshes.forEach((mi,i)=>{if(name==='lit'){mi.material=qa.savedMaterials[i];return;}
   const m=qa.savedMaterials[i].clone();m.useSkybox=false;m.metalness=0;m.useMetalness=true;m.diffuse.set(0,0,0);m.specular.set(0,0,0);m.emissive.set(1,1,1);m.emissiveMap=name==='unlit'?m.diffuseMap:null;m.diffuseMap=null;
   if(name==='normal')m.getShaderChunks(SHADERLANGUAGE_GLSL).set('litUserMainEndPS','gl_FragColor = vec4(normalize(vNormalW)*0.5+0.5, 1.0);');
   m.update();mi.material=m;
  });
 };
 qa.adapter=adapter;
 const gl=app.graphicsDevice.gl;
 qa.gpuCapture=async frame=>{
  qa.sample(frame);const captures=[],programs=new Map(),original=gl.drawElements;
  function capture(program,a){
   let p=programs.get(program);if(!p){p=gl.createProgram();for(const shader of gl.getAttachedShaders(program)){
    if(gl.getShaderParameter(shader,gl.SHADER_TYPE)===gl.VERTEX_SHADER){const copy=gl.createShader(gl.VERTEX_SHADER),source=gl.getShaderSource(shader).replace(/void main\s*\(/,'void compatOriginalMain(')+`\nout vec3 compatLocalP;\nout vec3 compatLocalN;\nvoid main(){compatOriginalMain();compatLocalP=getLocalPosition(vertex_position.xyz);compatLocalN=getLocalNormal(vertex_normal);}`;gl.shaderSource(copy,source);gl.compileShader(copy);if(!gl.getShaderParameter(copy,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(copy));gl.attachShader(p,copy);gl.deleteShader(copy);}else gl.attachShader(p,shader);
   }for(let i=0;i<gl.getProgramParameter(program,gl.ACTIVE_ATTRIBUTES);i++){const at=gl.getActiveAttrib(program,i);gl.bindAttribLocation(p,gl.getAttribLocation(program,at.name),at.name);}gl.transformFeedbackVaryings(p,['vPositionW','vNormalW','compatLocalP','compatLocalN'],gl.INTERLEAVED_ATTRIBS);gl.linkProgram(p);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(p));programs.set(program,p);}
   gl.useProgram(p);const nu=gl.getProgramParameter(program,gl.ACTIVE_UNIFORMS);
   for(let i=0;i<nu;i++){const u=gl.getActiveUniform(program,i),loc=gl.getUniformLocation(p,u.name);if(loc===null)continue;const v=gl.getUniform(program,gl.getUniformLocation(program,u.name));switch(u.type){case gl.FLOAT:gl.uniform1fv(loc,typeof v==='number'?[v]:v);break;case gl.FLOAT_VEC2:gl.uniform2fv(loc,v);break;case gl.FLOAT_VEC3:gl.uniform3fv(loc,v);break;case gl.FLOAT_VEC4:gl.uniform4fv(loc,v);break;case gl.FLOAT_MAT4:gl.uniformMatrix4fv(loc,false,v);break;case gl.FLOAT_MAT3:gl.uniformMatrix3fv(loc,false,v);break;case gl.INT:case gl.BOOL:case gl.SAMPLER_2D:case gl.INT_SAMPLER_2D:case gl.UNSIGNED_INT_SAMPLER_2D:case gl.SAMPLER_CUBE:case gl.SAMPLER_2D_SHADOW:gl.uniform1iv(loc,typeof v==='number'?[v]:v);break;default:throw Error('Unhandled GPU uniform '+u.name+' '+u.type);}}
   const count=a.mi.mesh.vertexBuffer.numVertices,buffer=gl.createBuffer(),tf=gl.createTransformFeedback(),oldTF=gl.getParameter(gl.TRANSFORM_FEEDBACK_BINDING),oldArray=gl.getParameter(gl.ARRAY_BUFFER_BINDING);
   gl.bindTransformFeedback(gl.TRANSFORM_FEEDBACK,tf);gl.bindBuffer(gl.TRANSFORM_FEEDBACK_BUFFER,buffer);gl.bufferData(gl.TRANSFORM_FEEDBACK_BUFFER,count*12*4,gl.STREAM_READ);gl.bindBufferBase(gl.TRANSFORM_FEEDBACK_BUFFER,0,buffer);gl.enable(gl.RASTERIZER_DISCARD);gl.beginTransformFeedback(gl.POINTS);gl.drawArrays(gl.POINTS,0,count);gl.endTransformFeedback();gl.disable(gl.RASTERIZER_DISCARD);
   const data=new Float32Array(count*12);gl.getBufferSubData(gl.TRANSFORM_FEEDBACK_BUFFER,0,data);const error=gl.getError();
   gl.bindBufferBase(gl.TRANSFORM_FEEDBACK_BUFFER,0,null);gl.bindTransformFeedback(gl.TRANSFORM_FEEDBACK,oldTF);gl.bindBuffer(gl.ARRAY_BUFFER,oldArray);gl.useProgram(program);gl.deleteTransformFeedback(tf);gl.deleteBuffer(buffer);
   const mats=matrices(a);let maxPosition=0,maxNormal=0,skinOnlyPosition=0,skinOnlyNormal=0,worst=-1;for(let i=0;i<count;i++){const contribution=contributions(a,i,mats),full=contribution.full,normal=qa.normalRepair?.enabled&&a.surface?Array.from(a.surface.n.subarray(i*3,i*3+3)):contribution.normal,p=Array.from(data.subarray(i*12,i*12+3)),n=Array.from(data.subarray(i*12+3,i*12+6)),local={p:Array.from(data.subarray(i*12+6,i*12+9)),n:Array.from(data.subarray(i*12+9,i*12+12))},matched=contributions(a,i,mats,local),e=dist(full,p),angle=(a,b)=>Math.acos(Math.max(-1,Math.min(1,norm(a).reduce((s,v,c)=>s+v*norm(b)[c],0))))*180/Math.PI;if(e>maxPosition){maxPosition=e;worst=i;}maxNormal=Math.max(maxNormal,angle(n,normal));skinOnlyPosition=Math.max(skinOnlyPosition,dist(p,matched.full));skinOnlyNormal=Math.max(skinOnlyNormal,angle(n,matched.normal));}
   captures.push({mesh:a.name,count,maxPosition,maxNormalDeg:maxNormal,skinOnlyPosition,skinOnlyNormalDeg:qa.normalRepair?.enabled&&a.surface?null:skinOnlyNormal,normalOracle:qa.normalRepair?.enabled&&a.surface?"current evaluated surface NORMAL stream":"exported morph/skin normal",worstVertex:worst,glError:error,method:'Transform feedback: actual material vertex shader with extra local P/N outputs; current draw VAO/uniforms/textures. CPU 8-weight oracle also receives captured GPU Morph P/N to isolate Skin.'});
  }
  gl.drawElements=function(...args){original.apply(this,args);try{const p=gl.getParameter(gl.CURRENT_PROGRAM),loc=gl.getAttribLocation(p,'vertex_boneWeights');if(loc<0)return;const vbo=gl.getVertexAttrib(loc,gl.VERTEX_ATTRIB_ARRAY_BUFFER_BINDING),a=affected.find(a=>a.mi.mesh.vertexBuffer.impl.bufferId===vbo||a.mi.mesh.vertexBuffer.impl._glBuffer===vbo);if(a&&!captures.some(c=>c.mesh===a.name))capture(p,a);}catch(e){captures.push({error:e.stack});}};
  try{await Promise.race([new Promise(r=>app.once('frameend',r)),new Promise(r=>setTimeout(r,5000))]);}finally{gl.drawElements=original;for(const p of programs.values())gl.deleteProgram(p);}
  return {frame,captures};
 };
 qa.gpuCapability={webgl2:!!gl.transformFeedbackVaryings,timerQuery:!!gl.getExtension('EXT_disjoint_timer_query_webgl2'),maxAttributes:gl.getParameter(gl.MAX_VERTEX_ATTRIBS)};
 qa.touchLog=[];document.querySelector('#play').addEventListener('pointerdown',e=>{const start=performance.now();requestAnimationFrame(()=>qa.touchLog.push({trusted:e.isTrusted,pointerType:e.pointerType,eventToRafMs:performance.now()-start,speed:qa.root.anim.speed}));});
}
