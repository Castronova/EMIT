__author__ = 'tonycastronova'

import datetime
import math

import netCDF4 as nc
import numpy

import jdutil
import stdlib
from emitLogging import elog
from sprint import *
from structures import *
from utilities import mdl, geometry
from wrappers import feed_forward


class ueb(feed_forward.Wrapper):

    def __init__(self, config_params):
        super(ueb,self).__init__(config_params)

        # build inputs and outputs
        # elog.info('Building exchange items')
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
            ModelUTCOffset = float(lines[12])
            inpDailyorSubdaily = bool(lines[13]==True)
            self.outtStride, outyStep, outxStep = [int(s) for s in lines[14].split(' ')]


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
        # aggoutvarindx = c_int(17)
        # size = c_int()
        # rank = c_int()
        # irank = c_int()
        # jrank = c_int()
        # startTimeT = c_double(0.0)
        # TotalTime = c_double(0.0)
        # totalmodelrunTime = c_double(0.0)
        # TsReadTime = c_double(0.0)
        # TSStartTime = c_double()
        # ComputeStartTime = c_double()
        # ComputeTime = c_double(0.0)
        # OutWriteTime = c_double()

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
                # print "%d %s %s\n" % (i, a.svFile,a.svVarName)
                retvalue = self.__uebLib.read2DNC(os.path.join(self.base_dir, a.svFile), a.svVarName, byref(a.svArrayValues))


        #//read input /forcing control file--all possible entries of input control have to be provided
        #readInputForcVars(inputconFile, strinpforcArray);

        # read input force variables (main.cpp, line 219)
        self.__uebLib.readInputForcVars(cast(C_inputconFile,c_char_p), self.C_strinpforcArray)


        # elog.info('UEB Start Date: %s' % sd.strftime("%m-%d-%Y %H:%M:%S"))
        # elog.info('UEB End Date: %s' % ed.strftime("%m-%d-%Y %H:%M:%S"))

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
        self.numTimeStep = int(math.ceil(modelSpan*(24./ModelDt)) ) + 1

        # initialize C_tsvarArray values (this replaces __uebLib.readTextData)
        self.initialize_timeseries_variable_array(self.C_strinpforcArray, self.numTimeStep)

        # NOTE: C_strinpforcArray stores info about the forcing data files

        # # read forcing data (main.cpp, line 226)
        # if self.C_strsvArray.contents[16].svType != 3: # no accumulation zone (fixme: ???)
        #     for it in xrange(13):
        #         inftype = self.C_strinpforcArray.contents[it].infType
        #         print 'infFile: ',self.C_strinpforcArray.contents[it].infFile
        #         if inftype == 0:
        #
        #             # read the files stored in C_strinpforcArray and populated C_tsvarArray
        #             self.__uebLib.readTextData(os.path.join(self.base_dir, self.C_strinpforcArray.contents[it].infFile), byref(self.C_tsvarArray.contents[it]), byref(C_ntimesteps[0]))
        #
        #         elif inftype == 2 or inftype == -1:
        #             self.C_tsvarArray.contents[it] = (c_float * 2)()
        #             C_ntimesteps.contents[0] = 2
        #             # copy the default value if a single value is the option
        #             self.C_tsvarArray.contents[it][0] = self.C_strinpforcArray.contents[it].infType
        #             self.C_tsvarArray.contents[it][1] = self.C_strinpforcArray.contents[it].infdefValue


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
        self.outvarArray = numpy.zeros(shape=(numOut+1, self.numTimeStep), dtype=numpy.float, order="C")
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
        # print 'Output Calculations available at: '
        # for pid in xrange(self.C_npout.value):
        #     print "  Point(",self.C_pOut[pid].xcoord,", ",self.C_pOut[pid].ycoord,') '



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
        self.pts = geometry.build_point_geometries(xcoords, ycoords)
        self.__swe = self.outputs()['Snow Water Equivalent']
        self.__swit = self.outputs()['Surface Water Input Total']
        self.__swe.addGeometries2(self.pts)
        self.__swit.addGeometries2(self.pts)



        # build input exchange items
        ds = nc.Dataset(C_watershedFile)
        Xlist = ds.variables['x']
        Ylist = ds.variables['y']
        self.geoms = self.build_geometries(Xlist, Ylist)
        self.inputs()['Precipitation'].addGeometries2(self.geoms)
        self.inputs()['Temperature'].addGeometries2(self.geoms)

        # set start, end, and timestep parameters
        ts = datetime.timedelta(hours=ModelDt)
        self.time_step(ts.total_seconds())
        sd = datetime.datetime(*ModelStartDate)
        ed = datetime.datetime(*ModelEndDate)
        self.simulation_start(sd)
        self.simulation_end(ed)



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

        # # get output exchange items
        # self.swe = self.outputs()['Snow Water Equivalent']
        # swit = self.outputs()['Surface Water Input Total']

        try:

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


                # todo: get all data at beginning of run, then slice as necessary here
                # get the input data for the current geometry
                prcp = self.inputs()['Precipitation'].getValues2(geom_idx_start=i, geom_idx_end=i)
                temp = self.inputs()['Temperature'].getValues2(geom_idx_start=i, geom_idx_end=i)

                # skip calculation if no temperatures are provided for the current point (i.e completely missing data)
                if max(temp[:-1]) > 0:
                    # set the input data for this geometry
                    for idx in range(len(prcp)):
                        # set air temperature and precipitation values in tsvarArray (index 0 and 1)
                        self.C_tsvarArray.contents[0][idx] = temp[idx][0]
                        self.C_tsvarArray.contents[1][idx] = prcp[idx][0]

                    # RUN THE UEB CALCS
                    self.__uebLib.RUNUEB(self.C_tsvarArray, C_SiteState, self.C_parvalArray,
                                         byref(pointer(self.C_outvarArray)), self.C_ModelStartDate, self.C_ModelStartHour,
                                         self.C_ModelEndDate, self.C_ModelEndHour, self.C_ModelDt, self.C_ModelUTCOffset)

                    # outvararray 70var * numtimesteps

                # set output data
                numtimesteps = len(self.__swe.getDates2())
                values = numpy.array(self.C_outvarArray[17][0:numtimesteps])            # convert C_type into numpy array
                values[numpy.isnan(values)] = self.__swe.noData()                       # set nan values to noData
                self.__swe.setValuesBySlice(values, geometry_index_slice=(i, i+1, 1))   # set data in wrapper

                values = numpy.array(self.C_outvarArray[25][0:numtimesteps])            # convert C_type into numpy array
                values[numpy.isnan(values)] = self.__swit.noData()                      # set nan values to noData
                self.__swit.setValuesBySlice(values, geometry_index_slice=(i, i+1, 1))  # set data in wrapper


                # if i % round((len(self.activeCells)) / 10) == 0:
                # print "%d of %d elements complete " % ((i+1), len(self.activeCells))
                # sys.stdout.flush()
                # elog.info("... %d of %d elements complete " % ((i+1), len(self.activeCells)), overwrite=True)

        except Exception, e:
            elog.critical('UEB run failed: %s' % e)
            sPrint('An error was encountered while running the UEB model: %s' % e)
            return False



    def finish(self):


        # write nc output
        for i in xrange(self.C_nncout.value):
            for j in xrange(70):
                if self.C_ncOut[i].symbol == self.uebVars[j]:
                    self.outvarindx.value = j;
                    break
            for j in xrange(self.C_outtSteps):
                self.t_out[j] = self.C_outvarArray[self.outvarindx.value][self.outtStride*j]

            # print 'Writing Output: ', os.path.join(self.curdir, self.C_ncOut[i].outfName)
            C_t_out = self.t_out.ctypes.data_as(POINTER(c_float))
            retvalue = self.__uebLib.WriteTSto3DNC(cast(os.path.join(self.curdir, self.C_ncOut[i].outfName), c_char_p), cast(self.C_ncOut[i].symbol, c_char_p), self.C_outDimord, self.C_uebCellY, self.C_uebCellX, self.C_outtSteps, C_t_out)

        # write point outputs
        for i in xrange(self.C_npout.value):
            # todo: this is inefficient
            if self.C_uebCellY == self.C_pOut[i].ycoord and self.C_uebCellX == self.C_pOut[i].xcoord:
                # print 'Writing Output: ', self.C_pOut[i].outfName
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
        # number_of_timesteps += 10
        variables = {'Ta':0, 'Prec':1, 'v':2, 'RH':3, 'AP':4, 'Qsi':5, 'Qli':6, 'Qnet':7, 'Qg':8, 'Snowalb':9, 'Tmin':10, 'Tmax':11, 'Vp':12}

        # loop over all of the variables
        for i in range(13):

            # get the variable name
            var_name = self.C_strinpforcArray.contents[i].infName

            # get the index corresponding to this variable
            idx = variables[var_name]

            # get the type of input forcing (0: dat, 1: netcdf, 2: parameter)
            infType = self.C_strinpforcArray.contents[i].infType

            # dat file
            if infType == 0:

                # initialize the array
                self.C_tsvarArray.contents[i] = (c_float * number_of_timesteps)()

                # read the DAT file and set data
                with open(os.path.join(self.base_dir, self.C_strinpforcArray.contents[i].infFile), 'r') as f:
                    lines = f.readlines()
                    row = 0
                    for l in range(1, len(lines)):
                        # DAT format:  Year	Month	Day	Hour	value
                        data = lines[l].strip().split()

                        # save the value column
                        self.C_tsvarArray.contents[i][row] = float(data[-1])

                        # increment the row
                        row += 1

            # netcdf file
            elif infType == 1:

                # # initialize the array
                self.C_tsvarArray.contents[i] = (c_float * number_of_timesteps)()

                message = 'NetCDF input files are not supported at this time.  Pass NetCDF values at runtime via data components instead.'
                elog.warning(message)

                # # initialize the array
                # self.C_tsvarArray.contents[i] = (c_float * number_of_timesteps)()

                # # get netcdf variables
                # tvar = self.C_strinpforcArray.contents[i].inftimeVar
                # var = self.C_strinpforcArray.contents[i].infvarName
                # numfiles =  self.C_strinpforcArray.contents[i].numNcfiles
                # # todo add support for multiple netcdf files
                # if numfiles > 1: raise Exception('Cannot process multiple netcdf files for a single variable.  Support for this feature is coming soon.')
                # f = self.C_strinpforcArray.contents[i].infFile
                # f = f + '0.nc' if f[-2:] != '.nc' else f
                #
                # # read netcdf data and set values
                # handle = nc.Dataset(os.path.join(self.base_dir, f), 'r')
                # values = [v.flatten() for v in handle.variables[var][:]]
                # for row in range(len(values)):
                #     self.C_tsvarArray.contents[i][row] = values[row]


            # parameter value
            elif infType == 2:

                # initialize space for parameters and set values
                self.C_tsvarArray.contents[i] = (c_float * 2)()
                self.C_tsvarArray.contents[i][0] = self.C_strinpforcArray.contents[i].infType
                self.C_tsvarArray.contents[i][1] = self.C_strinpforcArray.contents[i].infdefValue


            # input component
            elif infType == 3:

                # initialize the array
                self.C_tsvarArray.contents[i] = (c_float * number_of_timesteps)()

                pass

            # variable not used (computed internally)
            else:
                self.C_tsvarArray.contents[i] = (c_float * 2)()
                self.C_tsvarArray.contents[i][0] = self.C_strinpforcArray.contents[i].infType
                self.C_tsvarArray.contents[i][1] = self.C_strinpforcArray.contents[i].infdefValue



        # # initialize the arrays base on number of timesteps.  This assumes that all datasets share a timestep
        # self.C_tsvarArray.contents[0] = (c_float * number_of_timesteps)()  # air temp
        # self.C_tsvarArray.contents[1] = (c_float * number_of_timesteps)()  # precipitation
        # self.C_tsvarArray.contents[2] = (c_float * number_of_timesteps)()  # windspeed
        # self.C_tsvarArray.contents[3] = (c_float * number_of_timesteps)()  # relative humidity
        # self.C_tsvarArray.contents[10] = (c_float * number_of_timesteps)()  # Min Air temperature
        # self.C_tsvarArray.contents[11] = (c_float * number_of_timesteps)()  # Max Air temperature
        #
        # # initialize parameter values
        # for i in [4,5,6,7,8,9,12]:
        #     #  4: AP: Air pressure   (always required)
        #     #  5: Qsi: Incoming shortwave(kJ/m2/hr)   (only required if irad=1 or 2)
        #     #  6: Qli: Long wave radiation(kJ/m2/hr)
        #     #  7: Qnet: Net radiation(kJ/m2/hr)   (only required if irad=3)
        #     #  8: Qg: Ground heat flux   (kJ/m2/hr)
        #     #  9: Snowalb: Snow albedo (0-1).  (only required if ireadalb=1) The albedo of the snow surface to be used when the internal albedo calculations are to be overridden
        #     # 12: Vp: Air vapor pressure
        #     self.C_tsvarArray.contents[i] = (c_float * 2)()  # Qsi: Incoming shortwave(kJ/m2/hr)
        #     self.C_tsvarArray.contents[i][0] = self.C_strinpforcArray.contents[i].infType
        #     self.C_tsvarArray.contents[i][1] = self.C_strinpforcArray.contents[i].infdefValue
        #
        #
        #
        # # populate data (loop over the strinpforcArray)
        # for i in range(13):
        #
        #     # get the variable name
        #     var_name = self.C_strinpforcArray.contents[i].infName
        #
        #     # get the index corresponding to this variable
        #     idx = variables[var_name]
        #
        #     if self.C_strinpforcArray.contents[i].infType == 0:
        #         # read DAT file
        #         with open(os.path.join(self.base_dir, self.C_strinpforcArray.contents[i].infFile), 'r') as f:
        #             lines = f.readlines()
        #             row = 0
        #             for l in range(1, len(lines)):
        #                 # DAT format:  Year	Month	Day	Hour	value
        #                 data = lines[l].strip().split()
        #
        #                 # save the value column
        #                 self.C_tsvarArray.contents[idx][row] = float(data[-1])
        #
        #                 # increment the row
        #                 row += 1


    def build_geometries(self, xcoords, ycoords):
        """
        builds point geometries consistent with the native UEB ordering
        :param xcoords:  list of x coordinates
        :param xyoords:  list of xycoordinates
        :return: a list of geometries
        """

        # build a meshgrid
        x, y = numpy.meshgrid(xcoords, ycoords)

        # x any y coords are paired using Fortran ordering to be consistent with the way activeCells are ordered.  This
        # is necessary to ensure that calculation looping is maintained in the run function.
        x = numpy.ravel(x, 'F')
        y = numpy.ravel(y, 'F')

        # build point geometries
        return geometry.build_point_geometries(x, y)



