"""Single neutral-clay diagnostic renders, consistent cameras and lighting."""
import sys,importlib,bpy
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
c=importlib.import_module('check-shushu-geometry-v002');b=c.b
c.init(b.ASSET)
s=bpy.context.scene;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.75,.75,.75,1)
if '--face-only' in sys.argv:
 for name in ['neutral','half','closed','mouth-open']:
  b.state(name);b.render('face-'+name,(0,-1,.02),True)
 sys.exit(0)
for name,d in [('front',(0,-1,.08)),('side',(1,0,.08)),('rear',(0,1,.08)),('three-quarter',(1,-2,.10))]:
 b.state('neutral');b.render('neutral-'+name,d)
for name in ['neutral','half','closed','left-closed','mouth-open','smile','surprise','combined']:
 b.state(name);b.render('face-'+name,(0,-1,.02),True)
for name in ['neutral','closed']:
 b.state(name);b.render('face-'+name+'-three-quarter',(1,-2,.02),True)
for name in ['rest','seat','offer','hold','hold-touch','head-turn','groom','chest-groom','pressure']:
 b.state(name);b.render(name,(1,-2,.12))
for name in ['rest','seat']:
 b.state(name);b.render(name+'-front');b.render(name+'-side',(1,0,.08))
# Identical inspection cameras/light for source B and the superseded v001 face.
for o in b.character:o.hide_render=True
b.proxy.hide_render=True;b.proxy.hide_viewport=True
archive=bpy.data.collections['SOURCE_B_REFERENCE_ONLY'];archive.hide_viewport=False;archive.hide_render=False
raw=bpy.data.objects['SourceB_UntouchedTopology'];raw.data.materials.clear();raw.data.materials.append(bpy.data.materials['Diagnostic neutral clay'])
for name,d in [('front',(0,-1,.08)),('side',(1,0,.08)),('rear',(0,1,.08)),('three-quarter',(1,-2,.10))]:
 b.render('donor-'+name,d)
b.render('donor-face',(0,-1,.02),True)
raw.hide_render=True
with bpy.data.libraries.load(str(b.ROOT/'assets/grimo/production/shushu/blender/shushu-geometry-v001.blend'),link=False) as (src,dst):
 dst.objects=[n for n in src.objects if n.startswith('Shushu_')]
for o in dst.objects:
 if o is None:continue
 s.collection.objects.link(o)
 if o.type=='MESH':
  o.data.materials.clear();o.data.materials.append(bpy.data.materials['Diagnostic neutral clay'])
  if o.data.shape_keys:
   o.data.shape_keys.animation_data_clear()
   for k in o.data.shape_keys.key_blocks:k.value=0
 elif o.type=='ARMATURE':
  o.animation_data_clear()
  for p in o.pose.bones:p.matrix_basis.identity()
b.render('v001-front');b.render('v001-face',(0,-1,.02),True)
