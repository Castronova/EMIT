__author__ = 'tonycastronova'



"""
Standard classes
"""

# On OSX you also need to install geos. e.g, sudo port install geos
import datetime
import hashlib
import uuid
from bisect import bisect_left, bisect_right

import numpy
from osgeo import osr, ogr

from emitLogging import elog
from sprint import *


class Status:
    READY = 'READY'
    NOTREADY = 'NOTREADY'
    RUNNING = 'RUNNING'
    UNDEFINED = 'UNDEFINED'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


# derived from GDAL types
class GeomType():
    POINT = 'POINT'
    LINESTRING = 'LINESTRING'
    POLYGON = 'POLYGON'
    MULTIPOINT = 'MULTIPOINT'
    MULTILINESTRING = 'MULTILINESTRING'
    MULTIPOLYGON = 'MULTIPOLYGON'
    GEOMETRYCOLLECTION = 'GEOMETRYCOLLECTION'
    CIRCULARSTRING = 'CIRCULARSTRING'
    COMPOUNDCURVE = 'COMPOUNDCURVE'
    CURVEPOLYGON = 'CURVEPOLYGON'
    MULTICURVE = 'MULTICURVE'
    MULTISURFACE = 'MULTISURFACE'
    _map = {'1': POINT,
            '2': LINESTRING,
            '3': POLYGON,
            '4': MULTIPOINT,
            '5': MULTILINESTRING,
            '6': MULTIPOLYGON,
            '7': GEOMETRYCOLLECTION,
            '8': CIRCULARSTRING,
            '9': COMPOUNDCURVE,
            '10': CURVEPOLYGON,
            '11': MULTICURVE,
            '12': MULTISURFACE}

class ExchangeItemType():
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

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

class Geometry2(ogr.Geometry):
    def __init__(self, wkb_geom):
        super(Geometry2, self).__init__(wkb_geom)

        self.type = getattr(GeomType, self.GetGeometryName())

        self.hash = None

    def update_hash(self):
        self.hash = hashlib.sha224(self.ExportToWkt()).hexdigest()

    def AddPoint(self, *args, **kwargs):
        super(Geometry2, self).AddPoint(*args, **kwargs)

        # only update the geometry hash if AddGeometry will not be called (i.e. POINT and LINESTRING objects)
        if self.type == GeomType.POINT or self.type == GeomType.LINESTRING:
            self.update_hash()

    def AddGeometry(self, *args):
        super(Geometry2, self).AddGeometry(*args)

        # update the geometry hash
        self.update_hash()

