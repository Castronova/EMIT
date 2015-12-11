__author__ = 'mike'

import datetime
import uuid
import numpy
import time
import pyspatialite.dbapi2 as spatialite
import pandas

# This is our API for simulation data that uses the latest ODM2PythonAPI code

from ODM2PythonAPI.src.api.ODMconnection import dbconnection
from ODM2PythonAPI.src.api.ODM2.services.readService import ReadODM2
from ODM2PythonAPI.src.api.ODM2.services.createService import CreateODM2
from ODM2PythonAPI.src.api.ODM2.services.updateService import UpdateODM2
from ODM2PythonAPI.src.api.ODM2.services.deleteService import DeleteODM2
from ODM2PythonAPI.src.api.ODM2 import models

from coordinator.emitLogging import elog

def connect(session):

    driver = session.engine.url.drivername

    if 'sqlite' in driver:
        return sqlite(session)

    # todo: implement MsSQL in dbapi_v2
    elif 'mssql' in driver:
        elog.error('MsSQL not supported yet')
        return None

    # todo: implement postgres in dbapi_v2
    elif 'postgresql' in driver:
        elog.error('PostgreSQL not supported yet')
        return None

    # todo: implement mysql in dbapi_v2
    elif 'mysql' in driver:
        elog.error('MySQL not supported yet')
        return None



