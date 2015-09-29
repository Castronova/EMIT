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
import numpy

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
            paramFile = './TWDEF_distributed/'+lines[1]
            sitevarFile = './TWDEF_distributed/'+lines[2]
            inputconFile = './TWDEF_distributed/'+lines[3]
            outputconFile = './TWDEF_distributed/'+lines[4]
            watershedFile = './TWDEF_distributed/'+lines[5]
            wsvarName = lines[6].split(' ')[0]
            wsycorName = lines[6].split(' ')[1]
            wsxcorName = lines[6].split(' ')[2]
            aggoutputconFile = './TWDEF_distributed/'+lines[7]
            aggoutputFile = './TWDEF_distributed/'+lines[8]
            ModelStartDate = [int(float(l)) for l in lines[9].split(' ') if l != '']
            ModelEndDate = [int(float(l)) for l in lines[10].split(' ') if l != '']
            ModelDt = float(lines[11])
            outtStride, outyStep, outxStep = [int(s) for s in lines[12].split(' ')]
            ModelUTCOffset = float(lines[13])
            inpDailyorSubdaily = bool(lines[14]==True)



        wsxcorArray = c_float()
        wsycorArray = c_float()
        wsArray = pointer(pointer(c_int32()))
        dimlen1 = c_int()
        dimlen2 = c_int()
        totalgrid = 0
        wsfillVal = c_int(-9999)
        npar = c_int(32)
        tinitTime = c_int(0)
        parvalArray = pointer(c_float(0));
        numOut = 70 # hack: number of outputs?

        pOut = pointer(pointOutput())
        aggOut = pointer(aggOutput())
        ncOut = pointer(ncOutput())
        npout = c_int(0)
        nncout = c_int(0)
        naggout = c_int(0)
        nZones = c_int(0)

        tNameout = c_char_p("time")
        tunits = (c_char*256)()
        tUnitsout = pointer(tunits)
        tlong_name = c_char_p("time")
        tcalendar = c_char_p("standard")
        t_out = pointer(c_float(0))
        out_fillVal = c_float(-9999.0)

        outDimord = c_int(0)
        aggoutDimord = c_int(1)
        outvarindx = c_int(17)
        aggoutvarindx = c_int(17)
        size = c_int()
        rank = c_int()
        irank = c_int()
        jrank = c_int()
        startTimeT = c_double(0.0)
        TotalTime = c_double(0.0)
        totalmodelrunTime = c_double(0.0)
        TsReadTime = c_double(0.0)
        TSStartTime = c_double()
        ComputeStartTime = c_double()
        ComputeTime = c_double(0.0)
        OutWriteTime = c_double()

        uebVars = (c_char_p * 70)("Year", "Month", "Day", "dHour", "atff", "HRI", "Eacl", "Ema", "conZen", "Ta", "P", "V", "RH", "Qsi", "Qli", "Qnet","Us", "SWE", "tausn", "Pr", "Ps", "Alb", "QHs", "QEs", "Es", "SWIT", "QMs", "Q", "FM", "Tave", "TSURFs", "cump", "cumes", "cumMr", "Qnet", "smelt", "refDepth", "totalRefDepth", "cf", "Taufb", "Taufd", "Qsib", "Qsid", "Taub", "Taud", "Qsns", "Qsnc", "Qlns", "Qlnc", "Vz", "Rkinsc", "Rkinc", "Inmax", "intc", "ieff", "Ur", "Wc", "Tc", "Tac", "QHc", "QEc", "Ec", "Qpc", "Qmc", "Mc", "FMc", "SWIGM", "SWISM", "SWIR", "errMB")


        zName = c_char_p("Outletlocations")

        # float *tcorvar[13], *tsvarArray[13], *tsvarArrayTemp[5];
        tcorvar = pointer((c_float * 13)())
        tsvarArray = pointer((c_float * 13)())
        tsvarArrayTemp = pointer((c_float * 5)())



        #todo: [#] == pointer, * == pointer

        tsvarArray = pointer((POINTER(c_float)*13)())

        ntimesteps = pointer((c_int * 5)())

        # create pointer to instance of sitevar struct array
        strsvArray = pointer((sitevar * 32)())

        # create pointer to instance of inpforcvar struct array
        strinpforcArray = pointer((inpforcvar * 13)())

        # mask = c_float()
        # pcap_lookupnet(dev, ctypes.byref(net), ctypes.byref(mask), errbuf)

        # read watershed netcdf file
        self.__uebLib.readwsncFile(watershedFile, wsvarName, wsycorName, wsxcorName, byref(wsycorArray), byref(wsxcorArray), byref(wsArray), byref(dimlen1), byref(dimlen2), byref(wsfillVal))


        # wsArray1D = numpy.empty((dimlen1.value*dimlen2.value),dtype=numpy.float)
        # wxi,wyj = numpy.meshgrid(numpy.arange(0,dimlen1.value,1),
        #                        numpy.arange(0,dimlen2.value, 1))
        # wsArray1D = wxi * dimlen2.value + wyj

        wsArray1D = numpy.empty((dimlen1.value*dimlen2.value),dtype=numpy.float)
        for i in xrange(dimlen1.value) :
            for j in xrange(dimlen2.value):
                wsArray1D[i*dimlen2.value + j] = wsArray[i][j];

        # zvalues is the unique set of wsArray1D
        zValues = list(set(wsArray1D))
        # fillset = [wsfillVal]

        # zVal is the set of zValues that do not equal wsFillVal
        zVal = [zValues[i] for i in xrange(len(zValues)) if zValues[i] != wsfillVal]

        nZones = len(zVal)
        z_ycor = [0.0 for i in xrange(nZones)]
        z_xcor = [0.0 for i in xrange(nZones)]


        # read params (#194)
        self.__uebLib.readParams(paramFile, byref(parvalArray), npar)

        # read site variables (#200)
        # void readSiteVars(const char* inpFile, sitevar *&svArr)
        # self.__uebLib.readSiteVars.argtypes = [POINTER(c_char), POINTER(sitevar)]
        self.__uebLib.readSiteVars(sitevarFile, byref(strsvArray))


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


        # calculate model time span as a julian date (main.cpp, line 220)
        modelSpan =  jdutil.datetime_to_jd(datetime.datetime(*ModelEndDate)) - \
                     jdutil.datetime_to_jd(datetime.datetime(*ModelStartDate))

        # setup the model start dates as UEB expects them
        ModelStartHour = ModelStartDate.pop(-1) # an integer representing the start hour (24 hour time)
        ModelEndHour = ModelEndDate.pop(-1)     # an integer representing the end hour (24 hour time)
        # ModelStartDate is a 3 element array: [year, month, day]
        # ModelEndDate is a 3 element array: [year, month, day]


        # calculate model time steps (main.cpp, line 222)
        numTimeStep = int(math.ceil(modelSpan*(24./ModelDt)) )
        print 'Number of time steps: ', numTimeStep

        # read forcing data (main.cpp, line 226)
        if strsvArray.contents[16].svType != 3: # no accumulation zone (fixme: ???)
            for it in xrange(13):
                inftype = strinpforcArray.contents[it].infType
                print 'infFile: ',strinpforcArray.contents[it].infFile
                if inftype == 0:
                    self.__uebLib.readTextData('./TWDEF_distributed/'+strinpforcArray.contents[it].infFile, byref(tsvarArray.contents[it]), byref(ntimesteps[0]))

                elif inftype == 2 or inftype == -1:
                    tsvarArray.contents[it] = (c_float * 2)()
                    ntimesteps.contents[0] = 2
                    # copy the default value if a single value is the option
                    tsvarArray.contents[it][0] = strinpforcArray.contents[it].infType
                    tsvarArray.contents[it][1] = strinpforcArray.contents[it].infdefValue

        # create a numpy array for outputs
        outvarArray = numpy.zeros(shape=(numOut, numTimeStep), dtype=numpy.float, order="C")
        arrays = outvarArray.astype(numpy.float32)
        rows, cols = outvarArray.shape
        arrays_as_list = list(arrays)
        #get ctypes handles
        ctypes_arrays = [numpy.ctypeslib.as_ctypes(array) for array in arrays_as_list]
        #Pack into pointer array
        C_outvarArray = (POINTER(c_float) * rows)(*ctypes_arrays)


        # total grid size to compute progess
        totalgrid = dimlen1.value*dimlen2.value

        # read output control file (main.cpp, line 251)
        # readOutputControl(outputconFile, aggoutputconFile, pOut, ncOut, aggOut, npout, nncout, naggout);

        self.__uebLib.readOutputControl(cast(outputconFile,c_char_p), cast(aggoutputconFile, c_char_p),
                                        byref(pOut), byref(ncOut), byref(aggOut),
                                        byref(npout), byref(nncout), byref(naggout))


        # create output netcdf
        outtSteps = numTimeStep / outtStride
        t_out = numpy.empty(shape=(outtSteps), dtype=numpy.float, order="C")
        for i in xrange(outtSteps):
            t_out[i] = i*outtStride*ModelDt

        # initialize the output arrays
        aggoutvarArray = numpy.zeros((nZones,naggout.value, outtSteps), dtype=numpy.float)
        totalAgg = numpy.empty((outtSteps,), dtype=numpy.float)
        ZonesArr = numpy.zeros((nZones,), dtype=numpy.int32)
        # for j in xrange(nZones):
        #     ZonesArr[j] = 0
            # aggoutvarArray[j] = numpy.empty((naggout.value,), dtype=numpy.float)
            # for i in xrange(naggout.value):
            #     aggoutvarArray[j][i] = numpy.empty((outtSteps,), dtype=numpy.float)
            #     for it in xrange(outtSteps):
            #         aggoutvarArray[j][i][it] = 0.0;

        # main.cpp, line 290
        # CREATE 3D NC OUTPUT FILES
        # convert t_out into a float pointer
        C_t_out = t_out.ctypes.data_as(POINTER(c_float))
        for i in xrange(nncout.value):
            '''
            for (int icout = 0; icout < nncout; icout++)
                retvalue = create3DNC_uebOutputs(ncOut[icout].outfName, (const char*)ncOut[icout].symbol, (const char*)ncOut[icout].units, tNameout, tUnitsout,
            tlong_name, tcalendar, outtSteps, outDimord, t_out, &out_fillVal, watershedFile, wsvarName, wsycorName, wsxcorName);
            '''

            retvalue = self.__uebLib.create3DNC_uebOutputs(ncOut[i].outfName, cast(ncOut[i].symbol, c_char_p), cast(ncOut[i].units, c_char_p), tNameout, tUnitsout, tlong_name, tcalendar, outtSteps, outDimord, C_t_out, byref(out_fillVal), watershedFile, wsvarName, wsycorName, wsxcorName);

        # CREATE 3D NC AGGREGATE OUTPUT FILE
        # convert z_ycor and x_xcor from list into ctype
        C_z_xcor = numpy.asarray(z_xcor).ctypes.data_as(POINTER(c_float))
        C_z_ycor = numpy.asarray(z_ycor).ctypes.data_as(POINTER(c_float))
        retvalue = self.__uebLib.create3DNC_uebAggregatedOutputs(aggoutputFile, aggOut, naggout, tNameout, tUnitsout, tlong_name, tcalendar, outtSteps, aggoutDimord, C_t_out, byref(out_fillVal), watershedFile, wsvarName, wsycorName, wsxcorName, nZones, zName, C_z_ycor, C_z_xcor);


        # main.cpp, line 303
        activeCells = []
        for iy in xrange(dimlen1.value):
            for jx in xrange(dimlen2.value):
                if wsArray[iy][jx] != wsfillVal.value and strsvArray.contents[16].svType != 3:
                    activeCells.append((iy, jx))

        SiteState = numpy.zeros((32,))
        for i in xrange(len(activeCells)):

            # track grid cell
            uebCellY = activeCells[i][0]
            uebCellX = activeCells[i][1]

            for s in xrange(32):

                if strsvArray.contents[s].svType == 1:
                    # print i, s, strsvArray.contents[s].svArrayValues[uebCellY][uebCellX]
                    SiteState[s] = strsvArray.contents[s].svArrayValues[uebCellY][uebCellX]
                else:
                    SiteState[s] = strsvArray.contents[s].svdefValue

            for t in xrange(13):
                # HACK: Everything inside this 'if' statement needs to be checked!!!!
                if strinpforcArray.contents[t].infType == 1:
                    print 'You are in un-tested code! '
                    ncTotaltimestep = 0;

                    for numNc in xrange(strinpforcArray[it].numNcfiles):
                        # read 3D netcdf data
                        tsInputfile = strinpforcArray[t].infFile + numNc + '.nc'

                        retvalue = self.__uebLib.readNC_TS(tsInputfile, strinpforcArray.contents[t].infvarName, strinpforcArray.contents[t].inftimeVar, wsycorName, wsxcorName, byref(tsvarArrayTemp[numNc]), byref(tcorvar[it]), uebCellY, uebCellX, byref(ntimesteps[numNc]));

                        ncTotaltimestep += ntimesteps[numNc];

                    tsvarArray[t] = (c_float * ncTotaltimestep)
                    tinitTime = 0
                    for numNc in xrange(strinpforcArray.contents[t].numNcFiles):
                        for tts in xrange(ntimesteps[numNc]):
                            tsvarArray.contents[t][tts + tinitTime] = tsvarArrayTemp.contents[numNc][tts]
                        tinitTime += ntimesteps[numNc]

            # convert SiteState into ctype
            C_SiteState = SiteState.ctypes.data_as(POINTER(c_float))  # fixme ???
            C_ModelStartDate = (c_int * len(ModelStartDate))(*ModelStartDate)
            C_ModelEndDate =(c_int * len(ModelEndDate))(*ModelEndDate)
            # C_outvarArray = outvarArray.ctypes.data_as(POINTER(POINTER(c_float)))
            # C_outvarArray = outvarArray.ctypes.data_as((POINTER(c_float)))
            # C_outvarArray = pointer(outvarArray.ctypes.data_as(POINTER(POINTER(c_float))))
            C_ModelDt = c_double(ModelDt)
            C_ModelUTCOffset = c_double(ModelUTCOffset)
            C_ModelStartHour = c_double(ModelStartHour)
            C_ModelEndHour = c_double(ModelEndHour)
            # RUN THE UEB CALCS
            ModelStartHour = 1


            self.__uebLib.RUNUEB(tsvarArray, C_SiteState, parvalArray, byref(pointer(C_outvarArray)), C_ModelStartDate, C_ModelStartHour, C_ModelEndDate, C_ModelEndHour, C_ModelDt, C_ModelUTCOffset);


            print "RESULT: ", C_outvarArray[5][i]


            a = 1



        # todo: move this to finish
        # unload ueb
        del self.__uebLib


        print 'success'
    def run(self, inputs):
        pass

    def save(self):
        pass

