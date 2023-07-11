import rpm_pyblish_plugins.constants as const
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, object_from_mesh


class ObjectArmature(pyblish.api.InstancePlugin):
    """Pyblish plugin to validate the presence of an armature modifier on a mesh instance."""

    label = "Object Armature"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = False
    families = ["Object", "Rig"]
    match = pyblish.api.Subset
    actions = [OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/mesh-validations/check-armature"  # noqa

    def process(self, instance):
        """
        Process the instance to validate the presence of an armature modifier.
        """

        mesh = get_mesh_by_name(instance.name)
        obj = object_from_mesh(mesh)

        if obj.find_armature() is None:
            self.log.error("Found %s with no armature modifier", mesh.name)
