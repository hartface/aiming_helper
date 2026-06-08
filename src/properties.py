import bpy


class AimingHelperProperties(bpy.types.PropertyGroup):
    eye_object: bpy.props.PointerProperty(type=bpy.types.Object)
    eye_local_pos: bpy.props.FloatVectorProperty(subtype='XYZ')
    eye_set: bpy.props.BoolProperty(default=False)

    rear_sight_object: bpy.props.PointerProperty(type=bpy.types.Object)
    rear_sight_local_pos: bpy.props.FloatVectorProperty(subtype='XYZ')
    rear_sight_set: bpy.props.BoolProperty(default=False)

    front_sight_object: bpy.props.PointerProperty(type=bpy.types.Object)
    front_sight_local_pos: bpy.props.FloatVectorProperty(subtype='XYZ')
    front_sight_set: bpy.props.BoolProperty(default=False)

    target_object: bpy.props.PointerProperty(type=bpy.types.Object)
    target_local_pos: bpy.props.FloatVectorProperty(subtype='XYZ')
    target_set: bpy.props.BoolProperty(default=False)

    visualizing: bpy.props.BoolProperty(default=False)
    threshold: bpy.props.FloatProperty(
        name="Alignment Threshold",
        default=0.05,
        min=0.001,
        max=1.0,
        description="How strict the alignment check is"
    )


def register():
    bpy.utils.register_class(AimingHelperProperties)
    bpy.types.Scene.aiming_helper = bpy.props.PointerProperty(type=AimingHelperProperties)


def unregister():
    del bpy.types.Scene.aiming_helper
    bpy.utils.unregister_class(AimingHelperProperties)
