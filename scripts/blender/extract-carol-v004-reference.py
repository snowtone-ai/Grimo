"""Extract literal authored design data, never execute the historical builder.

Usage: python scripts/blender/extract-carol-v004-reference.py --repository ../task-plant
"""
import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHA = '15bfa8e4c3a8ba24c246fe806bd125b307d8f076'
SOURCE = 'scripts/grimo/build-carol-reference.py'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', required=True)
    args = parser.parse_args()
    raw = subprocess.check_output(['git', '-C', args.repository, 'show', f'{SHA}:{SOURCE}'])
    tree = ast.parse(raw.decode())
    data = {'repository': 'snowtone-ai/grimoire', 'commit': SHA, 'source': SOURCE,
            'sourceSha256': hashlib.sha256(raw).hexdigest(), 'sourceResolution': [624, 400]}
    keys = {'HEAD', 'FACE', 'EAR_L', 'EAR_R', 'BODY_OUTLINE', 'BODY_LOCKS', 'HEAD_LOCKS', 'eye_centers', 'moon_center'}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in keys:
                    data[target.id] = ast.literal_eval(node.value)
    data['features'] = {
        'eyeBasis': [[.947, -.322], [.322, .947]],
        'eyeLineDegreesSource': -18.96,
        'eyeWarpInfluenceRadii_NOT_visibleEyeRadii': [36,40],
        'eyeVisibleRadii': [[18,24],[18,24]],
        'eyeVisibleRadiiProvenance': 'New manual approximation from canonical pixels; historical eyes are painted, not independent geometry.',
        'mouthCenter': [431,254], 'noseCenter': [431,242],
        'noseProvenance': 'Manual canonical pixel estimate, not a historical mesh landmark.',
        'cheekCenters': [[359,271],[496,234]],
        'cheekProvenance': 'Manual canonical pixel estimate; blush, not a long muzzle.',
        'earRoots': [[304,246],[519,186]], 'earCenters': [[268,271],[544,192]],
        'innerEarSource': 'Source-derived opaque volume paint. No separate trace in historical builder.',
        'innerEarTraces': [[[236,285],[258,278],[280,269],[301,250],[294,274],[277,287],[255,292]],
                           [[520,195],[539,193],[561,181],[568,181],[557,201],[539,213],[526,211]]],
        'innerEarTraceProvenance': 'New manual traces from canonical pixels, separately authored per side.',
        'mouthTrace': [[422,255],[431,259],[441,250],[441,263],[436,273],[428,273],[423,266]],
        'mouthTraceProvenance': 'New canonical pixel trace; historical mouth is source paint with pivot at 431,254.',
        'fringe': 'HEAD_LOCKS and HEAD outline; no separately authored fringe mesh.',
        'stars': [['CrownStar',361,137,25],['TopStar',314,67,23],['WoolStar',184,287,23],['ChestStar',443,322,19],['LowerStar',302,332,14]],
        'recess': {'center':[426,242],'radii':[70,58],'power':4,'historicalDepth':.17},
        'paletteSource': 'back_paint / volume_paint: cream skin, cocoa/rose ears, ivory-blue-lavender fleece, warm gold. Diagnostic swatches only; no UV/material lock.'}
    data['mapping'] = {
        'sourceBounds': [0,0,624,400], 'bodyBounds': [93,8,539,380],
        'faceBounds': [337,175,512,302], 'earRoots': [[304,246],[519,186]],
        'normalizedFront': 'u=(x-324)/446; v=(380-y)/372',
        'blenderFront': 'X=u*3.2112; Z=0.37+v*2.604; front=-Y, up=+Z',
        'scaleX': .0072, 'scaleZ': .007, 'originSource': [324,380], 'groundOffset': .37,
        'depth': 'Independent Full-3D volume, not source depth copied in pixel units.',
        'interpretation': 'Retain source-specific angled front composition. This is a proposed neutral identity interpretation, subject to HUMAN Gate.'}
    out = ROOT/'scripts/blender/carol-v004-reference-data.json'
    out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(out)

if __name__ == '__main__': main()
