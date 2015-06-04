__author__ = 'tonycastronova'

import random
from wrappers import feed_forward
import stdlib
from utilities import mdl


class randomizer(feed_forward.feed_forward_wrapper):
    def __init__(self, config_params):
        super(randomizer, self).__init__(config_params)

        # .__ts = [(date,val),(date,val),]
        self.__ts = []

        # build inputs and outputs
        io = mdl.build_exchange_items_from_config(config_params)

        # set inputs and outputs
        self.inputs(value=io['input'])
        self.outputs(value=io['output'])


    def run(self, inputs):
        """
        This is an abstract method that must be implemented.
        :param exchangeitems: list of input exchange items
        :return: true
        """

        # Note: this calculation requires no input timeseries

        outputs = [self.get_output_by_name('random 1-10'),
                   self.get_output_by_name('random 10-100'),
                   self.get_output_by_name('random 100-1000')
                   ]

        for output in outputs:

            geoms = output.geometries()

            random.randrange(5,60,5)

            c = 0
            # for i in range(900000000):
            #     c += 1

            # loop over each output geometry instance and generate a random number
            for g in geoms:
                # get the geometry
                geom = g.geom()
                ts = []

                # calculate a random number timeseries
                current_time = self.current_time()
                end = self.simulation_end()
                while (current_time <= end):

                    Min,Max = output.name().split(' ')[-1].split('-')
                    val = random.random()*float(Max) + float(Min)
                    ts.append(((current_time), (val)))

                    # increment time
                    current_time = self.increment_time(current_time)


                # save this timeseries to the output geom
                self.set_geom_values(output, geom, ts)


    def save(self):
        """
        This function is used to build output exchange items
        :return: list of output exchange items
        """

        # save all timeseries
        return self.outputs()
