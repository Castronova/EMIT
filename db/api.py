__author__ = 'tonycastronova'

import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import simulation, core

# link exchange item with database entry
#   ts input into models
#   model output saved into database

class postgresdb():

    def __init__(self,user,password,host,database):

        #self.connection = psycopg2.connect(database=database,user=user,password=password,host=host)
        #self.cursor = self.connection.cursor()
        self.cursor = None

        # create postgres engine
        engine = create_engine("postgresql+psycopg2://tonycastronova:waterd@/odm2?host=localhost")
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        self._session = Session()

        #self.connection = self.engine.connect()
        #self.engine = create_engine(database=database,user=user,password=password,host=host)
        #self.engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')

    def close(self):
        self._session.close()

    #def connection(self):
    #    return self.__cnx

    def get_all_variables(self):
        #self.get_simulations()
        #return self._session.query(m.core.Variable).all()
        pass

    def get_simulations(self):
        self._session.query(simulation.Simulation).all()

    def get_all_ts_alc(self):
        return self._session.query(core.Result,core.Samplingfeature).all()
        #return self._session.query(m.Variable).filter_by(VariableID=variableId).one()


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


class mssql():

    def __init__(self,user,password,host,database):
        conn = pyodbc.connect("DRIVER={MsSQL};SERVER=localhost;DATABASE=test;USER=openerp;OPTION=3;")
        self.connection = pyodbc.connect('DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (host, user, password, database))
        self.cursor = self.connection.cursor()


    def close(self):
        self.connection.close()

    #def connection(self):
    #    return self.__cnx

    def get_all_ts_meta(self):
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
        return self.results_to_dict()



# #dsn = 'sqlserverdatasource'
# #user = '<username>'
# #password = '<password>'
# #database = '<dbname>'
#
# con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user, password, database)
# cnxn = pyodbc.connect(con_string)




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