import uuid

__author__ = 'tonycastronova'

import wx

from gui.views.viewLink import ViewLink
import coordinator.engineAccessors as engine
import wx.lib.newevent as ne


LinkUpdatedEvent, EVT_LINKUPDATED  =ne.NewEvent()



class LogicLink(ViewLink):
    def __init__(self, parent, outputs, inputs):

        ViewLink.__init__(self, parent, outputs, inputs)

        self.l = None
        # self.cmd = cmd




        # class link variables used to save link
        self.__selected_link = None

        self.__spatial_interpolation = None
        self.__temporal_interpolation = None
        self.__link_source_id = self.output_component['id']
        self.__link_source_item = None
        self.__link_target_id = self.input_component['id']
        self.__link_target_item = None
        self.__link_name = None
        self.__link_ids = {}
        self.__links = {}

        self.OnStartUp()
        self.InitBindings()

    def InitBindings(self):
        self.LinkNameListBox.Bind(wx.EVT_LISTBOX, self.OnChange)
        self.ButtonNew.Bind(wx.EVT_BUTTON, self.OnSave)
        self.ButtonNew.Bind(wx.EVT_BUTTON, self.NewButton)
        self.ButtonDelete.Bind(wx.EVT_BUTTON, self.OnDelete)
        self.ComboBoxTemporal.Bind(wx.EVT_COMBOBOX, self.on_select_temporal)
        self.ComboBoxSpatial.Bind(wx.EVT_COMBOBOX, self.on_select_spatial)
        self.ButtonCancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.OutputComboBox.Bind(wx.EVT_COMBOBOX, self.on_select_output)
        self.InputComboBox.Bind(wx.EVT_COMBOBOX, self.on_select_input)
        self.ButtonSave.Bind(wx.EVT_BUTTON, self.OnSave)
        self.Bind(EVT_LINKUPDATED, self.linkSelected)

    def OnChange(self, event):
        linkname =event.GetString()
        l = self._LogicLink__links[linkname]
        # linkid = self.__selected_link[linkname]['uid']

        # if self.__link_name in self.__link_ids.keys():
        #     linkid = self.__link_ids[self.__link_name]
        link = engine.getLinkById(l.uid)
        self.OutputComboBox.SetStringSelection(l.oei)
        self.InputComboBox.SetStringSelection(l.iei)
        self.ComboBoxTemporal.SetStringSelection(str(l.temporal_interpolation))
        self.ComboBoxSpatial.SetStringSelection(str(l.spatial_interpolation))
        wx.PostEvent(self, LinkUpdatedEvent())
            # self.l = LinkObject

    def linkSelected(self, event):

        # get the selected link object
        selected = self.LinkNameListBox.GetStringSelection()
        l = self.__links[selected]
        self.__selected_link = l


        # build link dictionary
        # current_link_dict = dict(source_id=self.__link_source_id,
        #                source_item=self.__link_source_item,
        #                target_id=self.__link_target_id,
        #                target_item=self.__link_target_item,
        #                spatial_interpolation=self.__spatial_interpolation,
        #                temporal_interpolation=self.__temporal_interpolation)

        # grab known link dictionary
        # if self.__link_name in self.__links.keys():
        #     known_link_dict = self.__links[self.__link_name]
        #
            # check if these are the same
            # if current_link_dict == known_link_dict:
            #
                # deactivate controls
                # self.activateControls(activate=False)
            # else:
            #     self.activateControls(activate=True)
        # else:
        #     self.activateControls(activate=True)
    #
    def activateControls(self, activate=True):

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

        # generate a unique name for this link
        oei = self.OutputComboBox.GetValue()
        iei = self.InputComboBox.GetValue()

        # create a link object and save it at the class level
        l = LinkInfo(oei, iei, self.__link_source_id, self.__link_target_id)
        self.__links[l.name] = l

        # add the link name to the links list box
        self.LinkNameListBox.Append(l.name)

        # set the currently selected link
        self.__selected_link = l

        # todo: clear this if the link is not saved
        # initialize the selected link dictionary
        # self.__selected_link['uid'] = uid
        # self.__selected_link['source_item'] = oei
        # self.__selected_link['target_item'] = iei
        # self.__selected_link['name'] = link_name

    def GetName(self, event):
        dlg = NameDialog(self)
        dlg.ShowModal()
        # self.txt.SetValue(dlg.result)
        self.LinkNameListBox.Append(str(dlg.result))

    def OnDelete(self, event):
        # First try to delete the item from the cmd, if it has not yet been saved, it will just
        # remove itself from the ListBox.
        try:
            sel = self.LinkNameListBox.GetStringSelection()
            if sel not in self.__link_ids.keys():
                # link has not been added yet
                pass
            else:
                # remove the link from the engine
                deleteid = self.__link_ids[sel]
                engine.removeLinkById(deleteid)
        except:
            print 'ERROR|Could not remove link'
            return

        # remove the link name from the links list box
        index = self.LinkNameListBox.GetSelection()
        self.LinkNameListBox.Delete(index)

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

    def OnCancel(self, event):

        dial = wx.MessageDialog(None, 'Are you sure that you want to close without saving?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.Destroy()

    def OnSave(self, event):
        """
        Saves all link objects to the engine and then closes the link creation window
        """

        for l in self.__links.values():

            try:
                kwargs =    dict(source_id=l.source_id,
                               source_item=l.oei,
                               target_id=l.target_id,
                               target_item=l.iei,
                               spatial_interpolation=l.spatial_interpolation,
                               temporal_interpolation=l.temporal_interpolation,
                               uid = l.uid)

                # remove the existing link, if there is one
                removed = engine.removeLinkById(l.uid)

                # add a new link inside the engine
                linkid = engine.addLink(**kwargs)

                if linkid:
                    l.saved = True

                # self.__links[current_link] = kwargs
                wx.PostEvent(self, LinkUpdatedEvent())
            except:
                print 'ERROR|Could not save link: %s'%l.name


        self.Destroy()

    def OnStartUp(self):
        links = engine.getLinksBtwnModels(self.output_component['id'], self.input_component['id'])
        for l in links:
            link = LinkInfo(l['source_item'],
                            l['target_item'],
                            l['source_id'],
                            l['target_id'],
                            l['id'],
                            l['spatial_interpolation'],
                            l['temporal_interpolation'])

            self.__links[link.name] = link

            self.LinkNameListBox.Append(link.name)

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

class LinkInfo():
    def __init__(self, oei, iei, source_id, target_id, uid=None, spatial_interpolation=None, temporal_interpolation=None):


        self.uid = 'L'+uuid.uuid4().hex[:5] if uid is None else uid
        self.name = self.generate_link_name(oei,iei,self.uid)
        self.oei = oei
        self.iei = iei
        self.source_id = source_id
        self.target_id = target_id
        self.spatial_interpolation =spatial_interpolation
        self.temporal_interpolation =  temporal_interpolation

        self.saved = False

    def generate_link_name(self, oei_name, iei_name, uid):

        return  '%s -> %s [unique id = %s]'%(oei_name, iei_name, uid)