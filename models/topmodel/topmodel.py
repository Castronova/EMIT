__author__ = 'tonycastronova'

import os
from wrappers import feed_forward
import stdlib
from utilities import mdl, spatial
import math
from shapely.geometry import Point
from coordinator.emitLogging import elog
import numpy as np


class topmodel(feed_forward.feed_forward_wrapper):


    def __init__(self,config_params):
        """
        initialization that will occur when loaded into a configuration

        """

        super(topmodel,self).__init__(config_params)

        elog.info('Begin Component Initialization')

        # build inputs and outputs
        elog.info('Building exchange items')
        io = mdl.build_exchange_items_from_config(config_params)

        # set inputs and outputs
        self.inputs(value=io['input'])
        self.outputs(value=io['output'])

        # model_inputs
        inputs = config_params['model inputs'][0]

        # read input parameters
        elog.info('Reading input parameters')
        self.topo_input = inputs["ti"];
        self.fac_input = inputs["fac"];

        #read model input parameters
        self.c = float(inputs['m'])
        self.Tmax = float(inputs["tmax"])
        self.R = float(inputs["r"])
        self.interception = float(inputs["interception"])
        self.ti = []
        self.freq = []

        # read topographic input file
        elog.info('Reading topographic input data')
        self.read_topo_input()

        elog.info('Building input/output geometries')
        self.ti_geoms = None
        self.output_soil_moisture_geoms = None
        self.calc_ti_geometries()

        # set precipitation geometries
        elog.info('Setting excess precipitation geometries')
        self.outputs()['excess'].addGeometries2(self.ti_geoms)

        # set saturation geometries
        # elog.info('Setting soil saturation geometries')
        # self.outputs()['soil moisture'].addGeometries2(self.ti_geoms)

        # ---- calculate saturation deficit
        elog.info('Calculating initial saturation deficit')
        TI_freq = [x*y for x,y in zip(self.ti, self.freq)]

        self.lamda_average = sum(TI_freq) / sum(self.freq)

        # catchment average saturation deficit(S_bar)
        self.s_average = (-1.)*self.c * ((math.log10(self.R / self.Tmax)) + self.lamda_average)

        elog.info('Component Initialization Completed Successfully')

    def run(self,inputs):



        precipitation = inputs['precipitation']
        vals = precipitation.getValues2()
        datetimes = precipitation.getDates2()

        # get output exchange items
        runoff = self.outputs()['excess']

        et = 0.0   # todo: this should be an input
        sat_deficit = np.zeros(len(self.ti))

        # elog.debug('Executing TOPMODEL... timestep [0 of %s]'%str(len(datetimes)))

        # loop through entire time horizon
        for i in range (0, len(datetimes)):

            # initialize arrays
            overland_flow = np.zeros(len(self.ti))  #Infiltration excess
            reduced_ET = np.zeros(len(self.ti)) #Reduced ET due to dryness
            MM = np.zeros(len(self.ti))
            NN = np.zeros(len(self.ti))

            # get current datetime
            idx, date = datetimes[i]

            # get precip at the current time
            precip = precipitation.getValues2(time_idx = i)

            #todo: this is a hack because i'm running out of time before the demo
            # todo: something is wrong with the data interpolation!
            p = precip[0][0]
            if isinstance(p, np.ndarray):
                precip = p[0]
            else:
                precip = p
            # precip = precip[0][0][0]

            # calculate saturation deficit
            sat_deficit = [self.s_average + self.c * (self.lamda_average - ti) for ti in self.ti]

            # account for interception and et
            p = max(0, (precip - et))
            sat_deficit = [s - p + et for s in sat_deficit]

            q_infiltration = p - et

            if q_infiltration > 0:

                for i in range(0, len(self.ti)):
                    if sat_deficit[i] < 0:
                        overland_flow[i] = -1*sat_deficit[i]
                        sat_deficit[i] = 0
                    else:
                        overland_flow[i] = 0

                    MM[i] = self.freq[i] * overland_flow[i]

            else:
                for i in range(0, len(self.ti)):
                    if sat_deficit[i] > 5000:
                        reduced_ET[i] = -5000 + sat_deficit[i]
                        sat_deficit[i] = 5000
                    else:
                        reduced_ET[i] = 0

                    NN[i] = self.freq[i] * reduced_ET[i]

                # todo: calculate sum(freq) outside of this loop, possibly in initialize
                q_infiltration += sum(NN) / sum(self.freq)


            q_subsurface = self.Tmax * (math.exp(-self.lamda_average)) * (math.exp(-self.s_average / self.c))
            q_overland = sum(MM) / sum(self.freq);

            # calculate the new average deficit using catchment mass balance
            self.s_average = self.s_average + q_subsurface + q_overland - q_infiltration

            # calculating runoff q
            q = q_overland + q_subsurface

            # save these data
            runoff.setValues2(q, date)
            # elog.info('OVERWRITE:Executing TOPMODEL... timestep [%d of %d]'%(i, len(datetimes)), True)
            # print precip, q

        return 1

    def save(self):
        return self.outputs()

    def calc_ti_geometries(self):

        # elog.info('TOPMODEL: Building Geometry Objects')
        tigeoms = []
        satgeoms = []
        with open(self.topo_input, 'r') as sr:

            lines = sr.readlines()
            ncols = int(lines[0].split(' ')[-1].strip())
            nrows = int(lines[1].split(' ')[-1].strip())
            lowerx = float(lines[2].split(' ')[-1].strip())
            lowery = float(lines[3].split(' ')[-1].strip())
            cellsize = float(lines[4].split(' ')[-1].strip())
            nodata = float(lines[5].split(' ')[-1].strip())

        # read ti data
        data = np.genfromtxt(self.topo_input, delimiter=' ', skip_header=6)

        # set start x, y
        y = lowery + cellsize * nrows
        i = 0

        for row in data:
            # elog.info('OVERWRITE:TOPMODEL: Building Geometry Objects [%d of %d]' % (i, nrows*ncols))
        # for line in lines[6:]:
            x = lowerx
            # l = line.strip().split(' ')
            for element in row:
                if element != nodata:
                    pt = Point(x,y)

                    # save as ti geometry
                    # srs = spatial.get_srs_from_epsg(None)   # get default
                    tigeoms.append(stdlib.Geometry(geom=pt))
                i += 1

                x += cellsize
            y += cellsize

        # # read ti data
        # fac_data = np.genfromtxt(self.fac_input, delimiter=' ', skip_header=6)
        #
        # # set start x, y
        # y = lowery + cellsize * nrows
        # for row in fac_data:
        #     x = lowerx
        #     for element in row:
        #         if element != nodata:
        #             pt = Point(x,y)
        #             if element >= 20.:
        #                 # save as sat geometry
        #                 # srs = spatial.get_srs_from_epsg(None)   # get default
        #                 satgeoms.append(stdlib.Geometry(geom=pt))
        #         x += cellsize
        #     y += cellsize

        self.ti_geoms = tigeoms
        # self.output_soil_moisture_geoms = satgeoms

    def read_topo_input(self):

        # ---- begin reading the values stored in the topo file
        with open(self.topo_input, 'r') as sr:

            lines = sr.readlines()
            cellsize = float(lines[4].split(' ')[-1].strip())
            nodata = lines[5].split(' ')[-1].strip()

            # generate topolist by parsing cell data
            topoList = [item for sublist in lines[6:] for item in sublist.strip().split(' ') if item != nodata]
            self._watershedArea = len(topoList) * cellsize


        # ---- calculate frequency of each topographic index
        # -- consolidate topo list into unique values
        d = {float(i):float(topoList.count(i)) for i in set(topoList)}

        # -- calculate topo frequency, then return both topographic index and topo frequency arrays
        total = len(topoList)
        self.ti = [round(k,4) for k in d.iterkeys()]
        self.freq = [round((k/total), 10) for k in d.iterkeys()]
