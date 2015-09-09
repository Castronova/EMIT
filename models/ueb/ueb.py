__author__ = 'tonycastronova'

import os
import stdlib
from os.path import *
from ctypes import *
from wrappers import feed_forward
from structures import *
import datetime
import jdutil
import math

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
            # lines = f.readlines()
            lines = f.read().splitlines()  # this will auto strip the \n \r
            paramFile = lines[1]
            sitevarFile = lines[2]
            inputconFile = './TWDEF_distributed/'+lines[3]
            outputconFile = lines[4]
            watershedFile = lines[5]
            wsvarName = lines[6].split(' ')[0]
            wsycorName = lines[6].split(' ')[1]
            wsxcorName = lines[6].split(' ')[2]
            aggoutputconFile = lines[7]
            aggoutputFile = lines[8]
            ModelStartDate = [int(float(l)) for l in lines[9].split(' ') if l != '']
            ModelEndDate = [int(float(l)) for l in lines[10].split(' ') if l != '']
            ModelDt = float(lines[11])
            outtStride, outyStep, outxStep = [int(s) for s in lines[12].split(' ')]
            ModelUTCOffset = float(lines[13])
            inpDailyorSubdaily = bool(lines[14]==True)


        wsxcorArray = c_float()
        wsycorArray = c_float()
        wsArray = c_int32()
        dimlen1 = c_int()
        dimlen2 = c_int()
        totalgrid = 0
        wsfillVal = c_int(-9999)
        npar = c_int(32)
        parvalArray = c_float(0)

        #todo: [#] == pointer, * == pointer
        # tsvarArray = pointer((c_float * 13)())
        # tsvarArray = POINTER(POINTER(c_float) * 13)()
        # tsvarArray = pointer(POINTER(c_float) * 13)()
        tsvarArray = pointer((POINTER(c_float)*13)())


        ntimesteps = pointer((c_int * 5)())

        # create pointer to instance of sitevar struct array
        strsvArray = pointer((sitevar * 32)())

        # create pointer to instance of inpforcvar struct array
        strinpforcArray = pointer((inpforcvar * 13)())

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


        # read 2d NetCDF Data
        for i  in range(0,32):
            a = strsvArray.contents[i]
            if a.svType == 1:
                print "%d %s %s\n" % (i, a.svFile,a.svVarName)
                retvalue = self.__uebLib.read2DNC('./TWDEF_distributed/'+a.svFile, a.svVarName, byref(a.svArrayValues))


        #//read input /forcing control file--all possible entries of input control have to be provided
        #readInputForcVars(inputconFile, strinpforcArray);
        print 'inputconFile: ',inputconFile
        print 'strinpforcArray: ', strinpforcArray.contents[0].infFile
        # read input force variables (main.cpp, line 219)
        self.__uebLib.readInputForcVars(cast(inputconFile,c_char_p), strinpforcArray)
        print 'strinpforcArray: ', strinpforcArray.contents[0].infFile



        # self.__uebLib.getObjectTypeCount.restype = c_int
        # self.__uebLib.swmm_getDateTime.restype = c_double

        # calculate model time span as a julian date (main.cpp, line 220)
        modelSpan =  jdutil.datetime_to_jd(datetime.datetime(*ModelEndDate)) - \
                     jdutil.datetime_to_jd(datetime.datetime(*ModelStartDate))

        # calculate model time steps (main.cpp, line 222)
        numTimeStep = int(math.ceil(modelSpan*(24./ModelDt)) )
        print 'Number of time steps: ', numTimeStep

        # read forcing data (main.cpp, line 226)
        # self.__uebLib.readTextData.argtypes = [POINTER(c_char), POINTER(c_float), POINTER(c_int)]

        if strsvArray.contents[16].svType != 3: # no accumulation zone (fixme: ???)
            for it in xrange(13):
                inftype = strinpforcArray.contents[it].infType
                print 'infFile: ',strinpforcArray.contents[it].infFile
                if inftype == 0:
                    # tsvar = cast(pointer(tsvarArray).contents[it], POINTER(c_float))
                    # nts = cast(pointer(ntimesteps).contents[0], POINTER(c_int))
                    # self.__uebLib.readTextData('./TWDEF_distributed/'+strinpforcArray.contents[it].infFile, byref(tsvar), byref(nts))
                    self.__uebLib.readTextData('./TWDEF_distributed/'+strinpforcArray.contents[it].infFile, byref(tsvarArray.contents[it]), byref(ntimesteps[0]))
                    # print 'tsvarArray: ',list(tsvarArray.contents)
                    # print 'ntimesteps: ',list(ntimesteps)

                elif inftype == 2 or inftype == -1:
                    pass

                print 'done'

        # todo: move this to finish
        # unload ueb
        del self.__uebLib


        print 'success'
    def run(self, inputs):
        pass

    def save(self):
        pass

