import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *
g=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('OriginalGLB'))
f=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('OriginalFBX'))
diff=[]
for i,(a,b) in enumerate(zip(g.data.polygons,f.data.polygons)):
    if sorted(a.vertices)!=sorted(b.vertices):
        diff.append({'id':i,'glb':list(a.vertices),'fbx':list(b.vertices)})
        if len(diff)==5:break
print('FIRST_FACE_DIFFS',json.dumps(diff))
info=json.loads((EVIDENCE/'plate-investigation.json').read_text())
faces=[i for c in info['small_components'] for i in c['faces']]
chosen=set(faces); vg=set(v for fi in faces for v in g.data.polygons[fi].vertices)
kept=set(v for p in g.data.polygons if p.index not in chosen for v in p.vertices)
print('SHARED_VERTICES',sorted(vg&kept))
print('SHARED_FACES',[(p.index,list(p.vertices)) for p in g.data.polygons if p.index not in chosen and any(v in vg for v in p.vertices)])
for i,c in enumerate(info['small_components']):
    me=bpy.data.meshes.new(f'PlateSet{i}'); me.from_pydata([tuple(v.co) for v in g.data.vertices],[],[list(g.data.polygons[fi].vertices) for fi in c['faces']])
    ob=bpy.data.objects.new(f'PlateSet{i}',me); bpy.context.scene.collection.objects.link(ob); ob.color=(.9,.12,.12,1)
    ob['source_faces']=c['faces']
g.hide_render=True
me=bpy.data.meshes.new('ContextWithSuspectFacesHidden'); me.from_pydata([tuple(v.co) for v in g.data.vertices],[],[list(p.vertices) for p in g.data.polygons if p.index not in chosen])
ob=bpy.data.objects.new('ContextPreviewOnly',me); bpy.context.scene.collection.objects.link(ob); ob.color=(.58,.68,.55,1)
for p in me.polygons:p.use_smooth=True
for name,d in [('front',(0,-1,0)),('side',(1,0,0)),('back',(0,1,0)),('3q',(1,-2,.4)),('rear3q',(-1,2,.3))]:
    render(bpy.context.scene,'suspect-highlight-'+name,d,(0,0,.5),1.16)
ob.hide_render=True
render(bpy.context.scene,'suspect-isolated',(1,-2,.4),(0,0,.5),1.16)
