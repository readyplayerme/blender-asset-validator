import rpm_pyblish_plugins.constants as const
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.action_texture_setcolorspace import TextureSetColorSpace


class TextureColorSpace(pyblish.api.InstancePlugin):
    """Validate texture colorspace.

    sRGB colospace for color and emissive textures.
    'Non-color' colorspace for roughness, normal, metallic, AO, world-space normal, and ID textures.
    """

    label = "Texture Colorspace"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Texture"]
    actions = [TextureSetColorSpace, OpenURL]

    # custom non pyblish data
    # TODO #77 should url member be moved to plugin.data['url']? investigate
    url = "https://www.notion.so/wolf3d/Color-space-3b57301aadc74da99ce71ba0031fc6bf"
    fix = TextureSetColorSpace

    def process(self, instance):
        tex_type = instance.data["texType"]
        valid_colorspace = const.COLORSPACE.get(tex_type, "Non-Color")
        instance_colorspace = instance.data["colorspace"]
        if instance_colorspace != valid_colorspace:
            self.log.error("Validating colorspace failed")
