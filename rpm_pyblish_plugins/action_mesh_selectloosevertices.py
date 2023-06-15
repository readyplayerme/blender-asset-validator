"""Select vertices that are not connected to any faces."""
import bmesh
import bpy
import numpy as np
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import deselect_all, deselect_objects, get_mesh_by_name, object_from_mesh


class MeshSelectLooseVertices(pyblish.api.Action):
    """Select vertices that are not connected to any faces."""

    label = "Select Loose Verts"
    icon = "mouse-pointer"
    on = "failedOrWarning"

    @context_window
    def process(self, context, plugin):
        deselect_objects()
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                try:
                    mesh = get_mesh_by_name(context.data["current_item"])
                    obj = object_from_mesh(mesh)
                except KeyError as e:
                    self.log.error(f"Action {self.label} failed. Parent of mesh '{mesh}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{mesh}'.") from e
                bpy.context.view_layer.objects.active = obj
                # Make sure we're in OBJECT mode for selection to work.
                bpy.ops.object.mode_set(mode="OBJECT")
                select_loose_vertices(mesh)
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.tool_settings.mesh_select_mode = (True, False, False)
                self.log.info(f"Successfully selected loose vertices for '{mesh}'.")


def select_loose_vertices(mesh: bpy.types.Mesh, replace: bool = True):
    """Select loose vertices."""
    if replace:
        deselect_all(mesh)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    is_non_manifold = np.array([v.is_wire for v in bm.verts])
    non_manifold_idx = np.argwhere(is_non_manifold).flatten()
    for idx in non_manifold_idx:
        bm.verts[idx].select_set(True)
    bm.to_mesh(mesh)
    bm.clear()
    bm.free()
    del bm
