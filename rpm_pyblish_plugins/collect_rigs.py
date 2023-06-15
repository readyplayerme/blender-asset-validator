"""Collect the skeletons (aka skeletons/rigs)."""
from typing import List

import bpy
import pyblish.api

from rpm_pyblish_plugins.shared_funcs import get_collections, get_transforms


class CollectRigs(pyblish.api.ContextPlugin):
    """Collect rig (armature) instances from the file."""

    label = f"Rig Instances"
    version = (0, 1, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]

    def process(self, context):
        rigs = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE']
        context.data['nArmatures'] = len(rigs)
        for armature in rigs:
            mod_affected = {child for child in bpy.data.objects if child.find_armature() == armature}
            children = get_children(armature)
            children = mod_affected.union(children)

            instance = context.create_instance(armature.name, family="Rig")
            instance.append(armature)

            # TODO #73 Only collect armature reference, not armature properties.
            instance.data['label'] = f"RIG:{armature.name}"  # Display name in pyblish UI.
            instance.data['collections'] = get_collections(armature)
            # Collect parent.
            instance.data['parent'] = armature.parent
            instance.data['children'] = children
            instance.data['bones'] = armature.data.bones.keys()
            # Object transforms.
            for key, value in get_transforms(armature).items():
                instance.data[key] = value


def get_children(obj: bpy.types.Object) -> List[bpy.types.Object]:
    """Recursively get all the children of an object.

    :param obj: Object for which to retrieve children.
    :type obj: bpy.types.Object
    :return: List of children.
    :rtype: List[bpy.types.Object]
    """
    children = [obj]
    if obj.children:
        for child in obj.children:
            children.extend(get_children(child))
    return children
