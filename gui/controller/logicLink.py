from collections import OrderedDict
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

        self.__links = []
        # self.__links = {}

        self.link_obj_hit = False


        self.OnStartUp()
        self.InitBindings()

    def InitBindings(self):
        self.LinkNameListBox.Bind(wx.EVT_LISTBOX, self.OnChange)
        self.LinkNameListBox.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
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

    def OnLeftUp(self, event):

        if not self.link_obj_hit:

            link_name = self.__selected_link.name()

            selected_index = self.LinkNameListBox.Items.index(link_name)
            self.LinkNameListBox.SetSelection(selected_index)
            # self.OnChange(None)

        # reset the state of link_obj_hit
        self.link_obj_hit = False



    def OnChange(self, event):
        link_name = self.LinkNameListBox.GetStringSelection()
        l = self.__selected_link
        # link = engine.getLinkById(l.uid)
        self.OutputComboBox.SetStringSelection(l.oei)
        self.InputComboBox.SetStringSelection(l.iei)
        self.ComboBoxTemporal.SetStringSelection(str(l.temporal_interpolation))
        self.ComboBoxSpatial.SetStringSelection(str(l.spatial_interpolation))

        self.__selected_link = l


        # set the state of link_obj_hit
        self.link_obj_hit = True

        wx.PostEvent(self, LinkUpdatedEvent())

    def linkSelected(self, event):

        # get the selected link object
        selected = self.LinkNameListBox.GetStringSelection()
        known_link_ids = [l.name() for l in self.__links]
        if selected in known_link_ids:
            l = self.__links[known_link_ids.index(selected)]
            # l = self.__links[selected]
            self.__selected_link = l

            # activate controls
            self.activateControls(True)

            self.populate_output_metadata(l)
            self.populate_input_metadata(l)

        else:
            # deactivate controls if nothing is selected
            self.activateControls(False)

    def activateControls(self, activate=True):

        # todo: this needs to be expanded to check if any forms have been changed

        if activate:
            self.ButtonSave.Enable()
            self.ComboBoxSpatial.Enable()
            self.ComboBoxTemporal.Enable()
            # self.OutputDataTreeCtrl.Enable()
            # self.InputDataTreeCtrl.Enable()
            self.InputComboBox.Enable()
            self.OutputComboBox.Enable()
            self.ButtonPlot.Enable()
        else:
            self.ButtonSave.Disable()
            self.ComboBoxSpatial.Disable()
            self.ComboBoxTemporal.Disable()
            # self.OutputDataTreeCtrl.Disable()
            # self.InputDataTreeCtrl.Disable()
            self.InputComboBox.Disable()
            self.OutputComboBox.Disable()
            self.ButtonPlot.Disable()

    def refreshLinkNameBox(self):

        self.LinkNameListBox.Clear()
        for l in self.__links:
            self.LinkNameListBox.Append(l.name())


    def NewButton(self, event):

        # generate a unique name for this link
        oei = self.OutputComboBox.GetValue()
        iei = self.InputComboBox.GetValue()

        # create a link object and save it at the class level
        l = LinkInfo(oei, iei, self.__link_source_id, self.__link_target_id)
        # self.__links[l.name()] = l
        self.__links.append(l)

        # add the link name to the links list box
        # self.LinkNameListBox.Append(l.name())
        self.refreshLinkNameBox()

        # set the currently selected link
        self.__selected_link = l

        # select the last value
        self.LinkNameListBox.SetSelection(self.LinkNameListBox.GetCount()-1)
        self.OnChange(None)


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

    def populate_output_metadata(self, l):

        # get the link object
        # l = self.__links[self.__selected_link.name()]
        outputs = l.output_metadata
        if l.oei in outputs:
            o = outputs[l.oei]

            # get the property values dictionary
            values = self.outputProperties.GetPropertyValues()

            # update the property values
            values['Variable Name'] = o['variable'].VariableNameCV()
            values['Unit Name'] = o['unit'].UnitName()
            values['Unit Type'] = o['unit'].UnitTypeCV()
            values['Unit Abbreviation'] = o['unit'].UnitAbbreviation()
            values['Variable Description'] = o['variable'].VariableDefinition()


            for k, v in values.iteritems():
                self.outputProperties.GetPropertyByLabel(k).SetValue(v)


    def populate_input_metadata(self,l):

        # get the link object
        # l = self.__links[self.__selected_link.name()]
        inputs = l.input_metadata
        if l.iei in inputs:
            i = inputs[l.iei]

            # get the property values dictionary
            values = self.inputProperties.GetPropertyValues()

            # update the property values
            values['Variable Name'] = i['variable'].VariableNameCV()
            values['Unit Name'] = i['unit'].UnitName()
            values['Unit Type'] = i['unit'].UnitTypeCV()
            values['Unit Abbreviation'] = i['unit'].UnitAbbreviation()
            values['Variable Description'] = i['variable'].VariableDefinition()


            for k, v in values.iteritems():
                self.inputProperties.GetPropertyByLabel(k).SetValue(v)

    def on_select_output(self, event):
        """
        sets the metadata for the selected output exchange item and populates a tree view
        """

        # get selected value
        output_name = self.OutputComboBox.GetValue()

        # get the current link
        l = self.__selected_link

        # get index of this link and then remove it from the links list
        link_idx = self.__links.index(l)
        self.__links.pop(link_idx)

        # change the link name to reflect output -> input
        l.oei = output_name
        l.refresh()

        # update the name in the links list
        self.__links.insert(link_idx, l)

        # refresh the link name box
        self.refreshLinkNameBox()

        # populate metadata
        self.populate_output_metadata(l)


    def on_select_input(self, event):
        """
        sets the metadata for the selected input exchange item and populates a tree view
        """

        # get selected value
        input_name = self.InputComboBox.GetValue()

       # get the current link
        l = self.__selected_link

        # get index of this link and then remove it from the links list
        link_idx = self.__links.index(l)
        self.__links.pop(link_idx)

        # change the link name to reflect output -> input
        l.iei = input_name
        l.refresh()

        # update the name in the links list
        self.__links.insert(link_idx, l)

        # refresh the link name box
        self.refreshLinkNameBox()

        # populate metadata
        self.populate_input_metadata(l)

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

        for l in self.__links:

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
        # set splitter location for the gridviews.  This needs to be done after the view is rendered
        self.inputProperties.SetSplitterPosition(130)
        self.outputProperties.SetSplitterPosition(130)

        links = engine.getLinksBtwnModels(self.output_component['id'], self.input_component['id'])
        if links:
            for l in links:
                link = LinkInfo(l['source_item'],
                                l['target_item'],
                                l['source_id'],
                                l['target_id'],
                                l['id'],
                                l['spatial_interpolation'],
                                l['temporal_interpolation'])

                self.__links.append(link)

            # select the first value
            self.refreshLinkNameBox()
            self.LinkNameListBox.SetSelection(0)
            self.__selected_link = self.__links[0]
            self.OnChange(None)

        # initialize the exchangeitem listboxes
        self.InputComboBox.SetItems(self.InputComboBoxChoices())
        self.OutputComboBox.SetItems(self.OutputComboBoxChoices())

        # if not links are found, need to deactivate controls
        self.activateControls(False)

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
        # self.name = self.generate_link_name(oei,iei,self.uid)
        self.oei = oei
        self.iei = iei
        self.source_id = source_id
        self.target_id = target_id
        self.spatial_interpolation =spatial_interpolation
        self.temporal_interpolation =  temporal_interpolation

        self.saved = False

        self.output_metadata = {}
        self.input_metadata = {}

        self.get_input_and_output_metadata()

    def refresh(self):

        self.get_input_and_output_metadata()


    def name(self):

        return  '%s -> %s [unique id = %s]'%(self.oei, self.iei, self.uid)

    def get_input_and_output_metadata(self):

        # get output information
        outputs = engine.getOutputExchangeItems(self.source_id)
        for output in outputs:
            self.output_metadata[output['name']] = output

        # get input information
        inputs = engine.getInputExchangeItems(self.target_id)
        for input in inputs:
            self.input_metadata[input['name']] = input

