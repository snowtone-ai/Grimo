// Local normal evaluation for the two paws only. POSITION, skin, Morph weights,
// textures and bones stay on the established eight-weight GPU path.
import {VertexIterator,SHADERLANGUAGE_GLSL} from '/node_modules/playcanvas/build/playcanvas.mjs';
export function installSurfaceNormals({qa,affected,access,Mat4,app,enabled=true}) {
 const paws=affected.filter(a=>a.name.startsWith('ShushuStatic_Paw_'));
 const times=[];
 for(const a of paws){
  const count=a.pos.length/3,weld=new Int32Array(count),map=new Map();let groups=0;
  for(let i=0;i<count;i++){
   const key=Array.from(a.pos.subarray(i*3,i*3+3),x=>Math.round(x*1e6)).join(',');
   if(!map.has(key))map.set(key,groups++);weld[i]=map.get(key);
  }
  a.surface={weld,groups,indices:access(a.p.indices),p:new Float64Array(count*3),n:new Float32Array(count*3),sum:new Float64Array(groups*3),local:new Float64Array(count*3)};
  if(enabled){
   const material=a.mi.material.clone();material.shaderChunksVersion='2.22';
   material.getShaderChunks(SHADERLANGUAGE_GLSL).set('normalVS',`
mat3 dNormalMatrix;
vec3 getNormal() {
    dNormalMatrix = getNormalMatrix(dModelMatrix);
    return normalize(vertex_normal);
}`);
   material.update();a.mi.material=material;
  }
 }
 function compute(a){
  const s=a.surface,p=s.p,local=s.local,count=p.length/3;local.set(a.pos);
  for(let t=0;t<a.targets.length;t++){
   const w=a.morph.getWeight(t),delta=a.targets[t].p;if(!w||!delta)continue;
   for(let k=0;k<local.length;k++)local[k]+=w*delta[k];
  }
  const mats=a.skin.bones.map((b,i)=>new Mat4().mul2(b.getWorldTransform(),a.skin.skin.inverseBindPose[i]).data);
  p.fill(0);
  for(let i=0;i<count;i++){
   const x=local[i*3],y=local[i*3+1],z=local[i*3+2];
   for(let k=0;k<8;k++){
    const w=(k<4?a.w0:a.w1)[i*4+k%4];if(!w)continue;
    const m=mats[(k<4?a.j0:a.j1)[i*4+k%4]];
    p[i*3]+=w*(m[0]*x+m[4]*y+m[8]*z+m[12]);
    p[i*3+1]+=w*(m[1]*x+m[5]*y+m[9]*z+m[13]);
    p[i*3+2]+=w*(m[2]*x+m[6]*y+m[10]*z+m[14]);
   }
  }
  s.sum.fill(0);const ix=s.indices;
  for(let f=0;f<ix.length;f+=3){
   const ia=ix[f],ib=ix[f+1],ic=ix[f+2],a3=ia*3,b3=ib*3,c3=ic*3;
   const ux=p[b3]-p[a3],uy=p[b3+1]-p[a3+1],uz=p[b3+2]-p[a3+2],vx=p[c3]-p[a3],vy=p[c3+1]-p[a3+1],vz=p[c3+2]-p[a3+2];
   const nx=uy*vz-uz*vy,ny=uz*vx-ux*vz,nz=ux*vy-uy*vx,area=Math.hypot(nx,ny,nz);if(area<1e-18)continue;
   for(let corner=0;corner<3;corner++){
    const i=ix[f+corner],j=ix[f+(corner+1)%3],k=ix[f+(corner+2)%3],i3=i*3,j3=j*3,k3=k*3;
    const ax=p[j3]-p[i3],ay=p[j3+1]-p[i3+1],az=p[j3+2]-p[i3+2],bx=p[k3]-p[i3],by=p[k3+1]-p[i3+1],bz=p[k3+2]-p[i3+2];
    const angle=Math.atan2(area,ax*bx+ay*by+az*bz),g=s.weld[i]*3,scale=angle/area;
    s.sum[g]+=nx*scale;s.sum[g+1]+=ny*scale;s.sum[g+2]+=nz*scale;
   }
  }
  for(let i=0;i<count;i++){
   const g=s.weld[i]*3,len=Math.hypot(s.sum[g],s.sum[g+1],s.sum[g+2]);
   if(len<1e-12){
    // Fully closed mouth intentionally collapses some interior faces. They
    // have no surface normal; retain the skinned Basis normal for those only.
    let x=0,y=0,z=0;const nx=a.normal[i*3],ny=a.normal[i*3+1],nz=a.normal[i*3+2];
    for(let k=0;k<8;k++){const w=(k<4?a.w0:a.w1)[i*4+k%4];if(!w)continue;const m=mats[(k<4?a.j0:a.j1)[i*4+k%4]];x+=w*(m[0]*nx+m[4]*ny+m[8]*nz);y+=w*(m[1]*nx+m[5]*ny+m[9]*nz);z+=w*(m[2]*nx+m[6]*ny+m[10]*nz);}
    const d=Math.hypot(x,y,z)||1;s.n[i*3]=x/d;s.n[i*3+1]=y/d;s.n[i*3+2]=z/d;continue;
   }
   for(let c=0;c<3;c++)s.n[i*3+c]=s.sum[g+c]/len;
  }
 }
 function update(){
  const start=performance.now();
  for(const a of paws){
   compute(a);
   if(enabled){const it=new VertexIterator(a.mi.mesh.vertexBuffer);it.writeData('NORMAL',a.surface.n,a.surface.n.length/3);it.end();}
  }
  times.push(performance.now()-start);if(times.length>30000)times.shift();
 }
 if(enabled)app.on('prerender',update);
 qa.surfaceNormals=frame=>{
  qa.sample(frame);for(const a of paws)compute(a);
  return {frame,meshes:paws.map(a=>({name:a.name,position:Array.from(a.surface.p),normal:Array.from(a.surface.n)}))};
 };
 qa.normalRepair={enabled,scope:paws.map(a=>({name:a.name,vertices:a.pos.length/3,weldedVertices:a.surface.groups,triangles:a.surface.indices.length/3})),method:'Angle weighted normals of current full-eight deformed surface; UV split vertices welded by 1e-6 rest position. Upload NORMAL only, world-space normalVS on two cloned paw materials.',times};
}
