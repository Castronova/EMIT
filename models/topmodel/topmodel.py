__author__ = 'tonycastronova'


from wrappers import feed_forward
import stdlib
from utilities import mdl
import math

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

        # build inputs and outputs
        io = mdl.build_exchange_items_from_config(config_params)

        # set inputs and outputs
        self.inputs(value=io['input'])
        self.outputs(value=io['output'])


        # Get config file path defined in sample.omi
        # string configFile = (string)properties["ConfigFile"];

        # model_inputs
        inputs = config_params['model inputs'][0]

        # read topographic input file
        self.topo_input = inputs["ti"];

        #read model input parameters
        self.c = float(inputs['m'])
        self.Tmax = float(inputs["tmax"])
        self.R = float(inputs["r"])
        self.interception = float(inputs["interception"])
        # self._watershedArea = float(inputs["watershed_area_square_meters"])
        self.ti = []
        self.freq = []

        #//set OpenMI internal variables
        #this.SetVariablesFromConfigFile(configFile);

        #// initialize a data structure to hold results
        #this.SetValuesTableFields();

        #//save input exchange item info
        #int num_inputs = this.GetInputExchangeItemCount();
        #_input_elementset = new string[num_inputs];
        #_input_quantity = new string[num_inputs];
        #for (int i = 0; i < num_inputs; i++)
        #{
        #    _input_elementset[i] = this.GetInputExchangeItem(i).ElementSet.ID;
        #    _input_quantity[i] = this.GetInputExchangeItem(i).Quantity.ID;
        #}
        #int num_outputs = this.GetOutputExchangeItemCount();

        #_output_elementset = new string[num_outputs];
        #_output_quantity = new string[num_outputs];
        #for (int i = 0; i < num_outputs; i++)
        #{
        #    _output_elementset[i] = this.GetOutputExchangeItem(i).ElementSet.ID;
        #    _output_quantity[i] = this.GetOutputExchangeItem(i).Quantity.ID;
        #}

        #//read topographic indices from input file
        self.read_topo_input()

        # ---- calculate saturation deficit
        # calculate lamda average for the watershed
        #double[] TI_freq = new double[TI.GetLength(0)];
        TI_freq = [x*y for x,y in zip(self.ti, self.freq)]

        #for i in range(0, len(self.ti)):
        #    TI_freq.append(self.ti[i] * self.freq[i])

        self.lamda_average = sum(TI_freq) / sum(self.freq)

        # catchement average saturation deficit(S_bar)
        self.S_average = (-1.)*self.c * ((math.log10(self.R / self.Tmax)) + self.lamda_average)


    def run(self,inputs):
        """
        This is an abstract method that must be implemented.
        :param exchangeitems: list of input exchange items
        :return: true
        """

        input_data = inputs['some_value'].get_geoms_and_timeseries()

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



    def read_topo_input(self):

        # ---- begin reading the values stored in the topo file
        with open(self.topo_input, 'r') as sr:

            lines = sr.readlines()

            # -- get cellsize and nodata from header
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
