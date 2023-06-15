"""Limit the number of bone influences on the vertices of meshes."""
import bpy
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import deselect_objects, get_mesh_by_name, object_from_mesh, select_all_bmesh


class MeshLimitBoneInfluences(pyblish.api.Action):
    """Limit the number of bone influences on the vertices of meshes."""

    label = "Limit Bone Influences"
    icon = "crop"
    on = "failedOrWarning"

    @context_window
    def process(self, context, plugin):
        deselect_objects()
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                instance = result["instance"]
                try:
                    mesh = get_mesh_by_name(instance.name)
                    obj = object_from_mesh(mesh)
                except KeyError as e:
                    self.log.error(f"Action {self.label} failed. Parent of mesh '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                bpy.context.view_layer.objects.active = obj
                # Make sure we're in EDIT mode for operator to work.
                bpy.ops.object.mode_set(mode="EDIT")
                select_all_bmesh(mesh)
                bone_limit = 4
                bpy.ops.object.vertex_group_limit_total(group_select_mode="ALL", limit=bone_limit)
                bpy.ops.object.mode_set(mode="OBJECT")
                self.log.info(f"Successfully limited number of bone influences to {bone_limit} for '{instance.name}'.")
