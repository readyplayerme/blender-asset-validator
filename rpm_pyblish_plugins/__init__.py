from pathlib import Path
import pyblish.api


plugin_path = Path(__file__).parent


def register():
    pyblish.api.register_plugin_path(plugin_path)


def deregister():
    pyblish.api.deregister_plugin_path(plugin_path)
    