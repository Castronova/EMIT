import wx
from gui.controller.ModelCtrl import ModelCtrl


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
        self.Bind(wx.EVT_MENU, self.show_model_ctrl, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.remove_model, mmi)

    def show_model_ctrl(self, event):

        frame = wx.Frame(None)
        frame.SetSize((640, 690))

        models_controller = ModelCtrl(frame)

        details = models_controller.add_detail_page()
        details.model_object = self.model_obj
        details.populate_grid_by_model_object()

        spatial = models_controller.add_spatial_page()
        iei = spatial.get_input_exchange_item_by_id(self.model_obj.ID)
        igeoms = spatial.get_geometries(iei)

        oei = spatial.get_output_exchange_item_by_id(self.model_obj.ID)
        ogeoms = spatial.get_geometries(oei)

        spatial.set_data(target=igeoms, source=ogeoms)
        spatial.raw_input_data = iei
        spatial.raw_output_data = oei

        spatial.add_input_combo_choices(igeoms.keys())
        spatial.add_output_combo_choices(ogeoms.keys())

        frame.Show()

    def remove_model(self, e):
        self.parent.remove_model(self.model_obj)
