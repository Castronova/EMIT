__author__ = 'tonycastronova'

import stdlib
import wrappers
from wrappers import base
from suds.client import Client
from utilities import geometry

class Wrapper(base.BaseWrapper):


    def __init__(self, args):
        super(Wrapper, self).__init__(self)

        self.args = args

        wsdl = self.args['wsdl']
        network = self.args['network']
        variable = '%s:%s' % (network, self.args['variable'])
        site = '%s:%s'%(network, self.args['site'])
        start = self.args['start'].strftime('%Y-%m-%dT%H:%M:%S')
        end = self.args['end'].strftime('%Y-%m-%dT%H:%M:%S')

        # connect to the server
        client = Client(wsdl)

        # get data
        queryInfo, timeSeries = client.service.GetValuesObject(site, variable, start, end)

        label, series = timeSeries

        # grab the first timeseries only
        ts = series[0]

        sourceInfo = ts['sourceInfo']
        variable = ts['variable']
        values = ts['values'][0]

        variableName = variable['variableName']
        unitName = variable['unit']['unitName']
        unitType = variable['unit']['unitType']
        unitAbbreviation = variable['unit']['unitAbbreviation']
        siteDescription = sourceInfo['siteName']
        geolocation_x = sourceInfo['geoLocation']['geogLocation']['longitude']
        geolocation_y = sourceInfo['geoLocation']['geogLocation']['latitude']
        geolocation_z = sourceInfo['elevation_m']

        # build unit
        unit = stdlib.Unit()
        unit.UnitName(unitName)
        unit.UnitAbbreviation(unitAbbreviation)
        unit.UnitTypeCV(unitType)

        # build variable
        var = stdlib.Variable()
        var.VariableNameCV(variableName)
        var.VariableDefinition(' ')

        # build geometry
        wkt = 'POINT(%s %s %s)' % (geolocation_x, geolocation_y, geolocation_z)
        geom = geometry.fromWKT(wkt)

        # build output exchange items
        oei = stdlib.ExchangeItem(name = variableName,
                                  desc = siteDescription,
                                  geometry= geom,
                                  unit= unit,
                                  variable= var,
                                  type= stdlib.ExchangeItemType.OUTPUT,
                                  # srs_epsg= ''
                                  )

        qualityControlLevelId = values['qualityControlLevel'][0]['qualityControlLevelCode']
        qualityControlLevelDef = values['qualityControlLevel'][0]['definition']
        qualityControlLevelExp = values['qualityControlLevel'][0]['explanation']

        dates = []
        vals = []
        # set data values
        for value in values.value:

            vals.append(float(value.value))
            dates.append(value._dateTime)

        oei.setValues2(values=vals, timevalue=dates)

        # set output
        self.outputs(oei)

        # set component metadata
        self.description(siteDescription)
        self.name(variableName)
        self.simulation_start(start)
        self.simulation_end(end)

    def prepare(self):
        self.status(stdlib.Status.READY)
        
    def type(self):
        return wrappers.Types().WOF

    def run(self,inputs):
        # set the status to finished
        self.status(stdlib.Status.FINISHED)

    def finish(self):
        self.status(stdlib.Status.FINISHED)