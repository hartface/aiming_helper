import bpy
from . import utils


class AIMING_HELPER_OT_set_point(bpy.types.Operator):
    bl_idname = "aiming_helper.set_point"
    bl_label = "Set Aiming Point"
    bl_description = "Click a point on a mesh to set it"

    point_type: bpy.props.StringProperty()

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            return {'PASS_THROUGH'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            coord  = (event.mouse_region_x, event.mouse_region_y)
            region = context.region
            rv3d   = context.region_data

            from bpy_extras.view3d_utils import region_2d_to_origin_3d, region_2d_to_vector_3d
            ray_origin = region_2d_to_origin_3d(region, rv3d, coord)
            ray_dir    = region_2d_to_vector_3d(region, rv3d, coord)

            depsgraph = context.evaluated_depsgraph_get()
            result, location, normal, index, obj, matrix = context.scene.ray_cast(
                depsgraph, ray_origin, ray_dir
            )

            if result and obj:
                local_pos = obj.matrix_world.inverted() @ location
                props = context.scene.aiming_helper
                pt = self.point_type
                setattr(props, f"{pt}_object",    obj)
                setattr(props, f"{pt}_local_pos", local_pos)
                setattr(props, f"{pt}_set",       True)
                self.report({'INFO'}, f"{pt.replace('_', ' ').title()} set on '{obj.name}'")
            else:
                self.report({'WARNING'}, "No mesh hit — click directly on a surface")

            context.window.cursor_modal_restore()
            return {'FINISHED'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.window.cursor_modal_restore()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "Must be run in the 3D viewport")
            return {'CANCELLED'}
        context.window.cursor_modal_set('EYEDROPPER')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


_draw_handle    = None
_draw_handle_2d = None


class AIMING_HELPER_OT_toggle_visualize(bpy.types.Operator):
    bl_idname = "aiming_helper.toggle_visualize"
    bl_label = "Toggle Visualization"

    def execute(self, context):
        global _draw_handle, _draw_handle_2d
        props = context.scene.aiming_helper

        if not props.visualizing:
            _draw_handle = bpy.types.SpaceView3D.draw_handler_add(
                utils.draw_callback_3d, (self, context), 'WINDOW', 'POST_VIEW'
            )
            _draw_handle_2d = bpy.types.SpaceView3D.draw_handler_add(
                utils.draw_callback_2d, (self, context), 'WINDOW', 'POST_PIXEL'
            )
            props.visualizing = True
        else:
            if _draw_handle:
                bpy.types.SpaceView3D.draw_handler_remove(_draw_handle, 'WINDOW')
            if _draw_handle_2d:
                bpy.types.SpaceView3D.draw_handler_remove(_draw_handle_2d, 'WINDOW')
            _draw_handle    = None
            _draw_handle_2d = None
            props.visualizing = False

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}


class AIMING_HELPER_OT_clear(bpy.types.Operator):
    bl_idname = "aiming_helper.clear"
    bl_label = "Clear All Points"

    def execute(self, context):
        props = context.scene.aiming_helper
        for pt in ['eye', 'rear_sight', 'front_sight', 'target']:
            setattr(props, f"{pt}_set",    False)
            setattr(props, f"{pt}_object", None)
        return {'FINISHED'}
