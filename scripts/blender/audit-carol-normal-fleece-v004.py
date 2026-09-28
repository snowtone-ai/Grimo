"""Reopen and audit the actual saved asset; does not infer visual acceptance."""
import bpy
import bmesh
import json
import math
import hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v004'
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v004.blend'
SKIN=ASSET.with_name('carol-skin-final-v002.blend')
EXPECTED='321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET))
    scene=bpy.context.scene
    report={'asset':ASSET.relative_to(ROOT).as_posix(),'sha256':sha(ASSET),
      'reopened':True,'skin_sha256':sha(SKIN),'accepted_skin_source_unchanged':sha(SKIN)==EXPECTED,
      'state':scene.get('phase1_state'),'non_finite_vertices':0,'meshes':{},'authorities':[],
      'cameras':{},'images':[],'active_shape_keys':{},'drivers':[],
      'human':'NOT_GRANTED','motion':'NOT_TESTED','deformation':'NOT_TESTED',
      'runtime':'NOT_TESTED','device':'NOT_TESTED','phase_2_started':False}
    for ob in scene.objects:
        if ob.animation_data and ob.animation_data.drivers:
            report['drivers'].extend({'object':ob.name,'path':d.data_path,'expression':d.driver.expression} for d in ob.animation_data.drivers)
        if ob.type=='MESH':
            points=[ob.matrix_world@v.co for v in ob.data.vertices]
            report['non_finite_vertices']+=sum(not all(math.isfinite(c) for c in p) for p in points)
            entry={'vertices':len(points),'faces':len(ob.data.polygons),
              'bounds':[[min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)]],
              'owner':ob.parent.name if ob.parent else None,'groups':[g.name for g in ob.vertex_groups]}
            if 'Fleece' in ob.name:
                bm=bmesh.new();bm.from_mesh(ob.data)
                entry['non_manifold_edges']=sum(not e.is_manifold for e in bm.edges)
                entry['zero_area_faces']=sum(f.calc_area()<1e-14 for f in bm.faces)
                bm.verts.ensure_lookup_table()
                remaining=set(bm.verts);components=[]
                while remaining:
                    todo=[remaining.pop()];component=[]
                    while todo:
                        vertex=todo.pop();component.append(vertex)
                        for edge in vertex.link_edges:
                            other=edge.other_vert(vertex)
                            if other in remaining:remaining.remove(other);todo.append(other)
                    components.append({'vertices':len(component),'bounds':[[min(v.co[i] for v in component) for i in range(3)],[max(v.co[i] for v in component) for i in range(3)]]})
                entry['connected_components']=sorted(components,key=lambda c:-c['vertices'])
                bm.free()
            report['meshes'][ob.name]=entry
            if ob.data.shape_keys:
                report['active_shape_keys'][ob.name]={k.name:k.value for k in ob.data.shape_keys.key_blocks if k.name!='Basis' and abs(k.value)>1e-8}
        elif ob.type=='CAMERA':
            report['cameras'][ob.name]={'matrix':[list(row) for row in ob.matrix_world],'type':ob.data.type,'ortho_scale':ob.data.ortho_scale}
    for item in json.loads((ROOT/'assets/grimo/source/carol/approved-3d/authority.json').read_text())['authorityOrder']:
        actual=sha(ROOT/item['path'])
        report['authorities'].append({'path':item['path'],'sha256':actual,'matches_manifest':actual==item['sha256'].lower()})
    for im in bpy.data.images:
        if im.type in ['RENDER_RESULT','COMPOSITING']:continue
        if im.source=='VIEWER':continue
        packed=bool(im.packed_file)
        exists=Path(bpy.path.abspath(im.filepath)).is_file() if im.filepath else False
        report['images'].append({'name':im.name,'packed':packed,'size':list(im.size),'source':im.source,'file_exists':exists})
    report['all_authorities_match']=all(a['matches_manifest'] for a in report['authorities'])
    report['all_used_images_stable']=all(i['packed'] or i['file_exists'] or i['source']=='GENERATED' for i in report['images'])
    report['all_images_embedded']=all(i['packed'] or i['source']=='GENERATED' for i in report['images'])
    report['fleece_closed_and_nondegenerate']=all(m.get('non_manifold_edges',0)==0 and m.get('zero_area_faces',0)==0 for m in report['meshes'].values())
    report['ornament_glint_owners_match']=all(
        entry['owner'] is not None and entry['owner']==report['meshes'][name.removesuffix('_glint')]['owner']
        for name,entry in report['meshes'].items() if name.endswith('_glint')
    )
    hashes=json.loads(scene.get('generator_hashes','{}'))
    report['generator_hashes']=hashes
    if scene.get('anatomy_source'):
        source=ASSET.with_name(scene['anatomy_source'])
        report['anatomy_source']={'file':source.name,'sha256':sha(source),
          'matches_saved_asset':sha(source)==scene['anatomy_source_sha256']}
    report['generator_matches_saved_asset']=bool(hashes) and all(sha(ROOT/'scripts/blender'/name)==value for name,value in hashes.items())
    report['no_compositing']=not scene.render.use_compositing
    report['skin_fleece_intersections']='Visual and spatial review required; boundary returns intentionally enter Skin. Not an automatic PASS.'
    report['technical_checks_pass']=bool(report['accepted_skin_source_unchanged'] and report['all_authorities_match'] and report['non_finite_vertices']==0 and report['all_images_embedded'] and report['fleece_closed_and_nondegenerate'] and report['generator_matches_saved_asset'] and report['ornament_glint_owners_match'])
    if 'anatomy_source' in report:
        report['technical_checks_pass'] &= report['anatomy_source']['matches_saved_asset']
    (OUT/'asset-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['sha256','technical_checks_pass','non_finite_vertices','state']}))
    assert report['technical_checks_pass']


if __name__=='__main__':main()
