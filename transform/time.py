__author__ = 'tonycastronova'

import time_base
import bisect
import numpy

def transform(temporal_map, source_values):
    """
    transforms source data into target data array using temporal map
    :param temporal_map: temporal mapping list (this can be a numpy array of a list)
    :param source_values: numpy array of values
    :return: numpy array of target values
    """

    if type(source_values) == list:
        source_values = numpy.array(source_values)

    if type(source_values) != numpy.ndarray:
        raise ValueError('Invalid source_values type for time mapping')

    # transform the datavalues from source to target using temporal map
    return source_values[temporal_map]

class temporal_nearest_neighbor(time_base.Time):

    def __init__(self):
        super(temporal_nearest_neighbor, self).__init__()

    def name(self):
        return 'Nearest Neighbor'

    def map(self, source_dates, target_dates):
        """
        Builds an index map using the source and target date arrays
        :param source_dates: array of source dates
        :param target_dates: array of target dates
        :return: numpy array representing index mapping from source dates to target dates
        """

        return numpy.array([bisect.bisect(source_dates, target_date) - 1 for target_date in target_dates])


# class temporal_nearest_neighbor(time_base.Time):
#
#     def __init__(self):
#         super(temporal_nearest_neighbor, self).__init__()
#
#     def name(self):
#         return 'Nearest Neighbor'
#
#     def transform(self, dates, values, target_dates):
#
#         mapped_dates = []
#         mapped_values = []
#         if not isinstance(target_dates, list):
#             target_dates = [target_dates]
#
#         for target_date in target_dates:
#
#             # get the closest date
#             closest = sorted(dates, key=lambda d: abs(target_date - d))[0]
#
#             mapped_dates.append(closest)
#             mapped_values.append(values[dates.index(closest)])
#
#         # return the closest date and its corresponding value
#         return mapped_dates, mapped_values
#



class TemporalInterpolation():
    NearestNeighbor = temporal_nearest_neighbor()

    def methods(self):
        return [self.NearestNeighbor]
