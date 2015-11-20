
-------------------
-- create Method --
-------------------

insert into Methods (MethodTypeCV, MethodCode, MethodName, OrganizationID)
values ('Simulation','unknown','Hydrologic Model Simulation',
	(select OrganizationID from Organizations where OrganizationCode = 'uwrl'));

-------------------
-- create Action --
-------------------

 insert  into Actions (ActionTypeCV,MethodID, BeginDateTime, BeginDateTimeUTCOffset, EndDateTime, EndDateTimeUTCOffset)
values ('Simulation',
	(select MethodID from Methods where MethodTypeCV='Simulation'),
	'2012-05-16 15:36:38',-6.00,'2012-05-16 15:40:00',-6.00);

---------------------
-- create Actionby --
---------------------

 insert  into ActionBy (ActionID, AffiliationID,IsActionLead)
values ((select min(ActionID) from Actions),
	(select AffiliationID from Affiliations where PersonID =
		(select PersonID from People where PersonLastName='castronova')),
	'true');

------------------
-- create Units --
------------------

 insert  into Units (UnitsTypeCV,UnitsAbbreviation,UnitsName)
			select 'flow' as 'UnitsTypeCV', 'm^3/s' as 'UnitsAbbreviation', 'cubic meters per second' as UnitsName
union select 'length', 'in', 'international inch'
union select 'flow', 'cfs', 'cubic feet per second'
union select 'length', 'm', 'meter'
union select 'velocity','in/hr','inches per hour'
union select 'time', 's', 'second'
union select 'time','hr', 'hour'
union select 'time','d',  'day'
union select 'time','m',  'minute';

----------------------
-- create Variables --
----------------------

 insert  into Variables (VariableTypeCV,VariableCode,VariableNameCV, VariableDefinition,NoDataValue)
 select 'Model Simulation Result' as VariableTypeCV, 'simflow' as VariableCode,'streamflow' as VariableNameCV,'the volume of water flowing past a fixed point.  equivalent to discharge' as VariableDefinition ,-999 as NoDataValue
union select 'field observation','obsgageheight','gage height',	'water Level with regard to an arbitrary gage datum',-999
union select 'field observation','obsrain','rainfall rate','a measure of the intensity of rainfall, calculated as the depth of water to fall over a given time period if the intensity were to remain constant over that time interval (in/hr, mm/hr, etc)',-999
union select 'field observation','obsstage','water depth',	'water depth is the distance between the water surface and the bottom of the water body at a specific location specified by the site location and offset.',-999;

------------------
-- create Model --
------------------

 insert into Models (ModelName,ModelCode,ModelDescription)
values ('soil and water assessment tool','swat',
	'The Soil and Water Assessment Tool (SWAT) is a public domain Model jointly developed by USDA Agricultural Research Service (USDA-ARS) and Texas A&M AgriLife Research, part of The Texas A&M University System. SWAT is a small watershed to river basin-scale Model to simulate the quality and quantity of surface and ground water and predict the environmental impact of land use, land management practices, and climate change.');

-----------------------
-- create Simulation --
-----------------------

insert  into Simulations (ActionID,SimulationName,SimulationDescription,SimulationStartDateTime,
                         SimulationStartDateTimeUTCOffset,SimulationEndDateTime,SimulationEndDateTimeUTCOffset,
                         TimeStepValue,TimeStepUnitsID,ModelID)
values ((select ActionID from Actions where ActionTypeCV='Simulation'),
	'swat Simulation','swat Simulation for the city of logan, ut',
	'2012-05-16 00:00:00',-6.00,'2012-06-20 00:00:00',-6.00,1,
	(select UnitsID from Units where UnitsTypeCV='time' and UnitsName = 'day'),
	(select ModelID from Models where ModelCode='swat'));

-----------------------------
-- create sampling feature --
-----------------------------

CREATE TEMP TABLE IF NOT EXISTS UUID (Name TEXT PRIMARY KEY, Value TEXT);
INSERT OR REPLACE INTO UUID VALUES
('SF_UUID', (select substr(u,1,8)||'-'||substr(u,9,4)||'-4'||substr(u,13,3)||
  '-'||v||substr(u,17,3)||'-'||substr(u,21,12) from (
    select lower(hex(randomblob(16))) as u, substr('89ab',abs(random()) % 4 + 1, 1) as v)));

insert into SamplingFeatures (SamplingFeatureUUID, SamplingFeatureTypeCV,SamplingFeatureCode,SamplingFeatureName,SamplingFeatureDescription,
									SamplingFeatureGeotypeCV,FeatureGeometry,Elevation_m,ElevationDatumCV)
