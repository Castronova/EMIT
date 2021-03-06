import wx
import wx.xrc
import wx.dataview
import wx.grid
from transform.time import *
from transform.space import *


class LinkView(wx.Frame):
    def __init__(self, parent, output, input):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        # Create all necessary panels
        panel = wx.Panel(self)  # Top level panel
        self.top_panel = wx.Panel(parent=panel)
        self.middle_panel = wx.Panel(panel)
        self.bottom_panel = wx.Panel(panel)

        self.input_component = input
        self.output_component = output

        self.link_instructions_text = wx.StaticText(parent=panel, label=u"Select add to create a new link")

        ###########################################
        # BUILD TOP PANEL
        ###########################################

        top_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_panel_button_sizer = wx.BoxSizer(wx.VERTICAL)

        self.link_name_list_box = wx.ListBox(self.top_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(575, 125), [], 0)
        self.new_button = wx.Button(parent=self.top_panel, label="New")
        self.delete_button = wx.Button(parent=self.top_panel, label="Delete")
        self.swap_button = wx.Button(parent=self.top_panel, label="Swap")

        top_panel_button_sizer.Add(self.new_button, 0, wx.ALL, 5)
        top_panel_button_sizer.Add(self.delete_button, 0, wx.ALL, 5)
        top_panel_button_sizer.Add(self.swap_button, 0, wx.ALL, 5)

        top_panel_sizer.Add(self.link_name_list_box, 1)  # Set to 1 so it list box resize
        top_panel_sizer.Add(top_panel_button_sizer, 0)  # Set to 0 so buttons do not resize

        self.top_panel.SetSizer(top_panel_sizer)

        ###########################################
        # BUILD MIDDLE PANEL
        ###########################################

        # Create components
        self.output_label = wx.StaticText(parent=self.middle_panel, label=u"Output", )
        self.input_label = wx.StaticText(parent=self.middle_panel, label="Input")
        self.output_combo = wx.ComboBox(parent=self.middle_panel, value='', size=wx.Size(320, -1), choices=[''])
        self.input_combo = wx.ComboBox(parent=self.middle_panel, value='', size=wx.Size(320, -1), choices=[''])
        self.output_grid = wx.grid.Grid(parent=self.middle_panel, size=(325, -1))
        self.input_grid = wx.grid.Grid(parent=self.middle_panel, size=(325, -1))
        self.init_grid(grid=self.output_grid)
        self.init_grid(self.input_grid)
        self.temporal_text = wx.StaticText(parent=self.middle_panel, label="Temporal Interpolation", style=wx.ALIGN_RIGHT)
        self.spatial_text = wx.StaticText(parent=self.middle_panel, label="Spatial Interpolation", style=wx.ALIGN_RIGHT)
        self.temporal_combo = wx.ComboBox(parent=self.middle_panel, value="None Specified", size=wx.Size(320, -1), choices=self.temporal_interpolation_combo_choices())
        self.spatial_combo = wx.ComboBox(parent=self.middle_panel, value="None Specified", size=wx.Size(320, -1), choices=self.spatial_interpolation_combo_choices())

        # Create sizers
        middle_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_sizer = wx.BoxSizer(wx.VERTICAL)  # sizer for all output components and temporal/spatial text
        input_sizer = wx.BoxSizer(wx.VERTICAL)  # sizer for all input components and temporal/spatial combo

        # Add components to sizers
        output_sizer.Add(self.output_label, proportion=0, flag=wx.ALL, border=5)
        output_sizer.Add(self.output_combo, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        output_sizer.Add(self.output_grid, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        output_sizer.Add(self.temporal_text, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
        output_sizer.AddSpacer((0, 12), 0, wx.EXPAND, 5)
        output_sizer.Add(self.spatial_text, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

        input_sizer.Add(self.input_label, 0, wx.ALL, 5)
        input_sizer.Add(self.input_combo, 0, flag=wx.EXPAND | wx.ALL, border=5)
        input_sizer.Add(self.input_grid, 0, flag=wx.EXPAND | wx.ALL, border=5)
        input_sizer.Add(self.temporal_combo, 0, wx.EXPAND | wx.ALIGN_LEFT, 5)
        input_sizer.Add(self.spatial_combo, 0, wx.EXPAND | wx.ALIGN_LEFT, 5)

        # Place input and output sizers onto the middle panel sizer
        middle_panel_sizer.Add(output_sizer, proportion=1, flag=wx.EXPAND, border=5)  # proportion = 1 so it will resize
        middle_panel_sizer.Add(input_sizer, proportion=1, flag=wx.EXPAND, border=5)

        self.middle_panel.SetSizer(middle_panel_sizer)

        ###########################################
        # BUILD BOTTOM PANEL
        ###########################################

        # Create necessary components
        self.plot_button = wx.Button(parent=self.bottom_panel, label="Plot Geometries")
        self.save_button = wx.Button(parent=self.bottom_panel, label="Save and Close")
        self.cancel_button = wx.Button(parent=self.bottom_panel, label="Cancel")

        # Create bottom panel sizer
        bottom_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add components to sizer
        bottom_panel_sizer.Add(self.plot_button, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        bottom_panel_sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        bottom_panel_sizer.Add(self.save_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        bottom_panel_sizer.Add(self.cancel_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.bottom_panel.SetSizer(bottom_panel_sizer)

        ###########################################
        # ADD PANELS TO FRAME SIZER
        ###########################################

        # Add everything to the frame
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(self.link_instructions_text, 0, wx.ALL, 5)
        frame_sizer.Add(self.top_panel, 0, wx.EXPAND | wx.ALL, 5)
        frame_sizer.Add(self.middle_panel, 1, wx.EXPAND | wx.ALL, 5)
        # proportion=0 so the bottom_panel stays at the bottom of the frame
        frame_sizer.Add(self.bottom_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(frame_sizer)
        frame_sizer.Fit(self)  # Sizes the window automatically so the components fit inside the window

        self.Centre(wx.BOTH)

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
