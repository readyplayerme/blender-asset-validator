import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_skin_weights


class MeshSkin(pyblish.api.InstancePlugin):
    """Validate the mesh is completely skinned.

    glTF client implementations are required to have all vertex skinned.
    """

    label = "Mesh Skinning"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = False
    families = ["Mesh", "Rigged"]
    match = pyblish.api.Subset
    actions = [OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/mesh-validations/check-skinning"  # noqa

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        weights = get_skin_weights(mesh)
        n_influences = (weights > 0.0).sum(axis=1)

        if np.any(n_influences == 0):
            idx = np.argwhere(n_influences == 0).flatten()
            self.log.error("Found %d vertices with no influence from any bone.", len(idx))
