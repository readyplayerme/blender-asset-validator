"""Validate that the parent of rigged objects is its armature."""
import pyblish.api
import rpm_pyblish_plugins.constants as const


class ObjectHierarchyParent(pyblish.api.InstancePlugin):
    """Validate that the parent of rigged objects is its armature.

    Other or nested parent-child relationships are not allowed.
    """

    label = f"Rig as Parent"
    version = (0, 1, 1)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Object", "Rigged"]
    match = pyblish.api.Subset

    def process(self, instance):
        parent = instance.data["parent"]
        rig = instance.data["armature"]
        if not (all((parent, rig)) and (parent == rig)):
            raise ValueError(
                f"'{instance.data['label']}' has failed {self.label} validation. "
                f"Objects in rigged asset types ({', '.join(const.RIGGED_ASSETS)}) should be children of "
                f"their associated Armature object. Found '{parent}' as parent instead. "
                "Make sure the object has an Armature modifier which Object-slot points to the armature."
            )
