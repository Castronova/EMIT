__author__ = 'tonycastronova'

import uuid
import datetime
from utilities import gui
import stdlib
from shapely.wkt import loads


from api.ODM2.Core.services import *
from api.ODM2.SamplingFeatures.services import *
from api.ODM2.Results.services import *
from api.ODM2.Simulation.services import *
from api.ODM2.Core.model import *


# from odm2.api.ODM2.Core.services import *
# from odm2.api.ODM2.SamplingFeatures.services import *
# from odm2.api.ODM2.Results.services import *
# from odm2.api.ODM2.Simulation.services import *
# from odm2.api.ODM2.Core.model import *
#
import time

def results_to_dict(cursor):

    datasets = cursor.fetchall()
    results = []
    for dataset in datasets:
        dict = {}
        desc = cursor.description

        for i in xrange(0,len(desc)):
            name = desc[i][0]
            value = dataset[i]
            if name in dict:
                dict[name].append(value)
            else:
                dict[name] = [value]

        results.append(dict)
    return results

class postgresdb():

    def __init__(self,connectionstring):
        self.sconn = connectionstring

        self._coreread = readCore(self.sconn)
        self._corewrite = createCore(self.sconn)
        self._sfread = readSamplingFeatures(self.sconn)
        self._sfwrite = createSamplingFeatures(self.sconn)
        self._reswrite = createResults(self.sconn)
        self._resread = readResults(self.sconn)
        self._simread = readSimulation(self.sconn)
        self._simwrite= createSimulation(self.sconn)


    def set_user_preferences(self, preferences):

        # parse user preferences file
        prefs = gui.parse_config_without_validation(preferences)

        # create people
        for person in prefs['person']:

            # check if the person exists
            p = self._coreread.getPersonByName(person['firstname'],person['lastname'])
            if not p:
                # insert person
                p = self._corewrite.createPerson(person['firstname'],person['lastname'])


        # create organization
        organizations = prefs['organization']
        while len(organizations) > 0:

            organization = organizations.pop(0)

            insert = True

            # make sure the parent exists in the database
            if organization.has_key('parentcode'):
                if not self._coreread.getOrganizationByCode(organization['parentcode']):
                    # move item to back of list
                    organizations.append(organization)
                    insert = False

            if insert:
                # check if organization already exists
                org = self._coreread.getOrganizationByCode(organization['code'])
                if not org:
                    # insert organization
                    desc = organization['description'] if organization.has_key('description') else None
                    link = organization['link'] if organization.has_key('link') else None
                    pcode = organization['parentcode'] if organization.has_key('parentcode') else None
                    parent = self._coreread.getOrganizationByCode(pcode).OrganizationID if pcode else None

                    org = self._corewrite.createOrganization(organization['type'],
                                                             organization['code'],
                                                             organization['name'],
                                                             desc,link,parent)


        # create affiliations
        for person in prefs['person']:

            # get the person id
            personid = None
            p = self._coreread.getPersonByName(person['firstname'],person['lastname'])
            if not p: raise Exception('Person Not found: %s %s' % (person['firstname'], person['lastname']))

            # get the organization id
            orgid = None
            o = self._coreread.getOrganizationByCode(person['organizationcode'])
            if not o: raise Exception('Organization Not found: %s' % person['organizationcode'])

            phone = person['phone'] if person.has_key('phone') else None
            email = person['email'] if person.has_key('email') else None
            addr = person['address'] if person.has_key('address') else None

            affiliations = self._coreread.getAffiliationByPersonAndOrg(p.PersonFirstName, p.PersonLastName,o.OrganizationCode)

            if not affiliations:
                affiliations = self._corewrite.createAffiliation(personid=p.PersonID,
                                                  organizationid=o.OrganizationID,
                                                  email=email,
                                                  phone=phone,
                                                  address=addr)


        return affiliations

    def create_input_dataset(self,connection, resultids,type,code="",title="",abstract=""):

        # always create a new dataset for each model
        dataset = self._corewrite.createDataSet(type,code,title,abstract)

        # link each input result ID to the simulation dataset
        for resultid in resultids:
            self._corewrite.createDataSetResults(dataset.DataSetID,resultid)

        return dataset

    def create_simulation(self,preferences_path, config_params, output_exchange_items):

        name = config_params['general'][0]['name']
        description = config_params['general'][0]['description']
        simstart = config_params['general'][0]['simulation_start']
        simend = config_params['general'][0]['simulation_end']
        modelcode = config_params['model'][0]['code']
        modelname = config_params['model'][0]['name']
        modeldesc = config_params['model'][0]['description']
        timestepvalue = config_params['time_step'][0]['value']
        timestepunittype = config_params['time_step'][0]['unit_type_cv']


        # create person / organization / affiliation
        affiliation = self.set_user_preferences(preferences_path)

        # get the timestep unit id
        #todo: This is not returning a timestepunit!!!  This may need to be added to the database
        timestepunit = self._coreread.getUnitByName(timestepunittype)

        # create method
        method = self._coreread.getMethodByCode('simulation')
        if not method: method = self._corewrite.createMethod(code= 'simulation',
                                                             name='simulation',
                                                             vType='calculated',
                                                             orgId=affiliation.OrganizationID,
                                                             description='Model Simulation Results')


        # create action
        action = self._corewrite.createAction(type='Simulation',
                                              methodid=method.MethodID,
                                              begindatetime=datetime.datetime.now(),
                                              begindatetimeoffset=int((datetime.datetime.now() - datetime.datetime.utcnow() ).total_seconds()/3600))
        # create actionby
        actionby = self._corewrite.createActionBy(actionid=action.ActionID,
                                                  affiliationid=affiliation.AffiliationID)

        # create processing level
        processinglevel = self._coreread.getProcessingLevelByCode(processingCode=2)
        if not processinglevel: processinglevel = self._corewrite.createProcessingLevel(code=2,
                                                                      definition='Derived Product',
                                                                      explanation='Derived products require scientific and technical interpretation and include multiple-sensor data. An example might be basin average precipitation derived from rain gages using an interpolation procedure.')

        # create dataset
        dataset = self._corewrite.createDataSet(dstype='Simulation Input',
                                                dscode='Input_%s'%name,
                                                dstitle='Input for Simulation: %s'%name,
                                                dsabstract=description)



        tsvalues = []

        # loop over output exchange items
        for exchangeitem in output_exchange_items:

            # create variable
            # TODO: This is not correct!
            # todo: implement variable vType
            variable = self._coreread.getVariableByCode(exchangeitem.variable().VariableNameCV())
            if not variable: variable = self._corewrite.createVariable(code=exchangeitem.variable().VariableNameCV(),
                                                                       name=exchangeitem.variable().VariableDefinition(),
                                                                       vType='unknown',
                                                                       nodv=-999)

            # create unit
            unit = self._coreread.getUnitByName(exchangeitem.unit().UnitName())
            if not unit: unit = self._corewrite.createUnit(type=exchangeitem.unit().UnitTypeCV(),
                                                           abbrev=exchangeitem.unit().UnitAbbreviation(),
                                                           name=exchangeitem.unit().UnitName())

            # create spatial reference
            refcode = "%s:%s" %(exchangeitem.geometries()[0].srs().GetAttrValue("AUTHORITY", 0),exchangeitem.geometries()[0].srs().GetAttrValue("AUTHORITY", 1))
            spatialref = self._sfread.getSpatialReferenceByCode(refcode)
            if not spatialref: spatialref = self._sfwrite.createSpatialReference(srsCode=refcode,
                                                                                 srsName=exchangeitem.geometries()[0].srs().GetAttrValue("GEOGCS", 0),
                                                                                 srsDescription="%s|%s|%s"%(exchangeitem.geometries()[0].srs().GetAttrValue("PROJCS", 0),exchangeitem.geometries()[0].srs().GetAttrValue("GEOGCS", 0),exchangeitem.geometries()[0].srs().GetAttrValue("DATUM", 0)))


            st = time.time()
            # loop over geometries
            for geometry in exchangeitem.geometries():

                geom = geometry.geom()

                dates,values = geometry.datavalues().get_dates_values()




                # create sampling feature
                samplingfeature = self._coreread.getSamplingFeatureByGeometry(geom.wkt)
                if not samplingfeature: samplingfeature = self._corewrite.createSamplingFeature(code=uuid.uuid4().hex,
                                                                                                vType="site",
                                                                                                name=None,
                                                                                                description=None,
                                                                                                geoType=geom.geom_type,
                                                                                                elevation=None,
                                                                                                elevationDatum=None,
                                                                                                featureGeo=geom.wkt)

                # create feature action
                featureaction = self._corewrite.createFeatureAction(samplingfeatureid=samplingfeature.SamplingFeatureID,
                                                                    actionid=action.ActionID)






                result = Result()
                result.ResultUUID = uuid.uuid4().hex
                result.FeatureActionID = featureaction.FeatureActionID
                result.ResultTypeCV = 'time series'
                result.VariableID = variable.VariableID
                result.UnitsID = unit.UnitsID
                result.ProcessingLevelID = processinglevel.ProcessingLevelID
                result.ValueCount = len(dates)
                result.SampledMediumCV = 'unknown'


                # create time series result
                timeseriesresult = self._reswrite.createTimeSeriesResult(result=result, aggregationstatistic='unknown',
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
                    tsrv = Timeseriesresultvalue()
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
        self._reswrite.createAllTimeSeriesResultValues(tsrv = tsvalues)

        #print '%3.5f sec' % (time.time() - st)

        # # loop over input exchange items
        # for exchangeitem in input_exchange_items:
        #
        #     # loop over geometries
        #     for geometry in exchangeitem.geometries():
        #
        #         geom = geometry.geom()
        #
        #         dates,values = geometry.datavalues().get_dates_values()

        # loop over input exchange items
            # get result instance
            # if result exists
                # create datasetresults

            # else
                # loop over geometries
                # create feature action
                # create variable
                # create unit
                # create result
                # create time series result
                # create time series result values


        # create model
        model = self._simread.getModelByCode(modelcode=modelcode)
        if not model: model = self._simwrite.createModel(code=modelcode,
                                                           name=modelname,
                                                           description=modeldesc)


        # create simulation

        #start = min([i.getStartTime() for i in output_exchange_items])
        #end = max([i.getEndTime() for i in output_exchange_items])

        # TODO: remove hardcoded time offsets!
        sim = self._simwrite.createSimulation(actionid=action.ActionID,
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

    def get_simulation_results(self,simulationName, dbactions, from_variableName, from_unitName, to_variableName, startTime, endTime):

        # get the simulation object from simulationName
        #simulation = self._simread.getSimulationByActionID(actionID=actionid)

        actionid, session, actiontype = dbactions[simulationName]

        # initialize the session
        #self._coreread = readCore(session)
        #self._resread = readResults(session)

        # get the simulation results
        if actiontype == 'action':
            results = self._coreread.getResultAndGeomByActionID(actionID=actionid)
        else:
            results = [self._coreread.getResultAndGeomByID(resultID=actionid)]

        exchangeitems = {}
        timeseries = []

        # select the result corresponding to the unit and variable
        resultid = None
        for result, geom in results:
            if result.VariableObj.VariableCode != from_variableName:
                print '> WARNING: Variables are inconsistent.  %s !=  %s' %(result.VariableObj.VariableCode, from_variableName)

            if result.UnitObj.UnitsName != from_unitName:
                print '> WARNING: Units are inconsistent.  %s !=  %s'%(result.UnitObj.UnitsName, from_unitName)

            resultid = result.ResultID


            # get the timeseries values
            values = self._resread.getTimeSeriesValuesByTime(resultid=resultid,starttime=startTime,endtime=endTime)

            if len(values) == 0:
                raise Exception('> [Error] Could not find any data for specified time range: %s, %s - %s'%(from_variableName,startTime,endTime))

            # save each timeseries to a geometry
            dv = stdlib.DataValues(timeseries=[(value.ValueDateTime,value.DataValue) for value in values])
            g = loads(geom)

            # save datavalues on the to_variableName
            if g not in exchangeitems:
                exchangeitems[g] = {to_variableName:dv}
            else:
                exchangeitems[g].update({to_variableName:dv})

        return exchangeitems



from api.ODM2 import serviceBase
from api.ODM2.Core.model import *
from api.ODM2.Results.model import *
from api.ODM2.Simulation.model import *

class utils(serviceBase):

    def getAllSeries(self):
        """ General select statement for retrieving many results.  This is intended to be used when populating gui tables

        :return :
            :type list:
        """

        return self._session.query(Result).\
                join(Variable). \
                join(Unit). \
                join(Featureaction). \
                join(Action). \
                join(Timeseriesresultvalue, Timeseriesresultvalue.ResultID == Result.ResultID).\
                filter(Action.ActionTypeCV != 'Simulation').\
                all()




    def getAllSimulations(self):
        """
        General select statement for retrieving many simulations.  This is intended to be used for populating gui tables
        :return:
        """

        try:
            res = self._session.query(Simulation, Model, Action, Person). \
                join(Model). \
                join(Action).\
                join(Actionby). \
                join(Affiliation).\
                join(Person).all()
            return res
        except Exception, e:
            print e












### OLD ###


    def insert_result_ts(self):

        # result uuid => calc
        # featureactionid => calc
        # result type
        # variable id
        # units id
        # processing level id
        # sample medium cv
        # value count
        # --
        # taxonomic classifier id (null)
        # result date time (null)
        # result date time offset (null)
        # valid date time (null)
        # valid date time offset (null)
        # status cv (null)

        # create action

        # select or insert sampling feature

        # create feature action associations

        # select or insert variable

        # select or insert unit

        # select or insert processing level

        # select or insert sample medium cv

        pass

    def get_all_variables(self):
        #self.get_simulations()
        #return self._session.query(m.core.Variable).all()
        pass

    # def get_simulations(self):
    #     self._session.query(simulation.Simulation).all()
    #
    # def get_all_ts_alc(self):
    #     return self._session.query(core.Result,core.Samplingfeature).all()
    #     #return self._session.query(m.Variable).filter_by(VariableID=variableId).one()


    def get_all_ts_meta(self):
        """
        Gets metadata for all timeseries in database
        :return: dictionary of metedata elements for each timeseries
        """

        # what - variable, quantity
        # when - start, end times
        # where - geography
        # how - provenance? simulation or sensor
        # who - person that created it

        querystring = """SELECT
                          u.unitsname,u.unitsabbreviation,u.unitstypecv,
                          v.variabletypecv,v.variablecode,v.variablenamecv,v.variabledefinition,
                          sf.featuregeometry,
                          r.resultdatetime,r.resultdatetimeutcoffset,
                          pl.processinglevelcode,pl.definition,pl.explanation,
                          tsr.intendedtimespacing,tsr.intendedtimespacingunitsid,
                          o.organizationcode,o.organizationname,o.organizationdescription,
                          p.personfirstname,p.personlastname,
                          m.methodcode,m.methodname,m.methoddescription,
                          ds.datasetid, ds.datasettypecv, ds.datasettitle
                        FROM
                          odm2core.results as r
                          join odm2core.variables as v on v.variableid = r.variableid
                          join odm2core.units as u on u.unitsid = r.unitsid
                          join odm2core.featureactions as fa on fa.featureactionid = r.featureactionid
                          join odm2core.samplingfeatures as sf on sf.samplingfeatureid = fa.samplingfeatureid
                          join odm2core.processinglevels as pl on pl.processinglevelid = r.processinglevelid
                          join odm2results.timeseriesresults as tsr on tsr.resultid = r.resultid
                          join odm2core.actions as a on a.actionid = fa.actionid
                          join odm2core.actionby as ab on ab.actionid = a.actionid
                          join odm2core.affiliations as aff on aff.affiliationid = ab.affiliationid
                          join odm2core.people as p on p.personid = aff.personid
                          join odm2core.methods as m on m.methodid = a.methodid
                          join odm2core.organizations o on o.organizationid = m.organizationid
                          left join odm2core.datasetsresults dsr on dsr.resultid = r.resultid
                          left join odm2core.datasets ds on ds.datasetid = dsr.datasetid"""

        query = ' '.join([s.strip() for s in querystring.split('\n')])
        self.cursor.execute(query)
        return results_to_dict(self.cursor)

    ##################
    # INSERT QUERIES #
    ##################

    def create_model_instance(self, modelcode, modelname, modeldescription=None):
        """
        Adds a record for the given model in the database, if it doesn't already exist
        :param modelcode: A unique string code given to the model (e.g. swat, swmm, ueb, etc.)
        :param modelname: The name of the model
        :param modeldescription: A short description of the model
        :return: record of the model
        """

        pass

    def create_dataset(self,typecv,code,title,abstract):
        """

        :param typecv:
        :param code:
        :param title:
        :param abstract:
        :return:
        """
        pass

    def insert_unit(self,unittypecv,unitabbreviation,unitname):
        """

        :param unittypecv:
        :param unitabbreviation:
        :param unitname:
        :return:
        """
        pass

    def insert_variable(self, typecv,code,namecv,definition,speciationcv=None,nodatavalue=None):
        """

        :param typecv:
        :param code:
        :param namecv:
        :param definition:
        :param speciationcv:
        :param nodatavalue:
        :return:
        """
        pass



    def insert_simulation(self,name,description,startdate,startoffset,enddate,endoffset,timestepvalue,timestepunitid,inputdatasetid,outputdatasetid,modelid):
        # prereq. model, input, output, timestepunit


        """

        :param name:
        :param description:
        :param startdate:
        :param startoffset:
        :param enddate:
        :param endoffset:
        :param timestepvalue:
        :param timestepunitid:
        :param inputdatasetid:
        :param outputdatasetid:
        :param modelid:
        :return:
        """
        pass

    def insert_method(self,typecv,code,name,description=None,link=None,organizationid=None):
        """

        :param typecv:
        :param code:
        :param name:
        :param description:
        :param link:
        :param organizationid:
        :return:
        """
        pass

    def insert_organization(self,typecv,code,name,description,link,parentid):
        """

        :param typecv: type of organization selected from controlled vocabulary (e.g. university)
        :param code: unique string identifying the organization (e.g. usu, usc, uwrl)
        :param name: name of the organization
        :param description: short description of the organization
        :param link:
        :param parentid: organization parent id
        :return:
        """

    def insert_affiliation(self,personid,startdate,email, organizationid=None,isprimarycontact=None,enddate=None,phone=None,address=None,link=None):
        """

        :param personid:
        :param startdate:
        :param email:
        :param organizationid:
        :param isprimarycontact:
        :param enddate:
        :param phone:
        :param address:
        :param link:
        :return:
        """
        pass

    def insert_people(self,first,last, middle=None):
        """

        :param first: first name of user
        :param last: last name of user
        :param middle: (optional) middle name of user
        :return: record id of the user
        """
        querystring = "INSERT "

    def insert_action(self,typecv,methodid,begindate,beginoffset,enddate=None,endoffset=None,description=None,filelink=None):
        """

        :param typecv:
        :param methodid:
        :param begindate:
        :param beginoffset:
        :param enddate:
        :param endoffset:
        :param description:
        :param filelink:
        :return:
        """
        pass


    def add_related_model(self,modelid,relatedmodelid,relationshiptypecv):
        """

        :param modelid:
        :param relatedmodelid:
        :param relationshiptypecv:
        :return:
        """

        pass


    ##################
    # SELECT QUERIES #
    ##################
    def get_unique_dataset_id(self):
        """
        finds the next unique dataset id
        :return: unique dataset id
        """

        # query the results table, return max(datasetid) + 1

    def get_model_by_code(self,modelcode):
        """

        :param modelcode:
        :return:
        """
        pass

    def get_simulations_by_model(self,modelcode):
        """

        :param modelcode:
        :return:
        """
        pass

    ##################
    # BRIDGE QUERIES #
    ##################

    def bridge_datasetsresults(self,resultid,datasetid):
        """

        :param resultid:
        :param datasetid:
        :return:
        """
        pass


#class mssql():

#     def __init__(self,user,password,host,database):
#         conn = pyodbc.connect("DRIVER={MsSQL};SERVER=localhost;DATABASE=test;USER=openerp;OPTION=3;")
#         self.connection = pyodbc.connect('DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (host, user, password, database))
#         self.cursor = self.connection.cursor()
#
#
#     def close(self):
#         self.connection.close()
#
#     #def connection(self):
#     #    return self.__cnx
#
#     def get_all_ts_meta(self):
#         # what - variable, quantity
#         # when - start, end times
#         # where - geography
#         # how - provenance? simulation or sensor
#         # who - person that created it
#
#         querystring = """SELECT
#                           u.unitsname,u.unitsabbreviation,u.unitstypecv,
#                           v.variabletypecv,v.variablecode,v.variablenamecv,v.variabledefinition,
#                           sf.featuregeometry,
#                           r.resultdatetime,r.resultdatetimeutcoffset,
#                           pl.processinglevelcode,pl.definition,pl.explanation,
#                           tsr.intendedtimespacing,tsr.intendedtimespacingunitsid,
#                           o.organizationcode,o.organizationname,o.organizationdescription,
#                           p.personfirstname,p.personlastname,
#                           m.methodcode,m.methodname,m.methoddescription,
#                           ds.datasetid, ds.datasettypecv, ds.datasettitle
#                         FROM
#                           odm2core.results as r
#                           join odm2core.variables as v on v.variableid = r.variableid
#                           join odm2core.units as u on u.unitsid = r.unitsid
#                           join odm2core.featureactions as fa on fa.featureactionid = r.featureactionid
#                           join odm2core.samplingfeatures as sf on sf.samplingfeatureid = fa.samplingfeatureid
#                           join odm2core.processinglevels as pl on pl.processinglevelid = r.processinglevelid
#                           join odm2results.timeseriesresults as tsr on tsr.resultid = r.resultid
#                           join odm2core.actions as a on a.actionid = fa.actionid
#                           join odm2core.actionby as ab on ab.actionid = a.actionid
#                           join odm2core.affiliations as aff on aff.affiliationid = ab.affiliationid
#                           join odm2core.people as p on p.personid = aff.personid
#                           join odm2core.methods as m on m.methodid = a.methodid
#                           join odm2core.organizations o on o.organizationid = m.organizationid
#                           left join odm2core.datasetsresults dsr on dsr.resultid = r.resultid
#                           left join odm2core.datasets ds on ds.datasetid = dsr.datasetid"""
#
#         query = ' '.join([s.strip() for s in querystring.split('\n')])
#         self.cursor.execute(query)
#         return self.results_to_dict()
#
#
#
# # #dsn = 'sqlserverdatasource'
# # #user = '<username>'
# # #password = '<password>'
# # #database = '<dbname>'
# #
# # con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user, password, database)
# # cnxn = pyodbc.connect(con_string)
#



