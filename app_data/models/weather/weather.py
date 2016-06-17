from wrappers import feed_forward
import stdlib
from utilities import mdl, geometry
from datetime import datetime as dt
import numpy
import uuid

class weatherReader(feed_forward.Wrapper):
    def __init__(self, config_params):
        super(weatherReader, self).__init__(config_params)

        # get weather data file
        self.weather_data_path = config_params['weather_csv']

        # object to hold weather data
        self.weather_data = {}

        # build oeis
        self.construct_oeis(self.weather_data_path)

        # set the model's status
        self.status(stdlib.Status.READY)


    def run(self, inputs):

        oeis = self.outputs()

        # loop through all of the output exchange items and set their output data
        for name, oei in oeis.items():

            # get the dates and values that were parsed during initialization
            dates, values = self.weather_data[oei.id()]

            # set output data
            oei.setValues2(values, dates)

        return 1

    def finish(self):
        self.status(stdlib.Status.FINISHED)

    def construct_oeis(self, weather_data):


        # read the weather data csv
        f = open(weather_data, 'r')
        lines = f.readlines()
        f.close()

        # read ei metadata
        ei_data = []
        for i in range(16,len(lines)):
            line = lines[i]
            if line[0] == '#' and len(line) > 3:
                if line[2] == 'V' and line[3] != '[':
                    data = line.split('=')
                    data = data[1].split(',')
                    trimmed = [d.strip() for d in data]
                    ei_data.append(trimmed)
            elif line[0] != '#':
                break

        def make_date(datestr):
            return dt.strptime(datestr, '%m-%d-%Y %H:%M:%S')

        # parse the weather data dates and values into numpy arrays
        date_arr = numpy.genfromtxt(weather_data, delimiter=',', converters={'Date':make_date}, names = ['Date'], dtype=None, usecols=[0])
        val_arr = numpy.genfromtxt(weather_data, delimiter=',', dtype=float)
        val_arr = numpy.delete(val_arr,0,1)

        # build exchange items
        col_idx = 0
        for item in ei_data:

            # map to stdlib units and variables
            unit = mdl.create_unit(item[2])
            variable = mdl.create_variable(item[1])

            uid = uuid.uuid4().hex

            ei = stdlib.ExchangeItem(id=uid,
                                     name=item[0],
                                     unit=unit,
                                     variable=variable,
                                     desc=item[3],
                                     type=stdlib.ExchangeItemType.OUTPUT)

            # build geometry
            pt = geometry.build_point_geometry(float(item[-2]), float(item[-1]))
            ei.addGeometry(pt)

            # add the oei to the outputs list
            self.outputs(value=ei)

            # save the data associated with this exchange item
            self.weather_data[uid] = [date_arr, val_arr[:, col_idx]]

            # increment the column index for the numpy array
            col_idx += 1





