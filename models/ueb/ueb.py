__author__ = 'tonycastronova'

import os
import stdlib
from os.path import *
from ctypes import *
from wrappers import feed_forward
from structures import *

class ueb(feed_forward.feed_forward_wrapper):

    def __init__(self, config_params):

        # super(ueb,self).__init__(config_params)

        # lib = './bin/libUEBHydroCoupleComponent.1.0.0.dylib'
        lib = '/Users/tonycastronova/Documents/projects/iUtah/models/ueb/UEBComponent/UEBHydroCoupleComponent/Mac_x86_64/Debug/libUEBHydroCoupleComponent.1.0.0.dylib'
        self.__uebLib = cdll.LoadLibrary(join(os.path.dirname(__file__),lib))
        # print 'UEB Loaded Successfully'

        # todo: move into config
        conFile = './TWDEF_distributed/control.dat'

        # get param, sitevar, input, output, and watershed files
        with open(conFile, 'r') as f:
            lines = f.readlines()
            paramFile = lines[1].strip()
            sitevarFile = lines[2].strip()
            inputconFile = lines[3].strip()
            outputconFile = lines[4].strip()
            watershedFile = lines[5].strip()
            wsvarName = lines[6].split(' ')[0].strip()
            wsycorName = lines[6].split(' ')[1].strip()
            wsxcorName = lines[6].split(' ')[2].strip()
            aggoutputconFile = lines[7].strip()
            aggoutputFile = lines[8].strip()

        # 2009 10 01 0.0
        # 2010 05 31 0.0
        # 1.0
        # 1 15 16
        # -7.0
        # 0


        wsxcorArray = c_float()
        wsycorArray = c_float()
        wsArray = c_int32()
        dimlen1 = c_int()
        dimlen2 = c_int()
        totalgrid = 0
        wsfillVal = c_int(-9999)
        npar = c_int(32)
        parvalArray = c_float(0)

        # create pointer to instance of sitevar struct array
        strsvArray = pointer((sitevar * 32)())

        # mask = c_float()
        # pcap_lookupnet(dev, ctypes.byref(net), ctypes.byref(mask), errbuf)

        # read watershed netcdf file
        self.__uebLib.readwsncFile('./TWDEF_distributed/'+watershedFile, wsvarName, wsycorName, wsxcorName, byref(wsycorArray), byref(wsxcorArray), byref(wsArray), byref(dimlen1), byref(dimlen2), byref(wsfillVal))

        # read params (#194)
        self.__uebLib.readParams(paramFile, byref(parvalArray), npar)

        # read site variables (#200)
        # void readSiteVars(const char* inpFile, sitevar *&svArr)
        # self.__uebLib.readSiteVars.argtypes = [POINTER(c_char), POINTER(sitevar)]
        self.__uebLib.readSiteVars('./TWDEF_distributed/'+ sitevarFile, byref(strsvArray))







        # self.__uebLib.getObjectTypeCount.restype = c_int
        # self.__uebLib.swmm_getDateTime.restype = c_double

        # todo: move this to finish
        # unload ueb
        del self.__uebLib


        print 'success'
    def run(self, inputs):
        pass

    def save(self):
        pass

