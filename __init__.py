bl_info = {
    "name": "Ready Player Me Validator",
    "description": "Validate your Ready Player Me avatar in Blender",
    "author": "Ready Player Me",
    "version": (0, 0, 1),
    "blender": (2, 91, 0),
    "location": "Window/RPM Validator",
    "category": "Development",
}


# get file path and add to sys.path, so modules can be imported
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

# import addon code
# addon code lives in a sep file, so we can also install it as a module,
# and then run register() and unregister() from the module.
from rpm_validator_addon import *
