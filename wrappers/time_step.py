__author__ = 'tonycastronova'

import datetime as dt
from utilities.status import Status
from stdlib import Geometry

class time_step_wrapper(object):

    def __init__(self, config_params):
        self.__params = config_params

        self.__outputs = {}
        self.__inputs = {}

        # set initial conditions
        self.__session = None

        self.__start_time = None
        self.__end_time = None
        self.__name = None
        self.__description = None
        self.__ts_value = None
        self.__ts_units = None

        self.__current_time = self.simulation_start()
        self.__status = Status.Loaded

        try:
            self.name(value=self.__params['model'][0]['code'])
            self.description(value=self.__params['model'][0]['description'])
        except:
            pass


    # def data_directory(self):
    #     raise NotImplementedError('This is an abstract method that must be implemented!')

    def save(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def run_timestep(self,inputs, current_time):
        raise NotImplementedError('This is an abstract method that must be implemented!')

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

    def time_step(self, value):
        """
        sets the simulation timestep
        :param value: timestep as a datetime object
        :return: timestep
        """

        if value is not None:
            self.__timestep = value
        return self.__timestep

    def outputs(self, value = None, name = None):

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

        # setter
        if value is not None:
            if name is None:
                for eitem in value:
                    self.__inputs[eitem.name()] = eitem
            else:
                self.__inputs[name] = value

        # getter
        return self.__inputs


    def simulation_start(self, value=None):

        if value is not None:
            self.__start_time = value
        else:
            return self.__start_time


        # ini configuration file
        # date_string = self.__params['general'][0]['simulation_start']
        # return dt.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S')


    def simulation_end(self, value=None):

        if value is not None:
            self.__end_time = value
        else:
            return self.__end_time

        # ini configuration file
        # date_string = self.__params['general'][0]['simulation_end']
        # return dt.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S')

    def name(self, value=None):

        if value is not None:
            self.__name = value
        else:
            return self.__name

        # ini configuration file
        #return self.__params['general'][0]['name']

    def description(self, value=None):

        if value is not None:
            self.__description = value
        else:
            return self.__description

        # ini configuration file
        # return self.__params['general'][0]['description']

    def current_time(self):
        if self.__current_time is None:
            self.__current_time = self.simulation_start()
        return self.__current_time

    def increment_time(self, step=None):
        """
        increments time
        :param step: the simulation timestep as a datetime object
        :return:  current time
        """

        if step is not None:

            # adjust the current time
            self.__current_time = self.current_time() + step

            if self.current_time() > self.simulation_end():
                self.status(Status.Finished)

            return self.current_time()



    def get_output_by_name(self,outputname=None):

        outputs = self.outputs()

        if outputs.has_key(outputname):
            return outputs[outputname]
        elif outputname == None:
            return outputs
        else:
            print 'Could not find output: %s' + outputname
            return None

    def set_output_by_name(self, outputname, value):
        outputs = self.outputs()

        for output in outputs:
            if output.name() == outputname:
                output = value

    def set_geom_values(self,variablename,geometry,datavalues):
        print '[deprecated] : this function has been replaced by time_step_wrapper.set_geom_values_by_hash'
        item = self.get_output_by_name(variablename)

        geometries = item.geometries()

        if type(geometry) == Geometry:
            for geom in geometries:
                if geom.geom().equals(geometry.geom()):
                    geom.datavalues().set_timeseries(datavalues)
                    return

        else:
            for geom in geometries:
                if geom.geom().equals(geometry):
                    geom.datavalues().set_timeseries(datavalues)
                    return
        raise Exception ('Error setting data for variable: %s' % variablename)

    def set_geom_values_by_hash(self,variablename,geometry,datavalues, append=False):

        item = self.get_output_by_name(variablename)

        geometries = item.geometries()

        if type(geometry) == Geometry:

            geom = next((x for x in geometries if x.hash() == geometry.hash()), None)
            if geom is not None:
                if append:
                    ts = geom.datavalues().timeseries()
                    if ts is not None:
                        ts.extend(datavalues)
                    else:
                        ts = datavalues
                    geom.datavalues().set_timeseries(ts)
                else:
                    geom.datavalues().set_timeseries(datavalues)

                return

        else:
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
