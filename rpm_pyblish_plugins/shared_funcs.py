"""Shared functions used in rpm_pyblish_plugins."""
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# Copyright (C) 2022 Ready Player Me
import functools
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import bmesh
import bpy
import numpy as np


def find_users(ID: str):
    """Find all objects that use the given ID."""

    def get_users(prop_collection):
        """Get all objects in the prop collection that use the ID.

        :type prop_collection: bpy.types.bpy_prop_collection
        """
        ret = tuple(o for o in prop_collection if o.user_of_id(ID))
        return ret or None

    # Filter out None returns from get_users.
    users: Iterable[Any] = filter(
        None,
        (
            get_users(attr)
            for p in dir(bpy.data)
            if isinstance(attr := getattr(bpy.data, p, None), bpy.types.bpy_prop_collection)
        ),
    )
    # Flatten the list of tuples.
    return functools.reduce(lambda x, y: x + y, users)


def deselect_objects():
    """Deselect all objects."""
    selected_objects = [obj for obj in bpy.data.objects if obj.select_get()]
    for obj in selected_objects:
        obj.select_set(False)


def select_all(mesh: bpy.types.Mesh, deselect: bool = False):
    """Select/deselect all components."""
    if mesh.is_editmode:
        select_all_bmesh(mesh, deselect=deselect)
    else:
        mesh.polygons.foreach_set("select", (not deselect,) * len(mesh.polygons))
        mesh.edges.foreach_set("select", (not deselect,) * len(mesh.edges))
        mesh.vertices.foreach_set("select", (not deselect,) * len(mesh.vertices))
        mesh.update()


def select_components(mesh: bpy.types.Mesh, indices: Union[List, np.ndarray], component: str = "VERT"):
    """Select vertices with indices, deselect others.

    :param component: one in {'VERT', 'EDGE', 'FACE'}
    :type component: str
    """
    select_all(mesh, deselect=True)
    if mesh.is_editmode:
        # Selection.
        bm = bmesh.from_edit_mesh(mesh)
        if component == "VERT":
            comps = bm.verts
        elif component == "EDGE":
            comps = bm.edges
        else:
            comps = bm.faces
        comps.ensure_lookup_table()
        for i, c in enumerate(comps):
            c.select = i in indices
            bm.select_mode |= {component}
            bm.select_flush_mode()
            bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)
        del bm  # Calling bm.free(), like recommended, messes things up. Instead delete the reference explicitly.
    else:
        if component == "VERT":
            comps = mesh.vertices
        elif component == "EDGE":
            comps = mesh.edges
        else:
            comps = mesh.polygons
        idx = np.zeros(len(comps), dtype=bool)
        idx[indices] = True
        comps.foreach_set("select", idx)
        mesh.update()


def deselect_all(mesh: bpy.types.Mesh):
    """Deselect all components.

    Deprecated in favor of select_all(mesh, deselect=True).
    """
    select_all(mesh, deselect=True)


def get_bmesh(mesh: bpy.types.Mesh) -> bmesh.types.BMesh:
    """Return a bmesh from OBJECT or EDIT mode.

    :param mesh: Mesh of interest.
    :type mesh: bpy.types.Mesh
    :return: A bmesh from the mesh.
    :rtype: bmesh.types.BMesh
    """
    if mesh.is_editmode:
        bm = bmesh.from_edit_mesh(mesh)
    else:
        bm = bmesh.new()
        bm.from_mesh(mesh)
    return bm


def select_all_bmesh(mesh: bpy.types.Mesh, deselect=False):
    """Select all vertices using bmesh."""
    # Get mesh data depending on current mode.
    bm = get_bmesh(mesh)

    # Selection.
    for v in bm.verts:
        v.select = not deselect
    for e in bm.edges:
        e.select = not deselect
    for f in bm.faces:
        f.select = not deselect
    bm.select_flush(False)

    # Write back to object data.
    if bm.is_wrapped:
        bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)
    else:
        bm.to_mesh(mesh)
        mesh.update()
    del bm


def deselect_all_bmesh(mesh: bpy.types.Mesh):
    """Deselect all vertices using bmesh.

    Deprecated in favor of select_all_bmesh(mesh, deselect=True).
    """
    select_all_bmesh(mesh, deselect=True)


