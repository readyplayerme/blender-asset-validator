import pyblish.api
from rpm_pyblish_plugins.action_mesh_clearvertexcolors import MeshClearVertexColors
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, has_vertex_colors


class MeshVertexColors(pyblish.api.InstancePlugin):
    """Validate there are no vertex colors.

    Even though glTF supports vertex colors, we don't utilize them yet.
    """

    label = "Vertex Colors"
    version = (0, 2, 1)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshClearVertexColors, OpenURL]

    fix = MeshClearVertexColors
    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/mesh-validations/check-vertex-colors"  # noqa

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        if has_vertex_colors(mesh):
            self.log.warning(
                "Meshes must not have vertex colors."
                f"You can fix this issue by using the action '{MeshClearVertexColors.label}' "
                "from the context menu of this validation."
            )
