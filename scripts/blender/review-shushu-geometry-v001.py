"""Comparable source/candidate renders + two short evaluated timeline reviews."""
import bpy, sys, importlib, json
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
b=importlib.import_module('build-shushu-geometry-v001')

def main():
    bpy.ops.wm.open_mainfile(filepath=str(b.ASSET))
    s=bpy.context.scene;b.cam=s.camera
    char=[o for o in bpy.data.objects if o.name.startswith('Shushu_') and o.type=='MESH']
    s.frame_set(1)
    for o in char:o.hide_render=True
    archive=bpy.data.collections['SOURCE_B_REFERENCE_ONLY'];archive.hide_render=False
    raw=bpy.data.objects['SourceB_UntouchedTopology'];raw.hide_render=False
    white=b.material('Source same ivory',(.92,.865,.79));pink=b.material('Source same sakura',(.85,.36,.46));dark=b.material('Source eye plum',(.038,.017,.030),.26)
    raw.data.materials.clear()
    for mat in [white,pink,dark]:raw.data.materials.append(mat)
    for i,group in enumerate(b.donor.components(raw.data)):
        ids={j for f in group for j in raw.data.polygons[f].vertices}
        center=sum((raw.data.vertices[j].co for j in ids),start=__import__('mathutils').Vector())/len(ids)
        index=1 if i in [2,3,4,5,6,7,8,9] else 0
        if .58<center.z<.74 and center.y<-.12 and .05<abs(center.x)<.19 and i>=8:index=2
        for f in group:raw.data.polygons[f].material_index=index
    bpy.data.objects['Reachable_Holding_Proxy'].hide_render=True
    b.render('source-front',(0,-1,0));b.render('source-threequarter',(1,-1,.10));b.render('source-side',(1,0,0))
    archive.hide_render=True
    for o in char:o.hide_render=False
    # Render genuine sampled animation, with temporary frames kept outside the repository.
    import tempfile
    temp=Path(tempfile.gettempdir())/'grimo-shushu-v001-review';temp.mkdir(exist_ok=True)
    s.render.resolution_x=400;s.render.resolution_y=450
    sets={'face':[1,5,9,11,13,15,17,19,25,31,37,43,46,49],
          'support':[49,55,61,67,73,79,85]}
    files={}
    for family,frames in sets.items():
        paths=[]
        for frame in frames:
            s.frame_set(frame)
            b.render(f'{family}-f{frame:03d}',(0,-1,0) if family=='face' else (1,-2,.03),family=='face')
            p=b.OUT/'renders'/f'{family}-f{frame:03d}.png';dest=temp/p.name;p.replace(dest);paths.append(str(dest))
        files[family]=paths
    (temp/'frames.json').write_text(json.dumps(files))
    print('REVIEW_FRAMES',temp)

if __name__=='__main__':main()
