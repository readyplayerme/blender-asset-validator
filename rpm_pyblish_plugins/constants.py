"""Configure known asset types, texture maps etc."""

PREFIX = "Wolf3D"
KNOWN_ASSET_TYPES = [
    "beard",
    "bottom",
    "eyebrow",
    "facewear",
    "footwear",
    "glasses",
    "hair",
    "headwear",
    "integral",
    "outfit",
    "shirt",
    "top",
]
SKINNED_MESHES = [
    "Wolf3D_Body",
    "Wolf3D_Body_Custom",
    "Wolf3D_Head_Custom",
    "Wolf3D_Outfit_Top",
    "Wolf3D_Outfit_Bottom",
    "Wolf3D_Outfit_Footwear",
    "Wolf3D_Teeth",
    "Wolf3D_EyeLeft",
    "Wolf3D_EyeRight",
    "Wolf3D_Hair",
    "Wolf3D_Glasses",
    "Wolf3D_Headwear",
    "Wolf3D_Facewear",
    "Wolf3D_Beard",
]


NAMES = [
    "Armature",
    f"{PREFIX}_Body",
    f"{PREFIX}_Body_Custom",
    f"{PREFIX}_Head_Custom",
    f"{PREFIX}_Outfit_Top",
    f"{PREFIX}_Outfit_Bottom",
    f"{PREFIX}_Outfit_Footwear",
    f"{PREFIX}_Teeth",
    f"{PREFIX}_EyeLeft",
    f"{PREFIX}_EyeRight",
    # Other categories.
    f"{PREFIX}_Hair",
    f"{PREFIX}_Glasses",
    f"{PREFIX}_Headwear",
    f"{PREFIX}_Facewear",
    f"{PREFIX}_Beard",
    # Additional material names.
    f"{PREFIX}_Eye",
    f"{PREFIX}_Skin",
]
KNOWN_OUTFIT_PARTS = ["body", "top", "bottom", "footwear"]
RIGGED_ASSETS = KNOWN_OUTFIT_PARTS + ["outfit", "beard"]
TRIANGLE_BUDGETS = {
    f"{PREFIX}_Body": 14000,
    f"{PREFIX}_outfit": 8000,  # Max. combined total of body, top, bottom, footwear.
    f"{PREFIX}_Outfit_Top": 6000,
    f"{PREFIX}_Outfit_Bottom": 5000,
    f"{PREFIX}_Outfit_Footwear": 2000,
    f"{PREFIX}_Teeth": 1000,
    f"{PREFIX}_Beard": 1000,
    f"{PREFIX}_Eyebrow": 60,
    f"{PREFIX}_Eye": 60,
    f"{PREFIX}_Facewear": 900,
    f"{PREFIX}_Glasses": 1000,
    f"{PREFIX}_Hair": 3000,
    f"{PREFIX}_Head": 4574,
    f"{PREFIX}_Head_Custom": 6000,
    f"{PREFIX}_Headwear": 2500,
    f"{PREFIX}_Shirt": 1000,
}
COLORSPACE = {
    "D": "sRGB",  # TODO #74 deprecate diffuse abbreviation, since we use metalness workflow, not diff + spec.
    "C": "sRGB",
    "R": "Non-Color",
    "N": "Non-Color",
    "M": "Non-Color",
    "E": "sRGB",
    "AO": "Non-Color",
    "WSN": "Non-Color",
    "ID": "Non-Color",
    "mask": "sRGB",
}
IMAGE_BUDGETS = {
    f"{PREFIX}_Body": 2048,
    f"{PREFIX}_Outfit_Top": 2048,
    f"{PREFIX}_Outfit_Bottom": 2048,
    f"{PREFIX}_Outfit_Footwear": 1024,
    f"{PREFIX}_Beard": 1024,
    f"{PREFIX}_Eye": 512,
    f"{PREFIX}_Eyebrow": 1024,
    f"{PREFIX}_Facewear": 1024,
    f"{PREFIX}_Glasses": 512,
    f"{PREFIX}_Hair": 1024,
    f"{PREFIX}_Head": 2048,
    f"{PREFIX}_Headwear": 1024,
    f"{PREFIX}_Shirt": 1024,
}
TEXEL_DENSITY = 20.48  # 2k texture on 1 square meter.
TEXEL_DENSITY_TOLERANCE = 17.1875  # Percent, +- 3.52. Density max. 24, min. ~17
FULLBODY_BONES = [
    "Hips",
    "Spine",
    "Spine1",
    "Spine2",
    "Neck",
    "Head",
    "HeadTop_End",
    "LeftShoulder",
    "LeftArm",
    "LeftForeArm",
    "LeftHand",
    "LeftHandThumb1",
    "LeftHandThumb2",
    "LeftHandThumb3",
    "LeftHandThumb4",
    "LeftHandIndex1",
    "LeftHandIndex2",
    "LeftHandIndex3",
    "LeftHandIndex4",
    "LeftHandMiddle1",
    "LeftHandMiddle2",
    "LeftHandMiddle3",
    "LeftHandMiddle4",
    "LeftHandRing1",
    "LeftHandRing2",
    "LeftHandRing3",
    "LeftHandRing4",
    "LeftHandPinky1",
    "LeftHandPinky2",
    "LeftHandPinky3",
    "LeftHandPinky4",
    "RightShoulder",
    "RightArm",
    "RightForeArm",
    "RightHand",
    "RightHandThumb1",
    "RightHandThumb2",
    "RightHandThumb3",
    "RightHandThumb4",
    "RightHandIndex1",
    "RightHandIndex2",
    "RightHandIndex3",
    "RightHandIndex4",
    "RightHandMiddle1",
    "RightHandMiddle2",
    "RightHandMiddle3",
    "RightHandMiddle4",
    "RightHandRing1",
    "RightHandRing2",
    "RightHandRing3",
    "RightHandRing4",
    "RightHandPinky1",
    "RightHandPinky2",
    "RightHandPinky3",
    "RightHandPinky4",
    "LeftUpLeg",
    "LeftLeg",
    "LeftFoot",
    "LeftToeBase",
    "LeftToe_End",
    "RightUpLeg",
    "RightLeg",
    "RightFoot",
    "RightToeBase",
    "RightToe_End",
]

