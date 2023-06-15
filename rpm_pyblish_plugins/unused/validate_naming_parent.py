import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import find_users


class HierarchyParentName(pyblish.api.InstancePlugin):
    """Validate the name of a mesh or material is the same as its parent's."""

    label = "Parent Name Match"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh", "Material"]
    actions = [OpenURL]

    # TODO #68 add action to rename parent or child, if one of them follows name conv
    # TODO hookup autofix
    url = "https://www.notion.so/wolf3d/Validate-Parent-Name-e2b69728270843438143e89df96de9ea"

    def process(self, instance):
        name = instance.data["name"]
        try:
            parent_name = find_users(instance[0])[0].name  # Just treat the first user as the parent.
        except (IndexError, AttributeError):
            parent_name = None
        if name == parent_name:  # ToDo: remove log on success. #67
            self.log.info(f"'{instance.name}' has passed {self.label} validation.")
        else:
            self.log.warning(
                f"'{instance.name}' has failed {self.label} validation. "
                f"'{name}' doesn't match its parent '{parent_name}'. "
                "Meshes and materials must have the same name as their parent. "
                "If the data-block is assigned to multiple objects, the first one found takes precedence."
            )
