__author__ = 'Ryan'

from gui.views.NetcdfDetailsView import NetcdfDetailsView
import wx
import netCDF4 as nc
import wx.propgrid as wxpg

class NetcdfDetailsCtrl(NetcdfDetailsView):

    def __init__(self, parent, file):
        self.fileurl = file
        NetcdfDetailsView.__init__(self, parent=parent)

        self.variables = []

        # populate the property grid
        self.populateList()

        # populate the combo boxes
        if len(self.variables) > 0:
            self.x_spatial_var_combo.AppendItems(self.variables)
            self.y_spatial_var_combo.AppendItems(self.variables)
            self.time_var_combo.AppendItems(self.variables)
        self.time_step_combo.AppendItems(['days', 'minutes', 'seconds', 'years'])
        self.Bind(wx.EVT_BUTTON, self.addToCanvasBTn, self.download_btn)

    def addToCanvasBTn(self, event):
        wx.MessageBox("1234567890SEARCHME0987654321W")

    def populateList(self):
        alreadyUsed = {}

        # connect to the selected netcdf file
        self.ds = nc.Dataset(self.fileurl)

        # get all of the attributes of this file and add them to the property grid
        keys =  self.ds.__dict__.keys()
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
            except: pass

        # get all of the variable properties and add them to the property grid
        self.variables = self.ds.variables.keys()
        for var in self.variables:
            g = self.property_grid.Append(wxpg.PropertyCategory(var +' (variable)'))
            info = self.ds.variables[var].__dict__.keys()
            for i in info:
                self.property_grid.Append(wxpg.StringProperty(label=str(i), name=str(var)+'_'+str(i), value=str(self.ds.variables[var].__dict__[i])))


