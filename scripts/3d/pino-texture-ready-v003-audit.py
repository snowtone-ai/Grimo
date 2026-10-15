from pathlib import Path
import json,hashlib,ast,re
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/pino/evidence/texture-ready-v003';DEST=ROOT/'assets/grimo/production/pino/candidate-c/texture-ready-v003'
def read(name):return json.loads((OUT/name).read_text(encoding='utf8'))
files=read('file-manifest.json');hashes={Path(f['path']).suffix:f['sha256'] for f in files}
assert all(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'] and (ROOT/f['path']).stat().st_size==f['bytes'] for f in files)
saved=read('saved-master-audit.json');assert saved['basis_vertex_max_delta']==saved['canonical_corner_normal_max_delta']==0 and saved['triangles_equal']
assert all(o['max_influences']<=4 and o['weight_sum_max_error']<1e-6 for o in saved['objects'])
assert all(v==0 for v in saved['uv_overlap_selection'].values())
uv=read('uv-audit.json');assert uv['positive_area_overlap_pairs']==uv['zero_area_uv_triangles']==0
protected=read('source-protection.json');assert all(p['matches_authority_HEAD'] for p in protected)
assert read('glb-normal-patch.json')['glb_sha256']==hashes['.glb']
runtime=read('runtime-probe.json');assert runtime['glb_sha256']==hashes['.glb'] and runtime['all_morph_normals'] and not runtime['errors'] and runtime['changed_skin_matrices']==2 and runtime['lid_retreat_targets']==2
assert runtime['Texture_GO'] is False and runtime['Human_Pre_Texture_Gate']=='PENDING'
assert read('transition-controls.json')['master_sha256']==hashes['.blend']
ri=read('reimport-audit.json')['comparisons'];assert len(ri)==36
maxima={k:max(x[k] for x in ri) for k in ['max_position_error','max_normal_vector_error','max_uv_error']}
assert maxima['max_position_error']<3e-6 and maxima['max_normal_vector_error']<1e-4 and maxima['max_uv_error']<3e-8
vis=read('visibility-probes.json');assert all(v['changed_pixels_when_hiding_closed_liner']==0 for v in vis['closed_liner_hidden_comparison'].values())
assert all(v['eye_blue_pixels']==0 for v in vis['samples'] if v['state']=='closed both')
assert read('glb-validator.json')['validator']['errors']==0
scripts=[*ROOT.glob('scripts/blender/pino-texture-ready-v003*.py'),*ROOT.glob('scripts/3d/*pino-texture-ready-v003*'),ROOT/'scripts/3d/pino-uv-overlap.py',ROOT/'scripts/3d/encode-pino-proof-gif.py']
for p in scripts:
    if p.suffix=='.py':ast.parse(p.read_text(encoding='utf8'),filename=str(p))
for p in [OUT/'REVIEW.md',OUT/'TEXTURE_CONTRACT.md',DEST/'README.md']:
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
        if not target.startswith(('http:','https:','#')):assert (p.parent/target.split('#')[0]).exists(),(p,target)
caps={str(p.relative_to(ROOT)):len(p.read_text(encoding='utf8')) for p in [ROOT/'AGENTS.md',ROOT/'docs/grimo/knowledge/Goal√map.md',ROOT/'docs/production/Handoff.md',DEST/'README.md']}
assert list(caps.values())[0]<=2500 and list(caps.values())[1]<=5000 and list(caps.values())[2]<=4000 and list(caps.values())[3]<=1500
result={'scope':'Delivery consistency only. Visual quality and complete Texture Ready are not approved.','overall':'HOLD','Human_Pre_Texture_Gate':'PENDING','Texture_GO':False,'protected_files':len(protected),'saved_master_basis_unchanged':True,'uv_positive_area_overlaps':0,'roundtrip_comparisons':len(ri),'roundtrip_maxima':maxima,'runtime_matches_glb_sha256':True,'gifs_match_master_sha256':True,'document_unicode_lengths':caps}
(OUT/'delivery-consistency.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
print('Mouth pixels',[(x['state'],x['oral_color_pixels_in_front_mouth_roi']) for x in vis['samples'] if x['view']=='front'][:5])
