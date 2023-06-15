"""Validate the rig is not a child of another object."""
import pyblish.api


class RigHierarchyParent(pyblish.api.InstancePlugin):
    """Validate the armature/rig is not a child of another object."""

    label = f"Armature's Parent"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Rig"]

    def process(self, instance):
        if instance.data['parent']:
            self.log.error(f"'{instance.data['label']}' has failed {self.label} validation. "
                           "The armature must not have a parent object.")
            raise ValueError(f"Validating parent object failed for {instance.data['label']}")
        self.log.info(f"'{instance.data['label']}' has passed {self.label} validation.")