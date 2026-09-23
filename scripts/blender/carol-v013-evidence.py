"""Small technical-failure evidence package; never substitute wires for renders."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/reconstruction-v013'
REF=ROOT/'assets/grimo/source/carol/approved-3d'
WIRE=json.loads((ROOT/'tmp-carol-v013/wire.json').read_text())
RESULT=json.loads((OUT/'measurements.json').read_text())
FONT='C:/Windows/Fonts/arial.ttf'
def font(size):return ImageFont.truetype(FONT,size)
BG='#f4f3f0'
INK='#252d35'
RED='#b33d35'


def label(draw,xy,text,size=18,color=INK):
    draw.text(xy,text,font=font(size),fill=color)


def diagnostic():
    sheet=Image.new('RGB',(1200,1040),BG);d=ImageDraw.Draw(sheet)
    label(d,(24,18),'v013-A | TECHNICAL FAIL | NOT REVIEW READY',28)
    label(d,(24,59),'36 disjoint control-face intersections. Stopped before shaded Front / Side renders.',19)
    label(d,(24,88),'Reference thumbnails below are source images, not registered candidate comparisons.',17)
    for row,view in enumerate(('front','side')):
        y=145+row*320
        label(d,(24,y),'LOCKED Skin '+view.title(),21)
        src=Image.open(REF/('carol_skin_'+view+'.png')).convert('RGB')
        src.thumbnail((285,270))
        sheet.paste(src,(65+(285-src.width)//2,y+35))
        for col,title in [(1,'Candidate'),(2,'50% overlay')]:
            x=24+col*400
            label(d,(x,y),title,21)
            d.rounded_rectangle((x,y+40,x+350,y+282),radius=10,outline='#d2ccc4',width=2)
            label(d,(x+24,y+120),'NOT RUN',24,RED)
            label(d,(x+24,y+158),'Technical prerequisite failed',17)
    for col,title in [(0,'Derived 3Q'),(1,'Derived Top')]:
        x=24+col*590
        label(d,(x,803),title,21)
        label(d,(x,842),'NOT RUN - Front / Side not eligible',20,RED)
    label(d,(24,918),'825 vertices / 1,646 edges / 823 quads | 1 component | nonmanifold edges: 0',19)
    label(d,(24,950),'Rear / .575 interface and frozen objects: preserved after save / reload.',19)
    label(d,(24,982),'Motion probe: NOT RUN | Human Geometry Gate: NOT_REVIEW_READY | Phase B/C: NOT STARTED',17)
    sheet.save(OUT/'diagnostic-sheet.png')


def project(p,view):
    return (-p[1],p[2]) if view=='front' else (p[0],p[2])


def panel(sheet,box,view,bounds,evaluated=False):
    x,y,w,h=box
    canvas=Image.new('RGB',(w,h),'#fffefd');d=ImageDraw.Draw(canvas)
    u0,u1,v0,v1=bounds
    scale=min((w-26)/(u1-u0),(h-26)/(v1-v0))
    def xy(p):
        u,v=project(p,view)
        return ((w-scale*(u1-u0))/2+(u-u0)*scale,
                (h-scale*(v1-v0))/2+(v1-v)*scale)
    mesh=WIRE['evaluated' if evaluated else 'control']
    for a,b in mesh['edges']:
        pa,pb=mesh['vertices'][a],mesh['vertices'][b]
        # A raw orthographic wire projection: no backface/occlusion claims.
        if all(not (u0<=project(p,view)[0]<=u1 and v0<=p[2]<=v1) for p in (pa,pb)):
            continue
        d.line((xy(pa),xy(pb)),fill='#c2c6c7' if evaluated else '#728890',width=1)
    if not evaluated:
        for pair in RESULT['control_disjoint_intersections']['pairs']:
            for face in pair['faces']:
                if any(u0<=project(p,view)[0]<=u1 and v0<=p[2]<=v1 for p in face):
                    pts=[xy(p) for p in face]
                    d.line(pts+[pts[0]],fill=RED,width=2)
    sheet.paste(canvas,(x,y))


def structure():
    sheet=Image.new('RGB',(1440,1110),BG);d=ImageDraw.Draw(sheet)
    label(d,(24,18),'v013-A | STRUCTURE DIAGNOSTIC - WIRE ONLY',27)
    label(d,(24,56),'Red: saved intersection witnesses (first 12 of 36 pairs). All-depth wire projection; no shaded visual gate.',18)
    items=[('Front face','front',(-.34,.34,.23,.73)),
           ('Side face / cranial overlap','side',(-.01,.65,.23,.73)),
           ('Under-jaw transition','side',(.15,.66,.08,.40)),
           ('24-edge socket / orbit','front',(.04,.285,.295,.545)),
           ('J0 / J1 / C0 / C1 saddle','side',(.27,.66,.10,.58))]
    for i,(title,view,bounds) in enumerate(items):
        x=20+(i%3)*475;y=108+(i//3)*468
        label(d,(x,y),title,21)
        panel(sheet,(x,y+35,455,410),view,bounds)
    x,y=970,576
    label(d,(x,y),'Subdivision OFF / ON',21)
    bounds=(-.01,.42,.24,.63)
    panel(sheet,(x,y+35,220,410),'side',bounds)
    panel(sheet,(x+235,y+35,220,410),'side',bounds,True)
    label(d,(24,1050),'Subdivision evaluates; evaluated intersections and adjacent-contact audit were not run after cheap-gate failure.',18)
    label(d,(24,1080),'Diagnostic only. No geometry promotion, visual acceptance, motion-readiness claim or Human approval.',18)
    sheet.save(OUT/'structure-sheet.png')


diagnostic()
structure()
