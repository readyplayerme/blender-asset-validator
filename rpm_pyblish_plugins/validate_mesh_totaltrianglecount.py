"""Validate triangle count is within the budget for total meshes."""
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class TotalTriangleCount(pyblish.api.InstancePlugin):
    """Validate triangle count is within the budget for individual meshes."""

    label = "Total Triangle Count"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Scenes"]

    actions = [OpenURL]
    # TODO add docs and links.
    url = ""  # noqa
    budget = 1000

    def process(self, instance):
        total_triangles = instance.context.data["total_triangles"]
        print(total_triangles)
        print(self.budget)
        if total_triangles > self.budget:
            self.log.warning(
                "The outfit has failed %s validation. "
                "The triangle budget for this mesh is %s. Found %s triangles instead.",
                self.label,
                self.budget,
                total_triangles,
            )