class ExchangeItem(object):
    def __init__(self, id=None, name=None, desc=None, geometry=[], unit=None, variable=None, noData=None, srs_epsg=4269, type=ExchangeItemType.INPUT):

        self.__name = name
        self.__description = desc

        # variable and unit come from Variable and Unit standard classes
        self.__unit = unit
        self.__variable = variable

        # set type using Exchange Item Type enum
        if type in ExchangeItemType.__dict__:
            self.__type = type
        else:
            raise Exception('Exchange Item of Type "%s" not recognized'%type)

        # new style data encapsulation (everything is appended with '2', temporarily)
        self.__geoms2 = []
        self.__times2 = []
        self.__values2 = []

        # todo: there should be similar functionality for times2 and values2
        # save the geometries (if provided)
        if geometry is not None:
            self.addGeometries2(geometry)

        # no data values
        self.__noData = noData

        self.__id = uuid.uuid4().hex
        if id is not None:
            if isinstance(id, str):
                self.__id = id

        # self.__srs = osr.SpatialReference()
        self.__srs = self.srs(srs_epsg=srs_epsg)
        # if self.__srs.ImportFromEPSG(srs_epsg)
        # except Exception, e:
        #     # set default
        #     elog.error('Error ExchangeItem.__init__: %s' % e)
        #     sPrint('Could not create spatial reference object from code: %s. '
        #                'Using the default spatial reference system: North American Datum 1983.'% str(srs_epsg),
        #            MessageType.ERROR)
        #
        #     self.__srs.ImportFromEPSG(4269)


        # todo: REMOVE THE DEPRECATED VARIABLES BELOW
        self.__geoms = geometry
        # variables for saving/retrieving values from database
        self.__session = None
        self.__saved = False
        self.__seriesID = None

    def initializeDatesValues(self, start_datetime, end_datetime, timestep_in_seconds):
        date = start_datetime
        dates = []
        while date <= end_datetime:
            dates.append(date)
            date = date + datetime.timedelta(seconds=timestep_in_seconds)

        self.__times2 = numpy.array(dates)
        geoms = self.__geoms2
        self.__values2 = numpy.zeros(shape=(len(dates), len(geoms)))
        self.__values2[:] = self.__noData

    def noData(self, value = None):
        if value is not None:
            self.__noData = value
        return self.__noData

    def srs(self, srs_epsg=None):
        if srs_epsg is not None:
            self.__srs = osr.SpatialReference()
            if self.__srs.ImportFromEPSG(srs_epsg) != 0:
                from osgeo import gdal
                msg = gdal.GetLastErrorMsg()
                elog.error('Could Not set srs: %s' % msg)
                sPrint('Unable to load spatial reference %s: %s  ' % (str(srs_epsg), msg), MessageType.ERROR)
                sPrint('This may cause errors with future operations.  It is recommended that the GDAL_DATA path is fixed in the ' +
                       'EMIT environment settings before continuing.', MessageType.CRITICAL)
        return self.__srs

    def getEarliestTime2(self):
        return self.__times2[0]

    def getLatestTime2(self):
        return self.__times2[-1]

    def getGeometries2(self, idx=None, ndarray=False):
        """
        returns geometries for the exchange item
        :param idx: index of the geometry
        :return: geometry of idx.  If idx is None, all geometries are returned
        """
        if idx is not None:
            return self.__geoms2[idx]
        else:
            if ndarray:
                return numpy.array(self.__geoms2)
            return self.__geoms2

    def addGeometry(self, geometry):

        geoms = []
        try:
            if isinstance(geometry, Geometry2):
                geoms.append(geometry)
            else:
                elog.error('Attempt to add unsupported geometry type: %s'%type(geometry))
                sPrint('Attempt to add unsupported geometry type: %s'%type(geometry), MessageType.ERROR)
                return 0
        except Exception, e:
            elog.error('Encountered an error while adding geometry: %s'%e)
            sPrint('Encountered an error while adding geometry: %s'%e, MessageType.ERROR)

        # save the geometry
        self.__geoms2.extend(geoms)

        return 1

    def addGeometries2(self, geometries=None):
        """
        adds geometries to the exchange item
        :param geom: list of geometries or a single value
        :return: None
        """

        # make sure the input geometries are iterable
        if not isinstance(geometries,list) and not isinstance(geometries,numpy.ndarray):
            elog.error('Encountered an error while adding geometries: Unsupported argument type: %s'%type(geometries))
            sPrint('Encountered an error while adding geometries: Unsupported argument type: %s'%type(geometries), MessageType.ERROR)
            return 0


        geoms = []
        count = 0
        for g in geometries:
            if isinstance(g, Geometry2):
                geoms.append(g)
            count += 1

        # save geometries
        self.__geoms2.extend(geoms)

        # notify that not all geometries were saved
        if len(geoms) != count:
            elog.error('Encountered unsupported geometry types while adding geometries to exchange item. Not all items may have been saved.')
            sPrint('Encountered unsupported geometry types while adding geometries to exchange item. Not all items may have been saved.', MessageType.WARNING)
            return 0



        return 1

    def setValuesBySlice (self, values, time_index_slice=(None, None, None), geometry_index_slice=(None, None, None)):
        """
        sets datavalues for the component.
        :param values:  Values to set
        # :param value_index_slice: tuple representing the start, stop, and step range of the values
        :param time_index_slice: tuple representing the start, stop, and step range of the date times
        :param geometry_index_slice: tuple representing the start, stop, and step range of the geometries
        :return: True if successful, otherwise False
        """

        if len(self.__values2) == 0 or len(self.__times2) == 0:
            elog.critical('Error ExchangeItem.setValuesBySlice: Exchange item values and/or times arrays were not set properly')
            sPrint('Exchange item values and/or times arrays were not set properly Make sure "initializeDatesValues" is being called during/after component initialization.', MessageType.CRITICAL)
            return False

        try:
            # get index ranges
            tb, te, tstep = time_index_slice
            gb, ge, gstep = geometry_index_slice

            # set initial values for missing slice indices
            tb = 0 if tb is None else tb
            gb = 0 if gb is None else gb
            te = len(self.__times2) if te is None else te
            ge = len(self.__geoms2) if ge is None else ge
            tstep = 1 if tstep is None else tstep
            gstep = 1 if gstep is None else gstep

            # convert the values into a numpy array if they aren't already
            if not isinstance(values, numpy.ndarray):
                values = numpy.array(values)

            # set the values[times][geoms]
            # reshape the input array to fit the desired slicing
            target_shape = ((te-tb) / tstep, (ge-gb) / gstep)
            values = values.reshape(target_shape)
            self.__values2[tb:te:tstep, gb:ge:gstep] = values


        except Exception as e:
            elog.error('Error ExchangeItem.setValuesBySlice: %s' % e)
            sPrint('Error setting values for times %s, geometries %s: %s' % (str(time_index_slice), str(geometry_index_slice), e),
                   MessageType.ERROR)
            return False
        return True

    def setValuesByTime(self, values, timevalue, geometry_index_slice=(None, None, None)):
        try:
            # get time index
            idx, date = self.getDates2(timevalue)

            # get index ranges
            gb, ge, gstep = geometry_index_slice

            # convert the values into a numpy array if they aren't already
            if not isinstance(values, numpy.ndarray):
                values = numpy.array(values)

            # set the values[times][geoms]
            self.__values2[idx, gb:ge:gstep] = values

        except Exception as e:
            elog.error('Error ExchangeItem.setValuesByTime: %s' % e)
            sPrint('Error setting values for times %s, geometries %s' % (str(time_index_slice), str(geometry_index_slice)),
                   MessageType.ERROR)
            return False
        return True

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
                sPrint('Could not set data values. Length of timevalues and datavalues lists must be equal.',
                       MessageType.WARNING)
                return 0

            invalid_dates = False
            for i in range(0, len(timevalue)):
                if isinstance(timevalue[i], datetime.datetime):
                    self._setValues2(values[i], timevalue[i])
                else: invalid_dates = True

            if invalid_dates:
                sPrint('Invalid datetimes were found while setting values.  Data values may not be set correctly.',
                             MessageType.WARNING)


            return 1

        elif isinstance(timevalue, datetime.datetime):
            self._setValues2(values, timevalue)

            return 1

        else:
            sPrint('Could not set data values.  Time value was not of type datetime.',
                         MessageType.WARNING)
            return 0

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

    def getValues2(self, geom_idx_start=0, geom_idx_end=None, start_time=None, end_time=None, time_idx=None, ndarray=False):
        """
        gets datavalues of the exchange item for idx
        :param geom_idx_start: the start value index to be returned.
        :param geom_idx_end: the end value index to be returned.
        :param start_time: start index for selecting a data subset
        :param end_time: end index for selecting a data subset
        :return: datavalues between start_time and end_time.  If not given, entire time range will be returned.
        """

        # set initial value end index as the length of the geometry array
        if geom_idx_end is None:
            geom_idx_end = len(self.__geoms2) + 1
        else:
            # add one to make return values from idx_start to idx_end inclusive
            geom_idx_end += 1

        if time_idx is None:
            start_time_slice_idx = 0
            end_time_slice_idx = len(self.__times2)
            if start_time is not None:
                start_time_slice_idx = self._nearest(self.__times2, start_time, 'left')
            if end_time is not None:
                end_time_slice_idx = self._nearest(self.__times2, end_time, 'right') + 1
        else:
            return self.__values2[time_idx][geom_idx_start:geom_idx_end]  # return a single time index of values

        values = []
        for i in range(start_time_slice_idx, end_time_slice_idx):
            values.append(self.__values2[i][geom_idx_start:geom_idx_end])

        # if ndarray:
        return numpy.array(values)
        # else:
        #     return values

    # def setDates2(self, timevalue):
    #     """
    #     sets the data-times for a geometry index.  These should directly correspond with
    #     :param timevalue: datetime object
    #     :return: index of the datetime value
    #     """
    #
    #     idx = self._nearest(self.__times2, timevalue, 'left') + 1
    #     self.__times2 = numpy.insert(self.__times2, idx, timevalue)
    #     # self.__times2.insert(idx+1, timevalue)
    #     return idx

    def getDates(self):
        """
        Get all datetimes for the exchange item
        Returns: numpy array of datetimes

        """
        times = [(idx, self.__times2[idx]) for idx in range(0, len(self.__times2))]
        return numpy.array(times)

    def getNearestDates(self, dateslist, search_direction='left'):
        """
        Get the exchange item datetime objects nearest the datelist argument
        Args:
            dateslist: list of datetimes to search
            search_direction: direction of search

        Returns: numpy array((index, datetime),)

        """

        if not isinstance(dateslist, list):
            sPrint('stdlib.getNearestDates requires input datetimes as a list', MessageType.ERROR)
            return numpy.empty((0,))

        times = []
        for t in dateslist:
            idx = self._nearest(self.__times2, t, search_direction)
            if len(self.__times2) and idx <= len(self.__times2):
                times.append((idx, self.__times2[idx]))
            else:
                times.append(0, None)

        return numpy.array(times)




    def getDates2(self, timevalue=None, start=None, end=None, ndarray=False):
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
            if ndarray:
                return numpy.array(times)
            else:
                return times

        elif start is not None and end is not None:
            if not isinstance(start, datetime.datetime) or not isinstance(end, datetime.datetime):
                elog.critical('ERROR ExchangeItem.getDates2: Could not fetch date time from range because the "start" and/or "endtimes" are not valued datetime objects.')
                sPrint('Could not fetch date time from range because the "start" and/or "endtimes" are not valued datetime objects.', MessageType.CRITICAL)
                return 0, None

            st = self._nearest(self.__times2, start, 'left')
            et = self._nearest(self.__times2, end, 'right') + 1
            times = [(idx, self.__times2[idx]) for idx in range(st, et)]

            if ndarray:
                return numpy.array(times)
            else:
                return times

        elif isinstance(timevalue, datetime.datetime):
            idx = self._nearest(self.__times2, timevalue, 'left')
            if len(self.__times2) and idx <= len(self.__times2):
                return idx, self.__times2[idx]
            else:
                return 0, None

        else: # return all known values
            times = [(idx, self.__times2[idx]) for idx in range(0, len(self.__times2))]

            if ndarray:
                return numpy.array(times)
            else:
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

    def id(self):
        return self.__id

    def type(self):
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

    def _nearest(self, array, time, direction='left'):
        """
        get the nearst datetime in list
        :param array: sorted numpy array of datetimes
        :param time: desired datetime
        :param direction: the bisect direction.
        :return: list index
        """
        lst = list(array)
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
