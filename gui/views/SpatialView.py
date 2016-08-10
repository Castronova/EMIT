import wx
import wx.grid
# from gui.Models.SpatialTemporalPlotter import SpatialTemporalPlotter
from gui.controller.PlotCtrl import PlotCtrl



class SpatialView(wx.Panel):

    def __init__(self, panel):

        wx.Panel.__init__(self, panel)

        # Creating all the necessary panels
        top_panel = wx.Panel(self)
        bottom_panel = wx.Panel(self)

        # create the sizers
        sizer_top_panel = wx.BoxSizer(wx.HORIZONTAL)
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        output_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_lower_panel = wx.BoxSizer(wx.HORIZONTAL)

        # add elements to the top panel
        self.plot = PlotCtrl(top_panel)
        sizer_top_panel.Add(self.plot.canvas, 1, wx.EXPAND | wx.ALL, 2)
        top_panel.SetSizer(sizer_top_panel)

        # create lower panel components
        self.input_combobox = wx.ComboBox(parent=bottom_panel, choices=["---"])
        self.input_grid = wx.grid.Grid(bottom_panel, size=(300, -1))
        self.output_combobox = wx.ComboBox(parent=bottom_panel, choices=["---"])
        self.output_grid = wx.grid.Grid(bottom_panel, size=(300, -1))

        setup_grid(self.input_grid, 'Input Exchange Item Metadata')
        setup_grid(self.output_grid, 'Output Exchange Item Metadata')

        # add elements to the bottom panel
        input_sizer.Add(self.input_combobox, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        # proportion=1 allows the grid to expand while resizing. Setting it to 0 will keep the grid height the same
        input_sizer.Add(self.input_grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        output_sizer.Add(self.output_combobox, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        output_sizer.Add(self.output_grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)

        sizer_lower_panel.Add(input_sizer, proportion=1, flag=wx.EXPAND, border=5)
        sizer_lower_panel.Add(output_sizer, proportion=1, flag=wx.EXPAND, border=5)

        bottom_panel.SetSizer(sizer_lower_panel)

        # add panels to frame
        sizer_spatial_view = wx.BoxSizer(wx.VERTICAL)
        sizer_spatial_view.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        #  proportion=0 makes the panel same size when resizing
        sizer_spatial_view.Add(bottom_panel, 0, wx.EXPAND | wx.ALL, 2)
        self.SetSizer(sizer_spatial_view)


def setup_grid(grid, title):
    """
    This function only works with type wx.grid.Grid
    The it will create a grid that is like the one found in LinkCtrl/View.
    :param grid:
    :return:
    """

    grid.CreateGrid(6, 2)
    grid.EnableEditing(False)
    grid.EnableGridLines(True)
    grid.SetGridLineColour(wx.Colour(0, 0, 0))
    grid.EnableDragGridSize(False)

    # Columns
    grid.EnableDragColMove(False)
    grid.EnableDragColSize(True)
    grid.SetColLabelSize(0)
    grid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
    grid.SetColSize(0, 110)

    # Rows
    grid.EnableDragRowSize(True)
    grid.SetRowLabelSize(0)
    grid.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

    # Defaults
    grid.SetDefaultCellBackgroundColour(wx.Colour(255, 255, 255))  # white
    grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

    # Set Cell Values
    grid.SetCellValue(0, 0, " %s" % title)
    grid.SetCellValue(1, 0, " Variable Name")
    grid.SetCellValue(2, 0, " Geometry Type")
    grid.SetCellValue(3, 0, " Geometry Count")
    grid.SetCellValue(4, 0, " Coordinate System")
    grid.SetCellValue(5, 0, " Spatial Extent")

    # set the default background color
    grid.SetDefaultCellBackgroundColour('WHITE')

    # change color and size of header
    grid.SetCellSize(0, 0, 1, 2)  # span cols 0 and 1
    grid.SetCellBackgroundColour(0, 0, wx.Colour(195, 195, 195))  # Grey

    # set the table column size
    grid.SetColSize(0, 133)
    grid.SetColSize(1, 155)

    # change color of properties
    for i in range(1, grid.GetNumberRows()):
        grid.SetCellBackgroundColour(i, 0, wx.Colour(250, 250, 250))  # light Grey

    grid.SetGridLineColour(wx.Colour(195, 195, 195))
