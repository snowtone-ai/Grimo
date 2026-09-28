"""Shared Front/Side envelope, with the donor's local fifth-power lock field.

The envelope carries low-frequency body volume. Locks are attached in space,
not extruded from either drawing. All cameras see the same surface and paint.
"""
import math
import json
import numpy as np
import bpy
import bmesh
from mathutils import Vector


class Envelope:
    def __init__(self, api):
        self.api = api
        front = api['pixels'](api['WORK'] / 'body-mask.png')[:, :, 0] > .5
        side = api['pixels'](api['WORK'] / 'silhouette-side.png')[:, :, 0] > .5
        z = np.linspace(.11, .95, 200)
        widths, lefts, rights = [], [], []
        for h in z:
            row = front[int(1161-h*1012)]
            xs = np.flatnonzero(row)
            widths.append((xs[-1]-xs[0])/2024)
            xs = np.flatnonzero(side[int(999-h*918)])
            # The separate tail is not part of the torso envelope.
            if .29 < h < .43:
                xs = xs[xs < 1200]
            lefts.append((xs[0]-145)/918)
            rights.append((xs[-1]-145)/918)
        self.z0, self.rz = .535, .435
        t = (z-self.z0)/self.rz
        factor = np.sqrt(np.maximum(.025, 1-t*t))
        self.w = np.polynomial.polynomial.polyfit(t, (np.array(widths)-.028)/factor, 4)
        self.r = np.polynomial.polynomial.polyfit(t, ((np.array(rights)-lefts)/2-.028)/factor, 4)
        self.c = np.polynomial.polynomial.polyfit(t, (np.array(rights)+lefts)/2, 3)

    def profile(self, z):
        t = np.clip((z-self.z0)/self.rz, -.999999, .999999)
        f = np.sqrt(1-t*t)
        poly = np.polynomial.polynomial.polyval
        return poly(t, self.c), np.maximum(.001, poly(t, self.r)*f), np.maximum(.001, poly(t, self.w)*f)

    def power(self, z):
        return 2

    def point(self, y, z, front=True):
        c, rx, ry = self.profile(z)
        p = self.power(z) if front else 2
        q = np.clip(1-(np.abs(y)/ry)**p, 0, 1)
        x = c+(-1 if front else 1)*rx*q**(1/p)
        if front:
            t = np.clip((abs(y)-.265)/.115, 0, 1)
            taper = t*t*(3-2*t)
            x += .38*taper*np.exp(-((z-.46)/.14)**4)*np.sqrt(q)
        return np.stack((x, y, z), axis=-1)

    def normal(self, points, front=True):
        x, y, z = points.T
        dy = (self.point(y+.0001, z, front)[:, 0]-self.point(y-.0001, z, front)[:, 0])/.0002
        dz = (self.point(y, z+.0001, front)[:, 0]-self.point(y, z-.0001, front)[:, 0])/.0002
        n = np.stack((-np.ones_like(y), dy, dz), axis=1)*(1 if front else -1)
        return n/np.maximum(1e-8, np.linalg.norm(n, axis=1))[:, None]

    def boundary(self, angles, center):
        lo = np.zeros_like(angles)
        hi = np.full_like(angles, 1.5)
        for _ in range(42):
            d = (lo+hi)/2
            y = center[0]+np.cos(angles)*d
            z = center[1]+np.sin(angles)*d
            _, _, width = self.profile(z)
            inside = (abs(z-self.z0)<self.rz) & (abs(y)<width)
            lo = np.where(inside, d, lo)
            hi = np.where(inside, hi, d)
        return (lo+hi)/2

    def lock_centers(self, inventory):
        result = []
        for view in ['front', 'side']:
            for lock in inventory[view]:
                if lock['region'] == 'tail':
                    continue
                if view == 'front' and lock['region'] == 'head':
                    continue
                u, v = lock['center_px']
                if view == 'front':
                    z = np.clip((1161-v)/1012, self.z0-self.rz+.005, self.z0+self.rz-.005)
                    c, rx, ry = self.profile(z)
                    y = np.clip((630-u)/1012, -ry*.99, ry*.99)
                    point = self.point(np.array(y), np.array(z))
                    axes = np.array([min(lock['width_px'], lock['height_px'])/2024,
                                     lock['width_px']/2024, lock['height_px']/2024])
                    result.append((point, axes, lock['relief_H'], lock['id'], view))
                else:
                    z = np.clip((999-v)/918, self.z0-self.rz+.005, self.z0+self.rz-.005)
                    c, rx, ry = self.profile(z)
                    x = np.clip((u-145)/918, c-rx*.99, c+rx*.99)
                    p = self.power(z) if x < c else 2
                    y = ry*max(0, 1-abs((x-c)/rx)**p)**(1/p)
                    for sign in [-1, 1]:
                        point = np.array([x, y*sign, z])
                        axes = np.array([lock['width_px']/1836,
                                         min(lock['width_px'], lock['height_px'])/1836, lock['height_px']/1836])
                        result.append((point, axes, lock['relief_H'], lock['id']+str(sign), view))
        # Rear has no image authority; staggered spatial locks continue the rhythm.
        for row, z in enumerate(np.linspace(.17, .87, 7)):
            _, _, width = self.profile(z)
            for col, y in enumerate(np.linspace(-.82, .82, 6)*width):
                zz = z+.017*math.sin(col*2+row)
                point = self.point(np.array(y), np.array(zz), False)
                result.append((point, np.array([.09, .093, .082]), .046,
                               f'R{row:02d}{col:02d}', 'rear'))
        return result


