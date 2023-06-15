import numpy as np
import pyblish.api
import rpm_pyblish_plugins.constants as const


class TextureResolutionBudget(pyblish.api.InstancePlugin):
    """Validate texture resolution budget.

    Each asset type has a texture resolution budget associated for its materials.
    """

    label = f"Texture Resolution Budget"
    __doc__ += "\nBudgets are as follows:\n" + \
        ',\n'.join(f'{k}: {v}' for k, v in const.IMAGE_BUDGETS.items())
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
        # Check texture budget.
        material = instance.data['material']
        budget = const.IMAGE_BUDGETS.get(material, 512)
        if res[0] > budget or res[1] > budget:
            self.log.error(f"{report_msg}Texture resolution for material {material} must not exceed "
                           f"{budget} x {budget} pixels. Found {res[0]} x {res[1]} pixels instead.")
            raise ValueError(error_msg)
        self.log.info(f"'{instance.name}' has passed {self.label} validation.")
