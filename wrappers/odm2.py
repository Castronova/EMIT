__author__ = 'tonycastronova'

import wrappers
import stdlib
from wrappers import base
from utilities import geometry
from utilities.status import Status
from api_old.ODM2.Core.services import readCore
from api_old.ODM2.Results.services import readResults

class wrapper(base.BaseWrapper):


    def __init__(self, args):
        super(wrapper, self).__init__()
        self.args = args

        session = self.args['session']
        resultid = self.args['resultid']

        # get result object and result timeseries
        core = readCore(session)
        obj = core.getResultByID(resultID=int(resultid))
        readres = readResults(session)
        results = readres.getTimeSeriesValuesByResultId(resultId=int(resultid))

        # separate the date and value pairs in the timeseries
        dates = [date.ValueDateTime for date in results]
        values = [val.DataValue for val in results]

        # basic exchange item info
        name = obj.VariableObj.VariableCode
        desc = obj.VariableObj.VariableDefinition
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
        oei = stdlib.ExchangeItem( name=name,
                                   desc=desc,
                                   geometry=geom,
                                   unit=unit,
                                   variable=variable,type=type )


        # set global parameters
        self.name(name)
        self.simulation_start(start)
        self.simulation_end(end)
        self.outputs(name=name, value=oei)
        self.description(obj.VariableObj.VariableDefinition)
        self.current_time(start)
        # self.__obj = obj
        # self.__resultid = obj.ResultID
        # self.__session = session

        # set model status
        self.status(Status.Loaded)



    def type(self):
        return wrappers.Types().ODM2

    def finish(self):
        return

    def prepare(self):
        self.status(Status.Ready)

    def run(self, inputs):
        self.status(Status.Finished)

