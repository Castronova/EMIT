import wx
import wx.grid
from gui.controller.PlotForSiteViewerCtrl import PlotForSiteViewerCtrl


class SpatialView(wx.Frame):

    def __init__(self, parent=None):

        wx.Frame.__init__(self, parent=parent, size=(650, 610))

        # Creating all the necessary panels
        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)
        lower_panel = wx.Panel(panel)
        input_grid_panel = wx.Panel(lower_panel)
        output_grid_panel = wx.Panel(lower_panel)

        # SETUP OF TOP PANEL
        sizer_top_panel = wx.BoxSizer(wx.HORIZONTAL)
        self.plot = PlotForSiteViewerCtrl(top_panel)
        sizer_top_panel.Add(self.plot.plot, 1, wx.EXPAND | wx.ALL, 2)
        top_panel.SetSizer(sizer_top_panel)

        # SETUP FOR LOWER PANEL
        sizer_lower_panel = wx.BoxSizer(wx.HORIZONTAL)

        input_sizer = wx.BoxSizer(wx.VERTICAL)
        self.input_grid = wx.grid.Grid(input_grid_panel, size=(300, -1))
        set_up_grid(self.input_grid)
        input_sizer.Add(self.input_grid, 1, wx.EXPAND | wx.ALL, 5)
        input_grid_panel.SetSizer(input_sizer)

        output_sizer = wx.BoxSizer(wx.VERTICAL)
        self.output_grid = wx.grid.Grid(output_grid_panel, size=(300, -1))
        set_up_grid(self.output_grid)
        output_sizer.Add(self.output_grid, 1, wx.EXPAND | wx.ALL, 5)
        output_grid_panel.SetSizer(output_sizer)

        #  ADD THE GRIDS TO THE LOWER PANEL
        sizer_lower_panel.Add(input_grid_panel, 1, wx.EXPAND | wx.ALL, 2)
        sizer_lower_panel.Add(output_grid_panel, 1, wx.EXPAND | wx.ALL, 2)
        lower_panel.SetSizer(sizer_lower_panel)

        # ADD PANEL TO THE FRAME
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lower_panel, 1, wx.EXPAND | wx.ALL, 2)
        panel.SetSizer(vbox)

        self.Show()


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

        grid.AutoSizeColumn(0)
        col_size = grid.GetColSize(0)
        C, R = grid.GetSize()
        grid.SetColSize(1, C - col_size)
    else:
        elog.debug("grid must be type wx.grid.Grid")
