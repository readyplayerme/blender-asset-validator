"""Export FBX file."""
import rpm_pyblish_plugins.constants as const
import pyblish.api
from pyblend import file_io
from ready_player_me.configs import fbx as presets


class ExportFBX(pyblish.api.ContextPlugin):
    """Export FBX file to the asset folder."""

    label = "Export FBX"
    version = (0, 2, 0)
    order = pyblish.api.ExtractorOrder
    hosts = ["blender"]
    optional = True

    def process(self, context):
        # Set paths.
        current_file = context.data["currentFile"]
        export_path = file_io.paths.get_abs_path(const.EXPORT_PATH)  # TODO support FBX export path by pyblish_config.
        dest_path = export_path / file_io.paths.filename_as(current_file, "fbx")
        # Get export options.
        settings = presets.get_outfit_export_settings()
        success, msg = file_io.fbx.export_fbx(dest_path, **settings)
        # Report.
        if not success:
            raise IOError(f"{self.label} failed. {msg}")
        # Save reference to exported file for integration.
        context.data["FBXFile"] = dest_path
