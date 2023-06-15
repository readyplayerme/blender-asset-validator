import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_mesh_normalizeweights import MeshNormalizeWeights
from rpm_pyblish_plugins.action_mesh_selectvertsbynonnormalweights import MeshSelectVerticesByNonNormalWeights
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_skin_weights


class MeshSkinWeightsNormalization(pyblish.api.InstancePlugin):
    """Validate that skin weights per vertex are normalized, i.e. add up to 1.

    The linear sum of the weights should be as close as reasonably possible to 1.0 for a given vertex.
    The threshold in the official glTF validation tool is set to 2e-7 times the number of non-zero weights per vertex.
    Normalizing weights is recommended for smooth animation deformations.
    If this valdiation does not pass, it can lead to affected vertices not deforming at all in a Ready Player Me Avatar!

    In Blender, you can turn on 'Auto Normalize' in the settings of the Draw tool under 'Options' to avoid this issue
    while painting skin weights.
    """

    label = "Normalized Skin Weights"
    version = (0, 2, 1)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh", "Rigged"]
    match = pyblish.api.Subset
    actions = [MeshSelectVerticesByNonNormalWeights, MeshNormalizeWeights, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/skinning-validations/check-skin-weight-normalization"  # noqa
    fix = MeshNormalizeWeights

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        weights = get_skin_weights(mesh)
        if not is_array_normalized(weights):
            self.log.warning(
                f"Skin weights per vertex do not sum up to 1. "
                f"You can use the '{MeshSelectVerticesByNonNormalWeights.label}' action in the "
                "context menu of this validation to select vertices with non-normalized skin weights. "
                f"To fix this issue, you can use the '{MeshNormalizeWeights.label}' action."
            )


def is_array_normalized(array: np.ndarray, tolerance: float = 2e-7, axis: int = 1) -> bool:
    """Check if values along an axis of a 2D array are normalized, i.e. add up to 1.

    Args:
        array (np.array): 2D array of values.
        tolerance (float): Tolerance multiplied with number of nonzero values along the axis. Defaults to 2e-7.
        axis (int): Axis along which to sum the values. Defaults to 1.

    Returns:
        bool: True if values along the given axis are normalized, False otherwise.
    """
    sums = array.sum(axis=axis)
    threshold = np.count_nonzero(array, axis=axis) * tolerance
    return np.isclose(sums, 1.0, atol=threshold).all()
