import bpy


class AIMING_HELPER_PT_panel(bpy.types.Panel):
    bl_label = "Aiming Helper"
    bl_idname = "AIMING_HELPER_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Aiming Helper"


    def draw(self, context):
        layout = self.layout
        props  = context.scene.aiming_helper


        for pt, label in [
            ('eye',         'Eye'),
            ('rear_sight',  'Rear Sight'),
            ('front_sight', 'Front Sight'),
            ('target',      'Target'),
        ]:
            row    = layout.row(align=True)
            is_set = getattr(props, f"{pt}_set")
            obj    = getattr(props, f"{pt}_object")
            icon   = 'CHECKMARK' if is_set else 'LAYER_USED'
            row.label(text=label, icon=icon)
            op = row.operator("aiming_helper.set_point", text="Pick")
            op.point_type = pt

        layout.separator()
        layout.prop(props, "threshold")
        layout.separator()

        vis_text = "Stop Visualizing" if props.visualizing else "Start Visualizing"
        layout.operator("aiming_helper.toggle_visualize", text=vis_text,
                        icon='HIDE_ON' if props.visualizing else 'X')
        layout.operator("aiming_helper.clear", text="Clear All", icon='X')
    

def register():
    bpy.utils.register_class(AIMING_HELPER_PT_panel)


def unregister():
    bpy.utils.unregister_class(AIMING_HELPER_PT_panel)
