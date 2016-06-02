import wx
from gui.controller.PlotForSiteViewerCtrl import PlotForSiteViewerCtrl
from gui.Models.CustomListCtrl import CustomListCtrl


class SimulationsVIew(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        # Create panels
        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)
        middle_panel = wx.Panel(panel)
        bottom_panel = wx.Panel(panel, size=(-1, 250))

        ###############################
        # TOP PANEL COMPONENTS
        ###############################

        # Create components
        self.temporal_plot = PlotForSiteViewerCtrl(top_panel)
        self.spatial_plot = PlotForSiteViewerCtrl(top_panel)

        # Create sizer and add components to sizer
        top_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_panel_sizer.Add(self.temporal_plot.plot, 1, wx.EXPAND | wx.ALL, 2)
        top_panel_sizer.Add(self.spatial_plot.plot, 1, wx.EXPAND | wx.ALL, 2)

        top_panel.SetSizer(top_panel_sizer)

        ###############################
        # MIDDLE PANEL COMPONENTS
        ###############################

        # Create components
        start_date_text = wx.StaticText(middle_panel, label="Start")
        self.start_date_picker = wx.DatePickerCtrl(middle_panel)
        end_date_text = wx.StaticText(middle_panel, label="End")
        self.end_date_picker = wx.DatePickerCtrl(middle_panel)
        self.plot_button = wx.Button(middle_panel, label="Plot")

        # Create sizer and add components to sizer
        middle_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        middle_panel_sizer.Add(start_date_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(self.start_date_picker, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(end_date_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(self.end_date_picker, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(self.plot_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)

        middle_panel.SetSizer(middle_panel_sizer)

        ###############################
        # BOTTOM PANEL COMPONENTS
        ###############################

        # Create components
        self.table = CustomListCtrl(bottom_panel)

        # Create sizer and add components to sizer
        bottom_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_panel_sizer.Add(self.table, 1, wx.EXPAND | wx.ALL, 5)
        bottom_panel.SetSizer(bottom_panel_sizer)

        # Add panels to the frame
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        frame_sizer.Add(middle_panel, 0, wx.EXPAND | wx.ALL, 2)
        frame_sizer.Add(bottom_panel, 0, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(frame_sizer)
        frame_sizer.Fit(self)
        data = [(1, 2,), (2, 3), (3, 4)]  # x, y
        self.plot_data(data)
        self.CenterOnScreen()
        self.Show()

        # Test data
        columns = ["column 1", "column 2", "column 3", "column 4"]
        data = [["row 1", "row 1", "row1", "row 1"], ["row 2", "row 2", "row 2", "row 2"]]
        self.table.set_columns(columns)
        self.table.set_table_content(data)

    def plot_data(self, data):
        if len(data):
            self.temporal_plot.plotData(data, "some name", None)


if __name__ == '__main__':
    app = wx.App()
    SimulationsVIew(None)
    app.MainLoop()
