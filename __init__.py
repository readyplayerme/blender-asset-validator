"""
small wrapper to make the validator available as a Blender addon
"""

bl_info = {
    "name": "Ready Player Me Validator",
    "description": "Validate your Ready Player Me avatar in Blender",
    "author": "Ready Player Me",
    "version": (0, 0, 1),
    "blender": (2, 91, 0),
    "location": "Window/RPM Validator",
    "category": "Development",
}


import bpy


class OpenRPMValidator(bpy.types.Operator):
    """Open the Ready Player Me Validator"""
    bl_idname = "RPM.show_validator"
    bl_label = "Open Ready Player Me Validator"
    widget = None

    def execute(self, context):
        import rpm_validator
        self.widget = rpm_validator.show()
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    """Add a menu item to the 'Window' menu"""
    self.layout.operator(OpenRPMValidator.bl_idname)


def register():
    bpy.utils.register_class(OpenRPMValidator)
    bpy.types.TOPBAR_MT_window.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OpenRPMValidator)
    bpy.types.TOPBAR_MT_window.remove(menu_func)
