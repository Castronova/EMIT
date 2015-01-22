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
# https://docs.python.org/2/library/ctypes.html


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