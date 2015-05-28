__author__ = 'tonycastronova'

import random
from wrappers import feed_forward
import stdlib
from utilities import mdl
import os

class randomizer(feed_forward.feed_forward_wrapper):

    def __init__(self,config_params):
        super(randomizer, self).__init__(config_params)

        #   .__ts = [(date,val),(date,val),]
        self.__ts = []

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

        # Note: this calculation requires no input timeseries

        # get spatial objects (assuming that all variable exist at the same locations)

        # loop over all output exchange items
        for oei in self.outputs().keys():

            output = self.get_output_by_name(oei)
            geoms = output.geometries()

            for g in geoms:
                # get the geometry
                geom = g.geom()
                ts = []

                # calculate a random number timeseries
                current_time = self.current_time()
                end = self.simulation_end()
                while(current_time <= end):
                    if oei == 'random 1-10':
                        ts.append(((current_time),(random.randint(1,10))))
                    elif oei =='random 10-100':
                        ts.append(((current_time),(random.randint(10,100))))
                    elif oei =='random 100-1000':
                        ts.append(((current_time),(random.randint(100,1000))))

                    # increment time
                    current_time = self.increment_time(current_time)

                # save this timeseries to the output geom
                self.set_geom_values(oei,geom,ts)



    def save(self):
        """
        This function is used to build output exchange items
        :return: list of output exchange items
        """

        # save calculations locally
        base = os.path.dirname(__file__)
        # save output locally
        with open(base+'/output.out', 'w') as f:
            for oei in self.outputs().keys():
                output = self.get_output_by_name(oei)
                geoms = output.geometries()
                f.write(oei+'\n')
                for g in geoms:
                    f.write(g.geom().to_wkt()+'\n')
                    date, val = g.datavalues().get_dates_values()
                    for i in xrange(0, len(date)):
                        f.write(date[i].strftime("%m-%d-%Y %H:%M")+','+str(val[i])+'\n')

                f.write('\n')

        # return all timeseries
        return self.outputs()
