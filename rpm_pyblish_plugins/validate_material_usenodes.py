"""Validate the material uses shader nodes in Blender."""
import pyblish.api
from rpm_pyblish_plugins.action_material_setusenodes import MaterialSetUseNodes
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class MaterialUseNodes(pyblish.api.InstancePlugin):
    """Validate that the material uses shader nodes."""

    label = "Material Nodes"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Material"]
    actions = [MaterialSetUseNodes, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/materials-validation/check-material-nodes"  # noqa
    fix = MaterialSetUseNodes

    def process(self, instance):
        material = instance[0]
        if not material.use_nodes:
            self.log.warning("Validating material nodes failed")
