"""Set the file-path to the texture maps in Blender as a relative path."""
import re

import bpy
import pyblish.api


class TextureSetRelativePaths(pyblish.api.Action):
    """Set the file-path to the texture map in Blender as a relative path."""

    label = "Relative Paths"
    icon = "pencil"
    on = "failedOrWarning"

    def process(self, context, plugin):
        from pathlib import Path
        for result in context.data['results']:
            if plugin == result["plugin"] and not result["action"]:
                instance = result['instance']
                try:
                    img = bpy.data.images[instance.name]
                except (AttributeError, KeyError) as e:
                    self.log.error(
                        f"Action {self.label} failed. Image '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                if not re.match(r"^//..[\\/]+textures[\\/]", img.filepath):
                    img.filepath = "//../textures/" + Path(instance.data['fileAbsolutePath']).name
                    self.log.info(f"Successfully set relative texture path for '{instance.name}'.")
