import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_mesh_selectzerolengthedges import MeshSelectZeroLengthEdges
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_edge_lengths


class MeshTopologyZeroLengthEdges(pyblish.api.InstancePlugin):
    """Validate mesh topology edge lengths."""

    label = f"Edge Lengths"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshSelectZeroLengthEdges]

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        # Zero edge length.
        edge_lengths = get_edge_lengths(mesh)
        edge_indices = np.argwhere(np.isclose(edge_lengths, 0.0)).flatten()
        if edge_indices.size:  # Can't use any(), because it misses index 0.
            self.log.warning(f"{edge_indices.shape[0]} Edges with zero length detected. "
                             f"You can use the {MeshSelectZeroLengthEdges.label} actions in the context menu "
                             "of this validation to select the edges. "
                             f"Invalid edge indices: {edge_indices.tolist()}")
