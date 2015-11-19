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
from coordinator.emitLogging import elog
from utilities import mdl, geometry
import netCDF4 as nc


class ueb(feed_forward.feed_forward_wrapper):

    def __init__(self, config_params):
        super(ueb,self).__init__(config_params)

        # build inputs and outputs
        elog.info('Building exchange items')
        io = mdl.build_exchange_items_from_config(config_params)

        # set input and output exchange items
        self.inputs(value=io[stdlib.ExchangeItemType.INPUT])
        self.outputs(value=io[stdlib.ExchangeItemType.OUTPUT])

        # get model parameters
        params = config_params['model_inputs'][0]

        # grab the C library path and the control file path
        lib = params['lib']
        conFile = params['control']

        # load the UEB C library
        self.__uebLib = cdll.LoadLibrary(join(os.path.dirname(__file__),lib))

        print join(os.path.dirname(__file__),lib)
        print lib

        # save the current directory for saving output data
        self.curdir = os.path.dirname(os.path.abspath(conFile))

        # the base directory for the control file is used to convert relative paths into absolute paths
        self.base_dir = os.path.dirname(conFile)

        # get param, sitevar, input, output, and watershed files
        with open(conFile, 'r') as f:
            # lines = f.readlines()
            lines = f.read().splitlines()  # this will auto strip the \n \r
            C_paramFile = os.path.join(self.base_dir, lines[1])
            C_sitevarFile = os.path.join(self.base_dir, lines[2])
            C_inputconFile = os.path.join(self.base_dir, lines[3])
            C_outputconFile = os.path.join(self.base_dir, lines[4])
            C_watershedFile = os.path.join(self.base_dir, lines[5])
            C_wsvarName = lines[6].split(' ')[0]
            C_wsycorName = lines[6].split(' ')[1]
            C_wsxcorName = lines[6].split(' ')[2]
            C_aggoutputconFile = os.path.join(self.base_dir, lines[7])
            C_aggoutputFile = os.path.join(self.base_dir, lines[8])
            ModelStartDate = [int(float(l)) for l in lines[9].split(' ') if l != '']
            ModelEndDate = [int(float(l)) for l in lines[10].split(' ') if l != '']
            ModelDt = float(lines[11])
            self.outtStride, outyStep, outxStep = [int(s) for s in lines[12].split(' ')]
            ModelUTCOffset = float(lines[13])
            inpDailyorSubdaily = bool(lines[14]==True)


        # build input geometries
        ds = nc.Dataset(C_watershedFile)
        Xlist = ds.variables['x']
        yList = ds.variables['y']
        xcoords, ycoords = numpy.meshgrid(Xlist, yList)
        xcoords = xcoords.flatten()
        ycoords = ycoords.flatten()
        geoms = geometry.build_point_geometries(xcoords, ycoords)
        self.inputs()['precipitation'].addGeometries2(geoms)




        C_wsxcorArray = c_float()
        C_wsycorArray = c_float()
        self.C_wsArray = pointer(pointer(c_int32()))
        self.C_dimlen1 = c_int()
        self.C_dimlen2 = c_int()
        totalgrid = 0
        self.C_wsfillVal = c_int(-9999)
        npar = c_int(32)
        tinitTime = c_int(0)
        self.C_parvalArray = pointer(c_float(0));
        numOut = 70 # hack: number of outputs?

        self.C_pOut = pointer(pointOutput())
        C_aggOut = pointer(aggOutput())
        self.C_ncOut = pointer(ncOutput())
        self.C_npout = c_int(0)
        self.C_nncout = c_int(0)
        C_naggout = c_int(0)
        C_nZones = c_int(0)

        C_tNameout = c_char_p("time")
        tunits = (c_char*256)()
        C_tUnitsout = pointer(tunits)
        C_tlong_name = c_char_p("time")
        C_tcalendar = c_char_p("standard")
        self.t_out = pointer(c_float(0))
        C_out_fillVal = c_float(-9999.0)

        self.C_outDimord = c_int(0)
        C_aggoutDimord = c_int(1)
        self.outvarindx = c_int(17)
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

        self.uebVars = (c_char_p * 70)("Year", "Month", "Day", "dHour", "atff", "HRI", "Eacl", "Ema", "conZen", "Ta", "P", "V", "RH", "Qsi", "Qli", "Qnet","Us", "SWE", "tausn", "Pr", "Ps", "Alb", "QHs", "QEs", "Es", "SWIT", "QMs", "Q", "FM", "Tave", "TSURFs", "cump", "cumes", "cumMr", "Qnet", "smelt", "refDepth", "totalRefDepth", "cf", "Taufb", "Taufd", "Qsib", "Qsid", "Taub", "Taud", "Qsns", "Qsnc", "Qlns", "Qlnc", "Vz", "Rkinsc", "Rkinc", "Inmax", "intc", "ieff", "Ur", "Wc", "Tc", "Tac", "QHc", "QEc", "Ec", "Qpc", "Qmc", "Mc", "FMc", "SWIGM", "SWISM", "SWIR", "errMB")


        C_zName = c_char_p("Outletlocations")

        C_tcorvar = pointer((c_float * 13)())
        self.C_tsvarArray = pointer((c_float * 13)())
        C_tsvarArrayTemp = pointer((c_float * 5)())



        #todo: [#] == pointer, * == pointer

        self.C_tsvarArray = pointer((POINTER(c_float)*13)())

        C_ntimesteps = pointer((c_int * 5)())

        # create pointer to instance of sitevar struct array
        self.C_strsvArray = pointer((sitevar * 32)())

        # create pointer to instance of inpforcvar struct array
        self.C_strinpforcArray = pointer((inpforcvar * 13)())

        # mask = c_float()
        # pcap_lookupnet(dev, ctypes.byref(net), ctypes.byref(mask), errbuf)

        # read watershed netcdf file
        self.__uebLib.readwsncFile(C_watershedFile, C_wsvarName, C_wsycorName, C_wsxcorName, byref(C_wsycorArray), byref(C_wsxcorArray), byref(self.C_wsArray), byref(self.C_dimlen1), byref(self.C_dimlen2), byref(self.C_wsfillVal))


        wsArray1D = numpy.empty((self.C_dimlen1.value*self.C_dimlen2.value),dtype=numpy.float)
        for i in xrange(self.C_dimlen1.value) :
            for j in xrange(self.C_dimlen2.value):
                wsArray1D[i*self.C_dimlen2.value + j] = self.C_wsArray[i][j];

        # zvalues is the unique set of wsArray1D
        zValues = list(set(wsArray1D))
        # fillset = [wsfillVal]

        # zVal is the set of zValues that do not equal wsFillVal
        zVal = [zValues[i] for i in xrange(len(zValues)) if zValues[i] != self.C_wsfillVal]

        C_nZones = len(zVal)
        z_ycor = [0.0 for i in xrange(C_nZones)]
        z_xcor = [0.0 for i in xrange(C_nZones)]


        # read params (#194)
        self.__uebLib.readParams(C_paramFile, byref(self.C_parvalArray), npar)

        # read site variables (#200)
        self.__uebLib.readSiteVars(C_sitevarFile, byref(self.C_strsvArray))


        # read 2d NetCDF Data
        for i  in range(0,32):
            a = self.C_strsvArray.contents[i]
            if a.svType == 1:
                print "%d %s %s\n" % (i, a.svFile,a.svVarName)
                retvalue = self.__uebLib.read2DNC(os.path.join(self.base_dir, a.svFile), a.svVarName, byref(a.svArrayValues))


        #//read input /forcing control file--all possible entries of input control have to be provided
        #readInputForcVars(inputconFile, strinpforcArray);
        print 'inputconFile: ',C_inputconFile
        print 'strinpforcArray: ', self.C_strinpforcArray.contents[0].infFile

        # read input force variables (main.cpp, line 219)
        self.__uebLib.readInputForcVars(cast(C_inputconFile,c_char_p), self.C_strinpforcArray)
        print 'strinpforcArray: ', self.C_strinpforcArray.contents[0].infFile

        ed = datetime.datetime(*ModelEndDate)
        sd = datetime.datetime(*ModelStartDate)
        elog.info('UEB Start Date: %s' % sd.strftime("%m-%d-%Y %H:%M:%S"))
        elog.info('UEB End Date: %s' % ed.strftime("%m-%d-%Y %H:%M:%S"))

        # calculate model time span as a julian date (main.cpp, line 220)
        modelSpan =  jdutil.datetime_to_jd(datetime.datetime(*ModelEndDate)) - \
                     jdutil.datetime_to_jd(datetime.datetime(*ModelStartDate))

        # setup the model start dates as UEB expects them
        ModelStartHour = ModelStartDate.pop(-1) # an integer representing the start hour (24 hour time)
        ModelEndHour = ModelEndDate.pop(-1)     # an integer representing the end hour (24 hour time)
        # ModelStartDate is a 3 element array: [year, month, day]
        # ModelEndDate is a 3 element array: [year, month, day]

        # convert Simulation Time parameters into ctypes
        self.C_ModelStartDate = (c_int * len(ModelStartDate))(*ModelStartDate)
        self.C_ModelEndDate =(c_int * len(ModelEndDate))(*ModelEndDate)
        self.C_ModelDt = c_double(ModelDt)
        self.C_ModelUTCOffset = c_double(ModelUTCOffset)
        self.C_ModelStartHour = c_double(ModelStartHour)
        self.C_ModelEndHour = c_double(ModelEndHour)


        # calculate model time steps (main.cpp, line 222)
        self.numTimeStep = int(math.ceil(modelSpan*(24./ModelDt)) )
        print 'Number of time steps: ', self.numTimeStep

        # initialize C_tsvarArray values (this replaces __uebLib.readTextData)
        self.initialize_timeseries_variable_array(self.C_strinpforcArray, self.numTimeStep)

        # NOTE: C_strinpforcArray stores info about the forcing data files

        # read forcing data (main.cpp, line 226)
        if self.C_strsvArray.contents[16].svType != 3: # no accumulation zone (fixme: ???)
            for it in xrange(13):
                inftype = self.C_strinpforcArray.contents[it].infType
                print 'infFile: ',self.C_strinpforcArray.contents[it].infFile
                if inftype == 0:

                    # read the files stored in C_strinpforcArray and populated C_tsvarArray
                    self.__uebLib.readTextData(os.path.join(self.base_dir, self.C_strinpforcArray.contents[it].infFile), byref(self.C_tsvarArray.contents[it]), byref(C_ntimesteps[0]))

                elif inftype == 2 or inftype == -1:
                    self.C_tsvarArray.contents[it] = (c_float * 2)()
                    C_ntimesteps.contents[0] = 2
                    # copy the default value if a single value is the option
                    self.C_tsvarArray.contents[it][0] = self.C_strinpforcArray.contents[it].infType
                    self.C_tsvarArray.contents[it][1] = self.C_strinpforcArray.contents[it].infdefValue


        # :: this array is initialized to (numOut+1, numTimeStep+1) rather than (numOut, numTimeStep)
        # :: b/c otherwise the calculations from RunUEB are incorrect for the first row.
        # :: e.g.
        # ::     2009 2010 5   30.000        23.999979
        # ::  rather than:
        # ::     2009 10 1    0.000         0.569902
        # ::
        # :: I thought this was b/c numpy.float32 (and 64) are smaller than c_float, however this change
        # :: below didn't fix the problem.
        # ::
        # create a numpy array for outputs
        self.outvarArray = numpy.zeros(shape=(numOut+1, self.numTimeStep+1), dtype=numpy.float, order="C")
        # arrays_old = self.outvarArray.astype(numpy.float32)
        arrays = self.outvarArray.astype(c_float)
        rows, cols = self.outvarArray.shape
        arrays_as_list = list(arrays)
        #get ctypes handles
        ctypes_arrays = [numpy.ctypeslib.as_ctypes(array) for array in arrays_as_list]
        #Pack into pointer array
        self.C_outvarArray = (POINTER(c_float) * rows)(*ctypes_arrays)

        # x = numpy.zeros(shape=(numOut, self.numTimeStep), dtype=numpy.float, order="C")
        # _floatpp = numpy.ctypeslib.ndpointer(dtype=numpy.uintp, ndim=1, flags='C')
        # xpp = (x.__array_interface__['data'][0] + numpy.arange(x.shape[0])*x.strides[0]).astype(numpy.uintp)
        # self.C_outvarArray = pointer(((POINTER(c_float) * self.numTimeStep) * numOut)())


        # a = (c_float * self.numTimeStep)()
        # outvarArray = pointer((a * numOut)())
        # for i in xrange(numOut):
        #     outvarArray[i] = pointer((c_float * self.numTimeStep)())

        # total grid size to compute progess
        totalgrid = self.C_dimlen1.value*self.C_dimlen2.value

        # read output control file (main.cpp, line 251)
        # readOutputControl(outputconFile, aggoutputconFile, pOut, ncOut, aggOut, npout, nncout, naggout);

        self.__uebLib.readOutputControl(cast(C_outputconFile,c_char_p), cast(C_aggoutputconFile, c_char_p),
                                        byref(self.C_pOut), byref(self.C_ncOut), byref(C_aggOut),
                                        byref(self.C_npout), byref(self.C_nncout), byref(C_naggout))


        # create output netcdf
        self.C_outtSteps = self.numTimeStep / self.outtStride
        self.t_out = numpy.empty(shape=(self.C_outtSteps), dtype=numpy.float, order="C")
        for i in xrange(self.C_outtSteps):
            self.t_out[i] = i*self.outtStride*ModelDt

        # initialize the output arrays
        aggoutvarArray = numpy.zeros((C_nZones,C_naggout.value, self.C_outtSteps), dtype=numpy.float)
        totalAgg = numpy.empty((self.C_outtSteps,), dtype=numpy.float)
        ZonesArr = numpy.zeros((C_nZones,), dtype=numpy.int32)

        # main.cpp, line 290
        # CREATE 3D NC OUTPUT FILES
        # convert self.t_out into a float pointer
        C_t_out = self.t_out.ctypes.data_as(POINTER(c_float))
        for i in xrange(self.C_nncout.value):
            '''
            for (int icout = 0; icout < nncout; icout++)
                retvalue = create3DNC_uebOutputs(ncOut[icout].outfName, (const char*)ncOut[icout].symbol, (const char*)ncOut[icout].units, tNameout, tUnitsout,
            tlong_name, tcalendar, outtSteps, outDimord, self.t_out, &out_fillVal, watershedFile, wsvarName, wsycorName, wsxcorName);
            '''

            retvalue = self.__uebLib.create3DNC_uebOutputs(self.C_ncOut[i].outfName, cast(self.C_ncOut[i].symbol, c_char_p), cast(self.C_ncOut[i].units, c_char_p), C_tNameout, C_tUnitsout, C_tlong_name, C_tcalendar, self.C_outtSteps, self.C_outDimord, C_t_out, byref(C_out_fillVal), C_watershedFile, C_wsvarName, C_wsycorName, C_wsxcorName);

        # CREATE 3D NC AGGREGATE OUTPUT FILE
        # convert z_ycor and x_xcor from list into ctype
        C_z_xcor = numpy.asarray(z_xcor).ctypes.data_as(POINTER(c_float))
        C_z_ycor = numpy.asarray(z_ycor).ctypes.data_as(POINTER(c_float))
        retvalue = self.__uebLib.create3DNC_uebAggregatedOutputs(C_aggoutputFile, C_aggOut, C_naggout, C_tNameout, C_tUnitsout, C_tlong_name, C_tcalendar, self.C_outtSteps, C_aggoutDimord, C_t_out, byref(C_out_fillVal), C_watershedFile, C_wsvarName, C_wsycorName, C_wsxcorName, C_nZones, C_zName, C_z_ycor, C_z_xcor);


        # todo: create output element set
        print 'Output Calculations available at: '
        for pid in xrange(self.C_npout.value):
            print "  Point(",self.C_pOut[pid].xcoord,", ",self.C_pOut[pid].ycoord,') '



        # todo: This is where UEB grid points are defined!, expose these as input/output spatial objects
        # main.cpp, line 303
        self.activeCells = []
        # print 'Calculations will be performed at: '
        for iy in xrange(self.C_dimlen1.value):
            for jx in xrange(self.C_dimlen2.value):
                if self.C_wsArray[iy][jx] != self.C_wsfillVal.value and self.C_strsvArray.contents[16].svType != 3:
                    # print "  Point(",jx,", ",iy,') '
                    self.activeCells.append((iy, jx))

        # build output exchange items
        xcoords = []
        ycoords = []
        for pid in xrange(self.C_npout.value):
            xcoords.append(self.C_pOut[pid].xcoord)
            ycoords.append(self.C_pOut[pid].ycoord)
        pts = geometry.build_point_geometries(xcoords, ycoords)
        self.outputs()['Snow Melt Equivalent'].addGeometries2(pts)



        print 'initialization successful'



    def run(self, inputs):

        # todo: Do ts variable all have the same shape (i.e. same timestep?)
        # NOTES:
        # C_tsvarArray (or RegArray in RunUEB C code) stores the time series values for all inputs
        # C_tsvarArray[0] --> Ta  (air temp)
        # C_tsvarArray[1] --> Precipitation (mm/day)
        # C_tsvarArray[2] --> V  (wind speed)
        # C_tsvarArray[3] --> RH (relative humidity)
        # C_tsvarArray[4] --> atmospheric pressure ?
        # C_tsvarArray[5] --> Qsiobs
        # C_tsvarArray[6] --> Qli
        # C_tsvarArray[7] --> Qnetob
        # C_tsvarArray[8] --> Qg
        # C_tsvarArray[9] --> Snowalb
        # C_tsvarArray[10] --> Tmin
        # C_tsvarArray[11] --> Tmax
        # C_tsvarArray[12] --> Vapor Pressure of air

        elog.info("\nBegin UEB Computation")

        # get output exchange items
        sme = self.outputs()['Snow Melt Equivalent']




        # Initialize SiteState
        SiteState = numpy.zeros((32,))

        # loop over all activeCells
        for i in xrange(len(self.activeCells)):

            # todo: remove, this is for debugging
            # if i > 10:
            #     break

            # track grid cell
            self.C_uebCellY = self.activeCells[i][0]
            self.C_uebCellX = self.activeCells[i][1]

            for s in xrange(32):
                if self.C_strsvArray.contents[s].svType == 1:
                    SiteState[s] = self.C_strsvArray.contents[s].svArrayValues[self.C_uebCellY][self.C_uebCellX]
                else:
                    SiteState[s] = self.C_strsvArray.contents[s].svdefValue

            # convert SiteState into a ctype
            C_SiteState = (c_float * len(SiteState))(*SiteState)

            for t in xrange(13):

                # HACK: Everything inside this 'if' statement needs to be checked!!!!

                # todo: what does infType == 1 mean?
                if self.C_strinpforcArray.contents[t].infType == 1:
                    print 'You are in un-tested code! '
                    ncTotaltimestep = 0;

                    for numNc in xrange(self.C_strinpforcArray[it].numNcfiles):
                        # read 3D netcdf data
                        tsInputfile = self.C_strinpforcArray[t].infFile + numNc + '.nc'

                        retvalue = self.__uebLib.readNC_TS(tsInputfile, self.C_strinpforcArray.contents[t].infvarName, self.C_strinpforcArray.contents[t].inftimeVar, C_wsycorName, C_wsxcorName, byref(C_tsvarArrayTemp[numNc]), byref(C_tcorvar[it]), self.C_uebCellY, self.C_uebCellX, byref(C_ntimesteps[numNc]));

                        ncTotaltimestep += C_ntimesteps[numNc];

                    self.C_tsvarArray[t] = (c_float * ncTotaltimestep)
                    tinitTime = 0
                    for numNc in xrange(self.C_strinpforcArray.contents[t].numNcFiles):
                        for tts in xrange(C_ntimesteps[numNc]):
                            self.C_tsvarArray.contents[t][tts + tinitTime] = C_tsvarArrayTemp.contents[numNc][tts]
                        tinitTime += C_ntimesteps[numNc]



            # RUN THE UEB CALCS
            ModelStartHour = 1

            self.__uebLib.RUNUEB(self.C_tsvarArray, C_SiteState, self.C_parvalArray, byref(pointer(self.C_outvarArray)), self.C_ModelStartDate, self.C_ModelStartHour, self.C_ModelEndDate, self.C_ModelEndHour, self.C_ModelDt, self.C_ModelUTCOffset);

            if i % 10 == 0:
                elog.info("%d of %d elements complete " % ((i+1), len(self.activeCells)))


        # # todo: set output data (point)
        # print 'set output data'

            # todo: make more efficient
            # write point outputs
            for i in xrange(self.C_npout.value):
                if self.C_uebCellY == self.C_pOut[i].ycoord and self.C_uebCellX == self.C_pOut[i].xcoord:
                    print '\n' + 100 *'-'
                    print 'Writing Output for Point :  %d, %d' % ( self.C_uebCellX, self.C_uebCellY)
                    # print 'Year, Month, Day, Hour, Ta, P, Ws, SWISM, SWIR, errMB '
                    for step in xrange(self.numTimeStep):
                        # print '%d %d %d %8.3f %16.6f %16.6f %16.6f %16.6f %16.6f %16.6f' % (self.C_outvarArray[0][step],  self.C_outvarArray[1][step], self.C_outvarArray[2][step], self.C_outvarArray[3][step], self.C_outvarArray[9][step], self.C_outvarArray[10][step],self.C_outvarArray[17][step],self.C_outvarArray[67][step],self.C_outvarArray[68][step], self.C_outvarArray[69][step])
                        print '%d %d %d %8.3f %16.6f %16.6f %16.6f %16.6f' % (self.C_outvarArray[0][step],  self.C_outvarArray[1][step], self.C_outvarArray[2][step], self.C_outvarArray[3][step], self.C_outvarArray[4][step], self.C_outvarArray[5][step],self.C_outvarArray[6][step],self.C_outvarArray[7][step])

                        if step == 10:
                            print "...\n", 100*'-'
                            break

        print 'Run Complete'

    def save(self):


        # write nc output
        for i in xrange(self.C_nncout.value):
            for j in xrange(70):
                if self.C_ncOut[i].symbol == self.uebVars[j]:
                    self.outvarindx.value = j;
                    break
            for j in xrange(self.C_outtSteps):
                self.t_out[j] = self.C_outvarArray[self.outvarindx.value][self.outtStride*j]

            print 'Writing Output: ', os.path.join(self.curdir, self.C_ncOut[i].outfName)
            C_t_out = self.t_out.ctypes.data_as(POINTER(c_float))
            retvalue = self.__uebLib.WriteTSto3DNC(cast(os.path.join(self.curdir, self.C_ncOut[i].outfName), c_char_p), cast(self.C_ncOut[i].symbol, c_char_p), self.C_outDimord, self.C_uebCellY, self.C_uebCellX, self.C_outtSteps, C_t_out)

        # write point outputs
        for i in xrange(self.C_npout.value):
            # todo: this is inefficient
            if self.C_uebCellY == self.C_pOut[i].ycoord and self.C_uebCellX == self.C_pOut[i].xcoord:
                print 'Writing Output: ', self.C_pOut[i].outfName
                with open(self.C_pOut[i].outfName, 'w') as f:
                    for step in xrange(self.numTimeStep):
                        f.write("\n %d %d %d %8.3f " % (self.C_outvarArray[0][step],  self.C_outvarArray[1][step], self.C_outvarArray[2][step], self.C_outvarArray[3][step]) )
                        for vnum in range(4,70):
                            f.write(" %16.6f " % self.C_outvarArray[vnum][step])

        # # write aggregated outputs
        # zoneid = wsArray[uebCellY][uebCellX] - 1
        # ZonesArr[zoneid] += 1
        # for i in xrange(naggout):
        #     # todo: this is inefficient
        #     for v in xrange(70):
        #         if aggOut[i].symbol == self.uebVars[v]:
        #             aggoutvarindx = v
        #             break
        #     for t in xrange(outtSteps):
        #         aggoutvarArray[zoneid][i][t] += self.outvarArray[aggoutvarindx][self.outtStride*t]
        #
        # for i in xrange(naggout):

        # unload ueb
        del self.__uebLib


    def initialize_timeseries_variable_array(self, forcing_data, number_of_timesteps):


        # initialize the arrays base on number of timesteps.  This assumes that all datasets share a timestep
        self.C_tsvarArray.contents[0] = (c_float * number_of_timesteps)()  # air temp
        self.C_tsvarArray.contents[1] = (c_float * number_of_timesteps)()  # precipitation
        self.C_tsvarArray.contents[2] = (c_float * number_of_timesteps)()  # windspeed
        self.C_tsvarArray.contents[3] = (c_float * number_of_timesteps)()  # relative humidity
        self.C_tsvarArray.contents[10] = (c_float * number_of_timesteps)()  # Min Air temperature
        self.C_tsvarArray.contents[11] = (c_float * number_of_timesteps)()  # Max Air temperature

        # initialize parameter values
        for i in [4,5,6,7,8,9,12]:
            #  4: AP: Air pressure   (always required)
            #  5: Qsi: Incoming shortwave(kJ/m2/hr)   (only required if irad=1 or 2)
            #  6: Qli: Long wave radiation(kJ/m2/hr)
            #  7: Qnet: Net radiation(kJ/m2/hr)   (only required if irad=3)
            #  8: Qg: Ground heat flux   (kJ/m2/hr)
            #  9: Snowalb: Snow albedo (0-1).  (only required if ireadalb=1) The albedo of the snow surface to be used when the internal albedo calculations are to be overridden
            # 12: Vp: Air vapor pressure
            self.C_tsvarArray.contents[i] = (c_float * 2)()  # Qsi: Incoming shortwave(kJ/m2/hr)
            self.C_tsvarArray.contents[i][0] = self.C_strinpforcArray.contents[i].infType
            self.C_tsvarArray.contents[i][1] = self.C_strinpforcArray.contents[i].infdefValue

        variables = {'Ta':0, 'Prec':1, 'v':2, 'RH':3, 'AP':4, 'Qsi':5, 'Qli':6, 'Qnet':7, 'Qg':8, 'Snowalb':9, 'Tmin':10, 'Tmax':11, 'Vp':12}

        # populate data (loop over the strinpforcArray)
        for i in range(13):

            # get the variable name
            var_name = self.C_strinpforcArray.contents[i].infName

            # get the index corresponding to this variable
            idx = variables[var_name]

            if self.C_strinpforcArray.contents[i].infType == 0:
                # read DAT file
                with open(os.path.join(self.base_dir, self.C_strinpforcArray.contents[i].infFile), 'r') as f:
                    lines = f.readlines()
                    row = 0
                    for l in range(1, len(lines)):
                        # DAT format:  Year	Month	Day	Hour	value
                        data = lines[l].strip().split()

                        # save the value column
                        self.C_tsvarArray.contents[idx][row] = float(data[-1])

                        # increment the row
                        row += 1

        print 'done'



