import numpy as np
import pyblish.api


class TextureResolutionSquare(pyblish.api.InstancePlugin):
    """Textures should be square (width=height) for the texture-atlassing optimization to work properly."""

    label = f"Resolution Square"
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
        # Make sure textures are square.
        if res[0] != res[1]:
            self.log.warning(f"{report_msg}Texture width and height must be the same. "
                             "This is currently necessary for the texture-atlassing optimization to work porperly. "
                             f"Found {res[0]} x {res[1]} pixels instead.")
        else:
            self.log.info(f"'{instance.name}' has passed {self.label} validation.")
