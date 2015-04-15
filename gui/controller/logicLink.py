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
        self.on_select_input(event)
        self.on_select_output(event)
        self.OnSave(event)
        self.LinkNameListBox.Append(self.l._Link__id)

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

    def on_select_output(self, event):
        output_value = self.OutputComboBox.GetValue()
        self.OutputDataTreeCtrl.DeleteAllItems()

        self.output_selected = self.output.get_output_exchange_item_by_name(output_value)
        self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.output_selected._ExchangeItem__name)
        self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem,
                                                self.output_selected._ExchangeItem__description)

        self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.output_selected._ExchangeItem__type)
        self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem,
                                                self.output_selected._ExchangeItem__unit._Unit__unitName)

    def on_select_input(self, event):
        input_value = self.InputComboBox.GetValue()
        self.input_selected = self.input.get_input_exchange_item_by_name(input_value)
        self.InputDataTreeCtrl.DeleteAllItems()

        self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.input_selected._ExchangeItem__name)
        self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem,
                                               self.input_selected._ExchangeItem__description)
        self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.input_selected._ExchangeItem__type)
        self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem,
                                               self.input_selected._ExchangeItem__unit._Unit__unitName)

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

    def OnSave(self, event):
        # TODO: Need to send information to cmd, unless there is another way, we need to add cmd into the class
        spatial, temporal = self.ComboBoxSpatial.GetValue(), self.ComboBoxTemporal.GetValue()
        # set the link in cmd
        self.l = l = self.cmd.add_link(self.output._Model__id, self.OutputComboBox.GetValue(),
                                       self.input._Model__id, self.InputComboBox.GetValue())

        # set interpolations
        # l.spatial_interpolation(spatial)
        # l.temporal_interpolation(temporal)

    def OnStartUp(self):
        Links = self.cmd.get_links_btwn_models(self.output, self.input)
        [self.LinkNameListBox.Append(str(i)) for i in Links]


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