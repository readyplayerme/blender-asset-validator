"""Select edges of meshes that have zero length."""
import bpy
import numpy as np
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import (
    deselect_objects,
    get_edge_lengths,
    get_mesh_by_name,
    object_from_mesh,
    select_components,
)


class MeshSelectZeroLengthEdges(pyblish.api.Action):
    """Select edges of a mesh with zero length."""

    label = "Select Zero Length Edges"
    icon = "mouse-pointer"
    on = "failedOrWarning"

    @context_window
    def process(self, context, plugin):
        deselect_objects()
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                # Display the selected edges in edit mode.
                mesh = get_mesh_by_name(context.data["current_item"])
                obj = object_from_mesh(mesh)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.tool_settings.mesh_select_mode = (False, True, False)
                select_zero_length_edges(mesh)


def select_zero_length_edges(mesh: bpy.types.Mesh):
    """Select edges with zero length."""
    lengths = get_edge_lengths(mesh)
    is_zero_length = np.isclose(lengths, 0.0)
    zero_length_idx = np.argwhere(is_zero_length).flatten()
    select_components(mesh, zero_length_idx, "EDGE")
