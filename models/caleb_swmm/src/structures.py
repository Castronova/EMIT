__author__ = 'tonycastronova'


from ctypes import *



class SWMM_Types():

    GAGE = c_int(0)                            # rain gage
    SUBCATCH = c_int(1)                        ## subcatchment
    NODE = c_int(2)                            ## conveyance system node
    LINK = c_int(3)                            ## conveyance system link

    # POLLUTANT = 5                       #   # pollutant
    # LANDUSE = 6                         ## land use category
    # TIMEPATTERN = 7                     ## dry weather flow time pattern
    # CURVE = 8                           ## generic table of values
    # TSERIES = 9                         ## generic time series of values
    # CONTROL = 10                        # # conveyance system control rules
    # TRANSECT = 11                       # # irregular channel cross-section
    # AQUIFER = 12                        # # groundwater aquifer
    # UNITHYD = 13                        # # RDII unit hydrograph
    # SNOWMELT = 14                       # # snowmelt parameter set
    # SHAPE = 15                          # # custom conduit shape
    # LID = 16                            # # LID treatment units
    # MAX_OBJ_TYPES = 17

class TNode(Structure):
    _fields_ =[
        ("ID", c_char_p),
        ("type", c_int),
        ("subIndex" , c_int),
        ("rptFlag" , c_char),
        ("invertElev" , c_double),
        ("fullDepth" , c_double),         ## dist. from invert to surface (ft),
        ("surDepth" , c_double),        ## added depth under surcharge (ft),
        ("pondedArea" , c_double),     ## area filled by ponded water (ft2),
        ("extInflow"   ,c_void_p),     ## pointer to external inflow data
        ('dwfInflow'    ,c_void_p),    ## pointer to dry weather flow inflow data
        ('rdiiInflow' ,c_void_p),      ## pointer to RDII inflow data
        ('treatment', c_void_p),       ## array of treatment data
        ('degree'   , c_int),       ## number of outflow links
        ('updated'  , c_char),       ## true if state has been updated
        ('crownElev', c_double),      # # top of highest connecting conduit (ft),
        ('inflow'  , c_double),        ## total inflow (cfs),
        ('outflow'  , c_double),       ## total outflow (cfs),
        ('oldVolume' , c_double),      ## previous volume (ft3),
        ('newVolume' , c_double),      ## current volume (ft3),
        ('fullVolume' , c_double),     ## max. storage available (ft3),
        ('overflow'   , c_double),     ## overflow rate (cfs),
        ('oldDepth' , c_double),       ## previous water depth (ft),
        ('newDepth' , c_double),       ## current water depth (ft),
        ('oldLatFlow' , c_double),     ## previous lateral inflow (cfs),
        ('newLatFlow' , c_double),     ## current lateral inflow (cfs),
        ('oldQual'  ,c_void_p),        ## previous quality state
        ('newQual'  ,c_void_p),       ## current quality state
        ('oldFlowInflow' , c_double),  ## previous flow inflow
        ("oldNetInflow", c_double)]   ## previous net inflow

class TSubarea(Structure):
    _fields_ = [
        ('routeTo',c_int),             # code indicating where outflow is sent
        ('fOutlet',c_double ),         # fraction of outflow to outlet
        ('N', c_double),               # Manning's n
        ('fArea', c_double),           # fraction of total area
        ('dStore', c_double),          # depression storage (ft)
        ('alpha', c_double),           # overland flow factor
        ('inflow', c_double),          # inflow rate (ft/sec)
        ('runoff', c_double),          # runoff rate (ft/sec)
        ('depth', c_double)            # depth of surface runoff (ft)
    ]


