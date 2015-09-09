__author__ = 'tonycastronova'

from ctypes import *

#
# class params(Structure):
#     _fields_ = [
#         ("irad", c_float),
#         ("ireadalb", c_float),
#         ("tr", c_float),
#         ("ts", c_float),
#         ("ems", c_float),
#         ("cg", c_float),
#         ("z", c_float),
#         ("zo", c_float),
#         ("rho", c_float),
#         ("rhog", c_float),
#         ("lc", c_float),
#         ("ks", c_float),
#         ("de", c_float),
#         ("avo", c_float),
#         ("anir0", c_float),
#         ("lans", c_float),
#         ("lang", c_float),
#         ("wlf", c_float),
#         ("rd1", c_float),
#         ("dnews", c_float),
#         ("emc", c_float),
#         ("alpha", c_float),
#         ("alphal", c_float),
#         ("gpar", c_float),
#         ("uc", c_float),
#         ("as", c_float),
#         ("Bs", c_float),
#         ("lambda", c_float),
#         ("rimax", c_float),
#         ("wcoeff", c_float),
#         ("apar", c_float),
#         ("cpar", c_float),
#         ]

class sitevar(Structure):
    _fields_ = [
        ("svName", c_char * 256),
        ("svType", c_int),
        ("svFile", c_char * 256),
        ("svVarName", c_char * 256),
        ("svdefValue", c_float),
        ("svArrayValues", POINTER(POINTER(c_float))), #float**
    ]

class inpforcvar(Structure):
    _fields_ = [
        ("infName", c_char * 256),
        ("infType", c_int),
        ("infFile", c_char * 256),
        ("infvarName", c_char * 256),
        ("inftimeVar", c_char * 256),
        ("infdefValue", c_float),
        ("numNcfiles", c_int),
    ]

class pointOutput(Structure):
    _fields_ = [
        ("outfName", c_char * 256),
        ("ycoord", c_int),
        ("xcoord", c_int),
    ]


class ncOutput(Structure):
    _fields_ = [
        ("outfName", c_char * 256),
        ("symbol", c_char * 256),
        ("units", c_char * 256),
    ]


class aggOutput(Structure):
# 	#char outfName[256];
    _fields_ = [
        ("symbol", c_char * 256),
        ("units", c_char * 256),
        ("aggop", c_char * 256),
    ]

class inptimeseries(Structure):
#         #CTime dtime;
        _fields_ = [
            ("datetime", c_float),
            ("tsValue", c_float),
        ]