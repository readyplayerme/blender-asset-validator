"""Enable backface culling on materials."""
import bpy
import pyblish.api


class MaterialEnableBackfaceCulling(pyblish.api.Action):
    """Enable backface culling on materials."""

    label = "Enable Backface Culling"
    icon = "eye-slash"
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
                if not mat.use_backface_culling:
                    mat.use_backface_culling = True
                    self.log.info(f"Successfully enabled backface culling for '{instance.name}'.")
