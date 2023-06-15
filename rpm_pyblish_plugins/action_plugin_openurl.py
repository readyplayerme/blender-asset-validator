"""Open a plugin-specific URL in a web browser."""
import webbrowser
import pyblish.api


class OpenURL(pyblish.api.Action):
    """Open a plugin-specific URL in a web browser."""

    label = "documentation"
    # icon = "trash"
    # on = "failedOrWarning"

    def process(self, context, plugin):
        url = plugin.url
        webbrowser.open(url, new=1, autoraise=True)
