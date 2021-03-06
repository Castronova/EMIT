__author__ = 'tonycastronova'

import datetime as dt
from api_old.ODM2.Core.services import readCore
from api_old.ODM2.Results.services import readResults
# from shapely import wkb
import stdlib, uuid
from utilities.status import Status
import datatypes
from utilities import geometry

class odm2(object):
    def __init__(self,resultid, session):



        # get result object and result timeseries
        core = readCore(session)
        obj = core.getResultByID(resultID=int(resultid))
        readres = readResults(session)
        results = readres.getTimeSeriesValuesByResultId(resultId=int(resultid))

        # separate the date and value pairs in the timeseries
        dates = [date.ValueDateTime for date in results]
        values = [val.DataValue for val in results]

        # basic exchange item info
        id = uuid.uuid4().hex[:8]
        name = obj.VariableObj.VariableCode
        desc = obj.VariableObj.VariableDefinition
        #unit = obj.UnitObj.UnitsName
        #vari = obj.VariableObj.VariableNameCV
        type = stdlib.ExchangeItemType.OUTPUT
        start = min(dates)
        end = max(dates)

        # build variable
        variable = stdlib.Variable()
        variable.VariableDefinition(obj.VariableObj.VariableDefinition)
        variable.VariableNameCV(obj.VariableObj.VariableNameCV)

        # build unit
        unit = stdlib.Unit()
        unit.UnitAbbreviation(obj.UnitObj.UnitsAbbreviation)
        unit.UnitName(obj.UnitObj.UnitsName)
        unit.UnitTypeCV(obj.UnitObj.UnitsTypeCV)

        # build geometries
        # todo: need to specify srs and elevation
        wkb = str(obj.FeatureActionObj.SamplingFeatureObj.FeatureGeometry.data)
        geom = geometry.fromWKB(wkb)

        # build exchange item object
        oei = stdlib.ExchangeItem(id=id,
                                   name=name,
                                   desc=desc,
                                   geometry=geom,
                                   unit=unit,
                                   variable=variable,type=type )


        # set global parameters
        self.__id = id
        self.__name = name
        self.__start=start
        self.__end=end
        self.__output={self.__name: oei}
        self.__desc=obj.VariableObj.VariableDefinition
        self.__current_time = self.simulation_start()
        self.__obj = obj
        self.__resultid = obj.ResultID
        self.__session = session
        self.__status = Status.Loaded

    def type(self):
        return datatypes.ModelTypes.Data

    def save(self):
        #return [self.get_output_by_name(outputname=self.name())]
        #return [self.__output]
        return []

    def run(self,inputs):
        # set the status to finished
        self.status(Status.Finished)

    def run_timestep(self,inputs,time):
        # set the status to finished
        self.status(Status.Finished)

    def prepare(self):
        '''
        Called before simulation run to prepare the model
        :return: READY status
        '''


        # query the database
        #return [self.get_output_by_name(outputname=self.name())]


        self.status(Status.Ready)

    def session(self):
        return self.__session

    def obj(self):
        return self.__obj
    #
    # def actionid(self):
    #     return self.__actionid

    def resultid(self):
        return self.__resultid

    def id(self):
        return self.__id

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
        return self.__output

    def inputs(self):
        return {}

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

        if unit == 'millisecond': time += dt.timedelta(milliseconds=value)
        elif unit == 'second': time +=  dt.timedelta(seconds =value)
        elif unit == 'minute': time +=  dt.timedelta(minutes=value)
        elif unit == 'hour': time +=  dt.timedelta(hours=value)
        elif unit == 'day': time +=  dt.timedelta(days=value)
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

        #return [self.__output]
        #
        # outputs = self.outputs()
        #
        # for output in outputs:
        #     if output.name() == outputname:
        #         return output
        #
        # raise Exception('Could not find output: %s' + outputname)
        #raise NotImplementedError('This is an abstract method that must be implemented!')

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

    def status(self, value=None):
        if value is not None:
            self.__status = value
        return self.__status