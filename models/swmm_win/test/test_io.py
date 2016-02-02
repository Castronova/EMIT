__author__ = 'tonycastronova'

# from examples.swmm.src import parse_swmm as ps
from os.path import *
import unittest
from models.swmm.src import parse_swmm as ps

class test_swmm(unittest.TestCase):


    def test_get_output(self):
        o =abspath(join(dirname(__file__),'../data/sim.out'))



        # get variables
        vars = ps.listvariables(o)

        for k, v in vars.iteritems():
            print k,v






