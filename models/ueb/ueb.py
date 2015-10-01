__author__ = 'tonycastronova'

import os
import sys
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
        curdir = os.path.dirname(os.path.abspath(conFile))

        # get param, sitevar, input, output, and watershed files
        with open(conFile, 'r') as f:
            # lines = f.readlines()
            lines = f.read().splitlines()  # this will auto strip the \n \r
            C_paramFile = './TWDEF_distributed/'+lines[1]
            C_sitevarFile = './TWDEF_distributed/'+lines[2]
            C_inputconFile = './TWDEF_distributed/'+lines[3]
            C_outputconFile = './TWDEF_distributed/'+lines[4]
            C_watershedFile = './TWDEF_distributed/'+lines[5]
            C_wsvarName = lines[6].split(' ')[0]
            C_wsycorName = lines[6].split(' ')[1]
            C_wsxcorName = lines[6].split(' ')[2]
            C_aggoutputconFile = './TWDEF_distributed/'+lines[7]
            C_aggoutputFile = './TWDEF_distributed/'+lines[8]
            ModelStartDate = [int(float(l)) for l in lines[9].split(' ') if l != '']
            ModelEndDate = [int(float(l)) for l in lines[10].split(' ') if l != '']
            ModelDt = float(lines[11])
            outtStride, outyStep, outxStep = [int(s) for s in lines[12].split(' ')]
            ModelUTCOffset = float(lines[13])
            inpDailyorSubdaily = bool(lines[14]==True)



        C_wsxcorArray = c_float()
        C_wsycorArray = c_float()
        C_wsArray = pointer(pointer(c_int32()))
        C_dimlen1 = c_int()
        C_dimlen2 = c_int()
        totalgrid = 0
        C_wsfillVal = c_int(-9999)
        npar = c_int(32)
        tinitTime = c_int(0)
        C_parvalArray = pointer(c_float(0));
        numOut = 70 # hack: number of outputs?

        C_pOut = pointer(pointOutput())
        C_aggOut = pointer(aggOutput())
        C_ncOut = pointer(ncOutput())
        C_npout = c_int(0)
        C_nncout = c_int(0)
        C_naggout = c_int(0)
        C_nZones = c_int(0)

        C_tNameout = c_char_p("time")
        tunits = (c_char*256)()
        C_tUnitsout = pointer(tunits)
        C_tlong_name = c_char_p("time")
        C_tcalendar = c_char_p("standard")
        t_out = pointer(c_float(0))
        C_out_fillVal = c_float(-9999.0)

        C_outDimord = c_int(0)
        C_aggoutDimord = c_int(1)
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


        C_zName = c_char_p("Outletlocations")

        C_tcorvar = pointer((c_float * 13)())
        C_tsvarArray = pointer((c_float * 13)())
        C_tsvarArrayTemp = pointer((c_float * 5)())



        #todo: [#] == pointer, * == pointer

        C_tsvarArray = pointer((POINTER(c_float)*13)())

        C_ntimesteps = pointer((c_int * 5)())

        # create pointer to instance of sitevar struct array
        C_strsvArray = pointer((sitevar * 32)())

        # create pointer to instance of inpforcvar struct array
        C_strinpforcArray = pointer((inpforcvar * 13)())

        # mask = c_float()
        # pcap_lookupnet(dev, ctypes.byref(net), ctypes.byref(mask), errbuf)

        # read watershed netcdf file
        self.__uebLib.readwsncFile(C_watershedFile, C_wsvarName, C_wsycorName, C_wsxcorName, byref(C_wsycorArray), byref(C_wsxcorArray), byref(C_wsArray), byref(C_dimlen1), byref(C_dimlen2), byref(C_wsfillVal))


        # wsArray1D = numpy.empty((dimlen1.value*dimlen2.value),dtype=numpy.float)
        # wxi,wyj = numpy.meshgrid(numpy.arange(0,dimlen1.value,1),
        #                        numpy.arange(0,dimlen2.value, 1))
        # wsArray1D = wxi * dimlen2.value + wyj

        wsArray1D = numpy.empty((C_dimlen1.value*C_dimlen2.value),dtype=numpy.float)
        for i in xrange(C_dimlen1.value) :
            for j in xrange(C_dimlen2.value):
                wsArray1D[i*C_dimlen2.value + j] = C_wsArray[i][j];

        # zvalues is the unique set of wsArray1D
        zValues = list(set(wsArray1D))
        # fillset = [wsfillVal]

        # zVal is the set of zValues that do not equal wsFillVal
        zVal = [zValues[i] for i in xrange(len(zValues)) if zValues[i] != C_wsfillVal]

        C_nZones = len(zVal)
        z_ycor = [0.0 for i in xrange(C_nZones)]
        z_xcor = [0.0 for i in xrange(C_nZones)]


        # read params (#194)
        self.__uebLib.readParams(C_paramFile, byref(C_parvalArray), npar)

        # read site variables (#200)
        # void readSiteVars(const char* inpFile, sitevar *&svArr)
        # self.__uebLib.readSiteVars.argtypes = [POINTER(c_char), POINTER(sitevar)]
        self.__uebLib.readSiteVars(C_sitevarFile, byref(C_strsvArray))


        # read 2d NetCDF Data
        for i  in range(0,32):
            a = C_strsvArray.contents[i]
            if a.svType == 1:
                print "%d %s %s\n" % (i, a.svFile,a.svVarName)
                retvalue = self.__uebLib.read2DNC('./TWDEF_distributed/'+a.svFile, a.svVarName, byref(a.svArrayValues))


        #//read input /forcing control file--all possible entries of input control have to be provided
        #readInputForcVars(inputconFile, strinpforcArray);
        print 'inputconFile: ',C_inputconFile
        print 'strinpforcArray: ', C_strinpforcArray.contents[0].infFile

        # read input force variables (main.cpp, line 219)
        self.__uebLib.readInputForcVars(cast(C_inputconFile,c_char_p), C_strinpforcArray)
        print 'strinpforcArray: ', C_strinpforcArray.contents[0].infFile


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
        if C_strsvArray.contents[16].svType != 3: # no accumulation zone (fixme: ???)
            for it in xrange(13):
                inftype = C_strinpforcArray.contents[it].infType
                print 'infFile: ',C_strinpforcArray.contents[it].infFile
                if inftype == 0:
                    self.__uebLib.readTextData('./TWDEF_distributed/'+C_strinpforcArray.contents[it].infFile, byref(C_tsvarArray.contents[it]), byref(C_ntimesteps[0]))

                elif inftype == 2 or inftype == -1:
                    C_tsvarArray.contents[it] = (c_float * 2)()
                    C_ntimesteps.contents[0] = 2
                    # copy the default value if a single value is the option
                    C_tsvarArray.contents[it][0] = C_strinpforcArray.contents[it].infType
                    C_tsvarArray.contents[it][1] = C_strinpforcArray.contents[it].infdefValue

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
        totalgrid = C_dimlen1.value*C_dimlen2.value

        # read output control file (main.cpp, line 251)
        # readOutputControl(outputconFile, aggoutputconFile, pOut, ncOut, aggOut, npout, nncout, naggout);

        self.__uebLib.readOutputControl(cast(C_outputconFile,c_char_p), cast(C_aggoutputconFile, c_char_p),
                                        byref(C_pOut), byref(C_ncOut), byref(C_aggOut),
                                        byref(C_npout), byref(C_nncout), byref(C_naggout))


        # create output netcdf
        C_outtSteps = numTimeStep / outtStride
        t_out = numpy.empty(shape=(C_outtSteps), dtype=numpy.float, order="C")
        for i in xrange(C_outtSteps):
            t_out[i] = i*outtStride*ModelDt

        # initialize the output arrays
        aggoutvarArray = numpy.zeros((C_nZones,C_naggout.value, C_outtSteps), dtype=numpy.float)
        totalAgg = numpy.empty((C_outtSteps,), dtype=numpy.float)
        ZonesArr = numpy.zeros((C_nZones,), dtype=numpy.int32)

        # main.cpp, line 290
        # CREATE 3D NC OUTPUT FILES
        # convert t_out into a float pointer
        C_t_out = t_out.ctypes.data_as(POINTER(c_float))
        for i in xrange(C_nncout.value):
            '''
            for (int icout = 0; icout < nncout; icout++)
                retvalue = create3DNC_uebOutputs(ncOut[icout].outfName, (const char*)ncOut[icout].symbol, (const char*)ncOut[icout].units, tNameout, tUnitsout,
            tlong_name, tcalendar, outtSteps, outDimord, t_out, &out_fillVal, watershedFile, wsvarName, wsycorName, wsxcorName);
            '''

            retvalue = self.__uebLib.create3DNC_uebOutputs(C_ncOut[i].outfName, cast(C_ncOut[i].symbol, c_char_p), cast(C_ncOut[i].units, c_char_p), C_tNameout, C_tUnitsout, C_tlong_name, C_tcalendar, C_outtSteps, C_outDimord, C_t_out, byref(C_out_fillVal), C_watershedFile, C_wsvarName, C_wsycorName, C_wsxcorName);

        # CREATE 3D NC AGGREGATE OUTPUT FILE
        # convert z_ycor and x_xcor from list into ctype
        C_z_xcor = numpy.asarray(z_xcor).ctypes.data_as(POINTER(c_float))
        C_z_ycor = numpy.asarray(z_ycor).ctypes.data_as(POINTER(c_float))
        retvalue = self.__uebLib.create3DNC_uebAggregatedOutputs(C_aggoutputFile, C_aggOut, C_naggout, C_tNameout, C_tUnitsout, C_tlong_name, C_tcalendar, C_outtSteps, C_aggoutDimord, C_t_out, byref(C_out_fillVal), C_watershedFile, C_wsvarName, C_wsycorName, C_wsxcorName, C_nZones, C_zName, C_z_ycor, C_z_xcor);


        print "\nBegin Computation: \n"



        # main.cpp, line 303
        activeCells = []
        for iy in xrange(C_dimlen1.value):
            for jx in xrange(C_dimlen2.value):
                if C_wsArray[iy][jx] != C_wsfillVal.value and C_strsvArray.contents[16].svType != 3:
                    activeCells.append((iy, jx))


        # Initialize SiteState
        SiteState = numpy.zeros((32,))

        # convert Simulation Time parameters into ctypes
        C_ModelStartDate = (c_int * len(ModelStartDate))(*ModelStartDate)
        C_ModelEndDate =(c_int * len(ModelEndDate))(*ModelEndDate)
        C_ModelDt = c_double(ModelDt)
        C_ModelUTCOffset = c_double(ModelUTCOffset)
        C_ModelStartHour = c_double(ModelStartHour)
        C_ModelEndHour = c_double(ModelEndHour)

        for i in xrange(len(activeCells)):

            # track grid cell
            C_uebCellY = activeCells[i][0]
            C_uebCellX = activeCells[i][1]

            for s in xrange(32):
                if C_strsvArray.contents[s].svType == 1:
                    SiteState[s] = C_strsvArray.contents[s].svArrayValues[C_uebCellY][C_uebCellX]
                else:
                    SiteState[s] = C_strsvArray.contents[s].svdefValue

            # convert SiteState into a ctype
            C_SiteState = (c_float * len(SiteState))(*SiteState)

            for t in xrange(13):

                # HACK: Everything inside this 'if' statement needs to be checked!!!!
                if C_strinpforcArray.contents[t].infType == 1:
                    print 'You are in un-tested code! '
                    ncTotaltimestep = 0;

                    for numNc in xrange(C_strinpforcArray[it].numNcfiles):
                        # read 3D netcdf data
                        tsInputfile = C_strinpforcArray[t].infFile + numNc + '.nc'

                        retvalue = self.__uebLib.readNC_TS(tsInputfile, C_strinpforcArray.contents[t].infvarName, C_strinpforcArray.contents[t].inftimeVar, C_wsycorName, C_wsxcorName, byref(C_tsvarArrayTemp[numNc]), byref(C_tcorvar[it]), C_uebCellY, C_uebCellX, byref(C_ntimesteps[numNc]));

                        ncTotaltimestep += C_ntimesteps[numNc];

                    C_tsvarArray[t] = (c_float * ncTotaltimestep)
                    tinitTime = 0
                    for numNc in xrange(C_strinpforcArray.contents[t].numNcFiles):
                        for tts in xrange(C_ntimesteps[numNc]):
                            C_tsvarArray.contents[t][tts + tinitTime] = C_tsvarArrayTemp.contents[numNc][tts]
                        tinitTime += C_ntimesteps[numNc]



            # RUN THE UEB CALCS
            ModelStartHour = 1
            self.__uebLib.RUNUEB(C_tsvarArray, C_SiteState, C_parvalArray, byref(pointer(C_outvarArray)), C_ModelStartDate, C_ModelStartHour, C_ModelEndDate, C_ModelEndHour, C_ModelDt, C_ModelUTCOffset);
            break

            print i+1, " of ", len(activeCells)


        # write nc output
        for i in xrange(C_nncout.value):
            for j in xrange(70):
                if C_ncOut[i].symbol == uebVars[j]:
                    outvarindx.value = j;
                    break
            for j in xrange(C_outtSteps):
                t_out[j] = outvarArray[outvarindx.value][outtStride*j]

            print 'Writing Output: ', os.path.join(curdir, C_ncOut[i].outfName)
            C_t_out = t_out.ctypes.data_as(POINTER(c_float))
            retvalue = self.__uebLib.WriteTSto3DNC(cast(os.path.join(curdir, C_ncOut[i].outfName), c_char_p), cast(C_ncOut[i].symbol, c_char_p), C_outDimord, C_uebCellY, C_uebCellX, C_outtSteps, C_t_out)

        # write point outputs
        for i in xrange(C_npout.value):
            # todo: this is inefficient
            if C_uebCellY == C_pOut[i].ycoord and C_uebCellX == C_pOut[i].xcoord:
                print 'Writing Output: ', C_pOut[i].outfName
                with open(C_pOut[i].outfName, 'w') as f:
                    for step in xrange(numTimeStep):
                        f.write("\n %d %d %d %8.3f " % (outvarArray[0][step],  outvarArray[1][step], outvarArray[2][step], outvarArray[3][step]) )
                        for vnum in range(4,70):
                            f.write(" %16.6f " % outvarArray[vnum][step])

        # # write aggregated outputs
        # zoneid = wsArray[uebCellY][uebCellX] - 1
        # ZonesArr[zoneid] += 1
        # for i in xrange(naggout):
        #     # todo: this is inefficient
        #     for v in xrange(70):
        #         if aggOut[i].symbol == uebVars[v]:
        #             aggoutvarindx = v
        #             break
        #     for t in xrange(outtSteps):
        #         aggoutvarArray[zoneid][i][t] += outvarArray[aggoutvarindx][outtStride*t]
        #
        # for i in xrange(naggout):




        # todo: move this to finish
        # unload ueb
        del self.__uebLib


        print 'success'
    def run(self, inputs):
        pass

    def save(self):
        pass

