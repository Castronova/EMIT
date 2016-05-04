import wx
import wx.grid

from gui.controller.PlotForSiteViewerCtrl import PlotForSiteViewerCtrl


class SpatialView(wx.Frame):

    def __init__(self, panel):

        self.biggest_col = 0

        # Creating all the necessary panels
        top_panel = wx.Panel(panel)
        middle_panel = wx.Panel(panel)
        lower_panel = wx.Panel(panel)

        # create the sizers
        sizer_top_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_middle_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_lower_panel = wx.BoxSizer(wx.HORIZONTAL)

        # add elements to the top panel
        self.plot = PlotForSiteViewerCtrl(top_panel)
        sizer_top_panel.Add(self.plot.plot, 1, wx.EXPAND | wx.ALL, 2)
        top_panel.SetSizer(sizer_top_panel)

        # add elements to the middle panel
        self.input_combobox = wx.ComboBox(parent=middle_panel, choices=["---"])
        self.output_combobox = wx.ComboBox(parent=middle_panel, choices=["---"])
        sizer_middle_panel.Add(self.input_combobox, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        sizer_middle_panel.AddSpacer(10)
        sizer_middle_panel.Add(self.output_combobox, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        middle_panel.SetSizer(sizer_middle_panel)


        # add elements to the bottom panel
        self.input_grid = wx.grid.Grid(lower_panel)
        self.output_grid = wx.grid.Grid(lower_panel)
        setup_grid(self.input_grid, 'Input Exchange Item Metadata')
        setup_grid(self.output_grid, 'Output Exchange Item Metadata')

        sizer_lower_panel.Add(self.input_grid, 1, wx.EXPAND|wx.ALL, 10)
        sizer_lower_panel.AddSpacer(10)
        sizer_lower_panel.Add(self.output_grid, 1, wx.EXPAND|wx.ALL, 10)
        lower_panel.SetSizer(sizer_lower_panel)
        #sizer_middle_panel.AddSpacer(10)

        # add panels to frame
        sizer_spatial_view = wx.BoxSizer(wx.VERTICAL)
        sizer_spatial_view.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        sizer_spatial_view.Add(middle_panel, 0, wx.EXPAND | wx.ALL, 2)
        sizer_spatial_view.Add(lower_panel, 1, wx.EXPAND | wx.ALL, 2)
        panel.SetSizer(sizer_spatial_view)

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
    grid.SetCellSize(0,0,1,2)  # span cols 0 and 1
    grid.SetCellBackgroundColour(0, 0, wx.Colour(195, 195, 195))  # Grey

    # set the table column size
    grid.SetColSize(0, 130)
    grid.SetColSize(1, 140)

    # change color of properties
    for i in range(1, grid.GetNumberRows()):
        grid.SetCellBackgroundColour(i, 0, wx.Colour(250, 250, 250))  # light Grey

    grid.SetGridLineColour(wx.Colour(195, 195, 195))
