import webbrowser
from pathlib import Path

import pyblish.api
import pyblish_config
import Qt5
from pyblish_simple.view import Ui_Form

config_dir = Path(__file__).parent / "configs"


class ModifiedUI(Ui_Form):
    """An UI class showing only validations that are active."""

    def populate_validation_plugins_list(self, selected_instance):
        self.list_validators.clear()

        if selected_instance is None:
            return

        plugins = pyblish.api.plugins_by_instance(self.plugins, selected_instance)
        for plugin in plugins:
            if not issubclass(plugin, pyblish.api.InstancePlugin):
                continue
            # adding only active rpm_pyblish_plugins
            if plugin.active:
                item = Qt5.QtWidgets.QListWidgetItem()
                item.setText(plugin.label)
                item.pyblish_data = plugin
                self.color_item(item, selected_instance)
                self.list_validators.addItem(item)

    def populate_instances_list(self):
        self.list_instance.clear()
        for instance in self.context:
            item = Qt5.QtWidgets.QListWidgetItem()
            item.setText(instance.data["family"].upper() + ": " + str(instance))
            plugins = pyblish.api.plugins_by_family(self.plugins, instance.data["family"])

            item.pyblish_data = instance
            self.color_item(item, instance)
            for plugin in plugins:
                if not issubclass(plugin, pyblish.api.InstancePlugin):
                    continue
                if plugin.active:
                    self.list_instance.addItem(item)
                    break

    def clicked_action(self, pyblish_action=None, item=None):

        selected_item = self.list_instance.currentItem().pyblish_data
        self.context.data["current_item"] = str(selected_item)  # Add the line only in File B
        # Call the original implementation from the superclass
        super().clicked_action(pyblish_action=pyblish_action, item=item)


class ValidatorSimpleUI(Qt5.QtWidgets.QDialog):
    """Add the Documentation button with the Ui_Form"""

    def __init__(self, parent=None):
        super(ValidatorSimpleUI, self).__init__(parent)
        widget = ModifiedUI()

        # create the new button widget
        self.doc_button = Qt5.QtWidgets.QPushButton("Documentation")

        # create the new vertical layout
        new_layout = Qt5.QtWidgets.QVBoxLayout()

        label = Qt5.QtWidgets.QLabel("Select Workflow")

        # # add the label and the dropdown to the layout
        # new_layout.addWidget(self.label)
        # new_layout.addWidget(self.dropdown)

        # create the dropdown
        self.dropdown = Qt5.QtWidgets.QComboBox()
        self.dropdown.addItem("NONE")
        self.populate_dropdown()
        self.dropdown.currentIndexChanged.connect(self.select_config)

        top_bar_layout = Qt5.QtWidgets.QHBoxLayout()
        top_bar_layout.addWidget(label)
        top_bar_layout.addWidget(self.dropdown)
        top_bar_layout.addWidget(self.doc_button)

        # add the new button to the new layout
        new_layout.addLayout(top_bar_layout)
        # new_layout.addWidget(self.dropdown, 0, Qt5.QtCore.Qt.AlignTop)
        new_layout.addWidget(widget)

        # New main window
        self.setLayout(new_layout)

        doc_url = "https://docs.readyplayer.me/asset-creation-guide/validation/validation-checks"
        self.doc_button.clicked.connect(lambda: webbrowser.open(doc_url, new=1, autoraise=True))

    def select_config(self):
        """Select the config to load"""
        config_name = self.dropdown.currentText()

        # unregister pyblish config
        pyblish.api.deregister_all_discovery_filters()
        if config_name == "NONE":
            return

        json_path = config_dir / f"{config_name}.json"  # get path to  config folder from this script
        pyblish_config.load_config_from_json(json_path).register()

    def populate_dropdown(self):
        """Populate the dropdown with the config files"""
        for config in config_dir.glob("*.json"):
            self.dropdown.addItem(config.stem)


# The parent can be overwritten
def show(parent=Qt5.QtWidgets.QApplication.instance().blender_widget):
    """Show the rpm_validator UI"""
    app = Qt5.QtWidgets.QApplication.instance()

    new_app_created = False
    if not app:
        app = Qt5.QtWidgets.QApplication([])
        new_app_created = True

    global window  # prevent widget being garbage collected
    window = ValidatorSimpleUI(parent=parent)
    window.show()

    if new_app_created:
        app.exec()

    return window
