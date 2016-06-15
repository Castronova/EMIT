import wx

from gui.Models.CustomListCtrl import CustomListCtrl
from gui.Models.SpatialTemporalPlotter import SpatialTemporalPlotter


class SimulationsPlotView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        # Create panels
        panel = wx.Panel(self)
        top_panel = wx.Panel(panel, size=(1050, 450))
        middle_panel = wx.Panel(panel)
        bottom_panel = wx.Panel(panel, size=(-1, 250))

        ###############################
        # TOP PANEL COMPONENTS
        ###############################

        # Create components
        self.spatial_plot = SpatialTemporalPlotter(top_panel)
        self.temporal_plot = SpatialTemporalPlotter(top_panel)

        # Allows the plots to size equally
        self.spatial_plot.plot.SetMinSize(wx.Size(1, 1))
        self.temporal_plot.plot.SetMinSize(wx.Size(1, 1))

        # Create sizer and add components to sizer
        top_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_panel_sizer.Add(self.spatial_plot.plot, 1, wx.EXPAND | wx.ALL, 2)
        top_panel_sizer.Add(self.temporal_plot.plot, 1, wx.EXPAND | wx.ALL, 2)

        top_panel.SetSizer(top_panel_sizer)
        top_panel_sizer.Fit(top_panel)

        ###############################
        # MIDDLE PANEL COMPONENTS
        ###############################

        # Create components
        start_date_text = wx.StaticText(middle_panel, label="Start")
        self.start_date_picker = wx.DatePickerCtrl(middle_panel)
        end_date_text = wx.StaticText(middle_panel, label="End")
        self.end_date_picker = wx.DatePickerCtrl(middle_panel)
        self.plot_button = wx.Button(middle_panel, label="Plot")
        self.export_button = wx.Button(middle_panel, label="Export")

        # Create sizer and add components to sizer
        middle_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        middle_panel_sizer.Add(start_date_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(self.start_date_picker, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(end_date_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(self.end_date_picker, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(self.plot_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        middle_panel_sizer.Add(self.export_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)

        middle_panel.SetSizer(middle_panel_sizer)
        middle_panel_sizer.Fit(middle_panel)

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
        self.CenterOnScreen()
        self.Show()
