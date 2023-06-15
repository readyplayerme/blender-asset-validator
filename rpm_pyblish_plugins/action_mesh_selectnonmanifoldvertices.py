"""Select edges that are non-manifold geometry."""
import bpy
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import deselect_objects, get_mesh_by_name, object_from_mesh


class MeshSelectNonManifoldVertices(pyblish.api.Action):
    """Select vertices that are non-manifold geometry."""

    label = "Select Non-manifold Vertices"
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
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action="DESELECT")
                bpy.context.tool_settings.mesh_select_mode = (True, False, False)
                bpy.ops.mesh.select_non_manifold()
                self.log.info(f"Successfully selected non-manifold edges for '{mesh}'.")
