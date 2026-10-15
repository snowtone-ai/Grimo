"""Evidence layout only: untouched render pixels, explicit overview resizing."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
def load(p):return Image.open(OUT/p).convert('RGB')
def grid(name,rows,columns,tile=640):
    board=Image.new('RGB',(len(columns)*tile,len(rows)*(tile+32)),(243,239,240));d=ImageDraw.Draw(board)
    for y,(label,prefix) in enumerate(rows):
        for x,(view,suffix) in enumerate(columns):
            im=load(prefix+suffix+'.png')
            if tile!=640:im=im.resize((tile,tile),Image.Resampling.LANCZOS)
            board.paste(im,(x*tile,y*(tile+32)+32));d.text((x*tile+8,y*(tile+32)+5),label+' / '+view,font=font,fill=(35,28,32))
    board.save(OUT/name)
states=['closed','small','medium','large'];views=['front','side','3q']
for kind in ['author','saved','runtime','geometry-clay','before']:
    grid(kind+'-states-native.png',[(s,kind+'/'+s+'-') for s in states],[(v,v) for v in views])
# Four stages in each view; 320px overview and a separate native mouth crop.
stages=['before','author','saved','runtime']
board=Image.new('RGB',(1280,3*352),(243,239,240));d=ImageDraw.Draw(board)
for y,v in enumerate(views):
    for x,k in enumerate(stages):
        p=f'{k}/closed-{v}.png';board.paste(load(p).resize((320,320),Image.Resampling.LANCZOS),(x*320,y*352+32));d.text((x*320+8,y*352+5),k+' / '+v,font=font,fill='black')
board.save(OUT/'closed-before-after-overview.png')
crops={'front':(230,340,410,490),'side':(460,340,640,490),'3q':(395,335,575,485)}
board=Image.new('RGB',(4*260,3*200),(243,239,240));d=ImageDraw.Draw(board)
for y,v in enumerate(views):
    for x,k in enumerate(stages):
        board.paste(load(f'{k}/closed-{v}.png').crop(crops[v]),(x*260+40,y*200+35));d.text((x*260+5,y*200+5),k+' / '+v,font=font,fill='black')
board.save(OUT/'closed-mouth-crops-native.png')
grid('seated-preservation-native.png',[(k+' '+s,k+'/'+s+'-') for s in ['seated-closed','seated-large'] for k in ['before-full','candidate-full']],[(v,v) for v in views])
# Generated reference remains separate from rendered evidence and never edits it.
ref=load('closed-mouth-model-v001.png');ref.thumbnail((1280,850))
board=Image.new('RGB',(1280,ref.height+32+3*352),(243,239,240));d=ImageDraw.Draw(board);d.text((8,5),'Generated closed-mouth model / mouth only, qualitative target',font=font,fill='black');board.paste(ref,((1280-ref.width)//2,32))
off=ref.height+32
for y,k in enumerate(['geometry-clay','author','runtime']):
    for x,v in enumerate(views):
        board.paste(load(f'{k}/closed-{v}.png').resize((320,320),Image.Resampling.LANCZOS),(x*420+50,off+y*352+32));d.text((x*420+50,off+y*352+5),k+' / '+v,font=font,fill='black')
board.save(OUT/'model-vs-closed-overview.png')
cards=[]
for kind in ['author','saved','runtime','before','geometry-clay']:
    body=''.join(f'<figure><a href="{kind}/{s}-{v}.png"><img loading="lazy" src="{kind}/{s}-{v}.png"></a><figcaption>{s} / {v} · 640×640原寸リンク</figcaption></figure>' for s in states for v in views)
    cards.append(f'<section><h2>{kind}</h2><div class="grid">{body}</div></section>')
page='''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shushu 口B v001 review</title><style>body{font:16px system-ui;background:#f3eff0;color:#302830;margin:24px auto;max-width:1200px;padding:0 16px}h1{font-size:28px}a{color:#784550}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}figure{margin:0}img,video{width:100%;height:auto;border-radius:6px}figcaption{padding:5px}section{margin-top:38px}.tag{background:#e8d7db;padding:12px;border-radius:8px} @media(max-width:700px){.grid{grid-template-columns:1fr}}</style><h1>Shushu v004 · 口B v001</h1><p class="tag">Human判定待ち / 原本置換・Motion量産 HOLD。PC比較まで。閉口基準 → 造形 → Textureの順で作成。</p><p><a href="REVIEW.md">変更範囲・検証・Human確認項目</a> · <a href="runtime.html">PlayCanvas local操作</a> · <a href="closed-mouth-crops-native.png">閉口の原寸切抜き比較</a></p><h2>生成モデルとの比較</h2><a href="model-vs-closed-overview.png"><img src="model-vs-closed-overview.png"></a><p>生成画像は口の設計参照。目・頭形などの生成差分は採用していない。比較画像は縮小overview、原寸レンダーは下記リンク。</p><h2>閉口の前後</h2><a href="closed-before-after-overview.png"><img src="closed-before-after-overview.png"></a><h2>連続性 · PlayCanvas実描画</h2><div class="grid">'''
page+=''.join(f'<figure><video controls loop preload="metadata" src="runtime/closed-open-closed-{v}.webm"></video><figcaption>{v} · closed → open → closed</figcaption></figure>' for v in views)+'</div>'+''.join(cards)
page+='<section><h2>座位保持 · 同条件の原本 / 候補</h2><a href="seated-preservation-native.png"><img loading="lazy" src="seated-preservation-native.png"></a></section></html>'
(OUT/'index.html').write_text(page,encoding='utf8')
if shutil.which('ffmpeg'):
    for v in views:
        video=OUT/'runtime'/f'closed-open-closed-{v}.webm'
        duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(video)]))
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),'-vf',f'fps={12/duration},scale=320:320,tile=4x3','-frames:v','1',str(OUT/f'transition-{v}-contact.png')],check=True)
print('BOARDS_READY')
