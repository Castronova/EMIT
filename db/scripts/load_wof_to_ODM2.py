# -----------------------------------------------------------------------
# Summary: Load data from a WaterML 1.1 file into an ODM2 SQLite database
# Created by: Jeff Horsburgh
# Created on: 11-13-2014
# Modified on: 6-5-2015 to retrieve temperature data for the Little Bear River
#
# Requirements:
# 1.  Expects a blank ODM2 SQLite database called ODM2.sqlite in the same
#     directory as this script
# 2.  Expects a WSDL URL for a WaterOneFlow web service that can deliver
#     WaterML 1.1 responses
# 3.  Requires NetworkCode, SiteCode, VariableCode, BeginDate and
#     EndDate for the web service call
#
# Outputs:
# 1.  Loads data into the input ODM2.sqlite database
#
# NOTE: WaterML 1.1 does not have all of the information needed to
#       populate the ODM2 database. I have made notes below where that
#       is the case.
# NOTE: The testing dataset I used didn't have any qualifiers and so
#       code would need to be added to handle these as ODM2 annotations
# ---------------------------------------------------------------------
from suds.client import Client
import sqlite3
import uuid
import datetime
import time
import os

# Can turn on logging of the suds client if needed
#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)


def load_wof(dbpath):
    # dbpath = os.path.abspath('odm2.sqlite')


    # Set the URL to the web service URL
    # ----------------------------------
    # url = 'http://data.iutahepscor.org/LittleBearRiverWOF/cuahsi_1_1.asmx?WSDL'
    url = 'http://data.iutahepscor.org/loganriverwof/cuahsi_1_1.asmx?WSDL'
    # url = 'http://data.iutahepscor.org/redbuttecreekwof/cuahsi_1_1.asmx?WSDL'  # Alternative WOF 1.1 URL
    # url = 'http://data.iutahepscor.org/provoriverwof/cuahsi_1_1.asmx?WSDL'  # Alternative WOF 1.1 URL
    client = Client(url)


    # Get DataValues for a Site and Variable (a time series)
    # ------------------------------------------------------
    # Set the parameters for the web service call
    # networkCode = 'LBR'
    # siteCode = 'USU-LBR-Mendon'
    # variableCode = 'USU36:methodCode=28:qualityControlLevelCode=1'
    # beginDate = '2005-01-01'
    # endDate = '2016-01-01'

    networkCode = 'iutah'
    siteCode = 'LR_WaterLab_AA'
    variableCode = 'ODO'
    # variableCode = 'Level_event'
    beginDate = '2014-11-10'  # Alternative beginDate for a shorter request
    endDate = '2015-01-01'  # Alternative endDate for a shorter request
    # beginDate = '2013-01-01'
    # endDate = '2015-01-01'
    print 'Retrieving data values...'
    # vars = client.service.GetVariables()
    # import xml.dom.minidom
    # xml = xml.dom.minidom.parseString(vars)
    # print xml.toprettyxml()
    valuesResult = client.service.GetValuesObject(networkCode + ':' + siteCode , \
                                                  networkCode + ':' + variableCode, \
                                                  beginDate, \
                                                  endDate,)

    # Create the connection to the SQLite database and get a cursor
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    # Get the SamplingFeatureInformation and load it into the database
    # ----------------------------------------------------------------
    print 'Loading SamplingFeature information'
    # WaterML 1.1 ----> ODM2 Mapping for SamplingFeature Information
    # SamplingFeatureID = Automatically generated by SQlite as autoincrement
    # SamplingFeatureUUID = Use python UUID to generate a UUID
    # SamplingFeatureTypeCV = 'Site'
    # SamplingFeatureCode = WaterML siteCode
    # SamplingFeatureName = WaterML siteName
    # SamplingFeatureDescription = NULL (doesn't exist in WaterML 1.1)
    # SamplingFeatureGeotypeCV = 'Point'
    # FeatureGeometry = String Well Known Text representation of point using WaterML latitude and longitude
    # Elevation_m = WaterML elevation_m
    # ElevationDatumCV = WaterML verticalDatum
    samplingFeatureInfo = (str(uuid.uuid1()),
                           'Site',
                           valuesResult.timeSeries[0].sourceInfo.siteCode[0].value,
                           valuesResult.timeSeries[0].sourceInfo.siteName,
                           'Point',
                           'POINT (' + str(valuesResult.timeSeries[0].sourceInfo.geoLocation.geogLocation.latitude) + ' ' + str(valuesResult.timeSeries[0].sourceInfo.geoLocation.geogLocation.longitude) + ')',
                           valuesResult.timeSeries[0].sourceInfo.elevation_m,
                           valuesResult.timeSeries[0].sourceInfo.verticalDatum)

    c.execute('INSERT INTO SamplingFeatures (SamplingFeatureID, SamplingFeatureUUID, '
              'SamplingFeatureTypeCV, SamplingFeatureCode, SamplingFeatureName, SamplingFeatureDescription,'
              'SamplingFeatureGeotypeCV, FeatureGeometry, '
              'Elevation_m, ElevationDatumCV) VALUES (NULL,?,?,?,?,NULL,?,?,?,?)', samplingFeatureInfo)

    # Get the ID of the SamplingFeature I just created
    samplingFeatureID = c.lastrowid



    # Get the Site information and load it into the database
    # ----------------------------------------------------------------
    print 'Loading Site information'
    # The WaterML 1.1 response doesn't have the spatial reference for the latitude and longitude
    # Insert a record into SpatialReferences to indicate that it is unknown
    spatialReferenceInfo = ('Unknown', 'The spatial reference is unknown')

    c.execute('INSERT INTO SpatialReferences(SpatialReferenceID, SRSCode, SRSName, SRSDescription, SRSLink) '
              'VALUES (NULL, NULL, ?, ?, NULL)', spatialReferenceInfo)

    #Get the ID of the SpatialReference I just created
    spatialReferenceID = c.lastrowid

    # WaterML 1.1 ----> ODM2 Mapping for Site Information
    # SamplingFeatureID = SamplingFeatureID of the record just loaded into the SamplingFeatures table
    # SiteTypeCV = Set to the WaterML SiteType property value for the site
    # Latitude = WaterML latitude
    # Longitude = WaterML longitude
    # SpatialReferenceID = SpatialReferenceID of the record just loaded into the SpatialReferences table
    siteInfo = (samplingFeatureID,
                valuesResult.timeSeries[0].sourceInfo.siteProperty[3].value,
                valuesResult.timeSeries[0].sourceInfo.geoLocation.geogLocation.latitude,
                valuesResult.timeSeries[0].sourceInfo.geoLocation.geogLocation.longitude,
                spatialReferenceID)

    c.execute('INSERT INTO Sites(SamplingFeatureID, SiteTypeCV, Latitude, Longitude, SpatialReferenceID) '
              'VALUES (?, ?, ?, ?, ?)', siteInfo)

    # Get the Method information and load it into the database
    # ----------------------------------------------------------------
    print 'Loading Method information'
    # NOTE:  Some hard coded stuff here - MethodCode, MethodTypeCV, and MethodDescription don't exist in
    #        WaterML
    # WaterML 1.1 ----> ODM2 Mapping for Method Information
    # MethodID = Automatically generated by SQLite as autoincrement
    # MethodTypeCV = HARD CODED FOR NOW (Could use generic MethodTypeCV of 'Observation')
    # MethodCode = WaterML methodCode
    # MethodName = Doesn't exist in WaterML, but required. Set this to the WaterML methodDescription
    # MethodDescription = WaterML MethodDescription
    # MethodLink = WaterML methodLink - but not all time series have a MethodLink, so need to fix this
    # OrganizationID = NULL (doesn't exist in WaterML)
    methodInfo = ('Instrument deployment',
                  valuesResult.timeSeries[0].values[0].method[0].methodCode,
                  valuesResult.timeSeries[0].values[0].method[0].methodDescription,
                  valuesResult.timeSeries[0].values[0].method[0].methodDescription)
    #              valuesResult.timeSeries[0].values[0].method[0].methodLink) # Not every time series has a MethodLink

    c.execute('INSERT INTO Methods(MethodID, MethodTypeCV, MethodCode, MethodName, MethodDescription, MethodLink) '
              'VALUES (NULL, ?, ?, ?, ?, NULL)', methodInfo)

    # Get the ID of the Method I just inserted
    methodID = c.lastrowid

    # Get the variable information and load it into the database
    # ----------------------------------------------------------------
    print 'Loading Variable information'
    # WaterML 1.1 ----> ODM2 Mapping for Variable Information
    # VariableID = Automatically generated by SQLite as autoincrement
    # VariableTypeCV = WaterML generalCategory
    # VariableCode = WaterML variableCode
    # VariableNameCV = WaterML variableName
    # VariableDefinition = Set to NULL because it doesn't exist in WaterML and is not required
    # SpeciationCV = WaterML speciation
    # NoDataValue = WaterML noDataValue
    variableInfo = (valuesResult.timeSeries[0].variable.generalCategory,
                    valuesResult.timeSeries[0].variable.variableCode[0].value,
                    valuesResult.timeSeries[0].variable.variableName,
                    valuesResult.timeSeries[0].variable.speciation,
                    valuesResult.timeSeries[0].variable.noDataValue)

    c.execute('INSERT INTO Variables(VariableID, VariableTypeCV, VariableCode, VariableNameCV, VariableDefinition, SpeciationCV, NoDataValue) '
              'VALUES (NULL, ?, ?, ?, NULL, ?, ?)', variableInfo)

    # Get the ID of the Variable I just inserted
    variableID = c.lastrowid

    # Get the Units information and load it into the database
    # ----------------------------------------------------------------
    print 'Loading Variable Units information'
    # WaterML 1.1 ----> ODM2 Mapping for Variable Information
    # UnitsID = WaterML unitCode (this keeps it consistent with the ODM 1.1.1/WaterML 1.1 UnitIDs)
    # UnitsTypeCV = WaterML unitType
    # UnitsAbbreviation = WaterML unitAbbreviation
    # unitsName = WaterML unitName
    # unitsLink = NULL (doesn't exist in WaterML)
    unitsInfo = (valuesResult.timeSeries[0].variable.unit.unitCode,
                 valuesResult.timeSeries[0].variable.unit.unitType,
                 valuesResult.timeSeries[0].variable.unit.unitAbbreviation,
                 valuesResult.timeSeries[0].variable.unit.unitName)

    c.execute('INSERT INTO Units(UnitsID, UnitsTypeCV, UnitsAbbreviation, UnitsName, UnitsLink) '
              'VALUES (?, ?, ?, ?, NULL)', unitsInfo)

    # Get the ID of the Units I just inserted
    unitsID = c.lastrowid

    # Get the ProcessingLevel information and load it into the database
    # -----------------------------------------------------------------
    print 'Loading ProcessingLevel information'
    # WaterML 1.1 ----> ODM2 Mapping for ProcessingLevel Information
    # ProcessingLevelID = WaterML _qualityControlLevelID
    # ProcessingLevelCode = WaterML qualityControlLevelCode
    # Definition = WaterML definition
    # Explanation = WaterML explanation
    processingLevelInfo = (valuesResult.timeSeries[0].values[0].qualityControlLevel[0]._qualityControlLevelID,
                           valuesResult.timeSeries[0].values[0].qualityControlLevel[0].qualityControlLevelCode,
                           valuesResult.timeSeries[0].values[0].qualityControlLevel[0].definition,
                           valuesResult.timeSeries[0].values[0].qualityControlLevel[0].explanation)

    c.execute('INSERT INTO ProcessingLevels(ProcessingLevelID, ProcessingLevelCode, Definition, Explanation) '
              'VALUES (?, ?, ?, ?)', processingLevelInfo)

    # Get the ID of the ProcessingLevel I just inserted
    processingLevelID = c.lastrowid

    # Get the People information and load it
    # -----------------------------------------------------------------
    print 'Loading People information'
    # WaterML 1.1 ----> ODM2 Mapping for People Information
    # PersonID = Automatically generated by SQlite as autoincrement
    # PersonFirstName = First element of WaterML contactName split by space delimiter
    # PersonMiddleName = NULL (this could be problematic if a WaterML person actually has a middle name)
    # PersonLastName = Last element of WaterML contactName split by space delimiter
    splitName = valuesResult.timeSeries[0].values[0].source[0].contactInformation[0].contactName.split(' ')
    personInfo = (splitName[0], splitName[-1])

    c.execute('INSERT INTO People(PersonID, PersonFirstName, PersonLastName) '
              'VALUES (NULL, ?, ?)', personInfo)

    # Get the ID of the person I just inserted
    personID = c.lastrowid

    # Get the Organization information and load it
    # -----------------------------------------------------------------
    print 'Loading Organization information'
    # WaterML 1.1 ----> ODM2 Mapping for Organization Information
    # OrganizationID = Automatically generated by SQlite as autoincrement
    # OrganizationTypeCV = 'Unknown' (doesn't exist in WaterML, but required by ODM2)
    # OrganizationCode = WaterML sourceCode
    # OrganizationName = WaterML organization
    # OrganizationDescription = WaterML sourceDescription
    # OrganizationLink = waterML sourceLink
    # ParentOrganizationID = NULL (doesn't exist in WaterML)
    organizationInfo = ('Unknown',
                        valuesResult.timeSeries[0].values[0].source[0].sourceCode,
                        valuesResult.timeSeries[0].values[0].source[0].organization,
                        valuesResult.timeSeries[0].values[0].source[0].sourceDescription,
                        valuesResult.timeSeries[0].values[0].source[0].sourceLink[0])

    c.execute('INSERT INTO Organizations(OrganizationID, OrganizationTypeCV, OrganizationCode, OrganizationName, OrganizationDescription, OrganizationLink) '
              'VALUES (NULL, ?, ?, ?, ?, ?)', organizationInfo)

    # Get the ID of the Organization I just inserted
    organizationID = c.lastrowid

    # Create the Affiliation between the person and the organization
    # -----------------------------------------------------------------
    print 'Loading Affiliation information'
    # WaterML 1.1 ----> ODM2 Mapping for Affiliation Information
    # AffiliationID = Automatically generated by SQlite as autoincrement
    # PersonID = ID of the person created above
    # OrganizationID = ID of the organization created above
    # IsPrimaryOrganizationContact = 'True' (hard coded for now, doesn't really exist in WaterML)
    # AffilationStartDate = set to the current system date (this is required, but doesn't exit in WaterML)
    # AffiliationEndDate = NULL (this doesn't exist in WaterML but is not required)
    # PrimaryPhone = WaterML phone of source contact
    # PrimaryEmail = WaterML email of source contact
    # PrimaryAddress = NULL (doesn't exist in WaterML)
    # PersonLink = NULL (doesn't exist in WaterML)
    affiliationInfo = (personID,
                       organizationID,
                       'True',
                       datetime.datetime.now(),
                       valuesResult.timeSeries[0].values[0].source[0].contactInformation[0].phone[0],
                       valuesResult.timeSeries[0].values[0].source[0].contactInformation[0].email[0], )

    c.execute('INSERT INTO Affiliations(AffiliationID, PersonID, OrganizationID, IsPrimaryOrganizationContact, AffiliationStartDate, PrimaryPhone, PrimaryEmail) '
              'VALUES (NULL, ?, ?, ?, ?, ?, ?)', affiliationInfo)

    # Get the ID of the Affiliation I just inserted
    affiliationID = c.lastrowid

    # Get the Action information and load it
    # -----------------------------------------------------------------
    print 'Loading Action information'
    # WaterML 1.1 ----> ODM2 Mapping for Action Information
    # ActionID = Automatically generated by SQlite as autoincrement
    # ActionTypeCV = 'Observation' (used the generic term because this doesn't exist in WaterML)
    # MethodID = ID of the Method created above
    # BeginDateTime = WaterML _dateTime of the first data value
    # BeginDateTimeUTCOffset = split hour off of WaterML _timeOffset of the first data value
    # EndDateTime = WaterML _dateTime of the last data value
    # EndDateTimeUTCOffset = split hour off of WaterML _timeOffset of the last data value
    # ActionDescription = 'An observation action that generated a time series result.' (HARD CODED FOR NOW - doesn't exist in WaterML)
    # ActionFileLink = NULL (doesn't exist in WaterML)
    actionInfo = ('Observation',
                  methodID,
                  valuesResult.timeSeries[0].values[0].value[0]._dateTime,
                  int(valuesResult.timeSeries[0].values[0].value[0]._timeOffset.split(':')[0]),
                  valuesResult.timeSeries[0].values[0].value[-1]._dateTime,
                  int(valuesResult.timeSeries[0].values[0].value[-1]._timeOffset.split(':')[0]),
                  'An observation action that generated a time series result.')

    c.execute('INSERT INTO Actions(ActionID, ActionTypeCV, MethodID, BeginDateTime, BeginDateTimeUTCOffset, EndDateTime, EndDateTimeUTCOffset, ActionDescription) '
              'VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)', actionInfo)

    # Get the ID of the Action I just created.
    actionID = c.lastrowid

    # Create the ActionBy information and load it into the database
    # -----------------------------------------------------------------
    print 'Loading ActionBy information'
    # WaterML 1.1 ----> ODM2 Mapping for ActionBy Information
    # BridgeID = Automatically generated by SQlite as autoincrement
    # ActionID = ID of the Action created above
    # AffiliationID = ID of the Affiliation created above
    # IsActionLead = 'True' (doesn't exist in WaterML, so hard coded)
    # RoleDescription = 'Responsible party' (doesn't exist in WaterML, so hard coded)
    actionByInfo = (actionID, affiliationID, 'True', 'Responsible party')

    c.execute('INSERT INTO ActionBy(BridgeID, ActionID, AffiliationID, IsActionLead, RoleDescription) '
              'VALUES (NULL, ?, ?, ?, ?)', actionByInfo)

    # Create the FeatureAction information and load it into the database
    # ------------------------------------------------------------------
    print 'Loading FeatureAction information'
    # WaterML 1.1 ----> ODM2 Mapping for FeatureAction Information
    # FeatureActionID = Automatically generated by SQlite as autoincrement
    # SamplingFeatureID = ID of the SamplingFeature created above
    # ActionID = ID of the Action created above
    featureActionInfo = (samplingFeatureID, actionID)

    c.execute('INSERT INTO FeatureActions(FeatureActionID, SamplingFeatureID, ActionID) '
              'VALUES (NULL, ?, ?)', featureActionInfo)

    # Get the FeatureActionID for the record I just created
    featureActionID = c.lastrowid

    # Create the Result information an load it into the database
    # ------------------------------------------------------------------
    print 'Loading Result information'
    # WaterML 1.1 ----> ODM2 Mapping for Result Information
    # ResultID = Automatically generated by SQlite as autoincrement
    # ResultUUID = Use python UUID to generate a UUID
    # FeatureActionID = ID of the FeatureAction created above
    # ResultTypeCV = 'Time series coverage' (doesn't exist in WaterML, so hard coded)
    # VariableID = ID of Variable created above
    # UnitsID = ID of Units created above
    # TaxonomicClassifierID = NULL (not needed)
    # ProcessingLevelID = ID of ProcessingLevel created above
    # ResultDateTime = current system time (basically the date the data was added to the database)
    # ResultDateTimeUTCOffset = UTCOffset of current system time
    # ValidDateTime = NULL (doesn't exist in WaterML and unknown)
    # ValidDateTImeUTCOffset = NULL (doesn't exist in WaterML and unknown)
    # StatusCV = 'Unknown' (doesn't exist in WaterML - could also be NULL)
    # SampledMediumCV = WaterML sampleMedium
    # ValueCount = python len function length of the WaterML values list
    resultInfo = (str(uuid.uuid1()),
                  featureActionID,
                  'Time series coverage',
                  variableID,
                  unitsID,
                  processingLevelID,
                  datetime.datetime.now(),
                  -time.timezone/3600,
                  'Unknown',
                  valuesResult.timeSeries[0].variable.sampleMedium,
                  len(valuesResult.timeSeries[0].values[0].value))

    c.execute('INSERT INTO Results(ResultID, ResultUUID, FeatureActionID, ResultTypeCV, VariableID, UnitsID, ProcessingLevelID, ResultDateTime, ResultDateTimeUTCOffset, StatusCV, SampledMediumCV, ValueCount) '
              'VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', resultInfo)

    # Get the ID for the Result I just created
    resultID = c.lastrowid

    # Load the Units information for the IntendedTimeSpacing into the database
    # ------------------------------------------------------------------------
    # NOTE: The intended time spacing information isn't in WaterML
    #       This is hard coded and could be problematic for some datasets.
    print 'Loading Units for TimeSupport'
    unitsInfo = (102, 'Time', 'min', 'Minute')

    c.execute('INSERT INTO Units(UnitsID, UnitsTypeCV, UnitsAbbreviation, UnitsName) '
              'VALUES (?, ?, ?, ?)', unitsInfo)

    # Get the ID of the Units I just inserted
    timeUnitsID = c.lastrowid

    # Get the TimeSeriesResult information and load it into the database
    # ------------------------------------------------------------------
    print 'Loading TimeSeriesResult information'
    # NOTE:  The intended time spacing information isn't in WaterML
    # NOTE:  My test dataset didn't have an Offset, so may need to handle that better here
    # WaterML 1.1 ----> ODM2 Mapping for TimeSeriesResult Information
    # XLocation = NULL
    # XLocationUnitsID = NULL
    # YLocation = NULL
    # YLocationUnitsID = NULL
    # ZLocation = NULL
    # ZLocationUnitsID = NULL
    # SpatialReferenceID = NULL
    # IntendedTimeSpacing = 30 (Hard Coded.  I know this for the test dataset, but would have to be null for generic WaterML files because it doesn't exist in WaterML)
    # IntendedTimeSpadingUnitsID = ID of TimeUnits created above (essentially hard coded - I know this for the test dataset, but would have to be null for generic WaterML files because it doesn't exist in WaterML)
    # AggregationStatisticCV = WaterML dataType
    timeSeriesResultInfo = (resultID, 30, timeUnitsID, valuesResult.timeSeries[0].variable.dataType)

    c.execute('INSERT INTO TimeSeriesResults(ResultID, IntendedTimeSpacing, IntendedTimeSpacingUnitsID, AggregationStatisticCV) '
              'VALUES (?, ?, ?, ?)', timeSeriesResultInfo)

    # Get the TimeSeriesResultValues information and load it into the database
    # ------------------------------------------------------------------------
    print 'Loading TimeSeriesResultValues'
    # WaterML 1.1 ----> ODM2 Mapping for TimeSeriesResultValues Information
    # ValueID = Automatically generated by SQLite as autoincrement
    # ResultID = ID of the Result created above
    # DataValue = WaterML value
    # ValueDateTime = WaterML _dateTime
    # ValueDateTimeUTCOffset = split the hour off of the WaterML _timeOffset
    # CensorCodeCV = WaterML _censorCode
    # QualityCodeCV = 'Unknown' (doesn't exist in WaterML, but required)
    # TimeAggregationInterval = WaterML timeSupport
    # TimeAggregationIntervalUnitsID = WaterML timeScale.unit.unitCode
    tsResultValues = []
    numValues = len(valuesResult.timeSeries[0].values[0].value)
    for z in range(0, numValues-1):
        tsResultValues.append((resultID,
                               valuesResult.timeSeries[0].values[0].value[z].value,
                               valuesResult.timeSeries[0].values[0].value[z]._dateTime,
                               int(valuesResult.timeSeries[0].values[0].value[z]._timeOffset.split(':')[0]),
                               valuesResult.timeSeries[0].values[0].value[z]._censorCode,
                               'Unknown',
                               valuesResult.timeSeries[0].variable.timeScale.timeSupport,
                               valuesResult.timeSeries[0].variable.timeScale.unit.unitCode))


    c.executemany('INSERT INTO TimeSeriesResultValues(ValueID, ResultID, DataValue, ValueDateTime, ValueDateTimeUTCOffset, CensorCodeCV, QualityCodeCV, TimeAggregationInterval, TimeAggregationIntervalUnitsID) '
                  'VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)', tsResultValues)

    # Get the TimeSeriesResultValues information and load it into the database
    # ------------------------------------------------------------------------
    print 'Loading DataSet information'
    # NOTE: The WaterML file doesn't have information in it to satisfy many of the Dublin Core elements of the HydroShare
    # Science Metadata. However ODM2 is capable of storing some of this information and so I am going to load it into the
    # database. I have this information because I know this particular data, but it obviously wouldn't be available from
    # other WaterML files
    dataSetInfo = (str(uuid.uuid1()),
                   'HydroShare Time Series Resource',
                   networkCode + ':' + siteCode + ':' + variableCode,
                   'Water temperature in the Little Bear River at Mendon Road near Mendon, UT',
                   'This dataset contains observations of water temperature in '
                   'the Little Bear River at Mendon Road near Mendon, UT. Data were recorded every '
                   '30 minutes. The values were recorded using a HydroLab MS5 multi-parameter water quality '
                   'sonde connected to a Campbell Scientific datalogger. Values represent quality controlled data '
                   'that have undergone quality control to remove obviously bad data.')

    c.execute('INSERT INTO Datasets(DataSetID, DataSetUUID, DataSetTypeCV, DataSetCode, DataSetTitle, DataSetAbstract) '
              'VALUES (NULL, ?, ?, ?, ?, ?)', dataSetInfo)

    # Get the ID of the DataSet record I just inserted
    dataSetID = c.lastrowid

    # Now create the DataSets Results bridge record
    dataSetsResultsInfo = (dataSetID, resultID)
    c.execute('INSERT INTO DataSetsResults(BridgeID, DataSetID, ResultID) Values (NULL, ?, ?)', dataSetsResultsInfo)

    # Save (commit) the changes
    conn.commit()

    # Close the connection to the database
    conn.close()

    print 'Done loading data!'








