import pyblish.api
from rpm_pyblish_plugins.action_mesh_renameuvmap import MeshRenameUVMap
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_uvmap_names


class MeshUVMapName(pyblish.api.InstancePlugin):
    """Validate the name of UV maps."""

    label = "UV Map Name"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshRenameUVMap, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/mesh-validations/check-uv-map-name"  # noqa
    fix = MeshRenameUVMap
    map_name = "UVMap"

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        try:
            name = get_uvmap_names(mesh)[0]
        except IndexError:
            self.log.warning("No UV maps found.")
        if name != self.map_name:
            self.log.warning(
                f"UV map 0 must be named '{self.map_name}'. Found '{name}' instead."
                f"You can fix this issue by using the action '{MeshRenameUVMap.label}' "
                "from the context menu of this validation."
            )
