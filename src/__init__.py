import bpy


from . import panels
from . import operators
from . import properties


def register():
    properties.register()
    operators.register()
    panels.register()


def unregister():
    properties.unregister()
    operators.unregister()
    panels.unregister()


if __name__ == "__main__":
    register()
