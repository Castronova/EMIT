import wx
import wx.grid
from gui.controller.PlotForSiteViewerCtrl import PlotForSiteViewerCtrl


class SpatialView:

    def __init__(self, panel):
        self.biggest_col = 0
        # Creating all the necessary panels
        top_panel = wx.Panel(panel)
        middle_panel = wx.Panel(panel)
        lower_panel = wx.Panel(panel)

        # SETUP OF TOP PANEL
        sizer_top_panel = wx.BoxSizer(wx.HORIZONTAL)
        self.plot = PlotForSiteViewerCtrl(top_panel)
        sizer_top_panel.Add(self.plot.plot, 1, wx.EXPAND | wx.ALL, 2)
        top_panel.SetSizer(sizer_top_panel)

        # SETUP OF MIDDLE PANEL
        sizer_middle_panel = wx.BoxSizer(wx.HORIZONTAL)
        self.input_checkbox = wx.CheckBox(parent=middle_panel, label="Input Exchange Item: ")
        self.output_checkbox = wx.CheckBox(parent=middle_panel, label="Output Exchange Item: ")
        sizer_middle_panel.AddSpacer(5)
        sizer_middle_panel.Add(self.input_checkbox, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        sizer_middle_panel.Add(self.output_checkbox, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        middle_panel.SetSizer(sizer_middle_panel)


        # SETUP OF LOWER PANEL
        sizer_lower_panel = wx.BoxSizer(wx.HORIZONTAL)
        self.input_grid = wx.grid.Grid(lower_panel, size=(300, -1))
        self.output_grid = wx.grid.Grid(lower_panel, size=(300, -1))
        set_up_grid(self.input_grid)
        set_up_grid(self.output_grid)
        sizer_lower_panel.Add(self.input_grid, 1, flag=wx.EXPAND | wx.ALL)
        sizer_lower_panel.Add(self.output_grid, 1, flag=wx.EXPAND | wx.ALL)
        lower_panel.SetSizer(sizer_lower_panel)

        # ADD PANEL TO THE FRAME
        sizer_spatial_view = wx.BoxSizer(wx.VERTICAL)
        sizer_spatial_view.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        sizer_spatial_view.Add(middle_panel, 0, wx.EXPAND | wx.ALL, 2)
        sizer_spatial_view.Add(lower_panel, 1, wx.EXPAND | wx.ALL, 2)
        panel.SetSizer(sizer_spatial_view)


def stretch_grid(grid):
    # 170 is a good size to stretch the grid
    if grid.GetColSize(1) < 170:
        grid.SetColSize(1, 170)


def set_up_grid(grid):
    """
    This function only works with type wx.grid.Grid
    The it will create a grid that is like the one found in LinkCtrl/View.
    :param grid:
    :return:
    """
    import wx.grid
    from coordinator.emitLogging import elog

    if isinstance(grid, wx.grid.Grid):
        grid.CreateGrid(6, 2)
        grid.EnableEditing(False)
        grid.EnableGridLines(True)
        grid.SetGridLineColour(wx.Colour(0, 0, 0))
        grid.EnableDragGridSize(False)
        grid.SetMargins(0, 0)

        # Columns
        grid.EnableDragColMove(False)
        grid.EnableDragColSize(True)
        grid.SetColLabelSize(0)
        grid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Rows
        grid.EnableDragRowSize(True)
        grid.SetRowLabelSize(0)
        grid.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Defaults
        grid.SetDefaultCellBackgroundColour(wx.Colour(255, 255, 255))  # white
        grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        # Set Cell Values
        grid.SetCellValue(0, 0, " Variable")
        grid.SetCellValue(1, 0, " Name")
        # grid.SetCellValue(2, 0, " Description")
        grid.SetCellValue(2, 0, " Geometry Type")
        grid.SetCellValue(3, 0, " Coordinate System")
        grid.SetCellValue(4, 0, " Extent")
        grid.SetCellValue(5, 0, " Number of elements")

        grid.SetCellBackgroundColour(0, 0, wx.Colour(195, 195, 195))  # Grey
        grid.SetCellBackgroundColour(0, 1, wx.Colour(195, 195, 195))
        # grid.SetCellBackgroundColour(3, 0, wx.Colour(195, 195, 195))
        # grid.SetCellBackgroundColour(3, 1, wx.Colour(195, 195, 195))
        grid.SetGridLineColour(wx.Colour(195, 195, 195))

        grid.AutoSize()
        stretch_grid(grid)
    else:
        elog.debug("grid must be type wx.grid.Grid")
