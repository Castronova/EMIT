from gui.views.ModelView import ModelView
from gui.views.ModelView import ModelDetailsView
from gui.controller.SpatialCtrl import SpatialCtrl
from sprint import *
from utilities import models
from gui.controller.CanvasObjectsCtrl import ModelBox
import coordinator.engineAccessors as engineAccessors
from gui.views.ModelView import ModelEditView


class ModelCtrl(ModelView):
    def __init__(self, parent):
        ModelView.__init__(self, parent)

        self.model_details_controller = None
        self.model_edit_controller = None
        self.model_spatial_controller = None

    def add_detail_page(self):
        self.model_details_controller = ModelDetailsCtrl(self.notebook)
        self.notebook.AddPage(self.model_details_controller, "Details")
        return self.model_details_controller

    def add_edit_page(self):
        self.model_edit_controller = ModelEditCtrl(self.notebook)
        self.notebook.AddPage(self.model_edit_controller, "Edit")
        return self.model_edit_controller

    def add_spatial_page(self):
        self.model_spatial_controller = SpatialCtrl(self.notebook)
        self.notebook.AddPage(self.model_spatial_controller, "Spatial")
        return self.model_spatial_controller


class ModelDetailsCtrl(ModelDetailsView):

    def __init__(self, parent):
        ModelDetailsView.__init__(self, parent)

        self.data_path = ""
        self._data = None
        self.model_object = None

    def populate_grid_by_model_object(self):
        if not isinstance(self.model_object, ModelBox):
            sPrint("ModelDetails.model_object needs to by type ModelBox")
            return

        model_as_json = engineAccessors.getModelById(self.model_object.ID)

        if not isinstance(model_as_json, dict):
            sPrint("ModelDetailsCtrl.populate_grid_by_model_object.model_as_json needs to be type dictionary")
            return

        if "params" in model_as_json:
            if "path" in model_as_json["params"]:
                self._data = models.parse_json(model_as_json["params"]["path"])
                self.grid.add_data(self._data)
                return

        elif "attrib" in model_as_json:
            if "mdl" in model_as_json["attrib"]:
                self._data = models.parse_json(model_as_json["attrib"]["mdl"])
                self.grid.add_data(self._data)
                return

        self.grid.add_section("General")
        for key, value in model_as_json.iteritems():
            if isinstance(value, dict):
                self.grid.add_dictionary(value, key)
            else:
                self.grid.add_data_to_section(0, key, value)
        return

    def populate_grid_by_path(self):
        if not os.path.exists(self.data_path):
            sPrint("ModelDetailsCtrl.data_path does not exist or has not been set")
            return

        self._data = models.parse_json(self.data_path)

        if self.data_path[-4:] == ".sim":
            self._load_simulation()
        else:
            self.grid.add_data(self._data)

    def _load_simulation(self):
        if not isinstance(self._data, dict):
            sPrint("ModelDetailsCtrl._data must be type dict")
            return

        sorted_sections = sorted(self._data.keys())
        for each_section in sorted_sections:
            if isinstance(self._data[each_section], list):
                if each_section == "links":
                    for item in self._data[each_section]:
                        self.grid.add_dictionary(item, "Link " + item["from_name"] + " -> " + item["to_name"])

                if each_section == "models":
                    self.grid.add_list_of_dictionary(self._data[each_section], "name")
        self.grid.enable_scroll_bar_on_startup()


class ModelEditCtrl(ModelEditView):
    def __init__(self, parent):
        ModelEditView.__init__(self, parent)
        self.file_path = ""

    def populate_edit(self):
        if not os.path.exists(self.file_path):
            sPrint("ModelEditCtrl.file_path does not exist or has not been set")
            return

        with open(self.file_path, "r") as file_handler:
            self.text_ctrl.SetValue(file_handler.read())
            file_handler.close()

