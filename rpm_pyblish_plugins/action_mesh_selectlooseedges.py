"""Select edges that are not connected to any faces."""
import bpy
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import (
    deselect_objects,
    get_loose_edges,
    get_mesh_by_name,
    object_from_mesh,
    select_components,
)


class MeshSelectLooseEdges(pyblish.api.Action):
    """Select Edges that are not connected to any faces."""

    label = "Select Loose Edges"
    icon = "mouse-pointer"
    on = "failedOrWarning"

    @context_window
    def process(self, context, plugin):
        deselect_objects()
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                mesh = get_mesh_by_name(context.data["current_item"])
                obj = object_from_mesh(mesh)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.tool_settings.mesh_select_mode = (False, True, False)
                loose_idx = get_loose_edges(mesh)
                select_components(mesh, loose_idx, component="EDGE")
