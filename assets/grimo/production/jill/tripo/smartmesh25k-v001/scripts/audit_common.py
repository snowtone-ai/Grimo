"""Read-only source audit. Run in a fresh background Blender, never in the user's scene."""
import bpy, json, hashlib, sys
from pathlib import Path
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[7]
ASSET = ROOT / 'assets/grimo/production/jill/tripo/smartmesh25k-v001'
EVIDENCE = ROOT / 'docs/production/jill/evidence/smartmesh25k-v001'

def write_json(name, data):
    (EVIDENCE/name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

def components(mesh):
    parents=list(range(len(mesh.vertices)))
    def root(a):
        while parents[a]!=a:
            parents[a]=parents[parents[a]]; a=parents[a]
        return a
    for edge in mesh.edges:
        a,b=map(root,edge.vertices); parents[b]=a
    groups={}
    for v in mesh.vertices: groups.setdefault(root(v.index), {'v':[], 'f':[]})['v'].append(v.index)
    for f in mesh.polygons: groups[root(f.vertices[0])]['f'].append(f.index)
    return sorted(groups.values(), key=lambda g:(-len(g['f']), min(g['v'])))

def audit(obj):
    m=obj.data; m.calc_loop_triangles()
    xyz=np.array([tuple(obj.matrix_world@v.co) for v in m.vertices])
    comps=components(m); out=[]
    for i,c in enumerate(comps):
        p=xyz[c['v']]; sv=np.linalg.svd(p-p.mean(axis=0),compute_uv=False)
        out.append({'id':i,'vertices':len(c['v']),'faces':len(c['f']),
                    'triangles':sum(len(m.polygons[f].vertices)-2 for f in c['f']),
                    'bounds':[p.min(0).tolist(),p.max(0).tolist()], 'svd':sv.tolist(),
                    'vertex_ids':c['v'] if len(c['v'])<20 else None,
                    'face_ids':c['f'] if len(c['f'])<20 else None})
    edges={}
    for p in m.polygons:
        for e in p.edge_keys: edges[e]=edges.get(e,0)+1
    return {'name':obj.name,'vertices':len(m.vertices),'polygons':len(m.polygons),'triangles':len(m.loop_triangles),
            'bounds':[xyz.min(0).tolist(),xyz.max(0).tolist()], 'matrix':list(map(list,obj.matrix_world)),
            'uv_layers':[u.name for u in m.uv_layers], 'materials':[x.name if x else None for x in m.materials],
            'boundary_edges':sum(v==1 for v in edges.values()),'nonmanifold_gt2':sum(v>2 for v in edges.values()),
            'degenerate_triangles':sum(t.area<1e-12 for t in m.loop_triangles),'components':out}

def setup_camera(scene, direction, target=(0,0,0), scale=3):
    cam=scene.camera
    if not cam:
        cam=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'))
        scene.collection.objects.link(cam); scene.camera=cam
    target=Vector(target); cam.location=target+Vector(direction).normalized()*10
    cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.type='ORTHO'; cam.data.ortho_scale=scale; cam.data.lens=50

def render(scene, name, direction, target=(0,0,0), scale=3):
    setup_camera(scene,direction,target,scale)
    scene.render.filepath=str(EVIDENCE/'renders'/f'{name}.png')
    bpy.ops.render.render(write_still=True)

def setup_render(scene):
    scene.render.engine='BLENDER_WORKBENCH'
    scene.render.resolution_x=900; scene.render.resolution_y=900; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
    s=scene.display.shading; s.light='STUDIO'; s.studiolight_rotate_z=0.4
    s.color_type='OBJECT'; s.show_shadows=True; s.show_cavity=True; s.cavity_type='BOTH'
    s.show_specular_highlight=True; s.background_type='WORLD'; s.background_color=(0.8,0.8,0.8)
    scene.world.color=(0.8,0.8,0.8); scene.view_settings.view_transform='Standard'

if __name__=='__main__':
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene; scene.world=bpy.data.worlds.new('ReviewWorld')
    src=ASSET/'input'/'cute dragon 3d model (1).glb'
    bpy.ops.import_scene.gltf(filepath=str(src),merge_vertices=False)
    glb=[o for o in scene.objects if o.type=='MESH']
    for o in glb: o.name='OriginalGLB_'+o.name; o.color=(0.58,0.68,0.55,1)
    ga=[audit(o) for o in glb]
    before=set(scene.objects)
    bpy.ops.import_scene.fbx(filepath=str(src.with_suffix('.fbx')))
    fbx=[o for o in scene.objects if o not in before and o.type=='MESH']
    fa=[audit(o) for o in fbx]
    for o in fbx: o.hide_render=True; o.hide_set(True); o.name='OriginalFBX_'+o.name
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (src,src.with_suffix('.fbx'))}
    write_json('source-audit.json',{'blender':bpy.app.version_string,'hashes':hashes,'glb':ga,'fbx':fa})
    setup_render(scene)
    points=[o.matrix_world@v.co for o in glb for v in o.data.vertices]
    lo=Vector(tuple(min(p[i] for p in points) for i in range(3)))
    hi=Vector(tuple(max(p[i] for p in points) for i in range(3)))
    center=(lo+hi)/2; scale=max(hi-lo)*1.16
    render(scene,'audit-original-front',(0,-1,0),center,scale)
    render(scene,'audit-original-three-quarter',(1,-2,0.6),center,scale)
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'jill-original-inspection.blend'))
    print('JILL_SOURCE_AUDIT_COMPLETE', json.dumps({'hashes':hashes,'glb':[(a['vertices'],a['triangles'],len(a['components'])) for a in ga],'fbx':[(a['vertices'],a['triangles'],len(a['components'])) for a in fa]}))
