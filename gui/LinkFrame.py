__author__ = 'mario'

# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Feb 25 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview
from transform.time import *
from transform.space import *

###########################################################################
## Class LinkStartSizer
###########################################################################

class LinkStart ( wx.Frame ):

    def __init__( self, parent, output, input):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 550,525 ), style = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )

        # self.SetBackgroundColour(wx.BLACK)
        self.input = input
        self.output = output
        # self.InterpolationComboBoxChoices()
        self.InitUI()
        self.InitBindings()

    def InitUI(self):
        # Set the Top Panel:
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        FrameSizer = wx.BoxSizer( wx.VERTICAL )

        self.LinkStartPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        LinkStartSizer = wx.BoxSizer( wx.HORIZONTAL )

        LinkNameListBoxChoices = []
        self.LinkNameListBox = wx.ListBox( self.LinkStartPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 425,125 ), LinkNameListBoxChoices, 0 )
        LinkStartSizer.Add( self.LinkNameListBox, 0, wx.ALL, 5 )

        ButtonSizer = wx.BoxSizer( wx.VERTICAL )

        self.ButtonAdd = wx.Button( self.LinkStartPanel, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
        ButtonSizer.Add( self.ButtonAdd, 0, wx.ALL, 5 )

        self.ButtonDelete = wx.Button( self.LinkStartPanel, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        ButtonSizer.Add( self.ButtonDelete, 0, wx.ALL, 5 )

        self.ButtonOther = wx.Button( self.LinkStartPanel, wx.ID_ANY, u"Other", wx.DefaultPosition, wx.DefaultSize, 0 )
        ButtonSizer.Add( self.ButtonOther, 0, wx.ALL, 5 )


        LinkStartSizer.Add( ButtonSizer, 1, wx.EXPAND, 5 )


        self.LinkStartPanel.SetSizer( LinkStartSizer )
        self.LinkStartPanel.Layout()
        LinkStartSizer.Fit( self.LinkStartPanel )
        FrameSizer.Add( self.LinkStartPanel, 1, wx.EXPAND |wx.ALL, 5 )

        self.ExchangeItemSizer = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        ExchangeItemSizer = wx.BoxSizer( wx.HORIZONTAL )

        OutputSizer = wx.BoxSizer( wx.VERTICAL )

        # OutputComboBoxChoices = []
        self.OutputComboBox = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"Select Output Item",
                                           wx.DefaultPosition, wx.Size( 250,35 ), self.OutputComboBoxChoices(), 0 )
        OutputSizer.Add( self.OutputComboBox, 0, wx.ALL, 5 )

        self.OutputDataTreeCtrl = wx.dataview.DataViewTreeCtrl( self.ExchangeItemSizer, wx.ID_ANY,
                                                                      wx.DefaultPosition, wx.Size( 250,150 ), 0 )
        OutputSizer.Add( self.OutputDataTreeCtrl, 0, wx.ALL, 5 )

        self.temporal_label = wx.StaticText(self, label = 'Temporal Interpolation: ', pos = (20,280))
        self.spatial_label = wx.StaticText(self, label = 'Spatial Interpolation: ', pos = (20, 300))

        # OutputSizer.AddSpacer( ( 20, 100), 0, wx.EXPAND, 5 )
        # OutputSizer.Add(self.temporal_label)
        # OutputSizer.AddSpacer( ( 20, 10), 0, wx.EXPAND, 5 )
        # OutputSizer.Add(self.spatial_label)
        ExchangeItemSizer.Add( OutputSizer, 1, wx.EXPAND, 5 )

        InputSizer = wx.BoxSizer( wx.VERTICAL )

        # InputComboBoxChoices = []
        self.InputComboBox = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"Select Input Item",
                                          wx.DefaultPosition, wx.Size( 250,35 ), self.InputComboBoxChoices(), 0 )
        InputSizer.Add( self.InputComboBox, 0, wx.ALL, 5 )

        self.InputDataTreeCtrl = wx.dataview.DataViewTreeCtrl( self.ExchangeItemSizer, wx.ID_ANY,
                                                                     wx.DefaultPosition, wx.Size( 250,150 ), 0 )
        InputSizer.Add( self.InputDataTreeCtrl, 0, wx.ALL, 5 )

        # ComboBoxTemporalChoices = []
        TemporalChoices = self.TemporalInterpolationChoices()
        self.ComboBoxTemporal = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"No interpolation",
                                             wx.DefaultPosition, wx.Size( 300,30 ),
                                             self.TemporalInterpolationChoices(), 0 )
        InputSizer.Add( self.ComboBoxTemporal, 0, wx.ALL, 5 )

        # ComboBoxSpatialChoices = []
        self.ComboBoxSpatial = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"No interpolation",
                                            wx.DefaultPosition, wx.Size( 300,30 ),
                                            self.SpatialInterpolationChoices(), 0 )
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
        self.ButtonAdd.Bind(wx.EVT_BUTTON, self.GetName)
        self.ComboBoxTemporal.Bind(wx.EVT_COMBOBOX, self.on_select_temporal)
        self.ComboBoxTemporal.Bind(wx.EVT_COMBOBOX, self.on_select_spatial)
        self.ButtonClose.Bind(wx.EVT_BUTTON, self.OnClose)

    def GetName(self, event):
        dlg = NameDialog(self)
        dlg.ShowModal()
        # self.txt.SetValue(dlg.result)
        self.LinkNameListBox.Append(dlg.result)

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

    def OutputTreePopulation(self):
        self.OutputDataTreeCtrl.Append
        pass

    def InputTreePopulation(self):
        self.InputDataTreeCtrl
        pass

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

    def on_select_spatial(self, event):
        spatial_value = self.ComboboxSpatial.GetValue()
        self.spatial_interpolation = self.spatial_transformations[spatial_value]

    def on_select_temporal(self, event):
        temporal_value = self.ComboboxTemporal.GetValue()
        self.temporal_interpolation = self.temporal_transformations[temporal_value]

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
        pass



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