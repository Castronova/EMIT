__author__ = 'mario'

import wx
import wx.xrc
import wx.dataview
from transform.time import *
from transform.space import *
import coordinator.engineAccessors as engine
import wx.propgrid as wxpg
import sys

class ViewLink(wx.Frame):
    def __init__(self, parent, output, input):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          # size=wx.Size(700, 560),
                          size=wx.Size(1000, 1000),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER| wx.TAB_TRAVERSAL)

        self.font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL)
        self.input_component = input
        self.output_component = output
        self.input_items = None
        self.output_items = None

        self.InitUI()
        # vs = self.GetBestSize()
        # self.SetSize(vs)

    def InitUI(self):

        # add some descriptive text at the top of the window
        self.LinkTitle_staticText = wx.StaticText(self, wx.ID_ANY, u"Select Add to Create a New Link", wx.Point(-1, -1),wx.DefaultSize, 0)
        self.LinkTitle_staticText.Wrap(-1)

        ####################################
        # CREATE PANELS TO HOLD UI ELEMENTS
        ####################################

        self.topPanel = wx.Panel(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)
        self.middlePanel = wx.Panel(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)
        self.bottomPanel = wx.Panel(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)

        #####################
        # TOP PANEL ELEMENTS
        #####################

        # create link list box; new and delete buttons
        self.LinkNameListBox = wx.ListBox(self.topPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(575, 125),[], 0)
        self.ButtonNew = wx.Button(self.topPanel, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, 0)
        self.ButtonDelete = wx.Button(self.topPanel, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0)

        ########################
        # MIDDLE PANEL ELEMENTS
        ########################

        # OUTPUT EXCHANGE ITEM - PROPERTY GRID VIEW
        self.OutputComboBox = wx.ComboBox(self.middlePanel, wx.ID_ANY, '',
                                          wx.DefaultPosition, wx.Size(320, -1), [''], 0)

        self.outputProperties = wxpg.PropertyGridManager(self.middlePanel, size=wx.Size(325, 130))
                                    # style= wxpg.PG_PROP_READONLY)
        # if sys.platform == 'linux2':
        #     self.outputProperties.SetFont(self.font)

        p1 = self.outputProperties.AddPage('Output Exchange Item Metadata')

        self.outputProperties.Append( wxpg.PropertyCategory("Variable") )
        self.outputProperties.Append( wxpg.StringProperty("Variable Name",value='') )
        self.outputProperties.Append( wxpg.ArrayStringProperty("Variable Description",value='') )

        self.outputProperties.Append( wxpg.PropertyCategory("Unit") )
        self.outputProperties.Append( wxpg.StringProperty("Unit Name",value='') )
        self.outputProperties.Append( wxpg.StringProperty("Unit Type",value='') )
        self.outputProperties.Append( wxpg.StringProperty("Unit Abbreviation",value='') )

        # adjust the properties box size to the ideal size
        x,y = self.outputProperties.GetBestVirtualSize()
        self.outputProperties.Layout()
        self.outputProperties.MinSize = (wx.Size(325,y-20))         # Need to set the minimum size b/c that is what the sizer uses



        # INPUT EXCHANGE ITEM - PROPERTY GRID VIEW
        self.InputComboBox = wx.ComboBox(self.middlePanel, wx.ID_ANY, '',
                                         wx.DefaultPosition, wx.Size(320, -1), [''], 0)

        self.inputProperties = wxpg.PropertyGridManager(self.middlePanel, size=wx.Size(325, 130))
                                    # style= wxpg.PG_PROP_READONLY|wxpg.PG_PROP_NOEDITOR)
        # if sys.platform == 'linux2':
        #     self.inputProperties.SetFont(self.font)

        page = self.inputProperties.AddPage('Input Exchange Item Metadata')

        self.inputProperties.Append( wxpg.PropertyCategory("Variable") )
        self.inputProperties.Append( wxpg.StringProperty("Variable Name",value='') )
        self.inputProperties.Append( wxpg.ArrayStringProperty("Variable Description",value='') )

        self.inputProperties.Append( wxpg.PropertyCategory("Unit") )
        self.inputProperties.Append( wxpg.StringProperty("Unit Name",value='') )
        self.inputProperties.Append( wxpg.StringProperty("Unit Type",value='') )
        self.inputProperties.Append( wxpg.StringProperty("Unit Abbreviation",value='') )

        # adjust the properties box size to the ideal size
        x,y = self.inputProperties.GetBestVirtualSize()
        self.inputProperties.Layout()
        self.inputProperties.MinSize = (wx.Size(325,y-20))  # Need to set the minimum size b/c that is what the sizer uses




        # SPATIAL AND TEMPORAL INTERPOLATIONS
        TemporalChoices = self.TemporalInterpolationChoices()  # Create the choices for the Temporal Interpolation Combobox
        self.ComboBoxTemporal = wx.ComboBox(self.middlePanel, wx.ID_ANY, u"None Specified",
                                            wx.DefaultPosition, wx.Size(320, -1),
                                            TemporalChoices, 0)


        SpatialChoices = self.SpatialInterpolationChoices()  # Create the choices for the Spatial Interpolation Combobox
        self.ComboBoxSpatial = wx.ComboBox(self.middlePanel, wx.ID_ANY, u"None Specified",
                                           wx.DefaultPosition, wx.Size(320, -1),
                                           SpatialChoices, 0)


        self.Temporal_staticText = wx.StaticText(self.middlePanel, wx.ID_ANY, u"Temporal Interpolation",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.Temporal_staticText.Wrap(-1)


        self.Spatial_staticText = wx.StaticText(self.middlePanel, wx.ID_ANY, u"Spatial Interpolation",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.Spatial_staticText.Wrap(-1)


        ########################
        # BOTTOM PANEL ELEMENTS
        ########################

        # PLOT, SAVE, CANCEL BUTTONS
        self.ButtonPlot = wx.Button(self.bottomPanel, wx.ID_ANY, u"SpatialPlot", wx.DefaultPosition, wx.DefaultSize, 0)
        self.ButtonSave = wx.Button(self.bottomPanel, wx.ID_ANY, u"Save and Close", wx.DefaultPosition, wx.DefaultSize, 0)
        self.ButtonCancel = wx.Button(self.bottomPanel, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)


        ###############
        # BUILD SIZERS
        ###############
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.BoxSizer(wx.VERTICAL)

        FrameSizer.Add(self.LinkTitle_staticText, 0, wx.ALL, 5)
        FrameSizer.AddSpacer(( 0, 0), 1, wx.EXPAND, 5)

        LinkStartSizer = wx.BoxSizer(wx.HORIZONTAL)
        LinkStartSizer.Add(self.LinkNameListBox, 0, wx.ALL, 5)

        ButtonSizer.Add(self.ButtonNew, 0, wx.ALL, 5)
        ButtonSizer.Add(self.ButtonDelete, 0, wx.ALL, 5)

        LinkStartSizer.Add(ButtonSizer, 1, wx.EXPAND, 5)

        self.topPanel.SetSizer(LinkStartSizer)
        self.topPanel.Layout()
        LinkStartSizer.Fit(self.topPanel)
        FrameSizer.Add(self.topPanel, 1, wx.EXPAND | wx.ALL, 5)


        ExchangeItemSizer = wx.BoxSizer(wx.HORIZONTAL)


        OutputSizer = wx.BoxSizer(wx.VERTICAL)
        OutputSizer.Add(self.OutputComboBox, 0, wx.ALL, 5)
        OutputSizer.Add(self.outputProperties, 0, wx.ALL, 5)

        OutputSizer.Add(self.Temporal_staticText, 0, wx.ALL, 5)

        OutputSizer.AddSpacer((0, 12), 0, wx.EXPAND,
                              5)  # This is to make sure that the static text stays the same distance apart

        OutputSizer.Add(self.Spatial_staticText, 0, wx.ALL, 5)

        ExchangeItemSizer.Add(OutputSizer, 1, wx.EXPAND, 5)

        InputSizer = wx.BoxSizer(wx.VERTICAL)
        InputSizer.Add(self.InputComboBox, 0, wx.ALL, 5)
        InputSizer.Add(self.inputProperties, 0, wx.ALL, 5)
        InputSizer.Add(self.ComboBoxTemporal, 0, wx.ALL, 5)
        InputSizer.Add(self.ComboBoxSpatial, 0, wx.ALL, 5)


        ExchangeItemSizer.Add(InputSizer, 1, wx.EXPAND, 5)

        self.middlePanel.SetSizer(ExchangeItemSizer)
        self.middlePanel.Layout()
        ExchangeItemSizer.Fit(self.middlePanel)
        FrameSizer.Add(self.middlePanel, 1, wx.EXPAND | wx.ALL, 5)


        PlottingButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        PlottingButtonSizer.Add(self.ButtonPlot, 0, wx.ALL, 5)
        ButtonSizerBottom = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizerBottom.Add(PlottingButtonSizer, 1, wx.EXPAND, 5)

        RightAlignSizer = wx.BoxSizer(wx.HORIZONTAL)
        RightAlignSizer.Add(self.ButtonSave, 0, wx.ALL, 5)
        RightAlignSizer.Add(self.ButtonCancel, 0, wx.ALL, 5)

        ButtonSizerBottom.Add(RightAlignSizer, 1, wx.EXPAND, 5)

        self.bottomPanel.SetSizer(ButtonSizerBottom)
        self.bottomPanel.Layout()
        ButtonSizerBottom.Fit(self.bottomPanel)
        FrameSizer.Add(self.bottomPanel, 1, wx.EXPAND | wx.ALL, 5)

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


