"""Current-image measurements and masks. Run with the existing desktop Python."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_fill_holes, binary_closing, distance_transform_edt, gaussian_filter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/production/carol/evidence/normal-fleece-v004'
WORK = ROOT / 'artifacts/carol-fleece-v004'
REF = ROOT / 'assets/grimo/source/carol/approved-3d'

# Measured on the current 1254x1254 Front; each row is center, radii, orientation,
# relative depth, region. No historical lock coordinates are used.
FRONT = [
 (627,211,84,64,0,.060,'crown'), (530,205,70,47,-15,.047,'crown'),
 (726,208,67,47,15,.047,'crown'), (420,237,89,57,-15,.065,'crown'),
 (832,238,89,57,15,.065,'crown'), (304,304,70,70,-30,.065,'crown'),
 (948,304,69,70,30,.065,'crown'), (490,257,60,57,-20,.048,'crown'),
 (758,256,63,57,20,.048,'crown'), (555,274,86,81,-20,.060,'crown'),
 (700,274,86,81,20,.060,'crown'), (382,291,49,39,-25,.040,'crown'),
 (426,320,53,53,-15,.043,'crown'), (867,291,49,39,25,.040,'crown'),
 (822,320,53,53,15,.043,'crown'), (487,331,49,45,-20,.040,'crown'),
 (766,331,49,45,20,.040,'crown'), (569,353,81,67,-20,.065,'crown'),
 (680,348,80,68,20,.065,'crown'),
 (241,392,67,63,-35,.052,'flank'), (1014,394,65,63,35,.052,'flank'),
 (189,440,41,48,-15,.030,'flank'), (1065,441,42,48,15,.030,'flank'),
 (164,504,68,71,-15,.054,'flank'), (1090,504,68,71,15,.054,'flank'),
 (133,590,70,65,-30,.045,'flank'), (1123,590,70,65,30,.045,'flank'),
 (110,674,73,67,-30,.055,'flank'), (1142,674,73,67,30,.055,'flank'),
 (161,832,83,59,-20,.045,'flank'), (1094,832,83,59,20,.045,'flank'),
 (181,902,70,64,10,.040,'flank'), (1077,902,70,64,-10,.040,'flank'),
 (229,981,61,65,-25,.047,'belly'), (1029,981,70,68,25,.047,'belly'),
 (311,1030,74,57,-15,.045,'belly'), (946,1026,72,58,15,.045,'belly'),
 (413,1031,57,48,10,.032,'belly'), (844,1030,58,48,-10,.032,'belly'),
 (548,1055,64,55,-15,.049,'belly'), (671,1055,72,54,15,.049,'belly'),
 (292,374,66,55,-20,.054,'blue_flank'), (409,382,78,63,-20,.060,'blue_flank'),
 (385,445,80,61,15,.059,'blue_flank'), (264,470,69,70,-10,.054,'blue_flank'),
 (478,416,57,46,10,.040,'blue_flank'), (455,475,48,52,0,.044,'blue_flank'),
 (207,535,54,63,-10,.043,'blue_flank'), (257,593,73,60,0,.045,'blue_flank'),
 (326,591,51,50,0,.039,'blue_flank'),
 (586,416,67,66,-20,.062,'head'), (666,412,69,66,20,.062,'head'),
 (765,407,98,66,-12,.064,'head'), (900,395,102,74,15,.058,'head'),
 (905,465,69,73,-15,.052,'head'), (992,476,58,58,-10,.057,'head'),
 (845,499,75,77,0,.065,'head'), (779,558,85,72,-15,.068,'head'),
 (715,568,55,65,10,.055,'head'), (614,554,66,79,10,.070,'head'),
 (550,537,57,81,30,.060,'head'), (479,512,46,59,-15,.055,'head'),
 (486,570,31,33,-15,.028,'head'), (413,596,59,47,15,.050,'head'),
 (328,631,55,52,-20,.044,'head'), (383,655,53,48,15,.052,'head'),
 (357,716,40,37,0,.028,'head'), (335,781,59,48,20,.052,'head'),
 (297,846,45,45,-10,.031,'head'), (355,861,52,53,-15,.050,'head'),
 (427,948,65,59,-20,.052,'head'), (504,981,58,52,25,.049,'head'),
 (577,976,46,45,0,.040,'head'), (696,976,48,46,0,.041,'head'),
 (772,979,62,60,-20,.052,'head'), (866,947,67,60,20,.054,'head'),
 (941,990,58,55,20,.037,'belly'), (969,881,63,58,20,.042,'head'),
 (960,781,58,50,-20,.052,'head'), (958,718,40,34,0,.027,'head'),
 (969,645,70,50,-20,.058,'head'), (916,585,69,57,-20,.058,'head'),
 (1024,577,56,49,-10,.040,'flank'), (1100,551,43,40,-10,.034,'flank'),
]

SIDE = [
 (655,159,139,80,0,.065,'crown'), (499,204,100,72,-15,.060,'crown'),
 (370,261,96,79,-25,.058,'crown'), (246,342,98,75,-30,.056,'head'),
 (172,463,64,73,-10,.055,'head'), (277,433,76,71,0,.060,'head'),
 (384,377,94,77,-20,.065,'head'), (358,474,73,55,10,.055,'head'),
 (478,409,93,77,0,.067,'head'), (565,456,85,75,10,.064,'head'),
 (460,548,79,57,-30,.060,'head'), (463,666,80,64,10,.060,'head'),
 (434,765,59,67,0,.050,'head'), (353,844,91,73,0,.056,'chest'),
 (440,850,70,63,0,.049,'chest'), (277,796,51,59,0,.040,'chest'),
 (585,796,101,102,-20,.063,'belly'), (650,867,69,58,0,.045,'belly'),
 (755,840,90,86,0,.060,'belly'), (830,872,61,53,0,.040,'belly'),
 (919,800,87,98,-20,.060,'rump'), (1052,804,91,95,-20,.060,'rump'),
 (1150,742,65,80,10,.055,'rump'), (1066,588,129,94,10,.070,'rump'),
 (944,646,107,94,-10,.061,'rump'), (813,723,70,86,-10,.053,'flank'),
 (1104,473,65,64,0,.050,'back'), (990,362,83,82,0,.058,'back'),
 (842,240,107,73,20,.060,'back'), (758,293,120,91,-20,.070,'back'),
 (707,411,81,74,-10,.058,'flank'), (607,234,72,60,0,.050,'crown'),
 (551,327,112,81,10,.062,'crown'), (673,531,72,65,30,.050,'flank'),
 (763,603,66,75,-10,.050,'flank'), (1232,658,42,51,-10,.030,'tail'),
 (1258,676,29,30,0,.020,'tail'), (1227,695,31,31,0,.021,'tail'),
]

HEAD_OUTLINE = [(280,644),(303,599),(354,578),(368,558),(416,548),
 (444,548),(434,508),(452,472),(485,454),(523,452),(526,408),
 (554,373),(600,355),(650,366),(684,386),(716,363),(765,355),
 (799,374),(824,365),(855,341),(900,320),(949,333),(985,362),
 (1008,405),(983,437),(1016,431),(1044,461),(1052,491),
 (1029,526),(1033,568),(1032,607),(1048,634),(1038,672),
 (1004,692),(985,704),(994,729),(985,750),(1017,784),
 (1001,818),(1032,850),(1019,905),(998,929),(981,962),
 (992,1005),(964,1041),(921,1049),(893,1023),(856,1014),
 (821,1010),(791,1037),(752,1037),(717,1013),(684,1008),
 (651,1034),(606,1038),(570,1013),(541,1015),(504,1030),
 (467,1020),(443,1005),(404,1001),(367,978),(359,939),
 (372,911),(335,914),(304,893),(301,866),(275,850),(254,827),
 (268,796),(281,770),(309,746),(318,724),(317,702),(297,683)]

FACE = [(477,600),(501,612),(525,619),(552,613),(565,628),(598,635),
 (628,631),(653,620),(669,604),(687,629),(716,635),(739,621),
 (767,627),(796,619),(817,603),(837,596),(850,625),(881,641),
 (905,644),(902,676),(921,704),(916,730),(934,750),(918,781),
 (918,819),(898,854),(871,884),(816,913),(755,929),(701,934),
 (648,932),(598,932),(545,929),(494,918),(453,901),(419,880),
 (405,850),(393,815),(391,785),(382,765),(398,738),(402,712),
 (419,683),(430,657),(454,640)]


def polygon(points, size):
    im = Image.new('L', size)
    ImageDraw.Draw(im).polygon(points, fill=255)
    return np.asarray(im) > 0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    data = {'schema':'carol.v004.tuft-inventory','units':'original authority pixels',
            'method':'Manual visible-unit centers and extents; radii describe the full visible lock, not the Gaussian sigma. Orientation clockwise in image space.',
            'uncertainty_px':5,'front':[], 'side':[]}
    for view, rows in [('front', FRONT), ('side', SIDE)]:
        im = Image.open(REF / f'carol_{view}.png').convert('RGBA')
        rgb = np.asarray(im)[:,:,:3].astype(float)
        if view == 'front':
            mask = np.asarray(im)[:,:,3] > 128
        else:
            ink = (rgb.min(2) < 224) & (rgb.max(2)-rgb.min(2) > 23)
            mask = binary_fill_holes(binary_closing(ink, iterations=3))
        distance=distance_transform_edt(mask)
        if view=='side':
            profile=[]
            for py in range(80,925):
                hits=np.where(mask[py])[0]
                if not len(hits):continue
                back=float(hits[-1])
                if 605<=py<=728:back=float(np.interp(py,[605,640,690,728],[1198,1193,1210,1216]))
                profile.append([(999-py)/918,(float(hits[0])-145)/918,(back-145)/918])
            (WORK/'side-profile.json').write_text(json.dumps(sorted(profile)),encoding='utf-8')
        for i,(x,y,rx,ry,angle,depth,region) in enumerate(rows):
            d = distance[min(int(y),im.height-1),min(int(x),im.width-1)]
            record = {'id':f'{view[0].upper()}{i+1:02}', 'region':region,'authority_view':view,
                'center_px':[x,y], 'width_px':rx*2, 'height_px':ry*2,
                'orientation_deg':angle, 'relief_H':depth,
                'classification':'silhouette' if d<max(rx,ry)*1.1 else 'interior',
                'pigment_srgb':[round(c/255,4) for c in rgb[y,x]],
                'neighbors':[]}
            data[view].append(record)
        for a in data[view]:
            a['neighbors'] = [b['id'] for b in sorted(data[view],key=lambda b:sum((u-v)**2 for u,v in zip(a['center_px'],b['center_px'])))[1:5]]
        wool = mask & (rgb[:,:,2] > rgb[:,:,0]*.89) & (rgb[:,:,2] > rgb[:,:,1]*.93) & (rgb.mean(2)>130)
        if view == 'front':
            wool &= ~polygon(FACE, im.size)
            yy,xx=np.mgrid[:im.height,:im.width]
            wool &= yy < 1107
            # Gold and the brown/pink ear and hoof pigments never transfer to fleece.
            wool &= ~((rgb[:,:,0]-rgb[:,:,2]>26)&(rgb[:,:,1]-rgb[:,:,2]>8))
            outer = binary_fill_holes(wool)
            # The torso continues behind each ear. Its hidden outline must not
            # follow the visible ear exclusion and form a radial notch.
            outer = binary_fill_holes(mask & (yy<1107))
            for cx,cy,rx,ry in [(627,272,80,82),(678,469,75,72),(151,628,67,72),(276,962,68,67),(629,1006,66,65),(326,446,119,145)]:
                wool &= ((xx-cx)/rx)**2+((yy-cy)/ry)**2>1
            head = polygon(HEAD_OUTLINE, im.size)
            head |= ((xx-630)/317)**2+((yy-661)/257)**2<1
            face = polygon(FACE,im.size)
            for name,m in [('body-mask',outer),('head-mask',head),('face-mask',face)]:
                Image.fromarray((m*255).astype('uint8')).save(WORK/(name+'.png'))
        if view=='side':
            yy,xx=np.mgrid[:im.height,:im.width]
            wool &= ~polygon([(120,498),(205,483),(364,529),(429,481),(524,505),(553,582),(524,718),(396,786),(215,795),(120,711)],im.size)
            for cx,cy,rx,ry in [(446,245,75,85),(854,405,130,138),(1044,699,80,79),(366,816,68,78)]:
                wool &= ((xx-cx)/rx)**2+((yy-cy)/ry)**2>1
        # Normalized multiscale color diffusion fills occluded pigment without
        # radial nearest-neighbor streaks from star/moon/face boundaries.
        small=tuple(max(1,n//4) for n in im.size)
        valid=np.asarray(Image.fromarray((wool*255).astype('uint8')).resize(small,Image.Resampling.BOX))/255
        color=np.asarray(im.convert('RGB').resize(small,Image.Resampling.BOX)).astype(float)
        result=np.zeros_like(color);missing=np.ones_like(valid,dtype=bool)
        for sigma in [2,4,8,16,32,64]:
            weight=gaussian_filter(valid,sigma)
            paint=gaussian_filter(color*valid[:,:,None],(sigma,sigma,0))/np.maximum(weight[:,:,None],1e-6)
            take=missing&(weight>.035);result[take]=paint[take];missing[take]=False
        # Remove diffusion-scale seams in occluded pigment without modifying
        # any observed wool pixels.
        for _ in range(240):
            result=gaussian_filter(result,(1,1,0))*(1-valid[:,:,None])+color*valid[:,:,None]
        filled=np.asarray(Image.fromarray(np.clip(result,0,255).astype('uint8')).resize(im.size,Image.Resampling.BICUBIC))
        pigment=np.where(wool[:,:,None],rgb,filled).astype('uint8')
        Image.fromarray(pigment).save(WORK/f'pigment-{view}.png')
        Image.fromarray((mask*255).astype('uint8')).save(WORK/f'silhouette-{view}.png')
        if view=='front':
            ear_trace=[(55,740),(107,708),(300,635),(350,666),(348,760),(313,803),(152,850),(77,819)]
            ear_region=polygon(ear_trace,im.size)|polygon([(1260-x,y) for x,y in ear_trace],im.size)
            hoof_region=(yy>1040)&(yy<1170)&(((xx>330)&(xx<570))|((xx>700)&(xx<935)))
        else:
            ear_region=polygon([(510,501),(566,520),(660,553),(716,583),(769,643),(770,679),(749,710),(694,726),(632,715),(580,681),(531,626),(514,573)],im.size)
            hoof_region=(yy>891)&(yy<1010)&(((xx>340)&(xx<635))|((xx>830)&(xx<1095)))
        for label,region in [('ear',ear_region),('hoof',hoof_region)]:
            valid=region&mask&(rgb[:,:,2]<rgb[:,:,0]*.86)&(rgb[:,:,0]>50)
            nearest=distance_transform_edt(~valid,return_distances=False,return_indices=True)
            colors=rgb[nearest[0],nearest[1]]
            Image.fromarray(colors.astype('uint8')).save(WORK/f'{label}-{view}.png')
    # Shared spatial masses, with explicit correspondence only where unambiguous.
    data['cross_view_correspondence'] = [
      {'front':['F01','F02','F03'],'side':['S01','S02'],'region':'crown'},
      {'front':['F60','F59','F51'],'side':['S09','S10','S11'],'region':'forelock'},
      {'front':['F67','F69','F80'],'side':['S12','S13'],'region':'cheek'},
      {'front':['F70','F71','F75','F76'],'side':['S14','S15'],'region':'lower_frame'},
    ]
    (OUT/'tuft-inventory.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    contract = {'schema':'carol.v004.authority-contract',
      'donor':{'repository':'snowtone-ai/grimoire','commit':'15bfa8e4c3a8ba24c246fe806bd125b307d8f076','file':'scripts/grimo/build-carol-reference.py','role':'method only'},
      'front_mapping':{'center_u':630,'ground_v':1161,'pixels_per_unit':1012},
      'side_mapping':{'face_tip_u':145,'ground_v':999,'pixels_per_unit':918},
      'coordinates':'X rearward; Y character left; Z up; H=1',
      'authorities':{view:{'path':f'assets/grimo/source/carol/approved-3d/carol_{view}.png','sha256':hashlib.sha256((REF/f'carol_{view}.png').read_bytes()).hexdigest()} for view in ['front','side']},
      'priority':'Current explicit Front/Side geometry; canonical identity supports softness and appeal only',
      'skin_sha256':'321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a'}
    (OUT/'authority-contract.json').write_text(json.dumps(contract,indent=2),encoding='utf-8')
    print('CURRENT_TUFTS',len(FRONT),len(SIDE))


if __name__ == '__main__':
    main()
