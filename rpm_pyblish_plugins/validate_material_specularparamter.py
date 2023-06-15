"""Validate the material has a specular value of 0.5."""
import pyblish.api
from rpm_pyblish_plugins.action_material_setspecular import MaterialSetSpecular
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class MaterialSpecular(pyblish.api.InstancePlugin):
    """Validate the material has a specular value of 0.5.

    The glTF default PBR shader uses a specular value of 0.5 that cannot be changed.
    Using a different value in Blender for preview can result in unexpected appearance.
    """

    label = "Material Specular"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Material"]
    actions = [MaterialSetSpecular, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/materials-validation/check-material-specular"  # noqa
    fix = MaterialSetSpecular

    def process(self, instance):
        material = instance[0]
        spec = material.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value
        if spec != 0.5:
            self.log.warning("Validating material specular failed")
