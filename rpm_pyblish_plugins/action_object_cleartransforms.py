"""Set the objects' transforms to their original state."""

import mathutils

import bpy
import pyblish.api
from rpm_pyblish_plugins.shared_funcs import deselect_objects


class ObjectClearTransforms(pyblish.api.Action):
    """Set the objects' transforms to their original state."""
    label = "Clear Transforms"
    icon = "eraser"
    on = "failedOrWarning"

    def process(self, context, plugin):
        deselect_objects()
        for result in context.data['results']:
            if plugin == result["plugin"] and not result["action"]:
                instance = result['instance']
                try:
                    obj = bpy.data.objects[instance.name]
                except KeyError as e:
                    self.log.error(
                        f"Action {self.label} failed. Object '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                clear_transforms(obj)
                self.log.info(f"Successfully cleared transforms for '{instance.name}'.")


def clear_transforms(obj: bpy.types.Object,
                     use_location: bool = True,
                     use_rotation: bool = True,
                     use_scale: bool = True):
    """Reset transforms.

    Location, rotation, and scale can individually be excluded from the reset.
    Does not accoutn for delta transforms.

    :param obj: Transformed object.
    :type obj: bpy.types.Object
    :param use_location: Clear location, defaults to True
    :type use_location: bool, optional
    :param use_rotation: Clear rotation, defaults to True
    :type use_rotation: bool, optional
    :param use_scale: Clear scale, defaults to True
    :type use_scale: bool, optional
    """
    # Decompose current matrix into translation, rotation, scale.
    loc, rot, scale = obj.matrix_basis.decompose()
    T = mathutils.Matrix.Translation(loc)
    R = rot.to_matrix().to_4x4()
    S = mathutils.Matrix.Diagonal(scale).to_4x4()
    basis = [T, R, S]
    # Neutral transform matrix.
    identity = mathutils.Matrix()
    transform = [identity, identity, identity]

    # Setup final transform matrix.
    def swap(i):
        transform[i], basis[i] = basis[i], transform[i]

    if use_location:
        swap(0)
    if use_rotation:
        swap(1)
    if use_scale:
        swap(2)
    matrix = transform[0] @ transform[1] @ transform[2]
    # Apply matrix to object.
    if hasattr(obj, "transform"):
        obj.data.transform(matrix)
    for c in obj.children:
        c.matrix_local = matrix @ c.matrix_local
    obj.matrix_basis = basis[0] @ basis[1] @ basis[2]
    if obj.type == 'ARMATURE':
        for pose_bone in obj.pose.bones:
            pose_bone.matrix_basis = matrix
