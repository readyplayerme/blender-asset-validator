import numpy as np
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class TexturePBRAlbedo(pyblish.api.InstancePlugin):
    """Validate albedo range is between 50-243 sRGB."""

    label = "Texture PBR Albedo"
    version = (0, 1, 1)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Texture", "BaseColor"]
    match = pyblish.api.Subset

    actions = [OpenURL]
    url = "https://www.notion.so/wolf3d/Texture-Albedo-f50c8c4e45c74be9b8f5f73ee17015a9"

    def process(self, instance):
        try:
            pixels = instance[0][:, :, :3]  # Exclude Alpha channel.
        except IndexError as e:
            self.log.error(f"has failed {self.label} validation. " "Could not retrieve pixel values.")
            raise ValueError(f"Validating albedo values failed for {instance.name}") from e

        tolerance_min = 50
        threshold_min = 30
        tolerance_max = 243
        range_hint = (
            "For metals, the luminance range is 186–255 sRGB. "
            "Please use a PBR validator before exporting the texture."
        )
        is_valid = True
        if np.any(pixels < threshold_min):
            self.log.error(
                f"has failed {self.label} validation. "
                f"Albedo values for non-metal PBR materials must not be below {threshold_min} sRGB. "
                f"Found a lowest value of {pixels.min()} instead. " + range_hint
            )
            is_valid = False
        elif np.any(pixels < tolerance_min):
            self.log.warning(
                f"shows issues with {self.label} validation. "
                f"Albedo values for non-metal PBR materials should not be below {tolerance_min} sRGB. "
                f"Found a lowest value of {pixels.min()} instead. " + range_hint
            )
            is_valid = False
        if np.any(pixels > tolerance_max):
            self.log.warning(
                f"shows issues with {self.label} validation. "
                f"Albedo values for non-metal PBR materials should not exceed {tolerance_max} sRGB. "
                f"Found a highest value of {pixels.max()} instead. " + range_hint
            )
            is_valid = False
        if is_valid:
            self.log.info(f"'{instance.name}' has passed {self.label} validation.")
