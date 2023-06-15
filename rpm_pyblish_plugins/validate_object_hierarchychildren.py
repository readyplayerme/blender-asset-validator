"""Validate that the object has no children."""
import pyblish.api


class ObjectHierarchyChildren(pyblish.api.InstancePlugin):
    """Validate that the object has no children.

    Object relationships must be really simple. Only armatures have other objects as children.
    """

    label = "Object Children"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Object"]

    def process(self, instance):
        if children := instance.data["children"]:
            self.log.error(
                f"'{instance.data['label']}' has failed {self.label} validation. "
                f"Mesh objects must not have children. Found {', '.join(children)} as children instead. "
                f"Consider joining them with '{instance.name}' if they share the same material."
            )
            raise ValueError(f"Validating children failed for {instance.data['label']}.")
        else:
            self.log.info(f"'{instance.data['label']}' has passed {self.label} validation.")
