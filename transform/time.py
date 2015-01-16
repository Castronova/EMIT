__author__ = 'tonycastronova'

import time_base

class temporal_nearest_neighbor(time_base.Time):

    def __init__(self):
        super(temporal_nearest_neighbor, self).__init__()

    def name(self):
        return 'Nearest Neighbor'

    def transform(self, dates, values, target_dates):

        # make sure that more than one date is provided
        if len(dates) < 2:
            raise Exception('> [ERROR]: Nearest neighbor time interpolation requires at least 2 input (source) dates!')

        mapped_dates = []
        mapped_values = []
        if type(target_dates) != []:
            target_dates = [target_dates]

        for target_date in target_dates:


                #raise Exception('> [ERROR]: Nearest neighbor time interpolation requires that the target date be between the first and last source dates!')


            # get the closest date
            closest = sorted(dates, key=lambda d: abs(target_date - d))[0]

             # make sure that the target_date is within the dates list
            if (target_date < min(dates)) or (target_date > max(dates)) :
                mapped_dates.append(closest)
                mapped_values.append(None)

            else:
                mapped_dates.append(closest)
                mapped_values.append(values[dates.index(closest)])

        # return the closest date and its corresponding value
        return mapped_dates, mapped_values

