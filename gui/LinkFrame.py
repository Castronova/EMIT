__author__ = 'mario'

import wx
import wx.xrc
import wx.dataview
from transform.time import *
from transform.space import *

class LinkStart ( wx.Frame ):

    def __init__( self, parent, output, input, cmd):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 550,560 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        # self.SetBackgroundColour(wx.BLACK)
        self.input = input
        self.output = output
        self.cmd = cmd
        # self.InterpolationComboBoxChoices()
        self.InitUI()
        self.InitBindings()
        self.l = None
        self.OnStartUp()

    def InitUI(self):
        # Set the Top Panel:
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        FrameSizer = wx.BoxSizer( wx.VERTICAL )

        self.LinkTitle_staticText = wx.StaticText( self, wx.ID_ANY, u"Select Add to Create a New Link", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.LinkTitle_staticText.Wrap( -1 )
        FrameSizer.Add( self.LinkTitle_staticText, 0, wx.ALL, 5 )


        FrameSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.LinkStartPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        LinkStartSizer = wx.BoxSizer( wx.HORIZONTAL )

        LinkNameListBoxChoices = []
        self.LinkNameListBox = wx.ListBox( self.LinkStartPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 425,125 ), LinkNameListBoxChoices, 0 )
        LinkStartSizer.Add( self.LinkNameListBox, 0, wx.ALL, 5 )

        ButtonSizer = wx.BoxSizer( wx.VERTICAL )

        self.ButtonNew = wx.Button( self.LinkStartPanel, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, 0 )
        ButtonSizer.Add( self.ButtonNew, 0, wx.ALL, 5 )

        self.ButtonDelete = wx.Button( self.LinkStartPanel, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        ButtonSizer.Add( self.ButtonDelete, 0, wx.ALL, 5 )

        # self.ButtonOther = wx.Button( self.LinkStartPanel, wx.ID_ANY, u"Other", wx.DefaultPosition, wx.DefaultSize, 0 )
        # ButtonSizer.Add( self.ButtonOther, 0, wx.ALL, 5 )


        LinkStartSizer.Add( ButtonSizer, 1, wx.EXPAND, 5 )


        self.LinkStartPanel.SetSizer( LinkStartSizer )
        self.LinkStartPanel.Layout()
        LinkStartSizer.Fit( self.LinkStartPanel )
        FrameSizer.Add( self.LinkStartPanel, 1, wx.EXPAND |wx.ALL, 5 )

        self.ExchangeItemSizer = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        ExchangeItemSizer = wx.BoxSizer( wx.HORIZONTAL )

        OutputSizer = wx.BoxSizer( wx.VERTICAL )

        # OutputComboBoxChoices = []
        OutChoice = self.OutputComboBoxChoices()
        self.OutputComboBox = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, OutChoice[0],
                                           wx.DefaultPosition, wx.Size( 250,-1 ), OutChoice, 0 )
        OutputSizer.Add( self.OutputComboBox, 0, wx.ALL, 5 )

        self.OutputDataTreeCtrl = wx.dataview.DataViewTreeCtrl( self.ExchangeItemSizer, id=wx.ID_ANY,
                                                                      pos=wx.DefaultPosition, size=wx.Size( 250,150 ),
                                                                      style=wx.dataview.DV_NO_HEADER)
        OutputSizer.Add( self.OutputDataTreeCtrl, 0, wx.ALL, 5 )
        self.Temporal_staticText = wx.StaticText( self.ExchangeItemSizer, wx.ID_ANY, u"Temporal Interpolation", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Temporal_staticText.Wrap( -1 )
        OutputSizer.Add( self.Temporal_staticText, 0, wx.ALL, 5 )

        OutputSizer.AddSpacer( (0,12), 0, wx.EXPAND, 5) # This is to make sure that the static text stays the same distance apart

        self.Spatial_staticText = wx.StaticText( self.ExchangeItemSizer, wx.ID_ANY, u"Spatial Interpolation", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Spatial_staticText.Wrap( -1 )
        OutputSizer.Add( self.Spatial_staticText, 0, wx.ALL, 5 )


        ExchangeItemSizer.Add( OutputSizer, 1, wx.EXPAND, 5 )

        InputSizer = wx.BoxSizer( wx.VERTICAL )

        InChoice = self.InputComboBoxChoices()
        self.InputComboBox = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, InChoice[0],
                                          wx.DefaultPosition, wx.Size( 250,-1 ), InChoice, 0 )
        InputSizer.Add( self.InputComboBox, 0, wx.ALL, 5 )

        self.InputDataTreeCtrl = wx.dataview.DataViewTreeCtrl( self.ExchangeItemSizer, id=wx.ID_ANY,
                                                                      pos=wx.DefaultPosition, size=wx.Size( 250,150 ),
                                                                      style=wx.dataview.DV_NO_HEADER )
        InputSizer.Add( self.InputDataTreeCtrl, 0, wx.ALL, 5 )

        TemporalChoices = self.TemporalInterpolationChoices() #Create the choices for the Temporal Interpolation Combobox
        self.ComboBoxTemporal = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"No interpolation",
                                             wx.DefaultPosition, wx.Size( 300,-1 ),
                                             TemporalChoices, 0 )
        InputSizer.Add( self.ComboBoxTemporal, 0, wx.ALL, 5 )

        SpatialChoices = self.SpatialInterpolationChoices() #Create the choices for the Spatial Interpolation Combobox
        self.ComboBoxSpatial = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"No interpolation",
                                            wx.DefaultPosition, wx.Size( 300,-1 ),
                                            SpatialChoices, 0 )
        InputSizer.Add( self.ComboBoxSpatial, 0, wx.ALL, 5 )

        ExchangeItemSizer.Add( InputSizer, 1, wx.EXPAND, 5 )


        self.ExchangeItemSizer.SetSizer( ExchangeItemSizer )
        self.ExchangeItemSizer.Layout()
        ExchangeItemSizer.Fit( self.ExchangeItemSizer )
        FrameSizer.Add( self.ExchangeItemSizer, 1, wx.EXPAND |wx.ALL, 5 )

        self.BottomPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        ButtonSizerBottom = wx.BoxSizer( wx.HORIZONTAL )

        PlottingButtonSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.ButtonPlot = wx.Button( self.BottomPanel, wx.ID_ANY, u"SpatialPlot", wx.DefaultPosition, wx.DefaultSize, 0 )
        PlottingButtonSizer.Add( self.ButtonPlot, 0, wx.ALL, 5 )


        ButtonSizerBottom.Add( PlottingButtonSizer, 1, wx.EXPAND, 5 )

        RightAlignSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.ButtonSave = wx.Button( self.BottomPanel, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
        RightAlignSizer.Add( self.ButtonSave, 0, wx.ALL, 5 )

        self.ButtonClose = wx.Button( self.BottomPanel, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        RightAlignSizer.Add( self.ButtonClose, 0, wx.ALL, 5 )


        ButtonSizerBottom.Add( RightAlignSizer, 1, wx.EXPAND, 5 )


        self.BottomPanel.SetSizer( ButtonSizerBottom )
        self.BottomPanel.Layout()
        ButtonSizerBottom.Fit( self.BottomPanel )
        FrameSizer.Add( self.BottomPanel, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( FrameSizer )
        self.Layout()

        self.Centre( wx.BOTH )

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

        rmlink = self.cmd.remove_link_all()
        all = self.listbox.GetSelections()

        try:
            for i in range(0,stop=None, step=1):
                self.listbox.Delete(i)
        except:
            pass

        sel = self.listbox.GetSelection()
        if sel != -1:
            self.listbox.Delete(sel)

    def OutputComboBoxChoices(self):
        OutputExchangeItemsList = [self.output.get_output_exchange_items()[i]._ExchangeItem__name for i in range(0, len(self.output.get_output_exchange_items()))]
        return OutputExchangeItemsList

    def InputComboBoxChoices(self):
        InputExchangeItemsList = [self.input.get_input_exchange_items()[i]._ExchangeItem__name for i in range(0, len(self.input.get_input_exchange_items()))]
        return InputExchangeItemsList

    def InterpolationComboBoxChoices(self):
        # populate spatial and temporal interpolations
        t = TemporalInterpolation()
        self.temporal_transformations = {i.name():i for i in t.methods()}
        self.ComboboxTemporalChoices = self.temporal_transformations.keys()

        s = SpatialInterpolation()
        self.spatial_transformations = {i.name():i for i in s.methods()}
        self.ComboboxSpatialChoices = self.spatial_transformations.keys()

    def TemporalInterpolationChoices(self):
        t = TemporalInterpolation()
        self.temporal_transformations = {i.name():i for i in t.methods()}
        return self.temporal_transformations.keys()

    def SpatialInterpolationChoices(self):
        s = SpatialInterpolation()
        self.spatial_transformations = {i.name():i for i in s.methods()}
        return self.spatial_transformations.keys()

    def on_select_output(self, event):
        output_value = self.OutputComboBox.GetValue()
        self.OutputDataTreeCtrl.DeleteAllItems()

        self.output_selected = self.output.get_output_exchange_item_by_name(output_value)
        self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.output_selected._ExchangeItem__name)
        self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.output_selected._ExchangeItem__description)
        # self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.output_selected._ExchangeItem__geoms)
        self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.output_selected._ExchangeItem__type)
        self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.output_selected._ExchangeItem__unit._Unit__unitName)
        # self.OutputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.output_selected._ExchangeItem__variable._Variable__variableNameCV)

    def on_select_input(self, event):
        input_value = self.InputComboBox.GetValue()
        self.input_selected = self.input.get_input_exchange_item_by_name(input_value)
        self.InputDataTreeCtrl.DeleteAllItems()

        self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.input_selected._ExchangeItem__name)
        self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.input_selected._ExchangeItem__description)
        # self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.input_selected._ExchangeItem__geoms)
        self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.input_selected._ExchangeItem__type)
        self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.input_selected._ExchangeItem__unit._Unit__unitName)
        # self.InputDataTreeCtrl.AppendContainer(wx.dataview.NullDataViewItem, self.input_selected._ExchangeItem__variable._Variable__variableNameCV)

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
        # if dial =='Yes':
        #     self.Close()

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

    def __del__( self ):
        pass


class NameDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Enter Name!"):
        wx.Dialog.__init__(self, parent, id, title, size=(400, 150))

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.label = wx.StaticText(self, label="Enter the Name of your Link:")
        self.field = wx.TextCtrl(self, value="", size=(300, 20))
        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)

        self.mainSizer.Add(self.label, 0, wx.ALL, 8 )
        self.mainSizer.Add(self.field, 0, wx.ALL, 8 )

        self.buttonSizer.Add(self.okbutton, 0, wx.ALL, 8 )

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