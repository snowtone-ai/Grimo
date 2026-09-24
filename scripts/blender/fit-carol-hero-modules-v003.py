"""Coarse-to-fine, shape-only local fitting of one spatial ear/hoof basis.

The orthographic projections are normalized uniformly. The source sheets
have no world-to-pixel registration. 3Q remains an independent validation.
"""
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from carol_hero_v003_geometry import EAR,HOOF,ear,hoof

spec=importlib.util.spec_from_file_location('compare',Path(__file__).with_name('compare-carol-hero-modules-v003.py'))
cmp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cmp)
OUT=ROOT/'docs/production/carol/evidence/hero-modules-v003'
SIZE=192;SPAN=164


def normalize_array(mask):
    im=Image.fromarray((mask*255).astype(np.uint8),'L') if isinstance(mask,np.ndarray) else mask
    box=im.getbbox()
    if box is None:return np.zeros((SIZE,SIZE),dtype=bool)
    crop=im.crop(box)
    scale=SPAN/max(crop.size)
    shape=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.BILINEAR)
    canvas=Image.new('L',(SIZE,SIZE))
    canvas.paste(shape,((SIZE-shape.width)//2,(SIZE-shape.height)//2))
    return np.asarray(canvas)>=128


def reference(module,view):
    path=cmp.REFS[module]
    col,row=cmp.VIEWS[view]
    panel=Image.open(path).crop((col*627,row*627,(col+1)*627,(row+1)*627))
    return normalize_array(cmp.reference_mask(panel,module))


REFS={module:{view:reference(module,view) for view in ('front','side','top')}
      for module in ('ear','hoof')}


def projection(vertices,view,module):
    v=np.asarray(vertices)
    if view=='front':return np.stack((-v[:,1],v[:,2]),axis=1)
    if view=='side':return np.stack((v[:,0],v[:,2]),axis=1)
    if module=='ear':return np.stack((-v[:,1],-v[:,0]),axis=1)
    return np.stack((-v[:,1],v[:,0]),axis=1)


def projected_mask(vertices,faces,view,module):
    points=projection(vertices,view,module)
    lo=points.min(axis=0);hi=points.max(axis=0)
    span=max(hi-lo)
    points=(points-lo)/span*SPAN+(SIZE-SPAN)/2
    points[:,1]=SIZE-points[:,1]
    img=Image.new('L',(SIZE,SIZE))
    draw=ImageDraw.Draw(img)
    if module=='ear':
        # Monotone-chain hull; the ear exterior is convex in primary views.
        ordered=sorted({(round(x,2),round(y,2)) for x,y in points})
        def cross(a,b,c):
            return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        lower=[];upper=[]
        for p in ordered:
            while len(lower)>1 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
            lower.append(p)
        for p in reversed(ordered):
            while len(upper)>1 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
            upper.append(p)
        draw.polygon(lower[:-1]+upper[:-1],fill=255)
    else:
        for f in faces:
            draw.polygon([tuple(points[i]) for i in f],fill=255)
    return normalize_array(img)


def metric(a,b):
    return float(np.logical_and(a,b).sum()/max(1,np.logical_or(a,b).sum()))


def scores(module,p):
    v,f,_=ear(-1,p) if module=='ear' else hoof(.390,-.145,p)
    if module=='hoof':
        # Hidden attachment collar does not belong to local visible shape.
        f=[face for face in f if all(v[i][2]<=.116 for i in face)]
    return {view:metric(REFS[module][view],projected_mask(v,f,view,module))
            for view in ('front','side','top')}


def fit(module):
    defaults=EAR if module=='ear' else HOOF
    p=defaults.copy()
    existing=OUT/'parameters.json'
    if existing.exists():p.update(json.loads(existing.read_text(encoding='utf8')).get(module,{}))
    if module=='ear':
        groups=[
            [('drop_ease',(1.2,3.2)),('aft_ease',(1.0,2.4)),('vertical_arch',(-.025,.025))],
            [('lateral',(.32,.45)),('fore_aft',(.19,.29)),('bend',(-.025,.045))],
            [('body_width',(.075,.135)),('body_cushion',(.06,.115)),('root_width',(.005,.07))],
            [('root_cushion',(.025,.11)),('upper_fullness',(.65,1.1)),('lower_fullness',(.9,1.55))],
            [('root_fullness',(.5,1.4)),('tip_taper',(.0,.6)),('tip_roundness',(.4,1.1))],
        ]
    else:
        groups=[
            [('depth',(.15,.24)),('heel_taper',(-.3,.4)),('heel_fullness',(.65,1.2))],
            [('toe_projection',(.008,.048)),('cleft_depth',(.008,.04)),('toe_spacing',(.060,.082))],
            [('upper_taper',(.4,.8)),('toe_roundness',(.015,.035))],
        ]
    history=[];best=-1;stall=0
    rng=np.random.default_rng(170)
    print(module,'seed',scores(module,p),flush=True)
    for round_index in range(12):
        group=groups[round_index%len(groups)]
        keys=[name for name,_ in group]
        bounds=[b for _,b in group]
        def objective(values):
            q=p.copy();q.update(zip(keys,values))
            if module=='ear':q['drop']=q['lateral']*math.tan(math.radians(18))
            m=scores(module,q)
            return .36*m['front']+.34*m['side']+.30*m['top']
        values=np.array([p[k] for k in keys]);candidate=values.copy()
        candidate_value=objective(candidate)
        # Grouped coordinate refinement, then bounded joint perturbations.
        for j,(low,high) in enumerate(bounds):
            for value in np.linspace(low,high,9):
                trial_values=candidate.copy();trial_values[j]=value
                value_score=objective(trial_values)
                if value_score>candidate_value:
                    candidate,candidate_value=trial_values,value_score
        for _ in range(32):
            trial_values=np.clip(candidate+rng.normal(0,.13, len(keys))*
                                 np.array([hi-lo for lo,hi in bounds]),
                                 [lo for lo,_ in bounds],[hi for _,hi in bounds])
            value_score=objective(trial_values)
            if value_score>candidate_value:
                candidate,candidate_value=trial_values,value_score
        trial=p.copy();trial.update(zip(keys,candidate))
        if module=='ear':trial['drop']=trial['lateral']*math.tan(math.radians(18))
        m=scores(module,trial)
        value=.36*m['front']+.34*m['side']+.30*m['top']
        improved=value>best+1e-5
        if improved:p=trial;best=value
        best_m=scores(module,p)
        history.append({'round':round_index+1,'group':keys,'trial':m,
                        'accepted':improved,'best':best_m,'weighted':best})
        print(module,'round',round_index+1,'best',best_m,'weighted',round(best,4),flush=True)
        if len(history)>1:
            prev=history[-2]
            gain=best-prev['weighted']
            weak_gain=max(best_m[v]-prev['best'][v] for v in best_m)
            stall=stall+1 if gain<.005 and weak_gain<.01 else 0
        if stall>=2 and round_index+1>=2*len(groups):break
    return p,history,'STALLED' if stall>=2 else 'ROUND_CEILING'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result={};history={};stops={}
    for module in ('ear','hoof'):
        p,h,stop=fit(module)
        result[module]=p;history[module]=h;stops[module]=stop
    (OUT/'parameters.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    (OUT/'fit-history.json').write_text(json.dumps({'rounds':history,'stop':stops},indent=2)+'\n',encoding='utf8')


if __name__=='__main__':main()
