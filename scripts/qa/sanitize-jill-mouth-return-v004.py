"""v003 protected-owner fill plus the corrected exposed host-mouth skin.

input.png output.png fills.json; explicit mouth-host-skin == mouth-skin required.
4K only. Approved palette must be supplied by the caller; no real texture here.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/mouth-profile-v004';OLD=ROOT/'docs/production/jill/rig-pretexture-technical-v003'
fills=json.loads(Path(sys.argv[3]).read_text());assert fills.get('mouth-host-skin')==fills.get('mouth-skin') and 'mouth-host-skin' in fills,'Explicit same approved host/mouth skin colour required: HOLD'
source=(ROOT/'scripts/qa/sanitize-jill-return-v003.py').read_text(encoding='utf8');exec(compile(source,str(ROOT/'scripts/qa/sanitize-jill-return-v003.py'),'exec'),{'__file__':str(ROOT/'scripts/qa/sanitize-jill-return-v003.py'),'__name__':'__main__'})
mask=np.array(Image.open(E/'mouth-host-fill-mask.png'))>0;owner=np.array(Image.open(OLD/'paint-owner-mask.png'));ids=json.loads((OLD/'paint-owner-mask.json').read_text())['ids']
region=distance_transform_edt(~mask)<=4
assert not np.any(region&~np.isin(owner,[0,ids['body_skin'],ids['mouth-skin']])),'Host fill crosses a protected owner: HOLD'
im=np.array(Image.open(sys.argv[2]).convert('RGB'));im[region]=fills['mouth-host-skin'];Image.fromarray(im).save(sys.argv[2]);assert np.all(im[mask]==fills['mouth-host-skin'])
print('HOST_MOUTH_FILL_PASS',int(mask.sum()),'synthetic unless caller supplies approved palette')
