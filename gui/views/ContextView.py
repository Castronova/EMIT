import wx
import coordinator.engineAccessors as engine
from gui.controller.ModelCtrl import ModelCtrl
from utilities import models
from sprint import *

class LinkContextMenu(wx.Menu):
    def __init__(self, parent, e):
        super(LinkContextMenu, self).__init__()

        self.arrow_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveLink, mmi)

    def RemoveLink(self, e):
        self.parent.remove_link(self.arrow_obj)


class ModelContextMenu(wx.Menu):
    def __init__(self, parent, e):
        super(ModelContextMenu, self).__init__()

        self.model_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.ShowModelDetails, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveModel, mmi)

    def ShowModelDetails(self, event):
        # create a frame to bind the details page to
        f = wx.Frame(self.GetParent())

        kwargs = {'edit': False, 'spatial': True}
        model_details = ModelCtrl(f, model_id=self.model_obj.ID, **kwargs)

        model = engine.getModelById(self.model_obj.ID)

        details_populated = False
        try:
            if "params" in model.keys():
                path = model["params"]["path"]  # Get the model file path
                data = models.parse_json(path)
                model_details.properties_page_controller.add_data(data)
                details_populated = True
        except:
            details_populated = False

        try:
            if "mdl" in model["attrib"] and not details_populated:
                # Populate the grid
                data = models.parse_json(model["attrib"]["mdl"])
                model_details.properties_page_controller.add_data(data)
                details_populated = True
        except:
            details_populated = False

        if not details_populated:
            try:
                # A default way to load the data
                model_details.properties_page_controller.add_section("General")
                for key, value in engine.getModelById(self.model_obj.ID).iteritems():
                    if isinstance(value, dict):
                        model_details.properties_page_controller.add_dictionary(value, key)
                    else:
                        model_details.properties_page_controller.add_data_to_section(0, key, value)
                details_populated = True
            except:
                details_populated = False

        if details_populated:
            model_details.Show()
        else:
            sPrint('Could not populate model details.  This is most likely '
                   'due to malformed data.', MessageType.ERROR)

    def RemoveModel(self, e):
        self.parent.remove_model(self.model_obj)
