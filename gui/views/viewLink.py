__author__ = 'mario'

import wx
import wx.xrc
import wx.dataview
from transform.time import *
from transform.space import *
import coordinator.engineAccessors as engine
import wx.propgrid as wxpg

class ViewLink(wx.Frame):
    def __init__(self, parent, output, input):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(700, 560), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER| wx.TAB_TRAVERSAL)

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
        # OUTPUT EXCHANGE ITEM - PROPERTY GRID VIEW
        ###########################################

        OutputSizer = wx.BoxSizer(wx.VERTICAL)

        OutChoice = self.OutputComboBoxChoices()
        self.OutputComboBox = wx.ComboBox(self.ExchangeItemSizer, wx.ID_ANY, OutChoice[0],
                                          wx.DefaultPosition, wx.Size(320, -1), OutChoice, 0)
        OutputSizer.Add(self.OutputComboBox, 0, wx.ALL, 5)


        self.outputProperties = wxpg.PropertyGridManager(self.ExchangeItemSizer, size=wx.Size(325, 130))
                                    # style= wxpg.PG_PROP_READONLY)

        p1 = self.outputProperties.AddPage('Output Exchange Item Metadata')

        self.outputProperties.Append( wxpg.PropertyCategory("Variable") )
        self.outputProperties.Append( wxpg.StringProperty("Variable Name",value='') )
        self.outputProperties.Append( wxpg.ArrayStringProperty("Variable Description",value='') )

        self.outputProperties.Append( wxpg.PropertyCategory("Unit") )
        self.outputProperties.Append( wxpg.StringProperty("Unit Name",value='') )
        self.outputProperties.Append( wxpg.StringProperty("Unit Type",value='') )
        self.outputProperties.Append( wxpg.StringProperty("Unit Abbreviation",value='') )

        OutputSizer.Add(self.outputProperties, 0, wx.ALL, 5)


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

        InChoice = self.InputComboBoxChoices()
        self.InputComboBox = wx.ComboBox(self.ExchangeItemSizer, wx.ID_ANY, InChoice[0],
                                         wx.DefaultPosition, wx.Size(320, -1), InChoice, 0)
        InputSizer.Add(self.InputComboBox, 0, wx.ALL, 5)

        self.inputProperties = wxpg.PropertyGridManager(self.ExchangeItemSizer, size=wx.Size(325, 130),
                                    style= wxpg.PG_PROP_READONLY|wxpg.PG_PROP_NOEDITOR)

        page = self.inputProperties.AddPage('Input Exchange Item Metadata')

        self.inputProperties.Append( wxpg.PropertyCategory("Variable") )
        self.inputProperties.Append( wxpg.StringProperty("Variable Name",value='') )
        self.inputProperties.Append( wxpg.ArrayStringProperty("Variable Description",value='') )

        self.inputProperties.Append( wxpg.PropertyCategory("Unit") )
        self.inputProperties.Append( wxpg.StringProperty("Unit Name",value='') )
        self.inputProperties.Append( wxpg.StringProperty("Unit Type",value='') )
        self.inputProperties.Append( wxpg.StringProperty("Unit Abbreviation",value='') )



        InputSizer.Add(self.inputProperties, 0, wx.ALL, 5)




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


