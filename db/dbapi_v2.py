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

    def create_simulation(self,preferences_path, config_params, output_exchange_items):
        pass

    def get_simulation_results(self,simulationName, dbactions, from_variableName, from_unitName, to_variableName, startTime, endTime):
        pass



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





