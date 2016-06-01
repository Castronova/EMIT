import wx
from gui.controller.PlotForSiteViewerCtrl import PlotForSiteViewerCtrl


class NewView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        # Create panels
        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)
        bottom_panel = wx.Panel(panel, size=(-1, 250))

        ###############################
        # TOP PANEL COMPONENTS
        ###############################

        # Grid panel
        grid_panel = wx.Panel(top_panel)
        grid_panel.SetBackgroundColour(wx.RED)
        self.plot = PlotForSiteViewerCtrl(grid_panel)
        grid_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_panel_sizer.Add(self.plot.plot, 1, wx.EXPAND | wx.ALL)
        grid_panel.SetSizer(grid_panel_sizer)

        # Map panel
        map_panel = wx.Panel(top_panel)
        map_panel.SetBackgroundColour(wx.YELLOW)

        # Add grid and map panel to the top panel
        top_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_panel_sizer.Add(grid_panel, 1, wx.EXPAND | wx.ALL)
        top_panel_sizer.Add(map_panel, 1, wx.EXPAND | wx.ALL)
        top_panel.SetSizer(top_panel_sizer)

        ###############################
        # BOTTOM PANEL COMPONENTS
        ###############################
        bottom_panel.SetBackgroundColour(wx.BLUE)

        # Add panels to the frame
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(top_panel, 1, wx.EXPAND)
        frame_sizer.Add(bottom_panel, 0, wx.EXPAND)

        panel.SetSizer(frame_sizer)
        frame_sizer.Fit(self)

        self.Show()


if __name__ == '__main__':

    app = wx.App()

    NewView(None)

    app.MainLoop()
