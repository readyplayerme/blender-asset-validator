import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_mesh_selectzeroareapolygons import MeshSelectZeroAreaPolygons
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_polygon_area


class MeshTopologyPolygonArea(pyblish.api.InstancePlugin):
    """Validate topology face area."""

    label = f"Polygon Area"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshSelectZeroAreaPolygons]

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        areas = get_polygon_area(mesh)
        zero_area_indices = np.argwhere(np.isclose(areas, 0.0)).flatten()
        if zero_area_indices.size:
            self.log.warning(f"{zero_area_indices.shape[0]} Faces with zero area detected. "
                             f"You can use the {MeshSelectZeroAreaPolygons.label} actions in the context menu "
                             "of this validation to select the faces. "
                             f"Invalid face indices: {zero_area_indices.tolist()}")
