"""Validate naming conventions."""
import rpm_pyblish_plugins.constants as const
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class NamingConvention(pyblish.api.InstancePlugin):
    """Validate object, mesh and material naming convention.

    They follow identical conventions, which means a mesh data-block always belongs to only 1 object of the same name.
    Each mesh has its own material.
    The naming convention depends on the asset type.
    """

    # TODO #76 Split naming convention checks for object, mesh, and material.

    label = "Naming Convention"
    version = (0, 1, 1)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = [fam for fam in ("Object", "Mesh", "Material")]

    actions = [OpenURL]
    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/hierarchy-objects/check-naming-conventions"  # noqa

    current_piece = const.NAMES

    def process(self, instance):

        name_found = instance.name in self.current_piece

        if not name_found:
            raise ValueError(f"Validating name failed for '{instance.name}'.")
