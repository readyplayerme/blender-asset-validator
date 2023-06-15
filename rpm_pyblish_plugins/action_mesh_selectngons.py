"""Select N-gons in a Blender mesh."""
import bpy
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import deselect_all, deselect_objects, get_mesh_by_name, get_polygon_sides, object_from_mesh


class MeshSelectNGons(pyblish.api.Action):
    """Select N-gons in a Blender mesh."""

    label = "Select N-gons"
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
                select_ngons(mesh)
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.tool_settings.mesh_select_mode = (False, False, True)
                self.log.info(f"Successfully selected N-gons for '{mesh}'.")


def select_ngons(mesh: bpy.types.Mesh):
    """Select faces with more than 4 edges."""
    deselect_all(mesh)
    n_edges = get_polygon_sides(mesh)
    ngons = n_edges > 4
    mesh.polygons.foreach_set("select", ngons)
