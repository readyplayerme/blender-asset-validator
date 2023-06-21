# rpm-blender-validator
The Python Blender validator code for your RPM content.

- rpm_pyblish_plugins: Pyblish validation plugins & fix actions
- rpm_validator: custom Pyblish UI

## Install
This repo can be installed either as a Blender add-on, or through PIP. 

#### Blender add-on (recommended)
Installing as a Blender add-on
- gives the option to disable this tool
- adds a menu button to launch the window

Instructions:
- download latest
- install as a blender add-on, by extracting the whole folder in your addons folder
- enable the add-on in blender
- PIP install the dependencies from `requirements.txt`

#### PIP
Installing through PIP
- installs the tool as a Python module
- no option to disable, which means it won't accidentally be disabled
- auto installs the dependencies
- no menu button, but can be launched from the python console

Instructions:
- PIP install the module from github
```
python -m pip install git+https://github.com/readyplayerme/rpm-blender-validator
```

## validation in a custom pipeline
Some of our partners require more advanced control of the validations.
Here's a sample going through the basics.

```python
import pyblish.api
import pyblish.util

# register rpm plugins
# this is done automatically if you use the RPM addon or script file path
import rpm_pyblish_plugins
rpm_pyblish_plugins.register()

# discover the validation plugins
plugins = pyblish.api.discover()

# collect meshes materials etc
context = pyblish.util.collect(plugins=plugins)

# run the validations
context = pyblish.util.validate(context=context, plugins=plugins)

# run autofix on all failed instances
for plugin in plugins:
    try:
        if hasattr(plugin, "fix"):
            pyblish_action = plugin.fix
            pyblish_action.process(self=pyblish_action, context=context, plugin=plugin)
    except Exception as e:
        print(traceback.print_tb(e.__traceback__))
        print("failed to fix:", e)
```

### Issues & bugs
Please report them here [here](https://github.com/readyplayerme/rpm-blender-validator/issues)
