"""Remove all animations from the current file."""
import bpy
import pyblish.api


class AnimationsClear(pyblish.api.Action):
    """Remove all animations from file."""

    label = "Remove animations"
    icon = "trash"
    on = "failedOrWarning"

    def process(self, context, plugin):
        remove_animations()


def remove_animations():
    """Remove all animations from the current file."""
    for animation in bpy.data.actions:
        bpy.data.actions.remove(animation)
