// Candidate production companion for PlayCanvas 2.22.2 / WebGL2. No DOM, qa,
// camera, diagnostic-frame or Blender-driver dependency. Caller owns the meshes.
// streams are decoded glTF POSITION/NORMAL/JOINTS_0,1/WEIGHTS_0,1 and Morph data,
// plus {mi, skin, morph, indices}. Keep this contract with the candidate GLB.
export function installShushuDeformation({pc, app, streams, normalsEnabled=true}) {
 const {VertexBuffer,VertexFormat,VertexIterator,TYPE_FLOAT32,SHADERLANGUAGE_GLSL,ShaderChunks,Mat4}=pc;
 const skinChunk=ShaderChunks.get(app.graphicsDevice,SHADERLANGUAGE_GLSL).get('skinVS');
 const owned=[],paws=[],times=[];
 for(const a of streams){
  const originalMesh=a.mi.mesh,originalMaterial=a.mi.material,old=originalMesh.vertexBuffer,format=old.format;
  if(format.elements.some(e=>['TEXCOORD6','TEXCOORD7'].includes(e.name)))throw Error('8-weight stream collision');
  const desc=format.elements.map(e=>({semantic:e.name,components:e.numComponents,type:e.dataType,normalize:e.normalize,asInt:e.asInt}));
  desc.push({semantic:'TEXCOORD6',components:4,type:TYPE_FLOAT32},{semantic:'TEXCOORD7',components:4,type:TYPE_FLOAT32});
  const vb=new VertexBuffer(app.graphicsDevice,new VertexFormat(app.graphicsDevice,desc),old.numVertices),src=new VertexIterator(old),dst=new VertexIterator(vb);
  for(const e of format.elements){const data=[];src.readData(e.name,data);dst.writeData(e.name,data,old.numVertices);}
  src.end();dst.writeData('TEXCOORD6',a.j1,old.numVertices);dst.writeData('TEXCOORD7',a.w1,old.numVertices);dst.end();
  // Asset resources can be instantiated more than once. Own the complete mesh
  // and buffers so installing or disposing one character never edits its peers.
  const mesh=new pc.Mesh(app.graphicsDevice);mesh.vertexBuffer=vb;
  mesh.indexBuffer=originalMesh.indexBuffer.map(b=>b?new pc.IndexBuffer(app.graphicsDevice,b.format,b.numIndices,b.usage,b.lock().slice(0)):null);
  mesh.primitive=originalMesh.primitive.map(p=>({...p}));mesh.skin=originalMesh.skin;mesh.morph=originalMesh.morph;mesh.aabb=originalMesh.aabb.clone();
  mesh.boneAabb=originalMesh.boneAabb?.map(b=>b.clone());mesh.boneUsed=originalMesh.boneUsed?.slice();
  mesh.updateRenderStates();a.mi.mesh=mesh;
  const material=originalMaterial.clone();material.shaderChunksVersion='2.22';material.setAttribute('compat_joint1','TEXCOORD6');material.setAttribute('compat_weight1','TEXCOORD7');
  material.getShaderChunks(SHADERLANGUAGE_GLSL).set('skinVS',skinChunk.replace('mat4 getSkinMatrix(', 'mat4 getSkinMatrix4(')+`
attribute vec4 compat_joint1;
attribute vec4 compat_weight1;
mat4 getSkinMatrix(const in vec4 indicesFloat, const in vec4 weights) {
 return getSkinMatrix4(indicesFloat,weights)+getSkinMatrix4(compat_joint1,compat_weight1);
}`);
  if(a.name.startsWith('ShushuStatic_Paw_')){
   const count=a.pos.length/3,weld=new Int32Array(count),map=new Map();let groups=0;
   for(let i=0;i<count;i++){const key=Array.from(a.pos.subarray(i*3,i*3+3),x=>Math.round(x*1e6)).join(',');if(!map.has(key))map.set(key,groups++);weld[i]=map.get(key);}
   a.surface={weld,groups,indices:a.indices,p:new Float64Array(count*3),n:new Float32Array(count*3),sum:new Float64Array(groups*3),local:new Float64Array(count*3),mats:a.skin.bones.map(()=>new Mat4())};paws.push(a);
   if(normalsEnabled)material.getShaderChunks(SHADERLANGUAGE_GLSL).set('normalVS',`
mat3 dNormalMatrix;
vec3 getNormal(){dNormalMatrix=getNormalMatrix(dModelMatrix);return normalize(vertex_normal);}`);
  }
  material.update();a.mi.material=material;owned.push({a,mesh,originalMesh,material,originalMaterial});
 }
 function compute(a){
  const s=a.surface,p=s.p,local=s.local,count=p.length/3;local.set(a.pos);
  for(let t=0;t<a.targets.length;t++){const w=a.morph.getWeight(t),d=a.targets[t].p;if(!w||!d)continue;for(let k=0;k<local.length;k++)local[k]+=w*d[k];}
  for(let j=0;j<s.mats.length;j++)s.mats[j].mul2(a.skin.bones[j].getWorldTransform(),a.skin.skin.inverseBindPose[j]);
  p.fill(0);
  for(let i=0;i<count;i++){const i3=i*3,x=local[i3],y=local[i3+1],z=local[i3+2];for(let k=0;k<8;k++){const offset=i*4+k%4,w=(k<4?a.w0:a.w1)[offset];if(!w)continue;const m=s.mats[(k<4?a.j0:a.j1)[offset]].data;p[i3]+=w*(m[0]*x+m[4]*y+m[8]*z+m[12]);p[i3+1]+=w*(m[1]*x+m[5]*y+m[9]*z+m[13]);p[i3+2]+=w*(m[2]*x+m[6]*y+m[10]*z+m[14]);}}
  s.sum.fill(0);const ix=s.indices,sum=s.sum;
  for(let f=0;f<ix.length;f+=3){
   const ia=ix[f],ib=ix[f+1],ic=ix[f+2],a3=ia*3,b3=ib*3,c3=ic*3;
   const ux=p[b3]-p[a3],uy=p[b3+1]-p[a3+1],uz=p[b3+2]-p[a3+2],vx=p[c3]-p[a3],vy=p[c3+1]-p[a3+1],vz=p[c3+2]-p[a3+2];
   const nx=uy*vz-uz*vy,ny=uz*vx-ux*vz,nz=ux*vy-uy*vx,area=Math.hypot(nx,ny,nz);if(area<1e-18)continue;
   const dot=ux*vx+uy*vy+uz*vz,A=Math.atan2(area,dot),B=Math.atan2(area,ux*ux+uy*uy+uz*uz-dot),C=Math.max(0,Math.PI-A-B),inv=1/area;
   const ga=s.weld[ia]*3,gb=s.weld[ib]*3,gc=s.weld[ic]*3;
   sum[ga]+=nx*A*inv;sum[ga+1]+=ny*A*inv;sum[ga+2]+=nz*A*inv;
   sum[gb]+=nx*B*inv;sum[gb+1]+=ny*B*inv;sum[gb+2]+=nz*B*inv;
   sum[gc]+=nx*C*inv;sum[gc+1]+=ny*C*inv;sum[gc+2]+=nz*C*inv;
  }
  for(let i=0;i<count;i++){
   const g=s.weld[i]*3;let x=sum[g],y=sum[g+1],z=sum[g+2],len=Math.hypot(x,y,z);
   if(len<1e-12){x=y=z=0;const nx=a.normal[i*3],ny=a.normal[i*3+1],nz=a.normal[i*3+2];for(let k=0;k<8;k++){const offset=i*4+k%4,w=(k<4?a.w0:a.w1)[offset];if(!w)continue;const m=s.mats[(k<4?a.j0:a.j1)[offset]].data;x+=w*(m[0]*nx+m[4]*ny+m[8]*nz);y+=w*(m[1]*nx+m[5]*ny+m[9]*nz);z+=w*(m[2]*nx+m[6]*ny+m[10]*nz);}len=Math.hypot(x,y,z)||1;}
   s.n[i*3]=x/len;s.n[i*3+1]=y/len;s.n[i*3+2]=z/len;
  }
 }
 function update(force=false){const start=performance.now();for(const a of paws){compute(a);if(normalsEnabled){const it=new VertexIterator(a.mi.mesh.vertexBuffer);it.writeData('NORMAL',a.surface.n,a.surface.n.length/3);it.end();}}times.push(performance.now()-start);if(times.length>30000)times.shift();}
 const prerender=()=>update();if(normalsEnabled)app.on('prerender',prerender);
 let disposed=false;
 return {update,streams:paws,times,enabled:normalsEnabled,scope:paws.map(a=>({name:a.name,vertices:a.pos.length/3,triangles:a.indices.length/3})),method:'Exact current full-eight surface angle normals; two atan2 per triangle, reusable bone matrices; world NORMAL on owned paw meshes and materials.',dispose(){if(disposed)return;disposed=true;app.off('prerender',prerender);for(const o of owned){o.a.mi.mesh=o.originalMesh;o.a.mi.material=o.originalMaterial;o.mesh.destroy();o.material.destroy();}}};
}
