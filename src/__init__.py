import bpy


from . import panels
from . import operators
from . import properties


def register():
    properties.register()
    operators.register()
    panels.register()


def unregister():
    panels.unregister()
    operators.unregister()
    properties.unregister()


if __name__ == "__main__":
    register()
