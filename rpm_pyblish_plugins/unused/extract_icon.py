"""Render a preview image of the asset to file."""
import bpy
import icon_render
import rpm_pyblish_plugins.constants as const
import pyblish.api
from pyblend import file_io, scenemanager


class ExtractIcon(pyblish.api.ContextPlugin):
    """Render a preview image of the asset to file."""

    label = "Render Icon"
    version = (0, 1, 1)
    order = pyblish.api.ExtractorOrder
    hosts = ["blender"]
    optional = True

    def process(self, context):
        from pathlib import Path

        current_file = Path(context.data["currentFile"])
        # Link proper render scene for this asset type.
        # Hack as long as we don't have a single body mesh.
        if (asset_type := context.data["assetType"]) == "outfit":
            gender = current_file.stem.split("-")[-1]
            asset_type = f"{asset_type}-{gender}"
        scene = get_icon_scene_by_type(asset_type)
        link_render_scene(scene)
        prepare_scene(scene)
        export_dir = file_io.paths.get_abs_path(const.EXPORT_PATH)
        icon_path = export_dir / current_file.with_suffix(".png").name
        file_io.image.render_image(icon_path)
        # Unlink render scene.
        unlink_render_scene()
        # Save reference to exported file for integration.
        context.data["IconFile"] = icon_path


def get_icon_scene_by_type(asset_type: str) -> str:
    """Get the corresponding scene name for a particular asset type."""
    if asset_type == "beard":
        return "facewear"
    if asset_type == "facewear":
        return "facewear"
    elif asset_type == "glasses":
        return "glasses"
    elif asset_type == "hair":
        return "hair"
    elif asset_type == "headwear":
        return "headwear"
    elif asset_type == "outfit-f":
        return "outfit-f"
    else:
        return "outfit-m"


def link_render_scene(scene_name: str):
    """Load render scene from file into current project."""
    raise NotImplementedError("Icon rendering will be reworked.")


def prepare_scene(bg_scene: str):
    """Prepare scene for rendering.

    Blender does not yet support overriding linked scenes, so we can't link objects to the render scene.
    Therefore, we bring the render scene to the active scene as a background.
    """
    # Set render scene as background scene and use its camera.
    bpy.context.scene.background_set = bpy.data.scenes[bg_scene]
    bpy.context.scene.camera = bpy.data.objects[f"{bg_scene}-cam"]
    bpy.context.scene.world = bpy.data.worlds[f"{bg_scene}-World"]
    # Set render options.
    if addon_path := file_io.paths.get_addon_path(icon_render.bl_info["name"]):
        preset_path = str(addon_path / "icon-settings.py")
        bpy.ops.script.execute_preset(filepath=preset_path, menu_idname="RENDER_PT_format_presets")


def unlink_render_scene():
    """Remove linked render scene from current project."""
    scenemanager.unlink_scenes(["icon-render.blend", "head.blend"])
    bpy.context.scene.world = bpy.data.worlds[0]
