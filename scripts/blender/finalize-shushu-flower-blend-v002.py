"""Link the standalone item library into its own editable scene."""
import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[2];p=R/'assets/grimo/production/shushu/equipment/standard-v002/shushu-head-flower-v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects['Shushu_HeadFlower_v002'];assert root.parent is None
scene=bpy.context.scene
if scene is None:scene=bpy.data.scenes.new('Shushu_HeadFlower_v002')
for o in [root]+list(root.children):
 if o.name not in scene.objects:scene.collection.objects.link(o)
assert sum(o.type=='MESH' for o in scene.objects)==12
bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
print('FLOWER_EDITABLE_SCENE',len(scene.objects),flush=True)
