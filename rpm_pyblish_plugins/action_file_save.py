"""Save current Blender content to file."""
import bpy
import pyblish.api


class FileSave(pyblish.api.Action):
    """Save the currently open blend file to disk."""

    label = "Save File"
    icon = "floppy-o"

    def process(self, context, plugin):
        if not bpy.data.is_saved or bpy.data.is_dirty:
            try:
                bpy.ops.wm.save_mainfile()
            except (IOError, RuntimeError) as e:
                self.log.error(f"Action {self.label} had errors.\n{str(e)}")
                raise ValueError(f"Action '{self.label}' failed.") from e
        self.log.info(f"Saved to file {bpy.data.filepath}")
