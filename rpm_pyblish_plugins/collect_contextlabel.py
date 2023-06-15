"""Set custom label for the context in the Pyblish GUI."""
import pyblish.api


class CollectContextLabel(pyblish.api.ContextPlugin):
    """Set custom label for the context in the Pyblish GUI."""

    order = pyblish.api.CollectorOrder
    label = f"Custom Context Label"
    hosts = ['blender']

    def process(self, context):
        context.data["label"] = "Blender File"
