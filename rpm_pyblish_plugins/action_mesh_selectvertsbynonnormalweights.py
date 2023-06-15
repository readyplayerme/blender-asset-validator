"""Select vertices which have non-normalized weights."""
import bpy
import numpy as np
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import deselect_all, deselect_objects, get_mesh_by_name, get_skin_weights, object_from_mesh


class MeshSelectVerticesByNonNormalWeights(pyblish.api.Action):
    """Select vertices which have non-normalized weights."""

    label = "Select Vertices"
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
                weights = get_skin_weights(mesh)
                select_vertices_by_weight(mesh, weights)
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.tool_settings.mesh_select_mode = (True, False, False)
                self.log.info(f"Successfully selected vertices with non-normalized weights for '{mesh}'.")


def select_vertices_by_weight(mesh: bpy.types.Mesh, weights: np.ndarray):
    """Select vertices which have non-normalized weights.

    :param mesh: Mesh data-block
    :type mesh: bpy.types.Mesh
    :param weights: Skin weights.
    :type weights: np.ndarray
    """
    deselect_all(mesh)
    total_weights = weights.sum(axis=1)
    select_verts = ~np.isclose(total_weights, 1.0)
    mesh.vertices.foreach_set("select", select_verts)