BEARD_BONES = ["Neck", "Bone_jaw_corner_L", "Bone_jaw_corner_R", "Bone_L", "Bone_R", "Bone_mustache", "Bone_chin"]
HEADWEAR_BONES = ["Spine", "Neck", "Head"]

NAMING_PATTERNS = [
    # File names.
    r"^([a-z]+)-(\d{2,})$",  # 0: type-01
    r"^([a-z]+)-(\d{2,})-(f|m)$",  # 1: type-01-f
    r"^([a-z]+)-[a-z0-9]+-(\d{2,})$",  # 2: type-something1-01
    r"^([a-z]+)-[a-z0-9]+-(\d{2,})-(f|m)$",  # 3: type-something2-01-m
    r"^([a-z]+)-(f|m)-(\d{2})$",  # 4: type-f-01              DEPRECATED
    r"^([a-z]+)-(f|m)-[a-z0-9]+-(\d{2})$",  # 5: type-m-s0mething-01    DEPRECATED
    r"^([a-z]+)-[a-z0-9]+-(\d{2,})-v\d-(f|m)$",  # 6: type-s0mething-01-v2-m
    # Object, mesh, material names.
    rf"^{PREFIX}_([A-Z][a-z]+)$",  # 7: Wolf3D_Type
    rf"^{PREFIX}_([A-Z][a-z]+)_(\d{2,})$",  # 8: Wolf3D_Type_01
    rf"^{PREFIX}_(Outfit)_(Top|Bottom|Footwear)$",  # 9: Wolf3D_Outfit_Top
    rf"^{PREFIX}_(Body)$",  # 10: Wolf3D_Body
    # Texture files.
    # 11: something-top-D, other-R, another-mask, integral-03-f-top-02-M
    r"^(<replace>)-(top-|bottom-|footwear-)?(\d{2,}-)?(\w|mask)$",
    r"^([a-z]+)-(\d{2,})-(\d{2})-(" + "|".join(COLORSPACE.keys()) + ")$",  # 12: type-01-01-textype
    r"^(body)-(\w+)-(m|f)-(\w)$",  # 13: body-athletic-f-N
    # Unknown.
    r"^designed-to-fail$",
]
EXPORT_PATH = "//../"  # Asset folder. This is hard-coded because it's a convention.
