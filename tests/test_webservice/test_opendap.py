__author__ = 'tonycastronova'

import os
import unittest
import netCDF4 as nc

class testOpenDAP(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_info(self):
        ds = nc.Dataset('http://129.123.51.203:80/opendap/data/nc/air.mean.nc')
        self.assertTrue('time' in ds.dimensions.keys())
        self.assertTrue('lat' in ds.dimensions.keys())
        self.assertTrue('lon' in ds.dimensions.keys())
        self.assertTrue('air' in ds.variables.keys())
        self.assertTrue(ds.variables['air'].shape[0] == 662)


        ds = nc.Dataset('http://129.123.51.203:80/opendap/data/nc/historical_new/1986_new/wrfout_d01_1986-01-01_00:00:00.nc')
        self.assertTrue('Time' in ds.dimensions.keys())


    def test_subset(self):
        ds = nc.Dataset('http://129.123.51.203:80/opendap/data/nc/air.mean.nc?air[0:1:10][0][0]')
        self.assertTrue(ds.variables['air'].shape == (11,1,1))

        ds = nc.Dataset('http://129.123.51.203:80/opendap/data/nc/coads_climatology.nc?'
                        'AIRT[0:1:11][0][0],'
                        'UWND[0:1:11][0:1:5][0:1:5],'
                        'VWND[0:1:11][0:1:5][0:1:5]')
        self.assertTrue(ds.variables['AIRT'].shape == (12,1,1))
        self.assertTrue(ds.variables['UWND'].shape == (12,6,6))
        self.assertTrue(ds.variables['VWND'].shape == (12,6,6))



    def test_download(self):

        # grab a subset of the data
        dsin = nc.Dataset('http://129.123.51.203:80/opendap/data/nc/coads_climatology.nc?AIRT[0:1:10][0][0]')

        # create an output file
        dsout = nc.Dataset("air_subset.nc", "w")

        #Copy dimensions
        for dname, the_dim in dsin.dimensions.iteritems():
            dsout.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)

        # Copy variables
        for v_name, varin in dsin.variables.iteritems():

            # create the variable
            outVar = dsout.createVariable(v_name, varin.datatype, varin.dimensions)

            # copy variable attributes
            outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})

            # copy variable data
            outVar[:] = varin[:]

        # close the output file
        dsout.close()

        # reopen the output dataset and make sure it was created correctly
        ds = nc.Dataset('air_subset.nc')
        self.assertTrue('AIRT' in ds.variables.keys())
        self.assertTrue('TIME' in ds.dimensions.keys())
        self.assertTrue('COADSX' in ds.dimensions.keys())
        self.assertTrue('COADSY' in ds.dimensions.keys())
        self.assertTrue(ds.variables['AIRT'].shape == (11,1,1))
        os.remove('air_subset.nc')
