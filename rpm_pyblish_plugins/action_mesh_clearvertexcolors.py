"""Remove vertex colors from meshes."""
import pyblish.api
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name


class MeshClearVertexColors(pyblish.api.Action):
    """Remove vertex colors from meshes."""

    label = "Clear Vertex Colors"
    icon = "trash"
    on = "failedOrWarning"

    def process(self, context, plugin):
        for result in context.data["results"]:
            if plugin == result["plugin"] and not result["action"]:
                instance = result["instance"]
                mesh = get_mesh_by_name(instance.name)
                for col in mesh.color_attributes:
                    mesh.color_attributes.remove(col)
