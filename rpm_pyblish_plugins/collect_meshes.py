"""Collect meshes."""
import bpy
import pyblish.api

from rpm_pyblish_plugins.shared_funcs import object_from_mesh


class CollectMeshes(pyblish.api.ContextPlugin):
    """Collect Mesh instances from the file."""

    label = "Mesh Instances"
    version = (0, 3, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]
    skinned_meshes = False

    def process(self, context):
        for mesh in bpy.data.meshes:
            instance = context.create_instance(name=mesh.name, family="Mesh")  # Name in Blender.
            instance.append(mesh.name)
            # Is this a rigged mesh?
            obj = object_from_mesh(mesh)
            if obj.find_armature() or self.skinned_meshes:
                instance.data["families"] = ["Rigged"]
