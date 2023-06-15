import pyblish.api
from rpm_pyblish_plugins.action_mesh_selectnonmanifoldvertices import MeshSelectNonManifoldVertices
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_nonmanifold_verts


class MeshTopologyNonManifold(pyblish.api.InstancePlugin):
    """Validate topology for non-manifold vertices."""

    label = f"Manifold Geometry"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshSelectNonManifoldVertices]

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        if (idx := get_nonmanifold_verts(mesh)).size:
            self.log.warning(f"Found {len(idx)} non-manifold vertices. "
                             f"You can use the {MeshSelectNonManifoldVertices.label} action in the context menu "
                             "of this validation to select non-manifold geometry.")
