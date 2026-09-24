"""Shared, camera-independent Carol ear and hoof parameterization (H = 1)."""
import math


EAR = dict(lateral=.382, drop=.124, drop_ease=2.0,
           fore_aft=.244, aft_ease=1.7, bend=.018,
           root_x=.352, root_y=.205, root_z=.566,
           root_width=.012, body_width=.101, tip_taper=.34,
           root_cushion=.035, body_cushion=.092, cushion_taper=.36,
           root_fullness=.70, mid_fullness=1.0, tip_roundness=.70,
           upper_fullness=1.0, lower_fullness=1.0, vertical_arch=.018,
           bowl_width=1.18, bowl_depth=.004, bowl_coverage=.34)

HOOF = dict(width=.219, depth=.190, crown=.111, overlap=.035,
            upper_taper=.56, toe_projection=.014, toe_spacing=.071,
            toe_roundness=.021, cleft_depth=.023, cleft_width=.007,
            heel_fullness=.90, heel_taper=.16, sole_curve=.009,
            front_roundness=.019)


def smooth(t):
    return t*t*(3-2*t)


def gaussian(x, center, sigma):
    return math.exp(-((x-center)/sigma)**2)


def ear(side, p=EAR):
    # One closed swept shell. The local root, centerline, breadth, cushion,
    # taper and bowl have independent controls; both ears share one basis.
    nl, na, nb, no = 48, 12, 24, 12
    nc = na+nb+no
    vertices, faces, materials = [], [], []
    for i in range(nl+1):
        t=i/nl
        s=1-(1-t)**p['drop_ease']
        x=p['root_x']+p['fore_aft']*t**p['aft_ease']+p['bend']*math.sin(math.pi*t)
        y=side*(p['root_y']+p['lateral']*t)
        z=p['root_z']-p['drop']*s+p['vertical_arch']*math.sin(math.pi*t)
        base=math.sin(math.pi*(.015+.97*t))**p['tip_roundness']
        fullness=p['root_fullness']+(p['mid_fullness']-p['root_fullness'])*math.sin(math.pi*t)
        taper=smooth(max(0,min(1,(t-.78)/.22)))
        w=(p['root_width']+p['body_width']*base*fullness)*(1-p['tip_taper']*taper)
        h=(p['root_cushion']+p['body_cushion']*base*fullness)*(1-p['cushion_taper']*taper)
        dx=p['fore_aft']*p['aft_ease']*max(.001,t)**(p['aft_ease']-1)+p['bend']*math.pi*math.cos(math.pi*t)
        norm=math.hypot(dx,p['lateral'])
        px,py=-p['lateral']/norm,dx/norm
        oval=max(.001,1-((t-.55)/.47)**2)
        half=p['bowl_width']*math.sqrt(oval)
        lower,upper=-.64-half,-.64+half
        angles=([-math.pi+(-math.pi-lower)*(-j/na) for j in range(na)]
                +[lower+(upper-lower)*j/nb for j in range(nb)]
                +[upper+(math.pi-upper)*j/no for j in range(no)])
        for a in angles:
            c,q=math.cos(a),math.sin(a)
            inset=gaussian(t,.54,p['bowl_coverage'])*max(0,c)**3*max(0,-q)**2
            cushion=h*q*(p['upper_fullness'] if q>=0 else p['lower_fullness'])
            vertices.append((x+px*w*c+.009*inset,
                             y+side*py*w*c,
                             z+cushion-p['bowl_depth']*inset))
    for i in range(nl):
        for j in range(nc):
            a=i*nc+j;b=i*nc+(j+1)%nc
            faces.append((a,b,b+nc,a+nc))
            materials.append(1 if na<=j<na+nb else 0)
    faces.extend([tuple(reversed(range(nc))),tuple(nl*nc+j for j in range(nc))])
    materials.extend([0,0])
    return vertices,faces,materials


def hoof(cx,cy,p=HOOF):
    # A closed loft. Toe relief and two clefts displace the same front wall;
    # a narrower hidden collar seats inside the unchanged limb.
    nr=96
    lateral_peak=max(abs(math.sin(2*math.pi*j/nr)*(1+p['heel_taper']*math.cos(2*math.pi*j/nr)))
                     for j in range(nr))
    stations=[(0,.78,.90),(.008,.91,.97),(.025,1,1),(.052,1,1),
              (.078,.95,.97),(.101,.82,.86),(.111,.72,.75),
              (.125,.56,.58),(.146,.39,.40)]
    vertices,faces=[],[]
    for base_z,sx,sy in stations:
        if base_z<=.111:
            z=base_z*p['crown']/.111
        else:
            z=p['crown']+(base_z-.111)*p['overlap']/.035
        if base_z>=.078:
            taper=smooth(min(1,(base_z-.078)/(.146-.078)))
            sx*=1-(1-p['upper_taper'])*taper
            sy*=1-(1-p['upper_taper'])*taper
        for j in range(nr):
            a=2*math.pi*j/nr;c,s=math.cos(a),math.sin(a)
            front=max(0,c)**max(.6,min(3,1.5*.019/p['front_roundness']))
            # Shift maximum width toward the toes; the back becomes a smaller
            # rounded heel instead of a symmetric tire footprint.
            lateral=(p['width']/2)/lateral_peak*sy*s*(1+p['heel_taper']*c)
            toe_y=lateral
            lobes=sum(gaussian(toe_y,v,p['toe_roundness']) for v in (-p['toe_spacing'],0,p['toe_spacing']))
            clefts=sum(gaussian(toe_y,v,p['cleft_width']*.9) for v in (-.040,.040))
            toe_zone=math.exp(-((z-.034)/.063)**4)
            rx=(p['depth']/2)*sx*(1 if c>=0 else p['heel_fullness'])
            xx=cx-rx*c-front*toe_zone*(p['toe_projection']*lobes-p['cleft_depth']*clefts)
            zz=z+(front*p['sole_curve']*clefts if z<.009 else 0)
            if z>=.078 and z<=p['crown']:
                zz+=.006*front*math.exp(-((z-.093)/.025)**2)
            vertices.append((xx,cy+lateral,zz))
    for i in range(len(stations)-1):
        for j in range(nr):
            a=i*nr+j;b=i*nr+(j+1)%nr
            faces.append((a,b,b+nr,a+nr))
    faces.extend([tuple(reversed(range(nr))),tuple((len(stations)-1)*nr+j for j in range(nr))])
    return vertices,faces,[0]*len(faces)