class TSubcatch(Structure):
    _fields_ = [
    ('ID', c_char_p),              # subcatchment name
    ('rptFlag',c_char ),           # reporting flag
    ('gage', c_int),               # raingage index
    ('outNode',c_int ),            # outlet node index
    ('outSubcatch', c_int),        # outlet subcatchment index
    ('infil',c_int),               # infiltration object index
    ('subArea', TSubarea * 3),     # sub-area data
    ('width', c_double),           # overland flow width (ft)
    ('area', c_double),            # area (ft2)
    ('fracImperv', c_double),      # fraction impervious
    ('slope', c_double),           # slope (ft/ft)
    ('curbLength', c_double),      # total curb length (ft)
    ('initBuildup', c_void_p),     # initial pollutant buildup (mass/ft2)
    ('landFactor', c_void_p),      # array of land use factors
    ('groundwater', c_void_p),     # associated groundwater data
    ('gwFlowExpr', c_void_p),      # user-supplied outflow expression
    ('snowpack', c_void_p),        # associated snow pack data
    ('lidArea', c_double),         # area devoted to LIDs (ft2)
    ('rainfall', c_double),        # current rainfall (ft/sec)
    ('evapLoss', c_double),        # current evap losses (ft/sec)
    ('infilLoss', c_double),       # current infil losses (ft/sec)
    ('runon', c_double),           # runon from other subcatchments (cfs)
    ('oldRunoff', c_double),       # previous runoff (cfs)
    ('newRunoff', c_double),       # current runoff (cfs)
    ('oldSnowDepth', c_double),    # previous snow depth (ft)
    ('newSnowDepth', c_double),    # current snow depth (ft)
    ('oldQual', c_void_p),         # previous runoff quality (mass/L)
    ('newQual',c_void_p ),         # current runoff quality (mass/L)
    ('pondedQual', c_void_p),      # ponded surface water quality (mass)
    ('totalLoad',c_void_p)         # total washoff load (lbs or kg)
]


class POINT(Structure):
    _fields_ = ("x", c_int), ("y", c_int)


class MyStruct(Structure):
    _fields_ = [
    ("a", c_int),
    ("b", c_float),
    ("point_array", POINT * 4)
    ]
#print len(MyStruct().point_array)
# https: #docs.python.org/2/library/ctypes.html


class TLink(Structure):
    _fields_ = [
        ('ID', c_char_p),              # link ID
        ('type', c_int),            # link type code
        ('subIndex', c_int),        # index of link's sub-category
        ('rptFlag', c_char_p),         # reporting flag
        ('node1', c_int),           # start node index
        ('node2', c_int),           # end node index
        ('offset1', c_double),         # ht. above start node invert (ft)
        ('offset2', c_double),         # ht. above end node invert (ft)
        #TXsect        'xsect', ),           # cross section data
        ('q0', c_double),              # initial flow (cfs)
        ('qLimit', c_double),          # constraint on max. flow (cfs)
        ('cLossInlet', c_double),      # inlet loss coeff.
        ('cLossOutlet',c_double ),     # outlet loss coeff.
        ('cLossAvg', c_double),        # avg. loss coeff.
        ('seepRate', c_double),        # seepage rate (ft/sec)
        ('hasFlapGate', c_int),     # true if flap gate present

        ('oldFlow', c_double),         # previous flow rate (cfs)
        ('newFlow', c_double),         # current flow rate (cfs)
        ('oldDepth', c_double),        # previous flow depth (ft)
        ('newDepth', c_double),        # current flow depth (ft)
        ('oldVolume', c_double),       # previous flow volume (ft3)
        ('newVolume', c_double),       # current flow volume (ft3)
        ('surfArea1', c_double),       # upstream surface area (ft2)
        ('surfArea2', c_double),       # downstream surface area (ft2)
        ('qFull', c_double),           # flow when full (cfs)
        ('setting', c_double),         # current control setting
        ('targetSetting', c_double),   # target control setting
        ('froude', c_double),          # Froude number
        ('oldQual', c_double),         # previous quality state
        ('newQual', c_double),         # current quality state
        ('totalLoad', c_double),       # total quality mass loading
        ('flowClass', c_int),       # flow classification
        ('dqdh', c_double),            # change in flow w.r.t. head (ft2/sec)
        ('direction', c_char),       # flow direction flag
        ('bypassed', c_char),        # bypass dynwave calc. flag
        ('normalFlow', c_char),      # normal flow limited flag
        ('inletControl', c_char),    # culvert inlet control flag
    ]

class TXsect(Structure):
    _fields_ = [
        ('type', c_int),            # type code of cross section shape
        ('culvertCode', c_int),     # type of culvert (if any)
        ('transect', c_int),        # index of transect/shape (if applicable)
        ('yFull',c_double ),           # depth when full (ft)
        ('wMax',c_double ),            # width at widest point (ft)
        ('ywMax',c_double ),           # depth at widest point (ft)
        ('aFull',c_double ),           # area when full (ft2)
        ('rFull',c_double ),           # hyd. radius when full (ft)
        ('sFull', c_double),           # section factor when full (ft^4/3)
        ('sMax', c_double),            # section factor at max. flow (ft^4/3)

        # These variables have different meanings depending on section shape
        ('yBot',c_double ),            # depth of bottom section
        ('aBot',c_double ),            # area of bottom section
        ('sBot', c_double),            # slope of bottom section
        ('rBot',c_double ),            # radius of bottom section
    ]


