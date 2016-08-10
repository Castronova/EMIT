
import unittest
from coordinator.engine import Coordinator, Serializable
from coordinator import units
from utilities.models import parse_json
import numpy

class test_units(unittest.TestCase):

    def setUp(self):
        self.engine = Coordinator()
        pass

    def test_basic_conversion(self):

        # add models to engine
        mdl1 = '../../app_data/models/randomizer/randomizer.mdl'
        params = parse_json(mdl1)
        params.update({'id': 'm1', 'mdl': mdl1, 'model_type': 'mdl'})
        m1 = self.engine.add_model(**params)

        mdl2 = '../../app_data/models/multiplier/multiplier.mdl'
        params = parse_json(mdl2)
        params.update({'id': 'm2', 'mdl': mdl2, 'model_type': 'mdl'})
        m2 = self.engine.add_model(**params)

        self.assertTrue(m1)
        self.assertTrue(m2)
        self.assertTrue(len(self.engine.Models()) == 2)

        mi1 = m1.instance()
        mi2 = m2.instance()

        # run the model mi1
        mi1.run(inputs={})

        # get the oei and iei that will be mapped
        oei = mi1.outputs()['random POINT 1-10']
        outvals = numpy.array(oei.getValues2())
        iei = mi2.inputs()['some_value']


        converted_vals = units.convert_units(oei=oei, iei=iei, vals=outvals)


        print  'done'



