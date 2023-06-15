import rpm_pyblish_plugins.constants as const
import pyblish.api
from rpm_pyblish_plugins.action_mesh_selectverticesinvalidbones import MeshSelectVerticesInvalidBones
from rpm_pyblish_plugins.action_plugin_openurl import OpenURL
from rpm_pyblish_plugins.shared_funcs import get_mesh_by_name, get_vertex_groups_name


class MeshSkinBoneNames(pyblish.api.InstancePlugin):
    """Validate that skin weights per vertex are applied only to valid bones.

    The weights should not have any other bones influences than the ones from the valid ARMATURE.
    Having weights assigned to neutral bones or other bones than the valid ones in the Armature, will create artefact.
    """

    label = "Skin Valid Bones"
    version = (0, 0, 1)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = False
    families = ["Mesh"]
    match = pyblish.api.Subset
    actions = [MeshSelectVerticesInvalidBones, OpenURL]
    # actions = [OpenURL]

    url = "https://app.gitbook.com/o/-MUPNxqiv9WwarP92bMF/s/xUzO7eCHFwBQ0Bq37zCT/validation/validation-checks/skinning-validations/check-skin-weight-valid-bones"  # noqa

    def process(self, instance):
        mesh = get_mesh_by_name(instance.name)
        vertex_names = get_vertex_groups_name(mesh)
        if invalid_bones := validate_bone_name(vertex_names):
            for bone, indices in invalid_bones.items():
                self.log.error(
                    "Skin weights have invalid bones assigned. "
                    f"Skin weights have {len(invalid_bones)} invalid bones assigned. "
                    f"Bone '{bone}' is invalid in vertices: {indices}"
                )


def validate_bone_name(array: dict) -> dict:
    """Checks if the the bone assigned to a vertex (vert groups / skinning) is valid."""
    invalid_bones: dict = {}
    for vertex_index, vertex_groups in enumerate(array.values()):
        if vertex_groups == []:
            vertex_groups = ["Vert_without_Weights"]
        for vertex_group in vertex_groups:
            if vertex_group not in const.FULLBODY_BONES:
                if vertex_group not in invalid_bones:
                    invalid_bones[vertex_group] = []
                invalid_bones[vertex_group].append(vertex_index)
    return invalid_bones
