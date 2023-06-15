import numpy as np
import pyblish.api


class TextureResolutionPowerOfTwo(pyblish.api.InstancePlugin):
    """Validate texture resolution is a power of 2.."""

    label = f"Resolution Power of Two"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Texture"]

    def process(self, instance):
        report_msg = f"has failed {self.label} validation.\n"
        error_msg = f"Validating texture resolution failed for {instance.name}"
        res = instance.data['resolution']
        # Make sure resolution was retrieved so we don't get division by zero error.
        if not np.all(res):
            self.log.error(f"{report_msg}Unable to retrieve resolution from image data-block. "
                           "Make sure the texture file-path is correct.")
            raise ValueError(error_msg)
        # Make sure textures are power of 2 (exponent is a whole number).
        elif not np.all(np.mod(np.log2(res), 1) == 0):
            self.log.error(f"{report_msg}The texture resolution must be a power of 2 (2^x)."
                           "Examples are: 512, 1024, 2048. "
                           f"Found {res[0]} x {res[1]} pixels instead.")
        else:
            self.log.info(f"'{instance.name}' has passed {self.label} validation.")
