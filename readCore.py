__author__ = 'Stephanie'

#from odm2.api.ODM2.base import serviceBase


from ...base import  serviceBase
#from ODM2 import serviceBase
import odm2.api.ODM2.Core.model as m
from ..model import *


class readCore(serviceBase):
    """queries to tables contained in the core schema"""

    """
    Variable
    """

    def getAllVariables(self):
        """Select all on Variables

        :return Variable Objects:
            :type list:
        """
        return self._session.query(m.Variable).all()

    def getVariableById(self, variableId):
        """Select by variableId

        :param variableId:
            :type Integer:
        :return Return matching Variable object filtered by variableId:
            :type Variable:
        """
        try:
            return self._session.query(Variable).filter_by(VariableID=variableId).one()
        except:
            return None

    def getVariableByCode(self, variableCode):
        """Select by variableCode

        :param variableCode:
            :type String:
        :return Return matching Variable Object filtered by variableCode:
            :type Variable:
        """
        try:
            return self._session.query(Variable).filter_by(VariableCode=variableCode).one()
        except:
            return None

    """
    Method
    """

    def getAllMethods(self):
        """Select all on Methods

        :return Method Objects:
            :type list:
        """
        return self._session.query(m.Method).all()

    def getMethodById(self, methodId):
        """Select by methodId

        :param methodId:
            :type Integer
        :return Return matching Method Object filtered by methodId:
            :type Method:
        """
        try:
            return self._session.query(m.Method).filter_by(MethodID=methodId).one()
        except:
            return None

    def getMethodByCode(self, methodCode):
        """Select by methodCode

        :param methodCode:
            :type String:
        :return Return matching Method Object filtered by method Code:
            :type Method:
        """
        try:
            return self._session.query(m.Method).filter_by(MethodCode=methodCode).one()
        except:
            return None

    """
    ProcessingLevel
    """

    def getAllProcessingLevel(self):
        """Select all on Processing Level

        :return ProcessingLevel Objects:
            :type list:
        """
        return self._session.query(m.Processinglevel).all()

    def getProcessingLevelById(self, processingId):
        """Select by processingId

        :param processingId:
            :type Integer:
        :return Return matching ProcessingLevel Object filtered by processingId:
            :type Processinglevel:
        """
        try:
            return self._session.query(m.Processinglevel).filter_by(ProcessingLevelID=processingId).one()
        except:
            return None


    def getProcessingLevelByCode(self, processingCode):
        """Select by processingCode

        :param processingCode:
            :type String(50):
        :return Return matching Processinglevel Object filtered by processingCode:
            :type Processinglevel:
        """
        try:
            return self._session.query(m.Processinglevel).filter_by(ProcessingLevelCode=processingCode).one()
        except:
            return None

    """
    Sampling Feature
    """

    def getAllSamplingFeature(self):
        """Select all on SamplingFeatures

        :return SamplingFeature Objects:
            :type list:
        """
        return self._session.query(m.Samplingfeature).all()

    def getSamplingFeatureById(self, samplingId):
        """Select by samplingId

        :param samplingId:
            :type Integer:
        :return Return matching SamplingFeature Object filtered by samplingId:
            :type SamplingFeature:
        """
        try:
            return self._session.query(m.Samplingfeature).filter_by(SamplingFeatureID=samplingId).one()
        except:
            return None

    def getSamplingFeaturebyCode(self, samplingCode):
        """Select by samplingCode

        :param samplingCode:
            :type String:
        :return Return matching SamplingFeature Object filtered by samplingId
            :type SamplingFeature:
        """
        try:
            return self._session.query(m.Samplingfeature).filter_by(SamplingFeatureCode=samplingCode).one()
        except:
            return None

    """
    Unit
    """
    def getAllUnits(self):
        """Select all on Unit

        :return Unit Objects:
            :type list:
        """
        return self._session.query(m.Unit).all()


    def getUnitById(self, unitId):
        """Select by samplingId

        :param unitId:
            :type Integer:
        :return Return matching Unit Object filtered by UnitId:
            :type Unit:
        """
        try:
            return self._session.query(m.Unit).filter_by(UnitsID=unitId).one()
        except:
            return None

    """
    Organization
    """
    def getAllOrganizations(self):
        """Select all on Organization

        :return Organization Objects:
            :type list:
        """
        return self._session.query(m.Organization).all()


    def getOrganizationById(self, orgId):
        """Select by orgId

        :param orgId:
            :type Integer:
        :return Return matching Unit Object filtered by orgId:
            :type Organization:
        """
        try:
            return self._session.query(m.Organization).filter_by(OrganizationID=orgId).one()
        except:
            return None


    def getOrganizationByCode(self, orgCode):
        """Select by orgCode

        :param orgCode:
            :type String:
        :return Return matching Organization Object filtered by orgCode
            :type Organization:
        """
        try:
            return self._session.query(m.Organization).filter_by(OrganizationCode=orgCode).one()
        except:
            return None
    """
    Person
    """
    def getAllPerson(self):
        """Select all on Person

        :return Person Objects:
            :type list:
        """
        return self._session.query(m.Person).all()


    def getPersonById(self, personId):
        """Select by personId

        :param personId:
            :type Integer:
        :return Return matching Person Object filtered by personId:
            :type Person:
        """
        try:
            return self._session.query(Person).filter_by(PersonID=personId).one()
        except:
            return None


    def getPersonByName(self, personfirst, personlast):
        """Select by person name, last name combination

        :param personfirst: first name of person
        :param personlast: last name of person
        :return Return matching Person Object:
            :type Person:
        """
        try:
            return self._session.query(Person).filter(Person.PersonFirstName.ilike(personfirst)). \
                                                 filter(Person.PersonLastName.ilike(personlast)).one()
        except:
            return None