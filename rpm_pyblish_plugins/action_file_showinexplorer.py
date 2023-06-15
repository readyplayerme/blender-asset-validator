"""Show the currently opened blend-file in the Windows Explorer."""

import os
from pathlib import Path

import pyblish.api


class FileShowInExplorer(pyblish.api.Action):
    """Show the currently opened blend-file in the Windows Explorer."""

    label = "Open in Explorer"
    icon = "folder-open"  # Icon from Awesome Icon

    def process(self, context, plugin):
        import platform
        import subprocess
        import webbrowser

        current_file = Path(context.data['currentFile'])
        if current_file.is_file():
            if platform.system() == "Windows":
                FILEBROWSER_PATH = Path(os.getenv('WINDIR')) / 'explorer.exe'
                subprocess.run([FILEBROWSER_PATH, '/select,', current_file])
            else:
                webbrowser.open(current_file.parent)
        else:
            self.log.error(f"File '{current_file}' not found!")