def get_transforms(obj: bpy.types.Object) -> Dict[str, Tuple[float, float, float]]:
    """Return location, rotation (Euler), and scale of the object, as well as their delta transforms.

    :param obj: Object from which to retrieve transforms.
    :type obj: bpy.types.Object
    :return: Dictionary with transforms.
    :rtype: Dict[str, List[float]]
    """
    return {
        "location": obj.location,
        "locationDeltas": obj.delta_location,
        "rotation": obj.rotation_euler,
        "rotationDeltas": obj.delta_rotation_euler,
        "scale": obj.scale,
        "scaleDeltas": obj.delta_scale,
    }


def get_collections(obj: bpy.types.Object) -> List[str]:
    """Return names of collections the object is linked to.

    :param obj: Object of interest.
    :type obj: bpy.types.Object
    :return: A list of names of all collections containing this object.
    :rtype: List[str]
    """
    return [coll.name for coll in obj.users_collection]


def recursive_layer_collection(layer_collection: bpy.types.LayerCollection, collection_name: str):
    """Recursivly traverse a LayerCollection for a particular collection name.

    :param layer_collection: [description]
    :type layer_collection: bpy.types.LayerCollection
    :param collection_name: [description]
    :type collection_name: str
    :return: [description]
    :rtype: [type]
    """
    found = None
    if layer_collection.name == collection_name:
        return layer_collection
    for layer in layer_collection.children:
        if found := recursive_layer_collection(layer, collection_name):
            return found


def set_active_collection(collection: str):
    """Set active collection tothe collection with the given name.

    :param collection: Name of collectiontoset as active.
    :type collection: str
    """
    root_layer_collection = bpy.context.view_layer.layer_collection
    layer_collection = recursive_layer_collection(root_layer_collection, collection)
    try:
        bpy.context.view_layer.active_layer_collection = layer_collection
    except TypeError:
        raise


def get_uvmap_names(mesh: bpy.types.Mesh) -> List[str]:
    """Return names of all UV maps on the mesh.

    :param mesh: Mesh of interest.
    :type mesh: bpy.types.Mesh
    :return: List of UV map names.
    :rtype: List[str]
    """
    return mesh.uv_layers.keys()


def get_uvs(mesh: bpy.types.Mesh, uv_layer_index: int = 0) -> np.ndarray:
    """Get UV data for the mesh.

    :param obj: Object from which to get UV data.
    :type obj: bpy.types.Object
    :param uv_layer_index: Index of UV layer for which to retrieve data.
    :type uv_layer_index: int
    :return: UV data. Coordinates in columns.
    :rtype: np.ndarray
    """
    if mesh.is_editmode:
        bm = bmesh.from_edit_mesh(mesh)
        try:
            uv_layer = bm.loops.layers.uv[uv_layer_index]
        except IndexError:
            # Return active UV layer or create a new one.
            uv_layer = bm.loops.layers.uv.verify()
        uvs = np.empty((len(mesh.loops), 2), dtype=np.float32)
        for face in bm.faces:
            for loop in face.loops:
                loop_uv = loop[uv_layer]
                uvs[loop.index] = loop_uv.uv
    else:
        uv_layer = mesh.uv_layers[uv_layer_index]
        uvs = np.empty((2 * len(mesh.loops), 1), dtype=np.float32)
        uv_layer.data.foreach_get("uv", uvs)
        uvs = uvs.reshape((-1, 2))
    return uvs


def calc_2D_poly_area(x: np.ndarray, y: np.ndarray) -> float:
    """Calculate the area of a polygon from the coordinates of its points."""
    # Coordinate shift. Avoids precision errors with big values. Not an issue with 0-1 UV range.
    x_ = x - x.mean()
    y_ = y - y.mean()
    # Correction term to avoid roll.
    correction = x_[-1] * y_[0] - y_[-1] * x_[0]
    area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
    return 0.5 * np.abs(area + correction)


def get_uv_area(mesh: bpy.types.Mesh) -> np.ndarray:
    """Get the area of each UV face.

    :param mesh: The mesh data to calculate UV areas for.
    :type mesh: bpy.types.Mesh
    :return: UV area for all faces.
    :rtype: np.ndarray
    """
    uvs = get_uvs(mesh)
    # Map UV coordinates to face loops.
    # Foreach_get fails for loop_indices attribute. Resort to list comprehension.
    loop_indices = [polygon.loop_indices for polygon in mesh.polygons]
    area = np.empty(len(loop_indices))
    for i, polygon_loop in enumerate(loop_indices):
        area[i] = calc_2D_poly_area(uvs[polygon_loop, 0], uvs[polygon_loop, 1])
    return area


