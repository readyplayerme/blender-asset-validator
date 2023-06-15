"""Set texture wrapping modes to Clip/Clamp to edge for texture maps."""
import bpy
import pyblish.api


class MaterialSetSamplerWrapping(pyblish.api.Action):
    """Set texture wrapping modes to Clip/Clamp to edge for texture maps."""

    label = "Set CLIP wrapping"
    icon = "cut"
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
                img_nodes = [node for node in mat.node_tree.nodes if node.type == 'TEX_IMAGE']
                for node in img_nodes:
                    node.extension = 'CLIP'
                self.log.info(f"Successfully set texture wrapping modes to 'CLIP' for '{instance.name}'.")
