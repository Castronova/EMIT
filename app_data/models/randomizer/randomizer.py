import os
import random
from wrappers import feed_forward
import stdlib
from utilities import mdl
import numpy
import datetime

class randomizer(feed_forward.Wrapper):
    def __init__(self, config_params):
        super(randomizer, self).__init__(config_params)

        # .__ts = [(date,val),(date,val),]
        self.__ts = []

        # build inputs and outputs
        io = mdl.build_exchange_items_from_config(config_params)

        # set inputs and outputs
        self.inputs(value=io[stdlib.ExchangeItemType.INPUT])
        self.outputs(value=io[stdlib.ExchangeItemType.OUTPUT])


    def run(self, inputs):
        """
        This is an abstract method that must be implemented.
        :param exchangeitems: list of input exchange items
        :return: true
        """

        # Note: this calculation requires no input timeseries

        o = self.outputs()
        outputs = [o['random POLYGON 1-10'],
                   o['random POLYGON 10-100'],
                   o['random POLYGON 100-1000'],
                   o['random POINT 1-10'],
                   o['random POINT 100-1000'],
                   o['random LINESTRING 10-100'],
                   ]


        # geoms = output.geometries()
        dates = []
        end = self.simulation_end()
        while (self.current_time() <= end):
            dates.append(self.current_time())
            self.increment_time()

        for output in outputs:

            geoms = output.getGeometries2()

            vals = []

            # calculate a random number for each timestep
            for ct in dates:

                v = []
                # loop over each output geometry instance and generate a random number
                for g in geoms:

                    # generate random numbers
                    Min,Max = output.name().split(' ')[-1].split('-')
                    v.append(random.random()*float(Max) + float(Min))

                # save list of values for each geom at current time
                vals.append(v)


            # save calculated values for this output exchange item
            output.setValues2(vals, dates)
            # self.set_geom_values(output.name(), geom, ts)

        print 'Run Complete'

    def finish(self):
        """
        This function is used to build output exchange items
        :return: list of output exchange items
        """

        # save calculations locally
        base = os.path.dirname(__file__)
        # save output locally
        with open(base+'/output.out', 'w') as f:
            for oei in self.outputs().keys():
                output = self.outputs()[oei]
                geoms = output.getGeometries2()
                dates = output.getDates2(ndarray=True)
                values = output.getValues2(ndarray=True)

                f.write(oei+'\n')
                f.write('GEOMETRIES AS WKT \n')
                for i in range(0, len(geoms)):
                    f.write(str(i+1)+'\t'+geoms[i].ExportToWkt()+'\n')

                # write header
                f.write('\n\ntime index\tdate time\t')
                for i in range(0, len(geoms)):
                    f.write('geometry '+str(i+1)+'\t')
                f.write('\n')

                output = numpy.hstack((dates, values))
                for r in range(0, output.shape[0]):
                    for c in range(0, output.shape[1]):
                        val = output[r,c]
                        if not isinstance(val, datetime.datetime):
                            f.write(str(val)+'\t')
                        else:
                            f.write(val.strftime('m/d/Y H:M:S') +'\t')

                    f.write('\n')

                f.write(100*'-' + '\n')


        # save all timeseries
        # return self.outputs()
