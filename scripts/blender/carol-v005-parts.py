"""Independent facial/part geometry, parameterized by the registered frontal plate."""
import math
from mathutils import Vector
def build(ctx):
    bpy=ctx['bpy']; meshobj=ctx['meshobj']; material=ctx['material']; volume=ctx['volume']; root=ctx['ROOTOBJ']
    cream=material('Proxy_Cream',(1,.83,.70),.72); brown=material('Proxy_Cocoa',(.20,.085,.053),.62)
    pink=material('Proxy_InnerEar',(.96,.32,.26),.65); dark=material('Proxy_Eye',(.036,.012,.021),.16)
    mouth=material('Proxy_Mouth',(.46,.025,.025),.62); tongue=material('Proxy_Tongue',(1,.22,.18),.64)
    glint=material('Proxy_Highlight',(1,.96,.85),.15)
    for ob in list(bpy.data.objects):
        if ob.name.startswith(('Primary_Face','Primary_Ear')):bpy.data.objects.remove(ob,do_unlink=True)
    face=volume('Carol_Face',(.025,-1.72,1.14),(.87,.34,.59),cream)
    for v in face.data.vertices:
        # Soften the squared cheek/chin contour, maintaining a closed volume.
        for ax,rad,power in [(0,.87,.80),(2,.59,.82)]:
            t=v.co[ax]/rad; v.co[ax]=math.copysign(abs(t)**power*rad,t)
    def fy(x,z):
        return -1.72-.34*math.sqrt(max(.001,1-(abs((x-.025)/.87)**2.5+abs((z-1.14)/.59)**(2/.82))))
    def patch(name,c,rx,rz,bulge,mat,tilt=0):
        verts=[]; faces=[]; n=96; rings=14
        for k in range(rings+1):
            r=k/rings
            for j in range(1 if k==0 else n):
                a=math.tau*j/n; xx=rx*r*math.cos(a); zz=rz*r*math.sin(a)
                x=c[0]+xx*math.cos(tilt)+zz*math.sin(tilt); z=c[1]-xx*math.sin(tilt)+zz*math.cos(tilt)
                verts.append((x,fy(x,z)-.004-bulge*(1-r*r),z))
        for j in range(n):faces.append((0,1+j,1+(j+1)%n))
        for k in range(1,rings):
            lo=1+(k-1)*n; hi=lo+n
            for j in range(n):faces.append((lo+j,hi+j,hi+(j+1)%n,lo+(j+1)%n))
        ob=meshobj(name,verts,faces,mat); mod=ob.modifiers.new('Closed thin surface','SOLIDIFY'); mod.thickness=.009
        return ob
    for x,side,tilt in [(-.437,'L',-.08),(.520,'R',.08)]:
        eye=patch('Carol_Eye_'+side,(x,1.148),.175,.205,.032,dark,tilt)
        # Vertex-colored diagnostic iris on the eye surface; no stacked iris solids.
        attr=eye.data.color_attributes.new(name='Proxy_Iris',type='FLOAT_COLOR',domain='POINT')
        for i,v in enumerate(eye.data.vertices):
            xx=(v.co.x-x)/.175; zz=(v.co.z-1.148)/.205
            lower=math.exp(-((xx/.70)**2+((zz+.65)/.34)**2)*1.8)
            amber=math.exp(-((xx/.88)**2+((zz+.37)/.64)**2)*1.5)
            base=(.029,.010,.014); col=tuple(base[k]+amber*(.23,.09,.025)[k]+lower*(.67,.35,.065)[k] for k in range(3))
            attr.data[i].color=(*col,1)
        m=dark.copy(); m.name='Proxy_Iris_'+side; eye.data.materials.clear(); eye.data.materials.append(m)
        nd=m.node_tree.nodes.new('ShaderNodeVertexColor'); nd.layer_name='Proxy_Iris'; m.node_tree.links.new(nd.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
        for j,(dx,dz,rx,rz) in enumerate([(-.045,.109,.046,.048),(-.076,.047,.018,.021)]):
            gx,gz=x+dx,1.148+dz; volume('Carol_Eye_Glint_'+side+str(j),(gx,fy(gx,gz)-.039,gz),(rx,.004,rz),glint)
        # Small four-point graphic highlight, shallow enough to disappear in clay override.
        gx,gz=x+.072,1.12; vs=[]
        for j in range(8):
            a=math.tau*j/8; r=.045 if j%2==0 else .013; xx=gx+r*math.sin(a); zz=gz+r*math.cos(a); vs.append((xx,fy(xx,zz)-.036,zz))
        meshobj('Carol_Eye_StarGlint_'+side,vs,[tuple(range(8))],glint)
    volume('Carol_Nose',(.025,-2.086,1.13),(.052,.026,.028),brown)
    # Smile is a true curve plus a recessed soft opening, not a placeholder dot.
    def curve(name,pts,r,mat):
        d=bpy.data.curves.new(name,'CURVE'); d.dimensions='3D'; d.bevel_depth=r; d.bevel_resolution=4; d.resolution_u=20
        s=d.splines.new('BEZIER'); s.bezier_points.add(len(pts)-1)
        for p,co in zip(s.bezier_points,pts):p.co=co; p.handle_left_type='AUTO'; p.handle_right_type='AUTO'
        ob=bpy.data.objects.new(name,d); ctx['HERO'].objects.link(ob); ob.parent=root; d.materials.append(mat)
    patch('Carol_Mouth_Opening',(.026,.971),.126,.116,.010,mouth)
    patch('Carol_Tongue',(.030,.920),.085,.059,.017,tongue)
    pts=[(-.133,1.047),(-.10,1.021),(-.055,1.027),(.023,1.071),(.092,1.022),(.148,1.028),(.177,1.053)]
    curve('Carol_Smile',[(x,fy(x,z)-.014,z) for x,z in pts],.009,mouth)
    curve('Carol_Philtrum',[(.025,fy(.025,z)-.015,z) for z in [1.113,1.09,1.071]],.008,brown)
    # Continuous bowl with integral pink material region; front and rear joined at the rim.
    for side in [-1,1]:
        verts=[]; faces=[]; n=96; rings=14; center=(1.32,1.22)
        for back in [False,True]:
            for k in range(rings+1):
                r=k/rings
                for j in range(1 if k==0 else n):
                    a=math.tau*j/n; along=.65*r*math.cos(a); x=center[0]+.62*along; z=center[1]+.215*r*math.sin(a)-.13*along
                    y=-1.25+.78*along
                    depth=(-.10*math.sqrt(max(0,1-r*r))) if back else (.055*r-.035*(1-r)**2)
                    x+=.78*depth; y-=.62*depth
                    verts.append((side*x,y,z+(0 if side<0 else .012)))
        count=1+rings*n
        for back in [0,1]:
            base=back*count
            for j in range(n):faces.append((base,base+1+j,base+1+(j+1)%n))
            for k in range(1,rings):
                lo=base+1+(k-1)*n; hi=lo+n
                for j in range(n):faces.append((lo+j,hi+j,hi+(j+1)%n,lo+(j+1)%n))
        lo=count-n
        for j in range(n):faces.append((lo+j,lo+(j+1)%n,count+lo+(j+1)%n,count+lo+j))
        ear=meshobj('Carol_Ear_'+('L' if side<0 else 'R'),verts,faces,brown); ear.data.materials.append(pink)
        for i,p in enumerate(ear.data.polygons):
            if i<10*n:p.material_index=1
    for ob in list(bpy.data.objects):
        if ob.name.startswith('Primary_Hoof'):
            ob.name=ob.name.replace('Primary','Carol'); ob.data.materials.clear(); ob.data.materials.append(brown)
    return face
