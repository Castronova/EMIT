# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from api_old.ODM2.Core.model import Action, Dataset, Method, Organization, Base, Unit



# todo:  This NEEDS to be updated in the ODM2 repository!!!

class Model(Base):
    __tablename__ = 'Models'
    __table_args__ = {u'schema': 'ODM2Simulation'}

    ModelID = Column(Integer, primary_key=True)
    ModelCode = Column(String(255), nullable=False)
    ModelName = Column(String(255), nullable=False)
    ModelDescription = Column(String(500))


class Relatedmodel(Base):
    __tablename__ = 'RelatedModels'
    __table_args__ = {u'schema': 'ODM2Simulation'}

    RelationID = Column(Integer, primary_key=True)
    ModelID = Column(ForeignKey('ODM2Simulation.Models.ModelID'), nullable=False)
    RelationshipTypeCV = Column(String(255), nullable=False)
    RelatedModelID = Column(ForeignKey('ODM2Simulation.Models.ModelID'), nullable=False)

    ModelObj = relationship(u'Model', primaryjoin='Relatedmodel.ModelID == Model.ModelID')
    RelatedModelObj = relationship(u'Model', primaryjoin='Relatedmodel.RelatedModelID == Model.ModelID')


class Simulation(Base):
    __tablename__ = 'Simulations'
    __table_args__ = {u'schema': 'ODM2Simulation'}

    SimulationID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey('ODM2Core.Actions.ActionID'), nullable=False)
    SimulationName = Column(String(255), nullable=False)
    SimulationDescription = Column(String(500))
    SimulationStartDateTime = Column(Date, nullable=False)
    SimulationStartDateTimeUTCOffset = Column(Integer, nullable=False)
    SimulationEndDateTime = Column(Date, nullable=False)
    SimulationEndDateTimeUTCOffset = Column(Integer, nullable=False)
    TimeStepValue = Column(Float(53), nullable=False)
    TimeStepUnitsID = Column(ForeignKey('ODM2Core.Units.UnitsID'), nullable=False)
    InputDataSetID = Column(ForeignKey('ODM2Core.DataSets.DataSetID'))
    OutputDataSetID = Column(Integer)
    ModelID = Column(ForeignKey('ODM2Simulation.Models.ModelID'), nullable=False)

    ActionObj = relationship(u'Action')
    DataSetObj = relationship(u'Dataset')
    ModelObj = relationship(u'Model')
    UnitObj = relationship(u'Unit')
