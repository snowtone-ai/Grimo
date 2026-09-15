import bpy, math, json
from mathutils import Vector
shell = bpy.data.objects['Carol_Fleece_Continuous']
points = [shell.matrix_world @ v.co for v in shell.data.vertices]
rows = []
for degrees in (20, 35, 45):
    a = math.radians(-degrees)
    # Coordinate-only envelope estimate about the neutral rear hip line.
    # Never transform objects, create a pose or save this inspection scene.
    min_z = min(.69 + (p.y-.91)*math.sin(a)+(p.z-.69)*math.cos(a) for p in points)
    rows.append({'liftDegrees': degrees, 'rigidFleeceMinimumZ': min_z,
                 'foreRootZ': .69+(-.69-.91)*math.sin(a),
                 'chassisCenterY': .91+(.12-.91)*math.cos(a)-(.73-.69)*math.sin(a)})
print('FEASIBILITY_ESTIMATE '+json.dumps(rows))
