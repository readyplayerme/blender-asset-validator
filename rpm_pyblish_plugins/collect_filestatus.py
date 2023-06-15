"""Inject the current blend-file status into the context."""
import bpy
import pyblish.api


class CollectFileStatus(pyblish.api.ContextPlugin):
    """Inject the current file status into context."""

    order = pyblish.api.CollectorOrder
    label = "Blender File Status"
    hosts = ['blender']
    version = (0, 1, 0)

    def process(self, context):
        """Inject the current working file."""
        context.data['fileIsSaved'] = bpy.data.is_saved
        context.data['fileIsDirty'] = bpy.data.is_dirty
