"""Arrange actual renders without image retouching. Run with Pillow Python."""
from pathlib import Path
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[2]
e=root/'docs/production/jill/evidence/tripo-input-v002'
board=Image.new('RGB',(1440,1536),'#eef0e9'); d=ImageDraw.Draw(board)
for row,label in enumerate(['source','fbx','glb']):
    for col,view in enumerate(['front','side','three-quarter']):
        x=col*480; y=row*512
        d.text((x+12,y+8),f'{label} / {view} / Geometry HOLD',fill='#202820')
        board.paste(Image.open(e/f'{label}-{view}.jpg'),(x,y+32))
board.save(e/'roundtrip-board.jpg',quality=96)
