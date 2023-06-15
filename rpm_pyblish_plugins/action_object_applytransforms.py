"""Apply all transforms to objects in Blender, keeping the objects' appearance."""
import bpy
import pyblish.api
from bqt.utils import context_window
from rpm_pyblish_plugins.shared_funcs import deselect_objects


class ObjectApplyTransforms(pyblish.api.Action):
    """Apply all transforms to objects in Blender, keeping the objects' appearance."""

    label = "Apply Transforms"
    icon = "check-circle"
    on = "failedOrWarning"

    @context_window
    def process(self, context, plugin):
        deselect_objects()
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                instance = result["instance"]
                try:
                    obj = bpy.data.objects[instance.name]
                except KeyError as e:
                    self.log.error(f"Action {self.label} failed. Object '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                bpy.ops.object.mode_set(mode="OBJECT")
                apply_transforms(obj)
                self.log.info(f"Successfully applied transforms for '{instance.name}'.")


def apply_transforms(obj: bpy.types.Object):
    """Apply all transformations (Translation, Rotation, Scale) to an object.

    :param obj: Mesh object.
    :type obj: bpy.types.Object
    """
    matrix_world = obj.matrix_world.copy()
    if obj.type == "MESH":
        for vert in obj.data.vertices:
            vert.co = matrix_world @ vert.co  # TODO #69 Vectorize transform of vertices.
    obj.matrix_world.identity()
