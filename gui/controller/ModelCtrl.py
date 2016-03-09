import wx
import wx.propgrid as wxpg
from wx.lib.pubsub import pub as Publisher

from gui.views.ModelView import ModelView
from utilities import gui


class ModelCtrl(ModelView):

    def __init__(self, parent, model_id=None, **kwargs):

        ModelView.__init__(self, parent, **kwargs)

        #Bindings
        if self.edit:
            self.SaveButton.Bind(wx.EVT_BUTTON, self.OnSave)

        if self.spatial:
            self.setup_spatial(model_id)

    def setup_spatial(self, model_id):
        iei = self.spatial_page.controller.get_input_exchange_item_by_id(model_id)
        igeoms = self.spatial_page.controller.get_geometries(iei)
        oei = self.spatial_page.controller.get_output_exchange_item_by_id(model_id)
        ogeoms = self.spatial_page.controller.get_geometries(oei)
        self.spatial_page.controller.set_data(target=igeoms, source=ogeoms)
        if iei:
            self.spatial_page.controller.set_selection_data(target_name=iei[0]['name'])
            self.spatial_page.controller.input_checkbox.SetValue(True)
            self.spatial_page.controller.update_plot(iei[0]['name'])
        else:
            self.spatial_page.controller.input_checkbox.Disable()
        if oei:
            self.spatial_page.controller.set_selection_data(source_name=oei[0]['name'])
            self.spatial_page.controller.output_checkbox.SetValue(True)
            self.spatial_page.controller.update_plot(oei[0]['name'])
        else:
            self.spatial_page.controller.output_checkbox.Disable()

        if self.spatial_page.controller.output_exchange_item:
            self.spatial_page.controller.edit_grid("output", 1, 1, self.spatial_page.controller.source_name)
            self.spatial_page.controller.edit_grid("output", 2, 1, self.spatial_page.controller.output_exchange_item[0].GetGeometryName())
            self.spatial_page.controller.edit_grid("output", 3, 1, self.spatial_page.controller.output_exchange_item[0].GetCoordinateDimension())
            self.spatial_page.controller.edit_grid("output", 5, 1, self.spatial_page.controller.output_exchange_item[0].GetPointCount())

        if self.spatial_page.controller.input_exchange_item:
            self.spatial_page.controller.edit_grid("input", 1, 1, self.spatial_page.controller.target_name)
            self.spatial_page.controller.edit_grid("input", 2, 1, self.spatial_page.controller.input_exchange_item[0].GetGeometryName())
            self.spatial_page.controller.edit_grid("input", 3, 1, self.spatial_page.controller.input_exchange_item[0].GetCoordinateDimension())
            self.spatial_page.controller.edit_grid("input", 5, 1, self.spatial_page.controller.input_exchange_item[0].GetPointCount())

    def update_plot_output(self, event):
        received_data = event.EventObject.StringSelection
        self.TopLevelParent.plotPanel.set_selection_output(received_data)
        self.TopLevelParent.plotPanel.updatePlot()

    def update_plot_input(self, event):
        received_data = event.EventObject.StringSelection
        self.TopLevelParent.plotPanel.set_selection_input(received_data)
        self.TopLevelParent.plotPanel.updatePlot()

    def PopulateEdit(self, fileExtension):

        # the text edit window
        self.current_file = fileExtension
        filehandle=open(fileExtension)
        self.TextDisplay.SetValue(filehandle.read())
        filehandle.close()
        self.SetTitle("Editor")

    def ConfigurationDisplay(self, fileExtension):
        self.current_file = fileExtension
        filehandle=open(fileExtension)
        self.xmlTextCtrl.SetValue(filehandle.read())
        filehandle.close()
        self.SetTitle("File Configurations (Read-Only)")

    def PopulateSummary(self, fileExtension):

        d = gui.parse_config(fileExtension)

        sections = sorted(d.keys())

        for section in sections:
            if section is 'basedir':
                pass
            else:
                try:
                    g = self.PropertyGrid.Append( wxpg.PropertyCategory(section))
                except:
                    pass

            if isinstance (d[section], list):
                items = d[section]
                for item in items:
                    while len(item.keys()) > 0:
                        for keyitem in item.keys():
                            var = item.pop(keyitem)
                            try:
                                self.PropertyGrid.Append( wxpg.StringProperty(str(keyitem), value=str(var)))
                            except:
                                pass

    def PopulateProperties(self, modelid, iei=None, oei=None):
        # Fills on the information for models from the database
        # Also implement this to populate all models not only from database
        # PopulateSummary works only for models not from database.
        # iei = input exchange item.
        # oei = output exchange item.
        # not all models will have inputs & outputs so that's why their set to None by default.

        self.PropertyGrid.Append(wxpg.PropertyCategory("General"))
        self.PopulatePropertyGrid(modelid)

        if iei:
            self.PropertyGrid.Append(wxpg.PropertyCategory("Input"))
            self.PopulatePropertyGrid(iei[0])

        if oei:
            self.PropertyGrid.Append(wxpg.PropertyCategory("Output"))
            self.PopulatePropertyGrid(oei[0])

    def PopulatePropertyGrid(self, dictionary):
        #  A recursive method, checks if there is a dictionary inside a dictionary.
        if not dictionary:  # if empty dictionary than do nothing
            return
        for key, value in dictionary.iteritems():
            if type(value) is dict:
                self.PopulatePropertyGrid(value)
            elif type(value) is list:
                value = value[0] # Extract dictionary
                self.PopulatePropertyGrid(value)
            else:
                try:
                    self.PropertyGrid.Append(wxpg.StringProperty(str(key).capitalize(), value=str(value)))
                except:
                    pass

    def PopulateDetails(self, fileExtension):

        # get a dictionary of config parameters
        d = gui.parse_config(fileExtension)

        root = self.DetailTree.AddRoot('Data')
        self.DetailTree.ExpandAll()

        # get sorted sections
        sections = sorted(d.keys())

        for section in sections:
            # add this item as a group

            g = self.DetailTree.AppendItem(root, section)

            if type(d[section]) == list:
                items = d[section]
                for item in items:
                    p = g
                    while len(item.keys()) > 0:

                        #for item in d[section]:
                        if 'variable_name_cv' in item:
                            var = item.pop('variable_name_cv')
                            p =  self.DetailTree.AppendItem(g,var)

                        # get the next item in the dictionary
                        i = item.popitem()

                        if i[0] != 'type':
                            k = self.DetailTree.AppendItem(p,i[0])
                            self.DetailTree.AppendItem(k, i[1])
            else:
                self.DetailTree.AppendItem(g,d[section])

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
