"""Valiate the amount of rigs in the blend file."""
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class RigCount(pyblish.api.InstancePlugin):
    """Validate there is only 1 armature/rig present in the scene."""

    label = "Rig Count"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Scenes"]
    actions = [OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/skinning-validations/check-rig-count"  # noqa
    target_rig_count = 1

    def process(self, instance):
        scene_data = instance.data.get("scene")
        armatures = [obj for obj in scene_data.objects if obj.type == "ARMATURE"]
        if (n_armatures := len(armatures)) != self.target_rig_count:
            self.log.error(
                f"Instance {instance} has failed {self.label} validation. "
                "There must only be 1 armature present in the scene. "
                f"Found {n_armatures} armatures instead."
            )
            raise ValueError(f"Validating {self.label} failed.")
        self.log.info(f"{self.label} has passed validation for instance {instance}.")
