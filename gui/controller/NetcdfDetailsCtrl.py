import datetime as dt
import netCDF4 as nc
import wx
import wrappers
from coordinator import engineAccessors as engine
from gui.views.NetcdfDetailsView import NetcdfDetailsView


class NetcdfDetailsCtrl(NetcdfDetailsView):

    def __init__(self, parent, file, filename):
        self.fileurl = file
        NetcdfDetailsView.__init__(self, parent=parent)
        self.Title = "NetCDF Viewer --- " + filename
        self.variables = []

        self.populate_grid()

        # populate the combo boxes
        if len(self.variables) > 0:
            self.x_spatial_var_combo.AppendItems(self.variables)
            self.y_spatial_var_combo.AppendItems(self.variables)
            self.time_var_combo.AppendItems(self.variables)
        self.time_step_combo.AppendItems(['seconds', 'minutes', 'hours', 'days', 'years'])
        self.Bind(wx.EVT_BUTTON, self.addToCanvasBTn, self.add_to_canvas_btn)
        #
        self.time_step_combo.Bind(wx.EVT_COMBOBOX, self.checkComboBoxSelections)
        self.x_spatial_var_combo.Bind(wx.EVT_COMBOBOX, self.checkComboBoxSelections)
        self.y_spatial_var_combo.Bind(wx.EVT_COMBOBOX, self.checkComboBoxSelections)
        self.time_var_combo.Bind(wx.EVT_COMBOBOX, self.checkComboBoxSelections)
        self.SetSize((-1, 565))

    def checkComboBoxSelections(self, event):
        """
        enable/disable the add_to_canvas button based on the values of the combo boxes
        :return: None
        """
        if self.x_spatial_var_combo.Selection >= 0 and \
           self.y_spatial_var_combo.Selection >= 0 and \
           self.time_var_combo.Selection >= 0 and \
           self.time_step_combo.Selection >= 0:
            self.add_to_canvas_btn.Enable()
            return
        self.add_to_canvas_btn.Disable()

    def addToCanvasBTn(self, event):
        '''
        adds the netcdf resource to the canvas
        :param event:
        :return:
        '''

        x = self.x_spatial_var_combo.GetStringSelection()
        y = self.y_spatial_var_combo.GetStringSelection()
        t = self.time_var_combo.GetStringSelection()
        time_unit = self.time_step_combo.GetStringSelection()
        st = dt.datetime.strptime('%s'%(self.startDatePicker.GetValue().FormatISODate()), "%Y-%m-%d")

        args = dict(ncpath=self.fileurl,
                    tdim=t,
                    xdim=x,
                    ydim=y,
                    tunit=time_unit,
                    starttime=st,
                    type=wrappers.Types.NETCDF
                    )

        engine.addModel(attrib=args)

        # close the window
        self.Close()

    def populate_grid(self):
        self.ds = nc.Dataset(self.fileurl)
        section = 0
        self.property_grid.add_section("Global Attributes")
        for key, value in self.ds.__dict__.iteritems():
            self.property_grid.add_data_to_section(section, key, value)

        for key, value in self.ds.dimensions.iteritems():
            self.property_grid.add_section(key + " (dimensions)")
            section += 1
            self.property_grid.add_data_to_section(section, "size", len(value))
            self.property_grid.add_data_to_section(section, "is unlimited", value.isunlimited())

        self.variables = self.ds.variables.keys()

        for key, value in self.ds.variables.iteritems():
            self.property_grid.add_section(key + " (variable)")
            section += 1
            for k, v in value.__dict__.iteritems():
                self.property_grid.add_data_to_section(section, k, v)
