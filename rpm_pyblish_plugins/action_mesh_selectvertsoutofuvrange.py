"""Select vartices that are associated with UV coordinates that are outside the 0-1 UV space."""
import bpy
import numpy as np
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.action_mesh_selectuvsoutofuvrange import select_uvs_out_of_range
from rpm_pyblish_plugins.shared_funcs import deselect_all, deselect_objects, get_mesh_by_name, object_from_mesh


class MeshSelectVerticesOutOfUVRange(pyblish.api.Action):
    """Select vartices that are associated with UV coordinates that are outside the 0-1 UV space."""

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
                # UV data is only accessible in object mode.
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode="OBJECT")
                select_uvs_out_of_range(mesh)
                select_vertices_by_selected_uvs(mesh)
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.tool_settings.mesh_select_mode = (True, False, False)
                self.log.info(f"Successfully selected vertices with UVs outside 0-1 UV space for '{mesh}'.")


def select_vertices_by_selected_uvs(mesh: bpy.types.Mesh, uv_layer_index: int = 0):
    """Select vertices that have any UV coordinates of adjacent corners that are outside the 0-1 UV space.

    :param mesh: Mesh data-block
    :type mesh: bpy.types.Mesh
    :param uv_layer_index: Which UV layer to consider, defaults to index 0
    :type uv_layer_index: int, optional
    """
    deselect_all(mesh)
    uv_layer = mesh.uv_layers[uv_layer_index]
    selected_uvs = np.empty((2, len(mesh.loops)), dtype=np.int32)
    mesh.loops.foreach_get("vertex_index", selected_uvs[0])
    uv_layer.data.foreach_get("select", selected_uvs[1])

    selected_verts = np.zeros(len(mesh.vertices), dtype=np.int32)

    np.logical_or.at(selected_verts, *selected_uvs)
    mesh.vertices.foreach_set("select", selected_verts)
    bpy.context.window.workspace = bpy.data.workspaces["UV Editing"]
