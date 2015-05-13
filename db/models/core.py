__author__ = "sqlacodegen"
# had to add geoalchemy to support geometry types
# see: https://bitbucket.org/agronholm/sqlacodegen/pull-request/1/added-support-for-geoalchemy2-and-backrefs/diff

from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from geoalchemy2.types import Geometry
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Actionby(Base):
    __tablename__ = 'actionby'
    __table_args__ = {u'schema': 'odm2core'}

    bridgeid = Column(Integer, primary_key=True)
    actionid = Column(ForeignKey('odm2core.actions.actionid'), nullable=False)
    affiliationid = Column(ForeignKey('odm2core.affiliations.affiliationid'), nullable=False)
    isactionlead = Column(Boolean, nullable=False)
    roledescription = Column(String(500))

    action = relationship(u'Action')
    affiliation = relationship(u'Affiliation')


class Action(Base):
    __tablename__ = 'actions'
    __table_args__ = {u'schema': 'odm2core'}

    actionid = Column(Integer, primary_key=True)
    actiontypecv = Column(String(255), nullable=False)
    methodid = Column(ForeignKey('odm2core.methods.methodid'), nullable=False)
    begindatetime = Column(DateTime, nullable=False)
    begindatetimeutcoffset = Column(Integer, nullable=False)
    enddatetime = Column(DateTime)
    enddatetimeutcoffset = Column(Integer)
    actiondescription = Column(String(500))
    actionfilelink = Column(String(255))

    method = relationship(u'Method')


class Affiliation(Base):
    __tablename__ = 'affiliations'
    __table_args__ = {u'schema': 'odm2core'}

    affiliationid = Column(Integer, primary_key=True)
    personid = Column(ForeignKey('odm2core.people.personid'), nullable=False)
    organizationid = Column(ForeignKey('odm2core.organizations.organizationid'))
    isprimaryorganizationcontact = Column(Boolean)
    affiliationstartdate = Column(Date, nullable=False)
    affiliationenddate = Column(Date)
    primaryphone = Column(String(50))
    primaryemail = Column(String(255), nullable=False)
    primaryaddress = Column(String(255))
    personlink = Column(String(255))

    organization = relationship(u'Organization')
    person = relationship(u'Person')


class Dataset(Base):
    __tablename__ = 'datasets'
    __table_args__ = {u'schema': 'odm2core'}

    datasetid = Column(Integer, primary_key=True)
    datasetuuid = Column(NullType, nullable=False)
    datasettypecv = Column(String(255), nullable=False)
    datasetcode = Column(String(50), nullable=False)
    datasettitle = Column(String(255), nullable=False)
    datasetabstract = Column(String(500), nullable=False)


class Datasetsresult(Base):
    __tablename__ = 'datasetsresults'
    __table_args__ = {u'schema': 'odm2core'}

    bridgeid = Column(Integer, primary_key=True)
    datasetid = Column(ForeignKey('odm2core.datasets.datasetid'), nullable=False)
    resultid = Column(ForeignKey('odm2core.results.resultid'), nullable=False)

    dataset = relationship(u'Dataset')
    result = relationship(u'Result')


class Featureaction(Base):
    __tablename__ = 'featureactions'
    __table_args__ = {u'schema': 'odm2core'}

    featureactionid = Column(Integer, primary_key=True)
    samplingfeatureid = Column(ForeignKey('odm2core.samplingfeatures.samplingfeatureid'), nullable=False)
    actionid = Column(ForeignKey('odm2core.actions.actionid'), nullable=False)

    action = relationship(u'Action')
    samplingfeature = relationship(u'Samplingfeature')


class Method(Base):
    __tablename__ = 'methods'
    __table_args__ = {u'schema': 'odm2core'}

    methodid = Column(Integer, primary_key=True)
    methodtypecv = Column(String(255), nullable=False)
    methodcode = Column(String(50), nullable=False)
    methodname = Column(String(255), nullable=False)
    methoddescription = Column(String(500))
    methodlink = Column(String(255))
    organizationid = Column(ForeignKey('odm2core.organizations.organizationid'))

    organization = relationship(u'Organization')


class Organization(Base):
    __tablename__ = 'organizations'
    __table_args__ = {u'schema': 'odm2core'}

    organizationid = Column(Integer, primary_key=True)
    organizationtypecv = Column(String(255), nullable=False)
    organizationcode = Column(String(50), nullable=False)
    organizationname = Column(String(255), nullable=False)
    organizationdescription = Column(String(500))
    organizationlink = Column(String(255))
    parentorganizationid = Column(ForeignKey('odm2core.organizations.organizationid'))

    parent = relationship(u'Organization', remote_side=[organizationid])


class Person(Base):
    __tablename__ = 'people'
    __table_args__ = {u'schema': 'odm2core'}

    personid = Column(Integer, primary_key=True)
    personfirstname = Column(String(255), nullable=False)
    personmiddlename = Column(String(255))
    personlastname = Column(String(255), nullable=False)


