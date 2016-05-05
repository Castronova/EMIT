import wx
import wx.xrc
import wx.dataview
import wx.grid
from transform.time import *
from transform.space import *
import coordinator.engineAccessors as engine
import sys


class LinkView(wx.Frame):
    def __init__(self, parent, output, input):
        if sys.platform == 'darwin':
            width, height = (700, 520)
        elif sys.platform == 'win32':
            width, height = (700, 530)
        else:
            width, height = (700, 625)

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(width, height),
                          style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)

        panel = wx.Panel(self)
        self.top_panel = wx.Panel(parent=panel)
        self.middle_panel = wx.Panel(panel)
        self.bottom_panel = wx.Panel(panel)

        self.input_component = input
        self.output_component = output
        self.input_items = None
        self.output_items = None

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        top_panel_button_sizer = wx.BoxSizer(wx.VERTICAL)

        self.link_instructions_text = wx.StaticText(parent=panel, label=u"Select add to create a new link")
        frame_sizer.Add(self.link_instructions_text, 0, wx.ALL, 5)

        LinkStartSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.link_name_list_box = wx.ListBox(self.top_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(575, 125), [], 0)
        self.new_button = wx.Button(parent=self.top_panel, label="New")
        self.delete_button = wx.Button(parent=self.top_panel, label="Delete")
        self.swap_button = wx.Button(parent=self.top_panel, label="Swap")

        LinkStartSizer.Add(self.link_name_list_box, 0, wx.ALL, 5)
        top_panel_button_sizer.Add(self.new_button, 0, wx.ALL, 5)
        top_panel_button_sizer.Add(self.delete_button, 0, wx.ALL, 5)
        top_panel_button_sizer.Add(self.swap_button, 0, wx.ALL, 5)

        LinkStartSizer.Add(top_panel_button_sizer, 1, wx.EXPAND, 5)

        self.top_panel.SetSizer(LinkStartSizer)
        self.top_panel.Layout()
        LinkStartSizer.Fit(self.top_panel)
        frame_sizer.Add(self.top_panel, 1, wx.EXPAND | wx.ALL, 5)

        middle_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)

        ###########################################
        # OUTPUT EXCHANGE ITEM - GRID VIEW
        ###########################################

        OutputSizer = wx.BoxSizer(wx.VERTICAL)

        self.outputLabel = wx.StaticText(parent=self.middle_panel, id=wx.ID_ANY, label=u"Output",
                                         pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.OutputComboBox = wx.ComboBox(parent=self.middle_panel, id=wx.ID_ANY, value='',
                                          pos=wx.DefaultPosition, size=wx.Size(320, -1), choices=[''], style=0)

        OutputSizer.Add(self.outputLabel, 0, wx.ALL, 5)
        OutputSizer.Add(self.OutputComboBox, 0, wx.ALL, 5)

        self.output_grid = wx.grid.Grid(self.middle_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(325, -1), 0)
        self.init_grid(self.output_grid)
        OutputSizer.Add(self.output_grid, 0, wx.ALL, 5)

        ###########################################
        # SPATIAL AND TEMPORAL INTERPOLATION LABELS
        ###########################################
        textSizer = wx.BoxSizer(wx.HORIZONTAL)

        textSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        rightAlignSizer = wx.BoxSizer(wx.VERTICAL)

        self.Temporal_staticText = wx.StaticText(self.middle_panel, wx.ID_ANY, u"Temporal Interpolation",
                                                 wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)
        self.Temporal_staticText.Wrap(-1)
        rightAlignSizer.Add(self.Temporal_staticText, 0, wx.ALL, 5)

        rightAlignSizer.AddSpacer((0, 12), 0, wx.EXPAND, 5)  # This is to make sure that the static text stays the same distance apart

        self.Spatial_staticText = wx.StaticText(self.middle_panel, wx.ID_ANY, u"    Spatial Interpolation",
                                                wx.DefaultPosition, wx.DefaultSize, 0) #The space before the word Spatial is to help it align Right
        self.Spatial_staticText.Wrap(-1)
        rightAlignSizer.Add(self.Spatial_staticText, 0, wx.ALL, 5)

        textSizer.Add(rightAlignSizer, 1, wx.EXPAND, 5)

        OutputSizer.Add(textSizer, 1, wx.EXPAND, 5)

        middle_panel_sizer.Add(OutputSizer, 1, wx.EXPAND, 5)


        ###########################################
        # INPUT EXCHANGE ITEM - PROPERTY GRID VIEW
        ###########################################

        InputSizer = wx.BoxSizer(wx.VERTICAL)

        self.input_label = wx.StaticText(self.middle_panel, wx.ID_ANY, u"Input", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.input_combo = wx.ComboBox(self.middle_panel, wx.ID_ANY, '',
                                       wx.DefaultPosition, wx.Size(320, -1), [''], 0)
        InputSizer.Add(self.input_label, 0, wx.ALL, 5)
        InputSizer.Add(self.input_combo, 0, wx.ALL, 5)

        self.input_grid = wx.grid.Grid(self.middle_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(325, -1), 0)
        self.init_grid(self.input_grid)
        InputSizer.Add(self.input_grid, 0, wx.ALL, 5)

        #####################################
        # SPATIAL AND TEMPORAL INTERPOLATIONS
        #####################################

        TemporalChoices = self.temporal_interpolation_combo_choices()  # Create the choices for the Temporal Interpolation Combobox
        self.ComboBoxTemporal = wx.ComboBox(self.middle_panel, wx.ID_ANY, u"None Specified",
                                            wx.DefaultPosition, wx.Size(320, -1),
                                            TemporalChoices, 0)
        InputSizer.Add(self.ComboBoxTemporal, 0, wx.ALL, 5)

        SpatialChoices = self.spatial_interpolation_combo_choices()  # Create the choices for the Spatial Interpolation Combobox
        self.ComboBoxSpatial = wx.ComboBox(self.middle_panel, wx.ID_ANY, u"None Specified",
                                           wx.DefaultPosition, wx.Size(320, -1),
                                           SpatialChoices, 0)
        InputSizer.Add(self.ComboBoxSpatial, 0, wx.ALL, 5)

        middle_panel_sizer.Add(InputSizer, 1, wx.EXPAND, 5)

        self.middle_panel.SetSizer(middle_panel_sizer)
        self.middle_panel.Layout()
        middle_panel_sizer.Fit(self.middle_panel)
        frame_sizer.Add(self.middle_panel, 1, wx.EXPAND | wx.ALL, 5)

        ButtonSizerBottom = wx.BoxSizer(wx.HORIZONTAL)

        PlottingButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ButtonPlot = wx.Button(parent=self.bottom_panel, label="Plot Geometries")
        PlottingButtonSizer.Add(self.ButtonPlot, 0, wx.ALL, 5)

        ButtonSizerBottom.Add(PlottingButtonSizer, 1, wx.EXPAND, 5)

        RightAlignSizer = wx.BoxSizer(wx.HORIZONTAL)

        RightAlignSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        self.save_button = wx.Button(parent=self.bottom_panel, label="Save and Close")
        RightAlignSizer.Add(self.save_button, 0, wx.ALL, 5)

        self.cancel_button = wx.Button(parent=self.bottom_panel, label=u"Cancel")
        RightAlignSizer.Add(self.cancel_button, 0, wx.ALL, 5)

        ButtonSizerBottom.Add(RightAlignSizer, 1, wx.EXPAND, 5)

        self.bottom_panel.SetSizer(ButtonSizerBottom)
        self.bottom_panel.Layout()
        ButtonSizerBottom.Fit(self.bottom_panel)
        frame_sizer.Add(self.bottom_panel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(frame_sizer)

        self.Bind(wx.EVT_SIZING, self.frame_resizing)
        self.Centre(wx.BOTH)

    def frame_resizing(self, event):
        self.resize_grid_to_fill_white_space(self.input_grid)
        self.resize_grid_to_fill_white_space(self.output_grid)

    def init_grid(self, grid):
        # Grid
        grid.CreateGrid(7, 2)
        grid.EnableEditing(False)
        grid.EnableGridLines(True)
        grid.SetGridLineColour(wx.Colour(0, 0, 0))
        grid.EnableDragGridSize(False)
        grid.SetMargins(0, 0)

        # Columns
        grid.EnableDragColMove(False)
        grid.EnableDragColSize(True)
        grid.SetColLabelSize(0)
        grid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        grid.EnableDragRowSize(True)
        grid.SetRowLabelSize(0)
        grid.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        grid.SetDefaultCellBackgroundColour(wx.Colour(255, 255, 255))
        grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        # Set Cell Values
        grid.SetCellValue(0, 0, " Variable")
        grid.SetCellValue(1, 0, " Name")
        grid.SetCellValue(2, 0, " Description")
        grid.SetCellValue(3, 0, " Unit")
        grid.SetCellValue(4, 0, " Name")
        grid.SetCellValue(5, 0, " Type")
        grid.SetCellValue(6, 0, " Abbreviation")

        grid.SetCellBackgroundColour(0, 0, wx.Colour(195, 195, 195))
        grid.SetCellBackgroundColour(0, 1, wx.Colour(195, 195, 195))
        grid.SetCellBackgroundColour(3, 0, wx.Colour(195, 195, 195))
        grid.SetCellBackgroundColour(3, 1, wx.Colour(195, 195, 195))
        grid.SetGridLineColour(wx.Colour(195, 195, 195))
        self.resize_grid_to_fill_white_space(grid)

    def input_combo_choices(self):
        self.input_items = engine.getExchangeItems(self.input_component['id'], stdlib.ExchangeItemType.INPUT, returnGeoms=False)
        if self.input_items is not None:
            return [item['name'] for item in self.input_items]
        else:
            return [' ']

    def output_combo_choices(self):
        self.output_items = engine.getExchangeItems(self.output_component['id'], stdlib.ExchangeItemType.OUTPUT, returnGeoms=False)
        if self.output_items is not None:
            return [item['name'] for item in self.output_items]
        else:
            return [" "]

    def resize_grid_to_fill_white_space(self, grid):
        col_size = grid.GetColSize(0)
        C, R = grid.GetSize()
        if C - col_size > 0:
            grid.SetColSize(1, C - col_size)

    def spatial_interpolation_combo_choices(self):
        s = SpatialInterpolation()
        self.spatial_transformations = {i.name(): i for i in s.methods()}
        return ['None Specified'] + self.spatial_transformations.keys()

    def temporal_interpolation_combo_choices(self):
        t = TemporalInterpolation()
        self.temporal_transformations = {i.name(): i for i in t.methods()}
        return ['None Specified'] + self.temporal_transformations.keys()
