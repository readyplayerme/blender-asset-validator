"""Collect meshes triangle count."""
import bpy
import pyblish.api
from rpm_pyblish_plugins.shared_funcs import get_polygon_sides


class CollectTotalTriangleCount(pyblish.api.ContextPlugin):
    """Collect total triangle count of the meshes."""

    label = "Total Triangles"
    version = (0, 1, 0)
    order = pyblish.api.CollectorOrder
    hosts = ["blender"]

    def process(self, context):
        context.data["total_triangles"] = 0
        for mesh in bpy.data.meshes:
            n_poly_sides = get_polygon_sides(mesh)
            n_triangles = (n_poly_sides - 2).sum()
            context.data["total_triangles"] += n_triangles
