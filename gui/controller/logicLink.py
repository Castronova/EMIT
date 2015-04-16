__author__ = 'tonycastronova'

import wx

from gui.views.viewLink import ViewLink
import coordinator.engineAccessors as engine

class LogicLink(ViewLink):
    def __init__(self, parent, outputs, inputs, cmd):

        ViewLink.__init__(self, parent, outputs, inputs)

        self.l = None
        self.cmd = cmd

        self.OnStartUp()
        self.InitBindings()

    def InitBindings(self):
        self.LinkNameListBox.Bind(wx.EVT_LISTBOX, self.OnChange)
        self.ButtonNew.Bind(wx.EVT_BUTTON, self.OnSave)
        self.ButtonNew.Bind(wx.EVT_BUTTON, self.NewButton)
        self.ComboBoxTemporal.Bind(wx.EVT_COMBOBOX, self.on_select_temporal)
        self.ComboBoxSpatial.Bind(wx.EVT_COMBOBOX, self.on_select_spatial)
        self.ButtonClose.Bind(wx.EVT_BUTTON, self.OnClose)
        self.OutputComboBox.Bind(wx.EVT_COMBOBOX, self.on_select_output)
        self.InputComboBox.Bind(wx.EVT_COMBOBOX, self.on_select_input)
        self.ButtonSave.Bind(wx.EVT_BUTTON, self.OnSave)

    def OnChange(self, event):
        LinkObject = self.cmd.get_link_by_id(event.GetString())
        # LinkObject = engine.GetLinkById(event.GetString())
        OutputObject = LinkObject.source_exchange_item()
        InputObject = LinkObject.target_exchange_item()
        OutputName = OutputObject._ExchangeItem__name
        InputName = InputObject._ExchangeItem__name
        self.OutputComboBox.SetStringSelection(OutputName)
        self.InputComboBox.SetStringSelection(InputName)
        self.ComboBoxTemporal.SetStringSelection(str(LinkObject._Link__temporal_interpolation))
        self.ComboBoxSpatial.SetStringSelection(str(LinkObject._Link__spatial_interpolation))
        self.l = LinkObject

    def NewButton(self, event):
        self.on_select_input()
        self.on_select_output()

        linkid = self.OnSave()

        if linkid is not None:
            oei = self.OutputComboBox.GetValue()
            iei = self.InputComboBox.GetValue()
            self.LinkNameListBox.Append(('%s -> %s, ID: %s' % (oei, iei, linkid)))

    def GetName(self, event):
        dlg = NameDialog(self)
        dlg.ShowModal()
        # self.txt.SetValue(dlg.result)
        self.LinkNameListBox.Append(str(dlg.result))

    def OnDelete(self, event):

        try:
            for i in range(0, stop=None, step=1):
                self.listbox.Delete(i)
        except:
            pass

        sel = self.listbox.GetSelection()
        if sel != -1:
            self.listbox.Delete(sel)

    def on_select_output(self):
        """
        gets the metadata for the selected output exchange item and populates a tree view
        :return: 1 if successful, else 0
        """
        output_value = self.OutputComboBox.GetValue()
        self.OutputDataTreeCtrl.DeleteAllItems()
        for item in self.output_items:
            if item['name'] == output_value:
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['name'])
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['description'])
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['type'])
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['unit'].UnitName())
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['variable'].VariableNameCV())
                return 1
        return 0

    def on_select_input(self):
        """
        gets the metadata for the selected input exchange item and populates a tree view
        :return: 1 if successful, else 0
        """
        input_value = self.InputComboBox.GetValue()
        self.InputDataTreeCtrl.DeleteAllItems()
        for item in self.input_items:
            if item['name'] == input_value:
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['name'])
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['description'])
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['type'])
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['unit'].UnitName())
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['variable'].VariableNameCV())
                return 1
        return 0

    def on_select_spatial(self, event):
        spatial_value = self.ComboBoxSpatial.GetValue()
        self.spatial_interpolation = self.spatial_transformations[spatial_value]
        self.l.spatial_interpolation(spatial_value)

    def on_select_temporal(self, event):
        temporal_value = self.ComboBoxTemporal.GetValue()
        self.temporal_interpolation = self.temporal_transformations[temporal_value]
        self.l.temporal_interpolation(temporal_value)

    def get_spatial_and_temporal_transformations(self):

        return (self.spatial_interpolation, self.temporal_interpolation)

    def OnClose(self, event):
        dial = wx.MessageDialog(None, 'Do you wish to close without saving?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.Destroy()

    def OnSave(self):
        """
        Saves a link object to the engine
        :return: linkif if successful, else None
        """
        spatial, temporal = self.ComboBoxSpatial.GetValue(), self.ComboBoxTemporal.GetValue()

        # create the link inside the engine
        success = engine.addLink(source_id=self.output_component['id'],
                       source_item=self.OutputComboBox.GetValue(),
                       target_id=self.input_component['id'],
                       target_item=self.InputComboBox.GetValue(),
                       spatial_interpolation=spatial,
                       temporal_interpolation=temporal)
        return success

    def OnStartUp(self):
        links = engine.getLinksBtwnModels(self.output_component['id'], self.input_component['id'])
        [self.LinkNameListBox.Append(str(i)) for i in links]


class NameDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Enter Name!"):
        wx.Dialog.__init__(self, parent, id, title, size=(400, 150))

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.label = wx.StaticText(self, label="Enter the Name of your Link:")
        self.field = wx.TextCtrl(self, value="", size=(300, 20))
        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)

        self.mainSizer.Add(self.label, 0, wx.ALL, 8)
        self.mainSizer.Add(self.field, 0, wx.ALL, 8)

        self.buttonSizer.Add(self.okbutton, 0, wx.ALL, 8)

        self.mainSizer.Add(self.buttonSizer, 0, wx.ALL, 0)

        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        self.Bind(wx.EVT_CLOSE, self.onOK)

        self.SetSizer(self.mainSizer)
        self.result = None

    def onOK(self, event):
        self.result = self.field.GetValue()
        self.Destroy()

    def onCancel(self, event):
        self.result = None
        self.Destroy()