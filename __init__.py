# get file path and add to sys.path, so modules can be imported
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

# import addon code
# addon code lives in a sep file, so we can also install it as a module,
# and then run register() and unregister() from the module.
from rpm_validator_addon import *
