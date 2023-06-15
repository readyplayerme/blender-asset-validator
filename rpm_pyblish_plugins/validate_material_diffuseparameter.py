"""Validate the materials' diffuse color parameter is pure white."""
import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_material_setdiffuse import MaterialSetDiffuseWhite
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class MaterialDiffuse(pyblish.api.InstancePlugin):
    """Validate that materials' diffuse color is pure white.

    Otherwise this value mixes with the base color map for FBX exports.
    """

    label = "Material Diffuse"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Material"]
    actions = [MaterialSetDiffuseWhite, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/materials-validation/check-material-base-color"  # noqa
    fix = MaterialSetDiffuseWhite

    def process(self, instance):
        material = instance[0]
        diffuse = list(material.diffuse_color)
        if not (np.array(diffuse) == 1.0).all():
            self.log.warning("Validating material diffuse failed")
