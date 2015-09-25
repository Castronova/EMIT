__author__ = 'Mario'

import wx
from ..ObjectListView import FastObjectListView


# class Database(object):  # todo: delete me because I'm not being used
#     """    Model of the Database object that is displayed in the Object List View control
#     """
#
#     def __init__(self, resultid, featurecode, variable, unit, data_type, org, date_created):
#         self.resultid = resultid
#         self.featurecode = featurecode
#         self.variable = variable
#         self.unit = unit
#         self.data_type = data_type
#         self.org = org
#         self.date_created = date_created
#
#
# class WOFRecord: #  todo: delete me because I'm not being used
#
#     def __init__(self, name_value_tuple_list):
#         for var, val in name_value_tuple_list:
#             setattr(WOFRecord, var, val)
#
#
# class DataRecord:  #  todo: delete me because I'm not being used
#     """    Model of the Data object that is displayed in the Object List View control
#
#      e.g. [(resultid,10),(date,11/7/14)]
#     """
#
#     def __init__(self, name_value_tuple_list):
#         for var, val in name_value_tuple_list:
#             setattr(DataRecord, var, val)


class ViewDatabase(FastObjectListView):
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        FastObjectListView.__init__(self, *args, **kwargs)

        self.useAlternateBackColors = True
        self.oddRowsBackColor = wx.Colour(191, 217, 217)