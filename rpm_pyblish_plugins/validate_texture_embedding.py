import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.action_texture_setembedding import TextureSetEmbedding


class TextureEmbedding(pyblish.api.InstancePlugin):
    """Validate texture embedding setting. Blend-files should not embed textures.

    By embedding images inside the blend-file, it's not guaranteed that the texture maps get updated once the external
    file is updated. This can lead to outdated texture maps in the blend-file.
    Embedding also increases storage needs by saving redundant information.
    You can disable auto-embedding in Blender by deactivating:
    File -> External Data -> Automatically Pack Into .blend
    """

    label = "Texture Embedding"
    version = (0, 2, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Texture"]
    actions = [TextureSetEmbedding, OpenURL]

    fix = TextureSetEmbedding
    url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks/texture-map-validations/check-texture-embedding"  # noqa

    def process(self, instance):
        if instance.data["isEmbedded"]:
            self.log.warning(
                f"'{instance.name}' has failed {self.label} validation. "
                f"The texture data is embedded in the blend-file. "
                f"You can fix this issue by using the action '{TextureSetEmbedding.label}' from the "
                "context menu of this validation."
            )
