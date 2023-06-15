"""Collect meshes."""
import bpy
import pyblish.api

from rpm_pyblish_plugins.shared_funcs import object_from_mesh


class CollectMeshes(pyblish.api.ContextPlugin):
    """Collect Mesh instances from the file."""

    label = f"Mesh Instances"
    version = (0, 2, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]

    def process(self, context):
        for mesh in bpy.data.meshes:
            instance = context.create_instance(name=mesh.name,  # Name in Blender.
                                               family="Mesh")
            instance.append(mesh.name)
            # Is this a rigged mesh?
            obj = object_from_mesh(mesh)
            if obj.find_armature():
                instance.data['families'] = ["Rigged"]
