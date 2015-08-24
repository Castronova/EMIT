__author__ = 'tonycastronova'



"""
Standard classes
"""

# On OSX you also need to install geos. e.g, sudo port install geos
from shapely.wkt import loads
import datetime
import uuid
import hashlib
from coordinator.emitLogging import elog
from bisect import bisect_left, bisect_right
from osgeo import osr
import numpy

class ElementType():
    Point = 'Point'
    Polygon = 'Polygon'
    PolyLine = 'PolyLine'
    Id = 'Id'

class ExchangeItemType():
    Input = 'input'
    Output = 'output'

class Variable(object):
    """
    Defines the variable object
    """
    def __init__(self):

        # ODM2 terms
        #__variableid = None
        #__variableCode = None
        self.__variableNameCV = None
        self.__variableDefinition = None
        #__speciationCV = None
        #__noDataValue = None


    def VariableNameCV(self,value=None):
        if value is None:
            return self.__variableNameCV
        else:
            self.__variableNameCV = value

    def VariableDefinition(self,value=None):
        if value is None:
            return self.__variableDefinition
        else:
            self.__variableDefinition = value

class Unit(object):
    """
    Defines the unit object
    """
    def __init__(self):

        # ODM2 terms
        #__unitID= None
        self.__unitTypeCV = None
        self.__unitAbbreviation = None
        self.__unitName = None


    def UnitTypeCV(self,value=None):
        if value is None:
            return self.__unitTypeCV
        else:
            self.__unitTypeCV = value

    def UnitAbbreviation(self,value=None):
        if value is None:
            return self.__unitAbbreviation
        else:
            self.__unitAbbreviation = value

    def UnitName(self,value=None):
        if value is None:
            return self.__unitName
        else:
            self.__unitName = value

class Geometry(object):

    def __init__(self,geom=None,srs=4269,elev=None,datavalues=None,id=uuid.uuid4().hex[:5]):
        elog.warning('deprecated: The Geometries class should no longer be used')
        self.__geom = geom
        self.__elev = elev
        self.__datavalues = datavalues
        self.__id = id
        self.__hash = None

        if geom is not None:
            self.build_hash(self.__geom)


        # TODO: use enum
        self.__type = None



        # set spatial reference
        self.__srs = osr.SpatialReference()
        try:
            self.__srs.ImportFromEPSG(srs)
        except:
            # set default
            elog.error('Could not create spatial reference object from code: %s. Using the default spatial reference system: North American Datum 1983.'% str(srs))
            self.__srs.ImportFromEPSG(4269)


    def id(self):
        return self.__id

    def hash(self):
        return self.__hash

    def geom(self,value=None):
        if value is None:
            return self.__geom
        else:
            self.__geom = value

    def set_geom_from_wkt(self,wkt):
        self.__geom = loads(wkt)
        self.build_hash(self.__geom)

    def build_hash(self, geom):
        self.__hash = hashlib.sha224(geom.to_wkt()).hexdigest()

    def srs(self,value=None):
        if value is None:
            return self.__srs
        else:
            self.__srs = value

    def elev(self,value=None):
        if value is None:
            return self.__elev
        else:
            self.__elev = value

    def type(self,value=None):
        if value is None:
            return self.__type
        else:
            self.__type = value

    def datavalues(self,value=None):
        if value is None:
            return self.__datavalues
        else:
            self.__datavalues = value

    def get_data(self):

        self.__datavalues.get_dates_values()

