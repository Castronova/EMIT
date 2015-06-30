__author__ = 'tonycastronova'

import os
from wrappers import feed_forward
import stdlib
from utilities import mdl
import math
from shapely.geometry import Point
from coordinator.emitLogging import elog
import numpy as np


#---- model inputs
# double R;//subsurface Recharge rate [L/T]
# double c; //recession parameter (m)
# double Tmax; //Average effective transmissivity of the soil when the profile is just saturated
# double interception;//intial interciption of the watershed
# double[] TI;//topographic index
# double[] freq;//topographic index frequency
# double lamda_average;//average lamda
# double PPT_daily;
# double ET_daily;
# double q_overland;
# double q_subsurface;
# double q_infiltration;
# double S_average; //average saturation deficit
# double _watershedArea = 0; //area of the watershed. used to convert runoff into streamflow
# Dictionary<DateTime, double> Precip = new Dictionary<DateTime, double>();
# Dictionary<DateTime, double> ET = new Dictionary<DateTime, double>();
# Dictionary<DateTime, double> outputValues = new Dictionary<DateTime, double>();
# string[] _input_elementset;
# string[] _output_elementset;
# string[] _output_quantity;
# string[] _input_quantity;
# ArrayList _DateTimes = new ArrayList();
# ArrayList q_outputs = new ArrayList();
# ArrayList q_infltration_outputs = new ArrayList();
# string outputPath = System.IO.Directory.GetCurrentDirectory() + "/output";



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
        self.input_ti_geoms = None
        self.output_soil_moisture_geoms = None
        self.calc_ti_geometries()

        # set precipitation geometries
        elog.info('Setting input precipitation geometries')
        self.inputs()['precipitation'].addGeometries2(self.input_ti_geoms)

        # set saturation geometries
        elog.info('Setting soil saturation geometries')
        self.outputs()['soil moisture'].addGeometries2(self.output_soil_moisture_geoms)

        # ---- calculate saturation deficit
        elog.info('Calculating initial saturation deficit')
        TI_freq = [x*y for x,y in zip(self.ti, self.freq)]

        self.lamda_average = sum(TI_freq) / sum(self.freq)

        # catchment average saturation deficit(S_bar)
        self.S_average = (-1.)*self.c * ((math.log10(self.R / self.Tmax)) + self.lamda_average)

        elog.info('Component Initialization Completed Successfully')

    def run(self,inputs):

        input_data = inputs['precipitation'].get_geoms_and_timeseries()

        # loop through each geometry
        for geom, dataset in input_data.iteritems():

            time = self.current_time()

            ts = []
            while time <= self.simulation_end():

                dates = dataset[0]
                values = dataset[1]

                for i in range(0,len(dates)):
                    # get value at this location / time
                    value = values[i]

                    # perform computation
                    new_value = value**2

                    # save this new value in a timeseries
                    ts.append((time,new_value))

                # increment time
                time = self.increment_time(time)


            # save results to this geometry as an output variable
            #self.set_geom_values('multipliedValue',geom,ts)





    def save(self):
        return self.outputs()

    def calc_ti_geometries(self):

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
        for row in data:

        # for line in lines[6:]:
            x = lowerx
            # l = line.strip().split(' ')
            for element in row:
                if element != nodata:
                    pt = Point(x,y)

                    # save as ti geometry
                    tigeoms.append(stdlib.Geometry(geom=pt))

                x += cellsize
            y += cellsize

        # read ti data
        fac_data = np.genfromtxt(self.fac_input, delimiter=' ', skip_header=6)

        # set start x, y
        y = lowery + cellsize * nrows
        for row in fac_data:
            x = lowerx
            for element in row:
                if element != nodata:
                    pt = Point(x,y)
                    if element >= 20.:
                        # save as sat geometry
                        satgeoms.append(stdlib.Geometry(geom=pt))
                x += cellsize
            y += cellsize

        self.input_ti_geoms = tigeoms
        self.output_soil_moisture_geoms = satgeoms


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
