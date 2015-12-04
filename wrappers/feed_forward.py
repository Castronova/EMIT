__author__ = 'tonycastronova'

import stdlib
import wrappers
import datetime
from wrappers import base
from coordinator.emitLogging import elog
from dateutil import parser

class Wrapper(base.BaseWrapper):
    """
    Wrapper for models that feed/accept data to other models in the forward direction only. This type of model does
    not exchange data on every time step of simulation
    """

    def __init__(self, args):
        '''
        Initializes the base wrapper and basic model parameters
        :param args: dictionary of arguments.  Should contain timestep name, timestep value, model code,
        model description, general simulation_start, general simulation_end
        '''

        super(Wrapper, self).__init__()

        try:

            if 'time_step' in args.keys():
                dt = {args['time_step'][0]['name']: float(args['time_step'][0]['value'])}
                t = datetime.timedelta(**dt)
                self.time_step(t.total_seconds())
            else:
                elog.warning('Missing "time_step" parameters in *.mdl.  You may encounter errors if you continue')

            if 'model' in args.keys():
                self.name(args['model'][0]['code'])
                self.description(args['model'][0]['description'])
            else:
                elog.warning('Missing "model" parameters in *.mdl.  You may encounter errors if you continue')

            if 'general' in args:
                self.simulation_start(parser.parse(args['general'][0]['simulation_start']))
                self.simulation_end(parser.parse(args['general'][0]['simulation_end']))
            else:
                elog.warning('Missing "general" parameters in *.mdl.  You may encounter errors if you continue')

        except:
            elog.error('Malformed parameters found in *.mdl')


        self.status(stdlib.Status.READY)

    def type(self):
        return wrappers.Types.FEEDFORWARD

    def finish(self):
        pass

    def run(self,inputs):
        self.status(stdlib.Status.FINISHED)

    def prepare(self):
        '''
        Called before simulation run to prepare the model
        :return: READY status
        '''
        self.status(stdlib.Status.READY)
