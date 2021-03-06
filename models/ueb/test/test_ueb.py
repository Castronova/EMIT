__author__ = 'tonycastronova'



import unittest
from models.ueb import ueb
from utilities.gui import parse_config
import wrappers
from coordinator.engine import Coordinator
import time
from transform import space

class testUEB(unittest.TestCase):


    def setup(self):
        pass

    def test_run(self):

        # intialize ueb
        mdl = '../ueb.mdl'
        config_params = parse_config(mdl)
        UEB = ueb.ueb(config_params)

        # run
        UEB.run(None)

        # finish
        UEB.save()

        print 'done'

    def test_geometry_creation_and_ordering(self):

        # intialize ueb
        mdl = '../ueb.mdl'
        config_params = parse_config(mdl)
        UEB = ueb.ueb(config_params)

        # get the active cells (these are looped through in run)
        cells = UEB.activeCells

        # build geometries
        xdim = UEB.C_dimlen1.value
        ydim = UEB.C_dimlen2.value
        geoms = UEB.build_geometries(range(xdim), range(ydim))

        # create point tuples from geoms
        pts = [ (int(g.GetX()), int(g.GetY())) for g in geoms]

        # make sure the ordering is correct
        self.assertTrue(cells == pts)




    def test_netcdf_input(self):
        engine = Coordinator()


        args = dict(ncpath = './TWDEF_distributed/prcp.nc',
                    tdim = 'time',
                    xdim = 'x',
                    ydim = 'y',
                    tunit = 'hours',
                    starttime = '10-26-2015 00:00:00',
                    type = wrappers.Types.NETCDF)



        # add the WaterOneFlow component to the engine
        engine.add_model(id=1234, attrib=args)

        # load ueb component
        mdl = '../ueb.mdl'
        args = dict(mdl = mdl)
        # config_params = parse_config(mdl)
        engine.add_model(id=1235, attrib=args)

        # assert that the models have been added correctly
        models = engine.get_all_models()
        self.assertTrue(len(models) == 2)

        spatial_interpolation = space.spatial_nearest_neighbor()


         # add a link from NetCDF to UEB
        netcdf = engine.get_output_exchange_items_summary(id=1234)
        ueb = engine.get_input_exchange_items_summary(id=1235)
        engine.add_link(from_id=1234, from_item_id = netcdf[0]['name'],
                        to_id=1235, to_item_id = ueb[0]['name'],
                        spatial_interp=spatial_interpolation,
                        temporal_interp=None,
                        uid=None)

        links = engine.get_all_links()
        self.assertTrue(len(links) == 1)

        # run the simulation
        engine.run_simulation()



        print 'done'