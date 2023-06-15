import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_mesh_selectzerouvareapolygons import MeshSelectZeroUVAreaPolygons
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_uv_area


class MeshUVFaceArea(pyblish.api.InstancePlugin):
    """Validate UV area per face is not zero."""

    label = f"UV Area"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshSelectZeroUVAreaPolygons]

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        areas = get_uv_area(mesh)
        zero_uv_area_indices = np.argwhere(np.isclose(areas, 0.0)).flatten()
        if (n := zero_uv_area_indices.size):
            self.log.warning(f"{n} Faces with zero or overlapping UV area detected. "
                             f"You can use the {MeshSelectZeroUVAreaPolygons.label} actions in the context menu "
                             "of this validation to select the faces. "
                             f"Invalid face indices: {zero_uv_area_indices.tolist()}")
