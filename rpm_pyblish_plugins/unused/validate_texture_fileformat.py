import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL


class TextureFileFormat(pyblish.api.InstancePlugin):
    """Validate texture file format.

    'JPEG' for textures without alpha/transparency. JPEG files are smaller due to compression and, therefore,
    better suited for web-transfer.
    'PNG' is used for textures providing transparency.
    """

    label = "Texture Format"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Texture"]
    actions = [OpenURL]

    url = "https://www.notion.so/wolf3d/texture-format-5f8195f91f5648adb8a7935f0bb99b7d"

    def process(self, instance):
        error_msg = "Validating texture file-format failed"
        tex_type = instance.data["texType"]
        format = instance.data["fileFormat"]
        if format not in ["JPEG", "PNG"]:
            raise ValueError(error_msg)
        elif tex_type != "D" and instance.data["fileFormat"] != "JPEG":
            raise ValueError(error_msg)
        elif tex_type == "D" and instance.data["fileFormat"] == "PNG":
            self.log.warning(
                f"has wrong file format: {format}. "
                f"PNG is only used if transparency is needed for the material. "
                f"Please make sure that's the case. Otherwise, textures of type '{tex_type}' must be JPEG."
            )