"""
Metadata Notes:

C_outvar_Array
        0	Year	        Year
        1	Month           Month
        2	Day	            Day
        3	dHour	        dHour
        4	atff	        Atmospheric transmission factor
        5	HRI	            Radiation index
        6	Eacl	        Clear sky emissivity
        7	Ema	            Atmospheric emissivity
        8	conZen	        Cos of solar zenith angle (Zen)
        9	Ta	            Air temperature(C)
        10	P	            Precipitation (m/hr)
        11	V	            Wind speed (m/s)
        12	RH	            Relative humidity
        13	Qsi	            Incoming solar radiation (kJ/m2/hr)
        14	Qli	            Incoming longwave radiation (kJ/m2/hr)
        15	Qnet	        Input net radiation (kJ/m2/hr)
        16	Us	            Energy content (kJ/m2)
        17	Ws	            Surface snow water equivalent (m)
        18	tausn	        Dimensionless age of the snow surface
        19	Pr	            Precipitation in the form of rain (m/hr)
        20	Ps	            Precipitation in the form of snow (m/hr)
        21	Alb	            Snow surface albedo
        22	QHs	            Surface Sensible heat flux (kJ/m2/hr)
        23	QEs	            Surface Latent heat flux (kJ/m2/hr)
        24	Es	            Surface sublimation (m)
        25	SWIT	        Total outflow (m/hr).  This combines rainfall (in the case of no snow/glacier)
                              snow/glacier melt, and it the surface water input to the runoff generation process.
        26	QMs	            Surface melt energy (kJ/m2/hr)
        27	Q	            Net surface energy exchange (kJ/m2/hr)
        28	FM	            Net surface mass exchange (m/h)
        29	Tave	        Average snow temperature (C)
        30	TSURFs	        Surface snow temperature (C)
        31	cump	        Cumulative precipitation (m)
        32	cumes	        Cumulative surface sublimation (m)
        33	cumMr	        Cumulative surface melt (m)
        34	Qnet	        Modeled surface net radiation (kJ/m2/hr)
        35	smelt	        Melt generated at surface (m/hr).  This is melt generated at the surface and modeled to
                            infiltrate into the snow or glacier where it may refreeze.  It is not base of the
                            snow/glacier outflow.
        36	refDepth	    Depth of penetration of top refreezing (m)
        37	totalRefDepth	Total depth of refreezing (m)
        38	cf	            Cloudiness fraction
        39	Taufb	        Direct solar radiation fraction
        40	Taufd	        Diffuse solar radiation fraction
        41	Qsib	        Direct solar radiation
        42	Qsid	        Diffuse solar radiation
        43	Taub	        Direct solar radiation canopy transmission fraction
        44	Taud	        Diffuse solar radiation canopy transmission fraction
        45	Qsns	        Solar radiation absorbed at surface (kJ/m2/hr)
        46	Qsnc	        Solar radiation absorbed in canopy (kJ/m2/hr)
        47	Qlns	        Longwave radiation absorbed a tsurface (kJ/m2/hr)
        48	Qlnc 	        Longwave radiation absorbed in canopy (kJ/m2/hr)
        49	Vz	            Modeled wind beneath canopy (m/s)
        50	Rkinsc	        Was canopy aerodynamic resistance -not used presently
        51	Rkinc	        Aerodynamic resistance of surface (below canopy)
        52	Inmax	        Canopy snow interception capacity (m)
        53	intc	        Canopy snow interception (m/hr)
        54	ieff	        Fraction of precipitation intercepted (m/hr)
        55	Ur	            Canopy mass unloading (m/hr)
        56	Wc	            Canopy snow water equivalent (m)
        57	Tc	            Canopy temperature(C)
        58	Tac	            Air temperature within canopy (C)
        59	QHc	            Canopy sensible heat flux (kJ/m2/hr)
        60	QEc	            Canopy latent heat flux (kJ/m2/hr)
        61	Ec	            Canopy sublimation (m/hr)
        62	Qpc	            Precipitation energy advected to canopy (kJ/m2/hr)
        63	Qmc	            Canopy melt energy (kJ/m2/hr)
        64	Mc	            Melt from canopy (m/hr)
        65	FMc	            Net canopy energy exchange (m/hr)
        66	SWIGM	        Glacier melt outflow (m/hr).  This is the part of total outflow that originates from
                            glacier melting.
        67	SWISM	        Rainfall outflow (m/hr).  This is the part of total outflow that is from rainfall in the
                            case of no snow/glacier.
        68	SWIR	        Snow melt outflow (m/hr).  This is the part of total outflow that originates from the
                            melting of seasonal snow pack (as distinct from glacier ice)
        69	errMB	        Mass balance closure error (m)
"""