def get_polygon_sides(mesh: bpy.types.Mesh) -> np.ndarray:
    """Return the number of edges for each polygon in the mesh.

    :param mesh: The mesh of which to get the number of sides per polygon.
    :type mesh: bpy.types.Mesh
    :return: An array of number of sides
    :rtype: np.ndarray
    """
    n_edges = np.empty(len(mesh.polygons))
    mesh.polygons.foreach_get("loop_total", n_edges)
    return n_edges


def get_polygon_area(mesh: bpy.types.Mesh) -> np.ndarray:
    """Get the area measurement of each polygon.

    :param mesh: The mesh data to calculate polygon areas for.
    :type mesh: bpy.types.Mesh
    :return: Area for all polygons.
    :rtype: np.ndarray
    """
    area = np.empty(len(mesh.polygons))
    mesh.polygons.foreach_get("area", area)
    return area


def get_edge_lengths(mesh: bpy.types.Mesh) -> np.ndarray:
    """Return lengths for each edge."""
    bm = get_bmesh(mesh)
    return np.array([e.calc_length() for e in bm.edges])


def get_nonmanifold_verts(mesh: bpy.types.Mesh) -> np.ndarray:
    """Return indices of non-manifold vertices found in the mesh.

    :param mesh: The mesh object in which to search for non-manifold geometry.
    :type mesh: bpy.types.Mesh
    :return: Indices of non-manifold vertices found.
    :rtype: np.ndarray
    """
    bm = get_bmesh(mesh)
    bm.verts.ensure_lookup_table()
    is_nonmanifold_vert = np.array([(not vert.is_manifold) or vert.is_wire for vert in bm.verts])
    return np.argwhere(is_nonmanifold_vert).flatten()


def get_loose_edges(mesh: bpy.types.Mesh) -> np.ndarray:
    """Return indices of loose edges.

    :param mesh: The mesh object in which to search for loose edges.
    :type mesh: bpy.types.Mesh
    :return: Indices of loose edges found.
    :rtype: np.ndarray
    """
    is_loose_edge = np.empty(len(mesh.edges))
    mesh.edges.foreach_get("is_loose", is_loose_edge)
    return np.argwhere(is_loose_edge).flatten()


def get_mesh_by_name(name: str) -> bpy.types.Mesh:
    """Get mesh by name.

    :param name: Name of mesh to get.
    :type name: str
    :return: Mesh with given name.
    :rtype: bpy.types.Mesh
    """
    try:
        return bpy.data.meshes[name]
    except KeyError as e:
        raise ValueError(f"Mesh '{name}' not found.") from e


def object_from_mesh(mesh: bpy.types.Mesh) -> Optional[bpy.types.Object]:
    """Return the first object found that uses the mesh data-block.

    :param mesh: Mesh for which to search its parent object.
    :type mesh: bpy.types.Mesh
    :return: Object, if found.
    :rtype: Optional[bpy.types.Object]
    """
    return next((obj for obj in bpy.data.objects if obj.data is mesh), None)


def get_skin_weights(mesh: bpy.types.Mesh) -> np.ndarray:
    """Get skin weights for each vertex and vertex group."""
    parent = object_from_mesh(mesh)
    assert parent is not None, f"Mesh '{mesh.name}' has no parent object. Can't access vertex groups."
    n_groups = len(parent.vertex_groups)
    weights = np.zeros((len(mesh.vertices), n_groups), dtype=np.float32)
    for vert in mesh.vertices:
        group_idx = np.empty(len(vert.groups), dtype=np.uint8)
        w = np.empty(len(vert.groups), dtype=np.float32)
        vert.groups.foreach_get("group", group_idx)
        vert.groups.foreach_get("weight", w)
        weights[vert.index, group_idx] = w
    return weights


def get_vertex_groups_name(mesh: bpy.types.Mesh) -> dict:
    """Get vertex groups (bones that influences the vertex) for each vertex"""
    parent = object_from_mesh(mesh)
    assert parent is not None, f"Mesh '{mesh.name}' has no parent object. Can't access vertex groups."

    # Create vertex group lookup dictionary for names.
    vgroup_names = {vgroup.index: vgroup.name for vgroup in parent.vertex_groups}

    # Create dictionary of vertex group assignments per vertex.
    vgroups = {v.index: [vgroup_names[g.group] for g in v.groups] for v in parent.data.vertices}  # noqa

    # Returning without assigning to the var vgroups fails.
    return vgroups


def has_vertex_colors(mesh: bpy.types.Mesh) -> bool:
    """Check if the mesh has vertex colors.

    :param mesh: Mesh to check.
    :type mesh: bpy.types.Mesh
    :return: True if mesh has vertex colors.
    :rtype: bool
    """
    return bool(mesh.color_attributes)
