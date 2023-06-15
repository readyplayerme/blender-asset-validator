"""Reload the texture maps in Blender from their file-paths."""
import bpy
import pyblish.api

import rpm_pyblish_plugins.constants as const


class TextureReload(pyblish.api.Action):
    """Reload the texture maps in Blender from their file-paths."""

    label = "Reload Textures"
    icon = "refresh"

    def process(self, context, plugin):
        for instance in context:
            if instance.data['family'] == f"{const.PREFIX}.Texture":
                try:
                    img = bpy.data.images[instance.name]
                except (AttributeError, KeyError) as e:
                    self.log.error(f"Action {self.label} failed. Image '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                img.reload()
                if len(img.pixels):
                    self.log.info(f"Successfully reloaded texture '{instance.name}'.")
                else:
                    self.log.error(f"Action {self.label} failed. Could not reload image '{instance.name}'. "
                                   f"Is the file-path '{img.filepath}' correct?")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.")
