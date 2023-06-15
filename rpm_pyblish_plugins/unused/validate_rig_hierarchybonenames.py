import rpm_pyblish_plugins.constants as const
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL

# Map asset type to required skeleton.
skeleton_map = {
    "outfit": const.FULLBODY_BONES,
    "top": const.FULLBODY_BONES,
    "bottom": const.FULLBODY_BONES,
    "footwear": const.FULLBODY_BONES,
    "integral": const.FULLBODY_BONES,
    "beard": const.BEARD_BONES,
    "headwear": const.HEADWEAR_BONES,
    "hair": const.HEADWEAR_BONES,
}


class RigBoneNames(pyblish.api.InstancePlugin):
    """Validate that names of the bones are correct for the asset type."""

    label = "Bone Names"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Rig"]

    actions = [OpenURL]
    url = "https://www.notion.so/wolf3d/Joint-names-b6484cd6daf64022bfd1d8f606956413"

    def process(self, instance):
        asset_type = instance.context.data["assetType"]
        bones = instance.data["bones"]
        if valid_bones := skeleton_map.get(asset_type, None):
            report_msg = (
                f"has failed {self.label} validation.\n"
                f"Bone names didn't match known configuration for asset type {asset_type}. "
            )
            failed = False
            if diff := set(valid_bones).difference(bones):
                failed = True
                self.log.error(report_msg + f"Missing bones: {', '.join(diff)}.")
            if diff := set(bones).difference(valid_bones):
                failed = True
                self.log.error(
                    report_msg + f"These bones do not belong to the configuration: {', '.join(diff)}. "
                    f"Asset type {asset_type} must have these bones: {', '.join(valid_bones)}"
                )
            if failed:
                raise ValueError(f"Validating names of bones failed for {instance.data['label']}")
            self.log.info(f"{instance.name}' has passed {self.label} validation.")
        else:
            self.log.warning(
                f"Can't validate bones for '{instance.data['label']}'. "
                f"Asset type {asset_type} has no known bones configuration."
            )