class ExchangeItem(object):
    def __init__(self, id=None, name=None, desc=None, geometry=[], unit=None, variable=None, srs_epsg=4269, type=ExchangeItemType.Input):

        self.__name = name
        self.__description = desc

        # variable and unit come from Variable and Unit standard classes
        self.__unit = unit
        self.__variable = variable
        self.__type = type

        # new style data encapsulation (everything is appended with '2', temporarily)
        self.__geoms2 = numpy.array()
        self.__times2 = numpy.array()
        self.__values2 = numpy.array()

        # no data values will be represented as None
        self.__noData = None

        self.__id = uuid.uuid4().hex[:5]
        if id is not None:
            if isinstance(id, str):
                self.__id = id

        self.__srs = osr.SpatialReference()
        try:
            self.__srs.ImportFromEPSG(srs_epsg)
        except:
            # set default
            elog.error('Could not create spatial reference object from code: %s. '
                       'Using the default spatial reference system: North American Datum 1983.'% str(srs_epsg))
            self.__srs.ImportFromEPSG(4269)


        # todo: REMOVE THE DEPRECATED VARIABLES BELOW
        self.__geoms = geometry
        # variables for saving/retrieving values from database
        self.__session = None
        self.__saved = False
        self.__seriesID = None

    def srs(self, srs_epsg=None):
        if srs_epsg is not None:
            self.__srs = osr.SpatialReference()
            try:
                self.__srs.ImportFromEPSG(srs_epsg)
            except:
                # set default
                elog.error('Could not create spatial reference object from code: %s. '
                           'Using the default spatial reference system: North American Datum 1983.'% str(srs_epsg))
                self.__srs.ImportFromEPSG(4269)

        return self.__srs

    def getEarliestTime2(self):
        return self.__times2[0]

    def getLatestTime2(self):
        return self.__times2[-1]

    def getGeometries2(self, idx=None):
        """
        returns geometries for the exchange item
        :param idx: index of the geometry
        :return: geometry of idx.  If idx is None, all geometries are returned
        """
        if idx is not None:
            return self.__geoms2[idx]
        else:
            return self.__geoms2

    def addGeometries2(self, geom):
        """
        adds geometries to the exchange item
        :param geom: list of geometries or a single value
        :return: None
        """
        if isinstance(geom,list):
            for g in geom:
                if not isinstance(g, Geometry):
                    return 0  # return failure code
            self.__geoms2.extend(geom)
        else:
            if not isinstance(geom, Geometry):
                return 0  # return failure code
            self.__geoms2.append(geom)
        return 1

    def setValues2(self, values, timevalue):
        """
        sets data values for all geometries at a given time index
        :param timevalue: datetime object value for which the datavalues are associated
        :param values: list of datavalues for all geometries at the given time
        :return: values list index
        """


        if  hasattr(timevalue, "__len__"):

            # make sure that the length of values matches the length of times
            if len(timevalue) != len(values):
                elog.critical('Could not set data values. Length of timevalues and datavalues lists must be equal.')
                return 0

            invalid_dates = False
            for i in range(0, len(timevalue)):
                if isinstance(timevalue[i], datetime.datetime):
                    self._setValues2(values[i], timevalue[i])
                else: invalid_dates = True

            if invalid_dates:
                elog.warning('Invalid datetimes were found while setting values.  Data values may not be set correctly.')


            return 1

        elif isinstance(timevalue, datetime.datetime):
            self._setValues2(values, timevalue)

            return 1

        else:
            elog.critical('Could not set data values.  Time value was not of type datetime.')
            return 0

        # if idx < len(self.__values2):
        #     self.__values2[idx] = values
        # else:
        #     self.__values2.append(values)
        #     idx = len(self.__values2) - 1
        # return idx

    def _setValues2(self, values, timevalue):

         # insert by datetime need to get dates to determine which index to use
        idx, date = self.getDates2(timevalue)
        if date is not None and timevalue == self.__times2[idx]:
            # replace the values for this time
            self.__values2[idx] = values
        else:
            # insert new values at the specified index
            if not hasattr(values, "__len__"):
                values = [values]
            self.__values2.insert(idx+1, values)
            self.__times2.insert(idx+1, timevalue)

            # self.__values2.append(values)
            # idx = len(self.__values2) - 1
            # self.setDates2(timevalue, idx)

    def getValues2(self, idx_start=0, idx_end=None, start_time=None, end_time=None, time_idx=None):
        """
        gets datavalues of the exchange item for idx
        :param idx_start: the start value index to be returned.
        :param idx_end: the end value index to be returned.
        :param start_time: start index for selecting a data subset
        :param end_time: end index for selecting a data subset
        :return: datavalues between start_time and end_time.  If not given, entire time range will be returned.
        """

        # set initial value end index as the length of the geometery array
        if idx_end is None:
            idx_end = len(self.__geoms2) + 1
        else:
            # add one to make return values from idx_start to idx_end inclusive
            idx_end += 1

        if time_idx is None:
            start_time_slice_idx = 0
            end_time_slice_idx = len(self.__times2)
            if start_time is not None:
                start_time_slice_idx = self._nearest(self.__times2, start_time, 'left')
            if end_time is not None:
                end_time_slice_idx = self._nearest(self.__times2, end_time, 'right') + 1
        else:
            return self.__values2[time_idx][idx_start:idx_end]  # return a single time index of values

        values = []
        for i in range(start_time_slice_idx, end_time_slice_idx):
            values.append(self.__values2[i][idx_start:idx_end])

        return values

    def setDates2(self, timevalue):
        """
        sets the data-times for a geometry index.  These should directly correspond with
        :param timevalue: datetime object
        :return: index of the datetime value
        """

        idx = self._nearest(self.__times2, timevalue, 'left') + 1
        # idx = len(self.__times2.keys())
        self.__times2.insert(idx+1, timevalue)
        return idx

    def getDates2(self, timevalue=None, start=None, end=None):
        """
        gets datavalue indices for a datetime
        :param timevalue: datetime object
        :return: returns the datavalue index, and the time value corresponding to the nearest requested datetime
        """
        if isinstance(timevalue, list):
            times = []
            for t in timevalue:
                idx = self._nearest(self.__times2, timevalue, 'left')
                if len(self.__times2) and idx <= len(self.__times2):
                    times.append((idx, self.__times2[idx]))
                else:
                    times.append(0, None)
            return times

        elif start is not None and end is not None:
            if not isinstance(start, datetime.datetime) or not isinstance(end, datetime.datetime):
                elog.critical('Could not fetch date time from range because the "start" and/or "endtimes" are not valued datetime objects.')
                return 0, None

            st = self._nearest(self.__times2, start, 'left')
            et = self._nearest(self.__times2, end, 'right') + 1
            times = [(idx, self.__times2[idx]) for idx in range(st, et)]
            return times


        elif isinstance(timevalue, datetime.datetime):
            idx = self._nearest(self.__times2, timevalue, 'left')
            if len(self.__times2) and idx <= len(self.__times2):
                return idx, self.__times2[idx]
            else:
                return 0, None

        else: # return all known values
            times = [(idx, self.__times2[idx]) for idx in range(0, len(self.__times2))]
            return times

    def unit(self,value=None):
        if value is None:
            return self.__unit
        else:
            self.__unit = value

    def variable(self,value=None):
        if value is None:
            return self.__variable
        else:
            self.__variable = value

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type

    def name(self,value=None):
        if value is None:
            return self.__name
        else:
            self.__name = value

    def description(self,value=None):
        if value is None:
            return self.__description
        else:
            self.__description = value

    def _nearest(self, lst, time, direction='left'):
        """
        get the nearst datetime in list
        :param lst: search list (sorted)
        :param time: desired datetime
        :param direction: the bisect direction.  'left' for start_time and 'right' for end_time
        :return: list index
        """

        if len(lst) == 0:
            return 0

        if direction == 'left':
            i = bisect_left(lst, time)
            nearest = min(lst[max(0, i-1): i+2], key=lambda t: abs(time - t))
            return lst.index(nearest)
        elif direction == 'right':
            i = bisect_right(lst, time)
            nearest = min(lst[max(0, i-1): i+2], key=lambda t: abs(time - t))
            return lst.index(nearest)



    # todo: REMOVE DEPRECATED FUNCTIONS BELOW

    def getStartTime(self):
        elog.warning('deprecated: Use getEarliestTime2 instead')
        return min(g.datavalues().start() for g in self.__geoms)

    def getEndTime(self):
        elog.warning('deprecated: Use getLatestTime2 instead')
        return max(g.datavalues().end() for g in self.__geoms)

    def geometries(self):
        elog.warning('deprecated: stdlib.geometries use getGeometries2 instead')
        g = self.getGeometries2()
        if len(g) != 0:
            return g
        return self.__geoms

    def add_geometry(self, geom):
        elog.warning('deprecated: stdlib.add_geometry use addGeometries2 instead')
        if isinstance(geom,list):
            self.__geoms.extend(geom)
            # for g in geom:
            #     self.__calculate_start_and_end_times(g.datavalues())
        else:
            self.__geoms.append(geom)
            # self.__calculate_start_and_end_times(geom.datavalues())

    def get_dataset(self,geometry):
        elog.warning('deprecated: stdlib.get_dataset use getValues2 instead')
        for geom in self.__geoms:
            if geom.geom() == geometry:
                return geometry.datavalues()
        raise Exception('Could not find geometry in exchange item instance: %s'%geometry)
        #return self.__dataset

    def get_all_datasets(self):
        elog.warning('deprecated: stdlib.get_all_datasets use getValues2 instead')
        """
        returns the input dataset as a dictionary of geometries
        """
        geom_dict = {}
        for geom in self.__geoms:
            geom_dict[geom] = geom.datavalues()
        return geom_dict

        # for datavalues in self.__dataset:
        #     dict[datavalues.element] = datavalues.values()
        # return dict

    def get_geoms_and_timeseries(self):
        elog.warning('deprecated: stdlib.get_geoms_and_timeseries')
        geom_dict = {}
        for geom in self.__geoms:
            geom_dict[geom] = geom.datavalues().get_dates_values()
        return geom_dict

    def get_timeseries_by_id(self, geom_id):
        elog.warning('deprecated: stdlib.get_timeseries_by_id')
        # TODO: loop using integers to speed this up
        for geom in self.__geoms:
            if geom.id() == geom_id:
                return geom.datavalues().get_dates_values()

    def set_timeseries_by_id(self, geom_id, timeseries):
        elog.warning('deprecated: stdlib.set_timeseries_by_id')
        '''
        sets the timeseries for a geometry using the geometry id
        :param geom_id: id of the geometry
        :param timeseries: zip([dates],[values])
        :return: None
        '''

        for geom in self.__geoms:
            if geom.id() == geom_id:
                geom.datavalues().set_timeseries(timeseries)
                return

    def get_timeseries_by_geom(self,geom):
        elog.warning('deprecated: stdlib.get_timeseries_by_geom')
        # """
        # geom = the geom of the desired timeseries
        # """
        # dict = self.get_dataset_dict()
        # for element in dict.keys():
        #     if element.geom() == geom:
        #         return dict[element]
        # return None
        pass

    def get_timeseries_by_element(self,element):
        elog.warning('deprecated: stdlib.get_timeseries_by_element')
        # """
        # element = the element of the desired timeseries
        # """
        # dict = self.get_dataset_dict()
        # return dict[element]
        pass



    def add_dataset(self,datavalues):
        elog.warning('deprecated: stdlib.add_dataset')
        # """
        # datavalues = list of datavalue objects
        # """
        # if isinstance(datavalues,list):
        #     self.get_dataset().extend(datavalues)
        #     self.__calculate_start_and_end_times(datavalues)
        #
        #     # save the geometries
        #
        # else:
        #     self.get_dataset().append(datavalues)
        #     self.__calculate_start_and_end_times([datavalues])
        pass

    def clear(self):
        elog.warning('deprecated: stdlib.add_dataset')
        #self.__dataset = []
        self.__geoms = []
        # self.StartTime = datetime.datetime(2999,1,1,1,0,0)
        # self.EndTime = datetime.datetime(1900,1,1,1,0,0)

    def set_dataset(self,value):
        # self.__dataset = value
        # self.__calculate_start_and_end_times(value)
        elog.warning('deprecated: stdlib.set_dataset')
        pass

    def session(self,value=None):
        """
        gets/sets the database session for this exchange item
        :param value: database session object
        :return: database session object
        """
        elog.warning('deprecated: stdlib.session')
        if value is not None:
            self.__session == value
        else:
            return self.__session

    def is_saved(self,value=None):
        """
        gets/sets the saved state of the exchange item
        :param value: Boolean type indicated if the exchange item has been saved to db
        :return: Boolean
        """
        elog.warning('deprecated: stdlib.is_saved')
        if value is not None:
            self.__saved = value
        else:
            return self.__saved

    def resultid(self,value):
        """
        gets/sets the database series id for the simulation results
        :param value: ODM2 resultID
        :return: ODM2 resultID
        """
        elog.warning('deprecated: stdlib.resultid')
        if value is not None:
            return self.__seriesID
        else:
            self.__seriesID = value



