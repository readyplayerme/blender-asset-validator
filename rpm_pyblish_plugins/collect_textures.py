"""Collect image texture maps."""
import re
from typing import Optional

import bpy
import numpy as np
import pyblish.api

import rpm_pyblish_plugins.constants as const


class CollectTextures(pyblish.api.ContextPlugin):
    """Collect texture image instances from the file."""

    label = f"Texture Instances"
    version = (0, 1, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]

    def process(self, context):
        from pathlib import Path

        for img in bpy.data.images:
            if img.name == "Render Result":
                continue
            instance = context.create_instance(name=img.name, family="Texture")  # Name in Blender.
            instance.append(img)

            instance.data['material'] = mat.name if (mat := get_material_by_image(img)) else None
            instance.data['filePath'] = img.filepath
            instance.data['fileAbsolutePath'] = img.filepath_from_user()
            instance.data['fileFormat'] = img.file_format
            # Get texture type from name, not from the channel its node is connected to.
            pattern = const.NAMING_PATTERNS[11].replace("<replace>", ".*")
            match = re.match(pattern, Path(img.filepath_from_user()).stem)

            tex_type = match[4] if match else "unknown"
            instance.data['texType'] = tex_type
            if tex_type in ["D", "C"]:
                instance.data['families'] = ["BaseColor"]
            elif tex_type == "M":
                instance.data['families'] = ["Metallic"]

            instance.data['hasData'] = img.has_data
            instance.data['isEmbedded'] = bool(img.packed_file)
            instance.data['resolution'] = (img.size[0], img.size[1])
            instance.data['colorspace'] = img.colorspace_settings.name


def get_pixels(image: bpy.types.Image) -> np.ndarray:
    """Get pixel values of a 2D image.

    :param image: Image data-block.
    :type image: bpy.types.Image
    :return: Pixel values in shape width x height x channels. Or an empty array if no pixel data was found.
    :rtype: np.ndarray
    """
    if image.has_data:
        pixels = np.array(image.pixels, dtype=np.float16).reshape((image.size[0], image.size[1], image.channels))
        # Convert to 0-255 integers, 8-bit per value, to save some memory.
        pixels = np.floor(pixels * 255 + 0.5).astype(np.uint8)
        return pixels
    else:
        return np.array([], dtype=np.uint8)


def get_material_by_image(img: bpy.types.Image) -> Optional[bpy.types.Material]:
    """Get the first material found that uses the given image.

    :param img: Image data-block to search for in materials.
    :type img: bpy.types.Image
    :return: First material that uses the image, or None.
    :rtype: Optional[bpy.types.Material]
    """
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        images = [node.image for node in mat.node_tree.nodes if node.type == "TEX_IMAGE"]
        if img in images:
            return mat
    return None
