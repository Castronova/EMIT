__author__ = 'sqlacodegen'
#sqlacodegen postgresql+psycopg2://tonycastronova:water@/odm2?host=localhost --schema odm2simulation --outfile simulation.py

# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


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


class Dataset(Base):
    __tablename__ = 'datasets'
    __table_args__ = {u'schema': 'odm2core'}

    datasetid = Column(Integer, primary_key=True)
    datasetuuid = Column(NullType, nullable=False)
    datasettypecv = Column(String(255), nullable=False)
    datasetcode = Column(String(50), nullable=False)
    datasettitle = Column(String(255), nullable=False)
    datasetabstract = Column(String(500), nullable=False)


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


class Unit(Base):
    __tablename__ = 'units'
    __table_args__ = {u'schema': 'odm2core'}

    unitsid = Column(Integer, primary_key=True)
    unitstypecv = Column(String(255), nullable=False)
    unitsabbreviation = Column(String(50), nullable=False)
    unitsname = Column(String(255), nullable=False)


class Model(Base):
    __tablename__ = 'models'
    __table_args__ = {u'schema': 'odm2simulation'}

    modelid = Column(Integer, primary_key=True)
    modelname = Column(String(255), nullable=False)
    modelcode = Column(String(255), nullable=False)
    modeldescription = Column(String(500))


class Relatedmodel(Base):
    __tablename__ = 'relatedmodels'
    __table_args__ = {u'schema': 'odm2simulation'}

    relationid = Column(Integer, primary_key=True)
    modelid = Column(ForeignKey('odm2simulation.models.modelid'), nullable=False)
    relationshiptypecv = Column(String(255), nullable=False)
    relatedmodelid = Column(ForeignKey('odm2simulation.models.modelid'), nullable=False)

    model = relationship(u'Model', primaryjoin='Relatedmodel.modelid == Model.modelid')
    model1 = relationship(u'Model', primaryjoin='Relatedmodel.relatedmodelid == Model.modelid')


class Simulation(Base):
    __tablename__ = 'simulations'
    __table_args__ = {u'schema': 'odm2simulation'}

    SimulationID = Column(Integer, primary_key=True)
    actionid = Column(ForeignKey('odm2core.actions.actionid'), nullable=False)
    simulationname = Column(String(255), nullable=False)
    simulationdescription = Column(String(500))
    simulationstartdatetime = Column(Date, nullable=False)
    simulationstartdatetimeutcoffset = Column(Integer, server_default=u'0')
    simulationenddatetime = Column(Date, nullable=False)
    simulationenddatetimeutcoffset = Column(Integer, server_default=u'0')
    timestepvalue = Column(Float(53), nullable=False)
    timestepunitsid = Column(ForeignKey('odm2core.units.unitsid'), nullable=False)
    inputdatasetid = Column(ForeignKey('odm2core.datasets.datasetid'))
    modelid = Column(ForeignKey('odm2simulation.models.modelid'), nullable=False)

    action = relationship(u'Action')
    dataset = relationship(u'Dataset')
    model = relationship(u'Model')
    unit = relationship(u'Unit')
