"""Exact distal triangle crossings on final saved GLB witnesses.

Reuses the established BVH/segment test, with this candidate's unchanged
topology and regenerated round-trip vertices; no source asset is modified.
"""
from pathlib import Path
import numpy as np, json, hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree

R = Path(__file__).resolve().parents[2]
D = R / 'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004'
s = np.load(D / 'source-diagnosis.npz')
r = np.load(D / 'saved-reference.npz')
headtri = s['ShushuStatic_Head__tri']
rows = []
source = (R / 'scripts/blender/audit-shushu-contact-v003.py').read_text()
source = source[source.index('def segment_triangle'):]
source = source.replace("s[name+'__Basis']", "s[name+'__base']")
frames = sorted({int(k.rsplit('__', 1)[1]) for k in r.files})
exec(compile(source, str(__file__) + '::established_segment_test', 'exec'))
