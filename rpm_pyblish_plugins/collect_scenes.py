"""Collect scenes instances from the blend-file."""
import bpy
import pyblish.api


class CollectScenes(pyblish.api.ContextPlugin):
    """Collect scenes instances from the file."""

    label = "Collection scenes"
    version = (0, 1, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]

    def process(self, context):
        for scene in bpy.data.scenes:
            instance = context.create_instance(name=scene.name, family="Scenes")  # Name in Blender.
            instance.append(scene)
            instance.data["scene"] = scene
