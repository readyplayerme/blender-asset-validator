"""Collect animations."""
import bpy
import pyblish.api


class CollectAnimations(pyblish.api.ContextPlugin):
    """Collect animations from the file."""

    label = "Animation Instances"
    version = (0, 1, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]

    def process(self, context):
        """Grab existing animations."""
        for animation in bpy.data.actions:
            instance = context.create_instance(name=animation.name, family="Animation")  # Name in Blender.
            instance.append(animation)
