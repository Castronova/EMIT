__author__ = 'mike'

import datetime
import uuid
import numpy
import time
import pyspatialite.dbapi2 as spatialite
import pandas

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

        # build sqlalchemy connection
        self.connection = dbconnection.createConnection('sqlite', sqlitepath)

        # create read, write, update, and delete ODM2PythonAPI instances
        self.read = ReadODM2(self.connection)
        self.write = CreateODM2(self.connection)
        self.update = UpdateODM2(self.connection)
        self.delete = DeleteODM2(self.connection)

        # create connection using spatialite for custom sql queries
        self.spatial_connection = spatialite.connect(sqlitepath)
        self.spatialDb = self.spatial_connection.cursor()

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
        simstart = datetime.datetime.strptime(config_params['simulation_start'], '%m/%d/%Y %H:%M:%S' )
        simend = datetime.datetime.strptime(config_params['simulation_end'], '%m/%d/%Y %H:%M:%S' )
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
            srs = e.srs()
            refcode = "%s:%s" %(srs.GetAttrValue("AUTHORITY", 0), srs.GetAttrValue("AUTHORITY", 1))
            spatialref = self.read.getSpatialReferenceByCode(refcode)
            if not spatialref:
                spatialref = self.write.createSpatialReference(srsCode=refcode,
                                                               srsName=srs.GetAttrValue("GEOGCS", 0),
                                                               srsDescription="%s|%s|%s"%(srs.GetAttrValue("PROJCS", 0),
                                                                                          srs.GetAttrValue("GEOGCS", 0),
                                                                                          srs.GetAttrValue("DATUM", 0)))

            # loop over geometries
            for i in range(0, len(geometries)):


                geom = geometries[i].geom()
                values = datavalues[:,i]   # all dates for geometry(i)

                # create sampling feature
                samplingfeature = self.read.getSamplingFeatureByGeometry(geom.wkt)
                if not samplingfeature:
                    samplingFeatureID = self.insert_sampling_feature(type='site',geometryType=geom.type, WKTgeometry=geom.wkt)


                # create feature action
                featureaction = self.write.createFeatureAction(samplingfeatureid=samplingFeatureID,
                                                                    actionid=action.ActionID)

                # create a result record
                result = self.write.createResult(featureactionid=featureaction.FeatureActionID,
                                              variableid=variable.VariableID,
                                              unitid=unit.UnitsID,
                                              processinglevelid=processinglevel.ProcessingLevelID,
                                              valuecount=len(dates),
                                              sampledmedium='unknown',          # todo: this should be determined from variable/unit
                                              resulttypecv='time series',       # todo: this should be determined from unit/variable
                                              taxonomicclass=None,
                                              resultdatetime=None,
                                              resultdatetimeutcoffset=None,
                                              validdatetime=None,
                                              validdatetimeutcoffset=None,
                                              statuscv=None
                                              )

                # create time series result
                # using the sqlalchemy function results in: FlushError: Instance <TimeSeriesResults at 0x1174b5fd0> has a NULL identity key.
                timeseriesresult = self.insert_timeseries_result(resultid=result.ResultID, timespacing=timestepvalue, timespacing_unitid=timestepunit.UnitsID)

                # todo: consider utc offset for each result value.
                # todo: get timezone based on geometry, use this to determine utc offset
                # todo: implement censorcodecv
                # todo: implement qualitycodecv


                # assemble the timeseriesresultvalues into a dictionary that will be used to build a pandas dataframe object
                data = []
                for i in xrange(len(values)):
                    d = dict(ResultID = result.ResultID,
                             CensorCodeCV = 'nc',
                             QualityCodeCV = 'unknown',
                             TimeAggregationInterval = timestepvalue,
                             TimeAggregationIntervalUnitsID = timestepunit.UnitsID,
                             DataValue = values[i],
                             ValueDateTime = dates[i][1],
                             ValueDateTimeUTCOffset = -6)
                    data.append(d)

                # create pandas dataframe
                df = pandas.DataFrame(data=data)

                # strftime datetime objects (required for SQLite bc lack of datetime64 support)
                df['ValueDateTime'] = df['ValueDateTime'].apply(lambda x: x.strftime('%m/%d/%y %H:%M:%S'))
                self.insert_timeseries_result_values(dataframe=df)


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



    ############ Custom SQL QUERIES ############

    def insert_sampling_feature(self, type='site',code='',name=None,description=None,geometryType=None,elevation=None,elevationDatum=None,WKTgeometry=None):
        '''
        Inserts a sampling feature.  This function was created to support the insertion of Geometry object since this
        functionality is currently lacking from the ODM2PythonAPI.
        :param type: Type of sampling feature.  Must match FeatureTypeCV, e.g. "site"
        :param name: Name of sampling feature (optional)
        :param description: Description of sampling feature (optional)
        :param geometryType: String representation of the geometry type, e.g. Polygon, Point, etc.
        :param elevation: Elevation of the sampling feature (float)
        :param elevationDatum: String representation of the spatial datum used for the elevation
        :param geometry: Geometry of the sampling feature (Shapely Geometry object)
        :return: ID of the sampling feature which was inserted into the database
        '''
        UUID=str(uuid.uuid4())
        FeatureTypeCV=type
        FeatureCode = code
        FeatureName=name
        FeatureDescription=description
        FeatureGeoTypeCV=geometryType
        FeatureGeometry=WKTgeometry
        Elevation=elevation
        ElevationDatumCV=elevationDatum

        # get the last record index
        res = self.spatialDb.execute('SELECT SamplingFeatureID FROM SamplingFeatures ORDER BY SamplingFeatureID DESC LIMIT 1').fetchall()
        ID = res[0][0]  # get the last id value
        ID += 1 # increment the last id

        values = [ID,UUID,FeatureTypeCV,FeatureCode,FeatureName,FeatureDescription, FeatureGeoTypeCV, FeatureGeometry, Elevation,ElevationDatumCV]
        self.spatialDb.execute('INSERT INTO SamplingFeatures VALUES (?, ?, ?, ?, ?, ?, ?, geomFromText(?), ?, ?)'
                               ,values)

        self.spatial_connection.commit()

        # return the id of the inserted record
        return self.spatialDb.lastrowid

        # pts = self.spatial_connection.execute('SELECT ST_AsText(FeatureGeometry) from SamplingFeatures').fetchall()
        # return ID

    def insert_timeseries_result(self, resultid, aggregationstatistic='Unknown', xloc=None, xloc_unitid=None, yloc=None,yloc_unitid=None, zloc=None, zloc_unitid=None, srsID=None, timespacing=None, timespacing_unitid=None):
        """
        Inserts a timeseries result value
        :param resultid: An ID corresponding to a result record (must exist) (int, not null)
        :param aggregationstatistic:  The time interval over which the recorded value represents an aggregation (varchar, not null)
        :param xloc: XLocation, numeric values and Units can be specified for all three dimensions (float, nullable)
        :param xloc_unitid: The unit id for the xloc (int, nullable)
        :param yloc: YLocation, numeric values and Units can be specified for all three dimensions (float, , nullable)
        :param yloc_unitid: The unit id for the yloc (int, nullable)
        :param zloc: ZLocation, numeric values and Units can be specified for all three dimensions (float, nullable)
        :param zloc_unitid: The unit id for the zloc (int, nullable)
        :param srsID: Spatial reference id for used for the x,y,z locations (int, nullable)
        :param timespacing:  Spacing of the time series values (float, nullable)
        :param timespacing_unitid: Unit of the spacing variable (int, nullable)
        :return: Time series result id
        """

        # insert these data
        values = [resultid, xloc, xloc_unitid, yloc, yloc_unitid, zloc, zloc_unitid, srsID, timespacing, timespacing_unitid, aggregationstatistic]
        self.spatialDb.execute('INSERT INTO TimeSeriesResults VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
        self.spatial_connection.commit()

        # return the id of the inserted record
        return self.spatialDb.lastrowid



    def insert_timeseries_result_values(self, dataframe):
        """
        Inserts timeseries result values using the Pandas library
        :param dataframe: a pandas datatable consisting of all records that will be inserted into the ODM2 database
        :return: true
        """

        # convert pandas table into an insert_many query
        dataframe.to_sql(name='TimeSeriesResultValues', con=self.spatial_connection, flavor='sqlite', if_exists='append', index=False)
        self.spatial_connection.commit()

        # return true
        return 1



