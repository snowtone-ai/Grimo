"""Enforce explicit owner fills before accepting generated base colour.

input.png output.png fills.json. Every protected owner needs an explicit RGB
fill from the approved palette. Never infer skin/mouth/eye artwork from Tripo.
This intentionally discards any printed eye/open-mouth pattern on closed skin.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/rig-pretexture-technical-v003'
contract=json.loads((E/'paint-owner-mask.json').read_text());fills=json.loads(Path(sys.argv[3]).read_text());ids=contract['ids']
required=['lids-L','lids-R','mouth-skin','mouth-inner','tongue','teeth']
assert all(n in fills and len(fills[n])==3 and all(type(v)==int and 0<=v<=255 for v in fills[n]) for n in required),'Missing explicit approved owner fill'
mask=np.array(Image.open(E/'paint-owner-mask.png'));im=np.array(Image.open(sys.argv[1]).convert('RGB'));assert im.shape==(*mask.shape,3),'Resolution/atlas mismatch: HOLD'
for n in required:
    owner=mask==ids[n];dist=distance_transform_edt(~owner);region=dist<=4
    # Padding must never overwrite a neighbour's owned surface.
    assert not np.any(region&(mask!=0)&(~owner)),'Insufficient owner padding: HOLD'
    im[region]=fills[n]
Image.fromarray(im).save(sys.argv[2])
print('PROTECTED_OWNERS_FILLED',required,'palette_is_caller_authority',sys.argv[3])