def spatial_paint(ob, rest, normals, api, pigment='pigment', lit=.36):
    me = ob.data
    for label, coordinates, filename in [
        ('FrontPaint', np.stack(((630-rest[:, 1]*1012)/1254, 1-(1161-rest[:, 2]*1012)/1254), axis=1), 'pigment-front.png'),
        ('SidePaint', np.stack(((145+rest[:, 0]*918)/1448, 1-(999-rest[:, 2]*918)/1086), axis=1), 'pigment-side.png'),
    ]:
        uv = me.uv_layers.new(name=label)
        indices = np.empty(len(me.loops), dtype=np.int32)
        me.loops.foreach_get('vertex_index', indices)
        uv.data.foreach_set('uv', coordinates[indices].astype(np.float32).ravel())
    w = np.maximum(0, -normals[:, 0])**4
    w /= w+np.abs(normals[:, 1])**4+np.maximum(0, normals[:, 0])**4+1e-8
    colors = np.ones((len(rest), 4), np.float32)
    colors[:, :3] = w[:, None]
    attr = me.color_attributes.new(name='FrontConfidence', type='FLOAT_COLOR', domain='POINT')
    attr.data.foreach_set('color', colors.ravel())
    mat = api['shader']('Attached '+pigment+' watercolor', color=(.82, .86, 1), lit=lit)
    ns, links = mat.node_tree.nodes, mat.node_tree.links
    textures = []
    for label, filename in [('FrontPaint', pigment+'-front.png'), ('SidePaint', pigment+'-side.png')]:
        uv = ns.new('ShaderNodeUVMap'); uv.uv_map = label
        im = bpy.data.images.load(str(api['WORK']/filename), check_existing=True); im.pack()
        tex = ns.new('ShaderNodeTexImage'); tex.image = im; tex.extension = 'EXTEND'
        links.new(uv.outputs['UV'], tex.inputs['Vector']); textures.append(tex)
    weight = ns.new('ShaderNodeVertexColor'); weight.layer_name = 'FrontConfidence'
    mix = ns.new('ShaderNodeMixRGB')
    links.new(weight.outputs['Color'], mix.inputs[0])
    links.new(textures[1].outputs['Color'], mix.inputs[1])
    links.new(textures[0].outputs['Color'], mix.inputs[2])
    color_output=mix.outputs[0]
    if pigment=='hoof':
        rear=me.color_attributes.new(name='HoofRearWeight',type='FLOAT_COLOR',domain='POINT')
        rear_colors=np.ones((len(rest),4),np.float32)
        rear_colors[:,:3]=api['smooth'](np.maximum(normals[:,0],0)/.7)[:,None]
        rear.data.foreach_set('color',rear_colors.ravel())
        rear_weight=ns.new('ShaderNodeVertexColor');rear_weight.layer_name=rear.name
        coordinates=ns.new('ShaderNodeTexCoord')
        noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=70
        links.new(coordinates.outputs['Object'],noise.inputs['Vector'])
        brown=ns.new('ShaderNodeMixRGB')
        brown.inputs[1].default_value=(*api['linear']((.43,.27,.21)),1)
        brown.inputs[2].default_value=(*api['linear']((.57,.38,.30)),1)
        links.new(noise.outputs['Fac'],brown.inputs[0])
        cap=ns.new('ShaderNodeMixRGB')
        links.new(rear_weight.outputs['Color'],cap.inputs[0]);links.new(color_output,cap.inputs[1]);links.new(brown.outputs[0],cap.inputs[2])
        color_output=cap.outputs[0]
    for node in ns:
        if node.type in ['BSDF_DIFFUSE', 'EMISSION']:
            links.new(color_output, node.inputs['Color'])
    me.materials.append(mat)


def regional_skin_paint(api):
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.name.startswith(('EAR_','HOOF_')):continue
        points=np.array([ob.matrix_world@v.co for v in ob.data.vertices])
        normals=np.array([ob.matrix_world.to_3x3()@v.normal for v in ob.data.vertices])
        normals/=np.maximum(1e-8,np.linalg.norm(normals,axis=1))[:,None]
        ob.data.materials.clear()
        for polygon in ob.data.polygons:polygon.material_index=0
        spatial_paint(ob,points,normals,api,'ear' if ob.name.startswith('EAR_') else 'hoof',lit=.22)


def constrain_outline(verts, api):
    """Orthogonal outline constraints act on independent spatial coordinates."""
    zgrid = np.linspace(.03, 1.04, 1011)
    front = api['pixels'](api['WORK']/'body-mask.png')[:, :, 0] > .5
    side = api['pixels'](api['WORK']/'silhouette-side.png')[:, :, 0] > .5
    targets = []
    for z in zgrid:
        xs = np.flatnonzero(front[int(np.clip(1161-z*1012, 0, 1253))])
        ys = np.flatnonzero(side[int(np.clip(999-z*918, 0, 1085))])
        if .29 < z < .43:
            ys = ys[ys < 1200]
        targets.append([(630-xs[0])/1012 if len(xs) else 0,
                        (xs[-1]-630)/1012 if len(xs) else 0,
                        (ys[-1]-145)/918 if len(ys) else .57])
    targets = np.array(targets)
    kernel = np.exp(-.5*(np.arange(-12,13)/4)**2);kernel /= kernel.sum()
    def filtered(data):
        return np.convolve(np.pad(data,12,mode='edge'),kernel,mode='valid')
    targets = np.stack([filtered(targets[:,i]) for i in range(3)],axis=1)
    left_z = np.array([.055,.10,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60,.65,.70,.75,.80,.85,.90,.95,1.0])
    left_x = np.array([.58,.205,.11,.104,.24,.26,.295,.285,.29,.036,-.03,-.024,.016,.055,.13,.16,.28,.38,.42,.55])
    index = np.clip(np.rint((verts[:, 2]-.03)/.001).astype(int), 0, len(zgrid)-1)
    for axis, sign, target in [(1,1,targets[:,0]),(1,-1,targets[:,1]),(0,1,targets[:,2]),(0,-1,-np.interp(zgrid,left_z,left_x))]:
        values = verts[:, axis]*sign
        extreme = np.full(len(zgrid), -np.inf)
        np.maximum.at(extreme, index, values)
        valid = np.isfinite(extreme)
        extreme = np.interp(zgrid, zgrid[valid], extreme[valid])
        extreme = filtered(extreme)
        current = np.interp(verts[:, 2], zgrid, extreme)
        wanted = np.interp(verts[:, 2], zgrid, target)
        if axis == 1:
            weight = api['smooth']((values/np.maximum(.02,current)-.58)/.40)
        else:
            low = np.min(verts[:, 0]); high = np.max(verts[:, 0])
            fraction = (verts[:,0]-low)/(high-low)
            weight = api['smooth']((fraction-.58)/.40) if sign==1 else api['smooth']((.42-fraction)/.40)
        verts[:,axis] += sign*(wanted-current)*weight
    return verts


def apply_modifier(ob, modifier):
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.modifier_apply(modifier=modifier.name)


