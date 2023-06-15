"""Validate triangle count is within the budget for individual meshes."""
import rpm_pyblish_plugins.constants as const
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class CheckRequiredElements(pyblish.api.InstancePlugin):
    """Validate if the required pieces are present and that there are no extras."""

    label = "Verify Required Meshes"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Scenes"]

    actions = [OpenURL]
    # TODO add docs and links.
    url = ""  # noqa
    pieces = const.NAMES

    def process(self, instance):
        # Access the meshes in the scene instance
        scene_data = instance.data.get("scene")
        meshes = [obj for obj in scene_data.objects if obj.type == "MESH"]
        mesh_names = [obj.name for obj in meshes]

        missing_elements = [item for item in self.pieces if item not in mesh_names]
        extra_elements = [item for item in mesh_names if item not in self.pieces]
        # Print the missing and extra elements
        if missing_elements:
            self.log.warning(f"Missing Elements: {', '.join(missing_elements)}")
        if extra_elements:
            self.log.warning(f"Extra Elements: {', '.join(extra_elements)}")
