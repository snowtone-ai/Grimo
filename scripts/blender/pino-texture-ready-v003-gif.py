"""Continuous representative transitions; one temporary PNG, streamed GIFs."""
import bpy,sys,subprocess,json,struct,importlib.util,hashlib
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sp=importlib.util.spec_from_file_location('v3',ROOT/'scripts/blender/pino-texture-ready-v003.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)

def run():
    python=sys.argv[sys.argv.index('--gif-python')+1]
    bpy.ops.wm.open_mainfile(filepath=str(v.DEST/'pino-c-texture-ready-v003-HOLD.blend'));o=bpy.data.objects['PINO_C_BASE_RIG_V001'];lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']];sc=bpy.context.scene;v.f.display(sc,360)
    for name,col in [('Pino_Eye_L',(.025,.10,.20,1)),('Pino_Eye_R',(.025,.10,.20,1)),('Pino_OralInterior',(.03,.018,.018,1))]:bpy.data.materials[name].diffuse_color=col
    sequences={
        'mouth-cycle':[(1,0,0,0),(0,0,0,0),(0,1,0,0),(0,0,0,0),(1,0,0,0)],
        'eyes-combined':[(0,0,0,0),(0,0,1,0),(0,0,0,0),(0,0,0,1),(0,0,0,0),(0,0,1,1),(1,0,.5,1),(0,0,1,1),(0,1,1,1),(0,0,0,0)]}
    manifest={};temporary=v.TMP/'stream-frame.png'
    for name,waypoints in sequences.items():
        frames=[waypoints[0]]
        for a,b in zip(waypoints,waypoints[1:]):
            frames.extend([tuple(np.array(a)*(1-t)+np.array(b)*t) for t in np.linspace(0,1,9)[1:]])
        frames.extend([waypoints[-1]]*3);manifest[name]=[list(p) for p in frames]
        child=subprocess.Popen([python,str(ROOT/'scripts/3d/encode-pino-proof-gif.py'),str(v.OUT/(name+'.gif'))],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        for i,args in enumerate(frames):
            v.state(o,lids,*args);label=f'{name}  {i+1}/{len(frames)}  c={args[0]:.2f} large={args[1]:.2f} L={args[2]:.2f} R={args[3]:.2f}'
            child.stdin.write((json.dumps({'label':label})+'\n').encode())
            for view in ['front','side','3q']:
                v.f.view(sc,view);v.f.render(sc,temporary);data=temporary.read_bytes();child.stdin.write(struct.pack('<I',len(data)));child.stdin.write(data)
            child.stdin.flush()
            if child.stdout.readline().strip()!=b'ok':raise RuntimeError('GIF encoder rejected a frame')
        child.stdin.write(b'{"end":true}\n');child.stdin.close()
        if child.wait()!=0:raise RuntimeError('GIF encoding failed')
    temporary.unlink(missing_ok=True)
    (v.OUT/'transition-controls.json').write_text(json.dumps({'master_sha256':hashlib.sha256((v.DEST/'pino-c-texture-ready-v003-HOLD.blend').read_bytes()).hexdigest(),'frame_ms':80,'controls_c_large_L_R':manifest,'storage':'one temporary PNG overwritten; GIF frames encoded in memory'},indent=2)+'\n',encoding='utf8')

if __name__=='__main__':run()
