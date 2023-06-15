"""Select vertices with invalid bones influencing them."""
from typing import List

import bpy
import rpm_pyblish_plugins.constants as const
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import (
    deselect_objects,
    get_mesh_by_name,
    get_vertex_groups_name,
    object_from_mesh,
    select_components,
)


class MeshSelectVerticesInvalidBones(pyblish.api.Action):
    """Select vertices ."""

    label = "Select Vertices"
    icon = "mouse-pointer"
    on = "failedOrWarning"

    @context_window
    def process(self, context, plugin):
        deselect_objects()
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                instance = result["instance"]
                # Display the selected edges in edit mode.
                mesh = get_mesh_by_name(instance.name)
                obj = object_from_mesh(mesh)
                bpy.context.view_layer.objects.active = obj
                vertex_names = get_vertex_groups_name(mesh)
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.tool_settings.mesh_select_mode = (True, False, False)
                select_vertices_by_invalid_bones(mesh, vertex_names)


def select_vertices_by_invalid_bones(mesh: bpy.types.Mesh, array: dict):
    """Selects vertices which have invalid bones influence"""
    invalid_indices: List[int] = []
    for vertex_index, vertex_groups in enumerate(array.values()):
        invalid_indices.extend(
            vertex_index for vertex_group in vertex_groups if vertex_group not in const.FULLBODY_BONES
        )
    select_components(mesh, invalid_indices, "VERT")
