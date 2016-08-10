__author__ = 'tonycastronova'

import bisect

import numpy

import time_base
from emitLogging import elog
from sprint import *


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

    try:
        # transform the datavalues from source to target using temporal map
        return source_values[temporal_map]
    except IndexError, e:
        elog.error('IndexError encountered when performing temporal mapping: %s' % e)
        sPrint('IndexError encountered when performing temporal mapping: %s. Cannot continue with simulation.' % e)


class temporal_nearest_neighbor(time_base.Time):

    def __init__(self):
        super(temporal_nearest_neighbor, self).__init__()

    def name(self):
        return 'Nearest Neighbor'

    def map(self, source_dates, target_dates):
        """
        Builds an index map using the source and target date arrays, assumes
        they are both sorted lists.
        :param source_dates: array of source dates
        :param target_dates: array of target dates
        :return: numpy array representing index mapping of nearest source date
                 index for each target date.  If two
        numbers are equally close, the smaller index is choosen.
        """

        # use bisect_left to find the 0-based index insertion point for
        map = numpy.array([bisect.bisect_left(source_dates, target_date)
                           for target_date in target_dates])

        # replace all insertion points at len(target_dates) with an index of -1
        map[map == len(source_dates)] = -1

        # compare each index of the mapped values to determine which
        # target date is closer to the source date
        ordered_map = []
        try:
            for i in range(0, len(target_dates)):

                # get the target date at index i
                target = target_dates[i]

                # get the mapped value for target[i]
                m = map[i]
                before = source_dates[m-1]
                after = source_dates[m]

                # det if the (i) or (i-1) source date is closer to the target
                if abs(after - target) < abs(target - before):
                    ordered_map.append(m)
                else:
                    ordered_map.append(m-1)
        except Exception:
            msg = 'An Exception occurred while temporally mapping the data'
            sPrint(msg, MessageType.ERROR)
            raise Exception(msg)

        return ordered_map


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
