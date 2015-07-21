BEGIN TRANSACTION;
CREATE TABLE ActionAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Annotations (
	AnnotationID INTEGER   NOT NULL PRIMARY KEY,
	AnnotationTypeCV VARCHAR (255)  NOT NULL,
	AnnotationCode VARCHAR (50)  NULL,
	AnnotationText VARCHAR (500)  NOT NULL,
	AnnotationDateTime DATETIME   NULL,
	AnnotationUTCOffset INTEGER   NULL,
	AnnotationLink VARCHAR (255)  NULL,
	AnnotatorID INTEGER   NULL,
	CitationID INTEGER   NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (AnnotationTypeCV) REFERENCES CV_AnnotationType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (AnnotatorID) REFERENCES People (PersonID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CategoricalResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ValueID) REFERENCES CategoricalResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE EquipmentAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	EquipmentID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (EquipmentID) REFERENCES Equipment (EquipmentID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE MeasurementResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (ValueID) REFERENCES MeasurementResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE MethodAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	MethodID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (MethodID) REFERENCES Methods (MethodID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE PointCoverageResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ValueID) REFERENCES PointCoverageResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ProfileResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ValueID) REFERENCES ProfileResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ResultAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	BeginDateTime DATETIME   NOT NULL,
	EndDateTime DATETIME   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SamplingFeatureAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	SamplingFeatureID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SectionResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ValueID) REFERENCES SectionResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SpectraResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ValueID) REFERENCES SpectraResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TimeSeriesResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ValueID) REFERENCES TimeSeriesResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TrajectoryResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ValueID) REFERENCES TrajectoryResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TransectResultValueAnnotations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ValueID INTEGER   NOT NULL,
	AnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ValueID) REFERENCES TransectResultValues (ValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ActionBy (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	AffiliationID INTEGER   NOT NULL,
	IsActionLead BIT   NOT NULL,
	RoleDescription VARCHAR (500)  NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (AffiliationID) REFERENCES Affiliations (AffiliationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Actions (
	ActionID INTEGER   NOT NULL PRIMARY KEY,
	ActionTypeCV VARCHAR (255)  NOT NULL,
	MethodID INTEGER   NOT NULL,
	BeginDateTime DATETIME   NOT NULL,
	BeginDateTimeUTCOffset INTEGER   NOT NULL,
	EndDateTime DATETIME   NULL,
	EndDateTimeUTCOffset INTEGER   NULL,
	ActionDescription VARCHAR (500)  NULL,
	ActionFileLink VARCHAR (255)  NULL,
	FOREIGN KEY (ActionTypeCV) REFERENCES CV_ActionType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (MethodID) REFERENCES Methods (MethodID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Affiliations (
	AffiliationID INTEGER   NOT NULL PRIMARY KEY,
	PersonID INTEGER   NOT NULL,
	OrganizationID INTEGER   NULL,
	IsPrimaryOrganizationContact BIT   NULL,
	AffiliationStartDate DATE   NOT NULL,
	AffiliationEndDate DATE   NULL,
	PrimaryPhone VARCHAR (50)  NULL,
	PrimaryEmail VARCHAR (255)  NOT NULL,
	PrimaryAddress VARCHAR (255)  NULL,
	PersonLink VARCHAR (255)  NULL,
	FOREIGN KEY (OrganizationID) REFERENCES Organizations (OrganizationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (PersonID) REFERENCES People (PersonID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Datasets (
	DatasetID INTEGER   NOT NULL PRIMARY KEY,
	DatasetUUID VARCHAR(36)   NOT NULL,
	DatasetTypeCV VARCHAR (255)  NOT NULL,
	DatasetCode VARCHAR (50)  NOT NULL,
	DatasetTitle VARCHAR (255)  NOT NULL,
	DatasetAbstract VARCHAR (500)  NOT NULL,
	FOREIGN KEY (DatasetTypeCV) REFERENCES CV_DatasetType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE DatasetsResults (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	DatasetID INTEGER   NOT NULL,
	ResultID INTEGER   NOT NULL,
	FOREIGN KEY (DatasetID) REFERENCES Datasets (DatasetID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE FeatureActions (
	FeatureActionID INTEGER   NOT NULL PRIMARY KEY,
	SamplingFeatureID INTEGER   NOT NULL,
	ActionID INTEGER   NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Methods (
	MethodID INTEGER   NOT NULL PRIMARY KEY,
	MethodTypeCV VARCHAR (255)  NOT NULL,
	MethodCode VARCHAR (50)  NOT NULL,
	MethodName VARCHAR (255)  NOT NULL,
	MethodDescription VARCHAR (500)  NULL,
	MethodLink VARCHAR (255)  NULL,
	OrganizationID INTEGER   NULL,
	FOREIGN KEY (MethodTypeCV) REFERENCES CV_MethodType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (OrganizationID) REFERENCES Organizations (OrganizationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Organizations (
	OrganizationID INTEGER   NOT NULL PRIMARY KEY,
	OrganizationTypeCV VARCHAR (255)  NOT NULL,
	OrganizationCode VARCHAR (50)  NOT NULL,
	OrganizationName VARCHAR (255)  NOT NULL,
	OrganizationDescription VARCHAR (500)  NULL,
	OrganizationLink VARCHAR (255)  NULL,
	ParentOrganizationID INTEGER   NULL,
	FOREIGN KEY (OrganizationTypeCV) REFERENCES CV_OrganizationType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ParentOrganizationID) REFERENCES Organizations (OrganizationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE People (
	PersonID INTEGER   NOT NULL PRIMARY KEY,
	PersonFirstName VARCHAR (255)  NOT NULL,
	PersonMiddleName VARCHAR (255)  NULL,
	PersonLastName VARCHAR (255)  NOT NULL
);
CREATE TABLE ProcessingLevels (
	ProcessingLevelID INTEGER   NOT NULL PRIMARY KEY,
	ProcessingLevelCode VARCHAR (50)  NOT NULL,
	Definition VARCHAR (500)  NULL,
	Explanation VARCHAR (500)  NULL
);
CREATE TABLE RelatedActions (
	RelationID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	RelatedActionID INTEGER   NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelatedActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Results (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	ResultUUID VARCHAR(36)   NOT NULL,
	FeatureActionID INTEGER   NOT NULL,
	ResultTypeCV VARCHAR (255)  NOT NULL,
	VariableID INTEGER   NOT NULL,
	UnitsID INTEGER   NOT NULL,
	TaxonomicClassifierID INTEGER   NULL,
	ProcessingLevelID INTEGER   NOT NULL,
	ResultDateTime DATETIME   NULL,
	ResultDateTimeUTCOffset INTEGER   NULL,
	ValidDateTime DATETIME   NULL,
	ValidDateTimeUTCOffset INTEGER   NULL,
	StatusCV VARCHAR (255)  NULL,
	SampledMediumCV VARCHAR (255)  NOT NULL,
	ValueCount INTEGER   NOT NULL,
	FOREIGN KEY (ResultTypeCV) REFERENCES CV_ResultType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SampledMediumCV) REFERENCES CV_SampledMedium (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (StatusCV) REFERENCES CV_Status (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (FeatureActionID) REFERENCES FeatureActions (FeatureActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ProcessingLevelID) REFERENCES ProcessingLevels (ProcessingLevelID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (TaxonomicClassifierID) REFERENCES TaxonomicClassifiers (TaxonomicClassifierID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (UnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (VariableID) REFERENCES Variables (VariableID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SamplingFeatures (
	SamplingFeatureID INTEGER   NOT NULL PRIMARY KEY,
	SamplingFeatureUUID VARCHAR(36)   NOT NULL,
	SamplingFeatureTypeCV VARCHAR (255)  NOT NULL,
	SamplingFeatureCode VARCHAR (50)  NOT NULL,
	SamplingFeatureName VARCHAR (255)  NULL,
	SamplingFeatureDescription VARCHAR (500)  NULL,
	SamplingFeatureGeotypeCV VARCHAR (255)  NULL,
	FeatureGeometry geometry   NULL,
	Elevation_m FLOAT   NULL,
	ElevationDatumCV VARCHAR (255)  NULL,
	FOREIGN KEY (ElevationDatumCV) REFERENCES CV_ElevationDatum (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureGeotypeCV) REFERENCES CV_SamplingFeatureGeoType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureTypeCV) REFERENCES CV_SamplingFeatureType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TaxonomicClassifiers (
	TaxonomicClassifierID INTEGER   NOT NULL PRIMARY KEY,
	TaxonomicClassifierTypeCV VARCHAR (255)  NOT NULL,
	TaxonomicClassifierName VARCHAR (255)  NOT NULL,
	TaxonomicClassifierCommonName VARCHAR (255)  NULL,
	TaxonomicClassifierDescription VARCHAR (500)  NULL,
	ParentTaxonomicClassifierID INTEGER   NULL,
	FOREIGN KEY (ParentTaxonomicClassifierID) REFERENCES TaxonomicClassifiers (TaxonomicClassifierID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (TaxonomicClassifierTypeCV) REFERENCES CV_TaxonomicClassifierType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Units (
	UnitsID INTEGER   NOT NULL PRIMARY KEY,
	UnitsTypeCV VARCHAR (255)  NOT NULL,
	UnitsAbbreviation VARCHAR (50)  NOT NULL,
	UnitsName VARCHAR (255)  NOT NULL,
	UnitsLink VARCHAR (255)  NULL,
	FOREIGN KEY (UnitsTypeCV) REFERENCES CV_UnitsType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Variables (
	VariableID INTEGER   NOT NULL PRIMARY KEY,
	VariableTypeCV VARCHAR (255)  NOT NULL,
	VariableCode VARCHAR (50)  NOT NULL,
	VariableNameCV VARCHAR (255)  NOT NULL,
	VariableDefinition VARCHAR (500)  NULL,
	SpeciationCV VARCHAR (255)  NULL,
	NoDataValue DOUBLE   NOT NULL,
	FOREIGN KEY (SpeciationCV) REFERENCES CV_Speciation (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (VariableNameCV) REFERENCES CV_VariableName (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (VariableTypeCV) REFERENCES CV_VariableType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CV_ActionType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_ActionType" VALUES('equipmentRetrieval','Equipment retrieval','The act of recovering a piece of equipment that made no observations from a deployment at a sampling feature or other location. For instruments, the more specific term Instrument retrieval should be used.','Equipment','http://vocabulary.odm2.org/actiontype/equipmentRetrieval');
INSERT INTO "CV_ActionType" VALUES('dataRetrieval','Data retrieval','The act of retrieving data from a datalogger deployed at a monitoring site.','Equipment','http://vocabulary.odm2.org/actiontype/dataRetrieval');
INSERT INTO "CV_ActionType" VALUES('equipmentProgramming','Equipment programming','The act of creating or modifying the data collection program running on a datalogger or other equipment deployed at a monitoring site.','Equipment','http://vocabulary.odm2.org/actiontype/equipmentProgramming');
INSERT INTO "CV_ActionType" VALUES('fieldActivity','Field activity','A generic, non-specific action type performed in the field at or on a sampling feature.','FieldActivity','http://vocabulary.odm2.org/actiontype/fieldActivity');
INSERT INTO "CV_ActionType" VALUES('specimenAnalysis','Specimen analysis','The analysis of a specimen ex situ using an instrument, typically in a laboratory, for the purpose of measuring properties of that specimen.','Observation','http://vocabulary.odm2.org/actiontype/specimenAnalysis');
INSERT INTO "CV_ActionType" VALUES('derivation','Derivation','The act of creating results by deriving them from other results.','Observation','http://vocabulary.odm2.org/actiontype/derivation');
INSERT INTO "CV_ActionType" VALUES('expedition','Expedition','A field visit action in which many sites are visited over a continguous period of time, often involving serveral investigators, and typically having a specific purpose.  Expedition actions are typically parents to other related Actions.','FieldActivity','http://vocabulary.odm2.org/actiontype/expedition');
INSERT INTO "CV_ActionType" VALUES('observation','Observation','The general act of making an observation. This term should be used when a Result is generated but the more specific terms of Instrument deployment or Specimen analysis are not applicable.','Observation','http://vocabulary.odm2.org/actiontype/observation');
INSERT INTO "CV_ActionType" VALUES('estimation','Estimation','The act of creating results by estimation or professional judgement.','Observation','http://vocabulary.odm2.org/actiontype/estimation');
INSERT INTO "CV_ActionType" VALUES('instrumentDeployment','Instrument deployment','The act of deploying an in situ instrument or sensor that creates an observation result.  This term is a specific form of the Observation actions category of actions, which is the only category of actions that can produce observation results.','Observation','http://vocabulary.odm2.org/actiontype/instrumentDeployment');
INSERT INTO "CV_ActionType" VALUES('equipmentMaintenance','Equipment maintenance','The act of performing regular or periodic upkeep or servicing of field or laboratory equipment. Maintenance may be performed in the field, in a laboratory, or at a factory maintenance center.','Equipment','http://vocabulary.odm2.org/actiontype/equipmentMaintenance');
INSERT INTO "CV_ActionType" VALUES('cruise','Cruise','A specialized form of an expedition action that involves an ocean-going vessel. Cruise actions are typically parents to other related Actions.','FieldActivity','http://vocabulary.odm2.org/actiontype/cruise');
INSERT INTO "CV_ActionType" VALUES('simulation','Simulation','The act of calculating results through the use of a simulation model.','Observation','http://vocabulary.odm2.org/actiontype/simulation');
INSERT INTO "CV_ActionType" VALUES('specimenPreparation','Specimen preparation','The processing of a specimen collected in the field to produce a sample suitable for analysis using a particular analytical procedure.','SamplingFeature','http://vocabulary.odm2.org/actiontype/specimenPreparation');
INSERT INTO "CV_ActionType" VALUES('specimenCollection','Specimen collection','The collection of a specimen in the field.','SamplingFeature','http://vocabulary.odm2.org/actiontype/specimenCollection');
INSERT INTO "CV_ActionType" VALUES('genericNonObservation','Generic non-observation','A generic, non-specific action type that does not produce a result.','Other','http://vocabulary.odm2.org/actiontype/genericNonObservation');
INSERT INTO "CV_ActionType" VALUES('instrumentCalibration','Instrument calibration','The act of calibrating an instrument either in the field or in a laboratory. The instrument may be an in situ field sensor or a laboratory instrument.  An instrument is the subclass of equipment that is capable of making an observation to produce a result.','Equipment','http://vocabulary.odm2.org/actiontype/instrumentCalibration');
INSERT INTO "CV_ActionType" VALUES('submersibleLaunch','Submersible launch','The act of deploying a submersible from a vessel or ship.','FieldActivity','http://vocabulary.odm2.org/actiontype/submersibleLaunch');
INSERT INTO "CV_ActionType" VALUES('specimenPreservation','Specimen preservation','The act of preserving a specimen collected in the field to produce a sample suitable for analysis using a particular analytical procedure.','SamplingFeature','http://vocabulary.odm2.org/actiontype/specimenPreservation');
INSERT INTO "CV_ActionType" VALUES('instrumentRetrieval','Instrument retrieval','The act of recovering an in situ instrument (which made observations) from a sampling feature. This action ends an instrument deployment action.','Equipment','http://vocabulary.odm2.org/actiontype/instrumentRetrieval');
CREATE TABLE CV_AggregationStatistic (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_AggregationStatistic" VALUES('categorical','Categorical','The values are categorical rather than continuous valued quantities.',NULL,'http://vocabulary.odm2.org/aggregationstatistic/categorical');
INSERT INTO "CV_AggregationStatistic" VALUES('variance','Variance','The values represent the variance of a set of observations made over a time interval. Variance computed using the unbiased formula SUM((Xi-mean)^2)/(n-1) are preferred. The specific formula used to compute variance can be noted in the methods description.',NULL,'http://vocabulary.odm2.org/aggregationstatistic/variance');
INSERT INTO "CV_AggregationStatistic" VALUES('continuous','Continuous','A quantity specified at a particular instant in time measured with sufficient frequency (small spacing) to be interpreted as a continuous record of the phenomenon.',NULL,'http://vocabulary.odm2.org/aggregationstatistic/continuous');
INSERT INTO "CV_AggregationStatistic" VALUES('maximum','Maximum','The values are the maximum values occurring at some time during a time interval, such as annual maximum discharge or a daily maximum air temperature.',NULL,'http://vocabulary.odm2.org/aggregationstatistic/maximum');
INSERT INTO "CV_AggregationStatistic" VALUES('unknown','Unknown','The aggregation statistic is unknown.',NULL,'http://vocabulary.odm2.org/aggregationstatistic/unknown');
INSERT INTO "CV_AggregationStatistic" VALUES('constantOverInterval','Constant over interval','The values are quantities that can be interpreted as constant for all time, or over the time interval to a subsequent measurement of the same variable at the same site.',NULL,'http://vocabulary.odm2.org/aggregationstatistic/constantOverInterval');
INSERT INTO "CV_AggregationStatistic" VALUES('average','Average','The values represent the average over a time interval, such as daily mean discharge or daily mean temperature.',NULL,'http://vocabulary.odm2.org/aggregationstatistic/average');
INSERT INTO "CV_AggregationStatistic" VALUES('bestEasySystematicEstimator','Best easy systematic estimator','Best Easy Systematic Estimator BES = (Q1 +2Q2 +Q3)/4. Q1, Q2, and Q3 are first, second, and third quartiles. See Woodcock, F. and Engel, C., 2005: Operational Consensus Forecasts.Weather and Forecasting, 20, 101-111. (http://www.bom.gov.au/nmoc/bulletins/60/article_by_Woodcock_in_Weather_and_Forecasting.pdf) and Wonnacott, T. H., and R. J. Wonnacott, 1972: Introductory Statistics. Wiley, 510 pp.',NULL,'http://vocabulary.odm2.org/aggregationstatistic/bestEasySystematicEstimator');
CREATE TABLE CV_AnnotationType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_AnnotationType" VALUES('resultAnnotation','Result annotation','An annotation or qualifying comment about a Result','Annotation','http://vocabulary.odm2.org/annotationtype/resultAnnotation');
INSERT INTO "CV_AnnotationType" VALUES('organizationAnnotation','Organization annotation','An annotation or qualifiying comment about an Organization','Annotation','http://vocabulary.odm2.org/annotationtype/organizationAnnotation');
INSERT INTO "CV_AnnotationType" VALUES('measurementResultValueAnnotation','Measurement result value annotation','An annotation or data qualifying comment applied to a data value from a measurement Result','Annotation','http://vocabulary.odm2.org/annotationtype/measurementResultValueAnnotation');
INSERT INTO "CV_AnnotationType" VALUES('specimenAnnotation','Specimen annotation','An annotation or qualifying comment about a Specimen','Annotation','http://vocabulary.odm2.org/annotationtype/specimenAnnotation');
INSERT INTO "CV_AnnotationType" VALUES('samplingFeatureAnnotation','Sampling feature annotation','An annotation or qualifiying comment about a SamplingFeature','Annotation','http://vocabulary.odm2.org/annotationtype/samplingFeatureAnnotation');
INSERT INTO "CV_AnnotationType" VALUES('profileResultValueAnnotation','Profile result value annotation','An annotation or data qualifying comment applied to a data value from a profile Result','Annotation','http://vocabulary.odm2.org/annotationtype/profileResultValueAnnotation');
INSERT INTO "CV_AnnotationType" VALUES('personAnnotation','Person annotation','An annotation or qualifying comment about a Person','Annotation','http://vocabulary.odm2.org/annotationtype/personAnnotation');
CREATE TABLE CV_CensorCode (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_CensorCode" VALUES('presentButNotQuantified','Present but not quantified','The anlayte is known to be present, but was not quantified. The recorded value represents the level below which the analyte can no longer be quantified.',NULL,'http://vocabulary.odm2.org/censorcode/presentButNotQuantified');
INSERT INTO "CV_CensorCode" VALUES('notCensored','Not censored','The reported value is not censored.',NULL,'http://vocabulary.odm2.org/censorcode/notCensored');
INSERT INTO "CV_CensorCode" VALUES('greaterThan','Greater than','The value is known to be greater than the recorded value.',NULL,'http://vocabulary.odm2.org/censorcode/greaterThan');
INSERT INTO "CV_CensorCode" VALUES('lessThan','Less than','The value is known to be less than the recorded value.',NULL,'http://vocabulary.odm2.org/censorcode/lessThan');
INSERT INTO "CV_CensorCode" VALUES('nonDetect','Non-detect','The value was reported as a non-detect. The recorded value represents the level at which the anlalyte can be detected.',NULL,'http://vocabulary.odm2.org/censorcode/nonDetect');
CREATE TABLE CV_DataQualityType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_DatasetType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_DatasetType" VALUES('multiTimeSeries','Multi-time series','A Dataset that contains multiple time series Results. This corresponds to the YAML Observations Data Archive (YODA) multi-time series profile.',NULL,'http://vocabulary.odm2.org/datasettype/multiTimeSeries');
INSERT INTO "CV_DatasetType" VALUES('singleTimeSeries','Single time series','A Dataset that contains a single time series Result. This corresponds to the YAML Observations Data Archive (YODA) singe time series profile.',NULL,'http://vocabulary.odm2.org/datasettype/singleTimeSeries');
INSERT INTO "CV_DatasetType" VALUES('other','Other','A set of Results that has been grouped into a Dataset because they are logically related. The group does not conform to any particular profile.',NULL,'http://vocabulary.odm2.org/datasettype/other');
INSERT INTO "CV_DatasetType" VALUES('multiVariableSpecimenMeasurements','Multi-variable specimen measurements','A dataset that contains multiple measurement Results derived from Specimens. This corresponds to the YAML Observations Data Archive (YODA) specimen time series profile.',NULL,'http://vocabulary.odm2.org/datasettype/multiVariableSpecimenMeasurements');
CREATE TABLE CV_DirectiveType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_DirectiveType" VALUES('monitoringProgram','Monitoring program','Environmental monitoring that is conducted according to a formal plan that may reflect the overall objectives of an organization, references specific strategies that help deliver the objectives and details of specific projects or tasks, and that contains a listing of what is being monitored, how that monitoring is taking place, and the time-scale over which monitoring should take place.',NULL,'http://vocabulary.odm2.org/directivetype/monitoringProgram');
INSERT INTO "CV_DirectiveType" VALUES('project','Project','A collaborative enterprise, involving research or design, the is carefully planned to achieve a particular aim.',NULL,'http://vocabulary.odm2.org/directivetype/project');
CREATE TABLE CV_ElevationDatum (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_ElevationDatum" VALUES('MSL','MSL','Mean Sea Level',NULL,'http://vocabulary.odm2.org/elevationdatum/MSL');
INSERT INTO "CV_ElevationDatum" VALUES('NGVD29','NGVD29','National Geodetic Vertical Datum of 1929',NULL,'http://vocabulary.odm2.org/elevationdatum/NGVD29');
INSERT INTO "CV_ElevationDatum" VALUES('NAVD88','NAVD88','North American Vertical Datum of 1988',NULL,'http://vocabulary.odm2.org/elevationdatum/NAVD88');
CREATE TABLE CV_EquipmentType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_EquipmentType" VALUES('solarPanel','Solar panel','A photovoltaic module that is electrically connected and mounted on a supporting structure.  Used to generate and supply electricity.','Power component','http://vocabulary.odm2.org/equipmenttype/solarPanel');
INSERT INTO "CV_EquipmentType" VALUES('tripod','Tripod','A portable, three-legged frame used as a platform for supporting the weight and maintaining the stability of some other object. Typically used as a data collection platform to which sensors are attached.','Observation platform','http://vocabulary.odm2.org/equipmenttype/tripod');
INSERT INTO "CV_EquipmentType" VALUES('enclosure','Enclosure','A cabinet or box within which electrical or electronic equipment are mounted to protect them from the environment.','Platform','http://vocabulary.odm2.org/equipmenttype/enclosure');
INSERT INTO "CV_EquipmentType" VALUES('laboratoryInstrument','Laboratory instrument','Any type of equipment, apparatus or device designed, constructed and refined to use well proven physical principles, relationships or technology to facilitate or enable the pursuit, acquisition, transduction and storage of repeatable, verifiable data, usually consisting of sets numerical measurements made upon otherwise unknown, unproven quantities, properties, phenomena, materials, forces or etc.','Instrument','http://vocabulary.odm2.org/equipmenttype/laboratoryInstrument');
INSERT INTO "CV_EquipmentType" VALUES('globalPositioningSystemReceiver','Global positioning system receiver','A device that accurately calculates geographical location by receiving information from Global Positioning System satellites.','Sensor','http://vocabulary.odm2.org/equipmenttype/globalPositioningSystemReceiver');
INSERT INTO "CV_EquipmentType" VALUES('pressureTransducer','Pressure transducer','A sensor that measures pressure, typically of gases or liquids.','Sensor','http://vocabulary.odm2.org/equipmenttype/pressureTransducer');
INSERT INTO "CV_EquipmentType" VALUES('datalogger','Datalogger','An electronic device that records data over time or in relation to location either with a built in instrument or sensor or via external instruments and sensors.','Datalogger','http://vocabulary.odm2.org/equipmenttype/datalogger');
INSERT INTO "CV_EquipmentType" VALUES('mast','Mast','A pole that supports sensors, instruments, or measurement peripherals.','Observation platform','http://vocabulary.odm2.org/equipmenttype/mast');
INSERT INTO "CV_EquipmentType" VALUES('measurementTower','Measurement tower','A free standing tower that supports measuring instruments or sensors.','Observation platform','http://vocabulary.odm2.org/equipmenttype/measurementTower');
INSERT INTO "CV_EquipmentType" VALUES('chargeRegulator','Charge regulator','An electroinic device that limits the rate at which electric current is added to or drawn from electric batteries.','Power component','http://vocabulary.odm2.org/equipmenttype/chargeRegulator');
CREATE TABLE CV_MethodType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_MethodType" VALUES('unknown','Unknown','The method type is unknown.','Other','http://vocabulary.odm2.org/methodtype/unknown');
INSERT INTO "CV_MethodType" VALUES('specimenPreparation','Specimen preparation','A method for processing a specimen collected in the field to produce a sample suitable for analysis using a particular analytical procedure.','SamplingFeature','http://vocabulary.odm2.org/methodtype/specimenPreparation');
INSERT INTO "CV_MethodType" VALUES('cruise','Cruise','A method for performing a cruise action.','FieldActivity','http://vocabulary.odm2.org/methodtype/cruise');
INSERT INTO "CV_MethodType" VALUES('specimenFractionation','Specimen fractionation','A method for separating a specimen into multiple different fractions or size classes.','SamplingFeature','http://vocabulary.odm2.org/methodtype/specimenFractionation');
INSERT INTO "CV_MethodType" VALUES('specimenPreservation','Specimen preservation','A method for preserving a specimen either in the field or in a laboratory prior to ex situ analysis.','SamplingFeature','http://vocabulary.odm2.org/methodtype/specimenPreservation');
INSERT INTO "CV_MethodType" VALUES('genericNonObservation','Generic non-observation','A method for completing a non-specific action that does not produce a result.','Other','http://vocabulary.odm2.org/methodtype/genericNonObservation');
INSERT INTO "CV_MethodType" VALUES('derivation','Derivation','A method for creating results by deriving them from other results.','Observation','http://vocabulary.odm2.org/methodtype/derivation');
INSERT INTO "CV_MethodType" VALUES('instrumentCalibration','Instrument calibration','A method for calibrating an instrument either in the field or in the laboratory. ','Equipment','http://vocabulary.odm2.org/methodtype/instrumentCalibration');
INSERT INTO "CV_MethodType" VALUES('instrumentRetrieval','Instrument retrieval','A method for retrieving or recovering an instrument that has been deployed at a smpling feature.','Equipment','http://vocabulary.odm2.org/methodtype/instrumentRetrieval');
INSERT INTO "CV_MethodType" VALUES('observation','Observation','A method for creating observation results. This term should be used when a Result is generated but the more specific terms of Instrument deployment or Specimen analysis are not applicable.','Observation','http://vocabulary.odm2.org/methodtype/observation');
INSERT INTO "CV_MethodType" VALUES('instrumentDeployment','Instrument deployment','A method for deploying an instrument to make observations at a sampling feature.','Observation','http://vocabulary.odm2.org/methodtype/instrumentDeployment');
INSERT INTO "CV_MethodType" VALUES('specimenCollection','Specimen collection','A method for collecting a specimen for ex situ analysis.','SamplingFeature','http://vocabulary.odm2.org/methodtype/specimenCollection');
INSERT INTO "CV_MethodType" VALUES('simulation','Simulation','A method for creating results by running a simulation model.','Observation','http://vocabulary.odm2.org/methodtype/simulation');
INSERT INTO "CV_MethodType" VALUES('specimenAnalysis','Specimen analysis','A method for ex situ analysis of a specimen using an instrument, typically in a laboratory, for the purpose of measuring properties of a specimen.','Observation','http://vocabulary.odm2.org/methodtype/specimenAnalysis');
INSERT INTO "CV_MethodType" VALUES('siteVisit','Site visit','A method for performing a site visit action.','FieldActivity','http://vocabulary.odm2.org/methodtype/siteVisit');
INSERT INTO "CV_MethodType" VALUES('submersibleLaunch','Submersible launch','A method for launching a submersible from a vessel or ship.','FieldActivity','http://vocabulary.odm2.org/methodtype/submersibleLaunch');
INSERT INTO "CV_MethodType" VALUES('estimation','Estimation','A method for creating results by estimation or professional judgement.','Observation','http://vocabulary.odm2.org/methodtype/estimation');
INSERT INTO "CV_MethodType" VALUES('fieldActivity','Field activity','A method for performing an activity in the field at or on a sampling feature.','FieldActivity','http://vocabulary.odm2.org/methodtype/fieldActivity');
INSERT INTO "CV_MethodType" VALUES('dataRetrieval','Data retrieval','A method for retrieving data from a datalogger deployed at a monitoring site.','Equipment','http://vocabulary.odm2.org/methodtype/dataRetrieval');
INSERT INTO "CV_MethodType" VALUES('equipmentRetrieval','Equipment retrieval','A method for retrieving equipment from a sampling feature at which or on which it was deployed.','Equipment','http://vocabulary.odm2.org/methodtype/equipmentRetrieval');
INSERT INTO "CV_MethodType" VALUES('expedition','Expedition','A method for performing an expedition action.','FieldActivity','http://vocabulary.odm2.org/methodtype/expedition');
INSERT INTO "CV_MethodType" VALUES('equipmentProgramming','Equipment programming','A method for creating or modifying the data collection program running on a datalogger or other equipment deployed at a monitoring site. ',NULL,'http://vocabulary.odm2.org/methodtype/equipmentProgramming');
INSERT INTO "CV_MethodType" VALUES('equipmentDeployment','Equipment deployment','A method for deploying a piece of equipment that will not make observations at a sampling feature.','Observation','http://vocabulary.odm2.org/methodtype/equipmentDeployment');
INSERT INTO "CV_MethodType" VALUES('equipmentMaintenance','Equipment maintenance','A method for performing periodic upkeep or servicing of field or laboratory equipment. Maintenance may be performed in the field, in a laboratory, or at a factory maintenance center.','Equipment','http://vocabulary.odm2.org/methodtype/equipmentMaintenance');
CREATE TABLE CV_OrganizationType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_OrganizationType" VALUES('college','College','An institution of higher education.',NULL,'http://vocabulary.odm2.org/organizationtype/college');
INSERT INTO "CV_OrganizationType" VALUES('researchOrganization','Research organization','A group of cooperating researchers.',NULL,'http://vocabulary.odm2.org/organizationtype/researchOrganization');
INSERT INTO "CV_OrganizationType" VALUES('museum','Museum','A building or institution dedicated to the acquisition, conservation, study, exhibition, and educational interpretation of objects having scientific, historical, cultural, or artistic value.',NULL,'http://vocabulary.odm2.org/organizationtype/museum');
INSERT INTO "CV_OrganizationType" VALUES('school','School','An educational institution providing primary or secondary education.',NULL,'http://vocabulary.odm2.org/organizationtype/school');
INSERT INTO "CV_OrganizationType" VALUES('department','Department','A subdivision or unit within a university, institution, or agency.',NULL,'http://vocabulary.odm2.org/organizationtype/department');
INSERT INTO "CV_OrganizationType" VALUES('program','Program','A set of structured activities.',NULL,'http://vocabulary.odm2.org/organizationtype/program');
INSERT INTO "CV_OrganizationType" VALUES('university','University','An institution of higher education.',NULL,'http://vocabulary.odm2.org/organizationtype/university');
CREATE TABLE CV_PropertyDataType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_PropertyDataType" VALUES('string','String','An array of characters including letters, digits, punctuation marks, symbols, etc.',NULL,'http://vocabulary.odm2.org/propertydatatype/string');
INSERT INTO "CV_PropertyDataType" VALUES('integer','Integer','An integer data type can hold a whole number, but no fraction. Integers may be either signed (allowing negative values) or unsigned (nonnegative values only). ',NULL,'http://vocabulary.odm2.org/propertydatatype/integer');
INSERT INTO "CV_PropertyDataType" VALUES('floatingPointNumber','Floading point number','A floating-point number represents a limited-precision rational number that may have a fractional part. ',NULL,'http://vocabulary.odm2.org/propertydatatype/floatingPointNumber');
INSERT INTO "CV_PropertyDataType" VALUES('boolean','Boolean','A boolean type is typically a logical type that can be either "true" or "false".',NULL,'http://vocabulary.odm2.org/propertydatatype/boolean');
CREATE TABLE CV_QualityCode (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_QualityCode" VALUES('marginal','Marginal','A quality assessment has been made and one or more data quality objectives has not been met. The observation may be suspect and has been assessed to be of marginal quality.',NULL,'http://vocabulary.odm2.org/qualitycode/marginal');
INSERT INTO "CV_QualityCode" VALUES('bad','Bad','A quality assessment has been made and enough of the data quality objectives have not been met that the observation has been assessed to be of bad quality.',NULL,'http://vocabulary.odm2.org/qualitycode/bad');
INSERT INTO "CV_QualityCode" VALUES('none','None','No data quality assessment has been made.',NULL,'http://vocabulary.odm2.org/qualitycode/none');
INSERT INTO "CV_QualityCode" VALUES('good','Good','A quality assessment has been made and all data quality objectives have been met.',NULL,'http://vocabulary.odm2.org/qualitycode/good');
CREATE TABLE CV_ReferenceMaterialMedium (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_RelationshipType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_RelationshipType" VALUES('documents','Documents','Use to indicate the relation to the work which is documentation.',NULL,'http://vocabulary.odm2.org/relationshiptype/documents');
INSERT INTO "CV_RelationshipType" VALUES('isAttachedTo','Is attached to','Used to indicate that one entity is attached to another. For example this term can be used to express the fact that a piece of equipment is attached to a related piece of equipment.',NULL,'http://vocabulary.odm2.org/relationshiptype/isAttachedTo');
INSERT INTO "CV_RelationshipType" VALUES('isChildOf','Is child of','Used to indicate that one entity is an immediate child of another entity. For example, this term can be used to express the fact that an instrument deployment Action is the child of a site visit Action.',NULL,'http://vocabulary.odm2.org/relationshiptype/isChildOf');
CREATE TABLE CV_ResultType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_ResultType" VALUES('truthObservation','Truth observation','A single ResultValue for a single Variable, measured on or at a single SamplingFeature, using a single Method.','Measurement','http://vocabulary.odm2.org/resulttype/truthObservation');
INSERT INTO "CV_ResultType" VALUES('pointCoverage','Point coverage','A series of ResultValues for a single Variable, measured on or at a single SamplingFeature, using a single Method, with specific Units, having a specific ProcessingLevel, with a fixed ValueDateTime, but measured over varying X,Y locations, where X and Y are horizontal coordinates.','Coverage','http://vocabulary.odm2.org/resulttype/pointCoverage');
INSERT INTO "CV_ResultType" VALUES('sectionCoverage','Section coverage','A series of ResultValues for a single Variable, measured on or at a single SamplingFeature, using a single Method, with specific Units, having a specific ProcessingLevel, but measured over varying X (horizontal) and Z (depth) coordinates. ValueDateTime may be fixed or controlled.','Coverage','http://vocabulary.odm2.org/resulttype/sectionCoverage');
INSERT INTO "CV_ResultType" VALUES('transectCoverage','Transect coverage','A series of ResultValues for a single Variable, measured on or at a single SamplingFeature, using a single Method, with specific Units, having a specific ProcessingLevel, but measured over multiple locations along a transect having varying location dimensions (e.g.,  X and/or Y, where X and Y are horizontal coordintes). ValueDateTime may be fixed or controlled.','Coverage','http://vocabulary.odm2.org/resulttype/transectCoverage');
INSERT INTO "CV_ResultType" VALUES('spectraCoverage','Spectra coverage','A series of ResultValues for a single Variable, measured on or at a single SamplingFeature, using a single Method, with specific Units, having a specific ProcessingLevel, but measured over multiple wavelengths of light. ValueDateTime may be fixed or controlled.','Coverage','http://vocabulary.odm2.org/resulttype/spectraCoverage');
INSERT INTO "CV_ResultType" VALUES('profileCoverage','Profile coverage','A series of ResultValues for a single Variable, measured on or at a single SamplingFeature, using a single Method, with specific Units, having a specific ProcessingLevel, but measured over multiple locations along a depth profile with only one varying location dimension (e.g., Z, where Z is depth). ValueDateTime may be fixed or controlled.','Coverage','http://vocabulary.odm2.org/resulttype/profileCoverage');
CREATE TABLE CV_SampledMedium (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_SamplingFeatureGeoType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_SamplingFeatureGeoType" VALUES('notApplicable','Not applicable','The sampling feature has no applicable geospatial feature type','Non-spatial','http://vocabulary.odm2.org/samplingfeaturegeotype/notApplicable');
CREATE TABLE CV_SamplingFeatureType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_SamplingFeatureType" VALUES('flightline','Flightline','A path along which an aircraft travels while measuring a phenomena of study.','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/flightline');
INSERT INTO "CV_SamplingFeatureType" VALUES('interval','Interval','A discrete segment along a longer path in which an observation or specimen is collected over the distance between the upper and lower bounds of the interval. A Depth Interval is a sub-type of Interval.','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/interval');
INSERT INTO "CV_SamplingFeatureType" VALUES('quadrat','Quadrat','A small plot used to isolate a standard unit of area for study of the distribution of an item over a large area.','SamplingSurface','http://vocabulary.odm2.org/samplingfeaturetype/quadrat');
INSERT INTO "CV_SamplingFeatureType" VALUES('observationWell','Observation well','A hole or shaft constructed in the earth intended to be used to locate, sample, or develop groundwater, oil, gas, or some other subsurface material. The diameter of a well is typically much smaller than the depth. Wells are also used to artificially recharge groundwater or to pressurize oil and gas production zones. Specific kinds of wells should be specified in the SamplingFeature description. For example, underground waste-disposal wells should be classified as waste injection wells.','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/observationWell');
INSERT INTO "CV_SamplingFeatureType" VALUES('trajectory','Trajectory','The path that a moving object follows through space as a function of time. A trajectory can be described by the geometry of the path or as the position of the object over time. ','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/trajectory');
INSERT INTO "CV_SamplingFeatureType" VALUES('fieldArea','Field area','A location at which field experiments or observations of ambient conditions are conducted. A field area may contain many sites and has a geographical footprint that can be represented by a polygon.','SamplingSurface','http://vocabulary.odm2.org/samplingfeaturetype/fieldArea');
INSERT INTO "CV_SamplingFeatureType" VALUES('soilPitSection','Soil pit section','Two-dimensional vertical face of a soil pit that is described and sampled.','SamplingSurface','http://vocabulary.odm2.org/samplingfeaturetype/soilPitSection');
INSERT INTO "CV_SamplingFeatureType" VALUES('traverse','Traverse','A field control network consisting of survey stations placed along a line or path of travel.','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/traverse');
INSERT INTO "CV_SamplingFeatureType" VALUES('shipsTrack','Ships track','A path along which a ship or vessel travels while measuring a phenomena of study.  Represented as a line connecting the ship''s consecutive positions on the surface of the earth.','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/shipsTrack');
INSERT INTO "CV_SamplingFeatureType" VALUES('specimen','Specimen','A physical sample (object or entity) obtained for observations, typically performed ex situ, often in a laboratory.  ','Specimen','http://vocabulary.odm2.org/samplingfeaturetype/specimen');
INSERT INTO "CV_SamplingFeatureType" VALUES('crossSection','Cross section','The intersection of a body in three-dimensional space with a plane.  Represented as a polygon. ','SamplingSurface','http://vocabulary.odm2.org/samplingfeaturetype/crossSection');
INSERT INTO "CV_SamplingFeatureType" VALUES('depthInterval','Depth interval','A discrete segment along a longer vertical path, such as a borehole, soil profile or other depth profile, in which an observation or specimen is collected over the distance between the upper and lower depth limits of the interval. A Depth Interval is a sub-type of Interval.','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/depthInterval');
INSERT INTO "CV_SamplingFeatureType" VALUES('scene','Scene','A two-dimensional visual extent within a physical environment.','SamplingSurface','http://vocabulary.odm2.org/samplingfeaturetype/scene');
INSERT INTO "CV_SamplingFeatureType" VALUES('weatherStation','Weather station','A facility, either on land or sea, with instruments and equipment for measuring atmospheric conditions to provide information for weather forecasts and to study weather and climate.','SamplingPoint','http://vocabulary.odm2.org/samplingfeaturetype/weatherStation');
INSERT INTO "CV_SamplingFeatureType" VALUES('CTD','CTD','A CTD (Conductivity, Temperature, and Depth) cast is a water column depth profile collected over a specific and relatively short date-time range, that can be considered as a parent specimen.','Specimen','http://vocabulary.odm2.org/samplingfeaturetype/CTD');
INSERT INTO "CV_SamplingFeatureType" VALUES('transect','Transect','A path along which ocurrences of a phenomena of study are counted or measured.','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/transect');
INSERT INTO "CV_SamplingFeatureType" VALUES('borehole','Borehole','A narrow shaft bored into the ground, either vertically or horizontally. A borehole includes the hole cavity and walls surrounding that cavity.  ','SamplingCurve','http://vocabulary.odm2.org/samplingfeaturetype/borehole');
CREATE TABLE CV_SiteType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_SiteType" VALUES('fieldPastureOrchardOrNursery','Field, Pasture, Orchard, or Nursery','A water-using facility characterized by an area where plants are grown for transplanting, for use as stocks for budding and grafting, or for sale. Irrigation water may or may not be applied.','Facility Sites','http://vocabulary.odm2.org/sitetype/fieldPastureOrchardOrNursery');
INSERT INTO "CV_SiteType" VALUES('shore','Shore','The land along the edge of the sea, a lake, or a wide river where the investigator considers the proximity of the water body to be important. Land adjacent to a reservoir, lake, impoundment, or oceanic site type is considered part of the shore when it includes a beach or bank between the high and low water marks.','Land Sites','http://vocabulary.odm2.org/sitetype/shore');
INSERT INTO "CV_SiteType" VALUES('animalWasteLagoon','Animal waste lagoon','A facility for storage and/or biological treatment of wastes from livestock operations. Animal-waste lagoons are earthen structures ranging from pits to large ponds, and contain manure which has been diluted with building washwater, rainfall, and surface runoff. In treatment lagoons, the waste becomes partially liquefied and stabilized by bacterial action before the waste is disposed of on the land and the water is discharged or re-used.','Facility Sites','http://vocabulary.odm2.org/sitetype/animalWasteLagoon');
INSERT INTO "CV_SiteType" VALUES('sinkhole','Sinkhole','A crater formed when the roof of a cavern collapses; usually found in limestone areas. Surface water and precipitation that enters a sinkhole usually evaporates or infiltrates into the ground, rather than draining into a stream.','Land Sites','http://vocabulary.odm2.org/sitetype/sinkhole');
INSERT INTO "CV_SiteType" VALUES('volcanicVent','Volcanic vent','Vent from which volcanic gases escape to the atmosphere. Also known as fumarole.','Geologic Sites','http://vocabulary.odm2.org/sitetype/volcanicVent');
INSERT INTO "CV_SiteType" VALUES('tunnelShaftMine','Tunnel, shaft, or mine','A constructed subsurface open space large enough to accommodate a human that is not substantially open to the atmosphere and is not a well. The excavation may have been for minerals, transportation, or other purposes. See also: Excavation.','Groundwater Sites','http://vocabulary.odm2.org/sitetype/tunnelShaftMine');
INSERT INTO "CV_SiteType" VALUES('outfall','Outfall','A site where water or wastewater is returned to a surface-water body, e.g. the point where wastewater is returned to a stream. Typically, the discharge end of an effluent pipe.','Facility Sites','http://vocabulary.odm2.org/sitetype/outfall');
INSERT INTO "CV_SiteType" VALUES('wastewaterTreatmentPlant','Wastewater-treatment plant','A facility where wastewater is treated to reduce concentrations of dissolved and (or) suspended materials prior to discharge or reuse.','Facility Sites','http://vocabulary.odm2.org/sitetype/wastewaterTreatmentPlant');
INSERT INTO "CV_SiteType" VALUES('subsurface','Subsurface','A location below the land surface, but not a well, soil hole, or excavation.','Groundwater Sites','http://vocabulary.odm2.org/sitetype/subsurface');
INSERT INTO "CV_SiteType" VALUES('combinedSewer','Combined sewer','An underground conduit created to convey storm drainage and waste products into a wastewater-treatment plant, stream, reservoir, or disposal site.','Water Infrastructure Sites','http://vocabulary.odm2.org/sitetype/combinedSewer');
INSERT INTO "CV_SiteType" VALUES('wastewaterLandApplication','Wastewater land application','A site where the disposal of waste water on land occurs. Use "waste-injection well" for underground waste-disposal sites.','Land Sites','http://vocabulary.odm2.org/sitetype/wastewaterLandApplication');
INSERT INTO "CV_SiteType" VALUES('landfill','Landfill','A typically dry location on the surface of the land where primarily solid waste products are currently, or previously have been, aggregated and sometimes covered with a veneer of soil. See also: Wastewater disposal and waste-injection well.','Facility Sites','http://vocabulary.odm2.org/sitetype/landfill');
INSERT INTO "CV_SiteType" VALUES('lakeReservoirImpoundment','Lake, Reservoir, Impoundment','An inland body of standing fresh or saline water that is generally too deep to permit submerged aquatic vegetation to take root across the entire body (cf: wetland). This site type includes an expanded part of a river, a reservoir behind a dam, and a natural or excavated depression containing a water body without surface-water inlet and/or outlet.','Surface Water Sites','http://vocabulary.odm2.org/sitetype/lakeReservoirImpoundment');
INSERT INTO "CV_SiteType" VALUES('outcrop','Outcrop','The part of a rock formation that appears at the surface of the surrounding land.','Land Sites','http://vocabulary.odm2.org/sitetype/outcrop');
INSERT INTO "CV_SiteType" VALUES('stormSewer','Storm sewer','An underground conduit created to convey storm drainage into a stream channel or reservoir. If the sewer also conveys liquid waste products, then the "combined sewer" secondary site type should be used.','Water Infrastructure Sites','http://vocabulary.odm2.org/sitetype/stormSewer');
INSERT INTO "CV_SiteType" VALUES('ocean','Ocean','Site in the open ocean, gulf, or sea. (See also: Coastal, Estuary, and Tidal stream).','Surface Water Sites','http://vocabulary.odm2.org/sitetype/ocean');
INSERT INTO "CV_SiteType" VALUES('hydroelectricPlant','Hydroelectric plant','A facility that generates electric power by converting potential energy of water into kinetic energy. Typically, turbine generators are turned by falling water.','Facility Sites','http://vocabulary.odm2.org/sitetype/hydroelectricPlant');
INSERT INTO "CV_SiteType" VALUES('spring','Spring','A location at which the water table intersects the land surface, resulting in a natural flow of groundwater to the surface. Springs may be perennial, intermittent, or ephemeral.','Spring Sites','http://vocabulary.odm2.org/sitetype/spring');
INSERT INTO "CV_SiteType" VALUES('coastal','Coastal','An oceanic site that is located off-shore beyond the tidal mixing zone (estuary) but close enough to the shore that the investigator considers the presence of the coast to be important. Coastal sites typically are within three nautical miles of the shore.','Surface Water Sites','http://vocabulary.odm2.org/sitetype/coastal');
INSERT INTO "CV_SiteType" VALUES('glacier','Glacier','Body of land ice that consists of recrystallized snow accumulated on the surface of the ground and moves slowly downslope (WSP-1541A) over a period of years or centuries. Since glacial sites move, the lat-long precision for these sites is usually coarse.','Glacier Sites','http://vocabulary.odm2.org/sitetype/glacier');
INSERT INTO "CV_SiteType" VALUES('stream','Stream','A body of running water moving under gravity flow in a defined channel. The channel may be entirely natural, or altered by engineering practices through straightening, dredging, and (or) lining. An entirely artificial channel should be qualified with the "canal" or "ditch" secondary site type.','Surface Water Sites','http://vocabulary.odm2.org/sitetype/stream');
INSERT INTO "CV_SiteType" VALUES('waterDistributionSystem','Water-distribution system','A site located somewhere on a networked infrastructure that distributes treated or untreated water to multiple domestic, industrial, institutional, and (or) commercial users. May be owned by a municipality or community, a water district, or a private concern.','Water Infrastructure Sites','http://vocabulary.odm2.org/sitetype/waterDistributionSystem');
INSERT INTO "CV_SiteType" VALUES('thermoelectricPlant','Thermoelectric plant','A facility that uses water in the generation of electricity from heat. Typically turbine generators are driven by steam. The heat may be caused by various means, including combustion, nuclear reactions, and geothermal processes.','Facility Sites','http://vocabulary.odm2.org/sitetype/thermoelectricPlant');
INSERT INTO "CV_SiteType" VALUES('aggregateSurfaceWaterUse','Aggregate surface-water-use','An Aggregate Surface-Water Diversion/Return site represents an aggregate of specific sites where surface water is diverted or returned which is defined by a geographic area or some other common characteristic. An aggregate surface-water site type is used when it is not possible or practical to describe the specific sites as diversions, outfalls, or land application sites, or when water-use information is only available for the aggregate. ','Aggregated Use Sites','http://vocabulary.odm2.org/sitetype/aggregateSurfaceWaterUse');
INSERT INTO "CV_SiteType" VALUES('aggregateGroundwaterUse','Aggregate groundwater use','An Aggregate Groundwater Withdrawal/Return site represents an aggregate of specific sites where groundwater is withdrawn or returned which is defined by a geographic area or some other common characteristic. An aggregate groundwater site type is used when it is not possible or practical to describe the specific sites as springs or as any type of well including ''multiple wells'', or when water-use information is only available for the aggregate. ','Aggregated Use Sites','http://vocabulary.odm2.org/sitetype/aggregateGroundwaterUse');
INSERT INTO "CV_SiteType" VALUES('wastewaterSewer','Wastewater sewer','An underground conduit created to convey liquid and semisolid domestic, commercial, or industrial waste into a treatment plant, stream, reservoir, or disposal site. If the sewer also conveys storm water, then the "combined sewer" secondary site type should be used.','Water Infrastructure Sites','http://vocabulary.odm2.org/sitetype/wastewaterSewer');
INSERT INTO "CV_SiteType" VALUES('wetland','Wetland','Land where saturation with water is the dominant factor determining the nature of soil development and the types of plant and animal communities living in the soil and on its surface (Cowardin, December 1979). Wetlands are found from the tundra to the tropics and on every continent except Antarctica. Wetlands are areas that are inundated or saturated by surface or groundwater at a frequency and duration sufficient to support, and that under normal circumstances do support, a prevalence of vegetation typically adapted for life in saturated soil conditions. Wetlands generally include swamps, marshes, bogs and similar areas. Wetlands may be forested or unforested, and naturally or artificially created.','Surface Water Sites','http://vocabulary.odm2.org/sitetype/wetland');
INSERT INTO "CV_SiteType" VALUES('aggregateWaterUseEstablishment','Aggregate water-use establishment','An Aggregate Water-Use Establishment represents an aggregate class of water-using establishments or individuals that are associated with a specific geographic location and water-use category, such as all the industrial users located within a county or all self-supplied domestic users in a county. An aggregate water-use establishment site type is used when specific information needed to create sites for the individual facilities or users is not available or when it is not desirable to store the site-specific information in the database. ','Aggregated Use Sites','http://vocabulary.odm2.org/sitetype/aggregateWaterUseEstablishment');
INSERT INTO "CV_SiteType" VALUES('unsaturatedZone','Unsaturated zone','A site equipped to measure conditions in the subsurface deeper than a soil hole, but above the water table or other zone of saturation.','Groundwater Sites','http://vocabulary.odm2.org/sitetype/unsaturatedZone');
INSERT INTO "CV_SiteType" VALUES('cistern','Cistern','An artificial, non-pressurized reservoir filled by gravity flow and used for water storage. The reservoir may be located above, at, or below ground level. The water may be supplied from diversion of precipitation, surface, or groundwater sources.','Water Infrastructure Sites','http://vocabulary.odm2.org/sitetype/cistern');
INSERT INTO "CV_SiteType" VALUES('cave','Cave','A natural open space within a rock formation large enough to accommodate a human. A cave may have an opening to the outside, is always underground, and sometimes submerged. Caves commonly occur by the dissolution of soluble rocks, generally limestone, but may also be created within the voids of large-rock aggregations, in openings along seismic faults, and in lava formations.','Groundwater Sites','http://vocabulary.odm2.org/sitetype/cave');
INSERT INTO "CV_SiteType" VALUES('estuary','Estuary','A coastal inlet of the sea or ocean; esp. the mouth of a river, where tide water normally mixes with stream water (modified, Webster). Salinity in estuaries typically ranges from 1 to 25 Practical Salinity Units (psu), as compared oceanic values around 35-psu. See also: tidal stream and coastal.','Surface Water Sites','http://vocabulary.odm2.org/sitetype/estuary');
INSERT INTO "CV_SiteType" VALUES('waterSupplyTreatmentPlant','Water-supply treatment plant','A facility where water is treated prior to use for consumption or other purpose.','Facility Sites','http://vocabulary.odm2.org/sitetype/waterSupplyTreatmentPlant');
INSERT INTO "CV_SiteType" VALUES('septicSystem','Septic system','A site within or in close proximity to a subsurface sewage disposal system that generally consists of: (1) a septic tank where settling of solid material occurs, (2) a distribution system that transfers fluid from the tank to (3) a leaching system that disperses the effluent into the ground.','Water Infrastructure Sites','http://vocabulary.odm2.org/sitetype/septicSystem');
INSERT INTO "CV_SiteType" VALUES('soilHole','Soil hole','A small excavation into soil at the top few meters of earth surface. Soil generally includes some organic matter derived from plants. Soil holes are created to measure soil composition and properties. Sometimes electronic probes are inserted into soil holes to measure physical properties, and (or) the extracted soil is analyzed.','Land Sites','http://vocabulary.odm2.org/sitetype/soilHole');
INSERT INTO "CV_SiteType" VALUES('laboratoryOrSamplePreparationArea','Laboratory or sample-preparation area','A site where some types of quality-control samples are collected, and where equipment and supplies for environmental sampling are prepared. Equipment blank samples are commonly collected at this site type, as are samples of locally produced deionized water. This site type is typically used when the data are either not associated with a unique environmental data-collection site, or where blank water supplies are designated by Center offices with unique station IDs.','Facility Sites','http://vocabulary.odm2.org/sitetype/laboratoryOrSamplePreparationArea');
INSERT INTO "CV_SiteType" VALUES('groundwaterDrain','Groundwater drain','An underground pipe or tunnel through which groundwater is artificially diverted to surface water for the purpose of reducing erosion or lowering the water table. A drain is typically open to the atmosphere at the lowest elevation, in contrast to a well which is open at the highest point.','Groundwater Sites','http://vocabulary.odm2.org/sitetype/groundwaterDrain');
INSERT INTO "CV_SiteType" VALUES('tidalStream','Tidal stream','A stream reach where the flow is influenced by the tide, but where the water chemistry is not normally influenced. A site where ocean water typically mixes with stream water should be coded as an estuary.','Surface Water Sites','http://vocabulary.odm2.org/sitetype/tidalStream');
INSERT INTO "CV_SiteType" VALUES('facility','Facility','A non-ambient location where environmental measurements are expected to be strongly influenced by current or previous activities of humans. *Sites identified with a "facility" primary site type must be further classified with one of the applicable secondary site types.','Facility Sites','http://vocabulary.odm2.org/sitetype/facility');
INSERT INTO "CV_SiteType" VALUES('pavement','Pavement','A surface site where the land surface is covered by a relatively impermeable material, such as concrete or asphalt. Pavement sites are typically part of transportation infrastructure, such as roadways, parking lots, or runways.','Land Sites','http://vocabulary.odm2.org/sitetype/pavement');
INSERT INTO "CV_SiteType" VALUES('ditch','Ditch','An excavation artificially dug in the ground, either lined or unlined, for conveying water for drainage or irrigation; it is smaller than a canal.','Surface Water Sites','http://vocabulary.odm2.org/sitetype/ditch');
INSERT INTO "CV_SiteType" VALUES('composite','Composite','A Composite site represents an aggregation of specific sites defined by a geographic location at which multiple sampling features have been installed. For example, a composite site might consist of a location on a stream where a streamflow gage, weather station, and shallow groundwater well have been installed.','Composite Sites','http://vocabulary.odm2.org/sitetype/composite');
INSERT INTO "CV_SiteType" VALUES('playa','Playa','A dried-up, vegetation-free, flat-floored area composed of thin, evenly stratified sheets of fine clay, silt or sand, and represents the bottom part of a shallow, completely closed or undrained desert lake basin in which water accumulates and is quickly evaporated, usually leaving deposits of soluble salts.','Land Sites','http://vocabulary.odm2.org/sitetype/playa');
INSERT INTO "CV_SiteType" VALUES('land','Land','A location on the surface of the earth that is not normally saturated with water. Land sites are appropriate for sampling vegetation, overland flow of water, or measuring land-surface properties such as temperature. (See also: Wetland).','Land Sites','http://vocabulary.odm2.org/sitetype/land');
INSERT INTO "CV_SiteType" VALUES('unknown','Unknown','Site type is unknown.','Unknown','http://vocabulary.odm2.org/sitetype/unknown');
INSERT INTO "CV_SiteType" VALUES('atmosphere','Atmosphere','A site established primarily to measure meteorological properties or atmospheric deposition.','Atmospheric Sites','http://vocabulary.odm2.org/sitetype/atmosphere');
CREATE TABLE CV_SpatialOffsetType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_SpatialOffsetType" VALUES('depth','Depth','Depth below the earth or water surface. Values are expressed as negative numbers and become more negative in the downward direction.','1D','http://vocabulary.odm2.org/spatialoffsettype/depth');
INSERT INTO "CV_SpatialOffsetType" VALUES('radialHorizontalOffsetWithHeight','Radial horizontal offset with height','Offset expressed as a distance along a ray that originates from a central point with a third coordinate that indicates the height above the earth or water surface. The angle of the ray is expressed as the first offset coordinate in degrees. The distance along the ray is expressed as the second offset coordinate. The height above the earth or water surface is expressed as the third coordinate.','3D','http://vocabulary.odm2.org/spatialoffsettype/radialHorizontalOffsetWithHeight');
INSERT INTO "CV_SpatialOffsetType" VALUES('depthInterval','Depth interval','Depth interval below the earth or water surface. The mininum depth value is expressed first and then maximum depth value. Values are expresssed as negative numbers and become more negative in the downward direction.','2D','http://vocabulary.odm2.org/spatialoffsettype/depthInterval');
INSERT INTO "CV_SpatialOffsetType" VALUES('heightInterval','Height interval','Height interval above the earth or water surface. The minimum height value is expressed first and then the maximum height value. Values increase in the upward direction.','2D','http://vocabulary.odm2.org/spatialoffsettype/heightInterval');
INSERT INTO "CV_SpatialOffsetType" VALUES('depthDirectional','Depth, directional','Depth below the earth or water surface along a non-vertical line. The first coordinate is the angle of the ray from north expressed in degrees. The second coordinate is the angle of the ray from horizontal expressed in negative degrees. The distance along the ray is expressed as a positive number that increases with distance along the ray. ','3D','http://vocabulary.odm2.org/spatialoffsettype/depthDirectional');
INSERT INTO "CV_SpatialOffsetType" VALUES('cartesianOffset','Cartesian offset','Offset expressed using cartesian coordinates where X is distance along axis aligned with true north, Y is distace aligned with true east, and Z is distance aligned straight up. Depths are expressed a negative numbers. The origin of the coordinate system is typically defined in the site description. ','3D','http://vocabulary.odm2.org/spatialoffsettype/cartesianOffset');
INSERT INTO "CV_SpatialOffsetType" VALUES('radialHorizontalOffset','Radial horizontal offset','Offset expressed as a distance along a ray that originates from a central point. The angle of the ray is expressed as the first offset coordinate in degrees. The distance along the ray is expressed as the second offset coordinate.','2D','http://vocabulary.odm2.org/spatialoffsettype/radialHorizontalOffset');
CREATE TABLE CV_Speciation (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_Speciation" VALUES('C6HCl5O','C6HCl5O','Expressed as pentachlorophenol',NULL,'http://vocabulary.odm2.org/speciation/C6HCl5O');
INSERT INTO "CV_Speciation" VALUES('Br','Br','Expressed as bromine',NULL,'http://vocabulary.odm2.org/speciation/Br');
INSERT INTO "CV_Speciation" VALUES('As','As','Expressed as arsenic',NULL,'http://vocabulary.odm2.org/speciation/As');
INSERT INTO "CV_Speciation" VALUES('CHBrCl2','CHBrCl2','Expressed as bromodichloromethane',NULL,'http://vocabulary.odm2.org/speciation/CHBrCl2');
INSERT INTO "CV_Speciation" VALUES('C13H10S','C13H10S','Expressed as methyldibenzothiophene',NULL,'http://vocabulary.odm2.org/speciation/C13H10S');
INSERT INTO "CV_Speciation" VALUES('C12H8','C12H8','Expressed as acenaphthylene',NULL,'http://vocabulary.odm2.org/speciation/C12H8');
INSERT INTO "CV_Speciation" VALUES('C2HCl3','C2HCl3','Expressed as trichloroethylene',NULL,'http://vocabulary.odm2.org/speciation/C2HCl3');
INSERT INTO "CV_Speciation" VALUES('C6H5Cl','C6H5Cl','Expressed as chlorobenzene',NULL,'http://vocabulary.odm2.org/speciation/C6H5Cl');
INSERT INTO "CV_Speciation" VALUES('Re','Re','Expressed as rhenium',NULL,'http://vocabulary.odm2.org/speciation/Re');
INSERT INTO "CV_Speciation" VALUES('C14H12','C14H12','Expressed as methylfluorene',NULL,'http://vocabulary.odm2.org/speciation/C14H12');
INSERT INTO "CV_Speciation" VALUES('C8H10','C8H10','Expressed as ethylbenzene',NULL,'http://vocabulary.odm2.org/speciation/C8H10');
INSERT INTO "CV_Speciation" VALUES('H2O','H2O','Expressed as water',NULL,'http://vocabulary.odm2.org/speciation/H2O');
INSERT INTO "CV_Speciation" VALUES('Mo','Mo','Expressed as molybdenum',NULL,'http://vocabulary.odm2.org/speciation/Mo');
INSERT INTO "CV_Speciation" VALUES('C18H12','C18H12','Expressed as C18H12, e.g., benz(a)anthracene, chrysene, triphenylene',NULL,'http://vocabulary.odm2.org/speciation/C18H12');
INSERT INTO "CV_Speciation" VALUES('C6H5NO2','C6H5NO2','Expressed as nitrobenzene',NULL,'http://vocabulary.odm2.org/speciation/C6H5NO2');
INSERT INTO "CV_Speciation" VALUES('C20H42','C20H42','Expressed as C20 n-alkane',NULL,'http://vocabulary.odm2.org/speciation/C20H42');
INSERT INTO "CV_Speciation" VALUES('C2H3Cl3','C2H3Cl3','Expressed as trichloroethane',NULL,'http://vocabulary.odm2.org/speciation/C2H3Cl3');
INSERT INTO "CV_Speciation" VALUES('PO4','PO4','Expressed as phosphate',NULL,'http://vocabulary.odm2.org/speciation/PO4');
INSERT INTO "CV_Speciation" VALUES('C3H6O','C3H6O','Expressed as acetone',NULL,'http://vocabulary.odm2.org/speciation/C3H6O');
INSERT INTO "CV_Speciation" VALUES('C4H8Cl2O','C4H8Cl2O','Expressed as bis(chloroethyl) ether',NULL,'http://vocabulary.odm2.org/speciation/C4H8Cl2O');
INSERT INTO "CV_Speciation" VALUES('TA','TA','Expressed as total alkalinity',NULL,'http://vocabulary.odm2.org/speciation/TA');
INSERT INTO "CV_Speciation" VALUES('C24H50','C24H50','Expressed as C24 n-alkane',NULL,'http://vocabulary.odm2.org/speciation/C24H50');
INSERT INTO "CV_Speciation" VALUES('C6H4N2O5','C6H4N2O5','Expressed as dinitrophenol',NULL,'http://vocabulary.odm2.org/speciation/C6H4N2O5');
INSERT INTO "CV_Speciation" VALUES('C4H8O','C4H8O','Expressed as butanone',NULL,'http://vocabulary.odm2.org/speciation/C4H8O');
INSERT INTO "CV_Speciation" VALUES('C6H5NH2','C6H5NH2','Expressed as aniline',NULL,'http://vocabulary.odm2.org/speciation/C6H5NH2');
INSERT INTO "CV_Speciation" VALUES('C2Cl4','C2Cl4','Expressed as tetrachloroethylene',NULL,'http://vocabulary.odm2.org/speciation/C2Cl4');
INSERT INTO "CV_Speciation" VALUES('C20H12','C20H12','Expressed as C20H12, e.g., benzo(b)fluoranthene, benzo(e)pyrene, perylene',NULL,'http://vocabulary.odm2.org/speciation/C20H12');
INSERT INTO "CV_Speciation" VALUES('deltaN15','delta N15','Expressed as nitrogen-15',NULL,'http://vocabulary.odm2.org/speciation/deltaN15');
INSERT INTO "CV_Speciation" VALUES('C22H14','C22H14','Expressed as Dibenz(a,h)anthracene',NULL,'http://vocabulary.odm2.org/speciation/C22H14');
INSERT INTO "CV_Speciation" VALUES('NH4','NH4','Expressed as ammonium',NULL,'http://vocabulary.odm2.org/speciation/NH4');
INSERT INTO "CV_Speciation" VALUES('C2H6','C2H6','Expressed as ethane',NULL,'http://vocabulary.odm2.org/speciation/C2H6');
INSERT INTO "CV_Speciation" VALUES('C16H10','C16H10','Expressed as C16H10, e.g., fluoranthene, pyrene',NULL,'http://vocabulary.odm2.org/speciation/C16H10');
INSERT INTO "CV_Speciation" VALUES('C15H12','C15H12','Expressed as C15H12, e.g., methylphenanthrene, Methylanthracene',NULL,'http://vocabulary.odm2.org/speciation/C15H12');
INSERT INTO "CV_Speciation" VALUES('C12H8S','C12H8S','Expressed as dibenzothiophene',NULL,'http://vocabulary.odm2.org/speciation/C12H8S');
INSERT INTO "CV_Speciation" VALUES('C6H5OH','C6H5OH','Expressed as phenol',NULL,'http://vocabulary.odm2.org/speciation/C6H5OH');
INSERT INTO "CV_Speciation" VALUES('Th','Th','Expressed as thorium',NULL,'http://vocabulary.odm2.org/speciation/Th');
INSERT INTO "CV_Speciation" VALUES('Pb','Pb','Expressed as lead',NULL,'http://vocabulary.odm2.org/speciation/Pb');
INSERT INTO "CV_Speciation" VALUES('C13H10','C13H10','Expressed as fluorene',NULL,'http://vocabulary.odm2.org/speciation/C13H10');
INSERT INTO "CV_Speciation" VALUES('O2','O2','Expressed as oxygen (O2)',NULL,'http://vocabulary.odm2.org/speciation/O2');
INSERT INTO "CV_Speciation" VALUES('C26H54','C26H54','Expressed as C26 n-alkane',NULL,'http://vocabulary.odm2.org/speciation/C26H54');
INSERT INTO "CV_Speciation" VALUES('C18H18','C18H18','Expressed as retene',NULL,'http://vocabulary.odm2.org/speciation/C18H18');
INSERT INTO "CV_Speciation" VALUES('C12H9N','C12H9N','Expressed as carbazole',NULL,'http://vocabulary.odm2.org/speciation/C12H9N');
INSERT INTO "CV_Speciation" VALUES('C4Cl6','C4Cl6','Expressed as hexchlorobutadiene',NULL,'http://vocabulary.odm2.org/speciation/C4Cl6');
INSERT INTO "CV_Speciation" VALUES('C31H64','C31H64','Expressed as C31 n-alkane',NULL,'http://vocabulary.odm2.org/speciation/C31H64');
INSERT INTO "CV_Speciation" VALUES('Tl','Tl','Expressed as thallium',NULL,'http://vocabulary.odm2.org/speciation/Tl');
INSERT INTO "CV_Speciation" VALUES('C12H8O','C12H8O','Expressed as dibenzofuran',NULL,'http://vocabulary.odm2.org/speciation/C12H8O');
INSERT INTO "CV_Speciation" VALUES('C15H32','C15H32','Expressed as C15 n-alkane',NULL,'http://vocabulary.odm2.org/speciation/C15H32');
INSERT INTO "CV_Speciation" VALUES('C2H3Cl','C2H3Cl','Expressed as vinyl chloride',NULL,'http://vocabulary.odm2.org/speciation/C2H3Cl');
INSERT INTO "CV_Speciation" VALUES('C18H38','C18H38','Expressed as C18 n-alkane',NULL,'http://vocabulary.odm2.org/speciation/C18H38');
INSERT INTO "CV_Speciation" VALUES('C19H14','C19H14','Expressed as methylchrysene',NULL,'http://vocabulary.odm2.org/speciation/C19H14');
INSERT INTO "CV_Speciation" VALUES('C2H6O2','C2H6O2','Expressed as Ethylene glycol',NULL,'http://vocabulary.odm2.org/speciation/C2H6O2');
INSERT INTO "CV_Speciation" VALUES('C10H5_CH3_3','C10H5(CH3)3','Expressed as trimethylnaphthalene',NULL,'http://vocabulary.odm2.org/speciation/C10H5_CH3_3');
INSERT INTO "CV_Speciation" VALUES('CH2Cl2','CH2Cl2','Expressed as dichloromethane',NULL,'http://vocabulary.odm2.org/speciation/CH2Cl2');
INSERT INTO "CV_Speciation" VALUES('C2H4Cl2','C2H4Cl2','Expressed as dichloroethane',NULL,'http://vocabulary.odm2.org/speciation/C2H4Cl2');
INSERT INTO "CV_Speciation" VALUES('Ba','Ba','Expressed as barium',NULL,'http://vocabulary.odm2.org/speciation/Ba');
INSERT INTO "CV_Speciation" VALUES('delta2H','delta 2H','Expressed as deuterium',NULL,'http://vocabulary.odm2.org/speciation/delta2H');
CREATE TABLE CV_SpecimenMedium (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_SpecimenType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_SpecimenType" VALUES('theSpecimenTypeIsUnknown','The specimen type is unknown','The specimen type is unknown',NULL,'http://vocabulary.odm2.org/specimentype/theSpecimenTypeIsUnknown');
INSERT INTO "CV_SpecimenType" VALUES('coreQuarterRound','Core quarter round','Quarter-cylindrical products of along-axis split of a half round.',NULL,'http://vocabulary.odm2.org/specimentype/coreQuarterRound');
INSERT INTO "CV_SpecimenType" VALUES('individualSample','Individual sample','A sample that is an individual unit, including rock hand samples, a biological specimen, or a bottle of fluid.',NULL,'http://vocabulary.odm2.org/specimentype/individualSample');
INSERT INTO "CV_SpecimenType" VALUES('forestFloorDigestion','Forest floor digestion','Sample that consists of a digestion of forest floor material',NULL,'http://vocabulary.odm2.org/specimentype/forestFloorDigestion');
INSERT INTO "CV_SpecimenType" VALUES('terrestrialSection','Terrestrial section','A sample of a section of the near-surface Earth, generally in the critical zone.',NULL,'http://vocabulary.odm2.org/specimentype/terrestrialSection');
INSERT INTO "CV_SpecimenType" VALUES('precipitationBulk','Precipitation bulk','Sample from bulk precipitation',NULL,'http://vocabulary.odm2.org/specimentype/precipitationBulk');
INSERT INTO "CV_SpecimenType" VALUES('corePiece','Core piece','Material occurring between unambiguous [as curated] breaks in recovery.',NULL,'http://vocabulary.odm2.org/specimentype/corePiece');
INSERT INTO "CV_SpecimenType" VALUES('automated','Automated','Sample collected using an automated sampler.',NULL,'http://vocabulary.odm2.org/specimentype/automated');
INSERT INTO "CV_SpecimenType" VALUES('coreSub-Piece','Core sub-piece','Unambiguously mated portion of a larger piece noted for curatorial management of the material.',NULL,'http://vocabulary.odm2.org/specimentype/coreSub-Piece');
INSERT INTO "CV_SpecimenType" VALUES('litterFallDigestion','Litter fall digestion','Sample that consists of a digestion of litter fall',NULL,'http://vocabulary.odm2.org/specimentype/litterFallDigestion');
CREATE TABLE CV_Status (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_TaxonomicClassifierType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_TaxonomicClassifierType" VALUES('chemistry','Chemistry','A taxonomy containing terms associated with chemistry, chemical analysis or processes.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/chemistry');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('soilTexture','Soil texture','A taxonomy containing terms describing soil texture.','Soil','http://vocabulary.odm2.org/taxonomicclassifiertype/soilTexture');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('waterQuality','Water quality','A taxonomy containing terms associated with water quality variables or processes.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/waterQuality');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('biology','Biology','A taxonomy containing terms associated with biological organisms.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/biology');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('instrumentation','Instrumentation','A taxonomy containing terms associated with instrumentation and instrument properties such as battery voltages, data logger temperatures, often useful for diagnosis.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/instrumentation');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('climate','Climate','A taxonomy containing terms associated with the climate, weather, or atmospheric processes.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/climate');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('geology','Geology','A taxonomy containing terms associated with geology or geological processes.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/geology');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('soilStructure','Soil structure','A taxonomy containing terms describing soil structure.','Soil','http://vocabulary.odm2.org/taxonomicclassifiertype/soilStructure');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('rock','Rock','A taxonomy containing terms describing rocks.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/rock');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('lithology','Lithology','A taxonomy containing terms associated with lithology.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/lithology');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('soilColor','Soil color','A taxonomy containing terms describing soil color.','Soil','http://vocabulary.odm2.org/taxonomicclassifiertype/soilColor');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('hydrology','Hydrology','A taxonomy containing terms associated with hydrologic variables or processes.',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/hydrology');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('soil','Soil','A taxonomy containing terms associated with soil variables or processes',NULL,'http://vocabulary.odm2.org/taxonomicclassifiertype/soil');
INSERT INTO "CV_TaxonomicClassifierType" VALUES('soilHorizon','Soil horizon','A taxonomy containing terms describing soil horizons.','Soil','http://vocabulary.odm2.org/taxonomicclassifiertype/soilHorizon');
CREATE TABLE CV_UnitsType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_VariableName (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_VariableName" VALUES('biphenyl','Biphenyl','Biphenyl ((C6H5)2), a polycyclic aromatic hydrocarbon (PAH), also known as diphenyl or phenylbenzene or 1,1''-biphenyl or lemonene',NULL,'http://vocabulary.odm2.org/variablename/biphenyl');
INSERT INTO "CV_VariableName" VALUES('carbonDissolvedOrganic','Carbon, dissolved organic','Dissolved Organic Carbon',NULL,'http://vocabulary.odm2.org/variablename/carbonDissolvedOrganic');
INSERT INTO "CV_VariableName" VALUES('nitrogenDissolvedKjeldahl','Nitrogen, dissolved Kjeldahl','Dissolved Kjeldahl (organic nitrogen + ammonia (NH3) + ammonium (NH4))nitrogen',NULL,'http://vocabulary.odm2.org/variablename/nitrogenDissolvedKjeldahl');
INSERT INTO "CV_VariableName" VALUES('dieldrin','Dieldrin','Dieldrin (C12H8Cl6O)',NULL,'http://vocabulary.odm2.org/variablename/dieldrin');
INSERT INTO "CV_VariableName" VALUES('area','Area','Area of a measurement location',NULL,'http://vocabulary.odm2.org/variablename/area');
INSERT INTO "CV_VariableName" VALUES('tideStage','Tide stage','Tidal stage',NULL,'http://vocabulary.odm2.org/variablename/tideStage');
INSERT INTO "CV_VariableName" VALUES('chrysene','Chrysene','Chrysene (C18H12), a polycyclic aromatic hydrocarbon (PAH)',NULL,'http://vocabulary.odm2.org/variablename/chrysene');
INSERT INTO "CV_VariableName" VALUES('nitrogenTotalOrganic','Nitrogen, total organic','Total (dissolved + particulate) organic nitrogen',NULL,'http://vocabulary.odm2.org/variablename/nitrogenTotalOrganic');
INSERT INTO "CV_VariableName" VALUES('4_4_Methylenebis_N_N_Dimethylaniline','4,4-Methylenebis(N,N-dimethylaniline)','4,4''-Methylenebis(N,N-dimethylaniline) (C17H22N2)',NULL,'http://vocabulary.odm2.org/variablename/4_4_Methylenebis_N_N_Dimethylaniline');
INSERT INTO "CV_VariableName" VALUES('bariumTotal','Barium, total','Total Barium (Ba). For chemical terms, "total" indicates an unfiltered sample.',NULL,'http://vocabulary.odm2.org/variablename/bariumTotal');
INSERT INTO "CV_VariableName" VALUES('bariumDistributionCoefficient','Barium, distribution coefficient','Ratio of concentrations of barium in two phases in equilibrium with each other. Phases must be specified',NULL,'http://vocabulary.odm2.org/variablename/bariumDistributionCoefficient');
INSERT INTO "CV_VariableName" VALUES('4_4_DDD','4,4-DDD','Dichlorodiphenyldichloroethane (C14H10Cl4)',NULL,'http://vocabulary.odm2.org/variablename/4_4_DDD');
INSERT INTO "CV_VariableName" VALUES('bis_2_Ethylhexyl_Phthalate','Bis-(2-ethylhexyl) phthalate','Bis-(2-ethylhexyl) phthalate (C6H4(C8H17COO)2)',NULL,'http://vocabulary.odm2.org/variablename/bis_2_Ethylhexyl_Phthalate');
INSERT INTO "CV_VariableName" VALUES('THSWIndex','THSW Index','The THSW Index uses temperature, humidity, solar radiation, and wind speed to calculate an apparent temperature.',NULL,'http://vocabulary.odm2.org/variablename/THSWIndex');
INSERT INTO "CV_VariableName" VALUES('waterUseDomesticWells','Water Use, Domestic wells','Water pumped by domestic wells; residents and landowners not using public supply. Nonagriculture wells.',NULL,'http://vocabulary.odm2.org/variablename/waterUseDomesticWells');
INSERT INTO "CV_VariableName" VALUES('2_3_5_Trimethylnaphthalene','2,3,5-Trimethylnaphthalene','2,3,5-Trimethylnaphthalene (C13H14), a polycyclic aromatic hydrocarbon (PAH)',NULL,'http://vocabulary.odm2.org/variablename/2_3_5_Trimethylnaphthalene');
INSERT INTO "CV_VariableName" VALUES('programSignature','Program signature','A unique data recorder program identifier which is useful for knowing when the source code in the data recorder has been modified.',NULL,'http://vocabulary.odm2.org/variablename/programSignature');
INSERT INTO "CV_VariableName" VALUES('leadDissolved','Lead, dissolved','Dissolved Lead (Pb). For chemical terms, dissolved indicates a filtered sample',NULL,'http://vocabulary.odm2.org/variablename/leadDissolved');
INSERT INTO "CV_VariableName" VALUES('2_Chloronaphthalene','2-Chloronaphthalene','2-Chloronaphthalene (C10H7Cl)',NULL,'http://vocabulary.odm2.org/variablename/2_Chloronaphthalene');
INSERT INTO "CV_VariableName" VALUES('arsenicTotal','Arsenic, total','Total arsenic (As). Total indicates was measured on a whole water sample.',NULL,'http://vocabulary.odm2.org/variablename/arsenicTotal');
INSERT INTO "CV_VariableName" VALUES('reservoirStorage','Reservoir storage','Reservoir water volume',NULL,'http://vocabulary.odm2.org/variablename/reservoirStorage');
CREATE TABLE CV_VariableType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_VariableType" VALUES('Chemistry','Chemistry','Variables associated with chemistry, chemical analysis or processes',NULL,'http://vocabulary.odm2.org/variabletype/Chemistry');
INSERT INTO "CV_VariableType" VALUES('Climate','Climate','Variables associated with the climate, weather, or atmospheric processes',NULL,'http://vocabulary.odm2.org/variabletype/Climate');
INSERT INTO "CV_VariableType" VALUES('Instrumentation','Instrumentation','Variables associated with instrumentation and instrument properties such as battery voltages, data logger temperatures, often useful for diagnosis.',NULL,'http://vocabulary.odm2.org/variabletype/Instrumentation');
INSERT INTO "CV_VariableType" VALUES('speciationRatio','Speciation ratio','Variables associated with a speciation ratio',NULL,'http://vocabulary.odm2.org/variabletype/speciationRatio');
INSERT INTO "CV_VariableType" VALUES('Soil','Soil','Variables associated with soil variables or processes',NULL,'http://vocabulary.odm2.org/variabletype/Soil');
INSERT INTO "CV_VariableType" VALUES('majorOxideElement','Major oxide or element','Variables associated with major oxides or elements',NULL,'http://vocabulary.odm2.org/variabletype/majorOxideElement');
INSERT INTO "CV_VariableType" VALUES('age','Age','Variables associated with age',NULL,'http://vocabulary.odm2.org/variabletype/age');
INSERT INTO "CV_VariableType" VALUES('ratio','Ratio','Variables associated with a ratio',NULL,'http://vocabulary.odm2.org/variabletype/ratio');
INSERT INTO "CV_VariableType" VALUES('Geology','Geology','Variables associated with geology or geological processes',NULL,'http://vocabulary.odm2.org/variabletype/Geology');
INSERT INTO "CV_VariableType" VALUES('modelData','Model data','Variables associated with modeled data',NULL,'http://vocabulary.odm2.org/variabletype/modelData');
INSERT INTO "CV_VariableType" VALUES('Unknown','Unknown','The VariableType is unknown.',NULL,'http://vocabulary.odm2.org/variabletype/Unknown');
INSERT INTO "CV_VariableType" VALUES('uraniumSeries','Uranium series','Variables associated with uranium series',NULL,'http://vocabulary.odm2.org/variabletype/uraniumSeries');
INSERT INTO "CV_VariableType" VALUES('Hydrology','Hydrology','Variables associated with hydrologic variables or processes',NULL,'http://vocabulary.odm2.org/variabletype/Hydrology');
INSERT INTO "CV_VariableType" VALUES('WaterQuality','Water quality','Variables associated with water quality variables or processes',NULL,'http://vocabulary.odm2.org/variabletype/WaterQuality');
INSERT INTO "CV_VariableType" VALUES('stableIsotopes','Stable isotopes','Variables associated with stable isotopes',NULL,'http://vocabulary.odm2.org/variabletype/stableIsotopes');
INSERT INTO "CV_VariableType" VALUES('radiogenicIsotopes','Radiogenic isotopes','Variables associated with radiogenic isotopes',NULL,'http://vocabulary.odm2.org/variabletype/radiogenicIsotopes');
INSERT INTO "CV_VariableType" VALUES('nobleGas','Noble gas','Variables associated with noble gasses',NULL,'http://vocabulary.odm2.org/variabletype/nobleGas');
INSERT INTO "CV_VariableType" VALUES('volatile','Volatile','Variables associated with volatile chemicals',NULL,'http://vocabulary.odm2.org/variabletype/volatile');
INSERT INTO "CV_VariableType" VALUES('traceElement','Trace element','Variables associated with trace elements',NULL,'http://vocabulary.odm2.org/variabletype/traceElement');
INSERT INTO "CV_VariableType" VALUES('Biota','Biota','Variables associated with biological organisms',NULL,'http://vocabulary.odm2.org/variabletype/Biota');
INSERT INTO "CV_VariableType" VALUES('rareEarthElement','Rare earth element','Variables associated with rare earth elements',NULL,'http://vocabulary.odm2.org/variabletype/rareEarthElement');
INSERT INTO "CV_VariableType" VALUES('endMember','End-Member','Variables associated with end members',NULL,'http://vocabulary.odm2.org/variabletype/endMember');
INSERT INTO "CV_VariableType" VALUES('rockMode','Rock mode','Variables associated with a rock mode',NULL,'http://vocabulary.odm2.org/variabletype/rockMode');
CREATE TABLE DataQuality (
	DataQualityID INTEGER   NOT NULL PRIMARY KEY,
	DataQualityTypeCV VARCHAR (255)  NOT NULL,
	DataQualityCode VARCHAR (255)  NOT NULL,
	DataQualityValue FLOAT   NULL,
	DataQualityValueUnitsID INTEGER   NULL,
	DataQualityDescription VARCHAR (500)  NULL,
	DataQualityLink VARCHAR (255)  NULL,
	FOREIGN KEY (DataQualityTypeCV) REFERENCES CV_DataQualityType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (DataQualityValueUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ReferenceMaterials (
	ReferenceMaterialID INTEGER   NOT NULL PRIMARY KEY,
	ReferenceMaterialMediumCV VARCHAR (255)  NOT NULL,
	ReferenceMaterialOrganizationID INTEGER   NOT NULL,
	ReferenceMaterialCode VARCHAR (50)  NOT NULL,
	ReferenceMaterialLotCode VARCHAR (255)  NULL,
	ReferenceMaterialPurchaseDate DATETIME   NULL,
	ReferenceMaterialExpirationDate DATETIME   NULL,
	ReferenceMaterialCertificateLink VARCHAR (255)  NULL,
	SamplingFeatureID INTEGER   NULL,
	FOREIGN KEY (ReferenceMaterialMediumCV) REFERENCES CV_ReferenceMaterialMedium (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ReferenceMaterialOrganizationID) REFERENCES Organizations (OrganizationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ReferenceMaterialValues (
	ReferenceMaterialValueID INTEGER   NOT NULL PRIMARY KEY,
	ReferenceMaterialID INTEGER   NOT NULL,
	ReferenceMaterialValue FLOAT   NOT NULL,
	ReferenceMaterialAccuracy FLOAT   NULL,
	VariableID INTEGER   NOT NULL,
	UnitsID INTEGER   NOT NULL,
	CitationID INTEGER   NOT NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ReferenceMaterialID) REFERENCES ReferenceMaterials (ReferenceMaterialID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (UnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (VariableID) REFERENCES Variables (VariableID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ResultNormalizationValues (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	NormalizedByReferenceMaterialValueID INTEGER   NOT NULL,
	FOREIGN KEY (NormalizedByReferenceMaterialValueID) REFERENCES ReferenceMaterialValues (ReferenceMaterialValueID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ResultsDataQuality (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataQualityID INTEGER   NOT NULL,
	FOREIGN KEY (DataQualityID) REFERENCES DataQuality (DataQualityID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CalibrationActions (
	ActionID INTEGER   NOT NULL PRIMARY KEY,
	CalibrationCheckValue FLOAT   NULL,
	InstrumentOutputVariableID INTEGER   NOT NULL,
	CalibrationEquation VARCHAR (255)  NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (InstrumentOutputVariableID) REFERENCES InstrumentOutputVariables (InstrumentOutputVariableID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CalibrationReferenceEquipment (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	EquipmentID INTEGER   NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES CalibrationActions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (EquipmentID) REFERENCES Equipment (EquipmentID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CalibrationStandards (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	ReferenceMaterialID INTEGER   NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES CalibrationActions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ReferenceMaterialID) REFERENCES ReferenceMaterials (ReferenceMaterialID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE DataloggerFileColumns (
	DataloggerFileColumnID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NULL,
	DataLoggerFileID INTEGER   NOT NULL,
	InstrumentOutputVariableID INTEGER   NOT NULL,
	ColumnLabel VARCHAR (50)  NOT NULL,
	ColumnDescription VARCHAR (500)  NULL,
	MeasurementEquation VARCHAR (255)  NULL,
	ScanInterval FLOAT   NULL,
	ScanIntervalUnitsID INTEGER   NULL,
	RecordingInterval FLOAT   NULL,
	RecordingIntervalUnitsID INTEGER   NULL,
	AggregationStatisticCV VARCHAR (255)  NULL,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (DataLoggerFileID) REFERENCES DataLoggerFiles (DataLoggerFileID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (InstrumentOutputVariableID) REFERENCES InstrumentOutputVariables (InstrumentOutputVariableID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RecordingIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ScanIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE DataLoggerFiles (
	DataLoggerFileID INTEGER   NOT NULL PRIMARY KEY,
	ProgramID INTEGER   NOT NULL,
	DataLoggerFileName VARCHAR (255)  NOT NULL,
	DataLoggerFileDescription VARCHAR (500)  NULL,
	DataLoggerFileLink VARCHAR (255)  NULL,
	FOREIGN KEY (ProgramID) REFERENCES DataloggerProgramFiles (ProgramID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE DataloggerProgramFiles (
	ProgramID INTEGER   NOT NULL PRIMARY KEY,
	AffiliationID INTEGER   NOT NULL,
	ProgramName VARCHAR (255)  NOT NULL,
	ProgramDescription VARCHAR (500)  NULL,
	ProgramVersion VARCHAR (50)  NULL,
	ProgramFileLink VARCHAR (255)  NULL,
	FOREIGN KEY (AffiliationID) REFERENCES Affiliations (AffiliationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Equipment (
	EquipmentID INTEGER   NOT NULL PRIMARY KEY,
	EquipmentCode VARCHAR (50)  NOT NULL,
	EquipmentName VARCHAR (255)  NOT NULL,
	EquipmentTypeCV VARCHAR (255)  NOT NULL,
	EquipmentModelID INTEGER   NOT NULL,
	EquipmentSerialNumber VARCHAR (50)  NOT NULL,
	EquipmentOwnerID INTEGER   NOT NULL,
	EquipmentVendorID INTEGER   NOT NULL,
	EquipmentPurchaseDate DATETIME   NOT NULL,
	EquipmentPurchaseOrderNumber VARCHAR (50)  NULL,
	EquipmentDescription VARCHAR (500)  NULL,
	EquipmentDocumentationLink VARCHAR (255)  NULL,
	FOREIGN KEY (EquipmentTypeCV) REFERENCES CV_EquipmentType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (EquipmentModelID) REFERENCES EquipmentModels (EquipmentModelID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (EquipmentVendorID) REFERENCES Organizations (OrganizationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (EquipmentOwnerID) REFERENCES People (PersonID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE EquipmentModels (
	EquipmentModelID INTEGER   NOT NULL PRIMARY KEY,
	ModelManufacturerID INTEGER   NOT NULL,
	ModelPartNumber VARCHAR (50)  NULL,
	ModelName VARCHAR (255)  NOT NULL,
	ModelDescription VARCHAR (500)  NULL,
	IsInstrument BIT   NOT NULL,
	ModelSpecificationsFileLink VARCHAR (255)  NULL,
	ModelLink VARCHAR (255)  NULL,
	FOREIGN KEY (ModelManufacturerID) REFERENCES Organizations (OrganizationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE EquipmentUsed (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	EquipmentID INTEGER   NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (EquipmentID) REFERENCES Equipment (EquipmentID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE InstrumentOutputVariables (
	InstrumentOutputVariableID INTEGER   NOT NULL PRIMARY KEY,
	ModelID INTEGER   NOT NULL,
	VariableID INTEGER   NOT NULL,
	InstrumentMethodID INTEGER   NOT NULL,
	InstrumentResolution VARCHAR (255)  NULL,
	InstrumentAccuracy VARCHAR (255)  NULL,
	InstrumentRawOutputUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (ModelID) REFERENCES EquipmentModels (EquipmentModelID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (InstrumentMethodID) REFERENCES Methods (MethodID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (InstrumentRawOutputUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (VariableID) REFERENCES Variables (VariableID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE MaintenanceActions (
	ActionID INTEGER   NOT NULL PRIMARY KEY,
	IsFactoryService BIT   NOT NULL,
	MaintenanceCode VARCHAR (50)  NULL,
	MaintenanceReason VARCHAR (500)  NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE RelatedEquipment (
	RelationID INTEGER   NOT NULL PRIMARY KEY,
	EquipmentID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	RelatedEquipmentID INTEGER   NOT NULL,
	RelationshipStartDateTime DATETIME   NOT NULL,
	RelationshipStartDateTimeUTCOffset INTEGER   NOT NULL,
	RelationshipEndDateTime DATETIME   NULL,
	RelationshipEndDateTimeUTCOffset INTEGER   NULL,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (EquipmentID) REFERENCES Equipment (EquipmentID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelatedEquipmentID) REFERENCES Equipment (EquipmentID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ActionExtensionPropertyValues (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	PropertyID INTEGER   NOT NULL,
	PropertyValue VARCHAR (255)  NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (PropertyID) REFERENCES ExtensionProperties (PropertyID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CitationExtensionPropertyValues (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	CitationID INTEGER   NOT NULL,
	PropertyID INTEGER   NOT NULL,
	PropertyValue VARCHAR (255)  NOT NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (PropertyID) REFERENCES ExtensionProperties (PropertyID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ExtensionProperties (
	PropertyID INTEGER   NOT NULL PRIMARY KEY,
	PropertyName VARCHAR (255)  NOT NULL,
	PropertyDescription VARCHAR (500)  NULL,
	PropertyDataTypeCV VARCHAR (255)  NOT NULL,
	PropertyUnitsID INTEGER   NULL,
	FOREIGN KEY (PropertyDataTypeCV) REFERENCES CV_PropertyDataType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (PropertyUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE MethodExtensionPropertyValues (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	MethodID INTEGER   NOT NULL,
	PropertyID INTEGER   NOT NULL,
	PropertyValue VARCHAR (255)  NOT NULL,
	FOREIGN KEY (PropertyID) REFERENCES ExtensionProperties (PropertyID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (MethodID) REFERENCES Methods (MethodID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ResultExtensionPropertyValues (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	PropertyID INTEGER   NOT NULL,
	PropertyValue VARCHAR (255)  NOT NULL,
	FOREIGN KEY (PropertyID) REFERENCES ExtensionProperties (PropertyID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SamplingFeatureExtensionPropertyValues (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	SamplingFeatureID INTEGER   NOT NULL,
	PropertyID INTEGER   NOT NULL,
	PropertyValue VARCHAR (255)  NOT NULL,
	FOREIGN KEY (PropertyID) REFERENCES ExtensionProperties (PropertyID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE VariableExtensionPropertyValues (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	VariableID INTEGER   NOT NULL,
	PropertyID INTEGER   NOT NULL,
	PropertyValue VARCHAR (255)  NOT NULL,
	FOREIGN KEY (PropertyID) REFERENCES ExtensionProperties (PropertyID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (VariableID) REFERENCES Variables (VariableID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CitationExternalIdentifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	CitationID INTEGER   NOT NULL,
	ExternalIdentifierSystemID INTEGER   NOT NULL,
	CitationExternalIdentifier VARCHAR (255)  NOT NULL,
	CitationExternalIdentifierURI VARCHAR (255)  NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ExternalIdentifierSystemID) REFERENCES ExternalIdentifierSystems (ExternalIdentifierSystemID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ExternalIdentifierSystems (
	ExternalIdentifierSystemID INTEGER   NOT NULL PRIMARY KEY,
	ExternalIdentifierSystemName VARCHAR (255)  NOT NULL,
	IdentifierSystemOrganizationID INTEGER   NOT NULL,
	ExternalIdentifierSystemDescription VARCHAR (500)  NULL,
	ExternalIdentifierSystemURL VARCHAR (255)  NULL,
	FOREIGN KEY (IdentifierSystemOrganizationID) REFERENCES Organizations (OrganizationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE MethodExternalIdentifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	MethodID INTEGER   NOT NULL,
	ExternalIdentifierSystemID INTEGER   NOT NULL,
	MethodExternalIdentifier VARCHAR (255)  NOT NULL,
	MethodExternalIdentifierURI VARCHAR (255)  NULL,
	FOREIGN KEY (ExternalIdentifierSystemID) REFERENCES ExternalIdentifierSystems (ExternalIdentifierSystemID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (MethodID) REFERENCES Methods (MethodID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE PersonExternalIdentifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	PersonID INTEGER   NOT NULL,
	ExternalIdentifierSystemID INTEGER   NOT NULL,
	PersonExternalIdentifier VARCHAR (255)  NOT NULL,
	PersonExternalIdentifierURI VARCHAR (255)  NULL,
	FOREIGN KEY (ExternalIdentifierSystemID) REFERENCES ExternalIdentifierSystems (ExternalIdentifierSystemID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (PersonID) REFERENCES People (PersonID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ReferenceMaterialExternalIdentifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ReferenceMaterialID INTEGER   NOT NULL,
	ExternalIdentifierSystemID INTEGER   NOT NULL,
	ReferenceMaterialExternalIdentifier VARCHAR (255)  NOT NULL,
	ReferenceMaterialExternalIdentifierURI VARCHAR (255)  NULL,
	FOREIGN KEY (ExternalIdentifierSystemID) REFERENCES ExternalIdentifierSystems (ExternalIdentifierSystemID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ReferenceMaterialID) REFERENCES ReferenceMaterials (ReferenceMaterialID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SamplingFeatureExternalIdentifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	SamplingFeatureID INTEGER   NOT NULL,
	ExternalIdentifierSystemID INTEGER   NOT NULL,
	SamplingFeatureExternalIdentifier VARCHAR (255)  NOT NULL,
	SamplingFeatureExternalIdentifierURI VARCHAR (255)  NULL,
	FOREIGN KEY (ExternalIdentifierSystemID) REFERENCES ExternalIdentifierSystems (ExternalIdentifierSystemID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SpatialReferenceExternalIdentifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	SpatialReferenceID INTEGER   NOT NULL,
	ExternalIdentifierSystemID INTEGER   NOT NULL,
	SpatialReferenceExternalIdentifier VARCHAR (255)  NOT NULL,
	SpatialReferenceExternalIdentifierURI VARCHAR (255)  NULL,
	FOREIGN KEY (ExternalIdentifierSystemID) REFERENCES ExternalIdentifierSystems (ExternalIdentifierSystemID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TaxonomicClassifierExternalIdentifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	TaxonomicClassifierID INTEGER   NOT NULL,
	ExternalIdentifierSystemID INTEGER   NOT NULL,
	TaxonomicClassifierExternalIdentifier VARCHAR (255)  NOT NULL,
	TaxonomicClassifierExternalIdentifierURI VARCHAR (255)  NULL,
	FOREIGN KEY (ExternalIdentifierSystemID) REFERENCES ExternalIdentifierSystems (ExternalIdentifierSystemID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (TaxonomicClassifierID) REFERENCES TaxonomicClassifiers (TaxonomicClassifierID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE VariableExternalIdentifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	VariableID INTEGER   NOT NULL,
	ExternalIdentifierSystemID INTEGER   NOT NULL,
	VariableExternalIdentifer VARCHAR (255)  NOT NULL,
	VariableExternalIdentifierURI VARCHAR (255)  NULL,
	FOREIGN KEY (ExternalIdentifierSystemID) REFERENCES ExternalIdentifierSystems (ExternalIdentifierSystemID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (VariableID) REFERENCES Variables (VariableID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ActionDirectives (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	DirectiveID INTEGER   NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (DirectiveID) REFERENCES Directives (DirectiveID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Directives (
	DirectiveID INTEGER   NOT NULL PRIMARY KEY,
	DirectiveTypeCV VARCHAR (255)  NOT NULL,
	DirectiveDescription VARCHAR (500)  NOT NULL,
	FOREIGN KEY (DirectiveTypeCV) REFERENCES CV_DirectiveType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SpecimenBatchPostions (
	FeatureActionID INTEGER   NOT NULL PRIMARY KEY,
	BatchPositionNumber INTEGER   NOT NULL,
	BatchPositionLabel VARCHAR (255)  NULL,
	FOREIGN KEY (FeatureActionID) REFERENCES FeatureActions (FeatureActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE AuthorLists (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	CitationID INTEGER   NOT NULL,
	PersonID INTEGER   NOT NULL,
	AuthorOrder INTEGER   NOT NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (PersonID) REFERENCES People (PersonID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Citations (
	CitationID INTEGER   NOT NULL PRIMARY KEY,
	Title VARCHAR (255)  NOT NULL,
	Publisher VARCHAR (255)  NOT NULL,
	PublicationYear INTEGER   NOT NULL,
	CitationLink VARCHAR (255)  NULL
);
CREATE TABLE DatasetCitations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	DataSetID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	CitationID INTEGER   NOT NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (DataSetID) REFERENCES Datasets (DatasetID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE DerivationEquations (
	DerivationEquationID INTEGER   NOT NULL PRIMARY KEY,
	DerivationEquation VARCHAR (255)  NOT NULL
);
CREATE TABLE MethodCitations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	MethodID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	CitationID INTEGER   NOT NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (MethodID) REFERENCES Methods (MethodID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE RelatedAnnotations (
	RelationID INTEGER   NOT NULL PRIMARY KEY,
	AnnotationID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	RelatedAnnotationID INTEGER   NOT NULL,
	FOREIGN KEY (AnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelatedAnnotationID) REFERENCES Annotations (AnnotationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE RelatedCitations (
	RelationID INTEGER   NOT NULL PRIMARY KEY,
	CitationID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	RelatedCitationID INTEGER   NOT NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelatedCitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE RelatedDatasets (
	RelationID INTEGER   NOT NULL PRIMARY KEY,
	DataSetID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	RelatedDatasetID INTEGER   NOT NULL,
	VersionCode VARCHAR (50)  NULL,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (DataSetID) REFERENCES Datasets (DatasetID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelatedDatasetID) REFERENCES Datasets (DatasetID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE RelatedResults (
	RelationID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	RelatedResultID INTEGER   NOT NULL,
	VersionCode VARCHAR (50)  NULL,
	RelatedResultSequenceNumber INTEGER   NULL,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelatedResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ResultDerivationEquations (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	DerivationEquationID INTEGER   NOT NULL,
	FOREIGN KEY (DerivationEquationID) REFERENCES DerivationEquations (DerivationEquationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CategoricalResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	XLocation FLOAT   NULL,
	XLocationUnitsID INTEGER   NULL,
	YLocation FLOAT   NULL,
	YLocationUnitsID INTEGER   NULL,
	ZLocation FLOAT   NULL,
	ZLocationUnitsID INTEGER   NULL,
	SpatialReferenceID INTEGER   NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE CategoricalResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue VARCHAR (255)  NOT NULL,
	ValueDateTime DATETIME   NOT NULL,
	ValueDateTimeUTCOffset INTEGER   NOT NULL,
	FOREIGN KEY (ResultID) REFERENCES CategoricalResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE MeasurementResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	XLocation FLOAT   NULL,
	XLocationUnitsID INTEGER   NULL,
	YLocation FLOAT   NULL,
	YLocationUnitsID INTEGER   NULL,
	ZLocation FLOAT   NULL,
	ZLocationUnitsID INTEGER   NULL,
	SpatialReferenceID INTEGER   NULL,
	CensorCodeCV VARCHAR (255)  NOT NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	TimeAggregationInterval FLOAT   NOT NULL,
	TimeAggregationIntervalUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (TimeAggregationIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (CensorCodeCV) REFERENCES CV_CensorCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (XLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (YLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ZLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE MeasurementResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue FLOAT   NOT NULL,
	ValueDateTime DATETIME   NOT NULL,
	ValueDateTimeUTCOffset INTEGER   NOT NULL,
	FOREIGN KEY (ResultID) REFERENCES MeasurementResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE PointCoverageResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	ZLocation FLOAT   NULL,
	ZLocationUnitsID INTEGER   NULL,
	SpatialReferenceID INTEGER   NULL,
	IntendedXSpacing FLOAT   NULL,
	IntendedXSpacingUnitsID INTEGER   NULL,
	IntendedYSpacing FLOAT   NULL,
	IntendedYSpacingUnitsID INTEGER   NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	TimeAggregationInterval FLOAT   NOT NULL,
	TimeAggregationIntervalUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedXSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedYSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ZLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE PointCoverageResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue INTEGER   NOT NULL,
	ValueDateTime DATETIME   NOT NULL,
	ValueDateTimeUTCOffset INTEGER   NOT NULL,
	XLocation FLOAT   NOT NULL,
	XLocationUnitsID INTEGER   NOT NULL,
	YLocation FLOAT   NOT NULL,
	YLocationUnitsID INTEGER   NOT NULL,
	CensorCodeCV VARCHAR (255)  NOT NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	FOREIGN KEY (CensorCodeCV) REFERENCES CV_CensorCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES PointCoverageResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (XLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (YLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ProfileResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	XLocation FLOAT   NULL,
	XLocationUnitsID INTEGER   NULL,
	YLocation FLOAT   NULL,
	YLocationUnitsID INTEGER   NULL,
	SpatialReferenceID INTEGER   NULL,
	IntendedZSpacing FLOAT   NULL,
	IntendedZSpacingUnitsID INTEGER   NULL,
	IntendedTimeSpacing FLOAT   NULL,
	IntendedTimeSpacingUnitsID INTEGER   NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedZSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedTimeSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (XLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (YLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ProfileResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue FLOAT   NOT NULL,
	ValueDateTime DATETIME   NOT NULL,
	ValueDateTimeUTCOffset INTEGER   NOT NULL,
	ZLocation FLOAT   NOT NULL,
	ZAggregationInterval FLOAT   NOT NULL,
	ZLocationUnitsID INTEGER   NOT NULL,
	CensorCodeCV VARCHAR (255)  NOT NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	TimeAggregationInterval FLOAT   NOT NULL,
	TimeAggregationIntervalUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (TimeAggregationIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (CensorCodeCV) REFERENCES CV_CensorCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ZLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES ProfileResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SectionResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	YLocation FLOAT   NULL,
	YLocationUnitsID INTEGER   NULL,
	SpatialReferenceID INTEGER   NULL,
	IntendedXSpacing FLOAT   NULL,
	IntendedXSpacingUnitsID INTEGER   NULL,
	IntendedZSpacing FLOAT   NULL,
	IntendedZSpacingUnitsID INTEGER   NULL,
	IntendedTimeSpacing FLOAT   NULL,
	IntendedTimeSpacingUnitsID INTEGER   NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedTimeSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (YLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedXSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedZSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SectionResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue DOUBLE   NOT NULL,
	ValueDateTime INTEGER   NOT NULL,
	ValueDateTimeUTCOffset INTEGER   NOT NULL,
	XLocation DOUBLE   NOT NULL,
	XAggregationInterval FLOAT   NOT NULL,
	XLocationUnitsID INTEGER   NOT NULL,
	ZLocation INTEGER   NOT NULL,
	ZAggregationInterval FLOAT   NOT NULL,
	ZLocationUnitsID INTEGER   NOT NULL,
	CensorCodeCV VARCHAR (255)  NOT NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	TimeAggregationInterval FLOAT   NOT NULL,
	TimeAggregationIntervalUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (TimeAggregationIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (CensorCodeCV) REFERENCES CV_CensorCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES SectionResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (XLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ZLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SpectraResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	XLocation FLOAT   NULL,
	XLocationUnitsID INTEGER   NULL,
	YLocation FLOAT   NULL,
	YLocationUnitsID INTEGER   NULL,
	ZLocation FLOAT   NULL,
	ZLocationUnitsID INTEGER   NULL,
	SpatialReferenceID INTEGER   NULL,
	IntendedWavelengthSpacing DOUBLE   NULL,
	IntendedWavelengthSpacingUnitsID INTEGER   NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedWavelengthSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (XLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (YLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ZLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SpectraResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue FLOAT   NOT NULL,
	ValueDateTime DATETIME   NOT NULL,
	ValueDateTimeUTCOffset INTEGER   NOT NULL,
	ExcitationWavelength FLOAT   NOT NULL,
	EmissionWavelength FLOAT   NOT NULL,
	WavelengthUnitsID INTEGER   NOT NULL,
	CensorCodeCV VARCHAR (255)  NOT NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	TimeAggregationInterval DOUBLE   NOT NULL,
	TimeAggregationIntervalUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (TimeAggregationIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (CensorCodeCV) REFERENCES CV_CensorCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES SpectraResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (WavelengthUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TimeSeriesResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	XLocation FLOAT   NULL,
	XLocationUnitsID INTEGER   NULL,
	YLocation FLOAT   NULL,
	YLocationUnitsID INTEGER   NULL,
	ZLocation FLOAT   NULL,
	ZLocationUnitsID INTEGER   NULL,
	SpatialReferenceID INTEGER   NULL,
	IntendedTimeSpacing FLOAT   NULL,
	IntendedTimeSpacingUnitsID INTEGER   NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedTimeSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (XLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (YLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ZLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TimeSeriesResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue FLOAT   NOT NULL,
	ValueDateTime DATETIME   NOT NULL,
	ValueDateTimeUTCOffset INTEGER   NOT NULL,
	CensorCodeCV VARCHAR (255)  NOT NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	TimeAggregationInterval FLOAT   NOT NULL,
	TimeAggregationIntervalUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (TimeAggregationIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (CensorCodeCV) REFERENCES CV_CensorCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES TimeSeriesResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TrajectoryResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	SpatialReferenceID INTEGER   NULL,
	IntendedTrajectorySpacing FLOAT   NULL,
	IntendedTrajectorySpacingUnitsID INTEGER   NULL,
	IntendedTimeSpacing FLOAT   NULL,
	IntendedTimeSpacingUnitsID INTEGER   NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedTrajectorySpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedTimeSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TrajectoryResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue FLOAT   NOT NULL,
	ValueDateTime DATETIME   NOT NULL,
	ValueDateTimeUTCOffset INTEGER   NOT NULL,
	XLocation FLOAT   NOT NULL,
	XLocationUnitsID INTEGER   NOT NULL,
	YLocation FLOAT   NOT NULL,
	YLocationUnitsID INTEGER   NOT NULL,
	ZLocation FLOAT   NOT NULL,
	ZLocationUnitsID INTEGER   NOT NULL,
	TrajectoryDistance FLOAT   NOT NULL,
	TrajectoryDistanceAggregationInterval FLOAT   NOT NULL,
	TrajectoryDistanceUnitsID INTEGER   NOT NULL,
	CensorCodeCV VARCHAR (255)  NOT NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	TimeAggregationInterval FLOAT   NOT NULL,
	TimeAggregationIntervalUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (TimeAggregationIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (CensorCodeCV) REFERENCES CV_CensorCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (TrajectoryDistanceUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES TrajectoryResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (XLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (YLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ZLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TransectResults (
	ResultID INTEGER   NOT NULL PRIMARY KEY,
	ZLocation FLOAT   NULL,
	ZLocationUnitsID INTEGER   NULL,
	SpatialReferenceID INTEGER   NULL,
	IntendedTransectSpacing FLOAT   NULL,
	IntendedTransectSpacingUnitsID INTEGER   NULL,
	IntendedTimeSpacing FLOAT   NULL,
	IntendedTimeSpacingUnitsID INTEGER   NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES Results (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedTimeSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (IntendedTransectSpacingUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ZLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE TransectResultValues (
	ValueID INTEGER   NOT NULL PRIMARY KEY,
	ResultID INTEGER   NOT NULL,
	DataValue FLOAT   NOT NULL,
	ValueDateTime DATETIME   NOT NULL,
	ValueDateTimeUTCOffset DATETIME   NOT NULL,
	XLocation FLOAT   NOT NULL,
	XLocationUnitsID INTEGER   NOT NULL,
	YLocation FLOAT   NOT NULL,
	YLocationUnitsID INTEGER   NOT NULL,
	TransectDistance FLOAT   NOT NULL,
	TransectDistanceAggregationInterval FLOAT   NOT NULL,
	TransectDistanceUnitsID INTEGER   NOT NULL,
	CensorCodeCV VARCHAR (255)  NOT NULL,
	QualityCodeCV VARCHAR (255)  NOT NULL,
	AggregationStatisticCV VARCHAR (255)  NOT NULL,
	TimeAggregationInterval FLOAT   NOT NULL,
	TimeAggregationIntervalUnitsID INTEGER   NOT NULL,
	FOREIGN KEY (TimeAggregationIntervalUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (AggregationStatisticCV) REFERENCES CV_AggregationStatistic (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (CensorCodeCV) REFERENCES CV_CensorCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (QualityCodeCV) REFERENCES CV_QualityCode (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (TransectDistanceUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ResultID) REFERENCES TransectResults (ResultID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (XLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (YLocationUnitsID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE RelatedFeatures (
	RelationID INTEGER   NOT NULL PRIMARY KEY,
	SamplingFeatureID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	RelatedFeatureID INTEGER   NOT NULL,
	SpatialOffsetID INTEGER   NULL,
	FOREIGN KEY (RelatedFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialOffsetID) REFERENCES SpatialOffsets (SpatialOffsetID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Sites (
	SamplingFeatureID INTEGER   NOT NULL PRIMARY KEY,
	SiteTypeCV VARCHAR (255)  NOT NULL,
	Latitude FLOAT   NOT NULL,
	Longitude FLOAT   NOT NULL,
	SpatialReferenceID INTEGER   NOT NULL,
	FOREIGN KEY (SiteTypeCV) REFERENCES CV_SiteType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpatialReferenceID) REFERENCES SpatialReferences (SpatialReferenceID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SpatialOffsets (
	SpatialOffsetID INTEGER   NOT NULL PRIMARY KEY,
	SpatialOffsetTypeCV VARCHAR (255)  NOT NULL,
	Offset1Value FLOAT   NOT NULL,
	Offset1UnitID INTEGER   NOT NULL,
	Offset2Value FLOAT   NULL,
	Offset2UnitID INTEGER   NULL,
	Offset3Value FLOAT   NULL,
	Offset3UnitID INTEGER   NULL,
	FOREIGN KEY (SpatialOffsetTypeCV) REFERENCES CV_SpatialOffsetType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (Offset1UnitID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (Offset2UnitID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (Offset3UnitID) REFERENCES Units (UnitsID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SpatialReferences (
	SpatialReferenceID INTEGER   NOT NULL PRIMARY KEY,
	SRSCode VARCHAR (50)  NULL,
	SRSName VARCHAR (255)  NOT NULL,
	SRSDescription VARCHAR (500)  NULL,
	SRSLink VARCHAR (255)  NULL
);
CREATE TABLE Specimens (
	SamplingFeatureID INTEGER   NOT NULL PRIMARY KEY,
	SpecimenTypeCV VARCHAR (255)  NOT NULL,
	SpecimenMediumCV VARCHAR (255)  NOT NULL,
	IsFieldSpecimen BIT   NOT NULL,
	FOREIGN KEY (SpecimenMediumCV) REFERENCES CV_SpecimenMedium (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SpecimenTypeCV) REFERENCES CV_SpecimenType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES SamplingFeatures (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE SpecimenTaxonomicClassifiers (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	SamplingFeatureID INTEGER   NOT NULL,
	TaxonomicClassifierID INTEGER   NOT NULL,
	CitationID INTEGER   NULL,
	FOREIGN KEY (CitationID) REFERENCES Citations (CitationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (SamplingFeatureID) REFERENCES Specimens (SamplingFeatureID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (TaxonomicClassifierID) REFERENCES TaxonomicClassifiers (TaxonomicClassifierID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE ModelAffiliations (
	BridgeID INTEGER   NOT NULL PRIMARY KEY,
	ModelID INTEGER   NOT NULL,
	AffiliationID INTEGER   NOT NULL,
	IsPrimary BIT   NOT NULL,
	RoleDescription VARCHAR (500)  NULL,
	FOREIGN KEY (AffiliationID) REFERENCES Affiliations (AffiliationID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ModelID) REFERENCES Models (ModelID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Models (
	ModelID INTEGER   NOT NULL PRIMARY KEY,
	ModelCode VARCHAR (50)  NOT NULL,
	ModelName VARCHAR (255)  NOT NULL,
	ModelDescription VARCHAR (500)  NULL,
	Version VARCHAR (255)  NULL,
	ModelLink VARCHAR (255)  NULL
);
CREATE TABLE RelatedModels (
	RelatedID INTEGER   NOT NULL PRIMARY KEY,
	ModelID INTEGER   NOT NULL,
	RelationshipTypeCV VARCHAR (255)  NOT NULL,
	RelatedModelID INTEGER   NOT NULL,
	FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ModelID) REFERENCES Models (ModelID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE Simulations (
	SimulationID INTEGER   NOT NULL PRIMARY KEY,
	ActionID INTEGER   NOT NULL,
	SimulationName VARCHAR (255)  NOT NULL,
	SimulationDescription VARCHAR (500)  NULL,
	SimulationStartDateTime DATETIME   NOT NULL,
	SimulationStartDateTimeUTCOffset INTEGER   NOT NULL,
	SimulationEndDateTime DATETIME   NOT NULL,
	SimulationEndDateTimeUTCOffset INTEGER   NOT NULL,
	TimeStepValue FLOAT   NOT NULL,
	TimeStepUnitsID INTEGER   NOT NULL,
	InputDataSetID INTEGER   NULL,
	ModelID INTEGER   NOT NULL,
	FOREIGN KEY (ActionID) REFERENCES Actions (ActionID)
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY (ModelID) REFERENCES Models (ModelID)
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMIT;
