"""Collect object instances."""

import bpy
import pyblish.api

import rpm_pyblish_plugins.constants as const
from rpm_pyblish_plugins.shared_funcs import get_collections, get_transforms


class CollectObjects(pyblish.api.ContextPlugin):
    """Collect object instances from the file."""

    label = f"Object Instances"
    version = (0, 2, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]
    skinned_meshes = False

    def process(self, context):
        for obj in bpy.data.objects:
            if obj.type != "MESH":
                continue
            instance = context.create_instance(name=obj.name, family="Object")  # Name in Blender.
            instance.append(obj)
            instance.data["label"] = f"GEO:{obj.name}"  # Display name in pyblish UI.

            # Disable some common reference instances by default.
            if obj.name.lower() == f"{const.PREFIX.lower()}_head":
                instance.data["publish"] = False

            if (rig := obj.find_armature()) or self.skinned_meshes:
                instance.data["families"] = ["Rigged"]

            # Scene hierarchy.
            instance.data["collections"] = get_collections(obj)
            instance.data["parent"] = obj.parent.name if obj.parent else None
            instance.data["armature"] = rig.name if rig else None
            instance.data["children"] = [child.name for child in obj.children if obj.children]

            for key, value in get_transforms(obj).items():
                instance.data[key] = value
