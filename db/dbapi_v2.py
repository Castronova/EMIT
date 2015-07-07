import datetime
import uuid
import numpy
import time

__author__ = 'mike'
# This is our API for simulation data that uses the latest ODM2PythonAPI code

from api_old.ODM2.Core.services import *
from api_old.ODM2.SamplingFeatures.services import *
from api_old.ODM2.Results.services import *
from api_old.ODM2.Simulation.services import *
from utilities import gui

from ODM2PythonAPI.src.api.ODMconnection import dbconnection
from ODM2PythonAPI.src.api.ODM2.services.readService import ReadODM2
from ODM2PythonAPI.src.api.ODM2.services.createService import CreateODM2
from ODM2PythonAPI.src.api.ODM2.services.updateService import UpdateODM2
from ODM2PythonAPI.src.api.ODM2.services.deleteService import DeleteODM2
from ODM2PythonAPI.src.api.ODM2 import models

class sqlite():

    def __init__(self, sqlitepath):
        self.connection = dbconnection.createConnection('sqlite', sqlitepath)
        self.read = ReadODM2(self.connection)
        self.write = CreateODM2(self.connection)
        self.update = UpdateODM2(self.connection)
        self.delete = DeleteODM2(self.connection)

    def create_user(self, userInfo):
        self.write.createPerson(userInfo['firstName'], userInfo['lastName'])
        print "in create_user"

    def create_organization(self, organInfo):
        self.write.createOrganization(organInfo['cvType'], organInfo['code'], organInfo['name'],
                                      organInfo['desc'], organInfo['link'], organInfo['parentOrgId'])

    def create_input_dataset(self, connection, resultids,type,code="",title="",abstract=""):
        pass

    def create_simulation(self, odm2_affiliation, config_params, ei):

        name = config_params['name']
        description = config_params['description']
        simstart = config_params['simulation_start']
        simend = config_params['simulation_end']
        modelcode = config_params['code']
        modelname = config_params['name']
        modeldesc = config_params['description']
        timestepvalue = config_params['value']
        timestepunittype = config_params['unit_type_cv']

        # create person / organization / affiliation
        # affiliation = self.set_user_preferences(preferences_path)

        # get the timestep unit id
        #todo: This is not returning a timestepunit!!!  This may need to be added to the database
        timestepunit = self.read.getUnitByName(timestepunittype)

        # create method
        method = self.read.getMethodByCode('simulation')
        org_id = odm2_affiliation[0].OrganizationID if len(odm2_affiliation) > 0 else None
        if not method: method = self.write.createMethod(code= 'simulation',
                                                             name='simulation',
                                                             vType='calculated',
                                                             orgId=org_id,
                                                             description='Model Simulation Results')


        # create action
        action = self.write.createAction(type='Simulation',
                                              methodid=method.MethodID,
                                              begindatetime=datetime.datetime.now(),
                                              begindatetimeoffset=int((datetime.datetime.now() - datetime.datetime.utcnow() ).total_seconds()/3600))

        # create actionby
        aff_id = odm2_affiliation[0].AffiliationID if len(odm2_affiliation) > 0 else None
        actionby = self.write.createActionBy(actionid=action.ActionID,
                                             affiliationid=aff_id)

        # create processing level
        processinglevel = self.read.getProcessingLevelByCode(processingCode=2)
        if not processinglevel: processinglevel = self.write.createProcessingLevel(code=2,
                                                                      definition='Derived Product',
                                                                      explanation='Derived products require scientific and technical interpretation and include multiple-sensor data. An example might be basin average precipitation derived from rain gages using an interpolation procedure.')

        # create dataset
        dataset = self.write.createDataset(dstype='Simulation Input',
                                                dscode='Input_%s'%name,
                                                dstitle='Input for Simulation: %s'%name,
                                                dsabstract=description)



        tsvalues = []

        # make sure the exchange item is represented as a list
        if not hasattr(ei,'__len__'):
            ei = [ei]

        # loop over output exchange items
        for e in ei:


            geometries = numpy.array(e.getGeometries2())
            dates = numpy.array(e.getDates2())
            datavalues = numpy.array( e.getValues2())

            # create variable
            # TODO: This is not correct!
            # todo: implement variable vType
            variable = self.read.getVariableByCode(e.variable().VariableNameCV())
            if not variable: variable = self.write.createVariable(code=e.variable().VariableNameCV(),
                                                                       name=e.variable().VariableDefinition(),
                                                                       vType='unknown',
                                                                       nodv=-999)

            # create unit
            unit = self.read.getUnitByName(e.unit().UnitName())
            if not unit: unit = self.write.createUnit(type=e.unit().UnitTypeCV(),
                                                           abbrev=e.unit().UnitAbbreviation(),
                                                           name=e.unit().UnitName())

            # create spatial reference
            srs = geometries[0].srs()  # get the srs from the first element
            # todo: Can geometries have difference srs in the same exchange item?  Something needs to check for this.  Should srs be at the exchange item level?
            refcode = "%s:%s" %(srs.GetAttrValue("AUTHORITY", 0), srs.GetAttrValue("AUTHORITY", 1))
            spatialref = self.read.getSpatialReferenceByCode(refcode)
            if not spatialref:
                spatialref = self.write.createSpatialReference(srsCode=refcode,
                                                               srsName=srs.GetAttrValue("GEOGCS", 0),
                                                               srsDescription="%s|%s|%s"%(srs.GetAttrValue("PROJCS", 0),
                                                                                          srs.GetAttrValue("GEOGCS", 0),
                                                                                          srs.GetAttrValue("DATUM", 0)))


            '''
            >>> exchangeitem.getGeometries2()
            >>> exchangeitem.getDates2()
            >>> didx, date = zip(*exchangeitem.getDates2())
            >>> vals = exchangeitem.getValues2()

            >>> import numpy
            >>> v = numpy.array(vals)
            >>> type(v)
            <type 'numpy.ndarray'>
            >>> v[:,0]
            '''

            # timer for benchmarking
            st = time.time()

            # loop over geometries
            for i in range(0, len(geometries)):


                geom = geometries[i].geom()
                values = datavalues[:,i]   # all dates for geometry(i)



                # dates,values = geometry.datavalues().get_dates_values()




                # create sampling feature
                samplingfeature = self.read.getSamplingFeatureByGeometry(geom.wkt)
                if not samplingfeature: samplingfeature = self.write.createSamplingFeature(code=uuid.uuid4().hex,
                                                                                                vType="site",
                                                                                                name=None,
                                                                                                description=None,
                                                                                                geoType=geom.geom_type,
                                                                                                elevation=None,
                                                                                                elevationDatum=None,
                                                                                                featureGeo=geom.wkt)



                # create feature action
                featureaction = self.write.createFeatureAction(samplingfeatureid=samplingfeature.SamplingFeatureID,
                                                                    actionid=action.ActionID)






                result = models.Results
                result.ResultUUID = uuid.uuid4().hex
                result.FeatureActionID = featureaction.FeatureActionID
                result.ResultTypeCV = 'time series'
                result.VariableID = variable.VariableID
                result.UnitsID = unit.UnitsID
                result.ProcessingLevelID = processinglevel.ProcessingLevelID
                result.ValueCount = len(dates)
                result.SampledMediumCV = 'unknown'


                # create time series result
                timeseriesresult = self.write.createTimeSeriesResult(result=result, aggregationstatistic='unknown',
                                                                         timespacing=timestepvalue,
                                                                         timespacing_unitid=timestepunit.UnitsID)


                # create time series result values
                # todo: consider utc offset for each result value.
                # todo: get timezone based on geometry, use this to determine utc offset
                # todo: implement censorcodecv
                # todo: implement qualitycodecv
                # timeseriesresultvalues = self._reswrite.createTimeSeriesResultValues(resultid=timeseriesresult.ResultID,
                #                                                                      datavalues=values,
                #                                                                      datetimes=dates,
                #                                                                      datetimeoffsets=[-6 for i in range(len(dates))],
                #                                                                      censorcodecv='nc',
                #                                                                      qualitycodecv='unknown',
                #                                                                      timeaggregationinterval=timestepvalue,
                #                                                                      timeaggregationunit=timestepunit.UnitsID)


                #st = time.time()
                for i in xrange(len(values)):
                    tsrv = models.TimeSeriesResultValues()
                    tsrv.ResultID = timeseriesresult.ResultID
                    tsrv.CensorCodeCV = 'nc'
                    tsrv.QualityCodeCV = 'unknown'
                    tsrv.TimeAggregationInterval = timestepvalue
                    tsrv.TimeAggregationIntervalUnitsID = timestepunit.UnitsID
                    tsrv.DataValue = values[i]
                    tsrv.ValueDateTime = dates[i]
                    tsrv.ValueDateTimeUTCOffset = -6
                    tsvalues.append(tsrv)
                #print '\nBuilding TSRV: %3.5f sec' % (time.time() - st)

        #print '\nBuilding All Exchange Item TSRV:  %3.5f sec' % (time.time() - st)

        #st = time.time()
        # insert ts values
        self.write.createTimeSeriesResultValues(tsrv = tsvalues)

        # create model
        model = self.read.getModelByCode(modelcode=modelcode)
        if not model: model = self.write.createModel(code=modelcode,
                                                           name=modelname,
                                                           description=modeldesc)


        # create simulation

        #start = min([i.getStartTime() for i in output_exchange_items])
        #end = max([i.getEndTime() for i in output_exchange_items])

        # TODO: remove hardcoded time offsets!
        sim = self.write.createSimulation(actionid=action.ActionID,
                                              modelID=model.ModelID,
                                              simulationName=name,
                                              simulationDescription=description,
                                              simulationStartDateTime=simstart ,
                                              simulationStartOffset=-6,
                                              simulationEndDateTime=simend,
                                              simulationEndOffset=-6,
                                              timeStepValue =timestepvalue,
                                              timeStepUnitID=timestepunit.UnitsID,
                                              inputDatasetID=dataset.DataSetID)

        return sim


    # def get_simulation_results(self,simulationName, dbactions, from_variableName, from_unitName, to_variableName, startTime, endTime):
    #     pass



# from api_old.ODM2 import serviceBase
# from api_old.ODM2.Core.model import *
# from api_old.ODM2.Results.model import *
# from api_old.ODM2.Simulation.model import *

# class utils(serviceBase):
#
#     def getAllSeries(self):
#         pass
#
#     def getAllSimulations(self):
#         pass





