"""Set color spaces of textures correctly."""
import bpy
import rpm_pyblish_plugins.constants as const
import pyblish.api


class TextureSetColorSpace(pyblish.api.Action):
    """Set colorspaces of textures correctly."""

    label = "Fix Colorspace"
    icon = "wrench"
    on = "failedOrWarning"

    def process(self, context, plugin):
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                instance = result["instance"]
                try:
                    img = bpy.data.images[instance.name]
                except (AttributeError, KeyError) as e:
                    self.log.error(f"Action {self.label} failed. Image '{instance.name}' not found.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.") from e
                tex_type = instance.data["texType"]
                if tex_type != "unknown":
                    img.colorspace_settings.name = colorspace = const.COLORSPACE.get(tex_type, "Non-Color")
                    self.log.info(f"Successfully set colorspace to '{colorspace}' for '{instance.name}'.")
                else:
                    self.log.error(f"Action {self.label} failed. Can't determine colorspace for '{instance.name}'.")
                    raise ValueError(f"Action '{self.label}' failed for '{instance.name}'.")