def remove_micro_components(ob):
    """Discard sub-voxel islands left by volume union/smoothing, not actual locks."""
    bm=bmesh.new();bm.from_mesh(ob.data)
    remaining=set(bm.verts);discard=[]
    while remaining:
        todo=[remaining.pop()];component=[]
        while todo:
            vertex=todo.pop();component.append(vertex)
            for edge in vertex.link_edges:
                other=edge.other_vert(vertex)
                if other in remaining:remaining.remove(other);todo.append(other)
        if len(component)<=32 and max(max(v.co[i] for v in component)-min(v.co[i] for v in component) for i in range(3))<.001:
            discard.extend(component)
    if discard:bmesh.ops.delete(bm,geom=discard,context='VERTS')
    bm.to_mesh(ob.data);bm.free();ob.data.update()


def lock_pigment(api, view, lock):
    """A small painted sparkle must not turn its entire blue lock white."""
    yy,xx=np.mgrid[-1:1:17j,-1:1:17j]
    inside=xx*xx+yy*yy<=1
    x=xx[inside]*lock['width_px']*.28;y=yy[inside]*lock['height_px']*.28
    a=math.radians(lock['orientation_deg']);u,v=lock['center_px']
    samples=api['sample'](api['pixels'](api['WORK']/f'pigment-{view}.png'),u+x*math.cos(a)-y*math.sin(a),v+x*math.sin(a)+y*math.cos(a))[:,:3]
    return np.median(samples,axis=0)


