"""Compact review sheets, preserving image aspect ratio and documenting display mirroring."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v001'
REF=ROOT/'assets/grimo/source/carol/approved-3d'
FONT=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',23)
SMALL=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)

def tile(path,mirror=False,size=650):
 im=Image.open(path).convert('RGBA')
 bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB')
 if mirror:im=ImageOps.mirror(im)
 im.thumbnail((size,size),Image.Resampling.LANCZOS)
 canvas=Image.new('RGB',(size,size),'white');canvas.paste(im,((size-im.width)//2,(size-im.height)//2));return canvas

def board(name,rows,footer):
 width=1300; height=len(rows)*710+65
 im=Image.new('RGB',(width,height),'white');d=ImageDraw.Draw(im)
 for y,row in enumerate(rows):
  for x,(label,path,mirror) in enumerate(row):
   d.text((x*650+18,y*710+12),label,font=FONT,fill='#302d40')
   im.paste(tile(path,mirror),(x*650,y*710+45))
 d.text((18,height-50),footer,font=SMALL,fill='#494357')
 im.save(OUT/name)

board('01-authority-comparison.jpg',[
 [('Approved Normal Front',REF/'carol_front.png',False),('Saved candidate — Front',OUT/'front.png',False)],
 [('Approved Normal Side',REF/'carol_side.png',False),('Moon side — display mirrored to source facing',OUT/'side.png',True)]
 ],'Only the side render is mirrored for comparison. Original native camera images remain available. No geometry changes by view.')
board('02-spatial-review.jpg',[
 [('Same asset — three-quarter',OUT/'3q.png',False),('Same asset — rear three-quarter',OUT/'rear.png',False)],
 [('Same asset — top',OUT/'top.png',False),('Same asset — opposite side',OUT/'opposite_side.png',False)]
 ],'Derived views are diagnostics, not additional visual authorities. Neutral geometry is identical in all cameras.')
board('03-deformation-samples.jpg',[
 [('Neutral Front',OUT/'front.png',False),('Left face-frame local compression',OUT/'diagnostic-cheek-compress.png',False)],
 [('Opening corrective sample (no head acting)',OUT/'diagnostic-opening.png',False),('Independent tail +20 degrees',OUT/'diagnostic-tail.png',True)]
 ],'Bounded geometry samples only; not a production rig, finished Face-in-Fleece behavior, motion approval, or Human Gate PASS.')