class TFile(Structure):

    _fields_ = [
        ('name', c_char * 260),          # file name
        ('mode',c_char),                 # NO_FILE, SCRATCH, USE, or SAVE
        ('state',c_char),                # current state (OPENED, CLOSED)
        ('file', c_void_p)               # FILE structure pointer, FILE*
 ]


class Project(Structure):

    _fields_ = [
		('J1', c_int ),
		('P1', c_int ),
		('J2', c_int ),
        ('RT', c_double ),


     #    ('Finp', TFile),                      # Input file
	# 	(' Fout',TFile),                      # Output file
	# 	(' Frpt',TFile),                      # Report file
	# 	(' Fclimate',TFile),                  # Climate file
	# 	(' Frain',TFile),                     # Rainfall file
	# 	(' Frunoff',TFile),                   # Runoff file
	# 	(' Frdii',TFile),                     # RDII inflow file
	# 	(' Fhotstart1',TFile),                # Hot start input file
	# 	(' Fhotstart2',TFile),                # Hot start output file
	# 	(' Finflows',TFile),                  # Inflows routing file
	# 	(' Foutflows',TFile ),                # Outflows routing file
    #
    #
     #    ('Nperiods', c_long ),                  # Number of reporting periods
     #    ('StepCount', c_long ),                 # Number of routing steps used
	# 	('NonConvergeCount', c_long),          # Number of non-converging steps
    #
    #
     #    ('Msg',c_char * 1025),             # Text of output message
     #    ('Title', [c_char*4]*1025),           # [MAXTITLE][MAXMSG + 1] ), # Project title
     #    ('TempDir', c_char* 260),       # Temporary file directory
    #
    #
	# 	#TRptFlags RptFlags ),                     # Reporting options
    #
    #
	# 	( 'Nobjects', c_int * 17 ),   # Number of each object type
	# 	( 'Nnodes', c_int * 4 ),    # Number of each node sub-type
	# 	( 'Nlinks', c_int * 5),    # Number of each link sub-type
	# 	( 'UnitSystem' , c_int),                # Unit system
	# 	( 'FlowUnits' , c_int),                 # Flow units
	# 	( 'InfilModel' , c_int),                # Infiltration method
	# 	( 'RouteModel' , c_int),                # Flow routing method
	# 	( 'ForceMainEqn' , c_int),              # Flow equation for force mains
	# 	( 'LinkOffsets', c_int ),               # Link offset convention
	# 	( 'AllowPonding', c_int),              # Allow water to pond at nodes
	# 	( 'InertDamping' , c_int),              # Degree of inertial damping
	# 	( 'NormalFlowLtd' , c_int),             # Normal flow limited
	# 	( 'SlopeWeighting' , c_int),            # Use slope weighting
	# 	( 'Compatibility' , c_int),             # SWMM 5/3/4 compatibility
	# 	( 'SkipSteadyState' , c_int),           # Skip over steady state periods
	# 	( 'IgnoreRainfall' , c_int),            # Ignore rainfall/runoff
	# 	( 'IgnoreRDII' , c_int),                # Ignore RDII                      #(5.1.004)
	# 	( 'IgnoreSnowmelt' , c_int),            # Ignore snowmelt
	# 	( 'IgnoreGwater' , c_int),              # Ignore groundwater
	# 	( 'IgnoreRouting' , c_int),             # Ignore flow routing
	# 	( 'IgnoreQuality' , c_int),             # Ignore water quality
	# 	( 'ErrorCode', c_int ),                 # Error code number
	# 	( 'WarningCode' , c_int),               # Warning code number
	# 	( 'WetStep', c_int ),                   # Runoff wet time step (sec)
	# 	( 'DryStep' , c_int),                   # Runoff dry time step (sec)
	# 	( 'ReportStep' , c_int),                # Reporting time step (sec)
	# 	( 'SweepStart' , c_int),                # Day of year when sweeping starts
	# 	( 'SweepEnd' , c_int),                  # Day of year when sweeping ends
	# 	( 'MaxTrials', c_int ),                 # Max. trials for DW routing
    #
    #
     #    ('RouteStep' ,c_double),                 # Routing time step (sec)
	# 	('LengtheningStep' ,c_double),           # Time step for lengthening (sec)
	# 	('StartDryDays' ,c_double),              # Antecedent dry days
	# 	('CourantFactor' ,c_double),             # Courant time step factor
	# 	('MinSurfArea' ,c_double),               # Minimum nodal surface area
	# 	('MinSlope' ,c_double),                  # Minimum conduit slope
	# 	('RunoffError' ,c_double),               # Runoff continuity error
	# 	('GwaterError' ,c_double),               # Groundwater continuity error
	# 	('FlowError',c_double ),                 # Flow routing error
	# 	('QualError' ,c_double),                 # Quality routing error
	# 	('HeadTol' ,c_double),                   # DW routing head tolerance (ft)
	# 	('SysFlowTol' ,c_double),                # Tolerance for steady system flow
	# 	('LatFlowTol' ,c_double),                # Tolerance for steady nodal inflow
    #
    #
	# 	# DateTime StartDate,  ),                 # Starting date
	# 	# DateTime StartTime ),                 # Starting time
	# 	# DateTime StartDateTime ),             # Starting Date+Time
	# 	# DateTime EndDate ),                   # Ending date
	# 	# DateTime EndTime ),                   # Ending time
	# 	# DateTime EndDateTime ),               # Ending Date+Time
	# 	# DateTime ReportStartDate ),           # Report start date
	# 	# DateTime ReportStartTime ),           # Report start time
	# 	# DateTime ReportStart ),               # Report start Date+Time
    #
    #
	# 	('ReportTime' ,c_double),                # Current reporting time (msec)
	# 	('OldRunoffTime' ,c_double),             # Previous runoff time (msec)
	# 	('NewRunoffTime' ,c_double),             # Current runoff time (msec)
	# 	('OldRoutingTime' ,c_double),            # Previous routing time (msec)
	# 	('NewRoutingTime' ,c_double),            # Current routing time (msec)
	# 	('TotalDuration' ,c_double),             # Simulation duration (msec)
    #
	# 	# TTemp      Temp ),                      # Temperature data
	# 	# TEvap      Evap ),                      # Evaporation data
	# 	# TWind      Wind ),                      # Wind speed data
	# 	# TSnow      Snow ),                      # Snow melt data
	# 	# TSnowmelt* Snowmelt ),                  # Array of snow melt objects
	# 	# TGage*     Gage ),                      # Array of rain gages
	# 	# TSubcatch* Subcatch ),                  # Array of subcatchments
	# 	# TAquifer*  Aquifer ),                   # Array of groundwater aquifers
	# 	# TUnitHyd*  UnitHyd ),                   # Array of unit hydrographs
	# 	# TNode*     Node ),                      # Array of nodes
	# 	# TOutfall*  Outfall ),                   # Array of outfall nodes
	# 	# TDivider*  Divider ),                   # Array of divider nodes
	# 	# TStorage*  Storage ),                   # Array of storage nodes
	# 	# TLink*     Link ),                      # Array of links
	# 	# TConduit*  Conduit ),                   # Array of conduit links
	# 	# TPump*     Pump ),                      # Array of pump links
	# 	# TOrifice*  Orifice ),                   # Array of orifice links
	# 	# TWeir*     Weir ),                      # Array of weir links
	# 	# TOutlet*   Outlet ),                    # Array of outlet device links
	# 	# TPollut*   Pollut ),                    # Array of pollutants
	# 	# TLanduse*  Landuse ),                   # Array of landuses
	# 	# TPattern*  Pattern ),                   # Array of time patterns
	# 	# TTable*    Curve ),                     # Array of curve tables
	# 	# TTable*    Tseries ),                   # Array of time series tables
	# 	# TTransect* Transect ),                  # Array of transect data
	# 	# TShape*    Shape ),                     # Array of custom conduit shapes
    #
	# 	# HTtable* Htable[MAX_OBJ_TYPES] ),  # Hash tables for object ID names
     #    ('MemPoolAllocated', c_char ),       # TRUE if memory pool allocated
    #
    #
	# 	 #-----------------------------------------------------------------------------
	# 	 #  Shared Variables from lid.c
	# 	 #-----------------------------------------------------------------------------
	# 	# TLidProc*  LidProcs ),             # array of LID processes
	# 	('LidCount', c_int ),             # number of LID processes
	# 	# TLidGroup* LidGroups ),            # array of LID process groups
	# 	('GroupCount' , c_int),           # number of LID groups (subcatchments)
    #
     #    ('EvapRate' ,c_double),             # evaporation rate (ft/s)
	# 	('NativeInfil' ,c_double),          # native soil infil. rate (ft/s)
	# 	('MaxNativeInfil' ,c_double),       # native soil infil. rate limit (ft/s)
    #
	# 	('TotalEvapVol' ,c_double),         # subcatch. evap loss (ft3)
	# 	('TotalPervEvapVol' ,c_double),     # evap loss over pervious area (ft3)
	# 	('TotalInfilVol' ,c_double),        # subcatch infiltration loss (ft3)
	# 	('NextReportTime' ,c_double),
	# 	('SaveResults',c_int ),          # = 1 if detailed results to be saved
	# 	 #typedef int (*swmm_retrieve_openmi_items)(int, char*, char* , double* ) ),
	# 	 #
	# 	 #  swmm_retrieve_openmi_items retrieve_openmi_exchangeItems ),
    #
	# 	 #-----------------------------------------------------------------------------
	# 	 #  Local Variables
	# 	 #-----------------------------------------------------------------------------
	# 	 #to do set to null
	# 	# THorton*   HortInfil ),
	# 	# TGrnAmpt*  GAInfil ),
	# 	# TCurveNum* CNInfil ),
    #
    #
	# 	 #-----------------------------------------------------------------------------
	# 	 #  Shared variables controls.c
	# 	 #-----------------------------------------------------------------------------
	# 	# TRule*  Rules ),              # Array of control rules
	# 	# TActionList* ActionList ),         # Linked list of control actions
	# 	('InputState' , c_int),                      # State of rule interpreter
	# 	('RuleCount' , c_int),                       # Total number of rules
     #    ('ControlValue',c_double ),                    # Value of controller variable
     #    ('SetPoint',c_double ),                        # Value of controller setpoint
    #
    #
	# 	 #-----------------------------------------------------------------------------
	# 	 #  Shared variables from  input.c
	# 	 #-----------------------------------------------------------------------------
	# 	#char *Tok[MAXTOKS] ),              # String tokens from line of input
	# 	('Ntokens' , c_int),                    # Number of tokens in line of input
	# 	('Mobjects', c_int *17),    # Working number of objects of each type
	# 	('Mnodes', c_int * 4 ),     # Working number of node objects
	# 	('Mlinks', c_int * 5),     # Working number of link objects
    #
    #
	# 	 #-----------------------------------------------------------------------------
	# 	 #  Shared variables from swmm.c
	# 	 #-----------------------------------------------------------------------------
	# 	('IsOpenFlag' , c_int),            # TRUE if a project has been opened
	# 	('IsStartedFlag', c_int ),         # TRUE if a simulation has been started
	# 	('SaveResultsFlag', c_int ),       # TRUE if output to be saved to binary file
	# 	('ExceptionCount' , c_int),        # number of exceptions handled
	# 	('DoRunoff' , c_int),              # TRUE if runoff is computed
	# 	('DoRouting' , c_int),             # TRUE if flow routing is computed
    #
    #
	# 	 #-----------------------------------------------------------------------------
	# 	 #  Shared variables from climate.c
	# 	 #-----------------------------------------------------------------------------
	# 	 # Temperature variables
     #    ('Tmin' ,c_double),                  # min. daily temperature (deg F)
	# 	    ('Tmax' ,c_double),                  # max. daily temperature (deg F)
	# 	    ('Trng' ,c_double),                  # 1/2 range of daily temperatures
	# 	    ('Trng1' ,c_double),                 # prev. max - current min. temp.
	# 	    ('Tave' ,c_double),                  # average daily temperature (deg F)
	# 	    ('Hrsr' ,c_double),                  # time of min. temp. (hrs)
	# 	    ('Hrss' ,c_double),                  # time of max. temp (hrs)
	# 	    ('Hrday' ,c_double),                 # avg. of min/max temp times
	# 	    ('Dhrdy' ,c_double),                 # hrs. between min. & max. temp. times
	# 	    ('Dydif' ,c_double),                 # hrs. between max. & min. temp. times
	# 	# DateTime  LastDay ,c_double),               # date of last day with temp. data
    #
	# 	 # Evaporation variables
	# 	# DateTime  NextEvapDate ),          # next date when evap. rate changes
	# 	    ('NextEvapRate',c_double ),          # next evaporation rate (user units)
    #
	# 	 # Climate file variables
	# 	(      'FileFormat' , c_int),             # file format (see ClimateFileFormats)
	# 	(      'FileYear', c_int ),               # current year of file data
	# 	(      'FileMonth' , c_int),              # current month of year of file data
	# 	(      'FileDay' , c_int),                # current day of month of file data
	# 	(      'FileLastDay' , c_int),            # last day of current month of file data
	# 	(      'FileElapsedDays' , c_int),        # number of days read from file
	# 	# double   FileValue[4] ,c_double),           # current day's values of climate data
	# 	# double   FileData[4][32],c_double ),        # month's worth of daily climate data
	# 	# char     FileLine[MAXLINE + 1] ),    # line from climate data file
    #
    #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Shared variables
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  NOTE: all flux rates are in ft/sec, all depths are in ft.
	# # 	double    Infil ,c_double),            # infiltration rate from surface
	# # 	double    MaxEvap ,c_double),          # max. evaporation rate
	# # 	double    AvailEvap,c_double ),        # available evaporation rate
	# # 	double    UpperEvap ,c_double),        # evaporation rate from upper GW zone
	# # 	double    LowerEvap ,c_double),        # evaporation rate from lower GW zone
	# # 	double    UpperPerc ,c_double),        # percolation rate from upper to lower zone
	# # 	double    LowerLoss ,c_double),        # loss rate from lower GW zone
	# # 	double    GWFlow ,c_double),           # flow rate from lower zone to conveyance node
	# # 	double    MaxUpperPerc ,c_double),     # upper limit on UpperPerc
	# # 	double    MaxGWFlowPos ,c_double),     # upper limit on GWFlow when its positve
	# # 	double    MaxGWFlowNeg ,c_double),     # upper limit on GWFlow when its negative
	# # 	double    FracPerv ,c_double),         # fraction of surface that is pervious
	# # 	double    TotalDepth ,c_double),       # total depth of GW aquifer
	# # 	double    Hgw ,c_double),              # ht. of saturated zone
	# # 	double    Hstar ,c_double),            # ht. from aquifer bottom to node invert
	# # 	double    Hsw ,c_double),              # ht. from aquifer bottom to water surface
	# # 	double    Tstep,c_double ),            # current time step (sec)
	# # 	TAquifer  A ),                # aquifer being analyzed
	# # 	TGroundwater* GW ),           # groundwater object being analyzed
	# # 	MathExpr* FlowExpr ),         # user-supplied GW flow expression
    # #
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Shared variables from treatment.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	(     ErrCode, c_int ),                 # treatment error code
	# # 	(     J , c_int),                       # index of node being analyzed
	# # 	double  Dt ,c_double),                      # curent time step (sec)
	# # 	double  Q ,c_double),                       # node inflow (cfs)
	# # 	double  V ,c_double),                       # node volume (ft3)
	# # 	( R ,c_double),                       # array of pollut. removals
	# # 	( Cin,c_double ),                     # node inflow concentrations
	# # 	TTreatment* Treatment ),           # pointer to Treatment object
    # #
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Exportable variables (shared with statsrpt.c) from stats.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	TSubcatchStats* SubcatchStats ),
	# # 	TNodeStats*     NodeStats ),
	# # 	TLinkStats*     LinkStats ),
	# # 	TStorageStats*  StorageStats ),
	# # 	TOutfallStats*  OutfallStats ),
	# # 	TPumpStats*     PumpStats ),
	# # 	double          MaxOutfallFlow ,c_double),
	# # 	double          MaxRunoffFlow,c_double),
    # #
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Shared variables   from massbalc.
	# # 	 #-----------------------------------------------------------------------------
	# # 	TRunoffTotals    RunoffTotals ),     # overall surface runoff continuity totals
	# # 	TLoadingTotals*  LoadingTotals ),    # overall WQ washoff continuity totals
	# # 	TGwaterTotals    GwaterTotals ),     # overall groundwater continuity totals
	# # 	TRoutingTotals   FlowTotals ),       # overall routed flow continuity totals
	# # 	TRoutingTotals*  QualTotals ),       # overall routed WQ continuity totals
	# # 	TRoutingTotals   StepFlowTotals ),   # routed flow totals over time step
	# # 	TRoutingTotals   OldStepFlowTotals ),
	# # 	TRoutingTotals*  StepQualTotals ),   # routed WQ totals over time step
    # #
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Imported variables from massbal.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	(  NodeInflow ,c_double),               # total inflow volume to each node (ft3)
	# # 	(  NodeOutflow ,c_double),              # total outflow volume from each node (ft3)
	# # 	(  TotalArea ,c_double),                # total drainage area (ft2)
    # #
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Shared variables from stats.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	TSysStats       SysStats ),
	# # 	TMaxStats       MaxMassBalErrs[MAX_STATS] ),
	# # 	TMaxStats       MaxCourantCrit[MAX_STATS] ),
	# # 	TMaxStats       MaxFlowTurns[MAX_STATS] ),
	# # 	(         SysOutfallFlow ,c_double),
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 # Shared variables   from subcatch.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	(    Losses ,c_double),         # subcatch evap. + infil. loss rate (ft/sec)
	# # 	(    Outflow ,c_double),        # subcatch outflow rate (ft/sec)
    # #
	# # 	 # Volumes as either total (ft3) or per unit area (ft) depending on context
	# # 	(    Vrain ,c_double),          # subcatch rain volume over a time step
	# # 	(    Vevap ,c_double),          # subcatch evap. volume over a time step
	# # 	(    Vinfil,c_double ),         # subcatch infil. volume over a time step
    # #
	# # 	(    Vrunon ,c_double),         # subcatch runon volume over a time step (ft3)
	# # 	(    Vponded ,c_double),        # volume of ponded water over subcatch (ft3)
	# # 	(    Voutflow ,c_double),       # subcatch outflow depth (ft3)
    # #
	# # 	TSubarea* theSubarea ),      # subarea to which getDdDt() is applied
    # #
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Shared variables    from output.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	INT4      IDStartPos ),            # starting file position of ID names
	# # 	INT4      InputStartPos ),         # starting file position of input data
	# # 	INT4      OutputStartPos ),        # starting file position of output data
	# # 	INT4      BytesPerPeriod ),        # bytes saved per simulation time period
	# # 	INT4      NsubcatchResults ),      # number of subcatchment output variables
	# # 	INT4      NnodeResults ),          # number of node output variables
	# # 	INT4      NlinkResults ),          # number of link output variables
	# # 	INT4      NumSubcatch ),           # number of subcatchments reported on
	# # 	INT4      NumNodes ),              # number of nodes reported on
	# # 	INT4      NumLinks ),              # number of links reported on
	# # 	INT4      NumPolluts ),            # number of pollutants reported on
	# # 	REAL4     SysResults[MAX_SYS_RESULTS] ),     # values of system output vars.
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Exportable variables (shared with report.c) from output.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	REAL4*           SubcatchResults ),
	# # 	REAL4*           NodeResults ),
	# # 	REAL4*           LinkResults ),
    # #
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 # Shared variables from runoff.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	char  IsRaining ),                 # TRUE if precip.falls on study area
	# # 	char  HasRunoff ),                 # TRUE if study area generates runoff
	# # 	char  HasSnow ),                   # TRUE if any snow cover on study area
	# # 	(   Nsteps ),                    # number of runoff time steps taken
	# # 	(   MaxSteps ),                  # final number of runoff time steps
	# # 	long  MaxStepsPos ),               # position in Runoff interface file
	# # 	 #    where MaxSteps is saved
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Exportable variables (shared with subcatch.c) from runoff.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	( OutflowLoad,c_double ),          # outflow pollutant mass from a subcatchment
	# # 	( WashoffLoad ,c_double),          # washoff pollutant mass from landuses
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 # Shared Variables from rdii.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	TUHGroup*  UHGroup ),              # processing data for each UH group
	# # 	(        RdiiStep, c_int ),             # RDII time step (sec)
	# # 	(        NumRdiiNodes , c_int),         # number of nodes w/ RDII data
	# # 	(       RdiiNodeIndex,c_int ),        # indexes of nodes w/ RDII data
	# # 	REAL4*     RdiiNodeFlow ),         # inflows for nodes with RDII           #(5.1.003)
	# # 	(        RdiiFlowUnits ),        # RDII flow units code
	# # 	DateTime   RdiiStartDate ),        # start date of RDII inflow period
	# # 	DateTime   RdiiEndDate ),          # end date of RDII inflow period
	# # 	(    TotalRainVol ,c_double),         # total rainfall volume (ft3)
	# # 	(    TotalRdiiVol,c_double ),         # total RDII volume (ft3)
	# # 	(        RdiiFileType , c_int),         # type (binary/text) of RDII file
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Shared variables ifil.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	(      IfaceFlowUnits , c_int),         # flow units for routing interface file
	# # 	(      IfaceStep , c_int),              # interface file time step (sec)
	# # 	(      NumIfacePolluts, c_int ),        # number of pollutants in interface file
	# # 	(     IfacePolluts ,c_int),           # indexes of interface file pollutants
	# # 	(      NumIfaceNodes , c_int),          # number of nodes on interface file
	# # 	(     IfaceNodes ,c_int),             # indexes of nodes on interface file
	# # 	(* OldIfaceValues ,c_double),         # interface flows & WQ at previous time
	# # 	(* NewIfaceValues ,c_double),         # interface flows & WQ at next time
	# # 	(  IfaceFrac ,c_double),              # fraction of interface file time step
	# # 	DateTime OldIfaceDate ),           # previous date of interface values
	# # 	DateTime NewIfaceDate ),           # next date of interface values
    # #
    # #
    # #
	# # 	 #-----------------------------------------------------------------------------
	# # 	 #  Shared variables from transect.c
	# # 	 #-----------------------------------------------------------------------------
	# # 	 (    Ntransects , c_int),               # total number of transects
	# # 	 (    Nstations , c_int),                # number of stations in current transect
	# # 	( Station[MAXSTATION + 1],c_double ),   # x-coordinate of each station
	# # 	( Elev[MAXSTATION + 1] ,c_double),      # elevation of each station
	# # 	( Nleft ,c_double),                   # Manning's n for left overbank
	# # 	( Nright ,c_double),                  # Manning's n for right overbank
	# # 	( Nchannel ,c_double),                # Manning's n for main channel
	# # 	( Xleftbank ,c_double),               # station where left overbank ends
	# # 	( Xrightbank ,c_double),              # station where right overbank begins
	# # 	( Xfactor ,c_double),                 # multiplier for station spacing
	# # 	( Yfactor ,c_double),                 # factor added to station elevations
	# # 	( Lfactor ,c_double),                 # main channel/flood plain length
    # #
    # #
	# # 	  #-----------------------------------------------------------------------------
	# # 	  #  Shared variables
	# # 	  #-----------------------------------------------------------------------------
	# # 	(Atotal,c_double ),
	# # 	(Ptotal,c_double ),
    # #
    # #
	# # 	  #-----------------------------------------------------------------------------
	# # 	  #  Shared variables from kinwave ),c
	# # 	  #-----------------------------------------------------------------------------
	# # 	(  Beta1 ,c_double),
	# # 	(  C1 ,c_double),
	# # 	(  C2 ,c_double),
	# # 	(  Afull ,c_double),
	# # 	(  Qfull ,c_double),
	# # 	 TXsect*  pXsect ),
    # #
	# # 	  #-----------------------------------------------------------------------------
	# # 	  #  Shared Variables from dynwave.c
	# # 	  #-----------------------------------------------------------------------------
	# # 	( VariableStep,c_double ),            # size of variable time step (sec)
	# # 	 TXnode* Xnode ),                   # extended nodal information
	# # 	( Omega,c_double ),                   # actual under-relaxation parameter
	# # 	 (     Steps, c_int ),                   # number of Picard iterations
    # #
	# # 	  #-----------------------------------------------------------------------------
	# # 	  # Shared variables from routing.c
	# # 	  #-----------------------------------------------------------------------------
	# # 	 ( SortedLinks ,c_int),
    # #
	# # 	  #-----------------------------------------------------------------------------
	# # 	  #  Shared variables from toposort.c
	# # 	  #-----------------------------------------------------------------------------
	# # 	  ( InDegree ,c_int),                   # number of incoming links to each node
	# # 	  ( StartPos ,c_int),                   # start of a node's outlinks in AdjList
	# # 	  ( AdjList,c_int ),                    # list of outlink indexes for each node
	# # 	  ( Stack ,c_int),                      # array of nodes "reached" during sorting
	# # 	  (  First , c_int),                      # position of first node in stack
	# # 	  (  Last , c_int),                       # position of last node added to stack
    # #
	# # 	  char* Examined ),                  # TRUE if node included in spanning tree
	# # 	  char* InTree ),                    # state of each link in spanning tree:
	# # 	  # 0 = unexamined,
	# # 	  # 1 = in spanning tree,
	# # 	  # 2 = chord of spanning tree
     # #      ( LoopLinks ,c_int),                 # list of links which forms a loop
	# # 	  (   LoopLinksLast , c_int),             # number of links in a loop
    # #
    # #
	# # 	   #-----------------------------------------------------------------------------
	# # 	   #  Shared variables from rain.c
	# # 	   #-----------------------------------------------------------------------------
	# # 	  TRainStats RainStats ),                   # see objects.h for definition
	# # 	  (        Condition , c_int),                   # rainfall condition code
	# # 	  (        TimeOffset , c_int),                  # time offset of rainfall reading (sec)
	# # 	  (        DataOffset , c_int),                  # start of data on line of input
	# # 	  (        ValueOffset, c_int ),                 # start of rain value on input line
	# # 	  (        RainType , c_int),                    # rain measurement type code
	# # 	  (        Interval , c_int),                    # rain measurement interval (sec)
	# # 	 (    UnitsFactor ,c_double),                 # units conversion factor
	# # 	  float      RainAccum ),                   # rainfall depth accumulation
	# # 	  char       *StationID ),                  # station ID appearing in rain file
	# # 	  DateTime   AccumStartDate ),              # date when accumulation begins
	# # 	  DateTime   PreviousDate ),                # date of previous rainfall record
	# # 	  (        GageIndex , c_int),                   # index of rain gage analyzed
    # # (        hasStationName , c_int),              # true if data contains station name
	# # } ),

]