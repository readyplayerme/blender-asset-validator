import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_mesh_limitboneinfluences import MeshLimitBoneInfluences
from rpm_pyblish_plugins.action_mesh_selectverticesbyboneinfluence import MeshSelectVerticesByBoneInfluence
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_skin_weights


class MeshSkinBoneInfluences(pyblish.api.InstancePlugin):
    """Validate there are no more than 4 bones influencing each vertex.

    glTF client implementations are only required to support a single set of up to four weights and joints.
    For performance reasons, the number of influences when using a soft bind is limited to a maximum of four.
    This is the maximum number that some engines like Unity support by default.
    Even though more influences are possible, more than four bones influencing a vertex reduces performance.
    """

    label = "Bone Influences"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh", "Rigged"]
    match = pyblish.api.Subset
    actions = [MeshSelectVerticesByBoneInfluence, MeshLimitBoneInfluences, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/skinning-validations/check-skin-weight-influences-count"  # noqa
    fix = MeshLimitBoneInfluences
    influences_target = 4

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        weights = get_skin_weights(mesh)
        n_influences = (weights > 0.0).sum(axis=1)
        if np.any(n_influences == 0):
            idx = np.argwhere(n_influences == 0).flatten()
            self.log.warning(
                f"Found {len(idx)} vertices with no influence from any bone. " f"Indices: {', '.join(idx.astype(str))}"
            )
        if np.any(n_influences > self.influences_target):
            idx = np.argwhere(n_influences > self.influences_target).flatten()
            self.log.warning(
                f"Found {len(idx)} vertices with influences from more than {self.influences_target} bones."
                f" You can use the '{MeshSelectVerticesByBoneInfluence.label}' action in the context menu "
                f"of this validation to select vertices with more than {self.influences_target} "
                "bone influences. "
                f"To fix this issue, you can use the '{MeshLimitBoneInfluences.label}' action. "
                f"Indices: {', '.join(idx.astype(str))}"
            )
