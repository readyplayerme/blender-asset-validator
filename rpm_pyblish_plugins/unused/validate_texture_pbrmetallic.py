import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class TexturePBRMetallic(pyblish.api.InstancePlugin):
    """Validate values for metallic channel are either 0 or 1."""

    label = "Texture PBR Metallic"
    version = (0, 1, 1)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Texture", "Metallic"]
    match = pyblish.api.Subset

    actions = [OpenURL]
    url = "https://www.notion.so/wolf3d/Texture-metalic-4cf5584c6d094ef4bd21622790ad5414"

    def process(self, instance):
        # First, check that we can read resolution from the image data-block.
        try:
            pixels = instance[0][:, :, :1]  # Only red channel.
        except IndexError as e:
            self.log.error(f"has failed {self.label} validation. " "Could not retrieve pixel values.")
            raise ValueError(f"Validating metallic values failed for {instance.name}") from e

        tol = 13  # Tolerance of roughly 5% of 255.
        if not np.all(np.isclose(pixels, 0, atol=tol) | np.isclose(pixels, 255, atol=tol)):
            self.log.warning(
                f"has failed {self.label} validation. "
                "Metallic values should be either 0 or 1. A tolerance for a 5% deviation was considered. "
                f"Found {np.unique(pixels).size} different values instead of only 0 and 1. "
                "Often, it's the image compression setting that causes this issue. Please check."
            )
        else:
            self.log.info(f"'{instance.name}' has passed {self.label} validation.")
