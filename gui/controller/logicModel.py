__author__ = 'tonycastronova'

from gui.views.viewModel import ViewModel
from utilities import gui
import wx.propgrid as wxpg
from wx.lib.pubsub import pub as Publisher
import wx


class LogicModel(ViewModel):

    def __init__(self, parent, **kwargs):

        ViewModel.__init__(self, parent, **kwargs)

        #Bindings
        if self.edit:
            self.SaveButton.Bind(wx.EVT_BUTTON, self.OnSave)

        # Add another conditional so these bindings don't get added when they don't need to perhaps?
        self.inputSelections.Bind(wx.EVT_COMBOBOX, self.update_plot)
        self.outputSelections.Bind(wx.EVT_COMBOBOX, self.update_plot)


    def update_plot(self, event):
        print "selection updates"

    def PopulateEdit(self, fileExtension):

        # the text edit window
        self.current_file = fileExtension
        filehandle=open(fileExtension)
        self.TextDisplay.SetValue(filehandle.read())
        filehandle.close()
        self.SetTitle("Editor")

    def PopulateSpatial(self, coordlist, type):
        if type == 'input':
            self.matplotView.input_data(coordlist)
        elif type == 'output':
            self.matplotView.output_data(coordlist)

    def PopulateSpatialGeoms(self, geometrycoords, type):

        if geometrycoords is None: return

        if type == 'input':
            self.plotPanel.set_input_data(geometrycoords)
        elif type == 'output':
                self.plotPanel.set_output_data(geometrycoords)

        # # todo: extend support for multiple inputs/outputs
        # for variable, geom in geometrycoords.iteritems():
        #
        #     if type == 'input':
        #         self.matplotView.input_data(geom)
        #     elif type == 'output':
        #         self.matplotView.output_data(geom)
        #     return

    def PopulateSummary(self, fileExtension):

        d = gui.parse_config_without_validation(fileExtension)

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


    def PopulateDetails(self, fileExtension):

        # get a dictionary of config parameters
        d = gui.parse_config_without_validation(fileExtension)

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

        else:
            pass