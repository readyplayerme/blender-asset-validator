import bpy
import pyblish.api
from rpm_pyblish_plugins.action_object_setmode import ObjectSetMode
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class ObjectMode(pyblish.api.InstancePlugin):
    """Validate objects are in OBJECT mode."""

    label = "Object Mode"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Object", "Rig"]
    actions = [ObjectSetMode, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/hierarchy-objects/check-object-mode"  # noqa
    fix = ObjectSetMode

    def process(self, instance):
        obj = instance[0]

        # HACK: update, else the obj.mode doesn't seem to update
        bpy.context.view_layer.update()

        if obj.mode != "OBJECT":
            raise ValueError(
                f"Validating current mode of object failed for {instance.name}. "
                "Objects should be in OBJECT mode. "
                f"Object '{instance.name}' is currently in {obj.mode} mode instead."
            )
