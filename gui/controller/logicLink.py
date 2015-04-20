__author__ = 'tonycastronova'

import wx

from gui.views.viewLink import ViewLink
import coordinator.engineAccessors as engine
import wx.lib.newevent as ne


LinkUpdatedEvent, EVT_LINKUPDATED  =ne.NewEvent()



class LogicLink(ViewLink):
    def __init__(self, parent, outputs, inputs, cmd):

        ViewLink.__init__(self, parent, outputs, inputs)

        self.l = None
        self.cmd = cmd

        self.OnStartUp()
        self.InitBindings()


        # class link variables used to save link
        self.__spatial_interpolation = None
        self.__temporal_interpolation = None
        self.__link_source_id = self.output_component['id']
        self.__link_source_item = None
        self.__link_target_id = self.input_component['id']
        self.__link_target_item = None
        self.__link_name = None
        self.__link_ids = {}
        self.__links = {}

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
        self.Bind(EVT_LINKUPDATED, self.linkUpdated)

    def OnChange(self, event):
        self.__link_name =event.GetString()
        if self.__link_name in self.__link_ids.keys():
            linkid = self.__link_ids[self.__link_name]
            link = engine.getLinkById(linkid)
            self.OutputComboBox.SetStringSelection(link['output_name'])
            self.InputComboBox.SetStringSelection(link['input_name'])
            self.ComboBoxTemporal.SetStringSelection(str(link['temporal_interpolation']))
            self.ComboBoxSpatial.SetStringSelection(str(link['spatial_interpolation']))
            wx.PostEvent(self, LinkUpdatedEvent())
            # self.l = LinkObject

    def linkUpdated(self, event):

        # build link dictionary
        current_link_dict = dict(source_id=self.__link_source_id,
                       source_item=self.__link_source_item,
                       target_id=self.__link_target_id,
                       target_item=self.__link_target_item,
                       spatial_interpolation=self.__spatial_interpolation,
                       temporal_interpolation=self.__temporal_interpolation)

        # grab known link dictionary
        if self.__link_name in self.__links.keys():
            known_link_dict = self.__links[self.__link_name]

            # check if these are the same
            if current_link_dict == known_link_dict:

                # deactivate controls
                self.activateControls(activate=False)
            else:
                self.activateControls(activate=True)
        else:
            self.activateControls(activate=True)

    def activateControls(self, activate=False):

        # todo: this needs to be expanded to check if any forms have been changed

        if activate:
            self.ButtonSave.Enable()
            self.ComboBoxSpatial.Enable()
            self.ComboBoxTemporal.Enable()
            self.OutputDataTreeCtrl.Enable()
            self.InputDataTreeCtrl.Enable()
            self.InputComboBox.Enable()
            self.OutputComboBox.Enable()
            self.ButtonPlot.Enable()
        else:
            self.ButtonSave.Disable()
            self.ComboBoxSpatial.Disable()
            self.ComboBoxTemporal.Disable()
            self.OutputDataTreeCtrl.Disable()
            self.InputDataTreeCtrl.Disable()
            self.InputComboBox.Disable()
            self.OutputComboBox.Disable()
            self.ButtonPlot.Disable()

    def NewButton(self, event):
        self.on_select_input()
        self.on_select_output()

        oei = self.OutputComboBox.GetValue()
        iei = self.InputComboBox.GetValue()

        self.__link_name = '%s -> %s' % (oei, iei)
        self.LinkNameListBox.Append(self.__link_name)

        # self.__links[self.__link_name] =  dict(source_id=self.__link_source_id,
        #                                        source_item=self.__link_source_item,
        #                                        target_id=self.__link_target_id,
        #                                        target_item=self.__link_target_item,
        #                                        spatial_interpolation=self.__spatial_interpolation,
        #                                        temporal_interpolation=self.__temporal_interpolation)

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

        # get selected value
        output_value = self.OutputComboBox.GetValue()

        # set selected value
        self.__link_source_item = output_value

        # set tree view
        self.OutputDataTreeCtrl.DeleteAllItems()
        for item in self.output_items:
            if item['name'] == output_value:
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['name'])
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['description'])
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['type'])
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['unit'].UnitName())
                self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['variable'].VariableNameCV())
                wx.PostEvent(self, LinkUpdatedEvent())
                return 1
        return 0

    def on_select_input(self):
        """
        gets the metadata for the selected input exchange item and populates a tree view
        :return: 1 if successful, else 0
        """

        # get selected value
        input_value = self.InputComboBox.GetValue()

        # set selected value
        self.__link_target_item = input_value

        # set tree view
        self.InputDataTreeCtrl.DeleteAllItems()
        for item in self.input_items:
            if item['name'] == input_value:
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['name'])
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['description'])
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['type'])
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['unit'].UnitName())
                self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, item['variable'].VariableNameCV())
                wx.PostEvent(self, LinkUpdatedEvent())
                return 1
        return 0

    def on_select_spatial(self, event):
        spatial_value = self.ComboBoxSpatial.GetValue()
        if spatial_value == 'None Specified':
            self.__spatial_interpolation = None
        else:
            self.__spatial_interpolation = self.spatial_transformations[spatial_value]
        wx.PostEvent(self, LinkUpdatedEvent())

    def on_select_temporal(self, event):
        temporal_value = self.ComboBoxTemporal.GetValue()
        if temporal_value == 'None Specified':
            self.__temporal_interpolation = None
        else:
            self.__temporal_interpolation = self.temporal_transformations[temporal_value]
        wx.PostEvent(self, LinkUpdatedEvent())

    def OnClose(self, event):

        if self.ButtonSave.Enabled:

            dial = wx.MessageDialog(None, 'Do you wish to close without saving?', 'Question',
                                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            if dial.ShowModal() == wx.ID_YES:
                self.Destroy()
        else:
            self.Destroy()

    def OnSave(self, event):
        """
        Saves a link object to the engine
        :return: linkif if successful, else None
        """

        kwargs =    dict(source_id=self.__link_source_id,
                       source_item=self.__link_source_item,
                       target_id=self.__link_target_id,
                       target_item=self.__link_target_item,
                       spatial_interpolation=self.__spatial_interpolation,
                       temporal_interpolation=self.__temporal_interpolation)

        # create the link inside the engine
        linkid = engine.addLink(**kwargs)

        current_link = self.__link_name
        self.__link_ids[current_link] = linkid
        self.__links[current_link] = kwargs
        wx.PostEvent(self, LinkUpdatedEvent())

        return linkid

    def OnStartUp(self):
        links = engine.getLinksBtwnModels(self.output_component['id'], self.input_component['id'])
        for l in links:
            link_id = '%s -> %s [unique id = %s]'%(l['source_item'],l['target_item'],l['id'])
            self.LinkNameListBox.Append(link_id)

        self.activateControls()

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