__author__ = 'tonycastronova'

import time_base





class temporal_nearest_neighbor(time_base.Time):

    def __init__(self):
        super(temporal_nearest_neighbor, self).__init__()

    def name(self):
        return 'Nearest Neighbor'

    def transform(self, dates, values, target_dates):

        mapped_dates = []
        mapped_values = []
        if not isinstance(target_dates, list):
            target_dates = [target_dates]

        for target_date in target_dates:

            # get the closest date
            closest = sorted(dates, key=lambda d: abs(target_date - d))[0]

            mapped_dates.append(closest)
            mapped_values.append(values[dates.index(closest)])

        # return the closest date and its corresponding value
        return mapped_dates, mapped_values




class TemporalInterpolation():
    NearestNeighbor = temporal_nearest_neighbor()

    def methods(self):
        return [self.NearestNeighbor]
