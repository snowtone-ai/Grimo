"""Measured UV diagnostics and temporary atlas swatches, never production texture."""
from pathlib import Path
import json, math
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'artifacts/pino-pretexture-v005'
OUT=ROOT/'docs/production/pino/evidence/pretexture-reliability-v005'
OUT.mkdir(parents=True,exist_ok=True)
SIZE=4096
def dump(n,d): (OUT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8', newline='\n')
def raster(uv,size=SIZE):
    q=uv*size-.5
    lo=np.maximum(0,np.ceil(q.min(0)-1e-6).astype(int));hi=np.minimum(size-1,np.floor(q.max(0)+1e-6).astype(int))
    if (hi<lo).any():return np.array([],int),np.array([],int),np.empty((0,3))
    yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];v=np.c_[xx.ravel(),yy.ravel()]
    mat=np.column_stack((q[1]-q[0],q[2]-q[0]))
    if abs(np.linalg.det(mat))<1e-12:return np.array([],int),np.array([],int),np.empty((0,3))
    bc=(v-q[0])@np.linalg.inv(mat).T;b=np.c_[1-bc.sum(1),bc]
    ok=(b>=-1e-6).all(1)
    return v[ok,0],v[ok,1],b[ok]
def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def colors(p,comp):
    x,y,z=p.T;col=np.tile([154.,205.,246.],(len(p),1))
    body=(1-smooth(.90,1.1,(x/.171)**2+((z-.273)/.225)**2))*(1-smooth(-.13,-.075,y))*(z<.5)
    face=(1-smooth(.90,1.08,(x/.32)**2+((z-.565)/.148)**2))*(1-smooth(-.24,-.18,y))*(z>.45)
    cream=np.maximum(body,face)
    col=col*(1-cream[:,None])+np.array([255.,248.,233.])*cream[:,None]
    pink=np.exp(-((abs(x)-.218)/.047)**2-((z-.596)/.029)**2)*(1-smooth(-.22,-.16,y))*.72
    col=col*(1-pink[:,None])+np.array([250.,155.,151.])*pink[:,None]
    if comp in (2,5): col[:]=[154,205,246]
    if comp in (6,7): col[:]=[231,155,182]
    if comp in (10,11): col[:]=[86,153,221]
    if comp in (8,9):
        cx=.142 if comp==9 else -.142
        t=np.clip((z-.595)/.12,0,1);col=np.c_[20+20*(1-t),36+82*(1-t),63+100*(1-t)]
        glint=np.exp(-((x-(cx-.018))/.012)**2-((z-.683)/.014)**2)
        col=col*(1-glint[:,None])+255*glint[:,None]
    if comp==12:col[:]=[79,52,57]
    if comp>=13:col[:]=[255,248,233]
    if comp==90:col[:]=[150,201,242]
    if comp==91:col[:]=[57,27,39]
    return np.uint8(np.clip(col,0,255))
