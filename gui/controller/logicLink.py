__author__ = 'tonycastronova'

import uuid

import wx
import wx.lib.newevent as ne
import wx.grid as gridlib

from gui.views.viewLink import ViewLink
import coordinator.engineAccessors as engine
from gui.controller.logicSpatialPlot import LogicSpatialPlot
# from gui.views.viewLinkSpatialPlot import ViewLinkSpatialPlot
from coordinator.emitLogging import elog

LinkUpdatedEvent, EVT_LINKUPDATED = ne.NewEvent()


class LogicLink(ViewLink):

    odesc = ""
    idesc = ""
    def __init__(self, parent, outputs, inputs):

        ViewLink.__init__(self, parent, outputs, inputs)

        # self.l = None
        self.parent = parent

        # class link variables used to save link
        self.__selected_link = None

        self.__link_source_id = self.output_component['id']
        self.__link_target_id = self.input_component['id']
        self.__link_ids = {}
        self.__links = []
        self.link_obj_hit = False

        self.OnStartUp()
        self.InitBindings()

        self.__checkbox_states = [None,None]


    def InitBindings(self):
        self.LinkNameListBox.Bind(wx.EVT_LISTBOX, self.OnChange)
        self.LinkNameListBox.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

        self.ButtonNew.Bind(wx.EVT_BUTTON, self.OnSave)
        self.ButtonNew.Bind(wx.EVT_BUTTON, self.NewButton)
        self.ButtonDelete.Bind(wx.EVT_BUTTON, self.OnDelete)
        self.ButtonCancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.ButtonSave.Bind(wx.EVT_BUTTON, self.OnSave)
        self.ButtonPlot.Bind(wx.EVT_BUTTON, self.OnPlot)
        self.Bind(EVT_LINKUPDATED, self.linkSelected)
        self.Bind(wx.EVT_CLOSE, self.OnCancel)
        self.outputGrid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OutputGridHover)
        self.inputGrid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.InputGridHover)

        self.OutputComboBox.Bind(wx.EVT_COMBOBOX, self.on_select_output)
        self.InputComboBox.Bind(wx.EVT_COMBOBOX, self.on_select_input)
        self.ComboBoxTemporal.Bind(wx.EVT_COMBOBOX, self.on_select_temporal)
        self.ComboBoxSpatial.Bind(wx.EVT_COMBOBOX, self.on_select_spatial)


    def OnPlot(self, event):
        '''__init__(self, Window parent, int id=-1, String title=EmptyString,
            Point pos=DefaultPosition, Size size=DefaultSize,
            long style=DEFAULT_FRAME_STYLE, String name=FrameNameStr) -> Frame'''

        title = self.__selected_link.name()
        plot_window = wx.Frame(self.parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=wx.Size(625, 625))

        # create a spatial plot instance
        plot_panel = LogicSpatialPlot(plot_window)

        # get the source and target ids from the link object
        source_model_id = self.__selected_link.source_id
        target_model_id = self.__selected_link.target_id

        # get the input geometries
        oei = engine.getOutputExchangeItems(source_model_id)
        ogeoms = {}
        for o in oei:
            name = o['name']
            geoms = [i['shape'] for i in o['geom']]
            ogeoms[name] = geoms

        # get the output geometries
        igeoms = {}
        iei = engine.getInputExchangeItems(target_model_id)
        for i in iei:
            name = i['name']
            geoms = [j['shape'] for j in o['geom']]
            igeoms[name] = geoms

        # set input and output geometries
        plot_panel.set_input_data(value=igeoms)
        plot_panel.set_output_data(value=ogeoms)

        # add some selection
        textLabel = wx.StaticText(plot_window, wx.ID_ANY, label='Toggle the Input and Output exchange element sets: ')
        textLabel.SetFont( wx.Font( 14, 70, 90, 92, False, wx.EmptyString ) )
        inputSelection = wx.CheckBox(plot_window, 998,label='Input Exchange Item: '+self.__selected_link.iei)
        outputSelection = wx.CheckBox(plot_window, 999,label='Output Exchange Item: '+self.__selected_link.oei)
        self.__checkbox_states = [self.__selected_link.iei, self.__selected_link.oei]  # initialize checkbox state

        def checked(event):
            chk = event.Checked()

            # make changes if selection is false
            if event.Id == 998:
                if chk: self.__checkbox_states[0] = self.__selected_link.iei
                else:   self.__checkbox_states[0] = None
            if event.Id == 999:
                if chk: self.__checkbox_states[1] = self.__selected_link.oei
                else:   self.__checkbox_states[1] = None

            # set the selected datasets in the controller
            plot_panel.set_selection_input(self.__checkbox_states[0])
            plot_panel.set_selection_output(self.__checkbox_states[1])

            # update the plot
            plot_panel.UpdatePlot()

        # add some handlers
        inputSelection.Bind(wx.EVT_CHECKBOX, checked)
        outputSelection.Bind(wx.EVT_CHECKBOX, checked)

        # set the initial state of the input and output selectors
        inputSelection.SetValue(True)
        outputSelection.SetValue(True)
        plot_panel.set_selection_input(self.__selected_link.iei)
        plot_panel.set_selection_output(self.__selected_link.oei)
        plot_panel.UpdatePlot()  # update the plot to reflect the input/output selection

        # add controls to frame
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        plotSizer = wx.BoxSizer(wx.VERTICAL)
        SelectionSizer= wx.BoxSizer(wx.VERTICAL)

        # nest sizers to pad bothe the top and left borders
        b = wx.BoxSizer(wx.VERTICAL)
        b.Add(textLabel, flag=wx.LEFT, border=20 )
        SelectionSizer.AddSizer(b, flag=wx.BOTTOM, border=10)
        SelectionSizer.Add(outputSelection, flag=wx.LEFT, border=20)
        SelectionSizer.Add(inputSelection, flag=wx.LEFT, border=20)
        plotSizer.Add(plot_panel)

        # add elements back to mainSizer
        mainSizer.Add(plotSizer)
        mainSizer.Add(SelectionSizer)
        plot_window.SetSizer(mainSizer)

        plot_window.Layout()
        plot_window.Show()

    def OnLeftUp(self, event):

        if not self.link_obj_hit:
            link_name = self.__selected_link.name()

            selected_index = self.LinkNameListBox.Items.index(link_name)
            self.LinkNameListBox.SetSelection(selected_index)

        # reset the state of link_obj_hit
        self.link_obj_hit = False

    def getLinkByName(self, name):
        for l in self.__links:
            if l.name() == name:
                return l
        return None

    def OnChange(self, event):
        link_name = self.LinkNameListBox.GetStringSelection()

        # get the selected link
        l = self.getLinkByName(link_name)

        # set the currently selected link
        self.__selected_link = l

        # update the combobox selections
        self.OutputComboBox.SetStringSelection(l.oei)
        self.InputComboBox.SetStringSelection(l.iei)

        if l.temporal_interpolation is not None:
            self.ComboBoxTemporal.SetStringSelection(l.temporal_interpolation)
        else:
            # set default value
            self.ComboBoxTemporal.SetSelection(0)

        if l.spatial_interpolation is not None:
            self.ComboBoxSpatial.SetStringSelection(l.spatial_interpolation)
        else:
            # set default value
            self.ComboBoxSpatial.SetSelection(0)

        # set the state of link_obj_hit
        self.link_obj_hit = True

        wx.PostEvent(self, LinkUpdatedEvent())

    def linkSelected(self, event):

        # get the selected link object
        selected = self.LinkNameListBox.GetStringSelection()
        known_link_ids = [l.name() for l in self.__links]
        if selected in known_link_ids:
            l = self.__links[known_link_ids.index(selected)]
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
            self.InputComboBox.Enable()
            self.OutputComboBox.Enable()
            self.ButtonPlot.Enable()
        else:
            self.ButtonSave.Disable()
            self.ComboBoxSpatial.Disable()
            self.ComboBoxTemporal.Disable()
            self.InputComboBox.Disable()
            self.OutputComboBox.Disable()
            self.ButtonPlot.Disable()

    def refreshLinkNameBox(self):

        self.LinkNameListBox.Clear()
        for l in self.__links:
            self.LinkNameListBox.Append(l.name())

    def NewButton(self, event):

        # set the exchange item values
        self.InputComboBox.SetSelection(0)
        self.OutputComboBox.SetSelection(0)

        # generate a unique name for this link
        oei = self.OutputComboBox.GetValue()
        iei = self.InputComboBox.GetValue()

        # create a link object and save it at the class level
        l = LinkInfo(oei, iei, self.__link_source_id, self.__link_target_id)
        self.__links.append(l)

        # add the link name to the links list box
        self.refreshLinkNameBox()

        # set the currently selected link
        self.__selected_link = l

        # select the last value
        self.LinkNameListBox.SetSelection(self.LinkNameListBox.GetCount() - 1)

        self.OnChange(None)

    # def GetName(self, event):
    # dlg = NameDialog(self)
    #     dlg.ShowModal()
    #     self.LinkNameListBox.Append(str(dlg.result))

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
            elog.error('ERROR|Could not remove link')
            return

        # remove the link name from the links list box
        index = self.LinkNameListBox.GetSelection()
        self.LinkNameListBox.Delete(index)

        # remove link from __links list so that it isn't repopulated on page refresh
        self.__links.pop(index)

    def populate_output_metadata(self, l):

        # get the link object
        outputs = l.output_metadata
        if l.oei in outputs:
            o = outputs[l.oei]

            self.outputGrid.SetCellValue(1, 1, o['variable'].VariableNameCV())
            self.outputGrid.SetCellValue(2, 1, o['variable'].VariableDefinition())
            self.odesc = o['variable'].VariableDefinition()

            self.outputGrid.SetCellValue(4, 1, o['unit'].UnitName())
            self.outputGrid.SetCellValue(5, 1, o['unit'].UnitTypeCV())
            self.outputGrid.SetCellValue(6, 1, o['unit'].UnitAbbreviation())

    def populate_input_metadata(self, l):

        # get the link object
        inputs = l.input_metadata
        if l.iei in inputs:
            i = inputs[l.iei]

            self.inputGrid.SetCellValue(1, 1, i['variable'].VariableNameCV())
            self.inputGrid.SetCellValue(2, 1, i['variable'].VariableDefinition())
            self.idesc = i['variable'].VariableDefinition()

            self.inputGrid.SetCellValue(4, 1, i['unit'].UnitName())
            self.inputGrid.SetCellValue(5, 1, i['unit'].UnitTypeCV())
            self.inputGrid.SetCellValue(6, 1, i['unit'].UnitAbbreviation())

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
        # get the current link
        l = self.__selected_link

        spatial_value = self.ComboBoxSpatial.GetValue()
        if spatial_value == 'None Specified':
            l.spatial_interpolation = None
        else:
            l.spatial_interpolation = self.spatial_transformations[spatial_value]

    def on_select_temporal(self, event):
        # get the current link
        l = self.__selected_link

        temporal_value = self.ComboBoxTemporal.GetValue()
        if temporal_value == 'None Specified':
            l.temporal_interpolation = None
        else:
            l.temporal_interpolation = self.temporal_transformations[temporal_value]

    def OnCancel(self, event):

        dial = wx.MessageDialog(self, 'Are you sure that you want to close without saving?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.Destroy()

    def OnSave(self, event):
        """
        Saves all link objects to the engine and then closes the link creation window
        """

        warnings = []
        errors = []
        for l in self.__links:

            if l.iei == '---' or l.oei == '--':
                warnings.append(l)
            else:

                try:
                    kwargs = dict(source_id=l.source_id,
                                  source_item=l.oei,
                                  target_id=l.target_id,
                                  target_item=l.iei,
                                  spatial_interpolation=l.spatial_interpolation,
                                  temporal_interpolation=l.temporal_interpolation,
                                  uid=l.uid)

                    # remove the existing link, if there is one
                    engine.removeLinkById(l.uid)

                    # add a new link inside the engine
                    linkid = engine.addLink(**kwargs)

                    if linkid:
                        l.saved = True

                    wx.PostEvent(self, LinkUpdatedEvent())
                except:
                    elog.error('ERROR|Could not save link: %s' % l.name)
                    errors.append(l)

        if len(warnings) > 0:
            warning_links = '\n'.join(l.name() for l in warnings)
            warning = wx.MessageDialog(self,
                                       "Could not save the following links because they lacking either input or output items: \n\n " + warning_links + "\n\n Would you like to discard these partial link objects?",
                                       'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)

            if warning.ShowModal() == wx.ID_YES:
                self.Destroy()
            else:
                return

        self.Destroy()

    def OnStartUp(self):
        # set splitter location for the gridviews.  This needs to be done after the view is rendered
        # self.inputProperties.SetSplitterPosition(130)
        # self.outputProperties.SetSplitterPosition(130)

        # initialize the exchangeitem listboxes
        self.InputComboBox.SetItems(['---'] + self.InputComboBoxChoices())
        self.OutputComboBox.SetItems(['---'] + self.OutputComboBoxChoices())
        self.InputComboBox.SetSelection(0)
        self.OutputComboBox.SetSelection(0)

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

        # if no links are found, need to deactivate controls
        self.activateControls(False)

    def OutputGridHover(self, e):
        self.OutGridToolTip(e)

    def InputGridHover(self, e):
        self.InGridToolTip(e)

    def OutGridToolTip(self, e):
        if e.GetRow() == 2 and e.GetCol() == 1:
            self.outputGrid.SetToolTip(wx.ToolTip(self.odesc))
        else:
            self.outputGrid.SetToolTip(wx.ToolTip(""))
        e.Skip()

    def InGridToolTip(self, e):
        if e.GetRow() == 2 and e.GetCol() == 1:
            self.inputGrid.SetToolTip(wx.ToolTip(self.idesc))
        else:
            self.inputGrid.SetToolTip(wx.ToolTip(""))
        e.Skip()


class LinkInfo():
    def __init__(self, oei, iei, source_id, target_id, uid=None, spatial_interpolation=None,
                 temporal_interpolation=None):


        self.uid = 'L' + uuid.uuid4().hex[:5] if uid is None else uid
        # self.name = self.generate_link_name(oei,iei,self.uid)
        self.oei = oei
        self.iei = iei
        self.source_id = source_id
        self.target_id = target_id
        self.spatial_interpolation = spatial_interpolation
        self.temporal_interpolation = temporal_interpolation

        self.saved = False

        self.output_metadata = {}
        self.input_metadata = {}

        self.get_input_and_output_metadata()

    def refresh(self):

        self.get_input_and_output_metadata()


    def name(self):
        iei_name = self.iei if self.iei != '---' else '?'
        oei_name = self.oei if self.oei != '---' else '?'

        if iei_name == '?' and oei_name == '?':
            return '%s' % self.uid
        else:
            return '%s | %s -> %s ' % (self.uid, oei_name, iei_name)

    def get_input_and_output_metadata(self):

        # get output information
        outputs = engine.getOutputExchangeItems(self.source_id)
        for output in outputs:
            self.output_metadata[output['name']] = output

        # get input information
        inputs = engine.getInputExchangeItems(self.target_id)
        for input in inputs:
            self.input_metadata[input['name']] = input

