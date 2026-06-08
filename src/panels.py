import bpy


class AIMING_HELPER_PT_main(bpy.types.Panel):
    bl_label = "Aiming Helper"
    bl_idname = "AIMING_HELPER_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aiming Helper"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Test")        


def register():
    bpy.utils.register_class(AIMING_HELPER_PT_main)


def unregister():
    bpy.utils.unregister_class(AIMING_HELPER_PT_main)
    
