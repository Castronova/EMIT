import wx
import wx.propgrid as wxpg
from wx.lib.pubsub import pub as Publisher
from gui.controller.PropertiesPageCtrl import PropertiesPageCtrl
from gui.views.ModelView import ModelView
from utilities import gui


class ModelCtrl(ModelView):

    def __init__(self, parent, model_id=None, **kwargs):

        ModelView.__init__(self, parent, **kwargs)

        self.parent = parent
        self.properties_page_controller = PropertiesPageCtrl(self.notebook)
        self.notebook.AddPage(self.properties_page_controller, "Properties")
        if self.spatial_page:
            self.notebook.AddPage(self.spatial_page, "Spatial Definition")

        #  Bindings
        if self.edit:
            self.notebook.AddPage(self.txtctrlView, "Edit Properties", False)
            self.SaveButton.Bind(wx.EVT_BUTTON, self.OnSave)

        if self.spatial:
            self.setup_spatial(model_id)

    def ConfigurationDisplay(self, fileExtension):
        self.current_file = fileExtension
        filehandle=open(fileExtension)
        self.xmlTextCtrl.SetValue(filehandle.read())
        filehandle.close()
        self.SetTitle("Details")

    def OnSave(self, event):

        dlg = wx.MessageDialog(None, 'Are you sure you would like to overwrite?', 'Question', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() !=wx.ID_NO:
            Publisher.subscribe(self.OnSave, 'textsavepath')

            # Grab the content to be saved
            itcontains = self.TextDisplay.GetValue().encode('utf-8').strip()

            # Open the file for write, write, close
            filehandle=open((self.current_file),'w')
            filehandle.write(itcontains)
            filehandle.close()

            self.Close()

    def PopulateEdit(self, fileExtension):
        # the text edit window
        self.current_file = fileExtension
        filehandle=open(fileExtension)
        self.TextDisplay.SetValue(filehandle.read())
        filehandle.close()
        self.SetTitle("Details")

    def setup_spatial(self, model_id):
        iei = self.spatial_page.controller.get_input_exchange_item_by_id(model_id)
        igeoms = self.spatial_page.controller.get_geometries(iei)

        oei = self.spatial_page.controller.get_output_exchange_item_by_id(model_id)
        ogeoms = self.spatial_page.controller.get_geometries(oei)

        self.spatial_page.controller.set_data(target=igeoms, source=ogeoms)
        self.spatial_page.controller.raw_input_data = iei
        self.spatial_page.controller.raw_output_data = oei

        self.spatial_page.controller.add_input_combo_choices(igeoms.keys())
        self.spatial_page.controller.add_output_combo_choices(ogeoms.keys())
