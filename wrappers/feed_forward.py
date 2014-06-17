__author__ = 'tonycastronova'

import datetime as dt
import utilities

class feed_forward_wrapper(object):
    def __init__(self, config_params):
        self.__params = config_params

        self.__outputs = None
        self.__inputs = None

        # set initial conditions
        self.__current_time = self.simulation_start()

    def data_directory(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def save(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def run(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def initialize(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def time_step(self):
        """
            ini configuration file
        """
        return (int(self.__params['time_step'][0]['value']),self.__params['time_step'][0]['unit_type_cv'])
        #raise NotImplementedError('This is an abstract method that must be implemented!')

    def outputs(self):
        """
            ini configuration file
        """
        if self.__outputs is None:
            ei = utilities.build_exchange_items(self.__params)
            self.__outputs = [i for i in ei if i.get_type() == 'output' ]
        return self.__outputs

        #raise NotImplementedError('This is an abstract method that must be implemented!')

    def inputs(self):
        """
            ini configuration file
        """
        raise NotImplementedError('This is an abstract method that must be implemented!')

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

    def increment_time(self):

        value,unit = self.time_step()

        if unit == 'millisecond': self.__current_time += dt.timedelta(milliseconds=value)
        elif unit == 'second': self.__current_time +=  dt.timedelta(seconds =value)
        elif unit == 'minute': self.__current_time +=  dt.timedelta(minutes=value)
        elif unit == 'hour': self.__current_time +=  dt.timedelta(hours=value)
        elif unit == 'day': self.__current_time +=  dt.timedelta(days=value)
        else:
            raise Exception('Unknown unit: %s'%unit)
