"""Compose the six rendered probe beats and 5-second review video."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
import sys

root = Path(sys.argv[1])
folder = root / 'docs/production/carol/evidence/hero-experience-probe-v001'
authority = root / 'assets/grimo/source/carol/approved-3d/carol_front.png'
comparison = Image.new('RGB',(1440,800),'#f7f6fb')
cdraw = ImageDraw.Draw(comparison)
cmp_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',27)
for i,(label,file) in enumerate([('Approved Normal Front',authority),('Attempt 2 / fixed Hero neutral',folder/'hero-neutral.png')]):
    source = Image.open(file).convert('RGBA')
    source.thumbnail((680,690))  # Uniform scaling only; authority aspect is preserved.
    tile = Image.new('RGBA',source.size,'white')
    tile.alpha_composite(source)
    x = i*720 + (720-source.width)//2
    y = 64 + (700-source.height)//2
    comparison.paste(tile.convert('RGB'),(x,y))
    cdraw.text((i*720+24,18),label,font=cmp_font,fill='#302c3c')
comparison.save(folder/'hero-neutral-comparison.png')
beats = [('Neutral','hero-neutral.png'), ('Immediate / local ACK','frame-ack.png'),
         ('Head commitment','frame-head.png'), ('Peak cheek lean','frame-peak.png'),
         ('Settle','frame-settle.png'), ('Afterglow','frame-afterglow.png')]
sheet = Image.new('RGB',(1080,780),'#f7f6fb')
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',25)
for i,(label,file) in enumerate(beats):
    img=Image.open(folder/file).convert('RGB')
    img.thumbnail((344,344))
    x=(i%3)*360+8; y=(i//3)*390+8
    sheet.paste(img,(x,y+34))
    draw.text((x+8,y),label,font=font,fill='#302c3c')
sheet.save(folder/'hero-contact-sheet.png')

frames=sorted(folder.glob('motion-*.png'))
assert len(frames)==60, len(frames)
playlist=folder/'motion-concat.txt'
playlist.write_text(''.join(f"file '{f.as_posix()}'\nduration 0.0833333333\n" for f in frames)+f"file '{frames[-1].as_posix()}'\n",encoding='utf-8')
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(playlist),
                '-fps_mode','cfr','-r','24','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',
                '-movflags','+faststart',str(folder/'hero-motion.mp4')],check=True)
playlist.unlink()
for file in frames: file.unlink()
for _,file in beats[1:]: (folder/file).unlink()
print('EVIDENCE_COMPLETE',folder/'hero-motion.mp4',folder/'hero-contact-sheet.png')
