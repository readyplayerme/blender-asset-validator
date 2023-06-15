"""Rename the first UV channel of the mesh to 'UVMap'."""
import bpy
import pyblish.api


class MeshRenameUVMap(pyblish.api.Action):
    """Rename the first UV channel of the mesh to 'UVMap'."""

    label = "Rename UV0"
    icon = "pencil"
    on = "failedOrWarning"

    def process(self, context, plugin):
        valid_name = "UVMap"
        for result in context.data['results']:
            if plugin == result["plugin"] and not result["action"]:
                instance = result['instance']
                err = f"Action '{self.label}' failed for '{instance.name}'."
                try:
                    mesh = bpy.data.meshes[instance.name]
                except KeyError as e:
                    self.log.error(f"Action {self.label} failed. Mesh '{instance.name}' not found.")
                    raise ValueError(err) from e
                try:
                    uv0 = mesh.uv_layers[0]
                except IndexError as exc:
                    self.log.error(
                        f"Action {self.label} failed. Mesh '{instance.name}' has no UV layers.")
                    raise ValueError(err) from exc

                if uv0.name != valid_name:
                    if valid_name in mesh.uv_layers.keys():
                        mesh.uv_layers[valid_name] = f"{valid_name}.001"
                    uv0.name = valid_name
                    self.log.info(
                        f"Successfully named UV layer 0 '{valid_name}' for '{instance.name}'.")
