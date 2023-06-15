import pyblish.api
import bpy


class CollectBlenderCurrentFile(pyblish.api.ContextPlugin):
    """Inject the current working file into context."""

    order = pyblish.api.CollectorOrder - 0.5
    label = "Blender Current File"
    hosts = ['blender']
    version = (0, 1, 0)

    def process(self, context):
        """Inject the current working file."""
        current_file = bpy.data.filepath
        context.data['currentFile'] = current_file
        self.log.info(f"Found: {current_file}")
