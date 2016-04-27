__author__ = 'tonycastronova'

import math
from distutils.version import LooseVersion

import numpy as np

import stdlib
from emitLogging import elog
from utilities import mdl, geometry
from wrappers import feed_forward


class topmodel(feed_forward.Wrapper):


    def __init__(self,config_params):
        """
        initialization that will occur when loaded into a configuration

        """

        super(topmodel,self).__init__(config_params)

        if LooseVersion(np.__version__) < LooseVersion('1.9.0'):
            elog.error('Could not load TOPMODEL, NumPY version 1.9.0 or greater required')
            raise Exception('Could not load TOPMODEL, NumPY version 1.9.0 or greater required')



        elog.info('Begin Component Initialization')

        # build inputs and outputs
        elog.info('Building exchange items')
        io = mdl.build_exchange_items_from_config(config_params)

        # set inputs and outputs
        self.inputs(value=io[stdlib.ExchangeItemType.INPUT])
        self.outputs(value=io[stdlib.ExchangeItemType.OUTPUT])

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
            in_precip = precipitation.getValues2(time_idx = i)

            #todo: this is a hack because i'm running out of time before the demo
            # todo: something is wrong with the data interpolation!
            # p = precip[0][0]
            # if isinstance(p, np.ndarray):
            #     precip = p[0]
            # else:
            #     precip = p
            # # precip = precip[0][0][0]

            precip = in_precip[0]

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

        elog.info('TOPMODEL: Building Geometry Objects')
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

        # build X and Y coordinate arrays
        xi = np.linspace(lowerx, lowerx+ncols*cellsize, ncols)
        yi = np.linspace(lowery+nrows*cellsize, lowery, nrows)
        x,y = np.meshgrid(xi,yi)    # generate 2d arrays from xi, yi
        x = x.ravel()   # convert to 1-d
        y = y.ravel()   # convert to 1-d
        data = data.ravel()  # convert to 1-d

        # remove all nodata points from x, y arrays
        nonzero = np.where(data != nodata)
        x = x[nonzero]
        y = y[nonzero]

        tigeoms = geometry.build_point_geometries(x,y)

        self.ti_geoms = tigeoms
        # self.output_soil_moisture_geoms = satgeoms

    def read_topo_input(self):


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

        topoList = data.ravel() # convert into 1-d list
        topoList = topoList[topoList != nodata] # remove nodata values
        self._watershedArea = topoList.shape[0]*cellsize  # calculate watershed area


        topoList = np.round(topoList, 4)         # round topoList items
        total = topoList.shape[0]                   # total number of element in the topoList
        unique, counts = np.unique(topoList, return_counts=True)    # get bins for topoList elements

        self.ti = unique                         # topographic index list
        self.freq = unique/total                 # freq of topo indices
        self.freq = np.round(self.freq, 10)        # round the frequencies