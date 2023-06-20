"""
small wrapper to make the validator available as a Blender addon
"""




import bpy


class OpenRPMValidator(bpy.types.Operator):
    """Open the Ready Player Me Validator"""
    bl_idname = "rpm.show_validator"
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
