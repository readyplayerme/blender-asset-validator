"""Export to GLB format."""
import rpm_pyblish_plugins.constants as const
import pyblish.api
from pyblend import file_io
from ready_player_me.configs import gltf as presets


class ExportGLB(pyblish.api.ContextPlugin):
    """Export GLB file to the asset folder."""

    label = "Export GLB"
    version = (0, 2, 0)
    order = pyblish.api.ExtractorOrder
    hosts = ["blender"]
    optional = True

    def process(self, context):
        # Set paths.
        current_file = context.data["currentFile"]
        export_path = file_io.paths.get_abs_path(const.EXPORT_PATH)  # TODO support GLB export path by pyblish_config.
        dest_path = export_path / file_io.paths.filename_as(current_file, "glb")
        # Get export options.
        settings = presets.get_outfit_export_settings()
        success, msg = file_io.gltf.export_gltf(dest_path, **settings)
        # Report.
        if not success:
            raise IOError(f"{self.label} failed. {msg}")
        # Save reference to exported file for integration.
        context.data["GLBFile"] = dest_path