def regional_head(api, skin, parent):
    """Rounded overlapping locks form the fringe/cheeks/chin, independently of the torso."""
    vertices, faces = [], []
    records = []
    nr, ns = 28, 56
    for lock in api['INVENTORY']['front']:
        if lock['region'] != 'head':
            continue
        u, v = lock['center_px'];cy=(630-u)/1012;cz=(1161-v)/1012
        ry = lock['width_px']/2024;rz=lock['height_px']/2024
        hit,_,_,_=skin.ray_cast(Vector((-1,cy,cz)),Vector((1,0,0)),3)
        depth = float(np.clip(.95*max(ry,rz),.04,.105))
        if hit:
            cx = min(hit.x+depth*.4,.35)
        else:
            cx = .21+.7*max(0,cz-.65)
        if cz < .26:
            cx = .16+.10*abs(cy)
            cz += .012;rz += .012
        elif cz < .50:
            cx = .34+.18*abs(cy)
        elif cz < .69:
            # Seat the whole visible fringe on Skin, not just its center sample.
            contact=[]
            for yy in np.linspace(-.75,.75,5):
                for zz in np.linspace(-.75,.75,5):
                    r2=yy*yy+zz*zz
                    if r2>.75:continue
                    p,_,_,_=skin.ray_cast(Vector((-1,cy+ry*yy,cz+rz*zz)),Vector((1,0,0)),3)
                    if p:contact.append(p.x+depth*math.sqrt(1-r2)-.012)
            if contact:cx=min(cx,min(contact))
        offset = len(vertices)
        a=math.radians(lock['orientation_deg'])
        for j in range(nr+1):
            theta=math.pi*j/nr
            for k in range(ns):
                phi=math.tau*k/ns
                x=-depth*math.cos(theta)
                y=ry*math.sin(theta)*math.cos(phi)
                z=rz*math.sin(theta)*math.sin(phi)
                vertices.append((cx+x,cy+y*math.cos(a)+z*math.sin(a),cz-y*math.sin(a)+z*math.cos(a)))
        for j in range(nr):
            for k in range(ns):
                aa=offset+j*ns+k;bb=offset+j*ns+(k+1)%ns
                faces.append((aa,bb,bb+ns,aa+ns))
        color=lock_pigment(api,'front',lock)
        records.append({'id':lock['id'],'center':[cx,cy,cz],'radii':[depth,ry,rz],'color':color.tolist()})
    ob=api['make_mesh']('HeadFleece',vertices,faces)
    remesh=ob.modifiers.new('Continuous rounded face locks','REMESH')
    remesh.mode='VOXEL';remesh.voxel_size=.0028;remesh.use_smooth_shade=True
    apply_modifier(ob,remesh)
    soften=ob.modifiers.new('Soft lock joins','SMOOTH');soften.factor=.65;soften.iterations=4
    apply_modifier(ob,soften)
    remove_micro_components(ob)
    points=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',points);points=points.reshape(-1,3)
    normals=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('normal',normals);normals=normals.reshape(-1,3)
    if '--solid-locks' in api['ARGS']:
        continuous_pigment(ob,records,api)
    else:
        spatial_paint(ob,points,normals,api)
    group=ob.vertex_groups.new(name='head');group.add(list(range(len(points))),1,'REPLACE')
    ob['motion_owner']='head';ob['construction']='Skin-attached region-specific rounded lock volume; continuous voxel joins'
    api['parent_keep'](ob,parent)
    (api['OUT']/'face-locks.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    return ob


def continuous_pigment(ob, records, api, base_colors=None):
    """Lock-attached pigment with spatial brush grain, no projected shading bands."""
    points=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',points);points=points.reshape(-1,3)
    colors=np.zeros((len(points),3));weights=np.zeros(len(points))
    patch_paint='--patch-paint' in api['ARGS']
    if patch_paint:
        front_paint=api['sample'](api['pixels'](api['WORK']/'pigment-front.png'),630-points[:,1]*1012,1161-points[:,2]*1012)[:,:3]
        side_paint=api['sample'](api['pixels'](api['WORK']/'pigment-side.png'),145+points[:,0]*918,999-points[:,2]*918)[:,:3]
    for record in records:
        delta=(points-np.array(record['center']))/np.array(record['radii'])
        weight=np.exp(-6*np.sum(delta*delta,axis=1))
        color=np.array(record['color'])
        # Source brush pigment is retained; avoid baking its directional shadow twice.
        color=np.minimum(1,color*.96+.035)
        colors+=weight[:,None]*color;weights+=weight
    colors/=np.maximum(1e-30,weights)[:,None]
    if base_colors is not None:
        colors=np.asarray(base_colors)
        assert colors.shape==(len(points),3), 'Pigment must match mesh vertices'
    if patch_paint:
        forward=np.maximum(.65-points[:,0],0)
        cosine=forward/np.maximum(1e-8,np.hypot(forward,points[:,1]))
        front_weight=api['smooth']((cosine-.3)/.6)
        rear_weight=api['smooth']((points[:,0]-1.0)/.17)
        paint=front_paint*front_weight[:,None]+side_paint*(1-front_weight[:,None])
        colors=paint*(1-rear_weight[:,None])+colors*rear_weight[:,None]
    rgba=np.ones((len(points),4),np.float32);rgba[:,:3]=api['linear'](colors)
    attr=ob.data.color_attributes.new(name='WoolPigment',type='FLOAT_COLOR',domain='POINT')
    attr.data.foreach_set('color',rgba.ravel())
    mat=api['shader']('Spatial pastel wool pigment',attribute='WoolPigment',lit=.20 if patch_paint or '--painted-shade' in api['ARGS'] else .72)
    ns,links=mat.node_tree.nodes,mat.node_tree.links
    attribute=next(n for n in ns if n.type=='VERTEX_COLOR')
    geometry=ns.new('ShaderNodeNewGeometry')
    coordinates=ns.new('ShaderNodeTexCoord')
    noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=95;noise.inputs['Detail'].default_value=3.2;noise.inputs['Roughness'].default_value=.75
    links.new(coordinates.outputs['Object'],noise.inputs['Vector'])
    ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.22;ramp.color_ramp.elements[0].color=(.86,.89,.99,1)
    ramp.color_ramp.elements[1].position=.78;ramp.color_ramp.elements[1].color=(1,1,1,1)
    links.new(noise.outputs['Fac'],ramp.inputs['Fac'])
    multiply=ns.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1
    links.new(attribute.outputs['Color'],multiply.inputs[1]);links.new(ramp.outputs['Color'],multiply.inputs[2])
    pigment=multiply.outputs[0]
    if '--painted-shade' in api['ARGS']:
        direction=ns.new('ShaderNodeVectorMath');direction.operation='DOT_PRODUCT'
        direction.inputs[1].default_value=(-.28,-.12,.952)
        links.new(geometry.outputs['Normal'],direction.inputs[0])
        remap=ns.new('ShaderNodeMapRange');remap.inputs['From Min'].default_value=-.8;remap.inputs['From Max'].default_value=.65
        links.new(direction.outputs['Value'],remap.inputs['Value'])
        tone=ns.new('ShaderNodeValToRGB')
        tone.color_ramp.elements.remove(tone.color_ramp.elements[1])
        for index,(position,color) in enumerate([(0,(.78,.76,.99)),(.45,(.93,.91,1)),(.72,(1,.98,1)),(1,(1,.98,.96))]):
            element=tone.color_ramp.elements[0] if index==0 else tone.color_ramp.elements.new(position)
            element.position=position;element.color=(*api['linear'](color),1)
        links.new(remap.outputs['Result'],tone.inputs['Fac'])
        glaze=ns.new('ShaderNodeMixRGB');glaze.blend_type='MULTIPLY';glaze.inputs[0].default_value=1
        links.new(pigment,glaze.inputs[1]);links.new(tone.outputs['Color'],glaze.inputs[2]);pigment=glaze.outputs[0]
        ao=ns.new('ShaderNodeAmbientOcclusion');ao.inputs['Distance'].default_value=.045;ao.samples=8;ao.only_local=True
        cavity=ns.new('ShaderNodeMixRGB');cavity.inputs[1].default_value=(*api['linear']((.67,.64,.96)),1);cavity.inputs[2].default_value=(1,1,1,1)
        links.new(ao.outputs['AO'],cavity.inputs[0])
        shade=ns.new('ShaderNodeMixRGB');shade.blend_type='MULTIPLY';shade.inputs[0].default_value=.45
        links.new(pigment,shade.inputs[1]);links.new(cavity.outputs[0],shade.inputs[2]);pigment=shade.outputs[0]
    for node in ns:
        if node.type in ['BSDF_DIFFUSE','EMISSION']:links.new(pigment,node.inputs['Color'])
    ob.data.materials.clear();ob.data.materials.append(mat)
    for polygon in ob.data.polygons:polygon.material_index=0


def anatomical_displacement(points, region):
    """Sculpt by anatomical region, not by either image's silhouette."""
    x,y,z=points.T;delta=np.zeros_like(points)
    if region=='HeadFleece':
        cheek=np.exp(-((abs(y)-.29)/.075)**4-((z-.40)/.17)**4-((x-.24)/.13)**4)
        delta[:,0]+=.024*cheek
        delta[:,1]-=np.sign(y)*.012*cheek
        # A smaller head mantle sits in front of the larger thoracic fleece.
        upper=np.clip((z-.56)/.24,0,1)
        upper=upper*upper*(3-2*upper)
        delta[:,0]+=.065-.14*x
        delta[:,1]-=.13*y*upper
        delta[:,1]-=.45*np.sign(y)*np.maximum(abs(y)-.30,0)
        delta[:,2]-=.34*np.maximum(z-.60,0)
    if region=='BodyFleece':
        bib=np.exp(-((x-.18)/.19)**4-(y/.30)**4-((z-.205)/.085)**4)
        delta[:,0]+=.030*bib
        delta[:,2]+=.014*bib
        shoulder=np.exp(-((x-.55)/.20)**4-((z-.44)/.15)**4)
        delta[:,1]-=np.sign(y)*.020*shoulder*np.clip((abs(y)-.27)/.15,0,1)
        # The low front wool belongs to the neck, not to the jaw or muzzle.
        collar=np.exp(-((x-.22)/.23)**4)
        delta[:,0]+=.055*collar
        delta[:,1]-=.06*y*collar
        delta[:,2]+=.020*collar*np.clip((.18-z)/.12,0,1)
        neck=np.exp(-((x-.48)/.18)**2)
        delta[:,1]-=.12*y*neck
        delta[:,2]-=.085*np.maximum(z-.48,0)*neck
        sculpted=points+delta
        delta[:]=np.array([.74,0,.06])+(sculpted-np.array([.74,0,.06]))*np.array([.94,.93,.94])-points
    if region=='CENTRAL_CHASSIS':
        under_chin=np.clip((.255-z)/.085,0,1)*np.exp(-((x-.22)/.23)**4)
        delta[:,0]+=.090*under_chin
        delta[:,1]-=y*.10*under_chin
    return delta


def sculpt_anatomy(ob):
    matrix=ob.matrix_world;inverse=matrix.inverted().to_3x3()
    points=np.array([matrix@v.co for v in ob.data.vertices])
    delta=anatomical_displacement(points,ob.name)
    local=np.array([inverse@Vector(d) for d in delta])
    keys=ob.data.shape_keys
    key_points=[] if keys is None else [np.array([v.co[:] for v in key.data]) for key in keys.key_blocks]
    original=np.array([v.co[:] for v in ob.data.vertices])
    ob.data.vertices.foreach_set('co',(original+local).ravel())
    if keys:
        for key,coordinates in zip(keys.key_blocks,key_points):
            key.data.foreach_set('co',(coordinates+local).ravel())
    ob.data.update()
    return {'max_displacement':float(np.linalg.norm(delta,axis=1).max()),
            'mean_displacement':float(np.linalg.norm(delta,axis=1).mean()),
            'bounds_before':[points.min(axis=0).tolist(),points.max(axis=0).tolist()],
            'bounds_after':[(points+delta).min(axis=0).tolist(),(points+delta).max(axis=0).tolist()]}


def head_backing(api):
    """A quiet inner mantle bridges locks without enlarging the exterior."""
    from mathutils.kdtree import KDTree
    head=bpy.data.objects['HeadFleece']
    tree=KDTree(len(head.data.vertices))
    for vertex in head.data.vertices:tree.insert(head.matrix_world@vertex.co,vertex.index)
    tree.balance()
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=40)
    ob=bpy.context.object;ob.name='HeadFleeceBacking'
    center=np.array([.39,0,.67]);radii=np.array([.235,.27,.16])
    for vertex in ob.data.vertices:vertex.co=Vector(center+np.array(vertex.co)*radii)
    ob.data.update()
    colors=[]
    pigment=head.data.color_attributes['WoolPigment']
    for vertex in ob.data.vertices:
        _,index,_=tree.find(vertex.co)
        linear=np.clip(np.array(pigment.data[index].color[:3]),0,1)
        colors.append(np.where(linear<=.0031308,linear*12.92,1.055*linear**(1/2.4)-.055))
    continuous_pigment(ob,[],api,base_colors=colors)
    for polygon in ob.data.polygons:polygon.use_smooth=True
    group=ob.vertex_groups.new(name='head');group.add(list(range(len(ob.data.vertices))),1,'REPLACE')
    ob['motion_owner']='head';ob['construction']='Inner scalp mantle within the smaller head lock envelope'
    api['parent_keep'](ob,head.parent)
    return {'center':center.tolist(),'radii':radii.tolist(),'purpose':'Bridge exposed scalp between reduced locks; no enlarged outer bounds',
            'deformation':'Not validated; backing is head-owned but has no local contact shape keys'}


