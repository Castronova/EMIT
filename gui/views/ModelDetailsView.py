import wx
import wx.grid


class ModelDetailsView(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None)

        self.panel = wx.Panel(self)

        self.grid = wx.grid.Grid(self.panel)

        self.grid.CreateGrid(0, 2)
        # self.refresh_grid()
        # self.grid.AppendRows(5)
        # self.grid.SetMargins(0, 0)

        # Disables the header row and column
        self.grid.SetColLabelSize(0)
        self.grid.SetRowLabelSize(0)


        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        self.panel.SetSizer(self.frame_sizer)

        self.frame_sizer.Fit(self)
        self.Show()

    def set_cell_background_color(self, row, column, color):
        self.grid.SetCellBackgroundColour(row, column, color)

    def refresh_grid(self):
        self.grid.ClearGrid()
        # self.grid.DeleteRows(0)
        # self.grid.DeleteRows(3)
        # self.grid.DeleteRows(2)

    def resize_window_to_fit(self):
        self.frame_sizer.Fit(self)
