"""Evidence contact sheets and sampled Blender videos; no retouch or interpolation."""
import json,subprocess,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-skin-compat'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
def board(name,rows):
    cols=len(rows[0]);canvas=Image.new('RGB',(640*cols,680*len(rows)),(242,240,242));draw=ImageDraw.Draw(canvas)
    for r,row in enumerate(rows):
        for c,(label,path) in enumerate(row):
            draw.text((c*640+10,r*680+7),label,font=font,fill=(20,20,20));im=Image.open(OUT/path).convert('RGB');assert im.size==(640,640),(path,im.size);canvas.paste(im,(c*640,r*680+40))
    canvas.save(OUT/name)
board('A-five-paths.png',[
 [('Blender authored / f533 Side','blender-author/f533-side.png'),('Saved GLB in Blender / f533 Side','blender-saved/f533-side.png')]+[(label+' / f533 Side',f'phone-{mode}-lit-hold-both-side.png') for label,mode in [('PlayCanvas stock','stock'),('Eight-weight CPU oracle','full8'),('Local eight-weight candidate','local8')]],
 [('Blender authored / f549 3Q','blender-author/f549-3q.png'),('Saved GLB in Blender / f549 3Q','blender-saved/f549-3q.png')]+[(label+' / f549 3Q',f'phone-{mode}-lit-half-hold-3q.png') for label,mode in [('PlayCanvas stock','stock'),('Eight-weight CPU oracle','full8'),('Local eight-weight candidate','local8')]]])
board('A-lighting-normal-separation.png',[[('Lit / '+mode,f'phone-{mode}-lit-half-hold-side.png'),('Texture without lighting / '+mode,f'phone-{mode}-unlit-half-hold-side.png'),('World normal / '+mode,f'phone-{mode}-normal-half-hold-side.png')] for mode in ['stock','full8','local8']])
mouth=[('Closed f333','mouth-closed',333),('Small mixed f345','mouth-small',345),('Medium f349','mouth-medium',349),('Large f357','mouth-large',357)]
board('B-closed-to-open.png',[[('Blender / '+label,f'blender-author/f{f}-front.png') for label,name,f in mouth],[('Phone local8 / '+label,f'phone-local8-lit-{name}-front.png') for label,name,f in mouth]])
ffmpeg=shutil.which('ffmpeg')
for kind in ['author','saved']:
 for view in ['side','3q']:
    seq=OUT/f'blender-{kind}'/f'arm-{view}-concat.txt'
    lines=[]
    for f in range(505,542,3):lines.extend([f"file 'f{f}-{view}.png'",'duration 0.125'])
    lines.append(f"file 'f541-{view}.png'");seq.write_text('\n'.join(lines)+'\n')
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(seq),'-fps_mode','vfr','-c:v','libx264','-pix_fmt','yuv420p',str(OUT/f'blender-{kind}-arm-{view}-sampled8fps.mp4')],check=True)
print('BOARDS_AND_SAMPLED_VIDEOS_DONE')
