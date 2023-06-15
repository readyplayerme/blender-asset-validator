import pyblish.api
from rpm_pyblish_plugins.action_mesh_selectuvsoutofuvrange import MeshSelectUVsOutOfUVRange
from rpm_pyblish_plugins.action_mesh_selectvertsoutofuvrange import MeshSelectVerticesOutOfUVRange
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_uvs


class MeshUVMapRange(pyblish.api.InstancePlugin):
    """Validate UVs are in the 0-1 range.

    Having all UVs in the 0-1 range of UV space is necessary for the texture atlassing to work correctly.
    Tip: In Blender you can enable 'Constrain to Image Bounds' in the UV menu of the UV editor.
    This will prevent leaving the 0-1 range while editing UVs.
    """

    label = "UV Map Range"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Mesh"]
    actions = [MeshSelectUVsOutOfUVRange, MeshSelectVerticesOutOfUVRange, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/mesh-validations/check-uv-map-range"  # noqa

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        uv_data = get_uvs(mesh)

        try:
            is_valid = uv_data.max() <= 1.0 and uv_data.min() >= 0.0
        except ValueError:
            self.log.warning("Could not read UV data. Please try again in OBJECT mode.")
        else:
            if not is_valid:
                self.log.warning(
                    f"UVs must be confined to the 0-1 UV space. "
                    "Otherwise the texture atlassing optimization may produce unwanted results."
                    f"You can use the '{MeshSelectUVsOutOfUVRange.label}' action in the context menu of "
                    "this validation to select UV outside the allowed range. To select vertices "
                    "associated with them, "
                    f"you can use the action '{MeshSelectVerticesOutOfUVRange.label}'."
                )
