import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_uvmap_names


class MeshUVMapCount(pyblish.api.InstancePlugin):
    """Validate there's only 1 UV map per mesh.

    Even though glTF and the WebGL renderer three.js support 2 UV maps, we currently only utilize one.
    """

    label = "UV Map Count"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]

    actions = [OpenURL]
    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/mesh-validations/check-uv-map-count"  # noqa
    map_count = 1

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        uv_maps = get_uvmap_names(mesh)
        if len(uv_maps) != self.map_count:
            self.log.warning(
                f"Meshes must only have 1 UV map. Found {len(uv_maps)} UV maps instead. "
                "Leaving out unnecessary UV maps keeps the file size and memory footprint low."
            )
