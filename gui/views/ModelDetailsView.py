import wx
import wx.grid


class ModelDetailsView(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, size=(550, 550))

        # Create panel
        self.panel = wx.Panel(self)

        # Create components
        self.grid = wx.grid.Grid(self.panel)

        self.grid.CreateGrid(0, 2)
        self._min_grid_width_size = 0  # Keeps track of the size needed to fit all the content

        # Disables the header row and column
        self.grid.SetColLabelSize(0)
        self.grid.SetRowLabelSize(0)

        # Add components to sizer
        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        self.panel.SetSizer(self.frame_sizer)

        # Events
        self.Bind(wx.EVT_SIZE, self.frame_resizing)

        self.Show()

    def get_grid_width(self):
        return self.grid.GetColSize(0) + self.grid.GetColSize(1)

    def resize_grid_to_fill_white_space(self):
        col_size = self.grid.GetColSize(0)
        C, R = self.grid.GetSize()
        if C - col_size > 0:
            self.grid.SetColSize(1, C - col_size)

    def restore_min_grid_width(self):
        # Sets the width of the grid to fit the content.
        self.grid.SetColSize(1, self._min_grid_width_size)

    def resize_window_to_fit(self):
        self.frame_sizer.Fit(self)

    def set_cell_background_color(self, row, column, color):
        self.grid.SetCellBackgroundColour(row, column, color)

    ###############################
    # EVENTS
    ###############################

    def frame_resizing(self, event):
        #  Handles resizing the grid so the content is always show
        if self.GetSize()[0] < self._min_grid_width_size:
            self.restore_min_grid_width()
        else:
            self.resize_grid_to_fill_white_space()
        event.Skip()


