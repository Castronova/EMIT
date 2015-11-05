__author__ = 'tonycastronova'


import datetime as dt
import stdlib
import dateutil.parser as dtparser

class BaseWrapper(object):

    def __init__(self, params):

        self.__params = params
        self.__outputs = {}
        self.__inputs = {}

        # set initial conditions
        # todo: is session needed?
        self.__session = None

        self.__timestep_in_seconds = 5 * 60
        self.__simulation_start_dt = None
        self.__simulation_end_dt = None
        self.__current_time = self.__simulation_start_dt
        self.__name = "Unspecified"
        self.__description = "No Description Provided"
        self.__status =  stdlib.Status.NOTREADY

    def prepare(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def type(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')
        # return datatypes.ModelTypes.FeedForward

    def run(self,inputs):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def finish(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')


    def status(self, value = None):
        if value is not None:
            try:
                if getattr(stdlib.Status, value):
                    self.__status = value
            except AttributeError:
                pass
        return self.__status

    # todo: is this really needed?
    def session(self, value = None):
        if value is not None:
            self.__session = value
        return self.__session

    def time_step(self, timestepinseconds = None):

        if timestepinseconds is not None:
            self.__timestep_in_seconds = timestepinseconds
        return self.__timestep_in_seconds


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


    def simulation_start(self, value = None):
        """
        Getter/Setter for simulation start date times
        :param value: datetime or string representation of datetime
        :return: simulation start datetime
        """

        if value is not None:

            # try to parse datetime string
            if not isinstance(value, dt.datetime):
                try:
                    value = dtparser.parse(value)
                except:
                    return self.__simulation_start_dt

            if self.__simulation_end_dt is not None:
                # check that start time is before end time
                if (self.__simulation_end_dt - value).total_seconds() > 0:
                    self.__simulation_start_dt = value

                    # set the current time
                    self.__current_time = value
            else:
                # set the value b/c end-start cannot be evaluated
                self.__simulation_start_dt = value

                # set the current time
                self.__current_time = value

        return self.__simulation_start_dt

    def simulation_end(self, value = None):
        """
        Getter/Setter for simulation end date times
        :param value: datetime or string representation of datetime
        :return: simulation end datetime
        """

        if value is not None:

            # try to parse datetime string
            if not isinstance(value, dt.datetime):
                try:
                    value = dtparser.parse(value)
                except:
                    return self.__simulation_end_dt

            if self.__simulation_start_dt is not None:
                # check that end time is after start time
                if  (value - self.__simulation_start_dt).total_seconds() > 0:
                    self.__simulation_end_dt = value
            else:
                # set the value b/c end-start cannot be evaluated
                self.__simulation_end_dt = value
        return self.__simulation_end_dt

    def name(self, value = None):
        if value is not None:
            self.__name = value
        return self.__name

    def description(self, value = None):
        if value is not None:
            self.__description = value
        return self.__description

    def current_time(self):
        return self.__current_time

    def increment_time(self):

        # get the current time
        time = self.current_time()

        # get the timestep in seconds
        ts_in_seconds = self.time_step()

        # calculate the new time
        time += dt.timedelta(seconds = ts_in_seconds)

        # update the current time
        self.__current_time = time



    # todo: is this really needed?
    def get_output(self, outputname):

        outputs = self.outputs()

        if outputs.has_key(outputname):
            return outputs[outputname]
        else:
            print 'Could not find output: %s' + outputname
            return None

    # todo: is this really needed?
    def get_input(self,inputname):

        inputs = self.inputs()

        for input in inputs:
            if input.name() == inputname:
                return input

        raise Exception('Could not find input: %s' + inputname)

