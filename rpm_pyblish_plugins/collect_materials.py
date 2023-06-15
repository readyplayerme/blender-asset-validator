"""Collect materials."""
import bpy
import pyblish.api


class CollectMaterials(pyblish.api.ContextPlugin):
    """Collect material instances from the file."""

    label = f"Material Instances"
    version = (0, 1, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]

    def process(self, context):
        for material in bpy.data.materials:
            if material.is_grease_pencil:
                continue
            instance = context.create_instance(name=material.name,  # Name in Blender.
                                               family="Material")
            instance.append(material)
