"""Continuous field sculpt for Carol v003. Run with Blender --background.

Historical fifth-norm Gaussian relief is extended over a closed 3D envelope.
v002 is opened, never regenerated or overwritten; structural parts are retained.
No projected image, billboard, rig, or runtime export is used. A single local
additive brush closes the crown saddle after the continuous field operation.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'assets/grimo/production/carol/blender/carol-blockout-v002.blend'
spec = importlib.util.spec_from_file_location('v002', Path(__file__).with_name('build-carol-blockout.py'))
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)

# Long, overlapping cloud banks. Angle is around Z; front is -90 degrees.
# (azimuth, elevation, longitudinal width, transverse width, height, tilt)
# Unequal widths and oblique flow replace isolated circular cross-sections.
BANKS = [
    (-118, 59, .44, .30, .24, -.3), (-59, 62, .38, .28, .20, .4),
    (-170, 34, .45, .32, .20, -.6), (-18, 30, .44, .31, .20, .5),
    (-158, -8, .44, .29, .18, .4), (-12, -14, .43, .30, .18, -.4),
    (151, 36, .48, .32, .20, .4), (38, 39, .47, .31, .23, -.5),
    (104, 58, .45, .33, .17, .3), (94, 13, .56, .32, .18, -.4),
    (153, -27, .43, .29, .19, -.35), (36, -29, .45, .28, .17, .3),
    (84, -42, .52, .28, .14, -.25), (-145, -44, .35, .26, .14, .3),
    (-34, -46, .38, .27, .15, -.4),
]
BREAKS = [
    (-141, 48, .22, .17, .10, .5), (-87, 71, .23, .17, .12, -.4),
    (-38, 48, .23, .18, .11, -.5), (-176, 12, .25, .17, .10, .4),
    (2, 8, .22, .16, .11, -.5), (177, -29, .24, .17, .10, .5),
    (13, -39, .25, .18, .10, .5), (126, 27, .23, .18, .09, -.4),
    (67, 38, .25, .17, .10, .6), (64, -10, .27, .18, .09, -.5),
    (125, -29, .25, .17, .10, -.4), (100, -57, .24, .17, .08, .4),
    (164, 54, .19, .15, .10, .35), (25, 58, .21, .16, .12, -.4),
    (139, 7, .22, .15, .12, -.4), (173, -9, .20, .15, .10, .3),
    (28, 16, .22, .16, .12, .4), (16, -14, .20, .16, .12, -.3),
    (108, 42, .22, .17, .11, -.5), (81, 3, .21, .16, .12, -.3),
    (49, -40, .22, .17, .12, .4), (151, -45, .21, .16, .10, -.3),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field(directions, controls):
    values = []
    for az, el, wu, wv, h, tilt in controls:
        a, e = math.radians(az), math.radians(el)
        center = np.array([math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)])
        u = np.array([-math.sin(a), math.cos(a), 0])
        v = np.cross(center, u)
        t = directions-center
        du, dv = t@u, t@v
        p = du*math.cos(tilt)+dv*math.sin(tilt)
        q = -du*math.sin(tilt)+dv*math.cos(tilt)
        values.append(h*np.exp(-1.5*((p/wu)**2+(q/wv)**2))*np.clip(directions@center, 0, 1)**4)
    return np.sum(np.array(values)**5, axis=0)**.2


def sculpt(pass_number):
    obj = bpy.data.objects['Carol_Fleece_Continuous']
    mat = obj.data.materials[0]
    # Recover v002's macro envelope, then diffuse away the union ridges.
    # The subsequent field is evaluated on the whole surface, never per ball.
    bpy.context.view_layer.objects.active = obj
    relax = obj.modifiers.new('Continuous envelope diffusion', 'SMOOTH')
    relax.factor = 1.0
    relax.iterations = 65
    bpy.ops.object.modifier_apply(modifier=relax.name)
    mesh = obj.data
    pos = np.array([v.co[:] for v in mesh.vertices], dtype=float)
    center = np.array([0, .16, 1.49])
    axes = np.array([1.52, 1.28, 1.23])
    dirs = (pos-center)/axes
    dirs /= np.linalg.norm(dirs, axis=1)[:, None]
    relief = .30*field(dirs, BANKS) + .65*field(dirs, BREAKS)
    radial = pos-center
    radial /= np.linalg.norm(radial,axis=1)[:,None]
    # Radial displacement avoids opposing normal directions folding in a saddle.
    pos += radial*relief[:,None]
    # Authored elliptical relief flows over the canopy and cheek/collar turns.
    x,y,z = pos.T.copy()
    front = np.clip(-dirs[:,1]*2,0,1)
    front = front*front*(3-2*front)
    def g(cx,cz,rx,rz):
        return np.exp(-2*((x-cx)/rx)**2-2*((z-cz)/rz)**2)
    ridges = [(-.62,2.40,.43,.28,.15),(-.09,2.60,.38,.25,.16),
              (.51,2.45,.41,.27,.17),(.99,2.12,.30,.40,.14),
              (-1.14,1.61,.32,.42,.15),(1.34,1.27,.28,.39,.15),
              (-1.31,.86,.34,.28,.16),(.99,.64,.35,.26,.16),
              (-.41,1.92,.40,.26,.14),(.37,1.88,.40,.29,.15),
              (-.84,1.03,.24,.33,.13),(.84,1.02,.24,.31,.14),
              (-.47,.60,.30,.24,.13),(.19,.51,.35,.20,.13)]
    relief_front = np.sum(np.array([h*g(cx,cz,rx,rz) for cx,cz,rx,rz,h in ridges])**5,axis=0)**.2
    pos[:,1] -= front*relief_front*.7
    if pass_number >= 2:
        # Break the two over-large side/rear masses into linked sweeping relief.
        pos += radial*(.20*field(dirs,BREAKS))[:,None]
    mesh.vertices.foreach_set('co',pos.astype(np.float32).ravel())
    mesh.update()
    # Local diffusion fills pinched saddles without flattening the whole fleece.
    group = obj.vertex_groups.new(name='Crown and temple saddle correction')
    for v in mesh.vertices:
        x,y,z = v.co
        weight = max(math.exp(-((x-.15)/.43)**2-((z-2.35)/.44)**2),
                     .55*math.exp(-((abs(x)-.95)/.30)**2-((z-1.73)/.32)**2))
        if y < -.3 and weight > .01: group.add([v.index],weight,'REPLACE')
    modifier = obj.modifiers.new('Relax local cloud saddles','SMOOTH')
    modifier.factor = 1.2
    modifier.iterations = 120
    modifier.vertex_group = group.name
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    if pass_number >= 2:
        # One additive sculpt brush fills the inherited deep crown saddle.
        # Revoxelize the whole field so the fill cannot become a folded flap.
        brush = old.uv('Temporary crown fill',(.10,-.48,2.36),(.40,.64,.34),mat)
        obj = old.fuse('Carol_Fleece_Continuous',[obj,brush],mat,
                       bpy.data.objects['Carol_Model'],voxel=.022,iterations=12)
    old.smooth(obj)
    obj['construction'] = 'diffused v002 envelope + fifth-norm anisotropic Gaussian cloud banks'
    obj['historical_transfer'] = 'locks_depth principle; no legacy projected paint or shallow reverse'
    obj['topology_status'] = 'structural study; production retopology deferred'
    if 'design_regions' in obj: del obj['design_regions']
    return obj


def structural_fingerprint():
    result = {}
    for o in bpy.data.objects:
        if o.name.startswith(('Carol_Fleece','Carol_Moon','Carol_Star','Carol_Review')): continue
        if o.type == 'MESH':
            co = np.array([v.co[:] for v in o.data.vertices], dtype=np.float32)
            result[o.name] = {'vertices': hashlib.sha256(co.tobytes()).hexdigest(),
                              'matrix': [list(row) for row in o.matrix_world]}
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pass-number',type=int,default=2,choices=(1,2))
    ap.add_argument('--width',type=int,default=1000)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--blend-path',type=Path)
    args = ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    out = args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    blend = (args.blend_path or out/'carol-blockout-v003.blend').resolve()
    assert blend not in (BASE.resolve(),old.V001.resolve())
    blend.parent.mkdir(parents=True,exist_ok=True)
    assert bpy.app.version == (5,2,1), bpy.app.version_string
    hashes = {str(p.relative_to(ROOT)):digest(p) for p in [BASE,old.V001,old.CANONICAL]}
    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    preserved = structural_fingerprint()
    for o in list(bpy.data.objects):
        if o.name.startswith(('Carol_Moon_Attached','Carol_Star_Attached','Carol_Review_')):
            bpy.data.objects.remove(o,do_unlink=True)
    shell = sculpt(args.pass_number)
    old.motifs(shell,bpy.data.materials['Diagnostic_Motifs'],bpy.data.objects['Carol_Model'])
    bpy.data.objects['Carol_Model']['stage']='v003 structural study / Human Gate pending'
    old.render_evidence(out,args.width)
    for view in old.VIEWS:
        (out/f'carol-v002-{view}.png').replace(out/f'carol-v003-{view}.png')
    checks = old.validate()
    assert structural_fingerprint() == preserved, 'v002 structural parts changed'
    checks['v002StructuralPartsByteIdentical']=True
    checks['preservedParts']=preserved
    bpy.ops.object.select_all(action='DESELECT')
    shell.select_set(True)
    bpy.context.view_layer.objects.active=shell
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    old.validate()
    assert structural_fingerprint()==preserved
    assert all(digest(ROOT/p)==h for p,h in hashes.items())
    manifest={'version':3,'pass':args.pass_number,'baselineCommit':'9ba1a188269e09ac4678a21254bd25ac8a1ffb59',
              'blender':bpy.app.version_string,'preservedHashes':hashes,'checks':checks,
              'blendSha256':digest(blend),'generatorSha256':digest(Path(__file__)),
              'helperSha256':digest(Path(old.__file__)),
              'historicalExcerptSha256':digest(ROOT/'docs/production/carol/evidence/blockout-v003/historical-fleece-excerpt.txt'),
              'renders':{v:digest(out/f'carol-v003-{v}.png') for v in old.VIEWS},
              'status':'awaiting Human Gate'}
    (out/'validation.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('V003 SAVED, REOPENED, VALIDATED',blend)


if __name__=='__main__': main()
