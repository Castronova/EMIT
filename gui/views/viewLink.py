__author__ = 'mario'

import wx
import wx.xrc
import wx.dataview
import wx.grid
from transform.time import *
from transform.space import *
import coordinator.engineAccessors as engine
import wx.propgrid as wxpg
import sys

class ViewLink(wx.Frame):
    def __init__(self, parent, output, input):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(700, 600),
                          style=wx.DEFAULT_FRAME_STYLE
                          ^(wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))

        self.font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL)
        self.input_component = input
        self.output_component = output
        self.input_items = None
        self.output_items = None

        self.InitUI()

    def InitUI(self):
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.BoxSizer(wx.VERTICAL)

        self.LinkTitle_staticText = wx.StaticText(self, wx.ID_ANY, u"Select Add to Create a New Link", wx.Point(-1, -1),
                                                  wx.DefaultSize, 0)
        self.LinkTitle_staticText.Wrap(-1)
        FrameSizer.Add(self.LinkTitle_staticText, 0, wx.ALL, 5)

        FrameSizer.AddSpacer(( 0, 0), 1, wx.EXPAND, 5)

        self.LinkStartPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        LinkStartSizer = wx.BoxSizer(wx.HORIZONTAL)

        LinkNameListBoxChoices = []
        self.LinkNameListBox = wx.ListBox(self.LinkStartPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(575, 125),
                                          LinkNameListBoxChoices, 0)
        LinkStartSizer.Add(self.LinkNameListBox, 0, wx.ALL, 5)


        self.ButtonNew = wx.Button(self.LinkStartPanel, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, 0)
        ButtonSizer.Add(self.ButtonNew, 0, wx.ALL, 5)

        self.ButtonDelete = wx.Button(self.LinkStartPanel, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0)
        ButtonSizer.Add(self.ButtonDelete, 0, wx.ALL, 5)


        LinkStartSizer.Add(ButtonSizer, 1, wx.EXPAND, 5)

        self.LinkStartPanel.SetSizer(LinkStartSizer)
        self.LinkStartPanel.Layout()
        LinkStartSizer.Fit(self.LinkStartPanel)
        FrameSizer.Add(self.LinkStartPanel, 1, wx.EXPAND | wx.ALL, 5)

        self.ExchangeItemSizer = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        ExchangeItemSizer = wx.BoxSizer(wx.HORIZONTAL)


        ###########################################
        # OUTPUT EXCHANGE ITEM - GRID VIEW
        ###########################################

        OutputSizer = wx.BoxSizer(wx.VERTICAL)

        # OutChoice = self.OutputComboBoxChoices()
        # self.OutputComboBox = wx.ComboBox(self.ExchangeItemSizer, wx.ID_ANY, OutChoice[0],
        #                                   wx.DefaultPosition, wx.Size(320, -1), OutChoice, 0)

        self.OutputComboBox = wx.ComboBox(self.ExchangeItemSizer, wx.ID_ANY, '',
                                          wx.DefaultPosition, wx.Size(320, -1), [''], 0)

        OutputSizer.Add(self.OutputComboBox, 0, wx.ALL, 5)


        # self.outputProperties = wxpg.PropertyGridManager(self.ExchangeItemSizer, size=wx.Size(325, 130))
                                    # style= wxpg.PG_PROP_READONLY)
        # if sys.platform == 'linux2':
        #     self.outputProperties.SetFont(self.font)

        self.outputGrid = wx.grid.Grid( self.ExchangeItemSizer, wx.ID_ANY, wx.DefaultPosition, wx.Size(325,-1), 0 )

        # Grid
        self.outputGrid.CreateGrid( 7, 2 )
        self.outputGrid.EnableEditing( False )
        self.outputGrid.EnableGridLines( True )
        self.outputGrid.SetGridLineColour( wx.Colour( 0, 0, 0 ) )
        self.outputGrid.EnableDragGridSize( False )
        self.outputGrid.SetMargins( 0, 0 )

        # Columns
        self.outputGrid.EnableDragColMove( False )
        self.outputGrid.EnableDragColSize( True )
        self.outputGrid.SetColLabelSize( 0 )
        self.outputGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )


        # Rows
        self.outputGrid.EnableDragRowSize( True )
        self.outputGrid.SetRowLabelSize( 0 )
        self.outputGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )


        # Label Appearance

        # Cell Defaults
        self.outputGrid.SetDefaultCellBackgroundColour( wx.Colour(255,255,255) )
        self.outputGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        OutputSizer.Add(self.outputGrid, 0, wx.ALL, 5)

        # Set Cell Values
        self.outputGrid.SetCellValue(0,0, " Variable")
        self.outputGrid.SetCellValue(1,0, " Name")
        self.outputGrid.SetCellValue(2,0, " Description")
        self.outputGrid.SetCellValue(3,0, " Unit")
        self.outputGrid.SetCellValue(4,0, " Name")
        self.outputGrid.SetCellValue(5,0, " Type")
        self.outputGrid.SetCellValue(6,0, " Abbreviation")



        self.outputGrid.SetCellBackgroundColour(0,0,wx.Colour(195,195,195))
        self.outputGrid.SetCellBackgroundColour(0,1,wx.Colour(195,195,195))
        self.outputGrid.SetCellBackgroundColour(3,0,wx.Colour(195,195,195))
        self.outputGrid.SetCellBackgroundColour(3,1,wx.Colour(195,195,195))
        self.outputGrid.SetGridLineColour(wx.Colour(195,195,195))

        self.outputGrid.AutoSizeColumn(0)
        outputcolsize = self.outputGrid.GetColSize(0)
        C,R = self.outputGrid.GetSize()
        self.outputGrid.SetColSize(1,C-outputcolsize)

        ###########################################
        # SPATIAL AND TEMPORAL INTERPOLATION LABELS
        ###########################################

        self.Temporal_staticText = wx.StaticText(self.ExchangeItemSizer, wx.ID_ANY, u"Temporal Interpolation",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.Temporal_staticText.Wrap(-1)
        OutputSizer.Add(self.Temporal_staticText, 0, wx.ALL, 5)

        OutputSizer.AddSpacer((0, 12), 0, wx.EXPAND,
                              5)  # This is to make sure that the static text stays the same distance apart

        self.Spatial_staticText = wx.StaticText(self.ExchangeItemSizer, wx.ID_ANY, u"Spatial Interpolation",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.Spatial_staticText.Wrap(-1)
        OutputSizer.Add(self.Spatial_staticText, 0, wx.ALL, 5)

        ExchangeItemSizer.Add(OutputSizer, 1, wx.EXPAND, 5)



        ###########################################
        # INPUT EXCHANGE ITEM - PROPERTY GRID VIEW
        ###########################################

        InputSizer = wx.BoxSizer(wx.VERTICAL)

        # InChoice = self.InputComboBoxChoices()

        # self.InputComboBox = wx.ComboBox(self.ExchangeItemSizer, wx.ID_ANY, InChoice[0],
        #                                  wx.DefaultPosition, wx.Size(320, -1), InChoice, 0)

        self.InputComboBox = wx.ComboBox(self.ExchangeItemSizer, wx.ID_ANY, '',
                                         wx.DefaultPosition, wx.Size(320, -1), [''], 0)

        InputSizer.Add(self.InputComboBox, 0, wx.ALL, 5)

        self.inputGrid = wx.grid.Grid( self.ExchangeItemSizer, wx.ID_ANY, wx.DefaultPosition, wx.Size(325,-1), 0 )

        # Grid
        self.inputGrid.CreateGrid( 7, 2 )
        self.inputGrid.EnableEditing( False )
        self.inputGrid.EnableGridLines( True )
        self.inputGrid.SetGridLineColour( wx.Colour(255,255,255) )
        self.inputGrid.EnableDragGridSize( False )
        self.inputGrid.SetMargins( 0, 0 )

        # Columns
        self.inputGrid.EnableDragColMove( False )
        self.inputGrid.EnableDragColSize( True )
        self.inputGrid.SetColLabelSize( 0 )
        self.inputGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )


        # Rows
        self.inputGrid.EnableDragRowSize( True )
        self.inputGrid.SetRowLabelSize( 0 )
        self.inputGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )


        # Label Appearance

        # Cell Defaults
        self.inputGrid.SetDefaultCellBackgroundColour( wx.Colour(255,255,255) )
        self.inputGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        InputSizer.Add(self.inputGrid, 0, wx.ALL, 5)

        # Set Cell Values
        self.inputGrid.SetCellValue(0,0, " Variable")
        self.inputGrid.SetCellValue(1,0, " Name")
        self.inputGrid.SetCellValue(2,0, " Description")
        self.inputGrid.SetCellValue(3,0, " Unit")
        self.inputGrid.SetCellValue(4,0, " Name")
        self.inputGrid.SetCellValue(5,0, " Type")
        self.inputGrid.SetCellValue(6,0, " Abbreviation")



        self.inputGrid.SetCellBackgroundColour(0,0,wx.Colour(195,195,195))
        self.inputGrid.SetCellBackgroundColour(0,1,wx.Colour(195,195,195))
        self.inputGrid.SetCellBackgroundColour(3,0,wx.Colour(195,195,195))
        self.inputGrid.SetCellBackgroundColour(3,1,wx.Colour(195,195,195))
        self.inputGrid.SetGridLineColour(wx.Colour(195,195,195))

        self.inputGrid.AutoSizeColumn(0)
        inputcolsize = self.inputGrid.GetColSize(0)
        C,R = self.inputGrid.GetSize()
        self.inputGrid.SetColSize(1,C-inputcolsize)


        #####################################
        # SPATIAL AND TEMPORAL INTERPOLATIONS
        #####################################

        TemporalChoices = self.TemporalInterpolationChoices()  # Create the choices for the Temporal Interpolation Combobox
        self.ComboBoxTemporal = wx.ComboBox(self.ExchangeItemSizer, wx.ID_ANY, u"None Specified",
                                            wx.DefaultPosition, wx.Size(320, -1),
                                            TemporalChoices, 0)
        InputSizer.Add(self.ComboBoxTemporal, 0, wx.ALL, 5)

        SpatialChoices = self.SpatialInterpolationChoices()  # Create the choices for the Spatial Interpolation Combobox
        self.ComboBoxSpatial = wx.ComboBox(self.ExchangeItemSizer, wx.ID_ANY, u"None Specified",
                                           wx.DefaultPosition, wx.Size(320, -1),
                                           SpatialChoices, 0)
        InputSizer.Add(self.ComboBoxSpatial, 0, wx.ALL, 5)







        ExchangeItemSizer.Add(InputSizer, 1, wx.EXPAND, 5)

        self.ExchangeItemSizer.SetSizer(ExchangeItemSizer)
        self.ExchangeItemSizer.Layout()
        ExchangeItemSizer.Fit(self.ExchangeItemSizer)
        FrameSizer.Add(self.ExchangeItemSizer, 1, wx.EXPAND | wx.ALL, 5)

        self.BottomPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        ButtonSizerBottom = wx.BoxSizer(wx.HORIZONTAL)

        PlottingButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ButtonPlot = wx.Button(self.BottomPanel, wx.ID_ANY, u"SpatialPlot", wx.DefaultPosition, wx.DefaultSize, 0)
        PlottingButtonSizer.Add(self.ButtonPlot, 0, wx.ALL, 5)

        ButtonSizerBottom.Add(PlottingButtonSizer, 1, wx.EXPAND, 5)

        RightAlignSizer = wx.BoxSizer(wx.HORIZONTAL)

        RightAlignSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.ButtonSave = wx.Button(self.BottomPanel, wx.ID_ANY, u"Save and Close", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.ButtonSave.Disable()
        RightAlignSizer.Add(self.ButtonSave, 0, wx.ALL, 5)

        self.ButtonCancel = wx.Button(self.BottomPanel, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        RightAlignSizer.Add(self.ButtonCancel, 0, wx.ALL, 5)

        ButtonSizerBottom.Add(RightAlignSizer, 1, wx.EXPAND, 5)

        self.BottomPanel.SetSizer(ButtonSizerBottom)
        self.BottomPanel.Layout()
        ButtonSizerBottom.Fit(self.BottomPanel)
        FrameSizer.Add(self.BottomPanel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(FrameSizer)
        self.Layout()

        self.Centre(wx.BOTH)


    def OutputComboBoxChoices(self):
        self.output_items = engine.getOutputExchangeItems(self.output_component['id'])
        if self.output_items is not None:
            return [item['name'] for item in self.output_items]
        else:
            return [" "]

    def InputComboBoxChoices(self):
        self.input_items = engine.getInputExchangeItems(self.input_component['id'])
        if self.input_items is not None:
            return [item['name'] for item in self.input_items]
        else:
            return [' ']

    def TemporalInterpolationChoices(self):
        t = TemporalInterpolation()
        self.temporal_transformations = {i.name(): i for i in t.methods()}
        return ['None Specified'] + self.temporal_transformations.keys()

    def SpatialInterpolationChoices(self):
        s = SpatialInterpolation()
        self.spatial_transformations = {i.name(): i for i in s.methods()}
        return ['None Specified'] + self.spatial_transformations.keys()