def main():
    data=np.load(TMP/'mesh-data.npz')
    records=json.loads((TMP/'inspect.json').read_text())
    labels=np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
    names=['PINO_C_BASE_RIG_V001','PinoSoftLids_L','PinoSoftLids_R','PinoOralLiner']
    rgb=np.zeros((SIZE,SIZE,3),np.uint8);island=np.full((SIZE,SIZE),-1,np.int32);tri_id=np.full((SIZE,SIZE),-1,np.int32)
    surfaces={};rows=[];offset=0;tid=0;allq=[];allp=[];alls=[];allc=[];allowner=[]
    for mi,name in enumerate(names):
        i=next(r['i'] for r in records if r['name']==name)
        p,t,li,uv=[data[f'{i}_{a}'] for a in ['p','t','li','uv']]
        q=uv[li];xyz=p[t]
        comps=labels[t[:,0]] if mi==0 else np.full(len(t),91 if mi==3 else 90)
        # Join only identical surface edges with continuous UV.
        par=np.arange(len(t));edges={}
        def find(a):
            while par[a]!=a:par[a]=par[par[a]];a=par[a]
            return a
        for ti,(vs,qs) in enumerate(zip(t,q)):
            for a,b in [(0,1),(1,2),(2,0)]:
                va,vb=int(vs[a]),int(vs[b]);qa,qb=qs[a],qs[b]
                if va>vb:va,vb=vb,va;qa,qb=qb,qa
                key=(va,vb,*np.round(qa,7),*np.round(qb,7))
                if key in edges:par[find(ti)]=find(edges[key])
                else:edges[key]=ti
        _,isl=np.unique([find(j) for j in range(len(t))],return_inverse=True);isl+=offset;offset=int(isl.max())+1
        a=xyz[:,1]-xyz[:,0];b=xyz[:,2]-xyz[:,0];area3=np.linalg.norm(np.cross(a,b),axis=1)/2
        u=q[:,1]-q[:,0];v=q[:,2]-q[:,0];area2=np.abs(u[:,0]*v[:,1]-u[:,1]*v[:,0])/2
        density=np.sqrt(area2/np.maximum(area3,1e-30))*SIZE
        e1=np.linalg.norm(a,axis=1);bx=np.einsum('ij,ij->i',a,b)/np.maximum(e1,1e-30);by=np.sqrt(np.maximum(0,(b*b).sum(1)-bx*bx))
        inv=np.zeros((len(t),2,2));inv[:,0,0]=1/np.maximum(e1,1e-30);inv[:,0,1]=-bx/np.maximum(e1*by,1e-30);inv[:,1,1]=1/np.maximum(by,1e-30)
        J=np.stack([u,v],axis=2)@inv;sv=np.linalg.svd(J,compute_uv=False);stretch=sv[:,0]/np.maximum(sv[:,1],1e-30)
        center=xyz.mean(1);x,y,z=center.T
        masks={'all':np.ones(len(t),bool),'face':(z>.50)&(z<.76)&(y<-.25),'eyes':np.isin(comps,[8,9]),'cheeks':(abs(x)>.16)&(abs(x)<.28)&(z>.54)&(z<.64)&(y<-.28),'mouth':(abs(x)<.07)&(z>.54)&(z<.64)&(y<-.34),'belly':(abs(x)<.17)&(z>.08)&(z<.45)&(y<-.13),'forelimbs':(abs(x)>.20)&(z>.24)&(z<.44),'tail':np.isin(comps,[2,5])}
        def stats(mask):
            ok=mask&(area3>1e-12)
            if not ok.any():return None
            return dict(triangles=int(ok.sum()),surface_area_m2=float(area3[ok].sum()),uv_area=float(area2[ok].sum()),density_px_per_m_p10_p50_p90=np.percentile(density[ok],[10,50,90]).tolist(),anisotropy_p50_p95_max=np.percentile(stretch[ok],[50,95,100]).tolist())
        rows.append(dict(mesh=name,islands=int(len(np.unique(isl))),regions={n:stats(m) for n,m in masks.items() if m.any()}))
        for j,coords in enumerate(q):
            xx,yy,bc=raster(coords)
            if len(xx):
                rgb[yy,xx]=colors(bc@xyz[j],int(comps[j]));island[yy,xx]=isl[j];tri_id[yy,xx]=tid+j
        allq.extend(q);allp.extend(xyz);alls.extend(isl);allc.extend(comps);allowner.extend([mi]*len(t));tid+=len(t)
    # Conservatively seed subpixel whisker charts at exact surface vertices,
    # edge midpoints and centroid. They otherwise have no interior pixel center.
    aq=np.array(allq);ap=np.array(allp);ac=np.array(allc);asi=np.array(alls)
    for comp in range(13,19):
        tids=np.where(ac==comp)[0]
        bary=np.array([[1,0,0],[0,1,0],[0,0,1],[.5,.5,0],[0,.5,.5],[.5,0,.5],[1/3,1/3,1/3]])
        qu=np.einsum('kj,nji->nki',bary,aq[tids]).reshape(-1,2)
        pts=np.einsum('kj,nji->nki',bary,ap[tids]).reshape(-1,3)
        xy=np.clip(np.floor(qu*SIZE).astype(int),0,SIZE-1);xx,yy=xy.T
        missing=island[yy,xx]<0;xx=xx[missing];yy=yy[missing]
        rgb[yy,xx]=colors(pts[missing],comp)
        owners=np.repeat(tids,len(bary))[missing]
        island[yy,xx]=asi[owners];tri_id[yy,xx]=owners
    covered=island>=0
    # Pixel-center estimate of foreign-island proximity, axis and diagonal offsets.
    gaps={}
    for rad in [1,2,4,8]:
        risk=np.zeros_like(covered)
        for dx,dy in [(rad,0),(0,rad),(rad,rad),(rad,-rad)]:
            a=(slice(max(0,dy),min(SIZE,SIZE+dy)),slice(dx,SIZE));b=(slice(max(0,-dy),min(SIZE,SIZE-dy)),slice(0,SIZE-dx))
            hit=(island[a]>=0)&(island[b]>=0)&(island[a]!=island[b]);risk[a]|=hit;risk[b]|=hit
        gaps[str(rad)]=dict(covered_pixels_near_other_island=int(risk.sum()),fraction=float(risk.sum()/covered.sum()))
    # Bounded nearest-front dilation, never overwrite a covered texel. 8 px max.
    padded=rgb.copy();known=covered.copy()
    for step in range(8):
        new=known.copy()
        for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
            a=(slice(max(0,dy),min(SIZE,SIZE+dy)),slice(max(0,dx),min(SIZE,SIZE+dx)));b=(slice(max(0,-dy),min(SIZE,SIZE-dy)),slice(max(0,-dx),min(SIZE,SIZE-dx)))
            fill=(~new[a])&known[b];target=padded[a];target[fill]=padded[b][fill];new[a]|=fill
        known=new
    padded[~known]=[154,205,246]
    Image.fromarray(padded[::-1]).save(TMP/'diagnostic-color-4k.png')
    yy,xx=np.indices((SIZE,SIZE));checks=((xx//64+yy//64)%2)
    checker=np.where(checks[:,:,None],np.array([223,226,229],np.uint8),np.array([65,77,94],np.uint8))
    Image.fromarray(checker[::-1]).save(TMP/'checker-4k.png')
    # UV map shown with stable island hues; white is empty.
    uvvis=np.full((SIZE,SIZE,3),250,np.uint8);ids=island[covered];uvvis[covered]=np.c_[(ids*71)%180+40,(ids*113)%180+40,(ids*47)%180+40]
    Image.fromarray(uvvis[::-1]).resize((1400,1400)).save(OUT/'uv-islands.png')
    np.savez_compressed(TMP/'surface.npz',q=np.array(allq),p=np.array(allp),island=np.array(alls),component=np.array(allc),owner=np.array(allowner),triangle_image=tri_id)
    dump('uv-audit.json',dict(resolution=SIZE,islands=offset,coverage_pixel_fraction=float(covered.mean()),uv_area_sum=float(sum(r['regions']['all']['uv_area'] for r in rows)),proximity_pixel_center_estimate=gaps,proximity_limit='Axis/diagonal raster estimate, not exact minimum segment clearance; no mipmap guarantee.',meshes=rows))
    print(json.dumps(dict(islands=offset,coverage=float(covered.mean()),regions=rows[0]['regions'],proximity=gaps)))
if __name__=='__main__':main()
