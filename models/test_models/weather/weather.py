__author__ = 'tonycastronova'

import os
from wrappers import feed_forward
import stdlib
from utilities import mdl
from datetime import datetime as dt

class weatherReader(feed_forward.Wrapper):
    def __init__(self, config_params):
        super(weatherReader, self).__init__(config_params)

        # build inputs and outputs
        io = mdl.build_exchange_items_from_config(config_params)
        self.outputs(value=io[stdlib.ExchangeItemType.OUTPUT])

        # set inputs and outputs
        self.p = self.outputs()['Precipitation']

        # get weather data file
        self.weather_data_path = config_params['model inputs'][0]['weather_csv']


    def run(self, inputs):

        # read weather data
        incremental_precip = []
        dates = []
        with open(self.weather_data_path, 'rU') as f:
            lines = f.readlines()

            # skip commented lines
            skip = 0
            for line in lines:
                if line[0] == '#':
                    skip += 1
                else:
                    # exit loop as soon as non-commented line is found
                    break

            # read all lines after header
            for line in lines[skip:]:
                data = line.split(',')

                # exit if the data is empty
                if data[0].strip() == '':
                    break

                # save dates to list
                dates.append(dt.strptime(data[0], "%m/%d/%y %H:%M"))

                # save incremental precipitation to list
                incremental_precip.append(float(data[2]))


        # set output data
        self.p.setValues2(incremental_precip, dates)
