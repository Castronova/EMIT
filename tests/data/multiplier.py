__author__ = 'tonycastronova'


import stdlib
from utilities import mdl
from wrappers import feed_forward

class multiply(feed_forward.Wrapper):


    def __init__(self,config_params):
        """
        initialization that will occur when loaded into a configuration

        """

        super(multiply,self).__init__(config_params)


        # build inputs and outputs
        io = mdl.build_exchange_items_from_config(config_params)

        # set inputs and outputs
        self.inputs(value=io['input'])
        self.outputs(value=io['output'])


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
