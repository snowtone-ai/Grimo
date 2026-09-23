"""Print compact world-space landmarks for the bounded v004 to v011 transfer."""
import bpy
import json
from mathutils import Vector


def bounds(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return [[round(min(p[i] for p in points), 5) for i in range(3)],
            [round(max(p[i] for p in points), 5) for i in range(3)]]


records = []
for obj in bpy.data.objects:
    if obj.type != 'MESH' and obj.type != 'CAMERA':
        continue
    if obj.type == 'MESH':
        box = bounds(obj)
    else:
        box = None
    records.append({
        'name': obj.name,
        'type': obj.type,
        'parent': obj.parent.name if obj.parent else None,
        'location': [round(v, 5) for v in obj.matrix_world.translation],
        'bounds': box,
        'vertices': len(obj.data.vertices) if obj.type == 'MESH' else None,
        'materials': [m.name if m else None for m in obj.data.materials] if obj.type == 'MESH' else None,
    })
print('AUDIT_JSON ' + json.dumps(records, separators=(',', ':')))
