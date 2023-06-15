"""Set Blender objects into Object mode."""
import bpy
import pyblish.api
from bqt.utils import context_window


class ObjectSetMode(pyblish.api.Action):
    """Set mode to object mode."""

    label = "set object mode"
    icon = "floppy-o"

    @context_window
    def process(self, context, plugin):
        # with maintain_selection():
        for obj in bpy.data.objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="OBJECT")
