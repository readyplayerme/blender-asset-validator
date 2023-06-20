# rpm-blender-validator
The Blender validator for your RPM content

- rpm_pyblish_plugins: Pyblish validation plugins & fix actions
- rpm_validator: custom Pyblish UI

## Install
This repo can be installed either as a Blender add-on, or through PIP. 

#### Blender add-on
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
- installs the tool as a python module
- no option to disable, which means it won't accidentally be disabled
- auto installs the dependencies
- no menu button, but can be launched from the python console

Instructions:
- PIP install the module from github
```
python -m pip install git+https://github.com/readyplayerme/rpm-blender-validator
```

### Issues & bugs
Please report them here [here](https://github.com/readyplayerme/rpm-blender-validator/issues)
