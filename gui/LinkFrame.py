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

###########################################################################
## Class LinkStartSizer
###########################################################################

class LinkStart ( wx.Frame ):

    def __init__( self, parent, input, output):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 550,525 ), style = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )

        # self.SetBackgroundColour(wx.BLACK)
        self.input = input
        self.output = output


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

        OutputComboBoxChoices = []
        self.OutputComboBox = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.Size( 250,35 ), OutputComboBoxChoices, 0 )
        OutputSizer.Add( self.OutputComboBox, 0, wx.ALL, 5 )

        self.Output_dataViewTreeCtrl1 = wx.dataview.DataViewTreeCtrl( self.ExchangeItemSizer, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,150 ), 0 )
        OutputSizer.Add( self.Output_dataViewTreeCtrl1, 0, wx.ALL, 5 )


        ExchangeItemSizer.Add( OutputSizer, 1, wx.EXPAND, 5 )

        InputSizer = wx.BoxSizer( wx.VERTICAL )

        InputComboBoxChoices = []
        self.InputComboBox = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.Size( 250,35 ), InputComboBoxChoices, 0 )
        InputSizer.Add( self.InputComboBox, 0, wx.ALL, 5 )

        self.Input_dataViewTreeCtrl2 = wx.dataview.DataViewTreeCtrl( self.ExchangeItemSizer, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,150 ), 0 )
        InputSizer.Add( self.Input_dataViewTreeCtrl2, 0, wx.ALL, 5 )

        ComboBoxTemporalChoices = []
        self.ComboBoxTemporal = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"No interpolation", wx.DefaultPosition, wx.Size( 300,30 ), ComboBoxTemporalChoices, 0 )
        InputSizer.Add( self.ComboBoxTemporal, 0, wx.ALL, 5 )

        ComboBoxSpatialChoices = []
        self.ComboBoxSpatial = wx.ComboBox( self.ExchangeItemSizer, wx.ID_ANY, u"No interpolation", wx.DefaultPosition, wx.Size( 300,30 ), ComboBoxSpatialChoices, 0 )
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

    def __del__( self ):
        pass


