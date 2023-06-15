import re

import rpm_pyblish_plugins.constants as const
import pyblish.api
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.action_texture_reload import TextureReload
from rpm_pyblish_plugins.action_texture_setembedding import TextureSetEmbedding
from rpm_pyblish_plugins.action_texture_setrelativepath import TextureSetRelativePaths
from rpm_pyblish_plugins.validate_file_path import pattern_map  # noqa


class TextureFilePath(pyblish.api.InstancePlugin):
    """Validate the texture file-path. It should be relative to the current file and follow naming conventions."""

    label = "Texture Path"
    __doc__ += "\nTexture names must end with one of these suffixes:\n-" + ",\n-".join(const.COLORSPACE.keys())
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    families = ["Texture"]
    actions = [TextureSetRelativePaths, TextureReload, TextureSetEmbedding, OpenURL]

    url = "https://www.notion.so/wolf3d/texture-path-d5ccb79612c2418985ea6d1c936d1cf1"

    def process(self, instance):
        from pathlib import Path

        img = instance[0]

        report_msg = "Validating file-path of image data-block failed"
        asset_type = instance.context.data["assetType"]
        # The default path // refers to the folder of the currently open blend-file.
        if not re.match(r"^//..[\\/]+textures[\\/]", img.filepath):
            self.log.warning(report_msg)

        fileAbsolutePath = img.filepath_from_user()
        abs_path = Path(fileAbsolutePath)

        if not abs_path.is_file():
            self.log.warning(
                f"{report_msg}Texture file not found at path '{str(abs_path)}'. "
                "Even when textures are embeded in the blend-file, the path to the source must be correct "
                "in order to quickly reload the file in case updates were made to it."
            )
        # Check naming conventions.
        asset_name = Path(instance.context.data["currentFile"]).stem
        try:
            patterns = [
                const.NAMING_PATTERNS[i].replace("<replace>", asset_name) for i in pattern_map[f"{asset_type}.tex"]
            ]

        except KeyError:
            patterns = []
        for pattern in patterns:
            if match := re.match(pattern, abs_path.stem):
                groups = match.groups()
                break
        else:
            groups = ()
        if not groups:
            self.log.warning(
                f"{report_msg}File-name '{Path(img.filepath).name}' does not follow any known "
                f"texture naming convention for asset type '{asset_type}'."
            )
