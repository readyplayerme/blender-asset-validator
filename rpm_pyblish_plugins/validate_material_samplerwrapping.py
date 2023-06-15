"""Validate the texture sampler wrapping modes are not set to 'REPEAT' because of MIP mapping."""
import pyblish.api
from rpm_pyblish_plugins.action_material_setsamplerwrapping import MaterialSetSamplerWrapping
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class MaterialSamplerWrapping(pyblish.api.InstancePlugin):
    """Validate the texture wrapping modes are not set to 'REPEAT'.

    Assets usually have non-repeating textures. To avoid issues with MIP mapping, wrapping mode should be set to 'CLIP'.
    """

    label = "Texture Wrapping"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Material"]
    actions = [MaterialSetSamplerWrapping, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/texture-map-validations/check-texture-wrapping"  # noqa
    fix = MaterialSetSamplerWrapping

    def process(self, instance):
        material = instance[0]
        img_nodes = [node for node in material.node_tree.nodes if node.type == "TEX_IMAGE"]
        wrapping_modes = [node.extension for node in img_nodes]
        if "REPEAT" in wrapping_modes:
            self.log.warning("Validating texture sampler wrapping failed")