values ((select Value from UUID where Name = 'SF_UUID'), 'outlet','logan_river_outlet','logan watershed outlet','the outlet of the logan river watershed','point1d',
	ST_GeomFromText('point(111.781944 41.743333)'),
		4680.0, 'epsg:5702');

--------------------------
-- create featureAction --
--------------------------

 insert into FeatureActions(SamplingFeatureID,ActionID)
values ((select SamplingFeatureID from SamplingFeatures where SamplingFeatureCode='logan_river_outlet'),
	(select ActionID from Actions where ActionTypeCV='Simulation'));

-----------------------------
-- create Processing Level --
-----------------------------

 insert into ProcessingLevels(ProcessingLevelCode, Definition, Explanation)
values ('NA','No Processing has been applied because it is not applicable','None');

-------------------
-- create Result --
-------------------

CREATE TEMP TABLE IF NOT EXISTS UUID (Name TEXT PRIMARY KEY, Value TEXT);
INSERT OR REPLACE INTO UUID VALUES
('RES_UUID', (select substr(u,1,8)||'-'||substr(u,9,4)||'-4'||substr(u,13,3)||
  '-'||v||substr(u,17,3)||'-'||substr(u,21,12) from (
    select lower(hex(randomblob(16))) as u, substr('89ab',abs(random()) % 4 + 1, 1) as v)));

insert into Results (ResultUUID,FeatureActionID,ResultTypeCV,VariableID,UnitsID,ProcessingLevelID,
					ResultDateTime,ResultDateTimeUTCOffset,SampledMediumCV,ValueCount)
values ((select Value from UUID where Name = 'RES_UUID'),
	(select FeatureActionID from FeatureActions where SamplingFeatureID =
		(select SamplingFeatureID from SamplingFeatures where SamplingFeatureCode = 'logan_river_outlet')),
	'Time series coverage',
	(select VariableID from Variables where VariableCode = 'simflow'),
	(select UnitsID from Units where UnitsTypeCV = 'flow' and UnitsName='cubic meters per second'),
	(select ProcessingLevelID from ProcessingLevels where ProcessingLevelCode='NA'),
	current_date,-6,'Surface Water',40);

------------------------------
-- create spatial reference --
------------------------------

insert into SpatialReferences (SRSCode, SRSName)
values (4267,'NAD27');

-- -------------------------------
-- -- create time series Result --
-- -------------------------------

insert into TimeSeriesResults (SpatialReferenceID, AggregationStatisticCV)
values ((select SpatialReferenceID from SpatialReferences where SRSName = 'NAD27'),
	'instantaneous');

-----------------------
-- add Result values --
-----------------------

insert into TimeSeriesResultValues (ResultID,DataValue,ValueDateTime,ValueDateTimeUTCOffset,
						CensorCodeCV,QualityCodeCV,TimeAggregationInterval,TimeAggregationIntervalUnitsID )
select (select min(ResultID) from Results) as ResultID, 200 as DataValue, '2013-05-06' as ValueDateTime, -6 as ValueDateTimeUTCOffset,'nc' as CensorCodeCV,'provisional' as QualityCodeCV, 0 as TimeAggregationInterval, (select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day') as TimeAggregationIntervalUnitsID
union select (select min(ResultID) from Results),	214,	'2013-05-07',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	229,	'2013-05-08',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	233,	'2013-05-09',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	265,	'2013-05-10',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	291,	'2013-05-11',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	316,	'2013-05-12',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	358,	'2013-05-13',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	422,	'2013-05-14',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	458,	'2013-05-15',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	478,	'2013-05-16',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	480,	'2013-05-17',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	453,	'2013-05-18',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results), 393,	'2013-05-19',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	367,	'2013-05-20',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	346,	'2013-05-21',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	341,	'2013-05-22',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	347,	'2013-05-23',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	338,	'2013-05-24',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	320,	'2013-05-25',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	322,	'2013-05-26',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	315,	'2013-05-27',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	321,	'2013-05-28',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	317,	'2013-05-29',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	306,	'2013-05-30',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	270,	'2013-05-31',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	254,	'2013-06-01',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	249,	'2013-06-02',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	263,	'2013-06-03',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	265,	'2013-06-04',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	258,	'2013-06-05',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	242,	'2013-06-06',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	243,	'2013-06-07',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	251,	'2013-06-08',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	260,	'2013-06-09',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	256,	'2013-06-10',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	245,	'2013-06-11',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	221,	'2013-06-12',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	208,	'2013-06-13',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	201,	'2013-06-14',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day')
union select (select min(ResultID) from Results),	184,	'2013-06-15',	-6,'nc','provisional',0,(select UnitsID from Units where UnitsTypeCV = 'time' and UnitsName='day');