# class Element(object):
#     """
#     Spatial definition of a calculation or timeseries
#     """
#
#     # TODO: SRS should be an ogr object NOT defined by name,def,and code!
#
#     def __init__(self):
#         self.__geom = None
#         #self.__srs_def = None
#         #self.__srs_name = None
#         #self.__srs_code = None
#         self.__srs = None
#         self.__elev = None
#
#
#
#         # TODO: use enum
#         self.__type = None
#
#         elog.warning('deprecated: The Element class should no longer be used')
#
#     def geom(self,value=None):
#         if value is None:
#             return self.__geom
#         else:
#             self.__geom = value
#
#     def set_geom_from_wkt(self,wkt):
#         self.__geom = loads(wkt)
#
#
#     # def srs(self,srsname=None,srscode=None):
#     #     if srsname is None and srscode is None:
#     #         return (self.__srs_name,self.__srs_code)
#     #     else:
#     #         self.__srs_name = srsname
#     #         self.__srs_code = srscode
#
#     def srs(self,value=None):
#         if value is None:
#             return self.__srs
#         else:
#             self.__srs = value
#
#     def elev(self,value=None):
#         if value is None:
#             return self.__elev
#         else:
#             self.__elev = value
#
#     def type(self,value=None):
#         if value is None:
#             return self.__type
#         else:
#             self.__type = value
#
# class DataValues(object):
#     """
#     A dataset associated with a geometry
#     """
#     def __init__(self,timeseries=None):
#
#         # timeseries = [(date,val),(date,val),]
#         self.__timeseries = timeseries
#
#         # element = shapely geometry
#         #self.__element = element
#
#         self.__start = None
#         self.__end = None
#
#         # start and end are the defined by the date range of the dataset
#         if timeseries is not None:
#             self.update_start_end_times()
#
#         elog.warning('deprecated: The DataValues class should no longer be used')
#
#     def timeseries(self):
#         return self.__timeseries
#
#     def set_timeseries(self,value):
#         self.__timeseries = value
#         self.update_start_end_times()
#
#     def get_dates_values(self):
#         if self.__timeseries:
#             return zip(*self.__timeseries)
#         else:
#             return None, None
#
#     def earliest_date(self):
#         return self.__start
#
#     def latest_date(self):
#         return self.__end
#
#     def update_start_end_times(self):
#         dates,values = zip(*self.__timeseries)
#         self.__start = min(dates)
#         self.__end = max(dates)
#
#     def start(self):
#         if self.__start is None:
#             self.update_start_end_times()
#         return self.__start
#     def end(self):
#         if self.__end is None:
#             self.update_start_end_times()
#         return self.__end









