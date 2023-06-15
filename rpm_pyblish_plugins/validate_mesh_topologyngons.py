import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_mesh_selectngons import MeshSelectNGons
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_polygon_sides


class MeshTopologyNGons(pyblish.api.InstancePlugin):
    """Validate there are no polygons with more than 4 or less than 3 edges in the mesh."""

    label = f"NGons"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshSelectNGons]

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        # N-gons.
        n_sides = get_polygon_sides(mesh)
        if np.any(n_sides > 4):
            self.log.warning(f"Only triangles and quads are allowed. Found {(n_sides > 4).sum()} ngons instead."
                             "This check ensures that tangent space can be computed on export."
                             f"You can use the {MeshSelectNGons.label} actions in the context menu of this "
                             "validation to select N-gons.")
        # Not even a triangle.
        if np.any(n_sides < 3):
            self.log.warning(f"Found {(n_sides < 3).sum()} two-edge-faces.")
