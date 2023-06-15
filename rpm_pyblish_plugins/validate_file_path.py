"""Validate the file path and name of the blend file."""
import re
from typing import List, Union

import pyblish.api
import rpm_pyblish_plugins.constants as const
from rpm_pyblish_plugins.action_file_save import FileSave
from rpm_pyblish_plugins.action_file_showinexplorer import FileShowInExplorer


class _FileHierarchy(pyblish.api.ContextPlugin):
    """Validate current file-path and file naming convention.

    The .blend file must be in a subfolder called 'working-files' within the asset's folder.
    The .blend file must have the same name as the asset's folder and follow the naming convention of that asset type.
    """

    label = f"File Path"
    version = (0, 1, 0)
    order = pyblish.api.ValidatorOrder
    hosts = ["blender"]
    optional = True
    actions = [FileShowInExplorer, FileSave]

    def process(self, context):
        from pathlib import Path

        current_file = context.data['currentFile']
        is_saved = context.data['fileIsSaved']
        is_dirty = context.data['fileIsDirty']

        assert current_file, "File is not saved."
        assert is_saved, "File is not saved."
        if is_dirty:
            self.log.warning("File has unsaved changes.")

        asset_type = context.data['assetType']
        current_file = Path(current_file)
        # Validate folder structure.
        report_msg = f"File '{current_file.name}' has failed {self.label} validation.\n"
        error_msg = "Validating file hierarchy convention failed."
        if current_file.parent.stem != "working-files":
            self.log.error(f"{report_msg}File must be saved in the subfolder 'working-files' of an asset's folder, "
                           f"e.g. /hair-01/working-files/hair-01.blend. Found '{current_file.parent.stem}' instead.")
            raise ValueError(error_msg)
        elif (asset_folder := current_file.parent.parent.stem) != current_file.stem:
            self.log.error(f"{report_msg}File name '{current_file.stem}' does not match asset folder '{asset_folder}'."
                           "File name must match asset-folder name, e.g. /hair-01/working-files/hair-01.blend.")
            raise ValueError(error_msg)
        # Do we know what kind of asset we are dealing with?
        if asset_type not in const.KNOWN_ASSET_TYPES:
            known_types_str = ",\n".join(const.KNOWN_ASSET_TYPES)
            self.log.error(
                f"{report_msg}First part of the '-' separated file-name must be one of: {known_types_str}.")
            raise ValueError("Unknown asset type.")
        # Does the name comply to the asset type convention?
        if error_report := validate_filename(current_file.stem, asset_type):
            self.log.error(report_msg + error_report)
            raise ValueError("Validating file naming convention failed.")
        # On Success.
        self.log.info(f"Current file '{current_file.name}' has passed {self.label} validation.")


# Asset type file patterns. The numbers relate to indices in the NAMING_PATTERNS list in constants
pattern_map = {"beard": [0],
               "eyebrow": [0],
               "facewear": [2],
               "glasses": [0, 2],
               "hair": [0],
               "headwear": [2, 3],
               "outfit": [3, 6],
               "shirt": [1, 3],
               # Textures.
               "beard.tex": [11],
               "bodymask.tex": [11],
               "bottom.tex": [11, 12],
               "hair.tex": [11],
               "eye.tex": [0],
               "eyebrow.tex": [11],
               "facemask.tex": [11],
               "facewear.tex": [11],
               "footwear.tex": [11, 12],
               "glasses.tex": [11],
               "headwear.tex": [11],
               "outfit.tex": [11, 12, 13],
               "shirt.tex": [11],
               "top.tex": [11, 12],
               # undefined.
               "unknown": [-1],
               }
# Instance family patterns.
pattern_map.update({key: value for key, value in [
    ("body", [7]),
    ("top", [9]),
    ("bottom", [9]),
    ("footwear", [9]),
    ("beard", [7]),
    ("eyebrow", [7]),
    ("facewear", [7]),
    ("glasses", [7]),
    ("hair", [7]),
    ("headwear", [7]),
    ("outfit", [9, 10]),
    ("shirt", [7]),
]})


def get_patterns(key: Union[str, List[str]]) -> List[str]:
    """Read a regular expression from constants, given a key."""
    if isinstance(key, str):
        return [const.NAMING_PATTERNS[i] for i in pattern_map[key]]
    idx = set()
    for k in key:
        for i in pattern_map[k]:
            idx.add(i)
    return [const.NAMING_PATTERNS[i] for i in idx]


def get_human_readable_patterns(key: Union[str, List[str]]) -> str:
    """Turn regular expressions into human-readable strings."""
    patterns = [p.replace('^', '').replace('$', '').replace(
        '(', '').replace(')', '') for p in get_patterns(key)]
    return ', '.join(patterns)


def get_matched_groups(key: Union[str, List[str]], string: str) -> tuple:
    """Return matched groups if the string matches one of the patterns defined for key.

    :param key: Key or list of keys to retrieve patterns from pattern map.
    :type key: Union[str, List[str]]
    :param string: String to match to patterns.
    :type string: str
    :return: Found content of groups defined in the matched pattern.
    :rtype: tuple
    """
    patterns = get_patterns(key)
    for pattern in patterns:
        if match := re.match(pattern, string):
            return match.groups()
    return ()


def validate_filename(filename: str, asset_type: str) -> str:
    """Validate the file name based on the asset type.

    :param filename: Name of the file.
    :type filename: str
    :param asset_type: Asset type (beard, hair, outfit etc.).
    :type asset_type: str
    :return: Error message. Empty if file name is valid.
    :rtype: str
    """
    if asset_type in (key := ["beard", "eyebrow", "glasses", "hair"]):
        error_msg = (f"File name must be the asset type '{asset_type}' "
                     f"followed by a dash ('-') and a number (at least 2 digits), e.g. '{asset_type}-01.blend'.")
    elif asset_type in (key := ["facewear", "headwear"]):
        error_msg = (f"File name must follow this pattern: '{asset_type}-<subcategory>-<number>' "
                     f"(without angle brackets), e.g. '{asset_type}-halloween-01.blend'.")
    elif asset_type == (key := "outfit"):
        error_msg = (f"File name must follow this pattern: '{asset_type}-<subcategory>-<number>-v<digit>-<f|m>' "
                     f"(without angle brackets), e.g. '{asset_type}-casual-01-v2-f.blend'.")
    elif asset_type == (key := "shirt"):
        error_msg = (f"File name must follow one of these patterns: '{asset_type}-<subcategory>-<number>-<f|m>' "
                     f"or '{asset_type}-<number>-<f|m>' (without angle brackets), "
                     "e.g. 'shirt-meetinvr-01-m.blend' or 'shirt-03-f.blend'.")
    else:
        key = "unknown"
        error_msg = "Unknown asset type. No known naming convention."

    if (groups := get_matched_groups(key, filename)) and groups[0] != asset_type:
        error_msg = f"First element of file name ('{groups[0]}') does not match asset type '{asset_type}'."
        groups = False
    error_msg += f"\nFound '{filename}.blend' instead."
    return (not groups) * error_msg
