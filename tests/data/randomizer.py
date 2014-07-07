__author__ = 'tonycastronova'

import random
from wrappers import feed_forward
import stdlib

class randomizer(feed_forward.feed_forward_wrapper):

    def __init__(self,config_params):
        super(randomizer, self).__init__(config_params)

        #   .__ts = [(date,val),(date,val),]
        self.__ts = []


    def run(self,inputs):
        """
        This is an abstract method that must be implemented.
        :param exchangeitems: list of input exchange items
        :return: true
        """

        # Note: this calculation requires no input timeseries

        # get spatial objects (assuming that all variable exist at the same locations)
        output = self.get_output_by_name('random_number')
        geoms = output.geometries()

        # loop over each output geometry instance and generate a random number
        for g in geoms:
            # get the geometry
            geom = g.geom()
            ts = []

            # calculate a random number timeseries
            current_time = self.current_time()
            end = self.simulation_end()
            while(current_time <= end):
                ts.append(((current_time),(random.random())))

                # increment time
                current_time = self.increment_time(current_time)


            # save this timeseries to the output geom
            self.set_geom_values('random_number',geom,ts)


    def save(self):
        """
        This function is used to build output exchange items
        :return: list of output exchange items
        """

        # save all timeseries
        return self.outputs()
