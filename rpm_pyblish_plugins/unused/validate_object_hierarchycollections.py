"""Check the object's placement in collections."""
import re

import pyblish.api


class ObjectHierarchyCollections(pyblish.api.InstancePlugin):
    """Validate that objects are in the correct collections.

    Objects in the scene must be organized in collections.
    In some cases it may be beneficial to keep references in the file.
    These should be limited to the absolute minimum that is necessary for the current asset.
    To easily identify references they must be placed in a collection with the name 'Reference'.
    References should be manually excluded from validation by unchecking their instance.
    """

    label = "Object's Collections"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Object", "Rig"]

    def process(self, instance):
        collections = instance.data["collections"]
        is_in_lod_collection = any(bool(re.match(r"LOD\d", coll)) for coll in collections)
        if not (is_in_lod_collection or "Reference" in collections):
            self.log.error(
                f"'{instance.data['label']}' has failed {self.label} validation. "
                "Must be in one of collections: 'LOD0', 'LOD1', 'LOD2', or 'LOD3', 'Reference'. "
                f"Found in collections {', '.join(collections)} instead."
            )
            raise ValueError(f"Validating object's collections failed for {instance.data['label']}.")
        self.log.info(f"'{instance.data['label']}' has passed {self.label} validation.")
