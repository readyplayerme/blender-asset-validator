"""Set embedding setting of textures for the blend-file."""
import bpy
import pyblish.api


class TextureSetEmbedding(pyblish.api.Action):
    """Unpack texture maps, use from given file path."""

    label = "Remove Texture Embedding"
    icon = "box-open"
    on = "failedOrWarning"

    def process(self, context, plugin):
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                instance = result["instance"]
                try:
                    img = bpy.data.images[instance.name]
                except (AttributeError, KeyError) as e:
                    raise ValueError(
                        f"Action '{self.label}' failed for '{instance.name}'."
                        "Image not found."
                        "If you changed the image node name, try again after resetting the validation."
                    ) from e
                try:
                    img.unpack(method="REMOVE")
                    img.reload()
                except RuntimeError:
                    self.log.info(f"Action '{self.label}': '{instance.name}' already unpacked.")
