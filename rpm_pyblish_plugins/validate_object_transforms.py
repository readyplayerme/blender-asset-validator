"""Validate object's location, rotation, and scale are neutral."""
import pyblish.api
from rpm_pyblish_plugins.action_object_applytransforms import ObjectApplyTransforms
from rpm_pyblish_plugins.action_object_cleartransforms import ObjectClearTransforms
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class ObjectTransforms(pyblish.api.InstancePlugin):
    """Validate location, rotation, and scale of an object are neutral.

    Location & rotation: 0.0, 0.0, 0.0
    Scale: 1.0, 1.0, 1.0
    """

    label = "Transforms"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Object", "Rig"]
    actions = [ObjectClearTransforms, ObjectApplyTransforms, OpenURL]
    fix = ObjectApplyTransforms

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/hierarchy-objects/check-transforms"  # noqa

    def process(self, instance):
        loc = list(instance.data["location"])
        loc_delta = list(instance.data["locationDeltas"])
        rot = list(instance.data["rotation"])
        rot_delta = list(instance.data["rotationDeltas"])
        scale = list(instance.data["scale"])
        scale_delta = list(instance.data["scaleDeltas"])
        report_msg = f"'{instance.data['label']}' has failed {self.label} validation.\n"
        fix_msg = (
            f"To fix the issue, you can try using the '{ObjectClearTransforms.label}' or "
            f"'{ObjectApplyTransforms.label}' actions in the context menu of this validation."
        )

        if any(v != 0.0 for v in loc):
            self.log.error(f"{report_msg}Location of objects must be (0.0, 0.0, 0.0). Found {loc} instead.{fix_msg}")
        if any(v != 0.0 for v in loc_delta):
            self.log.error(
                f"{report_msg}Delta location of objects must be (0.0, 0.0, 0.0). "
                f"Found {loc_delta} instead. No funny business with deltas, please. :)"
            )
        if any(v != 0.0 for v in rot):
            self.log.error(
                f"{report_msg}Rotation of objects must be (0.0, 0.0, 0.0). "
                f"Found ({', '.join([str(i) for i in rot])}) instead.{fix_msg}"
            )
        if any(v != 0.0 for v in rot_delta):
            self.log.error(
                f"{report_msg}Delta rotation of objects must be (0.0, 0.0, 0.0). "
                f"Found ({', '.join([str(i) for i in rot_delta])}) instead. "
                "No funny business with deltas, please. :)"
            )
        if any(v != 1.0 for v in scale):
            self.log.error(f"{report_msg}Scale of objects must be (1.0, 1.0, 1.0). Found {scale} instead.{fix_msg}")
        if any(v != 1.0 for v in scale_delta):
            self.log.error(
                f"{report_msg}Delta scale of objects must be (1.0, 1.0, 1.0). "
                f"Found {scale_delta} instead. No funny business with deltas, please. :)"
            )
        if all(v == 0.0 for v in loc + loc_delta + rot + rot_delta) and all(v == 1.0 for v in scale + scale_delta):
            self.log.info(f"'{instance.data['label']}' has passed {self.label} validation.")
