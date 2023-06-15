import pyblish.api
from rpm_pyblish_plugins.action_mesh_selectlooseedges import MeshSelectLooseEdges
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_loose_edges


class MeshTopologyLooseEdges(pyblish.api.InstancePlugin):
    """Validate topology loose edges."""

    label = f"Loose Edges"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshSelectLooseEdges]

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        if (idx := get_loose_edges(mesh)).size:
            self.log.warning(f"Found loose edges. "
                             f"You can use the {MeshSelectLooseEdges.label} action in the context menu of this "
                             "validation to select loose edges."
                             f"Loose Edge Indexes: {', '.join((str(i) for i in idx))}"
                             )
