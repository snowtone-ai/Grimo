"""Encode Blender's streamed diagnostic renders in memory, without frame files."""
import sys,json,struct,io
from PIL import Image,ImageDraw,ImageFont

def read(n):
    data=bytearray()
    while len(data)<n:
        chunk=sys.stdin.buffer.read(n-len(data))
        if not chunk:raise EOFError('Incomplete render stream')
        data.extend(chunk)
    return bytes(data)

def main():
    frames=[];font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
    while True:
        header=json.loads(sys.stdin.buffer.readline())
        if header.get('end'):break
        board=Image.new('RGB',(1080,400),(28,32,39));d=ImageDraw.Draw(board)
        d.text((10,8),header['label']+' | FRONT / SIDE / 3Q | diagnostic colors | Human Gate PENDING',font=font,fill='white')
        for col in range(3):
            image=Image.open(io.BytesIO(read(struct.unpack('<I',read(4))[0]))).convert('RGB');board.paste(image,(col*360,35))
        frames.append(board);print('ok',flush=True)
    palette=frames[0].quantize(colors=256);frames=[p.quantize(palette=palette) for p in frames]
    frames[0].save(sys.argv[1],save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True,disposal=2)

if __name__=='__main__':main()
