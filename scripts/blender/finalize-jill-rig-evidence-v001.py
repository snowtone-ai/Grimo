"""Hash output/source pairs and protected authorities; no rig/source mutations."""
from pathlib import Path
import json,hashlib,subprocess,re
R=Path(__file__).resolve().parents[2];E=R/'docs/production/jill/rig-other-v001';A=R/'assets/grimo/production/jill/tripo/rig-other-v001'
ORIGINAL=Path('C:/Users/chidj/project/プロダクト/Grimo')
JILL=Path('C:/Users/chidj/.codex/worktrees/jill-smartmesh25k-inspection/Grimo')
BASE='8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def git(*args,root=R):return subprocess.check_output(['git','-C',str(root),*args]).decode('utf8').strip()
expected={'tripo-other-original.fbx':'1d9ecfae60f0fcb1a8bbffeb81fd2a931b1dba0907af43487bf0d1f1e3a7dc14',
 'tripo-other-original.glb':'a93cd56d4b9658596284288ef8f5ebabffae0d3c5f7024e591269ce95eff0378',
 'jill-v002-authority-donor.blend':'8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97'}
origins={'tripo-other-original.fbx':ORIGINAL/'tripo_convert_77a7aeee-faff-4d3b-8082-d15dddbe9fc8.fbx',
 'tripo-other-original.glb':ORIGINAL/'jill-v002-neutral-tripo.fbx.glb',
 'jill-v002-authority-donor.blend':JILL/'assets/grimo/production/jill/tripo/smartmesh25k-v002/jill-geometry-master-v002.blend'}
sources=[]
for name,want in expected.items():
    original=sha(origins[name]);copy=sha(A/'source'/name);assert original==copy==want,name
    sources.append({'copy':str((A/'source'/name).relative_to(R)).replace('\\','/'),'original_path':str(origins[name]),'sha256':copy,'expected_intake_sha256':want,'original_still_identical':True})
protected=[]
for p in [R/'assets/grimo/source/jill/jill-Identity-canonical.png',*sorted((R/'assets/grimo/source/jill/tripo-generation-pose').glob('jill_bodyonly_*.png'))]:
    rel=p.relative_to(R).as_posix();committed=subprocess.check_output(['git','-C',str(R),'show',BASE+':'+rel]);want=hashlib.sha256(committed).hexdigest()
    actual=sha(p);original=sha(ORIGINAL/rel);assert actual==original==want,rel
    protected.append({'path':rel,'baseline_commit':BASE,'baseline_sha256':want,'worktree_sha256':actual,'original_checkout_sha256':original,'unchanged':True})
build=read(E/'build-report.json')
if 'build_stage_sha256' not in build:build['build_stage_sha256']=build.pop('output_sha256')
build['output_sha256']=sha(A/'jill-rig-other-v001.blend');build['output_hash_stage']='Final saved blend including proof action; source surface unchanged'
write(E/'build-report.json',build)
contract=read(E/'control-contract.json');contract['runtime_mapping_file']='runtime-mapping.json';contract['artifact_status']='REVIEW CANDIDATE / visual HOLD / Human PENDING';write(E/'control-contract.json',contract)
roundtrip=read(E/'roundtrip-validation.json');assert roundtrip['bounded_roundtrip_pass']
assert roundtrip['glb_structure']['sha256']==sha(A/'jill-rig-other-v001.glb')
artifacts=[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in [A/'jill-rig-other-v001.blend',A/'jill-rig-other-v001.glb',E/'Plan.md',E/'Evidence.md',E/'runtime-mapping.json',E/'control-contract.json']]
links=[]
for p in [E/'Plan.md',E/'Evidence.md',R/'docs/production/jill/HANDOFF.md',A/'README.md',A/'source/README.md']:
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
        if '://' in target or target.startswith('#'):continue
        resolved=(p.parent/target.split('#')[0]).resolve();links.append({'document':p.relative_to(R).as_posix(),'target':target,'exists':resolved.exists() or resolved==E/'manifest.json'})
assert all(x['exists'] for x in links),[x for x in links if not x['exists']]
write(E/'manifest.json',{'date':'2026-10-15','status':'REVIEW CANDIDATE / overall HOLD / Human appearance PENDING','baseline_main':BASE,
 'plan_frozen_commit':'832e1e89bcbfadb74f14154a87211056b997497c','branch':git('branch','--show-current'),
 'original_checkout_initial_head':'0947d03efabbf3df04ed18e0ec6f99cc9efd2727','original_checkout_observed_final_head':git('rev-parse','HEAD',root=ORIGINAL),
 'original_checkout_status_observed':git('status','--short',root=ORIGINAL).splitlines(),
 'parallel_edit_note':'Original checkout advanced concurrently. It was never reset, checked out or written by this rig task. Dirty contents had no full pre-task hash baseline; no unsupported byte-preservation claim is made for concurrent user edits.',
 'sources':sources,'protected_images':protected,'artifacts':artifacts,'relative_links_checked':len(links),
 'render_note':'Actual unretouched Blender Workbench renders. Capture-only diagnostic palette. Final node-only surface projection did not change geometry/weights/morph/proof; full body images retained and final GLB geometry/node rechecked.',
 'bounded_roundtrip_pass':True,'formal_texture':False,'full_motion_library':False,'human_visual_approval':False})
print('MANIFEST_COMPLETE',json.dumps({'source_pairs':len(sources),'protected_images':len(protected),'artifacts':len(artifacts),'links':len(links),'sha256_glb':sha(A/'jill-rig-other-v001.glb')}))
