__author__ = 'tonycastronova'

import datetime as dt
from utilities.status import Status
import datatypes

class feed_forward_wrapper(object):
    def __init__(self, config_params):
        self.__params = config_params

        self.__outputs = {}
        self.__inputs = {}

        # set initial conditions
        self.__current_time = self.simulation_start()
        self.__session = None

        self.__status = Status.Loaded


    # def data_directory(self):
    #     raise NotImplementedError('This is an abstract method that must be implemented!')

    def type(self):
        return datatypes.ModelTypes.FeedForward

    def save(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def run(self,inputs):
        self.status(Status.Finished)

    # def initialize(self):
    #     raise NotImplementedError('This is an abstract method that must be implemented!')

    def session(self, value = None):
        if value is not None:
            self.__session = value
        return self.__session

    def prepare(self):
        '''
        Called before simulation run to prepare the model
        :return: READY status
        '''
        self.status(Status.Ready)

    def time_step(self):
        """
            ini configuration file
        """
        return (int(self.__params['time_step'][0]['value']),self.__params['time_step'][0]['unit_type_cv'])
        #raise NotImplementedError('This is an abstract method that must be implemented!')

    def outputs(self, value = None, name = None):
        # """
        #     ini configuration file
        # """
        # if self.__outputs is None:
        #     ei = utilities.build_exchange_items(self.__params)
        #     self.__outputs = [i for i in ei if i.get_type() == 'output' ]
        # return self.__outputs
        #
        # #raise NotImplementedError('This is an abstract method that must be implemented!')

        # setter
        if value is not None:
            if name is None:
                for eitem in value:
                    self.__outputs[eitem.name()] = eitem
            else:
                self.__outputs[name] = value

        # getter
        return self.__outputs



    def inputs(self, value = None, name = None):

        # todo: utilities should have a config parsing function that can be used to populate inputs and outputs

        # """
        #     ini configuration file
        # """
        # raise NotImplementedError('This is an abstract method that must be implemented!')

        # if value is not None:
        #     self.__inputs = value
        # return self.__inputs

        # setter
        if value is not None:
            if name is None:
                for eitem in value:
                    self.__inputs[eitem.name()] = eitem
            else:
                self.__inputs[name] = value

        # getter
        return self.__inputs


    def simulation_start(self):
        """
            ini configuration file
        """
        date_string = self.__params['general'][0]['simulation_start']
        return dt.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S')

        #raise NotImplementedError('This is an abstract method that must be implemented!')

    def simulation_end(self):
        """
            ini configuration file
        """
        date_string = self.__params['general'][0]['simulation_end']
        return dt.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S')
        #raise NotImplementedError('This is an abstract method that must be implemented!')

    def name(self):
        """
            ini configuration file
        """
        return self.__params['general'][0]['name']
        #raise NotImplementedError('This is an abstract method that must be implemented!')

    def description(self):
        """
            ini configuration file
        """
        return self.__params['general'][0]['description']
        #raise NotImplementedError('This is an abstract method that must be implemented!')

    def current_time(self):
        return self.__current_time

    def increment_time(self, time):

        value,unit = self.time_step()

        # if unit == 'millisecond': self.__current_time += dt.timedelta(milliseconds=value)
        # elif unit == 'second': self.__current_time +=  dt.timedelta(seconds =value)
        # elif unit == 'minute': self.__current_time +=  dt.timedelta(minutes=value)
        # elif unit == 'hour': self.__current_time +=  dt.timedelta(hours=value)
        # elif unit == 'day': self.__current_time +=  dt.timedelta(days=value)
        # else:
        #     raise Exception('Unknown unit: %s'%unit)

        if unit == 'milliseconds': time += dt.timedelta(milliseconds=value)
        elif unit == 'seconds': time +=  dt.timedelta(seconds =value)
        elif unit == 'minutes': time +=  dt.timedelta(minutes=value)
        elif unit == 'hours': time +=  dt.timedelta(hours=value)
        elif unit == 'days': time +=  dt.timedelta(days=value)
        else:
            raise Exception('Unknown unit: %s'%unit)

        return time


    def get_output_by_name(self,outputname):

        outputs = self.outputs()

        if outputs.has_key(outputname):
            return outputs[outputname]
        else:
            print 'Could not find output: %s' + outputname
            return None

        # for output in outputs:
        #     if output.name() == outputname:
        #         return output

        #raise Exception('Could not find output: %s' + outputname)

    def set_output_by_name(self, outputname, value):
        outputs = self.outputs()

        for output in outputs:
            if output.name() == outputname:
                output = value



    def set_geom_values(self,variablename,geometry,datavalues):

        item = self.get_output_by_name(variablename)

        geometries = item.geometries()
        for geom in geometries:
            if geom.geom().equals(geometry):
                geom.datavalues().set_timeseries(datavalues)
                return
        raise Exception ('Error setting data for variable: %s' % variablename)

    def get_input_by_name(self,inputname):

        inputs = self.inputs()

        for input in inputs:
            if input.name() == inputname:
                return input

        raise Exception('Could not find input: %s' + inputname)

    def status(self, value=None):
        if value is not None:
            self.__status = value
        return self.__status
