"""Collect collection instances from the blend-file."""
import bpy
import pyblish.api


class CollectCollections(pyblish.api.ContextPlugin):
    """Collect collection instances from the file."""

    label = f"Collection Instances"
    version = (0, 1, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]

    def process(self, context):
        for coll in bpy.data.collections:
            instance = context.create_instance(name=coll.name, family="Collection")  # Name in Blender.
            # instance.append(coll)

            # TODO #70 get rid of LOD0 collection family, used in extractor rpm_pyblish_plugins. collect only ref to blender data.
            instance.data['label'] = f"COL:{coll.name}"  # Display name in pyblish UI.
            if coll.name == "LOD0":
                instance.data['families'] = ["LOD0"]
            instance.data['children'] = [c.name for c in coll.children]  # Nested collections.
            instance.data['objects'] = [obj.name for obj in coll.objects]
