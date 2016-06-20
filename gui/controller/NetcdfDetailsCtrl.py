import datetime as dt

import netCDF4 as nc
import wx
import wx.propgrid as wxpg

import wrappers
from coordinator import engineAccessors as engine
from gui.views.NetcdfDetailsView import NetcdfDetailsView


class NetcdfDetailsCtrl(NetcdfDetailsView):

    def __init__(self, parent, file, filename):
        self.fileurl = file
        NetcdfDetailsView.__init__(self, parent=parent)
        self.Title = "NetCDF Viewer --- " + filename
        self.variables = []

        # populate the property grid
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

    def populateList(self):
        # connect to the selected netcdf file
        self.ds = nc.Dataset(self.fileurl)

        # get all of the attributes of this file and add them to the property grid
        keys = self.ds.__dict__.keys()
        g = self.property_grid.Append(wxpg.PropertyCategory("Global Attributes"))
        for key in keys:
            self.property_grid.Append(wxpg.StringProperty(str(key), value=str(self.ds.__dict__[key])))


        # get all of the dimension properties and add them to the property grid
        dims = self.ds.dimensions.keys()
        for dim in dims:
            self.property_grid.Append(wxpg.PropertyCategory(dim + ' (dimension)'))
            self.property_grid.Append(wxpg.StringProperty(label='size', name=dim+'_size', value=str(len(self.ds.dimensions[dim]))))
            self.property_grid.Append(wxpg.StringProperty(label='is unlimited', name=dim+'_isunlimited', value=str(self.ds.dimensions[dim].isunlimited())))

            try:
                drange = '%3.3f.....%3.3f' % (self.ds.variables[dim][0], self.ds.variables[dim][-1])
                self.property_grid.Append(wxpg.StringProperty(label='data range', name=dim+'_min', value=str(drange)))
            except:
                pass

        # get all of the variable properties and add them to the property grid
        self.variables = self.ds.variables.keys()
        for var in self.variables:
            g = self.property_grid.Append(wxpg.PropertyCategory(var +' (variable)'))
            info = self.ds.variables[var].__dict__.keys()
            for i in info:
                self.property_grid.Append(wxpg.StringProperty(label=str(i), name=str(var)+'_'+str(i), value=str(self.ds.variables[var].__dict__[i])))

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

        for key, value in self.ds.variables.iteritems():
            self.property_grid.add_section(key + " (variable)")
            section += 1
            for k, v in value.__dict__.iteritems():
                self.property_grid.add_data_to_section(section, k, v)
