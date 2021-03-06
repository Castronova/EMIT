__author__ = 'tonycastronova'

import datetime as dt

class data_wrapper(object):
    def __init__(self,name, starttime, endtime, output, description=''):
        self.__output = output
        self.__start = starttime
        self.__end = endtime
        self.__name = name
        self.__desc = description

        # set initial conditions
        self.__current_time = self.simulation_start()

    def save(self):
        return self.__output

    def run(self,inputs):
        pass

    def time_step(self):
        """
            ini configuration file
        """
        #return (int(self.__params['time_step'][0]['value']),self.__params['time_step'][0]['unit_type_cv'])
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def outputs(self):
        """
            ini configuration file
        """
        # if self.__outputs is None:
        #     ei = utilities.build_exchange_items(self.__params)
        #     self.__outputs = [i for i in ei if i.get_type() == 'output' ]
        # return self.__outputs

        raise NotImplementedError('This is an abstract method that must be implemented!')

    def simulation_start(self):
        return self.__start


    def simulation_end(self):
        return self.__end

    def name(self):
        return self.__name

    def description(self):
        return self.__desc

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
        #
        # outputs = self.outputs()
        #
        # for output in outputs:
        #     if output.name() == outputname:
        #         return output
        #
        # raise Exception('Could not find output: %s' + outputname)
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def set_geom_values(self,variablename,geometry,datavalues):
        #
        # item = self.get_output_by_name(variablename)
        #
        # geometries = item.geometries()
        # for geom in geometries:
        #     if geom.geom().equals(geometry):
        #         geom.datavalues().set_timeseries(datavalues)
        #         return
        # raise Exception ('Error setting data for variable: %s' % variablename)
        raise NotImplementedError('This is an abstract method that must be implemented!')