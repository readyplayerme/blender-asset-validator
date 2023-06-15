"""Set the specular value of materials in Blender to 0.5.

This is the fixed specular value for the default PBR material in glTF.
It corresponds to an IOR of 1.5.  specular = ((1-ior)/(1+ior))^2 / 0.08
"""
import bpy
import pyblish.api


class MaterialSetSpecular(pyblish.api.Action):
    """Set the specular value of materials in Blender to 0.5."""

    label = "Set Specular to 0.5"
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
                try:
                    mat.node_tree.nodes['Principled BSDF'].inputs['Specular'].default_value = 0.5
                    self.log.info(f"Successfully set specular value to 0.5 for '{instance.name}'.")
                except AttributeError as e:
                    self.log.error(
                        f"Action {self.label} failed. Could not find 'Principled BSDF' node in " f"'{instance.name}'."
                    )
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
