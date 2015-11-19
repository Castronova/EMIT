import wx
import wx.propgrid as wxpg


class NetcdfDetailsView(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, id=-1, title=str("Netcdf file information"), pos=wx.DefaultPosition,
                          size=(650, 700), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        panel = wx.Panel(self)
        self.top_panel = wx.Panel(panel)
        self.bottom_panel = wx.Panel(panel)

        self.property_grid = MyPropertyGrid(self.top_panel, id=wx.ID_ANY, pos=wx.Point(0, 0), size=(500, 400))


        #  Makes the property grid fill the entire top panel
        hbox_top_panel = wx.BoxSizer(wx.HORIZONTAL)
        hbox_top_panel.Add(self.property_grid, 1, wx.EXPAND | wx.ALL, 2)
        self.top_panel.SetSizer(hbox_top_panel)

        #  Bottom Panel
        self.start_date = wx.DateTime_Now()
        vbox_bottom_panel = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(rows=6, cols=4, vgap=10, hgap=8)

        x_spatial_var = wx.StaticText(self.bottom_panel, label="X Spatial Variable:")
        self.x_spatial_var_combo = wx.ComboBox(self.bottom_panel, value="---")
        y_spatial_var = wx.StaticText(self.bottom_panel, label="Y Spatial Variable:")
        self.y_spatial_var_combo = wx.ComboBox(self.bottom_panel, value="---")
        time_var = wx.StaticText(self.bottom_panel, label="Time Variable:")
        self.time_var_combo = wx.ComboBox(self.bottom_panel, value="---")
        start_time = wx.StaticText(self.bottom_panel, label="Start Time:")
        self.startDatePicker = wx.DatePickerCtrl(self.bottom_panel, dt=self.start_date)
        time_unit = wx.StaticText(self.bottom_panel, label="Time Units:")
        self.time_step_combo = wx.ComboBox(self.bottom_panel, value="---")

        fgs.AddMany([x_spatial_var, self.x_spatial_var_combo, y_spatial_var, self.y_spatial_var_combo,
                     time_var, self.time_var_combo, start_time, self.startDatePicker,
                      time_unit, self.time_step_combo])

        vbox_bottom_panel.Add(fgs, 1, wx.EXPAND | wx.ALL, 10)

        self.bottom_panel.SetSizer(vbox_bottom_panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.top_panel, 1, wx.EXPAND | wx.ALL, 2)
        sizer.Add(self.bottom_panel, 1, wx.EXPAND | wx.ALL, 2)
        panel.SetSizer(sizer)

        self.Show()

class MyPropertyGrid(wx.propgrid.PropertyGrid):
    def __init__(self, *args, **kwargs):
        wxpg.PropertyGrid.__init__(self, *args, **kwargs)
