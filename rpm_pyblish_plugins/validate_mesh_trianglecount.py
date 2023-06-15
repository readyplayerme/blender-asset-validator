"""Validate triangle count is within the budget for individual meshes."""
import rpm_pyblish_plugins.constants as const
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_polygon_sides


class MeshTriangleCount(pyblish.api.InstancePlugin):
    """Validate triangle count is within the budget for individual meshes."""

    label = "Mesh Triangle Count"
    __doc__ += "\nBudgets are as follows:\n" + ",\n".join(f"{k}: {v}" for k, v in const.TRIANGLE_BUDGETS.items())
    version = (0, 3, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True

    actions = [OpenURL]
    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/mesh-validations/check-mesh-triangle-count"  # noqa
    families = ["Mesh"]
    budget = 1000

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        n_poly_sides = get_polygon_sides(mesh)
        n_triangles = (n_poly_sides - 2).sum()
        try:
            self.budget = const.TRIANGLE_BUDGETS[instance.name]
        except KeyError:
            self.budget = 1000
            self.log.warning(f"No budget found for '{instance.name}'. Using {self.budget} triangles as a limit.")
        if n_triangles > self.budget:
            self.log.warning(
                f"'{instance.name}' has failed {self.label} validation. "
                f"The triangle budget for this mesh is {self.budget}. Found {n_triangles} triangles instead."
            )