class sqlite():

    def __init__(self, session):

        # build sqlalchemy connection
        # self.connection = dbconnection.createConnection('sqlite', sqlitepath)
        self.connection = session
        sqlitepath = session.engine.url.database

        # create read, write, update, and delete ODM2PythonAPI instances
        self.read = ReadODM2(self.connection)
        self.write = CreateODM2(self.connection)
        self.update = UpdateODM2(self.connection)
        self.delete = DeleteODM2(self.connection)

        # create connection using spatialite for custom sql queries
        self.spatial_connection = spatialite.connect(sqlitepath)
        self.spatialDb = self.spatial_connection.cursor()

    def create_user(self, userInfo):
        person = self.write.createPerson(userInfo['firstName'], userInfo['lastName'])
        return person.PersonID

    def create_organization(self, organInfo):
        org = self.write.createOrganization(organInfo['cvType'], organInfo['code'], organInfo['name'],
                                            organInfo['desc'], organInfo['link'], organInfo['parentOrgId'])
        return org.OrganizationID

    def create_input_dataset(self, connection, resultids,type,code="",title="",abstract=""):
        pass

    def create_simulation(self, coupledSimulationName, user_obj, config_params, ei, simulation_start, simulation_end, timestep_value, timestep_unit, description, name):
        """
        Inserts a simulation record into the database
        :param simulationName: user provided name for simulation
        :param user_obj: engine.users.Affiliation object
        :param config_params: Simulation configuration parameters (from engine)
        :param ei: list of exchange item objects (stdlib.ExchangeItem)
        """

        bench_insert_result = 0
        bench_insert_tsresult = 0
        bench_insert_tsresultvalues = 0
        bench_assemble_tsresultvalues = 0
        bench_assemble_tsrvpandas = 0
        bench_insert_sf = 0
        bench_insert_fa = 0

        # # parse simulation configuration parameters
        # description = config_params['general'][0]['description']
        # simstart = datetime.datetime.strptime(config_params['general'][0]['simulation_start'], '%m/%d/%Y %H:%M:%S' )
        # simend = datetime.datetime.strptime(config_params['general'][0]['simulation_end'], '%m/%d/%Y %H:%M:%S' )
        # modelcode = config_params['model'][0]['code']
        # modelname = config_params['model'][0]['name']
        # modeldesc = config_params['model'][0]['description']
        # timestepvalue = config_params['time_step'][0]['value']
        #
        # # default to a timestep of seconds
        # timestepname = config_params['time_step'][0].get('name') or 'seconds'
        # timestepabbv = config_params['time_step'][0].get('abbreviation') or ' '

        # create person / organization / affiliation
        # affiliation = self.set_user_preferences(preferences_path)

        # todo: handle multiple affiliations
        # for obj in user_obj:
        person = self.createPerson(user_obj)
        organization = self.createOrganization(user_obj)
        affiliation = self.createAffiliation(organization.OrganizationID, person.PersonID, user_obj)

        # get the timestep unit id
        #todo: This is not returning a timestepunit!!!  This may need to be added to the database
        timestepunit = self.createTimeStepUnit(timestep_unit, timestep_unit)

        method = self.createMethod(organization)

        action = self.write.createAction(type='Simulation',
                                         methodid=method.MethodID,
                                         begindatetime=datetime.datetime.now(),
                                         begindatetimeoffset=int((datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds()/3600))

        # create actionby
        # aff_id = odm2_affiliation[0].AffiliationID if len(odm2_affiliation) > 0 else None
        actionby = self.write.createActionBy(actionid=action.ActionID,
                                             affiliationid=affiliation.AffiliationID)

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
            if not unit:
                unit = self.write.createUnit(type=e.unit().UnitTypeCV(), abbrev=e.unit().UnitAbbreviation(),  name=e.unit().UnitName())

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
            st = time.time()
            samplingfeaturesids = []
            for i in range(0, len(geometries)):
                # create sampling features
                geom_wkt = geometries[i].ExportToWkt()
                geom_type = geometries[i].type
                samplingFeature = self.getSamplingFeatureID__Geometry_EQUALS(geom_wkt)
                if not samplingFeature:
                    samplingFeature = self.insert_sampling_feature(type='site',geometryType=geom_type, WKTgeometry=geom_wkt)
                samplingfeaturesids.append(samplingFeature.SamplingFeatureID)
            bench_insert_sf = (time.time() - st)
            print 'Inserting Sampling Features (not bulk) %3.5f sec' % bench_insert_sf

            st = time.time()
            featureactions = []
            action_ids = [action.ActionID] * len(samplingfeaturesids)
            featureactionids = self.insert_feature_actions_bulk(samplingfeaturesids, action_ids)
            bench_insert_fa += (time.time() - st)
            print 'Inserting Feature Actions (bulk) %3.5f sec' % bench_insert_fa

            # st = time.time()
            # featureactions = []
            # for i in range(len(samplingfeaturesids)):
            #     # create feature action
            #     featureAction = self.write.createFeatureAction(samplingfeatureid=samplingfeaturesids[i], actionid=action.ActionID)
            #     featureactions.append(featureAction)
            # bench_insert_fa += (time.time() - st)
            # print 'Inserting Feature Actions (not bulk) %3.5f sec' % bench_insert_fa


            st = time.time()
            resultids = self.insert_results_bulk(FeatureActionIDs=featureactionids, ResultTypeCV='time series', VariableID=variable.VariableID,
                                     UnitsID=unit.UnitsID, ValueCount=len(dates), ProcessingLevelID=processinglevel.ProcessingLevelID,
                                                 SampledMediumCV='unknown')
            print 'Inserting Results (bulk) %3.5f sec' % (time.time() - st)


            # st = time.time()
            # results = []
            # for i in range(len(featureactionids)):
            #     # create a result record
            #     result = self.write.createResult(featureactionid=featureactionids[i],
            #                                      variableid=variable.VariableID,
            #                                      unitid=unit.UnitsID,
            #                                      processinglevelid=processinglevel.ProcessingLevelID,
            #                                      valuecount=len(dates),
            #                                      sampledmedium='unknown',          # todo: this should be determined from variable/unit
            #                                      resulttypecv='time series',       # todo: this should be determined from unit/variable
            #                                      taxonomicclass=None,
            #                                      resultdatetime=None,
            #                                      resultdatetimeutcoffset=None,
            #                                      validdatetime=None,
            #                                      validdatetimeutcoffset=None,
            #                                      statuscv=None
            #                                      )
            #     results.append(result)
            # bench_insert_result +=  (time.time() - st)
            # print 'Inserting Results (not bulk) %3.5f sec' % bench_insert_result

            st = time.time()
            # create time series result
            timeseriesresult = self.insert_timeseries_results_bulk(resultIDs=resultids, timespacing=timestep_value, timespacing_unitid=timestepunit.UnitsID)
            print 'Inserting Timeseries Results (bulk) %3.5f sec' % (time.time() - st)

            # st = time.time()
            # for i in range(len(results)):
            #     # create time series result
            #     timeseriesresult = self.insert_timeseries_result(resultid=results[i].ResultID, timespacing=timestep_value, timespacing_unitid=timestepunit.UnitsID)
            # bench_insert_tsresult += (time.time() - st)
            # print 'Inserting Timeseries Results (not bulk) %3.5f sec' % bench_insert_tsresult

            # for i in range(len(geometries)):
            #     v = datavalues[:,i]   # all dates for geometry(i)

            # datavalues[times, geoms]
            values = datavalues.flatten(order='C') # flatten row-wise, [t1g1, t1g2, ..., t1gn, t2g1, t2g2, ..., t2gn, ...]
            valuedates = dates[:,1]  # get all rows of the datetime column of the dates array [t1, t2, t3, ..., tn]
            flattened_ids = []
            flattened_dates = []
            geom_count = len(geometries)
            # for id in resultids:
            #     flattened_ids.extend([id] * geom_count)

            for dt in valuedates:
                flattened_dates.extend([dt] * geom_count)  # [t1, t1, ..., t1, t2, t2, ..., t2, tn, tn, ..., tn]

            for i in range(geom_count):
                flattened_ids.extend(resultids)     # [id1, id2, ..., idn, id1, id2, ..., idn, ...]

                # flattened_dates.extend(valuedates)
            # valuedates [valuedates] * geom_count

            st = time.time()
            print 'Bulk Inserting Timeseries Results Values (%d records)' % (len(flattened_ids))
            # TimeAggregationIntervalUnitsID = None, DataValue = [], ValueDateTime = [], ValueDateTimeUTCOffset = -6):
            success = self.insert_timeseries_result_values_bulk(  ResultIDs = flattened_ids, TimeAggregationInterval= timestep_value,
                                                                  TimeAggregationIntervalUnitsID=timestepunit.UnitsID,
                                                                  DataValues = values, ValueDateTimes = flattened_dates,
                                                                  ValueDateTimeUTCOffset=-6, CensorCodeCV='nc', QualityCodeCV='unknown')
            bulk = time.time() - st
            print 'Elapsed time: %3.5f sec' % bulk


            # # loop over geometries
            # for i in range(0, len(geometries)):
            #     # elog.info('OVERWRITE: Saving %s series %d of %d' % (e.variable().VariableNameCV(), i, len(geometries)))
            #     total = (bench_insert_sf / (i+1)) + \
            #             (bench_insert_fa / (i+1)) + \
            #             (bench_insert_result / (i+1)) + \
            #             (bench_insert_tsresult / (i+1)) + \
            #             (bench_assemble_tsresultvalues / (i+1)) + \
            #             (bench_assemble_tsrvpandas / (i+1)) + \
            #             (bench_insert_tsresultvalues / (i+1)) + 0.001
            #     print '\n[%d of %d] ' %(i, len(geometries))
            #     print '%-15s %-15s %-15s %-15s' % ('Operation', 'Total [sec]', 'Ave [sec]', '%')
            #     print '-' * (15*4+3)
            #     print '%-15s %-15s %-15s %-15s' % ('insert sf', str(round(bench_insert_sf,5)), str(round(bench_insert_sf / (i+1), 5)), str(round(bench_insert_sf/(i+1)/total * 100., 1)))
            #     print '%-15s %-15s %-15s %-15s' % ('insert fa', str(round(bench_insert_fa,5)), str(round(bench_insert_fa / (i+1), 5)), str(round(bench_insert_fa/(i+1)/total * 100., 1)))
            #     print '%-15s %-15s %-15s %-15s' % ('insert result', str(round(bench_insert_result,5)), str(round(bench_insert_result / (i+1), 5)), str(round(bench_insert_result/(i+1)/total * 100., 1)))
            #     print '%-15s %-15s %-15s %-15s ' % ('insert tsr',  str(round(bench_insert_tsresult,5)), str(round(bench_insert_tsresult / (i+1), 5)), str(round(bench_insert_tsresult/ (i+1)/total * 100., 1)))
            #     print '%-15s %-15s %-15s %-15s ' % ('assemble trsv', str(round(bench_assemble_tsresultvalues,5)), str(round(bench_assemble_tsresultvalues / (i+1), 5)), str(round(bench_assemble_tsresultvalues/ (i+1)/total * 100., 1)))
            #     print '%-15s %-15s %-15s %-15s ' % ('tsrv pandas', str(round(bench_assemble_tsrvpandas,5)), str(round(bench_assemble_tsrvpandas / (i+1), 5)), str(round(bench_assemble_tsrvpandas/ (i+1)/total * 100., 1)))
            #     print '%-15s %-15s %-15s %-15s ' % ('insert tsrv', str(round(bench_insert_tsresultvalues,5)), str(round(bench_insert_tsresultvalues / (i+1), 5)), str(round(bench_insert_tsresultvalues/ (i+1)/total * 100., 1)))
            #     print '-' * (15*4+3)
            #     print 'Total Estimated Time is %3.5f minutes' % ((total* len(geometries)) / 60)
            #
            #
            #     geom_wkt = geometries[i].ExportToWkt()
            #     geom_type = geometries[i].type
            #
            #     values = datavalues[:,i]   # all dates for geometry(i)
            #
            #     st = time.time()
            #     # create sampling feature
            #     samplingFeature = self.getSamplingFeatureID__Geometry_EQUALS(geom_wkt)
            #     if not samplingFeature:
            #         samplingFeature = self.insert_sampling_feature(type='site',geometryType=geom_type, WKTgeometry=geom_wkt)
            #     bench_insert_sf += (time.time() - st)
            #
            #     st = time.time()
            #     # create feature action
            #     featureaction = self.write.createFeatureAction(samplingfeatureid=samplingFeature.SamplingFeatureID,
            #                                                    actionid=action.ActionID)
            #     bench_insert_fa += (time.time() - st)
            #
            #     st = time.time()
            #     # create a result record
            #     result = self.write.createResult(featureactionid=featureaction.FeatureActionID,
            #                                      variableid=variable.VariableID,
            #                                      unitid=unit.UnitsID,
            #                                      processinglevelid=processinglevel.ProcessingLevelID,
            #                                      valuecount=len(dates),
            #                                      sampledmedium='unknown',          # todo: this should be determined from variable/unit
            #                                      resulttypecv='time series',       # todo: this should be determined from unit/variable
            #                                      taxonomicclass=None,
            #                                      resultdatetime=None,
            #                                      resultdatetimeutcoffset=None,
            #                                      validdatetime=None,
            #                                      validdatetimeutcoffset=None,
            #                                      statuscv=None
            #                                      )
            #     bench_insert_result +=  (time.time() - st)
            #
            #     # create time series result
            #     # using the sqlalchemy function results in: FlushError: Instance <TimeSeriesResults at 0x1174b5fd0> has a NULL identity key.
            #
            #     st = time.time()
            #     timeseriesresult = self.insert_timeseries_result(resultid=result.ResultID, timespacing=timestep_value, timespacing_unitid=timestepunit.UnitsID)
            #     bench_insert_tsresult += (time.time() - st)
            #
            #
            #     # todo: consider utc offset for each result value.
            #     # todo: get timezone based on geometry, use this to determine utc offset
            #     # todo: implement censorcodecv
            #     # todo: implement qualitycodecv
            #
            #
            #     st = time.time()
            #     # assemble the timeseriesresultvalues into a dictionary that will be used to build a pandas dataframe object
            #     data = []
            #     for ii in xrange(len(values)):
            #         d = dict(ResultID = result.ResultID,
            #                  CensorCodeCV = 'nc',
            #                  QualityCodeCV = 'unknown',
            #                  TimeAggregationInterval = timestep_value,
            #                  TimeAggregationIntervalUnitsID = timestepunit.UnitsID,
            #                  DataValue = values[ii],
            #                  ValueDateTime = dates[ii][1],
            #                  ValueDateTimeUTCOffset = -6)
            #         data.append(d)
            #     bench_assemble_tsresultvalues += (time.time() - st)
            #
            #     st = time.time()
            #     # create pandas dataframe
            #     df = pandas.DataFrame(data=data)
            #     bench_assemble_tsrvpandas += (time.time() - st)
            #
            #
            #     st = time.time()
            #     # strftime datetime objects (required for SQLite bc lack of datetime64 support) YYYY-MM-DD HH:MM:SS
            #     df['ValueDateTime'] = df['ValueDateTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
            #     self.insert_timeseries_result_values(dataframe=df)
            #     bench_insert_tsresultvalues += (time.time() - st)
            #
            #     st = time.time()
            #     # TimeAggregationIntervalUnitsID = None, DataValue = [], ValueDateTime = [], ValueDateTimeUTCOffset = -6):
            #     success = self.insert_timeseries_result_values_bulk(  ResultID=result.ResultID, TimeAggregationInterval= timestep_value,
            #                                                           TimeAggregationIntervalUnitsID=timestepunit.UnitsID,
            #                                                           DataValues = values, ValueDateTimes = dates[:,1],
            #                                                           ValueDateTimeUTCOffset=-6, CensorCodeCV='nc', QualityCodeCV='unknown')
            #     bulk = time.time() - st
            #     print 'Bulk Insert %3.5f sec' % (bulk)
            #     total_sqlalchemy = (bench_assemble_tsrvpandas + bench_assemble_tsresultvalues + bench_insert_tsresultvalues) / (i+1)
            #     print 'Non-Bulk Insert %3.5f sec' % (total_sqlalchemy)
            #     print 'Speedup of %3.fX' % (total_sqlalchemy / bulk)


        model = self.createModel(name, description, name)

        # create simulation

        #start = min([i.getStartTime() for i in output_exchange_items])
        #end = max([i.getEndTime() for i in output_exchange_items])

        # TODO: remove hardcoded time offsets!
        sim = self.write.createSimulation(actionid=action.ActionID,
                                          modelID=model.ModelID,
                                          simulationName=coupledSimulationName,
                                          simulationDescription=description,
                                          simulationStartDateTime=simulation_start ,
                                          simulationStartOffset=-6,
                                          simulationEndDateTime=simulation_end,
                                          simulationEndOffset=-6,
                                          timeStepValue =timestep_value,
                                          timeStepUnitID=timestepunit.UnitsID,
                                          inputDatasetID=dataset.DataSetID)

        return sim

    def createTimeStepUnit(self, timestepabbv, timestepname):
        timestepunit = self.read.getUnitByName(timestepname)
        if timestepunit is None:
            timestepunit = self.write.createUnit('time', timestepabbv, timestepname)
        return timestepunit

    def createModel(self, modelcode, modeldesc, modelname):
        model = self.read.getModelByCode(modelcode=modelcode)
        if not model:
            model = self.write.createModel(code=modelcode, name=modelname, description=modeldesc)

        return model

    def createMethod(self, organization):
        method = self.read.getMethodByCode('simulation')
        if not method:
            method = self.write.createMethod(code='simulation', name='simulation', vType='calculated',
                                             orgId=organization.OrganizationID, description='Model Simulation Results')
        return method

    def createAffiliation(self, organizationid, personid, user_obj):


        affiliation = self.read.getAffiliationByPersonAndOrg(user_obj.person.firstname, user_obj.person.lastname,
                                                             user_obj.organization.code)
        if not affiliation:
            affiliation = self.write.createAffiliation(personid, organizationid, user_obj.email,
                                                       user_obj.phone, user_obj.address, user_obj.personLink,
                                                       user_obj.isPrimaryOrganizationContact, user_obj.startDate,
                                                       user_obj.affiliationEnd)
        return affiliation

    def createOrganization(self, user_obj):

        organization = self.read.getOrganizationByCode(user_obj.organization.code)
        if not organization:
            organization = self.write.createOrganization(user_obj.organization.typeCV, user_obj.organization.code,
                                                         user_obj.organization.name, user_obj.organization.description,
                                                         user_obj.organization.link, user_obj.organization.parent)
        return organization

    def createPerson(self, user_obj):

        person = self.read.getPersonByName(user_obj.person.firstname, user_obj.person.lastname)
        if not person:
            person = self.write.createPerson(user_obj.person.firstname, user_obj.person.lastname, user_obj.person.middlename)
        return person

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
        res = self.spatialDb.execute('SELECT last_insert_rowid() FROM SamplingFeatures')
        ID = res.fetchone() or (-1,)
        ID = ID[0] + 1 # increment the last id

        values = [ID,UUID,FeatureTypeCV,FeatureCode,FeatureName,FeatureDescription, FeatureGeoTypeCV, FeatureGeometry, Elevation,ElevationDatumCV]
        self.spatialDb.execute('INSERT INTO SamplingFeatures VALUES (?, ?, ?, ?, ?, ?, ?, geomFromText(?), ?, ?)'
                               ,values)

        self.spatial_connection.commit()

        featureObj = models.SamplingFeatures()
        featureObj.SamplingFeatureID = ID
        featureObj.SamplingFeatureUUID = UUID
        featureObj.SamplingFeatureTypeCV = FeatureTypeCV
        featureObj.SamplingFeatureCode = FeatureName
        featureObj.SamplingFeatureName = FeatureCode
        featureObj.SamplingFeatureDescription = FeatureDescription
        featureObj.SamplingFeatureGeotypeCV = FeatureGeoTypeCV
        featureObj.Elevation_m = Elevation
        featureObj.ElevationDatumCV = ElevationDatumCV
        featureObj.FeatureGeometry = FeatureGeometry

        return featureObj


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

    def insert_timeseries_result_values_bulk(self, ResultIDs = [], DataValues = [], ValueDateTimes = [],
                                             QualityCodeCV = 'unknown', TimeAggregationIntervalUnitsID = 1,
                                             TimeAggregationInterval = 1, CensorCodeCV = 'nc', ValueDateTimeUTCOffset = -6):
        """
        Performs a bulk insert of time series result values
        :return: True if successful, else False
        ValueID                         (integer)
        ResultID                        (integer)
        DataValue                       (float)
        ValueDateTime                   (datetime)
        ValueDateTimeUTCOffset          (integer)
        CensorCodeCV                    (varchar(255))
        QualityCodeCV                   (varchar(255))
        TimeAggregationInterval         (float)
        TimeAggregationIntervalUnitsID  (integer)
        """
        if ResultIDs == None:
            elog.error('Result ID cannot be None')
            return False

        if len(DataValues) != len(ValueDateTimes):
            elog.error('Length of Values and Dates must be equal')
            return False

        valCount = len(DataValues)

        # convert parameters values into array values
        censor_codes = [CensorCodeCV] * valCount
        quality_codes = [QualityCodeCV] * valCount
        time_unit_ids = [TimeAggregationIntervalUnitsID] * valCount
        time_intervals = [TimeAggregationInterval] * valCount
        time_offsets = [ValueDateTimeUTCOffset] * valCount
        # result_ids = [ResultID] * valCount

        # cannot be none: resultid, timeaggregation interval
        # cannot be empty: datavale, valuedatetime
        # self.spatialDb.execute('INSERT INTO')
        # get the last record index
        res = self.spatialDb.execute('SELECT last_insert_rowid() FROM TimeSeriesResultValues')
        startID = res.fetchone() or (-1,)
        startID = startID[0] + 1 # increment the last id

        valueIDs = range(startID, startID + valCount, 1)
        # vals = [ID, ResultID, DataValue, ValueDateTime, ValueDateTimeUTCOffset, CensorCodeCV, QualityCodeCV, TimeAggregationInterval, TimeAggregationIntervalUnitsID]
        vals = zip(valueIDs, ResultIDs, DataValues, ValueDateTimes, time_offsets, censor_codes, quality_codes, time_intervals, time_unit_ids)

        # insert values in chunks of 10,000
        chunk_size = 10000
        percent_complete = 0
        for i in range(0, len(vals), chunk_size):
            sidx = i
            eidx = i + chunk_size if (i + chunk_size) < len(vals) else len(vals)
            percent_complete = float(i) / float(len(vals)) * 100
            print '.. inserting records %3.1f %% complete' % (percent_complete)
            self.spatialDb.executemany('INSERT INTO TimeSeriesResultValues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', vals[sidx:eidx])

        print '.. committing changes to database'
        self.spatial_connection.commit()


        return 1

    def insert_feature_actions_bulk(self, SamplingFeatureIDs = [], ActionIDs = []):
        """
        Performs a bulk insert of feature action ids
        :return: list of feature action ids
        FeatureActionID                (integer)
        SamplingFeatureID              (integer)
        ActionID                       (integer)
        """

        if len(SamplingFeatureIDs) != len(ActionIDs):
            elog.error('Length SamplingFeatureIDs, and ActionIDs must be equal')
            return False

        valCount = len(SamplingFeatureIDs)

        # get the last record index
        res = self.spatialDb.execute('SELECT last_insert_rowid() FROM FeatureActions')
        startID = res.fetchone() or (-1,)
        startID = startID[0] + 1 # increment the last id

        FeatureActionIDs = range(startID, startID + valCount, 1)
        vals = zip(FeatureActionIDs, SamplingFeatureIDs, ActionIDs)
        self.spatialDb.executemany('INSERT INTO FeatureActions VALUES (?, ?, ?)', vals)
        self.spatial_connection.commit()


        # return the feature action ids
        return FeatureActionIDs

    def insert_results_bulk(self, FeatureActionIDs=[], ResultTypeCV=None, VariableID=None, UnitsID=None, TaxonomicClassfierID=None,
        ProcessingLevelID=None, ResultDateTime=None, ResultDateTimeUTCOffset=None, ValidDateTime=None, ValidDateTimeUTCOffset=None,
                            StatusCV=None, SampledMediumCV=None, ValueCount=None):
        """
        Performs a bulk insert of results
        :return: list of result ids
        ResultID
        ResultUUID
        FeatureActionID
        ResultTypeCV
        VariableID
        UnitsID
        TaxonomicClassfierID
        ProcessingLevelID
        ResultDateTime
        ResultDateTimeUTCOffset
        ValidDateTime
        ValidDateTimeUTCOffset
        StatusCV
        SampledMediumCV
        ValueCount
        """

        if VariableID is None or UnitsID is None or ProcessingLevelID is None or ValueCount is None \
                        or SampledMediumCV is None or FeatureActionIDs == []:
            elog.error('Failed to bulk insert Results.  VariableID, UnitID, ProcessingLevelID, ValueCount, SampledMediumCV, FeatureActionIDs are required fields.')
            return False

        valCount = len(FeatureActionIDs)

        # get the last record index
        res = self.spatialDb.execute('SELECT last_insert_rowid() FROM Results')
        startID = res.fetchone() or (-1,)
        startID = startID[0] + 1 # increment the last id

        # generate UUIDs for each Result record
        uuids = [uuid.uuid4().hex for i in range(valCount)]
        ResultIDs = range(startID, startID + valCount, 1)

        # convert parameter values into lists
        ResultTypeCV = [ResultTypeCV] * valCount
        VariableID = [VariableID] * valCount
        UnitsID = [UnitsID] * valCount
        TaxonomicClassfierID = [TaxonomicClassfierID] * valCount
        ProcessingLevelID = [ProcessingLevelID] * valCount
        ResultDateTime = [ResultDateTime] * valCount
        ResultDateTimeUTCOffset = [ResultDateTimeUTCOffset] * valCount
        ValidDateTime = [ValidDateTime] * valCount
        ValidDateTimeUTCOffset = [ValidDateTimeUTCOffset] * valCount
        StatusCV = [StatusCV] * valCount
        SampledMediumCV = [SampledMediumCV] * valCount
        ValueCount = [ValueCount] * valCount

        # zip the values up
        vals = zip(ResultIDs, uuids, FeatureActionIDs, ResultTypeCV, VariableID, UnitsID, TaxonomicClassfierID,
                   ProcessingLevelID, ResultDateTime, ResultDateTimeUTCOffset, ValidDateTime, ValidDateTimeUTCOffset,
                   StatusCV, SampledMediumCV, ValueCount)
        self.spatialDb.executemany('INSERT INTO Results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', vals)
        self.spatial_connection.commit()


        # return the feature action ids
        return ResultIDs

    def insert_timeseries_results_bulk(self, resultIDs = [], aggregationstatistic='Unknown', xloc=None, xloc_unitid=None, yloc=None, yloc_unitid=None,
        zloc=None, zloc_unitid=None, srsID=None, timespacing=None, timespacing_unitid=None):
        """
        Performs a bulk insert of timeseries results
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

        # if VariableID is None or UnitsID is None or ProcessingLevelID is None or ValueCount is None \
        #                 or SampledMediumCV is None or FeatureActionIDs == []:
        #     elog.error('Failed to bulk insert Results.  VariableID, UnitID, ProcessingLevelID, ValueCount, SampledMediumCV, FeatureActionIDs are required fields.')
        #     return False

        valCount = len(resultIDs)

        # # get the last record index
        # res = self.spatialDb.execute('SELECT last_insert_rowid() FROM TimeSeriesResults')
        # startID = res.fetchone() or (-1,)
        # startID = startID[0] + 1 # increment the last id
        #
        # # generate UUIDs for each Result record
        # ResultIDs = range(startID, startID + valCount, 1)

        # convert parameter values into lists
        aggregationstatistic = [aggregationstatistic] * valCount
        xloc = [xloc] * valCount
        xloc_unitid = [xloc_unitid] * valCount
        yloc = [yloc] * valCount
        yloc_unitid = [yloc_unitid] * valCount
        zloc = [zloc] * valCount
        zloc_unitid = [zloc_unitid] * valCount
        srsID = [srsID] * valCount
        timespacing = [timespacing] * valCount
        timespacing_unitid = [timespacing_unitid] * valCount

        # zip the values up
        vals = zip(resultIDs, aggregationstatistic, xloc, xloc_unitid, yloc, yloc_unitid, zloc, zloc_unitid, srsID,
                   timespacing, timespacing_unitid)
        self.spatialDb.executemany('INSERT INTO TimeSeriesResults VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', vals)
        self.spatial_connection.commit()


        # return the feature action ids
        return None


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

    ###################
    #### GETTERS ######
    ###################

    def getSamplingFeatureID__Geometry_EQUALS(self, wkt_geometry):

        try:
            res = self.spatialDb.execute('SELECT SamplingFeatureID,'
                                         'SamplingFeatureUUID,'
                                         'SamplingFeatureTypeCV,'
                                         'SamplingFeatureCode,'
                                         'SamplingFeatureName,'
                                         'SamplingFeatureDescription,'
                                         'SamplingFeatureGeotypeCV,'
                                         'Elevation_m,'
                                         'ElevationDatumCV,'
                                         'AsText(FeatureGeometry) '
                                         'FROM SamplingFeatures '
                                         'WHERE Equals ( geomFromText(?) , SamplingFeatures.FeatureGeometry )', [wkt_geometry])

            sf = res.fetchone()
            if sf is None:
                return None

            featureObj = models.SamplingFeatures()
            featureObj.SamplingFeatureID =sf[0]
            featureObj.SamplingFeatureUUID = sf[1]
            featureObj.SamplingFeatureTypeCV = sf[2]
            featureObj.SamplingFeatureCode = sf[3]
            featureObj.SamplingFeatureName = sf[4]
            featureObj.SamplingFeatureDescription = sf[5]
            featureObj.SamplingFeatureGeotypeCV = sf[6]
            featureObj.Elevation_m = sf[7]
            featureObj.ElevationDatumCV = sf[8]
            featureObj.FeatureGeometry = sf[9]

            return featureObj

        except Exception, e:
            print e
            return None


    def getAllSeries(self):
        """ General select statement for retrieving many results.  This is intended to be used when populating gui tables

        :return :
            :type list:
        """
        try:
            res = self.connection.getSession().query(models.Results). \
                join(models.Variables). \
                join(models.Units). \
                join(models.FeatureActions). \
                join(models.Actions). \
                join(models.TimeSeriesResultValues, models.TimeSeriesResultValues.ResultID == models.Results.ResultID). \
                filter(models.Actions.ActionTypeCV != 'Simulation'). \
                all()
            return res
        except Exception, e:
            print e

    def getAllSimulations(self):
        """
        General select statement for retrieving many simulations.  This is intended to be used for populating gui tables
        :return:
        """
        try:
            res = self.connection.getSession().query(models.Simulations, models.Models, models.Actions, models.People). \
                join(models.Models). \
                join(models.Actions). \
                join(models.ActionBy). \
                join(models.Affiliations). \
                join(models.People).all()
            return res
        except Exception, e:
            print e

    def getCurrentSession(self):
        return self.connection.getSession()

    ###################
    #### DELETES ######
    ###################

    def deleteSimulation(self, record):
        self.delete.deleteRecord(record.simulation_id)
        if not self.delete.isModelConstraint(record.model_id):
            self.delete.deleteModelByName(record.model_name)


