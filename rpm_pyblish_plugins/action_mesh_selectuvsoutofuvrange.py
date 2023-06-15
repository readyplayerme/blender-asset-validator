"""Select UVs that are not within 0-1 range of UV space."""
import bpy
import numpy as np
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import deselect_objects, get_mesh_by_name, get_uvs, object_from_mesh, select_all


class MeshSelectUVsOutOfUVRange(pyblish.api.Action):
    """Select UVs that are not within 0-1 range of UV space."""

    label = "Select UVs"
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
                # UV data is only accessible in object mode.
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode="OBJECT")
                select_uvs_out_of_range(mesh)
                bpy.ops.object.mode_set(mode="EDIT")
                self.log.info(f"Successfully selected UVs outside 0-1 UV space for '{mesh}'.")


def select_uvs_out_of_range(mesh: bpy.types.Mesh, uv_layer_index: int = 0):
    """Select UVs that are not within 0-1 range of UV space.

    :param mesh: Mesh data-block
    :type mesh: bpy.types.Mesh
    :param uv_layer_index: Which UV layer to consider, defaults to index 0
    :type uv_layer_index: int, optional
    """
    # In order to see the selected UVs in the editor, the vertices must be selected.
    select_all(mesh)
    # Get current UV data.
    u, v = get_uvs(mesh, uv_layer_index).T
    uv_layer = mesh.uv_layers[uv_layer_index]
    uv_layer.data.foreach_set("select", np.logical_or((u <= 0) | (u >= 1), (v <= 0) | (v >= 1)))
