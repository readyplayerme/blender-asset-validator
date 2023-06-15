"""Validate collections in the blend-file."""
import re
import pyblish.api


class CollectionHierarchy(pyblish.api.InstancePlugin):
    """Validate collections are not empty, are not nested, and have a descriptive name, like 'LOD0' or 'Reference'.

    The content should be structured the same way for each asset.
    Upon opening the file it should immediately be clear to the user what purpose each piece of content is for.
    There should only be content directly related to the current asset in the file and no unnecessary extras.
    """

    label = f"Collections"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Collection"]

    def process(self, instance):
        report_msg = f"'{instance.data['label']}' has failed {self.label} validation.\n"
        name = instance.data['name']
        failed = False
        if not re.match(r"LOD\d", name):
            self.log.warning(f"Collection '{name}' does not match 'LOD0', 'LOD1', etc. Please consider removing it.")
            failed = True
        if re.match(r"^collection$|^collection\W[^a-zA-Z]+|\d{3}", name.lower()):
            self.log.warning(f"{report_msg}The collection '{name}' has a non-descriptive name. "
                             "Better names are, e.g.: 'LOD0', 'Reference'.")
            failed = True

        if children := instance.data['children']:
            self.log.error(f"{report_msg}Nested collections found in '{name}': {', '.join(children)}.")
            failed = True

        objects = instance.data['objects']
        if not objects:
            self.log.error(f"{report_msg}Collection '{name}' is empty. Please remove it.")
            failed = True
        if not failed:
            self.log.info(f"'{instance.data['label']}' has passed {self.label} validation.")
