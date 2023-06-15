"""Enable the Use Nodes option on materials in Blender."""
import bpy
import pyblish.api


class MaterialSetUseNodes(pyblish.api.Action):
    """Enable the Use Nodes option on materials in Blender."""

    label = "Enable Use Nodes"
    icon = "toggle-on"
    on = "failedOrWarning"

    def process(self, context, plugin):
        for result in context.data['results']:
            if plugin == result["plugin"] and not result["action"]:
                instance = result['instance']
                try:
                    mat = bpy.data.materials[instance.name]
                except (AttributeError, KeyError) as e:
                    self.log.error(
                        f"Action {self.label} failed. Material '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                if not mat.use_nodes:
                    mat.use_nodes = True
                    self.log.info(f"Successfully enabled Use Nodes for '{instance.name}'.")
