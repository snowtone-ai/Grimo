"""Front eye dark-silhouette dimensions normalized by whole-character height."""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v002'
report={'method':'Alpha >128 outline; dark eye silhouette max RGB <125 and min RGB <85 in separate eye ROIs. Normalize by full character height, retaining aspect ratio. Pixel/antialias uncertainty about one pixel.'}
for label,path in [('authority',ROOT/'assets/grimo/source/carol/approved-3d/carol_front.png'),('candidate',OUT/'front.png')]:
 im=Image.open(path).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox()
 x0,y0,x1,y1=box;w=x1-x0;h=y1-y0;eyes=[]
 for lo,hi in [(.29,.45),(.57,.73)]:
  pts=[(x,y) for y in range(round(y0+h*.49),round(y0+h*.71)) for x in range(round(x0+w*lo),round(x0+w*hi)) if max(im.getpixel((x,y))[:3])<125 and min(im.getpixel((x,y))[:3])<85]
  b=[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts)+1,max(y for x,y in pts)+1]
  eyes.append({'bbox_px':b,'width_over_height':(b[2]-b[0])/h,'height_over_height':(b[3]-b[1])/h})
 report[label]={'outline_bbox_px':box,'eyes':eyes}
report['relative_error_percent']=[{k:100*(c[k]/a[k]-1) for k in ['width_over_height','height_over_height']} for a,c in zip(report['authority']['eyes'],report['candidate']['eyes'])]
(OUT/'eye-measurements.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
