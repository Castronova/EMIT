__author__ = 'Ryan'

from gui.views.NASViewer import NASViewer
import wx
import netCDF4 as nc
import wx.propgrid as wxpg

class NASCtrl(NASViewer):

    def __init__(self, parent, file):
        self.fileurl = file
        NASViewer.__init__(self, parent=parent)
        g = self.property_grid.Append(wxpg.PropertyCategory("test"))
        self.property_grid.Append(wxpg.StringProperty(str(file), value=str("oops")))
        self.populateList()
        self.last = " "

    def populateList(self):
        alreadyUsed = {}
        self.ds = nc.Dataset(self.fileurl)
        keys =  self.ds.__dict__.keys()
        g = self.property_grid.Append(wxpg.PropertyCategory("Global Attributes"))
        for key in keys:
            print self.ds.__dict__[key]
            self.property_grid.Append(wxpg.StringProperty(str(key), value=str(self.ds.__dict__[key])))
        variables = self.ds.variables.keys()
        for var in variables:
            g = self.property_grid.Append(wxpg.PropertyCategory(var))
            info = self.ds.variables[var].__dict__.keys()
            for i in info:
                if i in alreadyUsed:
                    self.property_grid.Append(wxpg.StringProperty(str(i + alreadyUsed[i]), value=str(self.ds.variables[var].__dict__[i])))
                    alreadyUsed[i] += " "
                else:
                    self.property_grid.Append(wxpg.StringProperty(str(i), value=str(self.ds.variables[var].__dict__[i])))
                    alreadyUsed[i] = " "
