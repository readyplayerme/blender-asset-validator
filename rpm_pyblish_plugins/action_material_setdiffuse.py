"""Set the 'diffuse' value of a material in Blender to white.

This is a setting separate from the base color texture through shader nodes.
It gets multiplied with the texture input.

Blender isn't consistent with the naming here. The setting in the API is called diffuse,
but the label is Base Color, even though these 2 are different approaches in PBR.
"""
import bpy
import pyblish.api


class MaterialSetDiffuseWhite(pyblish.api.Action):
    """Set the 'diffuse' value of a material in Blender to white."""

    label = "Set White BaseColor"
    icon = "pencil"
    on = "failedOrWarning"

    def process(self, context, plugin):
        for result in context.data['results']:
            if plugin == result["plugin"] and not result["action"]:
                instance = result['instance']
                try:
                    mat = bpy.data.materials[instance.name]
                except (AttributeError, KeyError) as e:
                    self.log.error(f"Action {self.label} failed. Material '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                mat.diffuse_color = [1.0, 1.0, 1.0, 1.0]
                self.log.info(f"Successfully set diffuse color to white for '{instance.name}'.")
