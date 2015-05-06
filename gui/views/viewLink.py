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
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL)
        self.input_component = input
        self.output_component = output
        self.input_items = None
        self.output_items = None

        self.CheckOS()

        self.InitUI()
        # vs = self.GetBestSize()
        # self.SetSize(vs)

        # print self.ClientSize

        # self.MinClientSize = wx.Size(100,100
        #                              )
        # print 'done'

    def CheckOS(self):
        if sys.platform == 'linux2':
            self.size = (100, 300)
        if sys.platform == 'darwin':
            self.size = wx.DefaultSize
        if sys.platform == 'win32':
            self.size = (100, 400)

    def InitUI(self):




        ####################################
        # CREATE PANELS TO HOLD UI ELEMENTS
        ####################################

        self.t = wx.Panel(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600,150), style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)
        self.m = wx.Panel(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500,250), style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)
        self.m2 = wx.Panel(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500,100), style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)
        self.b = wx.Panel(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500,75), style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)
        #####################
        # TOP PANEL ELEMENTS
        #####################

         # add some descriptive text at the top of the window
        self.LinkTitle_staticText = wx.StaticText(self.t, wx.ID_ANY, u"Select Add to Create a New Link", wx.Point(-1, -1),wx.DefaultSize, 0)

        # create link list box; new and delete buttons
        self.LinkNameListBox = wx.ListBox(self.t, wx.ID_ANY, wx.DefaultPosition,wx.Size(400, 100), [], 0)
        self.ButtonNew = wx.Button(self.t, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, 0)
        self.ButtonDelete = wx.Button(self.t, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0)


        ########################
        # MIDDLE PANEL ELEMENTS
        ########################

        # OUTPUT EXCHANGE ITEM - PROPERTY GRID VIEW

        # if sys.platform == 'linux2':
        #     self.outputProperties.SetFont(self.font)

        self.OutputComboBox = wx.ComboBox(self.m, wx.ID_ANY, '',wx.DefaultPosition, wx.Size(150, -1), [''], 0)
        self.outputProperties = wxpg.PropertyGridManager(self.m, size=self.size,style=wxpg.PG_PROP_READONLY)
        p1 = self.outputProperties.AddPage('Output Exchange Item Metadata')
        self.outputProperties.Append( wxpg.PropertyCategory("Variable") )
        self.outputProperties.Append( wxpg.StringProperty("Variable Name",value='') )
        self.outputProperties.Append( wxpg.ArrayStringProperty("Variable Description",value='') )
        self.outputProperties.Append( wxpg.PropertyCategory("Unit") )
        self.outputProperties.Append( wxpg.StringProperty("Unit Name",value='') )
        self.outputProperties.Append( wxpg.StringProperty("Unit Type",value='') )
        self.outputProperties.Append( wxpg.StringProperty("Unit Abbreviation",value='') )
        self.outputProperties.SetPageSplitterPosition(page=p1.GetIndex(), pos=300)

        # adjust the properties box size to the ideal size
        # x,y = self.outputProperties.GetBestVirtualSize()
        # self.outputProperties.Layout()
        # self.outputProperties.MinSize = (wx.Size(325,y-20))         # Need to set the minimum size b/c that is what the sizer uses


        # INPUT EXCHANGE ITEM - PROPERTY GRID VIEW

        # # if sys.platform == 'linux2':
        # #     self.inputProperties.SetFont(self.font)
        #
        self.InputComboBox = wx.ComboBox(self.m, wx.ID_ANY, '',wx.DefaultPosition, wx.Size(150, -1),[''], 0)
        self.inputProperties = wxpg.PropertyGridManager(self.m, size=self.size,style=wxpg.PG_PROP_READONLY )
        page = self.inputProperties.AddPage('Input Exchange Item Metadata')
        self.inputProperties.Append( wxpg.PropertyCategory("Variable") )
        self.inputProperties.Append( wxpg.StringProperty("Variable Name",value='') )
        self.inputProperties.Append( wxpg.ArrayStringProperty("Variable Description",value='') )
        self.inputProperties.Append( wxpg.PropertyCategory("Unit") )
        self.inputProperties.Append( wxpg.StringProperty("Unit Name",value='') )
        self.inputProperties.Append( wxpg.StringProperty("Unit Type",value='') )
        self.inputProperties.Append( wxpg.StringProperty("Unit Abbreviation",value='') )
        self.inputProperties.SetPageSplitterPosition(page=0, pos=120)

        g = self.inputProperties.GetGrid().GetClientSize()
        x,y = self.inputProperties.GetBestVirtualSize()
        self.inputProperties.MinSize = wx.Size(x,y+4)
        self.inputProperties.Layout()

        # adjust the properties box size to the ideal size
        # x,y = self.inputProperties.GetBestVirtualSize()
        # self.inputProperties.Layout()
        # self.inputProperties.MinSize = (wx.Size(325,y-20))  # Need to set the minimum size b/c that is what the sizer uses




        # # SPATIAL AND TEMPORAL INTERPOLATIONS
        TemporalChoices = self.TemporalInterpolationChoices()  # Create the choices for the Temporal Interpolation Combobox
        SpatialChoices = self.SpatialInterpolationChoices()  # Create the choices for the Spatial Interpolation Combobox
        self.ComboBoxTemporal = wx.ComboBox(self.m2, wx.ID_ANY, u"None Specified",wx.DefaultPosition, wx.Size(150, -1),TemporalChoices, 0)
        self.ComboBoxSpatial = wx.ComboBox(self.m2, wx.ID_ANY, u"None Specified",wx.DefaultPosition, wx.Size(150, -1),SpatialChoices, 0)
        self.Temporal_staticText = wx.StaticText(self.m2, wx.ID_ANY, u"Temporal Interpolation",wx.DefaultPosition, wx.DefaultSize, 0)
        self.Spatial_staticText = wx.StaticText(self.m2, wx.ID_ANY, u"Spatial Interpolation",wx.DefaultPosition, wx.DefaultSize, 0)

        ########################
        # BOTTOM PANEL ELEMENTS
        ########################

        # PLOT, SAVE, CANCEL BUTTONS
        self.ButtonPlot = wx.Button(self.b, wx.ID_ANY, u"SpatialPlot", wx.DefaultPosition, wx.DefaultSize, 0)
        self.ButtonSave = wx.Button(self.b, wx.ID_ANY, u"Save and Close", wx.DefaultPosition, wx.DefaultSize, 0)
        self.ButtonCancel = wx.Button(self.b, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)



        ###############
        # BUILD SIZERS
        ###############

        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.BoxSizer(wx.VERTICAL)

        gbs_t = wx.GridBagSizer(15, 15)
        ButtonSizer.Add(self.ButtonNew, 0, wx.ALL, 5)
        ButtonSizer.Add(self.ButtonDelete, 0, wx.ALL, 5)
        gbs_t.Add(self.LinkTitle_staticText,(0,0))
        gbs_t.Add(self.LinkNameListBox,(1,0),flag=wx.EXPAND)
        gbs_t.Add(ButtonSizer,(1,2))
        gbs_t.AddGrowableCol(0)
        # gbs.AddGrowableRow(1)
        self.t.SetSizer(gbs_t)


        gbs_m = wx.GridBagSizer(15, 15)
        gbs_m.Add(self.OutputComboBox, (0,0), flag=wx.ALIGN_RIGHT)
        gbs_m.Add(self.InputComboBox, (0,1), flag=wx.ALIGN_RIGHT)
        gbs_m.Add(self.outputProperties, (1,0), flag=wx.EXPAND)
        gbs_m.Add(self.inputProperties, (1,1), flag=wx.EXPAND)
        gbs_m.AddGrowableCol(0)
        gbs_m.AddGrowableCol(1)
        # gbs_m.AddGrowableRow(1)
        self.m.SetSizer(gbs_m)


        gbs_m2 = wx.GridBagSizer(15, 15)
        gbs_m2.Add(self.Temporal_staticText, (0,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        gbs_m2.Add(self.Spatial_staticText, (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        gbs_m2.Add(self.ComboBoxTemporal, (0,1), flag=wx.EXPAND)
        gbs_m2.Add(self.ComboBoxSpatial, (1,1), flag=wx.EXPAND)
        gbs_m2.AddGrowableCol(0)
        self.m2.SetSizer(gbs_m2)



        gbs_b = wx.GridBagSizer(15, 15)
        plot = wx.BoxSizer(wx.HORIZONTAL)
        plot.Add(self.ButtonPlot, 0, wx.ALL, 5)
        gbs_b.Add(plot,(0,0),flag=wx.ALIGN_LEFT)
        bs = wx.BoxSizer(wx.HORIZONTAL)
        bs.Add(self.ButtonSave, 0, wx.ALL, 5)
        bs.Add(self.ButtonCancel, 0, wx.ALL, 5)
        gbs_b.Add(bs, (0,1), flag=wx.ALIGN_RIGHT)
        gbs_b.AddGrowableCol(0)
        self.b.SetSizer(gbs_b)

        # determine minimum window size
        height = 0
        width = 0
        for g in [self.t, self.m, self.m2, self.b]:
            height += g.GetMinSize().Get()[1]
            width = g.GetEffectiveMinSize().Get()[0] if g.GetEffectiveMinSize().Get()[0] > width else width
        print height
        print width

        FrameSizer.Add(self.t, 0, wx.EXPAND, 5)
        FrameSizer.Add(self.m, 1, wx.EXPAND | wx.ALL, 5)
        FrameSizer.Add(self.m2, 1, wx.ALIGN_RIGHT | wx.ALL, 5)
        FrameSizer.Add(self.b, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(FrameSizer)
        self.Centre(wx.BOTH)

        # set both min and max sizes to disable resizing
        self.MinSize = wx.Size(width, height+22)
        self.MaxSize = wx.Size(width,height+22)
        self.SetClientSize(wx.Size(width,height))

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


