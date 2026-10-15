"""Additional posed front 3Q / transition evidence; no mesh edits or save."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from audit_common import *

scene = bpy.context.scene
proof = json.loads((EVIDENCE/'deformation-validation.json').read_text())
scene.frame_set(1)
render(scene, 'proof-neutral-front3q', (1,-2,.45), (0,0,.5), 1.16)
for ci, case in enumerate(proof['cases']):
    for prefix, offset in [('half',6), ('proof',12)]:
        scene.frame_set(1+24*ci+offset)
        render(scene, prefix+'-'+case['name']+'-front3q', (1,-2,.45), (0,0,.5), 1.16)
print('APPEARANCE_LOCK_CAPTURES_COMPLETE; master not resaved')
