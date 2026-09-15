import bpy
import json


def extension_enabled(module_name):
    return module_name in bpy.context.preferences.addons


result = {
    "blenderVersion": bpy.app.version_string,
    "initialObjects": len(bpy.data.objects),
    "extensions": {
        "mcp": extension_enabled("bl_ext.blender_lab.mcp"),
        "cloudrig": extension_enabled("bl_ext.blender_org.cloudrig"),
        "easyweight": extension_enabled("bl_ext.blender_org.easyweight"),
        "pose_shape_keys": extension_enabled("bl_ext.blender_org.pose_shape_keys"),
    },
}

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.0))
temporary = bpy.context.object
temporary.name = "GRIMO_DOCTOR_TEMP"
result["temporaryObjectCreated"] = temporary.name in bpy.data.objects
bpy.data.objects.remove(temporary, do_unlink=True)
result["temporaryObjectDeleted"] = "GRIMO_DOCTOR_TEMP" not in bpy.data.objects

print("GRIMO_BLENDER_DOCTOR=" + json.dumps(result, sort_keys=True))
