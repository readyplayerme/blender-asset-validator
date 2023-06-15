"""Validate the material has backface culling enabled."""
import pyblish.api
from rpm_pyblish_plugins.action_material_setbackfaceculling import MaterialEnableBackfaceCulling
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class MaterialBackfaceCulling(pyblish.api.InstancePlugin):
    """Validate that materials have backface culling enabled.

    Double-sided faces do cost performance in the shader and are rarely desired.
    """

    label = "Backface Culling"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Material"]
    actions = [MaterialEnableBackfaceCulling, OpenURL]

    fix = MaterialEnableBackfaceCulling
    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/materials-validation/check-backface-culling"  # noqa
    backface_enabled = True

    def process(self, instance):
        material = instance[0]
        if material.use_backface_culling != self.backface_enabled:
            self.log.warning(f"Backface culling expected to be {self.backface_enabled} for material {material.name}")
