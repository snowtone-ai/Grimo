"""Local topology plots; copied texture samples are diagnostic, never asset edits."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'
d=np.load(OUT/'mouth-source.npz');p=d['Head__base'];tri=d['Head__tri'];uv=d['Head__uv']
im=np.asarray(Image.open(OUT.parent/'production-rig-v004-skin-compat/ShushuStatic_Head-original-basecolor.png').convert('RGB'))
uvv=np.zeros((len(p),2));uvv[tri.ravel()]=uv.reshape(-1,2)
px=np.clip((uvv[:,0]*im.shape[1]).astype(int),0,im.shape[1]-1);py=np.clip(((1-uvv[:,1])*im.shape[0]).astype(int),0,im.shape[0]-1);colors=im[py,px]/255
m=(abs(p[:,0])<.08)&(p[:,2]>.53)&(p[:,2]<.65)&(p[:,1]<-.19)
print('local count',m.sum(),'bounds',p[m].min(0),p[m].max(0))
edges={}
for t in tri:
    for a,b in zip(t,np.roll(t,-1)):
        e=tuple(sorted((int(a),int(b))));edges[e]=edges.get(e,0)+1
boundary=np.array([e for e,n in edges.items() if n==1]); print('head boundary',len(boundary),'local boundary',sum(m[e].any() for e in boundary))
fig=Image.new('RGB',(2100,750),'#dddddd');draw=ImageDraw.Draw(fig)
for panel,(name,axis,lo,hi) in enumerate([('Basis',0,-.08,.08),('MouthOpen',1,-.29,-.13),('MouthClose',1,-.29,-.13)]):
    a=d['Head__'+name];draw.text((panel*700+20,20),name+' / '+('front X Z' if axis==0 else 'side Y Z'),fill='black')
    for idx in np.where(m)[0]:
        u=panel*700+40+(a[idx,axis]-lo)/(hi-lo)*620;v=710-(a[idx,2]-.52)/.14*620
        draw.ellipse((u-3,v-3,u+3,v+3),fill=tuple((colors[idx]*255).astype(int)),outline='#555555')
fig.save(OUT/'source-topology-front-side.png')
np.savez_compressed(OUT/'source-mouth-mapping.npz',uv=uvv,colors=colors)
u,ix=np.unique(np.round(p,6),axis=0,return_inverse=True)
e=np.sort(np.concatenate([ix[tri[:,[0,1]]],ix[tri[:,[1,2]]],ix[tri[:,[2,0]]]]),axis=1)
ee,n=np.unique(e,axis=0,return_counts=True);bound=ee[n==1]
near=(abs(u[bound].mean(1)[:,0])<.06)&(u[bound].mean(1)[:,2]>.595)&(u[bound].mean(1)[:,2]<.615)&(u[bound].mean(1)[:,1]<-.23)
b=bound[near];np.save(OUT/'mouth-boundary.npy',u[b])
plot=Image.new('RGB',(1400,700),'white');dd=ImageDraw.Draw(plot)
for i,(a,c) in enumerate(b):
    for panel,axis,lo,hi in [(0,0,-.06,.06),(1,1,-.28,-.16)]:
        points=[(panel*700+30+(u[j,axis]-lo)/(hi-lo)*640,650-(u[j,2]-.59)/.03*580) for j in [a,c]]
        dd.line(points,fill='red',width=2)
plot.save(OUT/'boundary-front-side.png')
print('mouth boundary',len(b),'extent',u[b].min((0,1)),u[b].max((0,1)))
