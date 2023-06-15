"""Validate animations in Blender.

There should be no animations in the file.
"""
import pyblish.api
from rpm_pyblish_plugins.action_animations_delete import AnimationsClear
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class AnimationsInFile(pyblish.api.InstancePlugin):
    """Validate that there are no animations in the file."""

    label = "Animation"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Animation"]
    actions = [AnimationsClear, OpenURL]

    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/animations/animation"  # noqa

    fix = AnimationsClear

    def process(self, instance):
        if instance:
            self.log.warning("There are animations in the file. There should be no animations.")
