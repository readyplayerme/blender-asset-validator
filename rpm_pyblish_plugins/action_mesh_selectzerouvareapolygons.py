"""Select polygons which UVs have an area of 0."""
import bpy
import numpy as np
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import deselect_all, deselect_objects, get_mesh_by_name, get_uv_area, object_from_mesh


class MeshSelectZeroUVAreaPolygons(pyblish.api.Action):
    """Select polygons which UVs have an area of 0."""

    label = "Select Zero UV Areas"
    icon = "mouse-pointer"
    on = "failedOrWarning"

    @context_window
    def process(self, context, plugin):
        deselect_objects()

        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                instance = result["instance"]
                try:
                    mesh = get_mesh_by_name(context.data["current_item"])
                    obj = object_from_mesh(mesh)
                except KeyError as e:
                    self.log.error(f"Action {self.label} failed. Parent of mesh '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                print(mesh, obj)
                bpy.context.view_layer.objects.active = obj
                # Make sure we're in OBJECT mode for selection to work.
                bpy.ops.object.mode_set(mode="OBJECT")
                select_zero_uv_area_polygons(mesh)
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.tool_settings.mesh_select_mode = (False, False, True)
                self.log.info(f"Successfully selected faces with invalid UV area for '{instance.name}'.")


def select_zero_uv_area_polygons(mesh: bpy.types.Mesh):
    """Select faces with zero or overlapping uv area."""
    deselect_all(mesh)
    area = get_uv_area(mesh)
    is_invalid_polygon = np.isclose(area, 0.0)
    mesh.polygons.foreach_set("select", is_invalid_polygon)
