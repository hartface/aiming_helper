import bpy


from . import panels


def register():
    panels.register()


def unregister():
    panels.unregister()


if __name__ == "__main__":
    register()