class Processinglevel(Base):
    __tablename__ = 'processinglevels'
    __table_args__ = {u'schema': 'odm2core'}

    processinglevelid = Column(Integer, primary_key=True)
    processinglevelcode = Column(String(50), nullable=False)
    definition = Column(String(500))
    explanation = Column(String(500))


class Relatedaction(Base):
    __tablename__ = 'relatedactions'
    __table_args__ = {u'schema': 'odm2core'}

    relationid = Column(Integer, primary_key=True)
    actionid = Column(ForeignKey('odm2core.actions.actionid'), nullable=False)
    relationshiptypecv = Column(String(255), nullable=False)
    relatedactionid = Column(ForeignKey('odm2core.actions.actionid'), nullable=False)

    action = relationship(u'Action', primaryjoin='Relatedaction.actionid == Action.actionid')
    action1 = relationship(u'Action', primaryjoin='Relatedaction.relatedactionid == Action.actionid')


class Result(Base):
    __tablename__ = 'results'
    __table_args__ = {u'schema': 'odm2core'}

    resultid = Column(BigInteger, primary_key=True)
    resultuuid = Column(NullType, nullable=False)
    featureactionid = Column(ForeignKey('odm2core.featureactions.featureactionid'), nullable=False)
    resulttypecv = Column(ForeignKey('odm2results.resulttypecv.resulttypecv'), nullable=False)
    variableid = Column(ForeignKey('odm2core.variables.variableid'), nullable=False)
    unitsid = Column(ForeignKey('odm2core.units.unitsid'), nullable=False)
    taxonomicclassifierid = Column(ForeignKey('odm2core.taxonomicclassifiers.taxonomicclassifierid'))
    processinglevelid = Column(ForeignKey('odm2core.processinglevels.processinglevelid'), nullable=False)
    resultdatetime = Column(DateTime)
    resultdatetimeutcoffset = Column(BigInteger)
    validdatetime = Column(DateTime)
    validdatetimeutcoffset = Column(BigInteger)
    statuscv = Column(String(255))
    sampledmediumcv = Column(String(255), nullable=False)
    valuecount = Column(Integer, nullable=False)

    featureaction = relationship(u'Featureaction')
    processinglevel = relationship(u'Processinglevel')
    resulttypecv1 = relationship(u'Resulttypecv')
    taxonomicclassifier = relationship(u'Taxonomicclassifier')
    unit = relationship(u'Unit')
    variable = relationship(u'Variable')


class Samplingfeature(Base):
    __tablename__ = 'samplingfeatures'
    __table_args__ = {u'schema': 'odm2core'}

    samplingfeatureid = Column(Integer, primary_key=True)
    samplingfeaturetypecv = Column(String(255), nullable=False)
    samplingfeaturecode = Column(String(50), nullable=False)
    samplingfeaturename = Column(String(255))
    samplingfeaturedescription = Column(String(500))
    samplingfeaturegeotypecv = Column(String(255))
    featuregeometry = Column(Geometry)
    elevation_m = Column(Float(53))
    elevationdatumcv = Column(String(255))


class Taxonomicclassifier(Base):
    __tablename__ = 'taxonomicclassifiers'
    __table_args__ = {u'schema': 'odm2core'}

    taxonomicclassifierid = Column(Integer, primary_key=True)
    taxonomicclassifiertypecv = Column(String(255), nullable=False)
    taxonomicclassifiername = Column(String(255), nullable=False)
    taxonomicclassifiercommonname = Column(String(255))
    taxonomicclassifierdescription = Column(String(500))
    parenttaxonomicclassifierid = Column(ForeignKey('odm2core.taxonomicclassifiers.taxonomicclassifierid'))

    parent = relationship(u'Taxonomicclassifier', remote_side=[taxonomicclassifierid])


class Unit(Base):
    __tablename__ = 'units'
    __table_args__ = {u'schema': 'odm2core'}

    unitsid = Column(Integer, primary_key=True)
    unitstypecv = Column(String(255), nullable=False)
    unitsabbreviation = Column(String(50), nullable=False)
    unitsname = Column(String(255), nullable=False)


class Variable(Base):
    __tablename__ = 'variables'
    __table_args__ = {u'schema': 'odm2core'}

    variableid = Column(Integer, primary_key=True)
    variabletypecv = Column(String(255), nullable=False)
    variablecode = Column(String(50), nullable=False)
    variablenamecv = Column(String(255), nullable=False)
    variabledefinition = Column(String(500))
    speciationcv = Column(String(255))
    nodatavalue = Column(Float(53), nullable=False)


class Resulttypecv(Base):
    __tablename__ = 'resulttypecv'
    __table_args__ = {u'schema': 'odm2results'}

    resulttypecv = Column(String(255), primary_key=True)
    resulttypecategory = Column(String(255), nullable=False)
    datatype = Column(String(255), nullable=False)
    resulttypedefinition = Column(String(500), nullable=False)
    fixeddimensions = Column(String(255), nullable=False)
    varyingdimensions = Column(String(255), nullable=False)
    spacemeasurementframework = Column(String(255), nullable=False)
    timemeasurementframework = Column(String(255), nullable=False)
    variablemeasurementframework = Column(String(255), nullable=False)
