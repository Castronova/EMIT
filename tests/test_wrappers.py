__author__ = 'tonycastronova'


import unittest
import wrappers
import stdlib
import datetime

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

    def test_base_start_end_times(self):
        pass

    def test_base_outputs(self):
        pass

    def test_base_inputs(self):
        pass

    def test_base_name(self):
        pass

    def test_base_description(self):
        pass

    def test_base_getoutput(self):
        pass

    def test_base_getinput(self):
        pass


class testWofWrapper(unittest.TestCase):
    pass

    # def test_wof(self):
    #
    #     type = wrappers.Types.WOF
    #
    #     model_wrapper = getattr(wrappers, "wof").wrapper()
    #
    #     d = model_wrapper.description()
    #
    #     network = 'iutah'
    #     sitecode = 'LR_WaterLab_AA'
    #     variable= 'RH_enc'
    #     start = '2015-10-26'
    #     end = '2015-10-30'
    #
    #     print 'here'