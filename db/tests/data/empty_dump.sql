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
CREATE TABLE CV_AggregationStatistic (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_AnnotationType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_CensorCode (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
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
CREATE TABLE CV_DirectiveType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_ElevationDatum (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_EquipmentType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_MethodType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_OrganizationType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_PropertyDataType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_QualityCode (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
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
CREATE TABLE CV_ResultType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
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
CREATE TABLE CV_SamplingFeatureType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_SiteType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_SpatialOffsetType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_Speciation (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
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
CREATE TABLE CV_UnitsType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
INSERT INTO "CV_UnitsType" VALUES('electricCapacitance','Electric capacitance','Capacitance is the ability of a body to store an electrical charge.',NULL,'http://vocabulary.odm2.org/unitstype/electricCapacitance');
INSERT INTO "CV_UnitsType" VALUES('doseEquivalent','Dose equivalent','Equivalent dose is a dose quantity used in radiological protection to represent the stochastic health effects (probability of cancer induction and genetic damage) of low levels of ionizing radiation on the human body. It is based on the physical quantity absorbed dose, but takes into account the biological effectiveness of the radiation, which is dependent on the radiation type and energy. [Wikipedia]','SpecificEnergy','http://vocabulary.odm2.org/unitstype/doseEquivalent');
INSERT INTO "CV_UnitsType" VALUES('electricCharge','Electric charge','Electric charge is the physical property of matter that causes it to experience a force when placed in an electromagnetic field. The SI derived unit of electric charge is the coulomb (C), although in electrical engineering it is also common to use the ampere-hour (Ah), and in chemistry it is common to use the elementary charge (e) as a unit. The symbol Q is often used to denote charge. [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/electricCharge');
INSERT INTO "CV_UnitsType" VALUES('electricFluxDensity','Electric flux density','In physics, the electric displacement field, denoted by D, is a vector field that appears in Maxwell''s equations. It accounts for the effects of free and bound charge within materials. "D" stands for "displacement", as in the related concept of displacement current in dielectrics. In free space, the electric displacement field is equivalent to flux density, a concept that lends understanding to Gauss''s law.',NULL,'http://vocabulary.odm2.org/unitstype/electricFluxDensity');
INSERT INTO "CV_UnitsType" VALUES('areaThermalExpansion','Area thermal expansion','When the temperature of a substance changes, the energy that is stored in the intermolecular bonds between atoms changes. When the stored energy increases, so does the length of the molecular bonds. As a result, solids typically expand in response to heating and contract on cooling; this dimensional response to temperature change is expressed by its coefficient of thermal expansion. Different coefficients of thermal expansion can be defined for a substance depending on whether the expansion is measured by: * linear thermal expansion * area thermal expansion * volumetric thermal expansion These characteristics are closely related. The volumetric thermal expansion coefficient can be defined for both liquids and solids. The linear thermal expansion can only be defined for solids, and is common in engineering applications. Some substances expand when cooled, such as freezing water, so they have negative thermal expansion coefficients. [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/areaThermalExpansion');
INSERT INTO "CV_UnitsType" VALUES('electricChargePerMass','Electric charge per mass','In electromagnetism, charge density is a measure of electric charge per unit volume of space, in one, two or three dimensions. More specifically: the linear, surface, or volume charge density is the amount of electric charge per unit length, surface area, or volume, respectively. The respective SI units are Cm1, Cm2 or Cm3.','Density','http://vocabulary.odm2.org/unitstype/electricChargePerMass');
INSERT INTO "CV_UnitsType" VALUES('volumetricHeatCapacity','Volumetric heat capacity','Volumetric heat capacity (VHC), also termed volume-specific heat capacity, describes the ability of a given volume of a substance to store internal energy while undergoing a given temperature change, but without undergoing a phase transition. It is different from specific heat capacity in that the VHC is a ''per unit volume'' measure of the relationship between thermal energy and temperature of a material, while the specific heat is a ''per unit mass'' measure (or occasionally per molar quantity of the material).',NULL,'http://vocabulary.odm2.org/unitstype/volumetricHeatCapacity');
INSERT INTO "CV_UnitsType" VALUES('specificEnergy','Specific energy','Specific energy is energy per unit mass. (It is also sometimes called "energy density," though "energy density" more precisely means energy per unit volume.) The SI unit for specific energy is the joule per kilogram (J/kg). Other units still in use in some contexts are the kilocalorie per gram (Cal/g or kcal/g), mostly in food-related topics, watt hours per kilogram in the field of batteries, and the Imperial unit BTU per pound (BTU/lb), in some engineering and applied technical fields.',NULL,'http://vocabulary.odm2.org/unitstype/specificEnergy');
INSERT INTO "CV_UnitsType" VALUES('liquidVolume','Liquid volume',NULL,'Volume','http://vocabulary.odm2.org/unitstype/liquidVolume');
INSERT INTO "CV_UnitsType" VALUES('energyDensity','Energy density','Energy density is the amount of energy stored in a given system or region of space per unit volume or mass, though the latter is more accurately termed specific energy.','Density','http://vocabulary.odm2.org/unitstype/energyDensity');
INSERT INTO "CV_UnitsType" VALUES('fluidPermeability','Fluid permeability','Permeability in fluid mechanics and the earth sciences (commonly symbolized as , or k) is a measure of the ability of a porous material (often, a rock or unconsolidated material) to allow fluids to pass through it.',NULL,'http://vocabulary.odm2.org/unitstype/fluidPermeability');
INSERT INTO "CV_UnitsType" VALUES('powerPerArea','Power per area',NULL,NULL,'http://vocabulary.odm2.org/unitstype/powerPerArea');
INSERT INTO "CV_UnitsType" VALUES('angularMomentum','Angular momentum','Quantity of rotational motion. Linear momentum is the quantity obtained by multiplying the mass of a body by its linear velocity. Angular momentum is the quantity obtained by multiplying the moment of inertia of a body by its angular velocity. The momentum of a system of particles is given by the sum of the momenta of the individual particles which make up the system or by the product of the total mass of the system and the velocity of the center of gravity of the system. The momentum of a continuous medium is given by the integral of the velocity over the mass of the medium or by the product of the total mass of the medium and the velocity of the center of gravity of the medium. In physics, the angular momentum of an object rotating about some reference point is the measure of the extent to which the object will continue to rotate about that point unless acted upon by an external torque. In particular, if a point mass rotates about an axis, then the angular momentum with respect to a point on the axis is related to the mass of the object, the velocity and the distance of the mass to the axis. While the motion associated with linear momentum has no absolute frame of reference, the rotation associated with angular momentum is sometimes spoken of as being measured relative to the fixed stars.','Momentum','http://vocabulary.odm2.org/unitstype/angularMomentum');
INSERT INTO "CV_UnitsType" VALUES('magneticFlux','Magnetic flux','Magnetic Flux is the product of the average magnetic field times the perpendicular area that it penetrates.',NULL,'http://vocabulary.odm2.org/unitstype/magneticFlux');
INSERT INTO "CV_UnitsType" VALUES('luminousFluxPerArea','Luminous flux per area','Luminous Flux or Luminous Power is the measure of the perceived power of light. It differs from radiant flux, the measure of the total power of light emitted, in that luminous flux is adjusted to reflect the varying sensitivity of the human eye to different wavelengths of light.',NULL,'http://vocabulary.odm2.org/unitstype/luminousFluxPerArea');
INSERT INTO "CV_UnitsType" VALUES('thermalResistance','Thermal resistance','Thermal resistance is a heat property and a measurement of a temperature difference by which an object or material resists a heat flow. Thermal resistance is the reciprocal of thermal conductance. (Absolute) thermal resistance R in K/W is a property of a particular component. For example, a characteristic of a heat sink. Specific thermal resistance or specific thermal resistivity R in (Km)/W is a material constant.',NULL,'http://vocabulary.odm2.org/unitstype/thermalResistance');
INSERT INTO "CV_UnitsType" VALUES('area','Area','Area is a quantity expressing the two-dimensional size of a defined part of a surface, typically a region bounded by a closed curve.',NULL,'http://vocabulary.odm2.org/unitstype/area');
INSERT INTO "CV_UnitsType" VALUES('specificSurfaceArea','Specific surface area ','Specific surface area "SSA" is a property of solids which is the total surface area of a material per unit of mass. It is a derived scientific value that can be used to determine the type and properties of a material (e.g. soil, snow). It is defined by surface area divided by mass (with units of m/kg).',NULL,'http://vocabulary.odm2.org/unitstype/specificSurfaceArea');
INSERT INTO "CV_UnitsType" VALUES('magneticDipoleMoment','Magnetic dipole moment','The magnetic moment of a system is a measure of the magnitude and the direction of its magnetism. Magnetic moment usually refers to its Magnetic Dipole Moment, and quantifies the contribution of the system''s internal magnetism to the external dipolar magnetic field produced by the system (that is, the component of the external magnetic field that is inversely proportional to the cube of the distance to the observer). The Magnetic Dipole Moment is a vector-valued quantity.',NULL,'http://vocabulary.odm2.org/unitstype/magneticDipoleMoment');
INSERT INTO "CV_UnitsType" VALUES('powerPerAreaAngle','Power per area angle',NULL,NULL,'http://vocabulary.odm2.org/unitstype/powerPerAreaAngle');
INSERT INTO "CV_UnitsType" VALUES('inverseLength','Inverse length','Inverse Length',NULL,'http://vocabulary.odm2.org/unitstype/inverseLength');
INSERT INTO "CV_UnitsType" VALUES('pressure','Pressure','Pressure is an effect which occurs when a force is applied on a surface. Pressure is the amount of force acting on a unit area. Pressure is distinct from stress, as the former is the ratio of the component of force normal to a surface to the surface area. Stress is a tensor that relates the vector force to the vector area.','ForcePerArea','http://vocabulary.odm2.org/unitstype/pressure');
INSERT INTO "CV_UnitsType" VALUES('fluorescence','Fluorescence','Fluorescence is the emission of light by a substance that has absorbed light or other electromagnetic radiation.','Dimensionless','http://vocabulary.odm2.org/unitstype/fluorescence');
INSERT INTO "CV_UnitsType" VALUES('heatCapacityRatio','Heat capacity ratio','The heat capacity ratio or adiabatic index or ratio of specific heats or Poisson constant, is the ratio of the heat capacity at constant pressure (C_P) to heat capacity at constant volume (C_V).',NULL,'http://vocabulary.odm2.org/unitstype/heatCapacityRatio');
INSERT INTO "CV_UnitsType" VALUES('areaPerLengthDensity','Area per length density','A type of Linear Density.','LinearDenisty','http://vocabulary.odm2.org/unitstype/areaPerLengthDensity');
INSERT INTO "CV_UnitsType" VALUES('absorptionCoefficient','Absorption coefficient','The absorption coefficient, or attenuation coefficient, is a quantity that characterizes how easily a material or medium can be penetrated by a beam of light, sound, particles, or other energy or matter. The attenuation coefficient is the reciprocal of the penetration depth, and is measured in units of reciprocal length. It is also sometimes refered to as specific absorbance or extinction coeffient. ',NULL,'http://vocabulary.odm2.org/unitstype/absorptionCoefficient');
INSERT INTO "CV_UnitsType" VALUES('angularAcceleration','Angular acceleration','Angular acceleration is the rate of change of angular velocity over time. Measurement of the change made in the rate of change of an angle that a spinning object undergoes per unit time. It is a vector quantity. Also called Rotational acceleration. In SI units, it is measured in radians per second squared (rad/s^2), and is usually denoted by the Greek letter alpha.','Acceleration','http://vocabulary.odm2.org/unitstype/angularAcceleration');
INSERT INTO "CV_UnitsType" VALUES('absorbedDoseRate','Absorbed dose rate','Absorbed dose per unit time.',NULL,'http://vocabulary.odm2.org/unitstype/absorbedDoseRate');
INSERT INTO "CV_UnitsType" VALUES('salinity','Salinity','Salinity is the saltiness or dissolved salt content of a body of water. Salinity is an important factor in determining many aspects of the chemistryof natural waters and of biological processes within it, and is a thermodynamic state variable that, along with temperature and pressure, governs physical characteristics like the density and heat capacity of the water. The use of electrical conductivity measurements to estimate the ionic content of seawater led to the development of the so-called practical salinity scale 1978 (PSS-78). Salinities measured using PSS-78 do not have units. The ''unit'' of PSU (denoting practical salinity unit) is sometimes added to PSS-78 measurements, however this is officially discouraged.','Dimensionless','http://vocabulary.odm2.org/unitstype/salinity');
INSERT INTO "CV_UnitsType" VALUES('concentrationMassPerVolume','Concentration mass per volume','A gram per litre or gram per liter (g/L or g/l) is a unit of measurement of mass concentration that shows how many grams of a certain substance are present in one litre of a usually liquid or gaseous mixture. It is not an SI unit because it contains the non-SI unit litre. The SI unit of mass concentration is kilogram per cubic metre, which is equivalent (1 g/L = 1 kg/m3).','Concentration','http://vocabulary.odm2.org/unitstype/concentrationMassPerVolume');
INSERT INTO "CV_UnitsType" VALUES('volumeThermalExpansion','Volume thermal expansion','When the temperature of a substance changes, the energy that is stored in the intermolecular bonds between atoms changes. When the stored energy increases, so does the length of the molecular bonds. As a result, solids typically expand in response to heating and contract on cooling; this dimensional response to temperature change is expressed by its coefficient of thermal expansion. Different coefficients of thermal expansion can be defined for a substance depending on whether the expansion is measured by: * linear thermal expansion * area thermal expansion * volumetric thermal expansion These characteristics are closely related. The volumetric thermal expansion coefficient can be defined for both liquids and solids. The linear thermal expansion can only be defined for solids, and is common in engineering applications. Some substances expand when cooled, such as freezing water, so they have negative thermal expansion coefficients.',NULL,'http://vocabulary.odm2.org/unitstype/volumeThermalExpansion');
INSERT INTO "CV_UnitsType" VALUES('inverseVolume','Inverse volume','Inverse Volume',NULL,'http://vocabulary.odm2.org/unitstype/inverseVolume');
INSERT INTO "CV_UnitsType" VALUES('solidAngle','Solid angle','The solid angle subtended by a surface S is defined as the surface area of a unit sphere covered by the surface S''s projection onto the sphere. A solid angle is related to the surface of a sphere in the same way an ordinary angle is related to the circumference of a circle. Since the total surface area of the unit sphere is 4*pi, the measure of solid angle will always be between 0 and 4*pi.','Angle','http://vocabulary.odm2.org/unitstype/solidAngle');
INSERT INTO "CV_UnitsType" VALUES('electricChargeLineDensity','Electric charge line density',NULL,'LinearDenisty','http://vocabulary.odm2.org/unitstype/electricChargeLineDensity');
INSERT INTO "CV_UnitsType" VALUES('luminance','Luminance','Luminance is a photometric measure of the luminous intensity per unit area of light travelling in a given direction. It describes the amount of light that passes through or is emitted from a particular area, and falls within a given solid angle.',NULL,'http://vocabulary.odm2.org/unitstype/luminance');
INSERT INTO "CV_UnitsType" VALUES('electricCurrentPerAngle','Electric current per angle',NULL,'Density','http://vocabulary.odm2.org/unitstype/electricCurrentPerAngle');
INSERT INTO "CV_UnitsType" VALUES('arealFlux','Areal flux','Rate of flow of a property per unit area.',NULL,'http://vocabulary.odm2.org/unitstype/arealFlux');
INSERT INTO "CV_UnitsType" VALUES('energy','Energy',NULL,NULL,'http://vocabulary.odm2.org/unitstype/energy');
INSERT INTO "CV_UnitsType" VALUES('force','Force','Force is an influence that causes mass to accelerate. It may be experienced as a lift, a push, or a pull. Force is defined by Newton''s Second Law as F = m  a, where F is force, m is mass and a is acceleration. Net force is mathematically equal to the time rate of change of the momentum of the body on which it acts. Since momentum is a vector quantity (has both a magnitude and direction), force also is a vector quantity.',NULL,'http://vocabulary.odm2.org/unitstype/force');
INSERT INTO "CV_UnitsType" VALUES('action','Action','In physics, action is an attribute of the dynamics of a physical system. It is a mathematical functional which takes the trajectory, also called path or history, of the system as its argument and has a real number as its result. Generally, the action takes different values for different paths. Action has the dimensions of [energy][time], and its SI unit is joule-second. This is the same unit as that of angular momentum.',NULL,'http://vocabulary.odm2.org/unitstype/action');
INSERT INTO "CV_UnitsType" VALUES('electricDipoleMoment','Electric dipole moment','In physics, the electric dipole moment is a measure of the separation of positive and negative electrical charges in a system of electric charges, that is, a measure of the charge system''s overall polarity. The SI units are Coulomb-meter (C m). [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/electricDipoleMoment');
INSERT INTO "CV_UnitsType" VALUES('electricFieldStrength','Electric field strength','The strength of the electric field at a given point is defined as the force that would be exerted on a positive test charge of +1 coulomb placed at that point; the direction of the field is given by the direction of that force. Electric fields contain electrical energy with energy density proportional to the square of the field intensity. The electric field is to charge as gravitational acceleration is to mass and force density is to volume.',NULL,'http://vocabulary.odm2.org/unitstype/electricFieldStrength');
INSERT INTO "CV_UnitsType" VALUES('catalyticActivity','Catalytic activity','Catalytic activity is usually denoted by the symbol z and measured in mol/s, a unit which was called katal and defined the SI unit for catalytic activity since 1999. Catalytic activity is not a kind of reaction rate, but a property of the catalyst under certain conditions, in relation to a specific chemical reaction. Catalytic activity of one katal (Symbol 1 kat = 1mol/s) of a catalyst means an amount of that catalyst (substance, in Mol) that leads to a net reaction of one Mol per second of the reactants to the resulting reagents or other outcome which was intended for this chemical reaction. A catalyst may and usually will have different catalytic activity for distinct reactions. [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/catalyticActivity');
INSERT INTO "CV_UnitsType" VALUES('angle','Plane angle','In planar geometry, an angle is the figure formed by two rays, called the sides of the angle, sharing a common endpoint, called the vertex of the angle.','Angle','http://vocabulary.odm2.org/unitstype/angle');
INSERT INTO "CV_UnitsType" VALUES('lengthTemperature','Length temperature',NULL,NULL,'http://vocabulary.odm2.org/unitstype/lengthTemperature');
INSERT INTO "CV_UnitsType" VALUES('mass','Mass','In physics, mass is a property of a physical body which determines the strength of its mutual gravitational attraction to other bodies, its resistance to being accelerated by a force, and in the theory of relativity gives the massenergy content of a system. The SI unit of mass is the kilogram (kg).',NULL,'http://vocabulary.odm2.org/unitstype/mass');
INSERT INTO "CV_UnitsType" VALUES('absorbance','Absorbance','Absorbance is the common logarithm of the ratio of incident to transmitted radiant power through a material. Absorbance is dimensionless, and in particular is not a length, though it is a monotonically increasing function of path length, and approaches zero as the path length approaches zero. See: http://en.wikipedia.org/wiki/Absorbance','Dimensionless','http://vocabulary.odm2.org/unitstype/absorbance');
INSERT INTO "CV_UnitsType" VALUES('massPerLengthUnit','Mass per length unit',NULL,NULL,'http://vocabulary.odm2.org/unitstype/massPerLengthUnit');
INSERT INTO "CV_UnitsType" VALUES('electricalConductance','Electrical conductance','Conductance is the reciprocal of resistance and is different from conductivitiy.  Conductance is the ease with which an electric current passes through a conductor.  The SI unit of electrical resistance is the ohm (), while electrical conductance is measured in siemens (S).  [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/electricalConductance');
INSERT INTO "CV_UnitsType" VALUES('turbidity','Turbidity','Turbidity is the cloudiness or haziness of a fluid, or of air, caused by individual particles (suspended solids) that are generally invisible to the naked eye, similar to smoke in air. Turbidity in open water is often caused by phytoplankton and the measurement of turbidity is a key test of water quality. The higher the turbidity, the higher the risk of the drinkers developing gastrointestinal diseases, especially for immune-compromised people, because contaminants like virus or bacteria can become attached to the suspended solid. The suspended solids interfere with water disinfection with chlorine because the particles act as shields for the virus and bacteria. Similarly suspended solids can protect bacteria from UV sterilisation of water. Fluids can contain suspended solid matter consisting of particles of many different sizes. While some suspended material will be large enough and heavy enough to settle rapidly to the bottom container if a liquid sample is left to stand (the settleable solids), very small particles will settle only very slowly or not at all if the sample is regularly agitated or the particles are colloidal. These small solid particles cause the liquid to appear turbid.','Dimensionless','http://vocabulary.odm2.org/unitstype/turbidity');
INSERT INTO "CV_UnitsType" VALUES('specificVolume','Specific volume','Specific volume () is the volume occupied by a unit of mass of a material. It is equal to the inverse of density.',NULL,'http://vocabulary.odm2.org/unitstype/specificVolume');
INSERT INTO "CV_UnitsType" VALUES('time','Time','Time is a basic component of the measuring system used to sequence events, to compare the durations of events and the intervals between them, and to quantify the motions of objects.',NULL,'http://vocabulary.odm2.org/unitstype/time');
INSERT INTO "CV_UnitsType" VALUES('electricPermittivity','Electric permittivity','In electromagnetism, absolute permittivity is the measure of the resistance that is encountered when forming an electric field in a medium. In other words, permittivity is a measure of how an electric field affects, and is affected by, a dielectric medium. The permittivity of a medium describes how much electric field (more correctly, flux) is ''generated'' per unit charge in that medium. More electric flux exists in a medium with a low permittivity (per unit charge) because of polarization effects. Permittivity is directly related to electric susceptibility, which is a measure of how easily a dielectric polarizes in response to an electric field. Thus, permittivity relates to a material''s ability to resist an electric field and "permit" is a misnomer.  In SI units, permittivity  is measured in farads per meter (F/m)',NULL,'http://vocabulary.odm2.org/unitstype/electricPermittivity');
INSERT INTO "CV_UnitsType" VALUES('energyPerArea','Energy per area','Energy per area density is the amount of energy stored in a given system or region of space per unit area.','Density','http://vocabulary.odm2.org/unitstype/energyPerArea');
INSERT INTO "CV_UnitsType" VALUES('specificHeatCapacity','Specific heat capacity','Heat capacity, or thermal capacity, is the measurable physical quantity of heat energy required to change the temperature of an object by a given amount. Specific heat capacity as an intensive property, the heat capacity is divided by the amount of substance, mass, or volume, so that the quantity is independent of the size or extent of the sample.',NULL,'http://vocabulary.odm2.org/unitstype/specificHeatCapacity');
INSERT INTO "CV_UnitsType" VALUES('massPerAreaUnit','Mass per area unit',NULL,NULL,'http://vocabulary.odm2.org/unitstype/massPerAreaUnit');
INSERT INTO "CV_UnitsType" VALUES('massTemperature','Mass temperature',NULL,NULL,'http://vocabulary.odm2.org/unitstype/massTemperature');
INSERT INTO "CV_UnitsType" VALUES('coefficientOfHeatTransfer','Coefficient of heat transfer','The heat transfer coefficient or film coefficient, in thermodynamics and in mechanics is the proportionality coefficient between the heat flux and the thermodynamic driving force for the flow of heat (i.e., the temperature difference, T)',NULL,'http://vocabulary.odm2.org/unitstype/coefficientOfHeatTransfer');
INSERT INTO "CV_UnitsType" VALUES('forcePerArea','Force per area',NULL,NULL,'http://vocabulary.odm2.org/unitstype/forcePerArea');
INSERT INTO "CV_UnitsType" VALUES('lengthMass','Length mass',NULL,NULL,'http://vocabulary.odm2.org/unitstype/lengthMass');
INSERT INTO "CV_UnitsType" VALUES('specificHeatVolume','Specific heat volume',NULL,NULL,'http://vocabulary.odm2.org/unitstype/specificHeatVolume');
INSERT INTO "CV_UnitsType" VALUES('electricChargePerAmountofSubstance','Electric charge per amount of substance',NULL,NULL,'http://vocabulary.odm2.org/unitstype/electricChargePerAmountofSubstance');
INSERT INTO "CV_UnitsType" VALUES('inductance','Inductance','Inductance is an electromagentic quantity that characterizes a circuit''s resistance to any change of electric current; a change in the electric current through induces an opposing electromotive force (EMF). Quantitatively, inductance is proportional to the magnetic flux per unit of electric current.',NULL,'http://vocabulary.odm2.org/unitstype/inductance');
INSERT INTO "CV_UnitsType" VALUES('volumePerUnitTime','Volume per unit time','Volume Per Unit Time, or Volumetric flow rate, is the volume of fluid that passes through a given surface per unit of time (as opposed to a unit surface).',NULL,'http://vocabulary.odm2.org/unitstype/volumePerUnitTime');
INSERT INTO "CV_UnitsType" VALUES('areaTemperature','Area temperature','Area temperature',NULL,'http://vocabulary.odm2.org/unitstype/areaTemperature');
INSERT INTO "CV_UnitsType" VALUES('radioactivity','Radioactivity','Activity is the term used to characterise the number of nuclei which disintegrate in a radioactive substance per unit time. Activity is usually measured in Becquerels (Bq), where 1 Bq is 1 disintegration per second.',NULL,'http://vocabulary.odm2.org/unitstype/radioactivity');
INSERT INTO "CV_UnitsType" VALUES('angularFrequency','Angular frequency','Angular frequency is a scalar measure of rotation rate. It is the magnitude of the vector quantity angular velocity. ','Frequency','http://vocabulary.odm2.org/unitstype/angularFrequency');
INSERT INTO "CV_UnitsType" VALUES('linearMomentum','Linear momentum','In classical mechanics, linear momentum or translational momentum (pl. momenta; SI unit kg m/s, or equivalently, N s) is the product of the mass and velocity of an object.','Momentum','http://vocabulary.odm2.org/unitstype/linearMomentum');
INSERT INTO "CV_UnitsType" VALUES('inverseAmountOfSubstance','Inverse amount of substance',NULL,NULL,'http://vocabulary.odm2.org/unitstype/inverseAmountOfSubstance');
INSERT INTO "CV_UnitsType" VALUES('electricChargePerArea','Electric charge per area','In electromagnetism, charge density is a measure of electric charge per unit volume of space, in one, two or three dimensions. More specifically: the linear, surface, or volume charge density is the amount of electric charge per unit length, surface area, or volume, respectively. The respective SI units are Cm1, Cm2 or Cm3.','Density','http://vocabulary.odm2.org/unitstype/electricChargePerArea');
INSERT INTO "CV_UnitsType" VALUES('lengthIntegratedMassConcentration','Length integrated mass concentration',NULL,'Concentration','http://vocabulary.odm2.org/unitstype/lengthIntegratedMassConcentration');
INSERT INTO "CV_UnitsType" VALUES('power','Power','Power is the rate at which work is performed or energy is transmitted, or the amount of energy required or expended for a given unit of time. As a rate of change of work done or the energy of a subsystem, power is: P = W/t where P is power W is work t is time.',NULL,'http://vocabulary.odm2.org/unitstype/power');
INSERT INTO "CV_UnitsType" VALUES('color','Color',NULL,'Dimensionless','http://vocabulary.odm2.org/unitstype/color');
INSERT INTO "CV_UnitsType" VALUES('illuminance','Illuminance','Illuminance is the total luminous flux incident on a surface, per unit area. It is a measure of the intensity of the incident light, wavelength-weighted by the luminosity function to correlate with human brightness perception.','LuminousFluxPerArea','http://vocabulary.odm2.org/unitstype/illuminance');
INSERT INTO "CV_UnitsType" VALUES('absorbedDose','Absorbed dose','Absorbed dose (also known as Total Ionizing Dose, TID) is a measure of the energy deposited in a medium by ionizing radiation. It is equal to the energy deposited per unit mass of medium, and so has the unit J/kg, which is given the special name Gray (Gy). Note that the absorbed dose is not a good indicator of the likely biological effect. 1 Gy of alpha radiation would be much more biologically damaging than 1 Gy of photon radiation for example. Appropriate weighting factors can be applied reflecting the different relative biological effects to find the equivalent dose. The risk of stoctic effects due to radiation exposure can be quantified using the effective dose, which is a weighted average of the equivalent dose to each organ depending upon its radiosensitivity. When ionising radiation is used to treat cancer, the doctor will usually prescribe the radiotherapy treatment in Gy. When risk from ionising radiation is being discussed, a related unit, the Sievert is used.','SpecificEnergy','http://vocabulary.odm2.org/unitstype/absorbedDose');
INSERT INTO "CV_UnitsType" VALUES('heatCapacity','Heat capacity','Heat capacity, or thermal capacity, is a measurable physical quantity equal to the ratio of the heat added to (or removed from) an object to the resulting temperature change. The SI unit of heat capacity is joule per kelvin mathrm{	frac{J}{K}} and the dimensional form is L2MT21. Specific heat is the amount of heat needed to raise the temperature of a certain mass 1 degree Celsius.',NULL,'http://vocabulary.odm2.org/unitstype/heatCapacity');
INSERT INTO "CV_UnitsType" VALUES('length','Length',NULL,NULL,'http://vocabulary.odm2.org/unitstype/length');
INSERT INTO "CV_UnitsType" VALUES('angularMass','Angular mass','Moment of Inertia, rotational inertia',NULL,'http://vocabulary.odm2.org/unitstype/angularMass');
INSERT INTO "CV_UnitsType" VALUES('amountOfSubstance','Amount of substance','Amount of substance is a standards-defined quantity that measures the size of an ensemble of elementary entities, such as atoms, molecules, electrons, and other particles. It is a macroscopic property and it is sometimes referred to as chemical amount. The International System of Units (SI) defines the amount of substance to be proportional to the number of elementary entities present. The SI unit for amount of substance is the mole. It has the unit symbol mol.',NULL,'http://vocabulary.odm2.org/unitstype/amountOfSubstance');
INSERT INTO "CV_UnitsType" VALUES('timeSquared','Time squared','Time Squared',NULL,'http://vocabulary.odm2.org/unitstype/timeSquared');
INSERT INTO "CV_UnitsType" VALUES('electricalConductivity','Electrical conductivity','Electrical conductivity or specific conductance is the reciprocal of electrical resistivity, and measures a material''s ability to conduct an electric current. It is commonly represented by the Greek letter  (sigma), but  (kappa) (especially in electrical engineering) or  (gamma) are also occasionally used. Its SI unit is siemens per metre (S/m) and CGSE unit is reciprocal second (s1).  [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/electricalConductivity');
INSERT INTO "CV_UnitsType" VALUES('linearAcceleration','Linear acceleration','Acceleration, in physics, is the rate at which the velocity of an object changes over time. Velocity and acceleration are vector quantities, with magnitude and direction that add according to the parallelogram law. The SI unit for acceleration is the metre per second squared (m/s2).','Acceleration','http://vocabulary.odm2.org/unitstype/linearAcceleration');
INSERT INTO "CV_UnitsType" VALUES('specificHeatPressure','Specific heat pressure',NULL,NULL,'http://vocabulary.odm2.org/unitstype/specificHeatPressure');
INSERT INTO "CV_UnitsType" VALUES('linearVelocity','Linear velocity','Velocity is the rate of change of the position of an object, equivalent to a specification of its speed and direction of motion.Velocity is an important concept in kinematics, the branch of classical mechanics which describes the motion of bodies.Velocity is a vector physical quantity; both magnitude and direction are required to define it. The scalar absolute value (magnitude) of velocity is called "speed", a quantity that is measured in metres per second (m/s or ms1) in the SI (metric) system.','Velocity','http://vocabulary.odm2.org/unitstype/linearVelocity');
INSERT INTO "CV_UnitsType" VALUES('stress','Stress','Stress is a measure of the average amount of force exerted per unit area of a surface within a deformable body on which internal forces act. In other words, it is a measure of the intensity or internal distribution of the total internal forces acting within a deformable body across imaginary surfaces. These internal forces are produced between the particles in the body as a reaction to external forces applied on the body. Pressure is distinct from stress, as the former is the ratio of the component of force normal to a surface to the surface area. Stress is a tensor that relates the vector force to the vector area.The dimension of stress is that of pressure, and therefore its coordinates are commonly measured in the same units as pressure: namely, pascals (Pa, that is, newtons per square metre) in the International System, or pounds per square inch (psi) in the Imperial system.','ForcePerArea','http://vocabulary.odm2.org/unitstype/stress');
INSERT INTO "CV_UnitsType" VALUES('concentrationPercentSaturation','Concentration percent saturation','Ratio of the dissolved concentration of a substance relative to that when completely saturated at the temperature of the measurement.','Concentration','http://vocabulary.odm2.org/unitstype/concentrationPercentSaturation');
INSERT INTO "CV_UnitsType" VALUES('forcePerLength','Force per length',NULL,NULL,'http://vocabulary.odm2.org/unitstype/forcePerLength');
INSERT INTO "CV_UnitsType" VALUES('thermalResistivity','Thermal resistivity','The reciprocal of thermal conductivity is thermal resistivity, measured in kelvin-metres per watt (K*m/W). Also called Specific Thermal Resistance.',NULL,'http://vocabulary.odm2.org/unitstype/thermalResistivity');
INSERT INTO "CV_UnitsType" VALUES('angularVelocity','Angular velocity','The change of angle per unit time; specifically, in celestial mechanics, the change in angle of the radius vector per unit time.','Velocity','http://vocabulary.odm2.org/unitstype/angularVelocity');
INSERT INTO "CV_UnitsType" VALUES('waveNumber','Wave number','In the physical sciences, the wavenumber (also wave number) is the spatial frequency of a wave, either in cycles per unit distance or radians per unit distance. It can be envisaged as the number of waves that exist over a specified distance (analogous to frequency being the number of cycles or radians per unit time).Because of the use of this term in applied physics, including spectroscopy, often the reference distance should be assumed to be cm.',NULL,'http://vocabulary.odm2.org/unitstype/waveNumber');
INSERT INTO "CV_UnitsType" VALUES('electricChargeVolumeDensity','Electric charge volume density','In electromagnetism, charge density is a measure of electric charge per unit volume of space, in one, two or three dimensions. More specifically: the linear, surface, or volume charge density is the amount of electric charge per unit length, surface area, or volume, respectively. The respective SI units are Cm1, Cm2 or Cm3.','Density','http://vocabulary.odm2.org/unitstype/electricChargeVolumeDensity');
INSERT INTO "CV_UnitsType" VALUES('thermalConductivity','Thermal conductivity','In physics, thermal conductivity (often denoted k, , or ) is the property of a material to conduct heat. Thermal conductivity of materials is temperature dependent. The reciprocal of thermal conductivity is called thermal resistivity.',NULL,'http://vocabulary.odm2.org/unitstype/thermalConductivity');
INSERT INTO "CV_UnitsType" VALUES('concentrationVolumePerVolume','Concentration volume per volume','The volume of one substance per unit volume of another substance. Concentration impliles the amount of one substance/item within another substance.','Concentration','http://vocabulary.odm2.org/unitstype/concentrationVolumePerVolume');
INSERT INTO "CV_UnitsType" VALUES('temperature','Temperature','A temperature is a numerical measure of hot and cold. Its measurement is by detection of heat radiation or particle velocity or kinetic energy, or by the bulk behavior of a thermometric material. It may be calibrated in any of various temperature scales, Celsius, Fahrenheit, Kelvin, etc. The fundamental physical definition of temperature is provided by thermodynamics.',NULL,'http://vocabulary.odm2.org/unitstype/temperature');
INSERT INTO "CV_UnitsType" VALUES('dimensionless','Dimensionless','Any unit or combination of units that has no dimensions',NULL,'http://vocabulary.odm2.org/unitstype/dimensionless');
INSERT INTO "CV_UnitsType" VALUES('massPerTimeUnit','Mass per time unit',NULL,NULL,'http://vocabulary.odm2.org/unitstype/massPerTimeUnit');
INSERT INTO "CV_UnitsType" VALUES('electricFlux','Electric flux','The Electric Flux through an area is defined as the electric field multiplied by the area of the surface projected in a plane perpendicular to the field. Electric Flux is a scalar-valued quantity.',NULL,'http://vocabulary.odm2.org/unitstype/electricFlux');
INSERT INTO "CV_UnitsType" VALUES('densityMassPerVolume','Density mass per volume','The density, or more precisely, the volumetric mass density, of a substance is its mass per unit volume. The symbol most often used for density is  (the lower case Greek letter rho). The word density usually refers to the amount of something within a fixed amount of space.  Distinct from concentration in that it does not imply 2 different substances.','Density','http://vocabulary.odm2.org/unitstype/densityMassPerVolume');
INSERT INTO "CV_UnitsType" VALUES('electricCurrent','Electric current','An electric current is a flow of electric charge. In electric circuits this charge is often carried by moving electrons in a wire. It can also be carried by ions in an electrolyte, or by both ions and electrons such as in a plasma.  The SI unit for measuring an electric current is the ampere, which is the flow of electric charge across a surface at the rate of one coulomb per second. [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/electricCurrent');
INSERT INTO "CV_UnitsType" VALUES('electricCurrentDensity','Electric current density','Electric current density is a measure of the density of flow of electric charge; it is the electric current per unit area of cross section. Electric current density is a vector-valued quantity.','Density','http://vocabulary.odm2.org/unitstype/electricCurrentDensity');
INSERT INTO "CV_UnitsType" VALUES('dryVolume','Dry volume','Dry measures are units of volume used to measure bulk commodities which are not gas or liquid. They are often confused or conflated with units of mass, assuming a nominal density, and indeed many units nominally of dry measure have become standardized as units of mass (see bushel)','Volume','http://vocabulary.odm2.org/unitstype/dryVolume');
INSERT INTO "CV_UnitsType" VALUES('electromotiveForce','Electromotive force','In physics, electromotive force, or most commonly emf (seldom capitalized), voltage, or (occasionally) electromotance is "that which tends to cause current (actual electrons and ions) to flow.". More formally, emf is the external work expended per unit of charge to produce an electric potential difference across two open-circuited terminals. The electric potential difference is created by separating positive and negative charges, thereby generating an electric field. The created electrical potential difference drives current flow if a circuit is attached to the source of emf. When current flows, however, the voltage across the terminals of the source of emf is no longer the open-circuit value, due to voltage drops inside the device due to its internal resistance.','ElectricChargePerArea','http://vocabulary.odm2.org/unitstype/electromotiveForce');
INSERT INTO "CV_UnitsType" VALUES('luminousIntensity','Luminous intensity','Luminous Intensity is a measure of the wavelength-weighted power emitted by a light source in a particular direction per unit solid angle. The weighting is determined by the luminosity function, a standardized model of the sensitivity of the human eye to different wavelengths.',NULL,'http://vocabulary.odm2.org/unitstype/luminousIntensity');
INSERT INTO "CV_UnitsType" VALUES('forcePerElectricCharge','Force per electric charge',NULL,NULL,'http://vocabulary.odm2.org/unitstype/forcePerElectricCharge');
INSERT INTO "CV_UnitsType" VALUES('frequency','Frequency','Frequency is the number of occurrences of a repeating event per unit time. The repetition of the events may be periodic (i.e. the length of time between event repetitions is fixed) or aperiodic (i.e. the length of time between event repetitions varies). Therefore, we distinguish between periodic and aperiodic frequencies. In the SI system, periodic frequency is measured in hertz (Hz) or multiples of hertz, while aperiodic frequency is measured in becquerel (Bq).',NULL,'http://vocabulary.odm2.org/unitstype/frequency');
INSERT INTO "CV_UnitsType" VALUES('concentrationCountPerMass','Concentration count per mass','Amount of substance or a count/number of items per unit mass. Concentration impliles the amount of one substance/item within another substance.','Concentration','http://vocabulary.odm2.org/unitstype/concentrationCountPerMass');
INSERT INTO "CV_UnitsType" VALUES('kinematicViscosity','Kinematic viscosity','The Kinematic Viscosity of a fluid is the dynamic viscosity divided by the fluid density.','AreaPerTime','http://vocabulary.odm2.org/unitstype/kinematicViscosity');
INSERT INTO "CV_UnitsType" VALUES('thermalDiffusivity','Thermal diffusivity','In heat transfer analysis, thermal diffusivity (usually denoted  but a, , and D are also used) is the thermal conductivity divided by density and specific heat capacity at constant pressure. It measures the ability of a material to conduct thermal energy relative to its ability to store thermal energy. It has the SI unit of m/s. The formula is:where is thermal conductivity (W/(mK)) is density (kg/m) is specific heat capacity (J/(kgK))Together, can be considered the volumetric heat capacity (J/(mK)).',NULL,'http://vocabulary.odm2.org/unitstype/thermalDiffusivity');
INSERT INTO "CV_UnitsType" VALUES('torque','Torque','In physics, a torque () is a vector that measures the tendency of a force to rotate an object about some axis. The magnitude of a torque is defined as force times its lever arm. Just as a force is a push or a pull, a torque can be thought of as a twist. The SI unit for torque is newton meters (N m). In U.S. customary units, it is measured in foot pounds (ft lbf) (also known as ''pounds feet''). Mathematically, the torque on a particle (which has the position r in some reference frame) can be defined as the cross product:  = r x F where r is the particle''s position vector relative to the fulcrum F is the force acting on the particles, or, more generally, torque can be defined as the rate of change of angular momentum,  = dL/dt where L is the angular momentum vector t stands for time.',NULL,'http://vocabulary.odm2.org/unitstype/torque');
INSERT INTO "CV_UnitsType" VALUES('dynamicViscosity','Dynamic viscosity','The dynamic (shear) viscosity of a fluid expresses its resistance to shearing flows, where adjacent layers move parallel to each other with different speeds. Both the physical unit of dynamic viscosity in SI Poiseuille (Pl) and the cgs units Poise (P) come from Jean Lonard Marie Poiseuille. The poiseuille, which is never used, is equivalent to the pascal-second (Pas), or (Ns)/m2, or kg/(ms).','Viscosity','http://vocabulary.odm2.org/unitstype/dynamicViscosity');
INSERT INTO "CV_UnitsType" VALUES('electricalResistance','Electrical resistance','Electrical resistance is a ratio of the degree to which an object opposes an electric current through it, measured in ohms. Its reciprocal quantity is electrical conductance measured in siemens.',NULL,'http://vocabulary.odm2.org/unitstype/electricalResistance');
INSERT INTO "CV_UnitsType" VALUES('luminousFlux','Luminous flux','Luminous Flux or Luminous Power is the measure of the perceived power of light. It differs from radiant flux, the measure of the total power of light emitted, in that luminous flux is adjusted to reflect the varying sensitivity of the human eye to different wavelengths of light.',NULL,'http://vocabulary.odm2.org/unitstype/luminousFlux');
INSERT INTO "CV_UnitsType" VALUES('concentrationVolumePerMass','Concentration volume per mass','mL of gas per kg of water','Concentration','http://vocabulary.odm2.org/unitstype/concentrationVolumePerMass');
INSERT INTO "CV_UnitsType" VALUES('massFraction','Mass fraction','In chemistry, the mass fraction is the ratio of one substance with mass to the mass of the total mixture , defined asThe sum of all the mass fractions is equal to 1:Mass fraction can also be expressed, with a denominator of 100, as percentage by weight (wt%). It is one way of expressing the composition of a mixture in a dimensionless size; mole fraction (percentage by moles, mol%) and volume fraction (percentage by volume, vol%) are others. For elemental analysis, mass fraction (or "mass percent composition") can also refer to the ratio of the mass of one element to the total mass of a compound. It can be calculated for any compound using its empirical formula. or its chemical formula','Concentration','http://vocabulary.odm2.org/unitstype/massFraction');
INSERT INTO "CV_UnitsType" VALUES('concentrationCountPerVolume','Concentration count per volume','Amount of substance or a count/number of items per unit volume. Concentration impliles the amount of one substance/item within another substance.','Concentration','http://vocabulary.odm2.org/unitstype/concentrationCountPerVolume');
INSERT INTO "CV_UnitsType" VALUES('electricResistivity','Electrical resistivity','Electrical resistivity (also known as resistivity, specific electrical resistance, or volume resistivity) is an intrinsic property that quantifies how strongly a given material opposes the flow of electric current. A low resistivity indicates a material that readily allows the movement of electric charge. Resistivity is commonly represented by the Greek letter  (rho). The SI unit of electrical resistivity is the ohmmetre (m) although other units like ohmcentimetre (cm) are also in use. [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/electricResistivity');
INSERT INTO "CV_UnitsType" VALUES('linearThermalExpansion','Linear thermal expansion','When the temperature of a substance changes, the energy that is stored in the intermolecular bonds between atoms changes. When the stored energy increases, so does the length of the molecular bonds. As a result, solids typically expand in response to heating and contract on cooling; this dimensional response to temperature change is expressed by its coefficient of thermal expansion. Different coefficients of thermal expansion can be defined for a substance depending on whether the expansion is measured by: * linear thermal expansion * area thermal expansion * volumetric thermal expansion These characteristics are closely related. The volumetric thermal expansion coefficient can be defined for both liquids and solids. The linear thermal expansion can only be defined for solids, and is common in engineering applications. Some substances expand when cooled, such as freezing water, so they have negative thermal expansion coefficients. [Wikipedia]',NULL,'http://vocabulary.odm2.org/unitstype/linearThermalExpansion');
CREATE TABLE CV_VariableName (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
CREATE TABLE CV_VariableType (
	Term VARCHAR (255)  NOT NULL,
	Name VARCHAR (255)  NOT NULL PRIMARY KEY,
	Definition VARCHAR (1000)  NULL,
	Category VARCHAR (255)  NULL,
	SourceVocabularyURI VARCHAR (255)  NULL
);
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