def anatomical_base(api):
    """Keep the v002 spatial anatomy; replace shading independently of volume."""
    source=api['ASSET'].with_name('carol-normal-fleece-v002.blend')
    bpy.ops.wm.open_mainfile(filepath=str(source))
    bpy.context.scene.frame_set(1)
    report={'source':source.name,'source_sha256':api['sha'](source),'regions':{},
            'method':'Anatomical base with local smooth sculpt fields, no image outline fitting',
            'human_acceptance':False}
    mapping={'FLEECE_HEAD_SURFACE':'HeadFleece',
             'FLEECE_TORSO_SURFACE':'BodyFleece','TAIL_FLEECE_SHELL':'TailFleece'}
    for old,new in mapping.items():
        ob=bpy.data.objects[old];ob.name=new
        if ob.data.shape_keys:
            for key in ob.data.shape_keys.key_blocks:key.value=0
        pigment=ob.data.color_attributes['pigment']
        linear=np.empty(len(pigment.data)*4,np.float32)
        pigment.data.foreach_get('color',linear)
        linear=np.clip(linear.reshape(-1,4)[:,:3],0,1)
        colors=np.where(linear<=.0031308,linear*12.92,1.055*linear**(1/2.4)-.055)
        colors=colors*.82+.18
        continuous_pigment(ob,[],api,base_colors=colors)
        if '--sculpt-anatomy' in api['ARGS']:report['regions'][new]=sculpt_anatomy(ob)
        ob['construction']='v002 spatial anatomy with v004 wool shading; no silhouette inflation'
    for mat in bpy.data.objects['CENTRAL_CHASSIS'].data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type=='EMISSION':node.inputs['Strength'].default_value=1.0
    if '--sculpt-anatomy' in api['ARGS']:
        report['head_backing']=head_backing(api)
        report['regions']['CENTRAL_CHASSIS']=sculpt_anatomy(bpy.data.objects['CENTRAL_CHASSIS'])
        for name in ['STAR_chest','STAR_lower_left','STAR_rump','STAR_rump_L','STAR_brow','STAR_crown','STAR_upper_left','MOON']:
            ob=bpy.data.objects.get(name)
            if ob:
                # Charms retain their rigid shape while following their mantle.
                center=np.mean([ob.matrix_world@v.co for v in ob.data.vertices],axis=0)
                region='BodyFleece' if name in ['STAR_chest','STAR_lower_left','STAR_rump','STAR_rump_L'] else 'HeadFleece'
                shift=anatomical_displacement(center[None,:],region)[0]
                for piece in [ob,bpy.data.objects.get(name+'_glint')]:
                    if piece is not None:
                        matrix=piece.matrix_world.copy();matrix.translation+=Vector(shift)
                        piece.matrix_world=matrix
    for ob in bpy.context.scene.objects:
        if ob.name.endswith('_glint'):
            base=bpy.data.objects.get(ob.name.removesuffix('_glint'))
            if base:api['parent_keep'](ob,base.parent)
    bpy.context.scene['anatomy_source_sha256']=api['sha'](source)
    bpy.context.scene['anatomy_source']=source.name
    (api['OUT']/'anatomy-construction.json').write_text(json.dumps(report,indent=2),encoding='utf-8')


