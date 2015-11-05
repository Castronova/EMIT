__author__ = 'tonycastronova'


import unittest
import wrappers
import stdlib
import datetime
from utilities import geometry

class testBaseWrapper(unittest.TestCase):

    def setUp(self):
        pass
        args = {}
        self.base = wrappers.BaseWrapper(args)

    def tearDown(self):
        pass

    def test_base_status(self):

        status = self.base.status()
        self.assertTrue(status == stdlib.Status.NOTREADY)

        self.base.status(stdlib.Status.READY)
        status = self.base.status()
        self.assertTrue(status == stdlib.Status.READY)

        self.base.status('IncorrectValue')
        status = self.base.status()
        self.assertTrue(status == stdlib.Status.READY)


    def test_base_time(self):
        start = self.base.simulation_start()
        self.assertTrue(start == None)

        current = self.base.current_time()
        self.assertTrue(current == None)

        end = self.base.simulation_end()
        self.assertTrue(end == None)

        st = datetime.datetime(2015, 1, 1, 12, 0, 0)
        et = datetime.datetime(2015, 3, 23, 12, 0, 0)
        ts = 60*60*24

        self.base.simulation_start(st)
        self.assertTrue(self.base.simulation_start() == st)
        self.assertTrue(self.base.current_time() == st)

        self.base.simulation_end(et)
        self.assertTrue(self.base.simulation_end() == et)

        self.base.time_step(ts)
        self.assertTrue(self.base.time_step() == ts)

        self.base.increment_time()
        self.assertTrue(self.base.current_time() != st)
        self.assertTrue(self.base.current_time() == (datetime.timedelta(seconds=ts) + st))

        # end time before start time
        et2 = datetime.datetime(2014, 3, 23, 12, 0, 0)
        self.base.simulation_end(et2)
        self.assertTrue(self.base.simulation_end() == et)

        # start time after end time
        st2 = datetime.datetime(2016, 3, 23, 12, 0, 0)
        self.base.simulation_start(st2)
        self.assertTrue(self.base.simulation_start() == st)

        st3 = '1/1/2014 12:00:00'
        et3 = '1/1/2015 12:00:00'
        self.base.simulation_start(st3)
        self.base.simulation_end(et3)
        self.assertTrue(self.base.simulation_start() == datetime.datetime.strptime(st3, '%m/%d/%Y %H:%M:%S') )
        self.assertTrue(self.base.simulation_end() == datetime.datetime.strptime(et3, '%m/%d/%Y %H:%M:%S') )

        st4 = 'invalid date'
        et4 = 'invalid date'
        self.base.simulation_start(st4)
        self.base.simulation_end(et4)
        self.assertTrue(self.base.simulation_start() == datetime.datetime.strptime(st3, '%m/%d/%Y %H:%M:%S') )
        self.assertTrue(self.base.simulation_end() == datetime.datetime.strptime(et3, '%m/%d/%Y %H:%M:%S') )


        pass

    def test_base_outputs(self):

        outputs = self.base.outputs()
        self.assertTrue(outputs == {})

        geom = geometry.fromWKT('POINT(1 2)')
        unit = stdlib.Unit()
        unit.UnitAbbreviation('cm')
        unit.UnitName('centimeters')
        var = stdlib.Variable()
        var.VariableNameCV('my variable')
        var.VariableDefinition('this is my variable definition')
        oei = stdlib.ExchangeItem(name = 'output1',
                            desc = 'my description',
                            unit = unit,
                            variable = var,
                            geometry = geom,
                            type = stdlib.ExchangeItemType.OUTPUT)
        outputs = self.base.outputs(oei)
        self.assertTrue(len(outputs.items()) == 1)

        # add duplicate
        outputs = self.base.outputs(oei)
        self.assertTrue(len(outputs.items()) == 1)

        # try to add an input type
        iei = stdlib.ExchangeItem(name = 'input1',
                            desc = 'my description',
                            unit = unit,
                            variable = var,
                            geometry = geom,
                            type = stdlib.ExchangeItemType.INPUT)
        outputs = self.base.outputs(iei)
        self.assertTrue(len(outputs.items()) == 1)


    def test_base_inputs(self):
        inputs = self.base.inputs()
        self.assertTrue(inputs == {})

        geom = geometry.fromWKT('POINT(1 2)')
        unit = stdlib.Unit()
        unit.UnitAbbreviation('cm')
        unit.UnitName('centimeters')
        var = stdlib.Variable()
        var.VariableNameCV('my variable')
        var.VariableDefinition('this is my variable definition')
        iei = stdlib.ExchangeItem(name = 'input1',
                            desc = 'my description',
                            unit = unit,
                            variable = var,
                            geometry = geom,
                            type = stdlib.ExchangeItemType.INPUT)
        outputs = self.base.inputs(iei)
        self.assertTrue(len(inputs.items()) == 1)

        # add duplicate
        outputs = self.base.inputs(iei)
        self.assertTrue(len(inputs.items()) == 1)

        # try to add output type
        oei = stdlib.ExchangeItem(name = 'output1',
                            desc = 'my description',
                            unit = unit,
                            variable = var,
                            geometry = geom,
                            type = stdlib.ExchangeItemType.OUTPUT)
        outputs = self.base.inputs(oei)
        self.assertTrue(len(inputs.items()) == 1)

    def test_base_name(self):

        self.assertTrue(self.base.name() == 'Unspecified')

        self.base.name('My Model')

        self.assertTrue(self.base.name() == 'My Model')

    def test_base_description(self):

        self.assertTrue(self.base.description() == 'No Description Provided')

        self.base.name('My Model Description')

        self.assertTrue(self.base.name() == 'My Model Description')



class testWofWrapper(unittest.TestCase):

    def test_wof_initialization(self):

        args = dict(network = 'iutah',
                    sitecode = 'LR_WaterLab_AA',
                    variable = 'RH_enc',
                    start = datetime.datetime(2015, 10, 26, 0, 0, 0),
                    end = datetime.datetime(2015, 10, 30, 0, 0, 0),
                    wsdl = 'http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL')


        model_wrapper = getattr(wrappers, wrappers.Types.WOF).Wrapper(args)


        self.assertTrue(model_wrapper.description() != 'No Description Provided')
        self.assertTrue(model_wrapper.name() != 'Unspecified')
        self.assertTrue(len(model_wrapper.outputs().keys()) > 0)
        self.assertTrue(model_wrapper.simulation_end() == args['end'])
        self.assertTrue(model_wrapper.simulation_start() == args['start'])

        # make sure date, values, and geometries are set correctly
        self.assertTrue(len(model_wrapper.outputs().values()[0].getValues2()) > 0)
        self.assertTrue(len(model_wrapper.outputs().values()[0].getDates2()) > 0)
        self.assertTrue(len(model_wrapper.outputs().values()[0].getGeometries2()) == 1)

