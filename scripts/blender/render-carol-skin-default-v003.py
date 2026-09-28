"""Matched diagnostic renders from saved sources, including temporary v004 occlusion."""
import importlib.util
import sys
from pathlib import Path

import bpy

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'assets/grimo/production/carol/blender'
OUT = ROOT / 'docs/production/carol/evidence/skin-default-v003'
spec = importlib.util.spec_from_file_location('ear_util', Path(__file__).with_name('build-carol-ear-production-v002.py'))
util = importlib.util.module_from_spec(spec)
spec.loader.exec_module(util)
SKIN = {'CENTRAL_CHASSIS','EAR_L','EAR_R','EYELID_L','EYELID_R','EYE_L','EYE_R',
        'FORE_L','FORE_R','HIND_L','HIND_R','HOOF_FORE_L','HOOF_FORE_R',
        'HOOF_HIND_L','HOOF_HIND_R','NOSE','SKIN_TAIL_CORE','MOUTH_closed','PHILTRUM'}
FLEECE = {'HeadFleece','BodyFleece','HeadFleeceBacking','TailFleece'}
VIEWS = [
    ('front',(-4,0,0),(.52,0,.395),1.29),
    ('side',(0,-4,0),(.53,0,.395),1.34),
    ('front-3q',(-4,-2,.35),(.52,0,.395),1.34),
]


def open_scene(name):
    bpy.ops.wm.open_mainfile(filepath=str(ASSETS/name))
    # All comparisons use the same v004 fixtures and world strength.
    if name != 'carol-normal-fleece-v004.blend':
        for ob in list(bpy.context.scene.objects):
            if ob.type == 'LIGHT':
                bpy.data.objects.remove(ob,do_unlink=True)
        with bpy.data.libraries.load(str(ASSETS/'carol-normal-fleece-v004.blend'),link=False) as (src,dst):
            dst.objects = ['Key','Fill','Rear','Low']
        for ob in dst.objects:
            bpy.context.scene.collection.objects.link(ob)
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.samples=16
    scene.cycles.use_denoising=True
    scene.render.use_compositing=False
    scene.view_settings.view_transform='AgX'
    if scene.world and scene.world.use_nodes:
        background=next((n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND'),None)
        if background:
            background.inputs['Strength'].default_value=.5
    scene.frame_set(1)


def render_set(label,visible,close=False):
    util.TMP=OUT/label
    util.TMP.mkdir(parents=True,exist_ok=True)
    for name,direction,target,scale in VIEWS:
        if label not in {'new-skin','fleece-occlusion'} and (util.TMP/(name+'.png')).exists():
            continue
        print('RENDER',label,name,flush=True)
        util.render(name,direction,target,scale,visible,size=(760,670))
    if close:
        for name,direction,target,scale in [
            ('ear-side',(0,-4,0),(.47,-.30,.535),.65),
            ('ear-top',(0,0,4),(.49,-.40,.52),.58)]:
            if label != 'new-skin' and (util.TMP/(name+'.png')).exists():
                continue
            print('RENDER',label,name,flush=True)
            util.render(name,direction,target,scale,visible,size=(760,670))


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if '--close-only' in sys.argv:
        open_scene('carol-skin-default-v003.blend')
        util.TMP=OUT/'new-skin'
        util.render('ear-side',(0,-4,0),(.47,-.30,.535),.65,SKIN,size=(760,670))
        return
    for label,asset,close in [
        ('old-skin','carol-skin-final-v002.blend',False),
        ('v004-internal-skin','carol-normal-fleece-v004.blend',False),
        ('ear-v001','carol-skin-ear-correction-v001.blend',True),
        ('new-skin','carol-skin-default-v003.blend',True),
    ]:
        open_scene(asset)
        render_set(label,SKIN,close)
    open_scene('carol-normal-fleece-v004.blend')
    with bpy.data.libraries.load(str(ASSETS/'carol-skin-default-v003.blend'),link=False) as (src,dst):
        dst.objects=['EAR_L','EAR_R']
    for source in dst.objects:
        target=bpy.data.objects[source.name.removesuffix('.001')]
        target.data=source.data.copy()
        bpy.data.objects.remove(source,do_unlink=True)
    render_set('fleece-occlusion',SKIN|FLEECE)


if __name__=='__main__':
    main()