def solid_body(core, api, parent):
    """Full rounded body locks over an inset mold; local unions keep soft joins."""
    from mathutils.bvhtree import BVHTree
    points=np.array([core.matrix_world@v.co for v in core.data.vertices])
    core_faces=[tuple(p.vertices) for p in core.data.polygons]
    tree=BVHTree.FromPolygons(points,core_faces)
    # The mold supports the locks from inside and is not the finished exterior.
    points[:,0]=.62+(points[:,0]-.62)*.88
    points[:,1]*=.86
    points[:,2]=.53+(points[:,2]-.53)*.88
    vertices=points.tolist();faces=core_faces.copy();records=[]
    front=api['pixels'](api['WORK']/'body-mask.png')[:,:,0]>.5
    def width(z,sign):
        xs=np.flatnonzero(front[int(np.clip(1161-z*1012,0,1253))])
        return ((630-xs[0]) if sign>0 else (xs[-1]-630))/1012 if len(xs) else .02
    def add(center,radii,color,name,rotation=0):
        nr,ns=20,40;offset=len(vertices);a=math.radians(rotation)
        for j in range(nr+1):
            theta=math.pi*j/nr
            for k in range(ns):
                phi=math.tau*k/ns
                d=np.array([-radii[0]*math.cos(theta),radii[1]*math.sin(theta)*math.cos(phi),radii[2]*math.sin(theta)*math.sin(phi)])
                d[1],d[2]=d[1]*math.cos(a)+d[2]*math.sin(a),-d[1]*math.sin(a)+d[2]*math.cos(a)
                vertices.append((np.array(center)+d).tolist())
        for j in range(nr):
            for k in range(ns):
                aa=offset+j*ns+k;bb=offset+j*ns+(k+1)%ns;faces.append((aa,bb,bb+ns,aa+ns))
        records.append({'id':name,'center':list(center),'radii':list(radii),'color':list(color)})
    for view in ['front','side']:
        pic=api['pixels'](api['WORK']/f'pigment-{view}.png')
        for lock in api['INVENTORY'][view]:
            if lock['region']=='tail' or (view=='front' and lock['region']=='head'):continue
            u,v=lock['center_px'];color=lock_pigment(api,view,lock)
            if view=='front':
                y=(630-u)/1012;z=(1161-v)/1012
                hit,_,_,_=tree.ray_cast(Vector((-1,y,z)),Vector((1,0,0)),3)
                if hit is None:continue
                depth=.09+.3*min(lock['width_px'],lock['height_px'])/2024
                ear_setback=.27*math.exp(-((abs(y)-.43)/.22)**4-((z-.43)/.13)**4)
                add([hit.x+.04+ear_setback,y,z],[depth,lock['width_px']/2024,lock['height_px']/2024],color,lock['id'],lock['orientation_deg'])
            else:
                x=(u-145)/918;z=(999-v)/918
                for sign in [-1,1]:
                    hit,_,_,_=tree.ray_cast(Vector((x,sign*2,z)),Vector((0,-sign,0)),4)
                    if hit is None:continue
                    depth=.105
                    y=sign*min(abs(hit.y)-.045,width(z,sign)-depth)
                    y-=sign*.17*math.exp(-((x-.50)/.21)**4-((z-.43)/.14)**4)
                    if lock['id']=='S01':
                        if sign==1:continue
                        y=0
                    add([x,y,z],[lock['width_px']/1836,depth,lock['height_px']/1836],color,lock['id']+str(sign))
    for i in range(53):
        nx=(i+.5)/53;spread=np.sqrt(1-nx*nx);angle=i*2.39996323
        z=.53+.40*math.sin(angle)*spread
        y=width(z,1)*math.cos(angle)*spread*.94
        hit,_,_,_=tree.ray_cast(Vector((2,y,z)),Vector((-1,0,0)),3)
        if hit is None:continue
        cold=.5+.5*math.sin(i*1.73)
        color=np.array([.67,.75,.98])*(1-cold)+np.array([.94,.94,1])*cold
        ry=.09+.015*math.sin(i*2.1)
        y=math.copysign(min(abs(y),max(.0,width(z,1 if y>0 else -1)-ry)),y)
        add([hit.x-.070,y,z],[.10,ry,.072+.014*math.cos(i*1.6)],color,f'R{i}',20*math.sin(i))
    ob=api['make_mesh']('CloudBody',vertices,faces)
    remesh=ob.modifiers.new('Soft continuous body locks','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.0038;remesh.use_smooth_shade=True
    apply_modifier(ob,remesh)
    soften=ob.modifiers.new('Wool lock valleys','SMOOTH');soften.factor=.6;soften.iterations=4;apply_modifier(ob,soften)
    remove_micro_components(ob)
    continuous_pigment(ob,records,api)
    bpy.data.objects.remove(core,do_unlink=True);ob.name='BodyFleece'
    ob['motion_owner']='torso';ob['construction']='Inset authority mold with spatial rounded lock volumes and continuous pigment'
    group=ob.vertex_groups.new(name='torso');group.add(list(range(len(ob.data.vertices))),1,'REPLACE')
    api['parent_keep'](ob,parent)
    (api['OUT']/'body-locks.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    return ob


def tail_fleece(api,parent):
    records=[];vertices=[];faces=[];nr,ns=22,40
    for i,(center,radii,color) in enumerate([
        ((1.178,0,.363),(.063,.055,.059),(.89,.91,1.0)),
        ((1.213,0,.381),(.042,.047,.043),(.98,.975,1.0)),
        ((1.220,0,.338),(.039,.042,.036),(.84,.87,1.0)),
    ]):
        offset=len(vertices)
        for j in range(nr+1):
            theta=math.pi*j/nr
            for k in range(ns):
                phi=math.tau*k/ns
                vertices.append((center[0]+radii[0]*math.cos(theta),center[1]+radii[1]*math.sin(theta)*math.cos(phi),center[2]+radii[2]*math.sin(theta)*math.sin(phi)))
        for j in range(nr):
            for k in range(ns):
                aa=offset+j*ns+k;bb=offset+j*ns+(k+1)%ns;faces.append((aa,bb,bb+ns,aa+ns))
        records.append({'id':f'T{i}','center':center,'radii':radii,'color':color})
    ob=api['make_mesh']('TailFleece',vertices,faces)
    remesh=ob.modifiers.new('Continuous tail cloud','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.0025;remesh.use_smooth_shade=True;apply_modifier(ob,remesh)
    soften=ob.modifiers.new('Tail softness','SMOOTH');soften.factor=.5;soften.iterations=3;apply_modifier(ob,soften)
    remove_micro_components(ob)
    continuous_pigment(ob,records,api)
    owner=api['empty']('FLEECE_TAIL_OWNER',(1.10,0,.36));api['parent_keep'](owner,parent);api['parent_keep'](ob,owner)
    ob['motion_owner']='tail';ob['construction']='Local three-lock tail volume attached to the torso'
    group=ob.vertex_groups.new(name='tail');group.add(list(range(len(ob.data.vertices))),1,'REPLACE')
    return ob


def radial_surface_diagnostic(api, tree, head_owner, body_owner):
    env = Envelope(api)
    count, rings = api['SEGMENTS'], api['RINGS']
    angle = np.arange(count)*math.tau/count
    center = np.array([(630-646)/1012, (1161-767)/1012])
    ca, sa = np.cos(angle), np.sin(angle)
    outer = env.boundary(angle, center)
    # Same radial-mask construction as the donor, with an open face domain.
    face = api['pixels'](api['WORK']/'face-mask.png')[:, :, 0] > .5
    image_angle = np.mod(np.arctan2(-sa, -ca), math.tau)
    radii = api['boundary_radii'](face, (646, 767))
    inner = np.interp(image_angle/math.tau*count, np.arange(count+1), np.r_[radii, radii[0]])/1012+.012
    rest_parts, normal_parts, radial_parts = [], [], []
    for front in [True, False]:
        r = np.sin(np.linspace(0, math.pi/2, rings+1))[:, None]
        distance = inner+(outer-inner)*r if front else outer*r
        y = center[0]+ca*distance
        z = center[1]+sa*distance
        points = env.point(y.ravel(), z.ravel(), front)
        # Both hemispheres use the identical boundary, avoiding a stitched ridge.
        points[-count:, 0] = env.profile(points[-count:, 2])[0]
        rest_parts.append(points)
        normal_parts.append(env.normal(points, front))
        radial_parts.append(np.broadcast_to(r, distance.shape).ravel())
    rest = np.concatenate(rest_parts)
    normals = np.concatenate(normal_parts)
    stride = (rings+1)*count
    seam = normals[stride-count:stride]+normals[-count:]
    seam /= np.maximum(1e-9,np.linalg.norm(seam,axis=1))[:,None]
    normals[stride-count:stride] = normals[-count:] = seam
    locks = env.lock_centers(api['INVENTORY'])
    total = np.zeros(len(rest))
    records = []
    for center3, axes, amplitude, name, view in locks:
        delta = (rest-center3)/axes
        value = amplitude*np.exp(-2*np.sum(delta*delta, axis=1))
        total += value**5
        records.append({'id': name, 'view': view, 'center': center3.tolist(), 'radii': axes.tolist(), 'relief_H': amplitude})
    relief = total**.2
    rim_distance = np.linalg.norm(rest[:stride, 1:]-rest[np.arange(stride) % count, 1:], axis=1)
    relief[:stride] *= api['smooth'](rim_distance/.035)
    verts = rest+normals*relief[:, None]
    verts = constrain_outline(verts, api)
    # The torso returns behind the independently fitted facial locks.
    verts[:stride,0] += .065*(1-api['smooth'](rim_distance/.065))
    faces = []
    for hemi in range(2):
        offset = hemi*stride
        for j in range(rings):
            for k in range(count):
                a = offset+j*count+k; b = offset+j*count+(k+1) % count
                faces.append((a, b, b+count, a+count))
    for k in range(count):
        a = rings*count+k; b = rings*count+(k+1) % count
        faces.append((a, b, b+stride, a+stride))
    ob = api['make_mesh']('BodyFleece', verts, faces)
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces)); bm.to_mesh(ob.data); bm.free()
    solid = ob.modifiers.new('Inner fleece return', 'SOLIDIFY'); solid.thickness = .012; solid.offset = -1
    apply_modifier(ob,solid)
    soften=ob.modifiers.new('Regularize envelope tangents','SMOOTH');soften.factor=.5;soften.iterations=5
    apply_modifier(ob,soften)
    points=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',points);points=points.reshape(-1,3)
    paint_normals=env.normal(points,True)
    back=points[:,0]>env.profile(points[:,2])[0]
    paint_normals[back]=env.normal(points[back],False)
    spatial_paint(ob,points,paint_normals,api)
    ob['construction'] = 'Joint low-frequency authority envelope; donor fifth-power spatial lock field; open Skin face domain'
    ob['motion_owner'] = 'torso with head deformation weights'
    for name in ['head', 'torso', 'touch_L', 'touch_R']:
        group = ob.vertex_groups.new(name=name)
        for vertex in ob.data.vertices:
            x, y, z = vertex.co
            h = (1-float(api['smooth']((x-.3)/.32)))*float(api['smooth']((z-.18)/.12))
            weight = h if name == 'head' else 1-h if name == 'torso' else float(api['smooth']((y*(1 if name.endswith('L') else -1)+.05)/.1))
            if weight > 0:
                group.add([vertex.index], weight, 'REPLACE')
    api['parent_keep'](ob, body_owner)
    (api['OUT']/'spatial-locks.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    return [ob,regional_head(api,tree,head_owner)]


def build_surface(api, tree, head_owner, body_owner):
    """Torso: stable closed horizontal contours with local spatial lock relief."""
    nz, nt = 384, 384
    zs = np.linspace(.054, 1.0, nz)
    theta = np.arange(nt)*math.tau/nt
    sine, cosine = np.sin(theta), np.cos(theta)
    front = api['pixels'](api['WORK']/'body-mask.png')[:,:,0]>.5
    side = api['pixels'](api['WORK']/'silhouette-side.png')[:,:,0]>.5
    widths=[];rear=[]
    for z in zs:
        xx=np.flatnonzero(front[int(np.clip(1161-z*1012,0,1253))])
        widths.append([(630-xx[0])/1012,(xx[-1]-630)/1012] if len(xx) else [.005,.005])
        xx=np.flatnonzero(side[int(np.clip(999-z*918,0,1085))])
        if .29<z<.43:xx=xx[xx<1200]
        rear.append((xx[-1]-145)/918 if len(xx) else .57)
    widths=np.array(widths);rear=np.array(rear)
    left_z=np.array([.054,.08,.10,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60,.65,.70,.75,.80,.85,.90,.95,1.0])
    left_x=np.array([.61,.40,.205,.11,.104,.24,.26,.295,.285,.29,.036,-.03,-.024,.016,.055,.13,.16,.28,.38,.42,.55])
    fore=np.interp(zs,left_z,left_x)
    kernel=np.exp(-.5*(np.arange(-30,31)/9)**2);kernel/=kernel.sum()
    def smooth_profile(values):return np.convolve(np.pad(values,30,mode='edge'),kernel,mode='valid')
    wp=np.maximum(.002,smooth_profile(widths[:,0])-.024)
    wn=np.maximum(.002,smooth_profile(widths[:,1])-.024)
    xf=smooth_profile(fore)+.022;xb=smooth_profile(rear)-.022
    cx=(xf+xb)/2;rx=(xb-xf)/2
    yy=np.where(sine[None,:]>=0,wp[:,None],wn[:,None])*sine
    xx=cx[:,None]-rx[:,None]*cosine
    zz=np.broadcast_to(zs[:,None],xx.shape)
    rest=np.stack((xx,yy,zz),axis=-1)
    total=np.zeros((nz,nt));records=[]
    for view in ['front','side']:
        for lock in api['INVENTORY'][view]:
            if lock['region']=='tail' or (view=='front' and lock['region']=='head'):continue
            u,v=lock['center_px'];z=(1161-v)/1012 if view=='front' else (999-v)/918
            cc=np.interp(z,zs,cx);rr=np.interp(z,zs,rx)
            positive=np.interp(z,zs,wp);negative=np.interp(z,zs,wn)
            a=math.radians(lock['orientation_deg'])
            if view=='front':
                y=np.clip((630-u)/1012,-negative*.99,positive*.99)
                x=cc-rr*np.sqrt(max(0,1-(y/(positive if y>=0 else negative))**2))
                centers=[np.array([x,y,z])]
                radii=np.array([.11,lock['width_px']/2024,lock['height_px']/2024])
            else:
                x=np.clip((u-145)/918,cc-rr*.99,cc+rr*.99)
                q=np.sqrt(max(0,1-((x-cc)/rr)**2))
                centers=[np.array([x,positive*q,z]),np.array([x,-negative*q,z])]
                radii=np.array([lock['width_px']/1836,.12,lock['height_px']/1836])
            for index,center in enumerate(centers):
                delta=rest-center
                axis=1 if view=='front' else 0
                dd=delta.copy()
                dd[:,:,axis]=delta[:,:,axis]*math.cos(a)+delta[:,:,2]*math.sin(a)
                dd[:,:,2]=-delta[:,:,axis]*math.sin(a)+delta[:,:,2]*math.cos(a)
                value=lock['relief_H']*np.exp(-2*np.sum((dd/radii)**2,axis=2))
                total+=value**5
                records.append({'id':lock['id']+f'_{index}','center':center.tolist(),'radii':radii.tolist(),'view':view})
    for row,z in enumerate(np.linspace(.18,.90,8)):
        for col,yfraction in enumerate([-.78,-.43,-.06,.30,.68]):
            z+=.004*math.sin(col*2+row)
            ww=np.interp(z,zs,wp if yfraction>0 else wn)
            y=yfraction*ww;x=np.interp(z,zs,cx)+np.interp(z,zs,rx)*np.sqrt(1-yfraction*yfraction)
            delta=(rest-np.array([x,y,z]))/np.array([.09,.095,.082])
            total+=(.053*np.exp(-2*np.sum(delta*delta,axis=2)))**5
    relief=total**.2
    direction=rest.copy();direction[:,:,0]-=cx[:,None];direction[:,:,2]=0
    direction/=np.maximum(.001,np.linalg.norm(direction,axis=2))[:,:,None]
    verts=rest+direction*relief[:,:,None]
    for _ in range(2):
        for axis,sign,target,weight in [
            (1,1,widths[:,0],np.maximum(0,sine)**8),
            (1,-1,widths[:,1],np.maximum(0,-sine)**8),
            (0,1,rear,np.maximum(0,-cosine)**8),
            (0,-1,-fore,np.maximum(0,cosine)**8),
        ]:
            current=np.max(verts[:,:,axis]*sign,axis=1)
            verts[:,:,axis]+=sign*(target-current)[:,None]*weight[None,:]
    # The fleece sits behind the ear leaves; the ear root is a local attachment,
    # not an opening punched through the whole torso.
    ear=.105*np.exp(-(((verts[:,:,0]-.51)/.19)**4+((zz-.435)/.092)**4))
    verts[:,:,1]-=np.sign(verts[:,:,1])*ear*np.abs(sine)[None,:]**5
    # The accepted Skin occupies the face opening. Torso wool stays behind it;
    # the independently rounded forehead/cheek locks provide the visible edge.
    face=api['pixels'](api['WORK']/'face-mask.png')[:,:,0]>.5
    for j in range(nz):
        if not .18<zs[j]<.60:continue
        for k in range(nt):
            if cosine[k]<=0:continue
            x,y,z=verts[j,k]
            u=int(np.clip(630-y*1012,0,1253));v=int(np.clip(1161-z*1012,0,1253))
            if not face[v,u]:continue
            hit,_,_,_=tree.ray_cast(Vector((-1,y,z)),Vector((1,0,0)),3)
            if hit:verts[j,k,0]=max(x,hit.x+.035)
    verts[0,:,0]=cx[0];verts[0,:,1]=0
    verts[-1,:,0]=cx[-1];verts[-1,:,1]=0
    faces=[]
    for j in range(nz-1):
        for k in range(nt):
            aa=j*nt+k;bb=j*nt+(k+1)%nt
            faces.append((aa,bb,bb+nt,aa+nt))
    ob=api['make_mesh']('BodyFleece',verts.reshape(-1,3),faces)
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    soften=ob.modifiers.new('Subpixel contour smoothing','SMOOTH');soften.factor=.5;soften.iterations=3
    apply_modifier(ob,soften)
    points=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',points);points=points.reshape(-1,3)
    normals=points.copy();normals[:,0]-=np.interp(points[:,2],zs,cx);normals[:,2]=0
    normals/=np.maximum(1e-8,np.linalg.norm(normals,axis=1))[:,None]
    spatial_paint(ob,points,normals,api)
    ob['construction']='Joint silhouette-constrained torso envelope with spatial fifth-power lock relief; regional ear-root clearance'
    ob['motion_owner']='torso'
    group=ob.vertex_groups.new(name='torso');group.add(list(range(len(points))),1,'REPLACE')
    for name,sign in [('touch_L',1),('touch_R',-1)]:
        group=ob.vertex_groups.new(name=name)
        for i,p in enumerate(points):
            weight=float(api['smooth']((p[1]*sign+.05)/.1))
            if weight:group.add([i],weight,'REPLACE')
    api['parent_keep'](ob,body_owner)
    (api['OUT']/'spatial-locks.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    if '--solid-locks' in api['ARGS']:ob=solid_body(ob,api,body_owner)
    return [ob,regional_head(api,tree,head_owner),tail_fleece(api,body_owner)]
